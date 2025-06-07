import pandas as pd
import shap
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load data
data = pd.read_csv('card_transdata.csv')

# Features and target
X = data.drop(columns=['fraud'])
y = data['fraud']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    stratify=y,
    random_state=42
)

# Initialize a gradient-boosting classifier with class imbalance handling
model = HistGradientBoostingClassifier(
    loss="log_loss",
    class_weight="balanced",
    learning_rate=0.05,
    max_iter=200,
    max_depth=8,
    random_state=42
)

# Train on the training set
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

print("\nTesting with all transactions...")

# Evaluate
print("Classification Report:")
print(classification_report(y_test, y_pred, digits=4))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# # Save and load the model using joblib
import joblib
def save_model(model, filename='fraud_model.pkl'):
    """Saves the trained model to a file."""
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

save_model(model)

def load_model(filename='fraud_model.pkl'):
    """Loads the saved model from a file."""
    model = joblib.load(filename)
    print(f"Model loaded from {filename}")
    return model

# Use SHAP to get feature importances
explainer = shap.Explainer(model.predict_proba, X_train)

def extract_top_features(single_row_df, top_n=3):
    # Returns the top N feature contributions for a single transaction in a formatted string to be fed into the agent
    shap_values = explainer(single_row_df)
    row_values = shap_values.values[0][:, 1]  # class 1 = fraud
    row_features = [(single_row_df.columns[i], row_values[i]) for i in range(len(row_values))]
    row_features.sort(key=lambda x: abs(x[1]), reverse=True)
    top_feature_contributions = f"Transaction's top features:\n" + "\n".join(f"  - {name}: contribution {value:.4f}" for name, value in row_features[:top_n])
    return top_feature_contributions
