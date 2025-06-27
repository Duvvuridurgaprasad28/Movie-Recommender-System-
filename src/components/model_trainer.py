# model_trainer.py placeholder
import os
import pickle
import logging
import yaml
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Setup logging
log_dir = 'logs' 
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("model_trainer") 
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler() 
file_handler = logging.FileHandler(os.path.join(log_dir, 'model_trainer.log'), mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter) 
file_handler.setFormatter(formatter)
logger.addHandler(console_handler) 
logger.addHandler(file_handler)

lemmatizer = WordNetLemmatizer()


def load_config(config_path: str) -> dict:
    """
    Load configuration from a YAML file.
    """
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error: {e}")
        raise


def load_params(params_path: str = "params.yaml") -> dict:
    """
    Load parameters from YAML.
    """
    try:
        with open(params_path, "r") as file:
            return yaml.safe_load(file)
            logger.debug(f"Loaded params: {params}")
    except FileNotFoundError:
        logger.error(f"Params file not found: {params_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error: {e}")
        raise


def apply_lemmatization(text: str) -> str:
    """
    Tokenize and lemmatize input text.
    """
    try:
        words = word_tokenize(text)
        return ' '.join([lemmatizer.lemmatize(w.lower()) for w in words if w.isalnum()])
    except Exception as e:
        logger.error(f"Lemmatization error: {e}")
        return ''


def apply_count_vectorizer(text_list, max_features, stop_words, vectorizer_path="artifacts/vectorizer.pkl"):
    """
    Apply CountVectorizer or load it from pickle if it exists.
    """
    try:
        if os.path.exists(vectorizer_path):
            with open(vectorizer_path, "rb") as f:
                cv = pickle.load(f)
            vectors = cv.transform(text_list).toarray()
            logger.info("Vectorizer loaded from artifacts.")
        else:
            cv = CountVectorizer(max_features=max_features, stop_words=stop_words)
            vectors = cv.fit_transform(text_list).toarray()
            with open(vectorizer_path, "wb") as f:
                pickle.dump(cv, f)
            logger.info("Vectorizer trained and saved to artifacts.")
        return cv, vectors
    except Exception as e:
        logger.error(f"CountVectorizer error: {e}")
        return None, np.array([])


def get_recommendations(movie_title, df, similarity_matrix, top_n=5):
    """
    Recommend top N similar movies for a given movie title.
    """
    try:
        movie_title = movie_title.lower()
        titles_lower = df['title'].str.lower()

        if movie_title not in titles_lower.values:
            logger.warning(f"Movie '{movie_title}' not found.")
            return []

        idx = titles_lower[titles_lower == movie_title].index[0]

        similarity_scores = similarity_matrix[idx]
        sorted_indices = np.argsort(similarity_scores)[::-1]

        # Remove the movie itself and get top N
        sorted_indices = [i for i in sorted_indices if i != idx][:top_n]
        recommended_titles = df.iloc[sorted_indices]["title"].tolist()
        return recommended_titles

    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}")
        return []


def main():
    """
    Train and save movie recommender artifacts.
    """
    try:
        logger.info(" Starting Movie Recommender training pipeline...")

        # Load configs
        config = load_config("config/config.yaml")
        logger.debug(f"Loaded config: {config}")
        params = load_params("params.yaml")
        model_params = params.get("model_trainer", {})

        max_features = model_params.get("max_features", 5000)
        stop_words = model_params.get("stop_words", "english")
        top_n_recommendations = model_params.get("top_n_recommendations", 5)

        transformed_path = config["paths"]["transformed_data"]

        if not os.path.exists(transformed_path):
            logger.error(f"Transformed data file missing: {transformed_path}")
            raise FileNotFoundError(f"Missing file: {transformed_path}")

        df = pd.read_csv(transformed_path)
        logger.info(f"Loaded transformed data: {df.shape}")

        # Lemmatize tags
        df['tags'] = df['tags'].apply(apply_lemmatization)
        logger.info(" Lemmatization applied to tags.")

        # Vectorization
        cv, vectors = apply_count_vectorizer(df['tags'], max_features, stop_words)
        if vectors.size == 0:
            raise ValueError("❌ Vectorization failed. No vectors returned.")

        # Similarity matrix
        similarity = cosine_similarity(vectors)
        logger.info(" Cosine similarity computed.")

        # Save artifacts
        os.makedirs("artifacts", exist_ok=True)
        with open("artifacts/movies.pkl", "wb") as f:
            pickle.dump(df, f)
        with open("artifacts/similarity.pkl", "wb") as f:
            pickle.dump(similarity, f)

        logger.info(" Artifacts saved to 'artifacts/'.")

        # Save processed data
        df.to_csv("data/processed_data.csv", index=False)
        logger.info("Processed data saved to data/processed_data.csv")

        # Example recommendation
        example_movie = df['title'].iloc[0]
        recommendations = get_recommendations(example_movie, df, similarity, top_n=top_n_recommendations)

        print(f"\n🎬 Top {top_n_recommendations} recommendations for '{example_movie}':")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
