# train_gpt_ai_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import os

# Load dataset
df = pd.read_csv("logs/gpt_training_dataset.csv", encoding="utf-8-sig")
X = df[["confidence"]].copy()
y = df["action"]

# Encode label
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("📊 Đánh giá mô hình:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/gpt_action_model.pkl")
joblib.dump(le, "models/gpt_label_encoder.pkl")
print("✅ Đã lưu mô hình vào thư mục models/")
