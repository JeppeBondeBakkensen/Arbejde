import pandas as pd
import re

from config import (
    STANDARDIZATION_SUBSTITUTIONS,
    STANDARDIZATIONS,
    TS_UPDATES,
    HOURLY_COLUMNS,
    CATEGORIES_TO_BE_REMOVE,
    DESIRED_ORDER2,
)
# ---------------------------
# Simple Functions
# ---------------------------
def filter_negative_counts(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only rows with non-negative TOTAL values
    return df[df['TOTAL'] >= 0].reset_index(drop=True)


def reorder_columns(df: pd.DataFrame, desired_order: list) -> pd.DataFrame:
    # Assumes all desired_order columns exist in df
    return df[desired_order]


def rename_categories(df: pd.DataFrame, rename_dict: dict) -> pd.DataFrame:
    # Standardize and rename values in the KATEGORI column
    df["KATEGORI"] = df["KATEGORI"].str.strip().str.upper()
    df["KATEGORI"] = df["KATEGORI"].replace(rename_dict)
    return df


def remove_categories(df: pd.DataFrame, categories_be_to_remove: list = CATEGORIES_TO_BE_REMOVE) -> pd.DataFrame:
    # Remove rows where KATEGORI is in the excluded list
    return df[~df["KATEGORI"].isin(categories_be_to_remove)]


def concat_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    # Concatenate two dataframes and reset the index
    df_combined = pd.concat([df1, df2], ignore_index=True)
    return df_combined


def total(df: pd.DataFrame) -> pd.DataFrame:
    # Sum all hourly columns into a new TOTAL column (assumes HOURLY_COLUMNS is defined)
    df[HOURLY_COLUMNS] = df[HOURLY_COLUMNS].apply(pd.to_numeric, errors='coerce').fillna(0)
    df["TOTAL"] = df[HOURLY_COLUMNS].sum(axis=1)
    return df

# ---------------------------
# Cleaning Functions
# ---------------------------

def clean_ts(df: pd.DataFrame) -> pd.DataFrame:
    # Remove rows where TS is -1 or missing (NaN), then sort by TS and ÅR
    cleaned_df = df[df["TS"] != -1].copy()
    cleaned_df = cleaned_df.dropna(subset=['TS'])  
    return cleaned_df.sort_values(by=['TS', 'ÅR'])


def extract_husnummer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Extract numbers from VEJNAVN into HUSNUMMER and clean VEJNAVN of numbers and extra spaces
    all_numbers = df['VEJNAVN'].apply(lambda x: re.findall(r'\d+', str(x)))
    df['VEJNAVN'] = df['VEJNAVN'].str.replace(r'\d+', '', regex=True).str.strip().str.replace(r'\s+', ' ', regex=True)
    df['HUSNUMMER'] = all_numbers.apply(lambda nums: ', '.join(nums) if nums else None)
    return df


def standardize_abbreviations(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize whitespace and apply regex-based standardizations from dictionary
    df["VEJNAVN"] = df["VEJNAVN"].fillna("").str.replace(r'\s+', ' ', regex=True).str.strip()
    for pattern, replacement in STANDARDIZATION_SUBSTITUTIONS.items():
        df["VEJNAVN"] = df["VEJNAVN"].str.replace(pattern, replacement, flags=re.IGNORECASE, regex=True)
    df["VEJNAVN"] = df["VEJNAVN"].str.replace(r'\s+', ' ', regex=True).str.strip()
    return df


def batch_standardize_location_descriptions(df: pd.DataFrame, standardizations: dict = STANDARDIZATIONS) -> pd.DataFrame:
    # Override location descriptions field-wise for specific TS values
    for ts, fields in standardizations.items():
        for field, value in fields.items():
            df.loc[df['TS'] == ts, field] = value
    return df


def split_vejnavn_beskrivelse(df: pd.DataFrame) -> pd.DataFrame:
    # Splits VEJNAVN into VEJNAVN (cleaned) and BESKRIVELSE based on pattern

    pattern = re.compile(r"^([A-ZÆØÅÉÜÖ'.\s\d]+)(.*)$")
    
    def split_func(vejnavn: str):
        try:
            text = str(vejnavn).strip()
        except AttributeError:
            return vejnavn, ""
        match = pattern.match(text)
        if match:
            return match.group(1).strip().upper(), match.group(2).strip()
        return vejnavn, ""

    split_data = df['VEJNAVN'].apply(lambda x: pd.Series(split_func(x)))
    df['VEJNAVN'] = split_data[0]

    # Insert BESKRIVELSE next to HUSNUMMER if it exists
    if 'HUSNUMMER' in df.columns:
        pos = df.columns.get_loc('HUSNUMMER')
        df.insert(pos + 1, 'BESKRIVELSE', split_data[1])
    else:
        df['BESKRIVELSE'] = split_data[1]

    return df


def rename_cykler_categories(df: pd.DataFrame, required: dict, disallowed: dict) -> pd.DataFrame:
    updated = []

    # Rename categories to 'CYKLER' if required categories exist and no disallowed ones are present for each TS+DATO group
    for (ts, dato), group in df.groupby(["TS", "DATO"]):
        cats = set(group["KATEGORI"].unique())
        if required & cats and not disallowed & cats:
            mask = df.index.isin(group.index) & df["KATEGORI"].isin(required)
            df.loc[mask, "KATEGORI"] = "CYKLER"
            updated.append((ts, group["ÅR"].iloc[0], group["VEJNAVN"].iloc[0]))

    return df

# ---------------------------
# Merging and Augmentation Functions
# ---------------------------

def add_tællestedstype(df: pd.DataFrame, station_df: pd.DataFrame) -> pd.DataFrame:
    # Validate expected columns
    if not all(col in station_df.columns for col in ['t_nr', 'wkb_geometry']):
        raise ValueError("station_df must contain 't_nr' and 'wkb_geometry' columns.")

    # Standardize naming and format
    station_df = station_df.rename(columns={"taellested_type": "TÆLLESTEDSTYPE"})
    station_df["TÆLLESTEDSTYPE"] = station_df["TÆLLESTEDSTYPE"].astype(str).str.strip().str.upper()

    # Extract X/Y coordinates from WKT POINT format
    coords = station_df['wkb_geometry'].str.extract(r'POINT \(([\d.]+) ([\d.]+)\)')
    station_df['Y-KOORDINAT'] = pd.to_numeric(coords[0], errors='coerce')
    station_df['X-KOORDINAT'] = pd.to_numeric(coords[1], errors='coerce')

    # Merge station data into traffic data
    merged_df = df.merge(
        station_df[['t_nr', 'TÆLLESTEDSTYPE', 'X-KOORDINAT', 'Y-KOORDINAT']],
        left_on='TS',
        right_on='t_nr',
        how='left'
    ).drop(columns=['t_nr'])

    # Default missing TÆLLESTEDSTYPE based on TS coverage across years
    ts_year_counts = merged_df.groupby('TS')['ÅR'].nunique().to_dict()
    merged_df['TÆLLESTEDSTYPE'] = merged_df['TÆLLESTEDSTYPE'].fillna(
        merged_df['TS'].map(lambda ts: "ANDRE FASTE TÆLLINGER" if ts_year_counts.get(ts, 0) >= 10 else "ANDRE TÆLLINGER")
    )

    return merged_df



def update_coordinates(df: pd.DataFrame, ts_updates: dict = TS_UPDATES) -> pd.DataFrame:
    # Ensure valid input
    if not isinstance(ts_updates, dict):
        raise TypeError("ts_updates must be a dictionary.")

    # Convert dict to DataFrame
    ts_updates_df = pd.DataFrame.from_dict(ts_updates, orient='index').reset_index()
    ts_updates_df.rename(columns={'index': 'TS'}, inplace=True)

    # Validate that updated columns exist in original df
    update_columns = [col for col in ts_updates_df.columns if col != 'TS']
    if not all(col in df.columns for col in update_columns):
        missing_cols = [col for col in update_columns if col not in df.columns]
        raise ValueError(f"The following columns are missing in the main DataFrame: {missing_cols}")

    # Merge updates into main df, prefer update values
    updated_df = df.merge(ts_updates_df, on='TS', how='left', suffixes=('', '_update'))

    for col in update_columns:
        if f"{col}_update" in updated_df.columns:
            updated_df[col] = updated_df[f"{col}_update"].combine_first(updated_df[col])
            updated_df.drop(columns=[f"{col}_update"], inplace=True)

    return updated_df



def format_date_column(df: pd.DataFrame, year_col: str = 'ÅR', date_col: str = 'DATO') -> pd.DataFrame:
    # Expect year and date columns in string/number format (e.g. "2023", "0301")

    if year_col not in df.columns or date_col not in df.columns:
        raise ValueError(f"Columns '{year_col}' and '{date_col}' must exist in the DataFrame.")

    # Normalize date formats and fill zeroes
    df[year_col] = df[year_col].astype(str).str.split('.').str[0]
    df[date_col] = df[date_col].astype(str).str.split('.').str[0].str.zfill(4)

    # Build full date string and format to YYYY-MM-DD
    df['DATO'] = pd.to_datetime(
        df[year_col] + "-" + df[date_col].str[:2] + "-" + df[date_col].str[2:],
        format="%Y-%m-%d",
        errors='coerce'
    )

    df['DATO'] = df['DATO'].dt.strftime('%Y-%m-%d')

    df['DATO'] = pd.to_datetime(df['DATO'], errors='coerce')

    # For each (TS, ÅR) group, find the first date and filter the rows accordingly
    df = (
        df
        .groupby(['TS', 'ÅR'])
        .apply(lambda g: g[g['DATO'] == g['DATO'].min()])
        .reset_index(drop=True)
    )
    return df




def merge_categories(df: pd.DataFrame, rename_dict: dict = None) -> pd.DataFrame:
    df = df.copy()

    # Apply renaming before aggregation
    df = rename_categories(df, rename_dict)

    # Ensure numeric count columns are ready to be summed
    antal_cols = [col for col in df.columns if col.startswith('ANTAL') or col.startswith('TOTAL')]
    df[antal_cols] = df[antal_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    group_keys = ['TS', 'DATO', 'KATEGORI']
    other_cols = [col for col in df.columns if col not in group_keys + antal_cols]

    grouped = df.groupby(group_keys, as_index=False)

    # Sum counts, take first for other fields (e.g. metadata)
    merged_df = grouped.agg({**{col: 'sum' for col in antal_cols},
                             **{col: 'first' for col in other_cols}})

    merged_df = merged_df[DESIRED_ORDER2]
    merged_df = merged_df.sort_values(by=['TS', 'ÅR'], ascending=True, na_position='last')

    return merged_df



def ÅDT_and_HDT(df: pd.DataFrame) -> pd.DataFrame:
    # Compute ÅDT and HDT estimates based on multipliers per KATEGORI type

    df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce').fillna(0)
    df[HOURLY_COLUMNS] = df[HOURLY_COLUMNS].apply(pd.to_numeric, errors='coerce').fillna(0)

    multipliers = {
        "MOTERTRAFIK I ALT": (1.17, 1.31),
        "CYKLER I ALT": (1.03, 1.22),
        "FODGÆNGERE I ALT": (1.17, 1.21)
    }

    for category, (multiplier_adt, multiplier_hdt) in multipliers.items():
        adt_column = f"{category} ÅDT"
        hdt_column = f"{category} HDT"

        # Use str.contains as a category membership check
        df[adt_column] = (df["TOTAL"] * multiplier_adt * df["KATEGORI"].str.contains(category, na=False)).round(-2).astype(int)
        df[hdt_column] = (df["TOTAL"] * multiplier_hdt * df["KATEGORI"].str.contains(category, na=False)).round(-2).astype(int)

    return df




