# data_ingestion.py placeholder
import os
import logging
import yaml
import pandas as pd
import numpy as np

# Setup logging
log_dir = 'logs' 
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("data_ingestion") 
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler() 
file_handler = logging.FileHandler(os.path.join(log_dir, 'data_ingstion.log'), mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter) 
file_handler.setFormatter(formatter)
logger.addHandler(console_handler) 
logger.addHandler(file_handler)

def load_config(config_path: str) -> dict:
    """
    Loads multiple datasets based on file paths specified in a configuration dictionary.

    Args:
        config (dict): A dictionary containing dataset names and file paths.

    Returns:
        dict: A dictionary with dataset names as keys and pandas DataFrames as values.
    """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            logger.info(f"Config file loaded successfully: {config_path}")  # ✅ Logging before return
            return config
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading config: {e}")
        raise

def load_dataset(data_path: str) -> dict:
    """
    Loads multiple datasets based on file paths specified in a YAML configuration file.

    Args:
        config_path (str): Path to the YAML config file containing dataset paths.

    Returns:
        dict: A dictionary with dataset names (like 'train' and 'test') as keys
              and pandas DataFrames as values.
    """
    try:
        with open(data_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"YAML file loaded successfully from: {data_path}")
        return config
    except FileNotFoundError:
        logger.error(f"YAML file not found: {data_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error in file {data_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading YAML file {data_path}: {e}")
        raise

def preprocess_data(train_df: pd.DataFrame, test_df: pd.DataFrame, save_path: str) -> pd.DataFrame:
    """
    Preprocess the train and test datasets and save both raw and cleaned datasets.

    Parameters:
        train (pd.DataFrame): The movies DataFrame.
        credits (pd.DataFrame): The credits DataFrame.
        save_path (str): Folder path to save raw and processed data.

    Returns:
        pd.DataFrame: A preprocessed DataFrame (merged and cleaned).
    """
    try:
        # Merging datasets
        movies = movies.merge(credits, on='title')
        logger.debug("Merged DataFrame created with %d rows and %d columns", movies.shape[0], movies.shape[1])

        # Selecting main columns
        movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
        logger.debug("Selected columns: %s", list(movies.columns))

        # Dropping null values
        rows_before = movies.shape[0]
        movies = movies.dropna()
        rows_after = movies.shape[0]
        logger.debug("Dropped %d rows containing null values", rows_before - rows_after)
        movies['title'] = movies['title'].str.lower()
        return movies

    except Exception as e:
        logger.error("Unexpected error occurred during preprocessing: %s", e)
        raise

def main():
    config_path = "config/config.yaml"  
    config = load_config(config_path)
    
    save_path = "data"  # saving the processed_data in data folder
    os.makedirs(save_path, exist_ok=True)

    # Load datasets using config values
    try:
        movies = pd.read_csv(config["paths"]['movies_path'])
        credits = pd.read_csv(config["paths"]['credits_path'])

        print("movies dataset loaded successfully with shape:", movies.shape)
        print("credits dataset loaded successfully with shape:", credits.shape)
        
        # Save processed data
        movies.to_csv(os.path.join(save_path, "processed_movies.csv"), index=False)
        logger.info("Processed data saved successfully.")

        # Preprocess and save the cleaned data
        processed = preprocess_data(movies, credits,save_path)
        processed.to_csv(os.path.join(save_path, "processed_movies.csv"), index=False)
        logger.info("Processed data saved successfully to %s.", save_path)
        logger.info("Preprocessing complete. Final shape: %s", processed.shape)
        
    except KeyError as e:
        print(f"Missing expected key in config: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error loading datasets: {e}")
        raise

if __name__ == "__main__":
    main()
