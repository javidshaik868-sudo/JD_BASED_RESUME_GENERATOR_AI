# train_models.py

# -------------------------------
# 📦 Imports
# -------------------------------
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Optional: custom classifier/regressor modules
from models.classifier import train_classifier, save_model as save_clf
from models.regressor import train_regressor, save_model as save_reg

# -------------------------------
# 📂 Paths and Directories
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sample_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

print("📂 Dataset Exists:", os.path.exists(DATA_PATH))

# -------------------------------
# 📄 Load Dataset
# -------------------------------
def load_data(path):
    """
    Load CSV dataset from the given path.

    Args:
        path (str): Path to CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    df = pd.read_csv(path)
    return df

data = load_data(DATA_PATH)

# -------------------------------
# ✨ Preprocess Data
# -------------------------------
# Combine relevant columns into a single 'text' column
data["text"] = (
    data["Primary Skills"].fillna("") + " " +
    data["Current Job Title"].fillna("") + " " +
    data["Job Category"].fillna("") + " " +
    data["Job Applied"].fillna("")
)

# Strip whitespace and remove empty rows
data["text"] = data["text"].str.strip()
data = data[data["text"] != ""]

print("🔍 Sample text data:")
print(data["text"].head(10))
print("✅ Total valid rows:", len(data))

# -------------------------------
# 🎯 Set Targets
# -------------------------------
y_class = data["Job Applied"]        # Classification target
y_reg = data.get("Salary", 0)        # Regression target (dummy if not present)

# -------------------------------
# 🏋️ Train Models
# -------------------------------
def train_models():
    """
    Train classification and regression models using raw text data.
    Vectorization-free approach.
    """
    X = data["text"]  # Features (raw text)

    # Split data for classification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_class, test_size=0.2, random_state=42
    )

    # Split data for regression
    _, _, y_reg_train, y_reg_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )

    # Train classifier
    print("🤖 Training classifier...")
    clf = train_classifier(X_train, y_train)

    # Train regressor
    print("📈 Training regressor...")
    reg = train_regressor(X_train, y_reg_train)

    # Save models
    print("💾 Saving models...")
    save_clf(clf, os.path.join(MODEL_DIR, "classifier.pkl"))
    save_reg(reg, os.path.join(MODEL_DIR, "regressor.pkl"))

    print("✅ Training completed successfully!")

# -------------------------------
# 🔥 Main Execution
# -------------------------------
if __name__ == "__main__":
    train_models()