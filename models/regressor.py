# models/regressor.py

# -------------------------------
# 📦 Imports
# -------------------------------
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------
# ✅ Train Regressor
# -------------------------------
def train_regressor(X_train, y_train):
    """
    Train a RandomForest regressor on the provided training data.

    Args:
        X_train (array-like): Features for training.
        y_train (array-like): Target numerical values for training.

    Returns:
        RandomForestRegressor: Trained regression model.
    """
    reg = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    reg.fit(X_train, y_train)
    return reg

# -------------------------------
# 🔮 Predict
# -------------------------------
def predict_regressor(model, X_test):
    """
    Make predictions using the trained regressor.

    Args:
        model (RandomForestRegressor): Trained regression model.
        X_test (array-like): Test features.

    Returns:
        array: Predicted numerical values.
    """
    return model.predict(X_test)

# -------------------------------
# 📊 Evaluate Model
# -------------------------------
def evaluate_regressor(model, X_test, y_test):
    """
    Evaluate the regression model performance using MSE, RMSE, and R2 score.

    Args:
        model (RandomForestRegressor): Trained regression model.
        X_test (array-like): Test features.
        y_test (array-like): True values for test set.

    Returns:
        dict: Contains MSE, RMSE, and R2 score.
    """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return {
        "mse": mse,
        "rmse": mse ** 0.5,
        "r2_score": r2
    }

# -------------------------------
# 💾 Save Model
# -------------------------------
def save_model(model, file_path="models/regressor.pkl"):
    """
    Save the trained regressor model to disk.

    Args:
        model (RandomForestRegressor): Trained model.
        file_path (str): Path to save the model.
    """
    with open(file_path, "wb") as f:
        pickle.dump(model, f)

# -------------------------------
# 📂 Load Model
# -------------------------------
def load_model(file_path="models/regressor.pkl"):
    """
    Load a saved regressor model from disk.

    Args:
        file_path (str): Path to the saved model.

    Returns:
        RandomForestRegressor: Loaded model.
    """
    with open(file_path, "rb") as f:
        return pickle.load(f)