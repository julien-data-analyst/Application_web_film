#### SAÉ Analyse et Conception d'outils décisionnels
#### BUT SD 3
# ---

# _This file contains the exploration, cleaning and preparation of the dataset "movies_complete.csv"._

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

see_unique_values("belongs_to_collection", dataset)[0:10]


see_unique_values("spoken_languages", dataset)[0:10]


# Traitement des données
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


film = dataset[['id', 'title', 'release_date', 'popularity', 'runtime', 
        'budget_musd', 'revenue_musd', 'overview', 'tagline', 
       'poster', 'vote_count', 'vote_average']]


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
    for _, row in data.iterrows():
        # Get the values for the specified column, handling NaN cases
        values = row[column] if pd.notna(row[column]) else 'Missing'
        
        # Split the values by the delimiter "|" (if not 'Missing')
        values = values.split('|') if values != 'Missing' else ['Missing']
        
        # Create a row for each split value, retaining the 'id'
        for value in values:
            expanded_rows.append({'id': row['id'], column: value})
    
    # Create a new DataFrame from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows)
    return expanded_df

expanded_genres = separate_and_expand('genres', dataset)

genre = separate_and_expand("genres", dataset)


def extract_collection(column: str, data: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts a subset of the DataFrame by keeping only the 'id' column 
    and the specified column after dropping any rows where the specified 
    column has missing (NaN) values.

    Parameters:
    column (str): The name of the column from which non-null values are extracted.
    data (pd.DataFrame): The DataFrame from which the subset is created.

    Returns:
    pd.DataFrame: A new DataFrame containing only the 'id' column and the 
                   specified column.
    
    """
    # Drop rows where the specified column has NaN values
    data = data.dropna(subset=[column])
    
    # Return only the 'id' column and the specified column
    return data[["id", column]]


collection = extract_collection("belongs_to_collection", dataset)


language_dict = {
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
    "xx": "Unknown", 
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

def extract_languages(column: str, data: pd.DataFrame, dicto: dict) -> pd.DataFrame:
    """
    This function maps language codes in the specified column of a DataFrame
    to their full language names using a provided dictionary. It then returns 
    a DataFrame containing the 'id' column and the specified column with the 
    full language names.

    Parameters:
    column (str): The name of the column containing language codes to be mapped.
    data (pd.DataFrame): The DataFrame containing the data to be processed.
    dicto (dict): A dictionary mapping language codes to full language names.

    Returns:
    pd.DataFrame: A DataFrame containing only the 'id' column and the 
                   specified column with full language names.
    """
    # Map language codes to full language names using the provided dictionary
    data[column] = data[column].map(dicto)
    
    # Return the DataFrame containing only the 'id' column and the specified column
    return data[["id", column]]

original_language = extract_languages("original_language", dataset, language_dict)

spoken_language = separate_and_expand("spoken_languages", dataset)


def sep_languages(data):
    """
    This function takes a DataFrame with movie information, including columns for actors ('cast') and directors ('director'),
    and creates a new DataFrame where each row represents either an actor or a director for a movie.
    
    It also includes a column indicating whether the person is a director (`True`) or an actor (`False`).

    Parameters:
    data (pd.DataFrame): A DataFrame containing movie data. The DataFrame should have:
        - 'id': The unique movie identifier.
        - 'cast': A string of actor names, possibly separated by "|" if there are multiple actors.
        - 'director': A string of director names, possibly separated by "|" if there are multiple directors.

    Returns:
    pd.DataFrame: A new DataFrame with the following columns:
        - 'idfilm': The movie identifier.
        - 'person': The name of the actor or director.
        - 'director': A boolean indicating whether the person is a director (True) or an actor (False).

    """
    # Initialize an empty list to hold the rows for the new DataFrame
    rows = []
    
    # Iterate through each movie in the original dataset
    for _, row in data.iterrows():
        data
        # Split by "|" for actors (handling multiple names)  
        languages = row["spoken_languages"].split('|') if pd.notna(row["spoken_languages"]) else []
        if languages != []:
            for l in languages:
                rows.append({'idfilm': row['id'], 'original_language': row["original_language"], 'spoken_languages': l})
        
    # Create a new DataFrame from the rows list
    result_df = pd.DataFrame(rows)
    return result_df

# Example of creating the new table
languages = sep_languages(dataset)


def language_classify(data:pd.DataFrame):
    """
    Adds a column indicating whether the spoken language matches the original language.

    Args:
        data (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The updated DataFrame.
    """
    data["original_or_not"] = data["original_language"] == data["spoken_languages"]
    return data

languages = language_classify(languages)


production = separate_and_expand("production_companies", dataset)

def create_person_director_table(data):
    """
    This function takes a DataFrame with movie information, including columns for actors ('cast') and directors ('director'),
    and creates a new DataFrame where each row represents either an actor or a director for a movie.
    
    It also includes a column indicating whether the person is a director (`True`) or an actor (`False`).

    Parameters:
    data (pd.DataFrame): A DataFrame containing movie data. The DataFrame should have:
        - 'id': The unique movie identifier.
        - 'cast': A string of actor names, possibly separated by "|" if there are multiple actors.
        - 'director': A string of director names, possibly separated by "|" if there are multiple directors.

    Returns:
    pd.DataFrame: A new DataFrame with the following columns:
        - 'idfilm': The movie identifier.
        - 'person': The name of the actor or director.
        - 'director': A boolean indicating whether the person is a director (True) or an actor (False).

    """
    # Initialize an empty list to hold the rows for the new DataFrame
    rows = []
    
    # Iterate through each movie in the original dataset
    for _, row in data.iterrows():
        # Handle missing values: replace NaN with 'Missing' and then split
        actors = row['cast'] if pd.notna(row['cast']) else 'Missing'
        director = row['director'] if pd.notna(row['director']) else 'Missing'
        
        # Split by "|" for actors (handling multiple names)
        actors = actors.split('|') if actors != 'Missing' else ['Missing']
        
        # Add directors to the rows with director=True
        rows.append({'idfilm': row['id'], 'person': director, 'director': True})
        
        # Add actors to the rows with director=False
        for actor in actors:
            rows.append({'idfilm': row['id'], 'person': actor, 'director': False})
    
    # Create a new DataFrame from the rows list
    result_df = pd.DataFrame(rows)
    return result_df

# Example of creating the new table
person_director_table = create_person_director_table(dataset)


director = person_director_table[person_director_table["director"].isin([True])]
actor = person_director_table[~person_director_table["director"].isin([True])]

def remove_column(column:str, dataset:pd.DataFrame) -> pd.DataFrame:
    """
    This functions takes as arguments a column and a dataframe.
    It deletes a cdefined column.
    It returns the dataframe without the deleted column.
    """
    data = dataset.drop(column, axis=1)
    return data

director = remove_column("director", director)
actor = remove_column("director", actor)


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


director = split_name_column("person",director)
actor = split_name_column("person",actor)


director = remove_column("person", director)
actor = remove_column("person", actor)



def dropping_dups(data:pd.DataFrame, col:list):
    """
    Removes duplicate rows based on specified columns.

    Args:
        data (pd.DataFrame): The DataFrame to process.
        col (list): The columns to consider for duplicate removal.

    Returns:
        pd.DataFrame: A DataFrame without duplicates.
    """
    list_data = data[col].drop_duplicates(subset=col)
    return list_data

list_languages = dropping_dups(languages, ["spoken_languages"])
list_genre = dropping_dups(genre, ["genres"])
list_collection = dropping_dups(collection, ["belongs_to_collection"])
list_production = dropping_dups(production, ["production_companies"])
list_actors = dropping_dups(actor, ["firstname", "lastname"])
list_directors = dropping_dups(director, ["firstname", "lastname"])

dataset = split_name_column("director", dataset)

def replace_na(data, col:list):
    data[col] = data[col].fillna(value="Missing")
    return data

dataset = replace_na(dataset, ["belongs_to_collection","director"])



