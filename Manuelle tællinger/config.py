import pandas as pd
import re

# ---------------------------
# Input file paths
# ---------------------------

INPUT_FILE = 'Output_files/0_inputfile.csv'
STATION_INFO_FILE = 'Tællestationer/tællestationer_0.csv'
MANUELLE_TILFØJELSER = "Manuelle_tilføjelser/manuelle_tilføjelser.csv"
AMGAGERMOTERVEJEN = "Manuelle_tilføjelser/amagermotervejen.csv"

# ---------------------------
# Output file paths
# ---------------------------

OUTPUT_FILE_CONCAT_DF = "Output_files/1_concat_DF.csv"
OUTPUT_FILE_CLEANED_TS = "Output_files/2_cleaned_TS.csv"
OUTPUT_FILE_VEJNAVN_HUSNUMMER = "Output_files/3_vejnavn_og_husnummer.csv"
OUTPUT_FILE_STANDARDIZED_ABBREVIATIONS = "Output_files/4_standardized_abbreviations.csv"
OUTPUT_FILE_CLEANED_VEJNAVNE = "Output_files/5_cleaned_vejnavne.csv"
OUTPUT_FILE_SPLIT_VEJNAVN = "Output_files/6_split_vejnavn_beskrivelse.csv"
OUTPUT_FILE_TÆLLESTEDTYPE = "Output_files/7_tilføj_tællestedstype.csv"
OUTPUT_FILE_COORDINATES = "Output_files/8_tilføje_koordinater.csv"
OUTPUT_FILE_FIXED_DATO = "Output_files/9_fixed_dato_format.csv"
OUTPUT_FILE_TOTAL_COLUMN = "Output_files/10_total_column.csv"
OUTPUT_FILE_FILTERED_TOTALS = "Output_files/11_filtered_totals.csv"
OUTPUT_FILE_REORDER_COLUMNS = "Output_files/12_reorder_columns.csv"
OUTPUT_FILE_RENAMED_CATEGORIES = "Output_files/13_renamed_categories.csv"
OUTPPUT_FILE_CONTROL_OF_CYKLER_I_ALT = "Output_files/14_control_of_cykler_i_alt.csv"
OUTPUT_FILE_REMOVE_CATEGORIES = "Output_files/15_remove_categories.csv"
OUTPUT_FILE_LAG0 = "Output_files/16_lag0.csv"

OUTPUT_FILE_MERGED_CATEGORIES = "Output_files/17_merged_categories.csv"
OUTPUT_FILE_RENAMED_CATEGORIES_PART2 = "Output_files/18_renamed_categories_part2.csv"
OUTPUT_FILE_MERGED_CATEGORIES_PART2 = "Output_files/19_merged_categories_part2.csv"
OUTPUT_FILE_CYKLER_CATEGORIES = "Output_files/20_cykler_categories.csv"
OUTPUT_FILE_RENAMED_CATEGORIES_PART3 = "Output_files/21_renamed_categories_part3.csv"
OUTPUT_FILE_LAG1 = "Output_files/22_lag1.csv"

OUTPUT_FILE_RENAMED_CATEGORIES_PART4 = "Output_files/23_renamed_categories_part4.csv"
OUTPUT_FILE_MERGED_CATEGORIES_PART3 = "Output_files/24_merged_categories_part3.csv"
OUTPUT_LAG2 = "Output_files/25_lag2.csv"

OUTPUT_FILE_RENAMED_CATEGORIES_PART5 = "Output_files/26_renamed_categories_part5.csv"
OUTPUT_FILE_MERGED_CATEGORIES_PART4 = "Output_files/27_merged_categories_part4.csv"
OUTPUT_FILE_RENAMED_CATEGORIES_PART6 = "Output_files/28_renamed_categories_part6.csv"
OUTPUT_FILE_REORDER_COLUMNS2 = "Output_files/29_reorder_columns2.csv"
OUTPUT_FILE_AMAGEREMOTORVEJEN = "Output_files/30_amagermotorvejen.csv"
OUTPUT_FILE_ÅDT_AND_HDT = "Output_files/31_ÅDT_and_HDT.csv"
OUTPUT_LAG3 = "Output_files/32_lag3.csv"



# ---------------------------
# Dictionary for standardizing abbreviations in the VEJNAVN column
# ---------------------------

STANDARDIZATION_SUBSTITUTIONS = {
    r"\bnord vest for\b": " nv.f. ",
    r"\bsyde vest for\b": " sv.f. ",
    r"\bsyde øst for\b": " sø.f. ",
    r"\bsydevest for\b": " sv.f. ",
    r"\bsydeøst for\b": " sø.f. ",
    r"\bsyd vest for\b": " sv.f. ",
    r"\bnord øst for\b": " nø.f. ",
    r"\bsyd øst for\b": " sø.f. ",
    r"\bnordvest for\b": " nv.f. ",
    r"\bsydvest for\b": " sv.f. ",
    r"\bsydøst for\b": " sø.f. ",
    r"\bnord for\b": " n.f. ",
    r"\bsyd for\b": " s.f. ",
    r"\bvest for\b": " v.f. ",
    r"\bøst for\b": " ø.f. ",
    r"\bsyv\.f\.\b": " sv.f. ",
    r"Andre faste tællestationer": "",
    r"andre faste tællestationer": "",
    r"\(ud for husnr\. \)": "",
    r"ud for husnr\.": "",
    r"\(husnr\. \)": "",
    r"\(": "",
    r"\)": "",
    r",": " ",
    r"/": " ",
    r"ENSRETTET": " (ensrettet)",
    r"- ensrettet": " (ensrettet)",
    r"-ensrettet": " (ensrettet)",
    r"- ENSRETTET": " (ensrettet)",
    r"-ENSRETTET": " (ensrettet)",
}


# ---------------------------
# Batch standardizations for location descriptions
# ---------------------------

STANDARDIZATIONS = {
    1: {"VEJNAVN": "H.C. ANDERSEN BOULEVARD sø.f. Jarmers Plads"},
    3: {"VEJNAVN": "BREDGADE n.f. Kongens Nytorv (ensrettet)"},
    4: {"VEJNAVN": "CHRISTIAN IV'S BRO s.f. Niels Juels gade"},
    5: {"VEJNAVN": "DRONNING LOUISES BRO"},
    6: {"VEJNAVN": "KAMPMANNSGADE ud for søerne"},
    7: {"VEJNAVN": "ELLEBJERGVEJ ø.f. Poppelstykket"},
    8: {"VEJNAVN": "ENGLANDSVEJ n.f. Følfodvej"},
    9: {"VEJNAVN": "FARVERGADE nø.f. Rådhuspladsen (ensrettet)"},
    11: {"VEJNAVN": "FREDERIKSHOLMS KANAL nv.f. Stormgade"},
    12: {"VEJNAVN": "FREDERIKSBORGGADE sø.f. Søtorvet"},
    13: {"VEJNAVN": "FREDERIKSBORGVEJ s.f. Gladsaxevej"},
    14: {"VEJNAVN": "FREDERIKSSUNDSVEJ v.f. Mørkhøjvej"},
    16: {"VEJNAVN": "GL. KØGE LANDEVEJ s.f. Vigerslevvej"},
    17: {"VEJNAVN": "GOTHERSGADE sø.f. Søtorvet"},
    18: {"VEJNAVN": "GRØNDALS PARKVEJ n.f. Peter Bangs Vej"},
    19: {"VEJNAVN": "GYLDENLØVESGADE ud for Søpavillonen"},
    20: {"VEJNAVN": "HARESKOVVEJ nv.f. Ruten (Hillerødmotorvejen)"},
    21: {"VEJNAVN": "HILLERØDGADE v.f. Borups Allé"},
    22: {"VEJNAVN": "ISTEDGADE nø.f. Absalonsgade"},
    23: {"VEJNAVN": "JAGTVEJ sv.f. Nørrebrogade"},
    24: {"VEJNAVN": "JYLLINGEVEJ v.f. Tudskærsvej"},
    25: {"VEJNAVN": "KALVEBOD BRYGGE sv.f. Bernstorffsgade"},
    26: {"VEJNAVN": "KNIPPELSBRO"},
    27: {"VEJNAVN": "KRISTEN BERNIKOWS GADE nv.f. Østergade (ensrettet)"},
    29: {"VEJNAVN": "LANGEBRO"},
    31: {"VEJNAVN": "LYNGBYVEJ n.f. Emdrupvej (Helsingørmotorvejen)"},
    32: {"VEJNAVN": "NØRRE ALLÉ s.f. Universitetsparken"},
    33: {"VEJNAVN": "NØRREGADE sø.f. Nørre Voldgade"},
    36: {"VEJNAVN": "ROSKILDEVEJ s.f. Damhussøen"},
    37: {"VEJNAVN": "SJÆLLANDSBROEN ø.f. Sluseholmen"},
    40: {"VEJNAVN": "SLOTSHERRENSVEJ v.f. Islev station"},
    41: {"VEJNAVN": "STORE KONGENSGADE n.f. Kgs. Nytorv (ensrettet)"},
    42: {"VEJNAVN": "STRANDBOULEVARDEN n.f. Classensgade"},
    43: {"VEJNAVN": "STRANDVEJEN s.f. Tuborgvej"},
    44: {"VEJNAVN": "SØLVGADE nv.f. Sølvtorvet (ensrettet)"},
    45: {"VEJNAVN": "SØNDERKÆR s.f. Holbækmotorvejen"},
    46: {"VEJNAVN": "TAGENSVEJ sø.f. Tuborgvej"},
    48: {"VEJNAVN": "TUBORGVEJ sv.f. Bispebjerg Parkallé"},
    49: {"VEJNAVN": "TUBORGVEJ sv.f. Lundedalsvej"},
    52: {"VEJNAVN": "VESTERBROGADE v.f. Rådhuspladsen"},
    53: {"VEJNAVN": "VESTER FARIMAGSGADE n.f. Ved Vesterport"},
    54: {"VEJNAVN": "VIGERSLEV ALLÉ ø.f. Toftegårds plads"},
    55: {"VEJNAVN": "VIGERSLEV ALLÉ sv.f. Vigerslevvej"},
    56: {"VEJNAVN": "VIGERSLEVVEJ n.f. Langagervej"},
    57: {"VEJNAVN": "ØSTBANEGADE n.f. Classensgade (ensrettet)"},
    58: {"VEJNAVN": "ØSTER ALLÉ ø.f. Nørre Allé"},
    60: {"VEJNAVN": "ØSTER SØGADE nø.f. Gothersgade"},
    61: {"VEJNAVN": "ÅBOULEVARD nv.f. Tømrergade"},
    62: {"VEJNAVN": "AMAGERBROGADE s.f. Adriansvej"},
    63: {"VEJNAVN": "AMAGER STRANDVEJ s.f. Hedegårdsvej"},
    65: {"VEJNAVN": "DAG HAMMARSKJÖLDS ALLÉ sø.f. Øster Farimagsgade"},
    67: {"VEJNAVN": "ENGHAVEVEJ n.f. P. Knudsens Gade"},
    68: {"VEJNAVN": "FOLKE BERNADOTTES ALLÉ nø.f. Oslo Plads"},
    69: {"VEJNAVN": "FREDENSBRO ved Sortedamssøen"},
    70: {"VEJNAVN": "GRØNNEMOSE ALLÉ v.f. Moseskellet"},
    71: {"VEJNAVN": "HORSEBAKKEN n.f. Mosesvinget"},
    72: {"VEJNAVN": "INGERSLEVSGADE sø.f. Tietgensgade"},
    73: {"VEJNAVN": "ISLEVHUSVEJ sv.f. Kildeløbeet"},
    74: {"VEJNAVN": "KASTRUPVEJ s.f. Beckersvej"},
    75: {"VEJNAVN": "KONGELUNDSVEJ n.f. Floridavej"},
    76: {"VEJNAVN": "KRONPRINSESSEGADE n.f. Gothersgade (ensrettet)"},
    78: {"VEJNAVN": "MØRKHØJVEJ n.f. Frederikssundsvej"},
    79: {"VEJNAVN": "RYGÅRDS ALLÉ s.f. Lundeskovsvej"},
    80: {"VEJNAVN": "RYVANGS ALLÉ s.f. Callisensvej"},
    81: {"VEJNAVN": "SUMATRAVEJ n.f. Hedegårdsvej"},
    82: {"VEJNAVN": "SVANEMØLLEVEJ s.f. Callisensvej"},
    84: {"VEJNAVN": "SØLVGADE v.f. Øster Voldgade"},
    86: {"VEJNAVN": "TORVEGADE n.f. Christnas Møllers Plads"},
    87: {"VEJNAVN": "UNIVERSITETSPARKEN sø.f. Jagtvej"},
    90: {"VEJNAVN": "ØSTER FARIGMAGSGADE nø.f. Gothersgade"},
    91: {"VEJNAVN": "ØSTER VOLDGADE s.f. Sølvgade"},
    92: {"VEJNAVN": "AMAGER BOULEVARD nv.f. Amagerbrogade"},
    93: {"VEJNAVN": "AMAGERBROGADE nordvest for Amager Boulevard"},
    109: {"VEJNAVN": "DYBBØLSBRO"},
    113: {"VEJNAVN": "FREDERIKSBERGGADE nø.f. Rådhuspladsen (ensrettet)"},
    117: {"VEJNAVN": "FREDERIKSSUNDSVEJ ø.f. Frederiksborgvej"},
    120: {"VEJNAVN": "FREDERIKSSUNDSVEJ ø.f. Krabbesholmvej"},
    121: {"VEJNAVN": "FÆLLEDVEJ nø.f. Nørrebrogade"},
    122: {"VEJNAVN": "GAMMEL KONGEVEJ vest for Stenosgade"},
    123: {"VEJNAVN": "GAMMEL KØGE LANDEVEJ s.f. Toftegårds Plads"},
    127: {"VEJNAVN": "GOTHERSGADE v.f. Kgs. Nytorv (ensrettet)"},
    129: {"VEJNAVN": "BRYGGEBROEN cykel- og gangbro"},
    132: {"VEJNAVN": "HILLERØDGADE v.f. Nattergalevej"},
    138: {"VEJNAVN": "HULGÅRDSVEJ n.f. Hillerødgade"},
    150: {"VEJNAVN": "LILLE KONGENSGADE v.f. Kgs. Nytorv (ensrettet)"},
    151: {"VEJNAVN": "LYGTEN s.f. Drejervej"},
    157: {"VEJNAVN": "NYHAVNSBROEN sv.f. Toldbodgade"},
    161: {"VEJNAVN": "ÅBUEN cykel- og gangbro"},
    166: {"VEJNAVN": "NØRREBROGADE nv.f. Jagtvej"},
    170: {"VEJNAVN": "NØRRE SØGADE sv.f. Vendersgade"},
    171: {"VEJNAVN": "PETER BANGS VEJ n.f. Roskildevej"},
    176: {"VEJNAVN": "REBILDVEJ sv.f. Dybensdalsvej"},
    176: {"VEJNAVN": "SANKT HANS GADE sø.f. Skt. Hans Torv"},
    184: {"VEJNAVN": "SLOTSHERRENSVEJ nv.f. Jyllingevej"},
    194: {"VEJNAVN": "STRANDVEJEN s.f. Callisensvej"},
    195: {"VEJNAVN": "STRANDVÆNGET ud for Roklubberne"},
    202: {"VEJNAVN": "TIETGENSBROEN"},
    203: {"VEJNAVN": "TOFTEGÅRDSBROEN"},
    207: {"VEJNAVN": "TUBORGVEJ v.f. Esthersvej"},
    210: {"VEJNAVN": "VALBY LANGGADE ø.f. Nakskovvej"},
    211: {"VEJNAVN": "VALBY LANGGADE v.f. Vestervang"},
    212: {"VEJNAVN": "VEJLANDS ALLÉ ø.f. Røde Mellemvej"},
    217: {"VEJNAVN": "VESTERGADE nø.f. Rådhuspladsen"},
    218: {"VEJNAVN": "VESTER VOLDGADE nv.f. Rådhuspladsen"},
    219: {"VEJNAVN": "VESTER VOLDGADE nv.f. Rådhuspladsen"},
    221: {"VEJNAVN": "VIGERSLEV ALLÉ v.f. Enghavevej"},
    227: {"VEJNAVN": "VINGÅRDSSTRÆDE sv.f. Kgs Nytorv"},
    228: {"VEJNAVN": "ØRESUNDSVEJ ø.f. Amagerbrogade"},
    229: {"VEJNAVN": "VESTERGADE nø.f. Rådhuspladsen"},
    234: {"VEJNAVN": "ØSTER FARIMAGSGADE sv.f. Lille Trianglen"},
    235: {"VEJNAVN": "ØSTERGADE v.f. Kgs Nytorv"},
    236: {"VEJNAVN": "ØSTER FARIMAGSGADE sv.f. Lille Triangel"},
    237: {"VEJNAVN": "ØSTER SØGADE sv.f. Lille Triangel"},
    240: {"VEJNAVN": "ÅLEKISTEVEJ nv.f. Peter Bangs Vej"},
    241: {"VEJNAVN": "ÅLEKISTEVEJ s.f. Slotsherrensvej"},
    242: {"VEJNAVN": "ÅLHOLMVEJ n.f. Roskildevej"},
    245: {"VEJNAVN": "AMAGER FÆLLEDVEJ s.f. Sundholmsvej"},
    255: {"VEJNAVN": "BLEGDAMSVEJ sv.f. Øster alle"},
    258: {"VEJNAVN": "CLASSENSGADE ø.f. Østerbrogade"},
    270: {"VEJNAVN": "GOTHERSGADE ø.f. Nørre Voldgade"},
    275: {"VEJNAVN": "HAMLETSGADE nø.f. Fenrisgade"},
    276: {"VEJNAVN": "HAMMERICHSGADE sv.f. H.C. Andersens Boulevard"},
    297: {"VEJNAVN": "GOTHERSGADE ø.f. Nørre Voldgade"},
    298: {"VEJNAVN": "LYRSKOVGADE ø.f. Vesterfælledvej"},
    300: {"VEJNAVN": "LØNGANGSSTRÆDE nø.f. Vester Voldgade (ensrettet)"},
    310: {"VEJNAVN": "PRINSESSEGADE sv.f. Burmeistergade"},
    321: {"VEJNAVN": "SANKT PEDERS STRÆDE nø.f. Vester Voldgade"},
    332: {"VEJNAVN": "STUDIESTRÆDE nø.f. Rådhuspladsen (ensrettet)"},
    341: {"VEJNAVN": "UPLANDSGADE nv.f. Prags Boulevard"},
    363: {"VEJNAVN": "ISLANDS BRYGGE s.f. Langebro"},
    376: {"VEJNAVN": "CHRISTIANS BRYGGE nø.f. Vester Voldgade"},
    377: {"VEJNAVN": "FIOLSTRÆDE sø.f. Nørre Voldgade"},
    379: {"VEJNAVN": "NY KONGENSGADE nø.f. Vester Voldgade"},
    380: {"VEJNAVN": "NY VESTERGADE nø.f. Vester Voldgade"},
    384: {"VEJNAVN": "LANDLYSTVEJ v.f. Engdals Allé"},
    392: {"VEJNAVN": "LANDLYSTVEJ v.f. Engdals Allé"},
    397: {"VEJNAVN": "BLEGDAMSVEJ sv.f. Fælledvej"},
    414: {"VEJNAVN": "HUSUMVEJ nv.f. Tølløsevej"},
    416: {"VEJNAVN": "LANGELINJEBROEN"},
    418: {"VEJNAVN": "NØRRE ALLÉ s.f. Tagensvej"},
    476: {"VEJNAVN": "CHRISTIANS BRYGGE nø.f Vester Voldgade"},
    478: {"VEJNAVN": "JAGTVEJ ø.f. Vibenshus Runddel"},
    479: {"VEJNAVN": "GAMMEL JERNBANEVEJ ø.f. Toftegårds Allé"},
    482: {"VEJNAVN": "GAMMEL JERNBANEVEJ ø.f. Toftegård Allé"},
    487: {"VEJNAVN": "HOLBÆKMOTORVEJ v.f. Sønderkær"},
    491: {"VEJNAVN": "WEBERSGADE nv.f. Øster Farimagsgade (ensrettet)"},
    492: {"VEJNAVN": "SUNDHOLMSVEJ ø.f. Amagerfælledvej"},
    496: {"VEJNAVN": "BORUPS ALLÉ nv.f. Hulgårdsvej"},
    500: {"VEJNAVN": "NORDRE FASANVEJ n.f. Hillerødgade"},
    501: {"VEJNAVN": "PETER BANGS VEJ v.f. Ålstrupvej"},
    503: {"VEJNAVN": "ÅKANDEVEJ n.f. Gadelandet"},
    515: {"VEJNAVN": "BISPEENGBUEN n.f. Kronprinsesse Sofies Vej"},
    525: {"VEJNAVN": "HØJBRO"},
    526: {"VEJNAVN": "CHR IX'S GADE sø.f. Gothersgade"},
    538: {"VEJNAVN": "BORGMESTER CHRSTANSENS GADE sø.f. K.M.Klausens Gade"},
    542: {"VEJNAVN": "LANDEMÆRKET s.f. Gothersgade"},
    544: {"VEJNAVN": "HØJE GLADSAXEVEJ nø.f. Hareskovvej"},
    546: {"VEJNAVN": "PEDER LYKKESVEJ ø.f. Vatnavej"},
    547: {"VEJNAVN": "PRINSESSE CHRISTINES VEJ sv.f. Amagerbrogade"},
    548: {"VEJNAVN": "GREISVEJ ø.f. Amagerbrogade"},
    549: {"VEJNAVN": "GODTHÅBSVEJ sø.f. Grøndals Parkvej"},
    551: {"VEJNAVN": "AMAGERBROGADE sø.f. Hollænderdybet"},
    552: {"VEJNAVN": "ØSTRIGSGADE sø.f. Holmbladsgade"},
    553: {"VEJNAVN": "KASTRUPVEJ sø.f. Øresundsvej"},
    554: {"VEJNAVN": "LOSSEPLADSVEJ s.f. Rundholtsvej"},
    557: {"VEJNAVN": "BLÅGÅRDSGADE nø.f. Åboulevard"},
    559: {"VEJNAVN": "GRIFFENFELDSGADE nø.f. Rantzausgade"},
    560: {"VEJNAVN": "GRIFFENFELDSGADE sv.f. Nørrebrogade"},
    561: {"VEJNAVN": "KAPELVEJ nø.f. Rantzausgade"},
    562: {"VEJNAVN": "KAPELVEJ sv.f. Nørrebrogade"},
    566: {"VEJNAVN": "VEJLANDS VEJ v.f. Kongelundsvej"},
    569: {"VEJNAVN": "THORSHAVNSGADE sv.f. Amager Boulevard"},
    576: {"VEJNAVN": "KRONPRINSESSEGADE"},
    577: {"VEJNAVN": "NØRRE FARIMAGSGADE s.f. Ahlefeldtsgade"},
    578: {"VEJNAVN": "FENGERSVEJ s.f. hyhøjgårdsvej"},
    579: {"VEJNAVN": "FENGERSVEJ n.f. Vigerslev"},    
    580: {"VEJNAVN": "JERNBANE ALLÉ nv.f. Grøndals Parkvej"},
    581: {"VEJNAVN": "JERNBANE ALLÉ sø.f. Jyllingevej"},
    583: {"VEJNAVN": "RANDBØLVEJ nv.f. Grøndals Parkvej"},
    586: {"VEJNAVN": "VALBY LANGGADE v.f. Toftegårds Allé"},
    587: {"VEJNAVN": "VALBY LANGGADE v.f. Gåsebækvej"},
    597: {"VEJNAVN": "NYGÅRDSVEJ v.f. Fanøgade"},
    601: {"VEJNAVN": "HALMTORVET nø.f. Gasværksvej (ensrettet)"},
    602: {"VEJNAVN": "ISTEDGADE nø.f. Gasværksvej"},
    603: {"VEJNAVN": "ISTEVESTERBROGADE sv.f. Stenosgade"},
    604: {"VEJNAVN": "AMAGERFÆLLEDVEJ s.f. Peter Vedels Gade"},
    605: {"VEJNAVN": "AMAGERFÆLLEDVEJ nø.f. Borgmester christiansens gade"},
    606: {"VEJNAVN": "LERSØ PARKALLÉ"},
    608: {"VEJNAVN": "STRANDBOULEVARDEN ø.f. Østerbrogade"},
    609: {"VEJNAVN": "TUBORGVEJ v.f. Rymarksvej"},
    614: {"VEJNAVN": "TAGENSVEJ nv.f. Frederik Bajers Plads"},
    617: {"VEJNAVN": "JAGTVEJ n.f. Universitetsparken"},
    623: {"VEJNAVN": "ØRESUNDSVEJ ø.f. Strandlodsvej"},
    625: {"VEJNAVN": "STORE KONGENSGADE n.f. Jens Kofods Gade (ensrettet)"},
    626: {"VEJNAVN": "FREDERIKSSUNDSVEJ nv.f. Åkandevej"},
    628: {"VEJNAVN": "ÅKANDEVEJ nø.f. Frederikssundsvej"},
    630: {"VEJNAVN": "NORDRE FRIHAVNSGADE nø.f. Trianglen"},
    631: {"VEJNAVN": "NØRRE VOLDGADE s.f. Frederiksborggade"},
    635: {"VEJNAVN": "HILLERØDGADE ø.f. Nordre Fasanvej"},
    636: {"VEJNAVN": "NORDRE FASANVEJ s.f. Hillerødsgade"},
    638: {"VEJNAVN": "JYLLINGEVEJ v.f. Slotsherrensvej"},
    639: {"VEJNAVN": "SALLINGVEJ sø.f. Jyllingevej"},
    641: {"VEJNAVN": "RETORTVEJ s.f. Vigerslev Allé"},
    643: {"VEJNAVN": "ENGLANDSVEJ nø.f. Sundholmsvej"},
    644: {"VEJNAVN": "ARTILLERIVEJ n.f. Njalsgade"},
    646: {"VEJNAVN": "NJALSGADE sø.f. Leifsgade"},
    647: {"VEJNAVN": "NJALSGADE sø.f. Artillerivej"},
    650: {"VEJNAVN": "HOVEDVAGTSGADE v.f. Kgs. Nytorv (ensrettet)"},
    652: {"VEJNAVN": "GRØNNEGADE s.f. Gothersgade (ensrettet)"},
    653: {"VEJNAVN": "STORE REGNEGADE s.f. Gothersgade (ensrettet)"},
    661: {"VEJNAVN": "RUTEN v.f. Hareskovvej"},
    663: {"VEJNAVN": "JERNBANE ALLÉ n.f. Vanløse Alle"},
    664: {"VEJNAVN": "JERNBANE ALLÉ s.f. Vanløse Allé"},
    665: {"VEJNAVN": "VANLØSE ALLÉ ø.f. Jernbane Allé"},
    667: {"VEJNAVN": "HOLMBLADSGADE v.f. Vermlandsgade"},
    669: {"VEJNAVN": "VERMLANDSGADE n.f. Holmbladsgade"},
    674: {"VEJNAVN": "IRLANDSVEJ s.f. Sundbyvestervej"},
    675: {"VEJNAVN": "IRLANDSVEJ s.f. Sundbyvestervej"},
    676: {"VEJNAVN": "SUNDBYVESTERVEJ ø.f. Irlandsvej"},
    677: {"VEJNAVN": "FREDERIKSBORGVEJ s.f. Bispebjerg Torv"},
    678: {"VEJNAVN": "LERSØ PARKALLÉ s.f. Tuborgvej"},
    679: {"VEJNAVN": "TAGENSVEJ sø.f. Bispebjerg Torv"},
    680: {"VEJNAVN": "UTTERSLEVVEJ n.f. Hareskovvej"},
    683: {"VEJNAVN": "SCANDIAGADE nø.f. Sydhavnsgade"},
    684: {"VEJNAVN": "VESTERFÆLLEDVEJ n.f. Ny Carlsberg Vej"},
    687: {"VEJNAVN": "STRANDØRE ø.f Strandvejen"},
    688: {"VEJNAVN": "AMAGERFÆLLEDVEJ n.f. Amager Boulevard"},
    691: {"VEJNAVN": "KLØVERMARKSVEJ ø.f. Raffinaderivej"},
    695: {"VEJNAVN": "HYLTEBRO sv.f. Nørrebrogade"},
    696: {"VEJNAVN": "STOREGÅRDSVEJ nø.f. Frederikssundsvej"},
    697: {"VEJNAVN": "BERNSTORFFSGADE nv.f. Kalvebod Brygge"},
    699: {"VEJNAVN": "VEJLANDS ALLÉ ø.f. Artillerivej"},
    700: {"VEJNAVN": "VEJLANDS ALLÉ"},
    702: {"VEJNAVN": "SKT. ANNÆ PLADS ø.f. Amaliegade"},
    703: {"VEJNAVN": "ANNEXSTRÆDE s.f. Valby Langgade"},
    705: {"VEJNAVN": "GLASVEJ sv.f. Frederiksborgvej"},
    708: {"VEJNAVN": "ØRESUNDSMOTORVEJEN s.f. Ørestad Station"},
    709: {"VEJNAVN": "AMAGERMOTORVEJEN på broen over Avedøre Holme"},
    710: {"VEJNAVN": "MARBJERGVEJ s.f. Frederikssundsvej"},
    711: {"VEJNAVN": "KONGELUNDSVEJ n.f. Slusevej"},
    713: {"VEJNAVN": "SØNDRE FASANVEJ s.f. Roskildevej"},
    716: {"VEJNAVN": "ROVSINGSGADE nø.f. Tagensvej"},
    717: {"VEJNAVN": "KALKBRÆNDERIHAVNSGADE n.f. Indiakaj"},
    724: {"VEJNAVN": "GYLDENLØVESGADE sø.f. Nørre Søgade"},
    725: {"VEJNAVN": "TAGENSVEJ sø.f. Rovsingsgade"},
    726: {"VEJNAVN": "BERNSTORFFSGADE nv.f. Tietgensgade"},
    731: {"VEJNAVN": "ØSTER VOLDGADE nø.f. Sølvgade"},
    733: {"VEJNAVN": "AMAGERMOTORVEJEN vestlig ben ved Vejlands Allé"},
    734: {"VEJNAVN": "AMAGERMOTORVEJEN østlig ben ved Vejlands Allé"},
    735: {"VEJNAVN": "AMAGERMOTORVEJEN s.f. Vejlands Allé"},
    736: {"VEJNAVN": "VEJLANDS ALLÉ mellem motorvejsafgreningerne"},
    737: {"VEJNAVN": "VEJLANDS ALLÉ v.f. Lossepladsvej"},
    738: {"VEJNAVN": "CENTER BOULEVARD s.f. Vejlands Allé"},
    739: {"VEJNAVN": "KLAKSVIGSGADE s.f. Amager Boulevard"},
    751: {"VEJNAVN": "TEGLVÆRKSBROEN n.f. Sluseholmen"},
    757: {"VEJNAVN": "MØLLEGADE nø.f. Nørrebrogade (ensrettet)"},
    804: {"VEJNAVN": "GASVÆRKSVEJ nv.f Istedgade"},
    834: {"VEJNAVN": "TEATERPASSAGEN VESTERBROGADE"},
    882: {"VEJNAVN": "JAGTVEJ sv.f. for Ydunsgade (miljømålestationen)"},
    884: {"VEJNAVN": "STI ø.f. Artillerivej"},
    901: {"VEJNAVN": "H.C. ØRSTEDSVEJ n.f. Niels Ebbesensvej"},
    902: {"VEJNAVN": "VESTERBROGADE ø.f. Pile Allé"},
    904: {"VEJNAVN": "GAMMEL KONGEVEJ ø.f. Allegade"},
    908: {"VEJNAVN": "FREDERIKGSBERG ALLÉ ø.f. Pile Allé"},
    909: {"VEJNAVN": "FINSENSVEJ nv.f. Sønderjyllands Allé"},
    910: {"VEJNAVN": "C.F. RICHS VEJ"},
    912: {"VEJNAVN": "NORDRE FASANVEJ n.f. Stær Johansens Vej"},
    913: {"VEJNAVN": "FALKONER ALLÉ s.f. Dronning Olgas vej"},
    914: {"VEJNAVN": " NYELANDSVEJ v.f. Falkonér Allé"},
    975: {"VEJNAVN": "CYKELSLANGEN"},
    985: {"VEJNAVN": "CYKELSLANGEN"},
    995: {"VEJNAVN": "CYKELBRO OVER LYNGBYVEJ"},
    996: {"VEJNAVN": "CYKELBRO OVER NORDHAVNSVEJEN"},
    4006: {"VEJNAVN": "NY KONGENSGADE nø.f. Vester Voldgade"},
    7102: {"VEJNAVN": "STRØGET ØST ved Østergade"},
    7103: {"VEJNAVN": "STRØGET ved vimmelskaftet"},
    7005: {"VEJNAVN": "DRONNING LOUISES BRO"},
    7167: {"VEJNAVN": "DAMHUSDÆMNINGEN albertslundruten"},
    8006: {"VEJNAVN": "CYKELRUTEN sv. f. Tagensvej"},
    9001: {"VEJNAVN": "KØDBODERNE ø.f. Skelbækgade"},
    9753: {"VEJNAVN": "BAGGESENSGADE nv.f. Blågårdsgade"},
    9756: {"VEJNAVN": "PEBLINGE DOSSERING"},
    9757: {"VEJNAVN": "PRINSESSE CHARLOTTES GADE mellem Meinungsgade og Frederik VII's Gade"},
    9758: {"VEJNAVN": "SLOTSGADE sv.f. Nørrebrogade mod Nørrebrogade (ensrettet)"},
    9871: {"VEJNAVN": "INDREHAVNSBROEN"},
    9872: {"VEJNAVN": "INDREHAVNSBROEN"},
    9873: {"VEJNAVN": "TRANGRAVSBROEN nordlige ben"},
    10029: {"VEJNAVN": "DRONNINGENSGADE nø. (ensrettet)"},
    10030: {"VEJNAVN": "OVERGADEN OVEN VANDET sv. (ensrettet)"},
    10096: {"VEJNAVN": "STRANDGADE ved Inderhavnsbroen"},
    10104: {"VEJNAVN": "WILDERSGADE nø. (ensrettet)"},
    10103: {"VEJNAVN": "TORDENSKJOLDSGADE nv. (ensrettet)"},
    10138: {"VEJNAVN": "TØJHUSGADE"},
    10166: {"VEJNAVN": "LILLE LANGEBRO"},
    10208: {"VEJNAVN": "FREDERIKSHOLMS KANAL sø.f. Tøjhusgade"},
    10217: {"VEJNAVN": "BORUPS ALLÉ v.f. Jagtvej"},
    10240: {"VEJNAVN": "CHRISTIAN IX'S GADE s.f. Gothersgade"},
    10276: {"VEJNAVN": "FÆRGEHAVNSVEJ n.f. Skudehavnsvej"},
}


# ---------------------------
# Add corrdinates to the TÆLLESTEDSTYPE missing coordinates
# ---------------------------

TS_UPDATES = {
    2: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69700352085171, "Y-KOORDINAT": 12.525406805828496},
    10: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69368858699946, "Y-KOORDINAT": 12.566712406281297},
    15: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.673497864199305, "Y-KOORDINAT": 12.554647881137168},
    22: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.669790164434886, "Y-KOORDINAT": 12.555315332141001},
    28: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.678951302272836, "Y-KOORDINAT": 12.579674513206506},
    30: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.71286739326837, "Y-KOORDINAT": 12.560278499040306},
    35: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.672822387615966, "Y-KOORDINAT": 12.47407675921467},
    38: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68107489660179, "Y-KOORDINAT": 12.576439072704565},
    39: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67892702745572, "Y-KOORDINAT": 12.573558695809002},
    47: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67367647677459, "Y-KOORDINAT": 12.589294066718761},
    50: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.65706271588264, "Y-KOORDINAT": 12.551745451738324},
    51: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68560506030741, "Y-KOORDINAT": 12.564912790351476},
    66: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67317753327398, "Y-KOORDINAT": 12.573577952087167},
    77: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.71552861511205, "Y-KOORDINAT": 12.552831207274917},
    85: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66811517557008, "Y-KOORDINAT": 12.55625587560994},
    88: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67260776557409, "Y-KOORDINAT": 12.553724111726025},
    89: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67748124731885, "Y-KOORDINAT": 12.554347863131284},
    93: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66541866761392, "Y-KOORDINAT": 12.599398901946794},
    95: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66656730494468, "Y-KOORDINAT": 12.59489166827586},
    96: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67575216180026, "Y-KOORDINAT": 12.568274815406207},
    97: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67563116703658, "Y-KOORDINAT": 12.56758816994113},
    100: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.674500047817304, "Y-KOORDINAT": 12.564384941716995},
    102: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68808092332209, "Y-KOORDINAT": 12.560113906182217},
    104: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.646606424353486, "Y-KOORDINAT": 12.541747685614846},
    106: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67593151148888, "Y-KOORDINAT": 12.584684754222772},
    110: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.689148637672346, "Y-KOORDINAT": 12.55738934529801},
    114: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70197529332133, "Y-KOORDINAT": 12.533385395162188},
    118: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70197529332135, "Y-KOORDINAT": 12.533385395162180},
    124: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.655776810532906, "Y-KOORDINAT": 12.512213981322427},
    133: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.694739107258975, "Y-KOORDINAT": 12.510161424118387},
    135: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69106402481068, "Y-KOORDINAT": 12.515489760956738},
    142: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.706398464115246, "Y-KOORDINAT": 12.562473662500565},
    143: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67671640157204, "Y-KOORDINAT": 12.568424095303019},
    148: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.675758855128784, "Y-KOORDINAT": 12.570633374061625},
    149: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.678849176400334, "Y-KOORDINAT": 12.58561018809148},
    156: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68080463739827, "Y-KOORDINAT": 12.587644283030233},
    159: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70538836726552, "Y-KOORDINAT": 12.563008212695346},
    160: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68805022709392, "Y-KOORDINAT": 12.560145241759134},
    167: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70049282146988, "Y-KOORDINAT": 12.539132629391334},
    173: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69348708934847, "Y-KOORDINAT": 12.495876451629574},
    181: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69348708934847, "Y-KOORDINAT": 12.495876451629574},
    182: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.690850398667216, "Y-KOORDINAT": 12.561260012126986},
    185: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.6976603838025, "Y-KOORDINAT": 12.480796905544626},
    186: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69767826779342, "Y-KOORDINAT": 12.539132629391334},
    188: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.689180691184646, "Y-KOORDINAT": 12.557274260496598},
    197: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64669573059999, "Y-KOORDINAT": 12.541991505855705},
    201: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.708318107371845, "Y-KOORDINAT": 12.539867049598065},
    207: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.72765665072438, "Y-KOORDINAT": 12.566617277328518},
    219: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67511903524132, "Y-KOORDINAT": 12.571773871659955},
    227: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67886860239812, "Y-KOORDINAT": 12.585662313424514},
    229: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69951056317702, "Y-KOORDINAT": 12.5363661176974},
    235: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67940143089582, "Y-KOORDINAT": 12.582654027592381},
    236: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68663855322803, "Y-KOORDINAT": 12.565822319718901},
    271: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64608435068647, "Y-KOORDINAT": 12.625349005909268},
    273: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.695643449521576, "Y-KOORDINAT": 12.553386326770944},
    296: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69249938547779, "Y-KOORDINAT": 12.538629608718406},
    297: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70670526216602, "Y-KOORDINAT": 12.56275574023203},
    310: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.654997868992176, "Y-KOORDINAT": 12.593944597997034},
    321: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67855523624317, "Y-KOORDINAT": 12.566293768736342},
    375: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68234618133666, "Y-KOORDINAT": 12.582153159204646},
    376: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.671630933848036, "Y-KOORDINAT": 12.578633982489924},
    378: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68094239565567, "Y-KOORDINAT": 12.568941289909151},
    379: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67333637914879, "Y-KOORDINAT": 12.575131702825876},
    380: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.673928265591236, "Y-KOORDINAT": 12.574113996412116},
    382: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.680078893611956, "Y-KOORDINAT": 12.56776855311956},
    383: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.684332074798554, "Y-KOORDINAT": 12.57297585446686},
    385: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66443916611311, "Y-KOORDINAT": 12.516179414006478},
    391: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66492401542144, "Y-KOORDINAT": 12.478571364643775},
    416: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.670358645744905, "Y-KOORDINAT": 12.578784064817839},
    470: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.72132509203993, "Y-KOORDINAT": 12.574880047749005},
    476: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70153226208004, "Y-KOORDINAT": 12.519508827201985},
    480: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64197465801249, "Y-KOORDINAT": 12.589216886912272},
    494: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66650434377111, "Y-KOORDINAT": 12.595041632077086},
    496: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66686792686445, "Y-KOORDINAT": 12.593295844704407},
    498: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68778953844097, "Y-KOORDINAT": 12.501101241822886},
    499: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.695344954374114, "Y-KOORDINAT": 12.527955991705845},
    502: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.72966854901359, "Y-KOORDINAT": 12.56848975289208},
    504: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.65464661089965, "Y-KOORDINAT": 12.59919318953654},
    505: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.678617743841265, "Y-KOORDINAT": 12.566329123315704},
    506: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67683004605032, "Y-KOORDINAT": 12.582629498624472},
    507: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67993060681668, "Y-KOORDINAT": 12.586402158086864},
    509: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69768783282057, "Y-KOORDINAT": 12.55269266285221},
    510: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.692712790636996, "Y-KOORDINAT": 12.551429298628639},
    512: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.692612121756234, "Y-KOORDINAT": 12.536305335042584},
    513: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.692612121756234, "Y-KOORDINAT": 12.536305335042584},
    514: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.679761324503076, "Y-KOORDINAT": 12.57927072408564},
    517: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.679687188616796, "Y-KOORDINAT": 12.574619082315934},
    518: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67780621787695, "Y-KOORDINAT": 12.576865816245752},
    519: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.651748315754894, "Y-KOORDINAT": 12.593045536131902},
    520: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.65098664486773, "Y-KOORDINAT": 12.502959417993244},
    521: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69850550404572, "Y-KOORDINAT": 12.523570546111822},
    522: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.71683019135573, "Y-KOORDINAT": 12.538527962849479},
    523: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.666472789144, "Y-KOORDINAT": 12.598553904141303},
    524: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66645012757935, "Y-KOORDINAT": 12.598594083540855},
    526: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.6827747725265, "Y-KOORDINAT": 12.580754448683805},
    527: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.681438181753215, "Y-KOORDINAT": 12.581106151073318},
    530: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69457283314211, "Y-KOORDINAT": 12.509840008623843},
    531: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68522218836566, "Y-KOORDINAT": 12.550395546460562},
    532: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70888614365448, "Y-KOORDINAT": 12.510553508943186},
    533: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.692807794649525, "Y-KOORDINAT": 12.568141969662411},
    534: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67631512363948, "Y-KOORDINAT": 12.57331844315621},
    535: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.670143896011034, "Y-KOORDINAT": 12.539560238921442},
    536: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.670293079266685, "Y-KOORDINAT": 12.539391938330356},
    537: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66180027410543, "Y-KOORDINAT": 12.603286093187577},
    538: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.648777260609485, "Y-KOORDINAT": 12.535565544239919},
    539: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.71030607112456, "Y-KOORDINAT": 12.536083142285088},
    540: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.694476083934745, "Y-KOORDINAT": 12.509925839306973},
    541: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.72073379267144, "Y-KOORDINAT": 12.556184469894715},
    543: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.682799512757875, "Y-KOORDINAT": 12.577771356896385},
    545: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.6537349372051, "Y-KOORDINAT": 12.604055525371997},
    546: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67031728155131, "Y-KOORDINAT": 12.539220276964087},
    547: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.65423553648251, "Y-KOORDINAT": 12.610743425372045},
    548: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64391309518653, "Y-KOORDINAT": 12.615464778610754},
    550: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.662185009972376, "Y-KOORDINAT": 12.631622793755248},
    555: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68257858238502, "Y-KOORDINAT": 12.557197675951492},
    556: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68320531946198, "Y-KOORDINAT": 12.55623101088988},
    557: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.684263032082704, "Y-KOORDINAT": 12.555355485301574},
    558: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68498836620067, "Y-KOORDINAT": 12.553419425653791},
    559: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68560171558478, "Y-KOORDINAT": 12.552188444168692},
    560: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68979415371742, "Y-KOORDINAT": 12.555692170299096},
    561: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68603147436452, "Y-KOORDINAT": 12.55105063474266},
    562: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69050338665616, "Y-KOORDINAT": 12.554554913747562},
    563: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69017775171553, "Y-KOORDINAT": 12.555158044710907},
    564: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.687379472490186, "Y-KOORDINAT": 12.56226293454662},
    565: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.687192417245306, "Y-KOORDINAT": 12.562488076849487},
    566: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64208955926989, "Y-KOORDINAT": 12.589304659893688},
    567: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66298916201312, "Y-KOORDINAT": 12.59385768961506},
    568: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66431561237554, "Y-KOORDINAT": 12.583913360521505},
    570: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.690588050828396, "Y-KOORDINAT": 12.554554913747559},
    571: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68759654013877, "Y-KOORDINAT": 12.555560195530465},
    572: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69057051271092, "Y-KOORDINAT": 12.554570868842326},
    573: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69026706951935, "Y-KOORDINAT": 12.555015979433199},
    574: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68125078798876, "Y-KOORDINAT": 12.560374213838683},
    575: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.69148858709734, "Y-KOORDINAT": 12.587919187404127},
    578: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66349728226457, "Y-KOORDINAT": 12.507180183114395},
    579: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.6610310292193, "Y-KOORDINAT": 12.504635679183206},
    580: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.687765578272256, "Y-KOORDINAT": 12.500609347030316},
    581: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.6924355171254, "Y-KOORDINAT": 12.486429093993966},
    582: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68780563328273, "Y-KOORDINAT": 12.50073838590096},
    583: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68821400265911, "Y-KOORDINAT": 12.501162913678185},
    584: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64822417107616, "Y-KOORDINAT": 12.528924069951506},
    585: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66435749802169, "Y-KOORDINAT": 12.516002390800594},
    587: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66639748675471, "Y-KOORDINAT": 12.506711800232948},
    588: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66901008088107, "Y-KOORDINAT": 12.506787776523488},
    589: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66731425603772, "Y-KOORDINAT": 12.506663523127157},
    590: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70106436966338, "Y-KOORDINAT": 12.539731892775409},
    591: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68559207093336, "Y-KOORDINAT": 12.552263180527838},
    599: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.65101373231064, "Y-KOORDINAT": 12.536601841849693},
    610: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.65343785617853, "Y-KOORDINAT": 12.493179890264175},
    611: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67265935628675, "Y-KOORDINAT": 12.557254397404822},
    612: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.673715175080154, "Y-KOORDINAT": 12.57233731387629},
    640: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68273610424327, "Y-KOORDINAT": 12.5806841098598},
    651: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68273910162856, "Y-KOORDINAT": 12.580657285272638},
    654: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.6841737467273, "Y-KOORDINAT": 12.575068852456036},
    655: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67882992753941, "Y-KOORDINAT": 12.585662759961512},
    656: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67553160039324, "Y-KOORDINAT": 12.575767511311524},
    657: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.676892351813, "Y-KOORDINAT": 12.582918055319187},
    658: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.677151917516184, "Y-KOORDINAT": 12.583743174775698},
    666: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68812973044711, "Y-KOORDINAT": 12.497009519618626},
    674: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64592204609383, "Y-KOORDINAT": 12.605528238199316},
    675: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.64592204609383, "Y-KOORDINAT": 12.605528238199316},
    707: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66394411181611, "Y-KOORDINAT": 12.542253051928789},
    727: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.67158257760781, "Y-KOORDINAT": 12.567872951496025},
    732: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.68758695625579, "Y-KOORDINAT": 12.57845715104822},
    3005: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.643814876667804, "Y-KOORDINAT": 12.615520731400707},
    7137: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.66399299714883, "Y-KOORDINAT": 12.560348816883248},
    9884: {"TÆLLESTEDSTYPE": "Andre faste tællinger", "X-KOORDINAT": 55.70819087189621, "Y-KOORDINAT": 12.539742685491689}
}


# ---------------------------
# List of hourly traffic count columns
# ---------------------------

HOURLY_COLUMNS = [
    "ANTAL 6-7", "ANTAL 7-8", "ANTAL 8-9", "ANTAL 9-10", 
    "ANTAL 10-11", "ANTAL 11-12", "ANTAL 12-13", "ANTAL 13-14", 
    "ANTAL 14-15", "ANTAL 15-16", "ANTAL 16-17", "ANTAL 17-18", 
    "ANTAL 18-19"
]

# ---------------------------
# Renname Categorys 
# ---------------------------

CATEGORIES_TO_BE_RENAMED = {

    # Personbiler
    "PERSONBILER + MOTORCYKL.": "PERSONBILER + MC",
    "PERSONBILER +MC": "PERSONBILER + MC",

    # A: LET TRAFIK I ALT
    "A: LET TRAFIK IALT": "A: LET TRAFIK I ALT",
    "A:LET TRAFIK I ALT": "A: LET TRAFIK I ALT",
    "A: LET MOTORTRAFIK I ALT": "A: LET TRAFIK I ALT",
    "LET TRAFIK": "A: LET MOTORTRAFIK I ALT",
    "A:LET TRAFIK IALT": "A: LET TRAFIK I ALT",
    "A: LET MOTORTRAFIK I ALT": "A: LET TRAFIK I ALT",
    "A: LET MOTORTRAFIK I ALT": "A: LET TRAFIK I ALT",
    "A: LET MOTORTRAFIK I ALT": "A: LET TRAFIK I ALT",
    
    # B: TUNG TRAFIK I ALT
    "TUNG TRAFIK": "B: TUNG TRAFIK I ALT",
    "B: TUNG TRAFIK IALT": "B: TUNG TRAFIK I ALT",
    "B: TUNG TRAFIK I ALT": "B: TUNG TRAFIK I ALT",

    # A+B: KØRETØJER I ALT
    "A+B: KØRETØJER IALT": "A+B: KØRETØJER I ALT",
    "KØRETØJER IALT": "A+B: KØRETØJER I ALT",
    "B:TUNG TRAFIK IALT": "B: TUNG TRAFIK I ALT",
    "A+B:KØRETØJER IALT": "A+B: KØRETØJER I ALT",
    "A+B: MOTORKØRETØJER I ALT": "A+B: KØRETØJER I ALT",
        "MOTORKØRETØJER I ALT": "A+B: KØRETØJER I ALT", 
    "KØRETØJER I ALT": "A+B: KØRETØJER I ALT",

    # CYKLER + KNALLERTER I ALT
    "CYKLER OG KNALLERTER I ALT": "CYKLER + KNALLERTER I ALT",

    # VAREVOGNE (MAX. 3,5 T)
    "VAREVOGE (UNDER 3,5 TON)": "VAREVOGNE (MAX. 3,5 T)",
    "VAREVOGNE (UNDER 3,5 TON)": "VAREVOGNE (MAX. 3,5 T)",
    "VAREVOGNE": "VAREVOGNE (MAX. 3,5 T)",
    "VAREVOGNE(MAX.3.5T)": "VAREVOGNE (MAX. 3,5 T)",

    # LASTBILER, 2 AKSLER
    "SOLOLASTBILER, 2 AKSLER": "LASTBILER, 2 AKSLER",
    "LASTBILER,2.AKSLER": "LASTBILER, 2 AKSLER",

    # LASTBILER, 3 AKSLER
    "SOLOLASTBILER, 3 AKSLER": "LASTBILER, 3 AKSLER",
    "LASTBILER,3.AKSLER": "LASTBILER, 3 AKSLER",

    # LASTBILER, 4 AKSLER
    "LASTBILER,4.AKSLER+": "LASTBILER, 4 AKSLER",
    "LASTBILER,4.AKSLER": "LASTBILER, 4 AKSLER",
    "LASTBILER 4+ AKSLER" : "LASTBILER, 4 AKSLER",
    "LASTBILER,4-HJULEDE": "LASTBILER, 4 AKSLER",
    "KØRETØJER 4 - FLERE AKSLER": "LASTBILER, 4 AKSLER",
    "LASTBILER, 4 - FL. AKSLER": "LASTBILER, 4 AKSLER",
    "LASTBILER, 4 - FLERE AKSLER": "LASTBILER, 4 AKSLER",
    "LASTBILER 4 - FLERE AKSLER": "LASTBILER, 4 AKSLER",

    # PERSONBILER + MC
    "PERSONB+MOTORCYKL." : "PERSONBILER + MC",
    "PERSONBILER + MOTORCYKLER": "PERSONBILER + MC",
    "PERSONBILER & MOTORCYKLER": "PERSONBILER + MC",
    "PERSONBILER OG MOTORCYKLER": "PERSONBILER + MC",

    # CYKLER + KNALLERTER
    "KNALLERTER+ CYKLER": "CYKLER + KNALLERTER",
    "CYKLER+KNALLERTER": "CYKLER + KNALLERTER",
    "KNALLERTER+CYKLER": "CYKLER + KNALLERTER",
    "CYKLER OG KNALLERTER": "CYKLER + KNALLERTER",

    # CYKLER + KNALLERTER I ALT
    "CYKLER + KNALLERTER  I ALT": "CYKLER + KNALLERTER I ALT",
    "CYKLER + KNALLERTER I ALT": "CYKLER + KNALLERTER I ALT",
    "CYKLER + KNALLERTER IALT": "CYKLER + KNALLERTER I ALT",
    "CYKLER IALT": "CYKLER + KNALLERTER I ALT",

    # KNALLERTER
    "KNALLERT": "KNALLERTER",
    # MOTERCYKLER
    "MOTORCYKLER,SOLO": "MOTORCYKLER",

    # LASTBILER, 2-3 AKSLER
    "LASTBILER 2-3 AKSLER": "LASTBILER, 2-3 AKSLER",

    # LASTBILER, 3+4 AKSLER + BUS
    "LASTBILER, 3 +4  AKSL. + BUS": "LASTBILER, 3+4 AKSLER + BUS",
    "LASTB. 3+4 AKS.+BUS.": "LASTBILER, 3+4 AKSLER + BUS",

    # LASTBILER, 3-4 AKSLER
    "LASTBILER,3+4.AKSLER": "LASTBILER, 3-4 AKSLER",
    "LASTBILER,3+4 AKSLER": "LASTBILER, 3-4 AKSLER",
    # FODGÆNGER - MÆND 
    "MÆND": "FODGÆNGERE - MÆND",

    # FODGÆNGER - KVINDER
    "KVINDER": "FODGÆNGERE - KVINDER",

    # FODGÆNGER - BARNEVOGNE
    "BARNEVOGN": "FODGÆNGER - BARNEVOGNE",

    # FODGÆNGER - LØBERE
    "LØBERE": "FODGÆNGER - LØBERE",
    # FODGÆNGER - BØRN U. 12 ÅR
    "BØRN U. 12 ÅR": "FODGÆNGER - BØRN U. 12 ÅR",
    "BØRN U. 12 ÅR OG BARNEVOGNE": "FODGÆNGER - BØRN U. 12 ÅR",
    "BØRN UNDER 12 ÅR": "FODGÆNGER - BØRN U. 12 ÅR",
    "BØRN UNDER 12 ÅR OG BARNEVOGNE": "FODGÆNGER - BØRN U. 12 ÅR",
    "FODGÆNGERE - BØRN U.12": "FODGÆNGER - BØRN U. 12 ÅR",
    "FODGÆNGERE - BØRN UNDER 12 ÅR": "FODGÆNGER - BØRN U. 12 ÅR",

    # TAXA
    "TAXI": "TAXA",

    # FODGÆNGERE - LØBEHJUL
    "FODGÆNGERE / LØBEHJUL": "FODGÆNGERE",

    # BØRN UNDER 12 PÅ EGEN CYKEL
    "BØRN UNDER 12 ÅR PÅ EGEN CYKEL": "BØRN UNDER 12 PÅ EGEN CYKEL",

    # FODGÆNGER - TRÆKKER MED CYKLE
    "TRÆKKER MED CYKLER": "FODGÆNGER - TRÆKKER MED CYKLER",
}

CATEGORIES_TO_BE_RENAMED2 = {
    # Pedestrians
    "FODGÆNGERE - KVINDER": "FODGÆNGERE",  
    
    # Bicycles
    "CYKLER MED 1 PERSON": "CYKLER",  
    "LADCYKEL MED 1 PERSON": "LADCYKLER", 
    
    # Personal vehicles
    "KØRETØJER": "PERSONBILER + MC",  
    "PERSONBILER, VAREVOGNE OG MOTORCYKLER": "PERSONBILER + MC", 
    
    # Public transport
    "CITY-BUSSER": "BUSSER",  
    "BUSSER I FAST RUTE": "BUSSER",  
    "OMNIBUSSER I FAST RUTE": "OMNIBUSSER",  
    "OMNIBUSSER I FAST RUTE": "OMNIBUSSER",
    "OMNIBUSSER I FAST RUTE 12,46": "OMNIBUSSER",  
    "SPORVOGNSTOG": "SPORVOGN",  
    
    # Trucks and heavy vehicles
    "SOLOLASTBILER > 3,5 T": "LASTBILER", 
    "SOLOLASTBILER, 3 - FLERE AKSLER": "LASTBILER", 
    "LASTBILER, 2-3 AKSLER": "LASTBILER", 
    "LASTBILER, 3-4 AKSLER": "LASTBILER",  
    "LASTBILER, 3-4 AKSLER + BUS": "LASTBILER",  
    "LASTBILER, 3+4 AKSLER + BUS": "LASTBILER",  
    "LASTBILER, 4 AKSLER": "LASTBILER",  
    "LASTBILER + BUSSER": "LASTBILER", 
    "BUSSER + STØRRE LASTBILER": "LASTBILER",  

    # Varevogne
    "VAREVOGNE (MAX. 3,5 T)": "VAREVOGNE",
    "VAREVOGNE (UNDER 3,5 TON)": "VAREVOGNE",
    "VAREVOGE (UNDER 3,5 TON)": "VAREVOGNE",
}

CATEGORIES_TO_BE_RENAMED3 = {
    "PERSONBILER": "PERSONBILER + MC",
    "CYKLER": "CYKLER + KNALLERTER",
    "OMNIBUSSER": "BUSSER",
    "LASTBILER, 4 - FLERE AKSLER": "LASTBILER",
    "CYKLER OG KNALLERTER": "CYKLER + KNALLERTER",
    "BUSSER OG LASTBILER": "LASTBILER",
    "LASTBILER OG BUSSER": "LASTBILER",
}

CATEGORIES_TO_BE_RENAMED4 = {
    "LASTBILER": "TUNG TRAFIK I ALT",
    "SPORVOGN": "TUNG TRAFIK I ALT",
    "BUSSER": "TUNG TRAFIK I ALT",
    "PERSONBILER + MC": "LET TRAFIK I ALT",
    "VAREVOGNE": "LET TRAFIK I ALT",
    "LADCYKLER": "CYKLER I ALT",
    "CYKLER + KNALLERTER": "CYKLER I ALT", 
    "FODGAENGERE": "FODGAENGERE I ALT",
}

CATEGORIES_TO_BE_RENAMED5 = {
    "TUNG TRAFIK I ALT": "LET TRAFIK I ALT"
}

CATEGORIES_TO_BE_RENAMED6 = {
    "LET TRAFIK I ALT": "MOTERTRAFIK I ALT",
}
# ---------------------------
# Remove Categories
# ---------------------------

CATEGORIES_TO_BE_REMOVE = [
    "ALT I ALT",
    "I ALT MOD NORDVEST",
    "I ALT MOD SYDØST",
    "CYKLER I ALT", 
    "I ALT MOD VEST",
    "I ALT MOD ØST",
    "I ALT MOD NØRREBRO",
    "I ALT MOD BYEN",
    "I ALT VESTLIG FORTOV",
    "I ALT SYDLIGE FORTOV",
    "I ALT NORDLIGE FORTOV",
    "TALTE I ALT", 
    "FODGÆNGERE + ANDET I ALT",
    "TALTE I ALT",
    "FODGÆNGERE I ALT",
    "I ALT MOD NORD",
    "I ALT MOD SYD",
    "I ALT ØSTLIG FORTOV",
    "I ALT VESTLIG FORTOV",
    "I ALT MOD BYEN",
    "I ALT IND PÅ LEGEPLADSEN",
    "I ALT LIGE HUSNR.-SIDE",
    "I ALT MOD",
    "I ALT MOD SYDVEST",
    "I ALT MOD FREDERIKSBERG",
    "I ALT MOD INDERHAVNSBROEN",
    "I ALT MOD NORDØST",
    "I ALT MOD RYVANGEN",
    "I ALT MOD STRANDGADE",
    "I ALT MOD SYDVEST",
    "I ALT PÅ NORDØSTLIGE FORTOV",
    "I ALT PÅ SYDVESTLIGE FORTOV",
    "I ALT UD FRA LEGEPLADSEN",
    "I ALT ULIGE HUSNR.-SIDE",
    "I ALT ULIGE HUSNR.SIDE",
    "TRAFIK IALT", 
    "I ALT MOD  SYDVEST", 
    "I ALT",
    "FODGÆNGERE IALT", 
    "FODGÆNGERE MOD NØRRE VOLD", 
    "FODGÆNGERE FRA NØRRE VOLD",
    "B: TUNG TRAFIK I ALT",
    "A: LET MOTORTRAFIK I ALT",
    "A: LET TRAFIK I ALT",
    "A+B: KØRETØJER I ALT",
    "CYKLER & KNALLERTER I ALT",
    "CYKLER + KNALLERTER I ALT",
    "LADCYKLER I ALT",
    "CYKLER + KNALLERTER + LADCYKLER",
    "CYKLER O.L. I ALT",
    "FODGÆNGERE + ANDET IALT",
    "FODGÆNGERE + LØBERE I ALT",
    "FODGÆNGERE + BARNEVOGNE I ALT",
    "I ALT MOD byen", 
    "I ALT MOD Nørrebro",
    "I Alt MOD",
    "I Alt MOD NORD",
    "I ALT MOD nordvest",
    "I ALT MOD sydøst",
    "I ALT MOD syd",
    "I ALT MOD nord"
]


# ---------------------------
# CATEGORIES TO BE MERGED
# ---------------------------

CATEGORIES_TO_BE_MERGED = {
    # Pedestrians (Fodgængere)
    "HERAF TIL S-TOG": "FODGÆNGERE",
    "HERAF FRA S-TOG": "FODGÆNGERE",
    "ANDET *)": "FODGÆNGERE",
    "*) ANDET: RULLESKØJTER, BARNEVOGN MED BARN M.V.": "FODGÆNGERE",
    "FODGÆNGER - LØBERE": "FODGÆNGERE",
    "BARNEVOGNE": "FODGÆNGERE",
    "FODGÆNGERE - MÆND": "FODGÆNGERE - KVINDER",
    "FODGÆNGER - BØRN U. 12 ÅR": "FODGÆNGERE - KVINDER",
    "FODGÆNGER - BARNEVOGNE": "FODGÆNGERE - KVINDER",
    "USPECIFIK": "FODGÆNGERE - KVINDER",
    "FODGÆNGER - TRÆKKER MED CYKLER": "FODGÆNGERE - KVINDER",

    # Bicycles (Cykler)
    "EL-CYKLER": "CYKLER MED 1 PERSON",
    "BØRN UNDER 12 PÅ EGEN CYKEL": "CYKLER MED 1 PERSON",
    "CYKLER MED 2 PERSONER": "CYKLER MED 1 PERSON",
    "CYKLER MED 3 PERSONER": "CYKLER MED 1 PERSON",
    "LADCYKEL MED 2 PERSONER": "LADCYKEL MED 1 PERSON",
    "LADCYKEL MED 3 PERSONER": "LADCYKEL MED 1 PERSON",
    "LADCYKEL MED 4+PERSONER": "LADCYKEL MED 1 PERSON",
    "TRUKNE CYKLER": "CYKLER",
    "CYKLER MOD ENSRETNING": "CYKLER + KNALLERTER",
    "EL-LØBEHJUL O.L.": "CYKLER + KNALLERTER",
    "CYKLER MOD ENSRETNINGEN": "CYKLER + KNALLERTER",

    # Cars and motorcycles
    "MOTORCYKLER,MED SIDEVOGN": "MOTORCYKLER",
    "MED CAMPINGVOGN": "PERSONBILER",
    "TAXA": "PERSONBILER",
    "KØRETØJER IND I P-HUS": "PERSONBILER + MC",
    "KØRETØJER UD AF P-HUS": "PERSONBILER + MC",

    # Buses
    "SAS OMNIBUSSER": "OMNIBUSSER I FAST RUTE",
    "OMNIBUSSER M.M.": "OMNIBUSSER I FAST RUTE",
    "OMNIBUSSER I FART 13,40": "OMNIBUSSER I FAST RUTE 12,46",
    "ANDRE BUSSER": "BUSSER I FAST RUTE",
    "ØVRIGE BUSSER": "BUSSER I FAST RUTE",

    # Trucks
    "LASTBILER, 2 AKSLER": "LASTBILER, 4 AKSLER",
    "LASTBILER, 3 AKSLER": "LASTBILER, 4 AKSLER",
    "LASTBILER,6-HJULEDE": "LASTBILER, 4 AKSLER",
    "LASTBILER,8-HJULEDE": "LASTBILER, 4 AKSLER",
    "ANDRE KØRETØJER": "LASTBILER, 4 AKSLER",
    "TANKVOGNE": "LASTBILER, 3-4 AKSLER",
    "STØRRE LASTBILER + BUS": "LASTBILER, 2-3 AKSLER",
    "LASTBILER MED SÆTTEVOGN": "SOLOLASTBILER > 3,5 T",
    "LASTBILER MED PÅHÆNG": "SOLOLASTBILER > 3,5 T",
    "SÆTTEVOGNSTOG": "SOLOLASTBILER > 3,5 T",
    "LASTBILER MED ANHÆNGER": "SOLOLASTBILER, 3 - FLERE AKSLER"
}

CATEGORIES_TO_BE_MERGED2 = {
    "MOTORCYKLER": "PERSONBILER",
    "KNALLERTER": "CYKLER",
    "LASTBILER 4+ AKSLER": "LASTBILER"
}

# ---------------------------
# Reorder columns 
# ---------------------------

DESIRED_ORDER1 = [
        'TS', 'VEJNAVN', 'BESKRIVELSE', 'HUSNUMMER', 'ÅR', 'DATO', 'RETNING', 'KATEGORI', "TÆLLESTEDSTYPE",
        'ANTAL 6-7', 'ANTAL 7-8', 'ANTAL 8-9', 'ANTAL 9-10', 'ANTAL 10-11', 'ANTAL 11-12',
        'ANTAL 12-13', 'ANTAL 13-14', 'ANTAL 14-15', 'ANTAL 15-16', 'ANTAL 16-17', 'ANTAL 17-18', 'ANTAL 18-19',
        'TOTAL', 'X-KOORDINAT', 'Y-KOORDINAT' 
    ]

DESIRED_ORDER2 = [
        'TS', 'VEJNAVN', 'BESKRIVELSE', 'HUSNUMMER', 'ÅR', 'DATO', 'KATEGORI', "TÆLLESTEDSTYPE",
        'ANTAL 6-7', 'ANTAL 7-8', 'ANTAL 8-9', 'ANTAL 9-10', 'ANTAL 10-11', 'ANTAL 11-12',
        'ANTAL 12-13', 'ANTAL 13-14', 'ANTAL 14-15', 'ANTAL 15-16', 'ANTAL 16-17', 'ANTAL 17-18', 'ANTAL 18-19',
        'TOTAL', 'X-KOORDINAT', 'Y-KOORDINAT' 
    ]

# ---------------------------
# Kepp I alt cykler if there is no cykler for a year 
# ---------------------------

REQUIRED = {
        "CYKLER + KNALLERTER I ALT",
        "CYKLER + KNALLERTER + LADCYKLER",
        "CYKLER & KNALLERTER I ALT",
        "CYKLER O.L. I ALT"
    }

DISALLOWED = {"CYKLER + KNALLERTER", "CYKLER", "CYKLER OG KNALLERTER"}


REQUIRED2 = {
        "CYKLER + KNALLERTER"
    }

DISALLOWED2 = {"CYKLER"}

# ---------------------------
# Remove years with more than one count 
# ---------------------------

