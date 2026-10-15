"""Train an experimental multi-output Big Five text regression pipeline.

Input CSV must have: cv_text, openness, conscientiousness, extraversion,
agreeableness, neuroticism. Use only appropriately licensed, consented data
with validated labels. This script is a research starting point, not a
production-ready model. Evaluate held-out performance and bias before use.
"""
from pathlib import Path
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research_tools" / "consented_big_five_dataset.csv"
OUT = ROOT / "recruitment" / "ml_artifacts" / "experimental_big_five_pipeline.joblib"
TEXT = "cv_text"
TARGETS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

if not DATA.exists():
    raise SystemExit(f"Dataset not found: {DATA}. Create it from consented, validated research data; do not use fabricated labels.")
df = pd.read_csv(DATA).dropna(subset=[TEXT, *TARGETS])
if len(df) < 50:
    raise SystemExit("For this experimental scaffold, provide at least 50 labeled examples; more diverse data is normally needed for meaningful evaluation.")
X_train, X_test, y_train, y_test = train_test_split(df[TEXT].astype(str), df[TARGETS], test_size=0.2, random_state=42)
model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=20000, min_df=2, stop_words="english")), ("regressor", MultiOutputRegressor(LinearSVR(random_state=42, max_iter=10000)))])
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Held-out MAE per trait (lower is better; compare to baseline):")
for name, value in zip(TARGETS, mean_absolute_error(y_test, pred, multioutput="raw_values")):
    print(f"  {name}: {value:.3f}")
print("IMPORTANT: compare against a mean-prediction baseline, test demographic/group differences where lawful and appropriate, and do not use for employment decisions.")
OUT.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, OUT)
print(f"Saved experimental model: {OUT}")
