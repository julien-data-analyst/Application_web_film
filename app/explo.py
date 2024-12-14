#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024 - 14/12/2024
# Sujet : Nettoyage, préparation des données des films.
#################################################

# _This file contains the exploration, cleaning and preparation of the dataset "movies_complete.csv"._

##############################################################
# Première partie : importation + préparation des données des films
##############################################################
# Librairies used
import pandas as pd
import re

# Settings
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

def read_dataset(chemin:str) -> pd.DataFrame:
    """
    This function reads and loads a csv file as a pandas Dataframe.
    It returns a pandas dataframe.
    """
    data = pd.read_csv(chemin, sep=",", encoding="utf-8")
    return data


# apply the function to read the dataset
dataset = read_dataset("./data/movies_complete.csv")

print(f"There are {dataset.shape} lines and columns.")

# Percentage of missing data
percentage_missing = dataset.isnull().sum() * 100 / len(dataset)

#print(percentage_missing)

def convert_date(column:str, data:pd.DataFrame) -> pd.DataFrame:
    """
    This function converts a column in a DataFrame from object type to datetype.
    It returns a Dataframe with the corrected datetype column.
    """
    data[column] = pd.to_datetime(data[column])
    return data


dataset = convert_date("release_date", dataset)

def see_unique_values(column:str, data:pd.DataFrame) -> pd.DataFrame:
    """
    This function shows the unique values present in a given column
    """
    unique = data[column].unique()
    return pd.DataFrame(unique)

#print(see_unique_values("belongs_to_collection", dataset)[0:10])


#print(see_unique_values("spoken_languages", dataset)[0:10])

def get_link(column: str, data: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts URLs from a specified column in a DataFrame. 
    
    If a cell contains no URL or is null/NaN, it replaces the value with "Missing".
    
    Args:
        column (str): The name of the column containing the HTML-like strings.
        data (pd.DataFrame): The DataFrame from which to extract links.
    
    Returns:
        list: A list of extracted URLs or "Missing" for rows where no valid URL is found.
    """
    links = []
    pattern = r"https?://[^\s'\"]+"  # Regex to match URLs
    
    for l in data[column]:
        if pd.isnull(l):  # Check for null or NaN values
            links.append("Missing")
        else:
            match = re.search(pattern, l)  # Find the first match for the pattern
            if match:
                links.append(match.group())  # Append the matched link
            else:
                links.append("Missing")  # No link found, add "Missing"
    data["poster"] = links
    data = data.drop("poster_path", axis=1)
    return data

dataset = get_link("poster_path", dataset)

# Gérer les valeurs manquantes
def replace_na(data, col:list):
    data[col] = data[col].fillna(value="Missing")
    return data

# Appliquer sur les colonnes concernées
dataset = replace_na(dataset, ["belongs_to_collection", "director", "original_language"])

# Pour faciliter l'insertion des données
dataset["director"] = dataset["director"].str.strip()
dataset["collection"] = dataset["director"].str.strip()

def separate_and_expand(column: str, data: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a DataFrame and a column with delimited values, 
    and expands the delimited values into separate rows while retaining 
    the corresponding 'id' for each value.

    Parameters:
    column (str): The name of the column to expand.
    data (pd.DataFrame): The DataFrame containing the data.

    Returns:
    pd.DataFrame: A new DataFrame with two columns:
        - 'id': The unique identifier for each row in the original DataFrame.
        - <column>: Each separated value from the specified column.

    """
    # Initialize an empty list to hold the new rows
    expanded_rows = []

    # Iterate through the rows of the DataFrame
    #i=0
    for _, row in data.iterrows():
        # Get the values for the specified column, handling NaN cases
        values = row[column] if pd.notna(row[column]) else 'Missing'
        
        # Split the values by the delimiter "|" (if not 'Missing')
        values = values.split('|') if values != 'Missing' else ['Missing']
        
        # Create a row for each split value, retaining the 'id'
        for value in values:
                expanded_rows.append({'id': row['id'], column: value.strip()})
        
        #i+= 1
        #print(i)

    # Create a new DataFrame from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows)

    return expanded_df.drop_duplicates(keep="first") # Enlever les éventuels

# Pour le genre 
genre = separate_and_expand("genres", dataset)
print("Les dimensions du dataframe genre : ", genre.shape)
#print(genre)

# Pour la collection
collection = dataset[["id", "belongs_to_collection"]]
print("Les dimensions du dataframe collection : ", collection.shape) # Même nombre de lignes de données que pour le dataset donc c'est bon
#print(collection)

# La création du dictionnaire des languages pour original language
language_dict = {
    "Missing" : "Missing",
    "en": "English",
    "fr": "French",
    "zh": "Chinese",
    "it": "Italian",
    "fa": "Persian",
    "nl": "Dutch",
    "de": "German",
    "cn": "Chinese",
    "ar": "Arabic",
    "es": "Spanish",
    "ru": "Russian",
    "sv": "Swedish",
    "ja": "Japanese",
    "ko": "Korean",
    "sr": "Serbian",
    "bn": "Bengali",
    "he": "Hebrew",
    "pt": "Portuguese",
    "wo": "Wolof",
    "ro": "Romanian",
    "hu": "Hungarian",
    "cy": "Welsh",
    "vi": "Vietnamese",
    "cs": "Czech",
    "da": "Danish",
    "no": "Norwegian",
    "nb": "Norwegian Bokmål",
    "pl": "Polish",
    "el": "Greek",
    "sh": "Serbo-Croatian",
    "xx": "Missing", 
    "mk": "Macedonian",
    "bo": "Tibetan",
    "ca": "Catalan",
    "fi": "Finnish",
    "th": "Thai",
    "sk": "Slovak",
    "bs": "Bosnian",
    "hi": "Hindi",
    "tr": "Turkish",
    "is": "Icelandic",
    "ps": "Pashto",
    "ab": "Abkhazian",
    "eo": "Esperanto",
    "ka": "Georgian",
    "mn": "Mongolian",
    "bm": "Bambara",
    "zu": "Zulu",
    "uk": "Ukrainian",
    "af": "Afrikaans",
    "la": "Latin",
    "et": "Estonian",
    "ku": "Kurdish",
    "fy": "Frisian",
    "lv": "Latvian",
    "ta": "Tamil",
    "sl": "Slovenian",
    "tl": "Tagalog",
    "ur": "Urdu",
    "rw": "Kinyarwanda",
    "id": "Indonesian",
    "bg": "Bulgarian",
    "mr": "Marathi",
    "lt": "Lithuanian",
    "kk": "Kazakh",
    "ms": "Malay",
    "sq": "Albanian",
    "qu": "Quechua",
    "te": "Telugu",
    "am": "Amharic",
    "jv": "Javanese",
    "tg": "Tajik",
    "ml": "Malayalam",
    "hr": "Croatian",
    "lo": "Lao",
    "ay": "Aymara",
    "kn": "Kannada",
    "eu": "Basque",
    "ne": "Nepali",
    "pa": "Punjabi",
    "ky": "Kyrgyz",
    "gl": "Galician",
    "uz": "Uzbek",
    "sm": "Samoan",
    "mt": "Maltese",
    "hy": "Armenian",
    "iu": "Inuktitut",
    "lb": "Luxembourgish",
    "si": "Sinhalese",
}

# Création du dictionnaire pour les langues parlés (spoken languages)
dictionnaire_spoken_lang = {
    "Missing" : "Missing",
    "English" : "English",
    "Français" : "French",
    "Español" : "Spanish",
    "Deutsch" : "German",
    "Pусский" : "Russian",
    "Nederlands" : "Dutch",
    "广州话 / 廣州話" : "Cantonese / Guangzhou Dialect",
    "普通话" : "Mandarin",
    "Magyar" : "Hungarian",
    "shqip" : "Albanian",
    "Italiano" : "Italian",
    "한국어/조선말" : "Korean",
    "فارسی" : "Persian",
    "Dansk" : "Danois",
    "日本語" : "Japanese",
    "العربية" : "Arabic",
    "Hrvatski" : "Croate",
    "Bosanski" : "Bosnian",
    "Română"   : "Romanian",
    "Bahasa indonesia" : "Indonesian",
    "Bahasa melayu" : "Malay",
    "svenska" : "Swedish",
    "עִבְרִית" : "Hebrew",
    "Český" : "Czech",
    "Polski" : "Polish",
    "Gaeilge" : "Irish",
    "Norsk" : "Norwegian",
    "Slovenčina" :  "Slovakia",
    "Tiếng Việt" : "Vietnamese",
    "Português" : "Portuguese",
    "हिन्दी" : "Hindi",
    "Català" : "Catalan",
    "Íslenska" : "Iceland",
    "Afrikaans" : "Afrikaans",
    "Srpski" : "Serbian",
    "বাংলা" : "Bengali",
    "Wolof" : "Wolof",
    "Cymraeg" : "Welsh",
    "ภาษาไทย" : "Thai",
    "Latviešu" : "Latvian",
    "Kiswahili" : "Swahili",
    "български език" : "Bulgarian",
    "ελληνικά" : "Greek",
    "Türkçe" : "Turkish",
    "suomi" : "Finnish",
    "Esperanto" : "Esperanto",
    "Український" : "Ukrainian",
    "ქართული" : "Georgian",
    "Bokmål" : "Norwegian Bokmâl",
    "No Language" : "No Language", # Film muets
    "euskera" : "Basque",
    "Azərbaycan" : "Azerbaijan",
    "Malti" : "Maltese",
    "اردو" : "Urdu",
    "isiZulu" : "Zulu",
    "Bamanankan" : "Bambara",
    "پښتو" : 'Pashto',
    "Somali" : "Somali",
    "ਪੰਜਾਬੀ" : "Punjabi",
    "беларуская мова" : "Belarusian",
    "தமிழ்" : "Tamil",
    "Galego" : "Galician",
    "Kinyarwanda" : "Kinyarwanda",
    "қазақ" : "Khazakh",
    "Eesti" : "Estonian",
    "Lietuvikai" : "Lithuanians",
    "Slovenščina" : "Slovenian",
    "తెలుగు" : "Telugu",
    "Fulfulde" : "Fula",
    "ozbek" : "Uzbek",
    "Hausa" : "Hausa",
    "Latin" : "Latin",
    "Lietuvi\x9akai" : "Lithuanians"
}

def extract_languages(column: str, data: pd.DataFrame, dicto: dict, id: str) -> pd.DataFrame:
    """
    This function maps language codes in the specified column of a DataFrame
    to their full language names using a provided dictionary. It then returns 
    a DataFrame containing the 'id' column and the specified column with the 
    full language names.

    Parameters:
    column (str): The name of the column containing language codes to be mapped.
    data (pd.DataFrame): The DataFrame containing the data to be processed.
    dicto (dict): A dictionary mapping language codes to full language names.
    id (str) : nom de la colonne de l'id

    Returns:
    pd.DataFrame: A DataFrame containing only the 'id' column and the 
                   specified column with full language names.
    """
    # Map language codes to full language names using the provided dictionary
    data[column] = data[column].map(dicto)

    # Return the DataFrame containing only the 'id' column and the specified column
    return data[[id, column]]

original_language = extract_languages("original_language", dataset, language_dict, "id")
#print(original_language.columns)
#print(original_language[original_language["original_language"].isna()])
print("Les dimensions du dataframe original_language : ", original_language.shape)

spoken_language = separate_and_expand("spoken_languages", dataset)
spoken_language_trad = extract_languages("spoken_languages", spoken_language, dictionnaire_spoken_lang, "id")
#print(spoken_language_trad[spoken_language_trad["spoken_languages"].isna()])
print("Les dimensions du dataframe spoken_language_trad : ", spoken_language_trad.shape)
#print(spoken_language_trad.columns)

# Renommer les colonnes des deux dataframes sur les langages
original_language.columns = ["id", "language"]
spoken_language_trad.columns = ["id", "language"]

# Supprimer les éventuelles valeurs manquantes (????, ???, "" == NaN)
spoken_language_trad.dropna(inplace=True)

# Application de la séparation des listes de valeurs :
production = separate_and_expand("production_companies", dataset)
print("Les dimensions du dataframe production : ", production.shape)
#print(production)

director = dataset[["id", "director"]]
print("Les dimensions du dataframe director : ", director.shape)
#print(director)

actor = separate_and_expand("cast", dataset)
print("Les dimensions du dataframe actor : ", actor.shape)
#print(actor.columns)

def remove_column(column:str, dataset:pd.DataFrame) -> pd.DataFrame:
    """
    This functions takes as arguments a column and a dataframe.
    It deletes a cdefined column.
    It returns the dataframe without the deleted column.
    """
    data = dataset.drop(column, axis=1)
    return data

def split_name_column(column:str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Splits the 'person' column in the given DataFrame into 'firstname' and 'lastname' columns.
    
    Args:
        df (pd.DataFrame): A DataFrame containing a 'person' column with full names.
        
    Returns:
        pd.DataFrame: The input DataFrame with two new columns, 'firstname' and 'lastname', 
                      extracted from the 'person' column.
    """
    df[['firstname', 'lastname']] = df[column].str.split(n=1, expand=True).copy(deep=True)
    return df

# Séparer le prénom (firstname) du nom (lastname)
director = split_name_column("director",director)
actor = split_name_column("cast",actor)

# Vérification du succès de l'opération
#print(director.head(5))
#print(actor.head(5))

##############################################################
# Deuxième partie : Création d'un DataFrame pour chaque table
# Commentaire : pour faciliter l'insertion des données, 
# Nous allons créer un dataframe pour chaque table de notre modèle (incluant aussi les tables d'associations).
# Nous allons créer nos id pour nos différentes tables (genres, collections, productions, actors, directors).
# Ensuite, ajouter ces id dans nos tables étrangères (orignal_language, spoken_languages_trad, collections, actors, directors, genres)
##############################################################

# Création des tables uniques :
def dropping_dups(data:pd.DataFrame, col:list):
    """
    Removes duplicate rows based on specified columns.

    Args:
        data (pd.DataFrame): The DataFrame to process.
        col (list): The columns to consider for duplicate removal.

    Returns:
        pd.DataFrame: A DataFrame without duplicates.
    """
    list_data = data[col].drop_duplicates(subset=col, keep="first")
    return list_data

# Pour les tables autres que films
#######################################
concatenation = pd.concat([original_language, spoken_language_trad]) 
# Pour récupérer toutes les langues possibles, nous devons regarder parmi les langues originels que parlés
list_languages = dropping_dups(concatenation, ["language"])
list_genre = dropping_dups(genre, ["genres"])
list_collection = dropping_dups(collection, ["belongs_to_collection"])
list_production = dropping_dups(production, ["production_companies"])
list_actors = dropping_dups(actor, ["firstname", "lastname"])
list_directors = dropping_dups(director, ["firstname", "lastname"])

# Créer la fonction de création d'id et de merge
def creation_id_merge(df_id, df_merge, cols_merge):
    """
    Fonction : création des id + ajout de ces identifiants dans les tables d'associations

    Arguments :
    - df_id : DataFrame où on va créer l'identifiant
    - df_merge : DataFrame où on va ajouter les identifiants (table d'association) / Liste de DataFrame où on va ajouter les identifiants
    - cols_merge : le/les colonnes qui permettent de merger entre les deux DataFrames

    Retour : 
    Ajout des id dans df_id et dans df_merge.
    """

    # Création des id
    df_id["id_cle"] = [x for x in range(1, df_id.shape[0]+1)]

    # Ajout des id dans la/les tables d'associations

    # Si une liste de DataFrame à merger
    if type(df_merge) == list:
        val_manq = []

        for ind in range(len(df_merge)):
            df_merge[ind] = pd.merge(df_merge[ind], df_id, on=cols_merge, how="left")
            val_manq.append(df_merge[ind].isna().sum())
    
    # Si qu'un seul DataFrame à merger
    else:
        df_merge = pd.merge(df_merge, df_id, on=cols_merge, how="left")
        val_manq = df_merge.isna().sum()

    # Retour des DataFrames + Le résulats des valeurs manquantes sur la fusion
    return df_id, df_merge, val_manq


# Application de l'ajout des id dans les différents DataFrames :

list_genre, genre, val_manq = creation_id_merge(list_genre, genre, "genres")
#print(list_genre.head(5))
#print(genre.head(5))
#print(val_manq)

list_collection, collection, val_manq_c = creation_id_merge(list_collection, collection, "belongs_to_collection")
#print(list_collection.head(5))
#print(collection.head(5))
#print(val_manq_c)

list_production, production, val_manq_p = creation_id_merge(list_production, production, "production_companies")
#print(list_production.head(5))
#print(production.head(5))
#print(val_manq_p)

list_actors, actor, val_manq_a = creation_id_merge(list_actors, actor, ["firstname", "lastname"])
#print(list_actors.head(5))
#print(actor.head(5))
#print(val_manq_a)

list_directors, director, val_manq_d = creation_id_merge(list_directors, director, ["firstname", "lastname"])
#print(list_directors.head(5))
#print(director.head(5))
#print(val_manq_d)

list_languages, liste_df_language, val_manq_l = creation_id_merge(list_languages, [original_language, spoken_language_trad], "language")
#print(list_languages.head(5))
#print(liste_df_language[0].head(5))
#print(liste_df_language[1].head(5))
#print(val_manq_l)

# Ajout dans le dataset original des id de collections + directeurs + original_language
dataset = pd.merge(dataset, director, how="left", on=["director", "id"])
dataset = pd.merge(dataset, collection, how="left", on=["belongs_to_collection", "id"], suffixes=["_dir", "_coll"])

# Pour original language
liste_df_language[0]["original_language"] = liste_df_language[0]["language"]
#print(liste_df_language[0].columns)
dataset = pd.merge(dataset, liste_df_language[0], how="left", on=["original_language", "id"])


# Les tables à insérer avec les DataFrames :
##############################################
# df => table_sql :
# dataset => Film
# list_languages => Language
# liste_df_language[1] => film_languages
# list_directors => Directeur
# list_actors => Acteur
# actor => acteur_films (table d'association)
# list_production => Company
# production => film_companies
# list_genre => Genre
# genre => film_genres
##############################################