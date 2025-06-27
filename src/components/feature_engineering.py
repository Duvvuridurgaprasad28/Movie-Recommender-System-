# feature_engineering.py
import pandas as pd 
import ast
import os 
import logging 
import yaml 
import pickle 
import numpy as np


#Set up logging
log_dir = 'logs' 
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("feature_engineering") 
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler() 
file_handler = logging.FileHandler(os.path.join(log_dir, 'feature_engineering.log'), mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter) 
file_handler.setFormatter(formatter)
logger.addHandler(console_handler) 
logger.addHandler(file_handler)


def load_config(config_path: str) -> dict: 
    """
    Load configuration from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: A dictionary with configuration keys and values.
    """
    try: 
        with open(config_path, "r") as file: 
            config = yaml.safe_load(file) 
            logger.debug('Config loaded from %s', config_path) 
            return config 
    except Exception as e: 
        logger.error(f"Failed to load config: {e}") 
        raise
 
def convert(text):
    """
    Parses a string representation of a list and extracts 'name' values from dictionaries.

    Args:
        text (str): A string containing a list of dictionaries.

    Returns:
        list: A list of names extracted from the input text.
    """

    try:
        parsed_data = ast.literal_eval(text)
        if not isinstance(parsed_data, list):
            raise ValueError("Parsed data is not a list")

        name_list = [i['name'] for i in parsed_data if 'name' in i]
        return name_list

    except (SyntaxError, ValueError, TypeError) as e:
        logger.error(f"Error processing input: {obj}, Exception: {e}")
        return []  # Return an empty list in case of an error
    

def convert_cast(obj: str):
    """
    Parses a string representation of a list containing cast details
    and extracts the first three names.

    Args:
        obj (str): A string containing a list of dictionaries with 'name' keys.

    Returns:
        list: A list of up to three names extracted from the input text.
    """
    try:
        parsed = ast.literal_eval(obj)  # Convert string to Python object
        return [i['name'] for i in parsed[:3] if 'name' in i]  # Extract up to three names
    except (SyntaxError, ValueError, TypeError):
        return []  # Return an empty list in case of an error


def convert_crew(obj):
    """
    Extracts the names of people with the job title 'Director' from a stringified list of dictionaries.

    Args:
        obj (str): A string representation of a list containing dictionaries with 'name' and 'job' keys.

    Returns:
        list: A list of names of directors.
    """
    try:
        lst = []
        parsed = ast.literal_eval(obj)  # Convert string to list
        if not isinstance(parsed, list):
            raise ValueError("Parsed data is not a list")
        
        for person in parsed:
            if person.get('job') == 'Director':
                lst.append(person['name'])
        return lst
        logger.info(f"Extracted {len(lst)} directors.")  # Logging success

    except (SyntaxError, ValueError, TypeError) as e:
        logger.error(f"Error processing input: {obj}, Exception: {e}")  # Logging error
        return []  # Return an empty list if there's an error
    
def combine_tags(movies):
    """
    Combines multiple columns into a single 'tags' column for content-based recommendations.

    Args:
        movies (pd.DataFrame): DataFrame containing 'overview', 'genres', 'keywords', 'cast', and 'crew' columns.

    Returns:
        pd.DataFrame: Updated DataFrame with a new 'tags' column.
    """
    try:
        movies["tags"] = movies["overview"]  + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]
        return movies
    except Exception as e:
        print(f"Error combining tags: {e}")
        return movies
    
def main():
    try:
        # Load config
        logger.info("Loading configuration file...")
        config = load_config("config/config.yaml")

        # Load processed dataset
        processed_path = config.get("processed_data_path", "data/processed_movies.csv")
        logger.info(f"Loading processed dataset from {processed_path}...")
        movies = pd.read_csv(processed_path)
        logger.info(f"Loaded processed data with shape {movies.shape}")

        # Apply transformation functions
        logger.info("Applying genre conversion...")
        movies['genres'] = movies['genres'].apply(convert)
        logger.debug(f"Sample genres after conversion: {movies['genres'].iloc[0]}")

        logger.info("Applying keyword conversion...")
        movies['keywords'] = movies['keywords'].apply(convert)
        logger.debug(f"Sample keywords after conversion: {movies['keywords'].iloc[0]}")

        logger.info("Applying cast conversion (top 3)...")
        movies['cast'] = movies['cast'].apply(convert_cast)
        logger.debug(f"Sample cast after conversion: {movies['cast'].iloc[0]}")

        logger.info("Applying crew conversion (director only)...")
        movies['crew'] = movies['crew'].apply(convert_crew)
        logger.debug(f"Sample crew after conversion: {movies['crew'].iloc[0]}")

        # Remove spaces in multi-word tokens
        logger.info("Removing spaces from cast, crew, genres, and keywords...")
        for col in ['cast', 'crew', 'genres', 'keywords']:
            movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])
            logger.debug(f"Sample {col} after removing spaces: {movies[col].iloc[0]}")

        # Tokenize the overview
        logger.info("Tokenizing overview text...")
        movies['overview'] = movies['overview'].apply(lambda x: x.split())
        logger.debug(f"Sample overview after tokenization: {movies['overview'].iloc[0]}")

        # Combine into tags column
        logger.info("Combining all features into 'tags' column...")
        movies = combine_tags(movies)
        logger.debug(f"Sample tags: {movies['tags'].iloc[0]}")

        # Drop unnecessary columns
        logger.info("Dropping intermediate columns: overview, genres, keywords, cast, crew...")
        movies = movies.drop(columns=['overview', 'genres', 'keywords', 'cast', 'crew'])

        print(type(movies['tags'].iloc[0]))

        movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
        # Save transformed data
        save_path = "data/transformed_data.csv"
        logger.info(f"Saving transformed data to {save_path}...")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        movies.to_csv(save_path, index=False)
        logger.info(f"Transformed data saved successfully with shape {movies.shape}")

    except Exception as e:
        logger.error(f"Feature engineering failed: {e}")
        raise


if __name__ == "__main__":
    main()
