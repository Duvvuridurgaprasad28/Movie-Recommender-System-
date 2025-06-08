
```markdown
# Movie Recommender System with Live Posters

This project is a content-based movie recommender system that suggests movies similar to a selected movie using metadata features and cosine similarity. The recommendations are enhanced with live movie posters fetched dynamically from the TMDB API, all presented via a Streamlit web app.

---

## Demo

🎬 Explore movie recommendations with posters in an interactive UI.

---

## Features

- **Content-based filtering** using movie tags derived from genres, cast, crew, keywords, and overview.
- **Text preprocessing** including tokenization, lemmatization, and vectorization.
- **Similarity computation** using cosine similarity.
- **Live fetching** of movie posters using TMDB API.
- **User-friendly interface** built with Streamlit.

---

## Repo Structure

```

├── data/                      # Raw and processed datasets
├── artifacts/                 # Pickled models and similarity matrices
├── src/
│   ├── components/            # Pipeline components (data ingestion, feature engineering, model training)
│   └── app.py                 # Streamlit application
├── config/
│   ├── config.yaml            # Configuration paths
│   └── params.yaml            # Hyperparameters and settings
├── logs/                      # Log files
├── dvc.yaml                   # DVC pipeline stages
├── README.md                  # This README
├── requirements.txt           # Python dependencies

````

---

## Getting Started

1. **Clone the repo**

```bash
git clone https://github.com/Duvvuridurgaprasad28/Movie-Recommender-System-.git
cd Movie-Recommender-System-
````

2. **Create and activate virtual environment**

```bash
python -m venv env
source env/bin/activate     # On Windows: env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure API key**

Add your TMDB API key in `src/app.py` (replace placeholder):

```python
TMDB_API_KEY = "your_api_key_here"
```

Sign up here: [TMDB API](https://www.themoviedb.org/documentation/api)

5. **Run the pipeline**

Use DVC to reproduce pipeline stages:

```bash
dvc repro
```

Or run stages manually:

```bash
python src/components/data_ingestion.py
python src/components/feature_engineering.py
python src/components/model_trainer.py
```

6. **Launch Streamlit app**

```bash
streamlit run src/app.py
```

---

## Configuration Files

* `config/config.yaml`: Defines paths to datasets and artifacts.
* `params.yaml`: Defines hyperparameters such as `max_features`, `stop_words`, and `top_n_recommendations`.

---

## Logs

Execution logs are saved under `logs/` directory for debugging and monitoring.

---

## Contributing

Contributions welcome! Feel free to open issues or pull requests.

---

## License

This project is licensed under the MIT License.

---

Enjoy discovering your next favorite movie! 🍿🎥

```

