import pandas as pd
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
