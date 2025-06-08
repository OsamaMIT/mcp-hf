import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from lime.lime_tabular import LimeTabularExplainer

# Load data
data = pd.read_csv('src/card_transdata.csv')

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



from lime.lime_tabular import LimeTabularExplainer

# Initialize LIME explainer on training data
explainer = LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=X_train.columns.tolist(),
    class_names=['not_fraud', 'fraud'],
    mode='classification'
)

def extract_top_features(single_row_df, top_n=3):
    # Generate explanation for the 'fraud' class (label=1)
    exp = explainer.explain_instance(
        single_row_df.values[0],
        lambda arr: model.predict_proba(
            pd.DataFrame(arr, columns=X_train.columns.tolist())
        ),
        num_features=top_n
    )

    # Get list of (feature, weight) for the fraud prediction
    feature_weights = exp.as_list(label=1)
    # Format the top features into a string
    formatted = "Transaction's top features:\n"
    formatted += "\n".join(f"  - {feat}: weight {weight:.4f}" for feat, weight in feature_weights)
    return formatted


# Show top contributing features for a few fraud examples
fraud_examples = X_test[y_test == 1].sample(5, random_state=42)
for idx, row in fraud_examples.iterrows():
    df_row = row.to_frame().T
    features_str = extract_top_features(df_row)
    print(f"\nTransaction {idx} top features:")
    print(features_str)
