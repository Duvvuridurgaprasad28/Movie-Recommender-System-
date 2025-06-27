import os

# Define the folder and file structure
structure = {
    "src/components": [
        "data_ingestion.py",
        "feature_engineering.py",
        "model_trainer.py"
    ],
    "config": ["config.yaml"],
    "data/raw": [],  # Folder only, no files
    "data": [],  # Skip transformed_data.csv, processed_data.csv
    "artifacts": [],  # Folder only, no files
    ".": ["params.yaml", "dvc.yaml", ".gitignore", "requirements.txt", "setup.py"]
}

# Files to skip (already created or not required)
skip_files = {"README.md", "app.py", "dvc.lock"}

def create_structure():
    for folder, files in structure.items():
        if folder != ".":
            os.makedirs(folder, exist_ok=True)
        for file in files:
            if file in skip_files:
                continue
            file_path = os.path.join(folder, file) if folder != "." else file
            with open(file_path, "w") as f:
                f.write(f"# {file} placeholder\n")

    print("✅ Project structure created successfully.")

if __name__ == "__main__":
    create_structure()
