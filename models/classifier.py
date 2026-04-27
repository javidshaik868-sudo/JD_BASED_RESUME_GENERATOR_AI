# models/classifier.py

# -------------------------------
# 📦 Imports
# -------------------------------
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -------------------------------
# ✅ Train Classifier
# -------------------------------
def train_classifier(X_train, y_train):
    """
    Train a RandomForest classifier on the provided training data.

    Args:
        X_train (array-like): Features for training.
        y_train (array-like): Target labels for training.

    Returns:
        RandomForestClassifier: Trained model.
    """
    clf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    return clf

# -------------------------------
# 🔮 Predict
# -------------------------------
def predict_classifier(model, X_test):
    """
    Make predictions using the trained classifier.

    Args:
        model (RandomForestClassifier): Trained classifier.
        X_test (array-like): Test features.

    Returns:
        array: Predicted labels.
    """
    return model.predict(X_test)

# -------------------------------
# 📊 Evaluate Model
# -------------------------------
def evaluate_classifier(model, X_test, y_test):
    """
    Evaluate the model performance using accuracy and classification report.

    Args:
        model (RandomForestClassifier): Trained classifier.
        X_test (array-like): Test features.
        y_test (array-like): True labels for test set.

    Returns:
        dict: Contains accuracy and classification report.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return {
        "accuracy": accuracy,
        "report": report
    }

# -------------------------------
# 💾 Save Model
# -------------------------------
def save_model(model, file_path="models/classifier.pkl"):
    """
    Save the trained model to disk.

    Args:
        model (RandomForestClassifier): Trained model.
        file_path (str): Path to save the model.
    """
    with open(file_path, "wb") as f:
        pickle.dump(model, f)

# -------------------------------
# 📂 Load Model
# -------------------------------
def load_model(file_path="models/classifier.pkl"):
    """
    Load a saved classifier from disk.

    Args:
        file_path (str): Path to the saved model.

    Returns:
        RandomForestClassifier: Loaded model.
    """
    with open(file_path, "rb") as f:
        return pickle.load(f)