# /// script
# requires-python = ">=3.10"
# dependencies = ["scikit-learn", "numpy"]
# ///
"""
Skrip Reproduksi Eksperimen Klasifikasi Situs Web Phishing (Dokumen 3 - JKI SINTA 4)
Dataset : UCI Machine Learning Repository - Phishing Websites (DOI DataCite: https://doi.org/10.24432/C51W2X)
Cara uji: uv run website/reproduksi-eksperimen/run_jki_phishing_experiment.py
"""
import datetime
import json
import platform
import time
import urllib.request
import zipfile
from pathlib import Path
import numpy as np
import sklearn
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

HERE = Path(__file__).resolve().parent
UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/327/phishing+websites.zip"
CACHE_ZIP = HERE / "uci_phishing_327.zip"


def load_dataset():
    if not CACHE_ZIP.exists():
        req = urllib.request.Request(UCI_ZIP_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            CACHE_ZIP.write_bytes(resp.read())
    with zipfile.ZipFile(CACHE_ZIP, "r") as zf:
        arff_name = next(
            n for n in zf.namelist() if n.lower().endswith(".arff") and not Path(n).name.startswith(".")
        )
        raw_text = zf.read(arff_name).decode("utf-8", errors="ignore")
    features, rows, in_data = [], [], False
    for line in raw_text.splitlines():
        s = line.strip()
        if not s or s.startswith("%"):
            continue
        if s.lower().startswith("@attribute"):
            features.append(s.split()[1].strip("'\""))
        elif s.lower().startswith("@data"):
            in_data = True
        elif in_data:
            rows.append([int(x.strip()) for x in s.split(",") if x.strip()])
    arr = np.array(rows, dtype=np.int32)
    X = arr[:, :-1]
    y = np.where(arr[:, -1] == -1, 1, 0)
    return X, y, features[:-1], arff_name


def main():
    X, y, feat_names, arff_name = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=None, random_state=42, n_jobs=1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    out_models = {}
    for name, clf in models.items():
        t0 = time.perf_counter()
        clf.fit(X_train, y_train)
        train_ms = (time.perf_counter() - t0) * 1000.0
        t1 = time.perf_counter()
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]
        infer_ms = (time.perf_counter() - t1) * 1000.0
        tn, fp, fn, tp = [int(v) for v in confusion_matrix(y_test, y_pred).ravel()]
        cv_scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy", n_jobs=1)
        imp = clf.feature_importances_
        top_idx = np.argsort(imp)[::-1][:10]
        out_models[name] = {
            "accuracy": round(float(accuracy_score(y_test, y_pred)) * 100, 2),
            "precision": round(float(precision_score(y_test, y_pred)) * 100, 2),
            "recall": round(float(recall_score(y_test, y_pred)) * 100, 2),
            "f1": round(float(f1_score(y_test, y_pred)) * 100, 2),
            "roc_auc": round(float(roc_auc_score(y_test, y_prob)) * 100, 2),
            "cv5_mean": round(float(np.mean(cv_scores)) * 100, 2),
            "cv5_std": round(float(np.std(cv_scores, ddof=1)) * 100, 2),
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
            "train_ms": round(train_ms, 2),
            "infer_test_ms": round(infer_ms, 2),
            "top_features": [{"feature": feat_names[i], "importance": round(float(imp[i]), 4)} for i in top_idx],
        }
    payload = {
        "timestamp_iso": datetime.datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "scikit_learn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "dataset_doi": "https://doi.org/10.24432/C51W2X",
        "arff_file": arff_name,
        "total_rows": int(X.shape[0]),
        "num_features": int(X.shape[1]),
        "phishing_rows": int(np.sum(y == 1)),
        "legitimate_rows": int(np.sum(y == 0)),
        "train_rows": int(len(y_train)),
        "test_rows": int(len(y_test)),
        "models": out_models,
    }
    (HERE / "jki_phishing_metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
