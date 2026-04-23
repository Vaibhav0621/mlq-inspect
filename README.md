# ⚡ MLQ — ML Model Inspector CLI

<div align="center">

[![PyPI - Version](https://img.shields.io/badge/version-0.1.0-FF0000?style=for-the-badge)](https://pypi.org/project/mlq/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-001F3F?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-FF0000?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Inspect, Explain & Audit Your ML Models — All in One Command**

*No Jupyter. No boilerplate. Just raw power.*

</div>

---

## 🚀 What is MLQ?

**mlq** is a production-quality Python CLI tool that lets any ML engineer inspect, explain, and audit a trained sklearn-compatible model from the terminal in one command:

```bash
mlq inspect model.pkl
```

Perfect for:
- 🔍 **Feature importance analysis** with SHAP explainability
- 📊 **Data drift detection** using KS-test and PSI metrics
- ⚖️ **Model comparison** side-by-side
- 📄 **Automated report generation** with embedded charts
- ✅ **Production audits** and compliance checks

---

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install mlq
```

### From Source (with dev dependencies)
```bash
git clone https://github.com/yourusername/mlq.git
cd mlq
pip install -e ".[dev]"
```

---

## 🎯 Quick Examples

### 1️⃣ Inspect a Model
```bash
mlq inspect model.pkl
```

**Output:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃            RandomForestClassifier             ┃
┃  📌 Features: 10  │  Classes: 2  │  Trees: 100 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📊 Feature Importance (SHAP - Top 10)
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Feature       ┃ Mean SHAP ┃ Importance     ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ feature_3     │ 0.4215    │ ████████████   │
│ feature_7     │ 0.3184    │ █████████      │
│ feature_1     │ 0.2456    │ ███████        │
└───────────────┴───────────┴────────────────┘
```

### 2️⃣ Detect Data Drift
```bash
mlq inspect model.pkl --ref training_data.csv --target target_col
```

Detects when your feature distributions have shifted from training data using:
- **KS-Test**: Statistical significance (p-value < 0.05 = drift)
- **PSI**: Shift magnitude (< 0.1 = OK, 0.1–0.25 = warning, ≥ 0.25 = drift)

### 3️⃣ Compare Two Models
```bash
mlq compare model_v1.pkl model_v2.pkl
```

Side-by-side view:
- Model metadata and hyperparameters
- Feature counts and class distribution
- Top-5 SHAP features ranked by importance

### 4️⃣ Generate HTML Report
```bash
mlq report model.pkl --output report.html --ref training_data.csv
```

Creates a **standalone, shareable HTML report** with:
- ✅ Full model metadata  
- ✅ Embedded SHAP charts  
- ✅ Drift analysis tables  
- ✅ Responsive dark theme  
- ✅ Zero dependencies (opens in any browser)

### 5️⃣ Version Info
```bash
mlq version
```

Shows installed versions of MLQ, Python, SHAP, scikit-learn, and other key dependencies.

---

## 📖 Command Reference

### `mlq inspect <model_path>`

**Main command** — Full model inspection and explanation.

| Option | Type | Description |
|--------|------|-------------|
| `--ref PATH` | Path | Reference CSV for drift detection (optional) |
| `--target TEXT` | Text | Target column name (default: `"target"`) |
| `--output PATH` | Path | Save as `.md` or `.html` (auto-detect by extension) |
| `--no-shap` | Flag | Skip SHAP (for very large models) |

**Auto-Detects Explainer:**
- 🌳 **Tree-based** (RF, GBM, XGBoost) → TreeExplainer (fastest)
- 📈 **Linear** (LogReg, LinearReg, Ridge) → LinearExplainer (fast)
- 🎯 **Other** (SVM, KNN) → KernelExplainer (slower)

---

### `mlq compare <model_a> <model_b>`

**Side-by-side model comparison** in rich formatted tables.

| Option | Type | Description |
|--------|------|-------------|
| `--ref PATH` | Path | Reference data for metrics |
| `--target TEXT` | Text | Target column name |

---

### `mlq report <model_path>`

**Generate standalone HTML/Markdown reports.**

| Option | Type | Description |
|--------|------|-------------|
| `--output PATH` | Path | (required) e.g., `report.html` |
| `--ref PATH` | Path | Reference data for drift section |
| `--target TEXT` | Text | Target column name |

---

### `mlq version`

Print version info for MLQ and all dependencies.

---

## 🧠 How SHAP Explainability Works

[SHAP (SHapley Additive exPlanations)](https://github.com/slundberg/shap) uses game theory to explain predictions:

> Each feature's contribution to a prediction is calculated as a **Shapley value**, representing its "fair share" of the prediction based on all possible feature combinations.

**Why it matters:**
- ✅ Theoretically sound (based on cooperative game theory)
- ✅ Model-agnostic (works with any sklearn estimator)
- ✅ Interpretable results (magnitude = feature importance)
- ✅ Fast with tree models (C++ backend)

**mlq's approach:**
1. Auto-selects the fastest SHAP explainer for your model type
2. Computes mean |SHAP value| across all predictions
3. Ranks features by importance
4. For multiclass: averages SHAP across all classes

---

## 📡 How Drift Detection Works

**Drift = Distribution Shift** — Your data changed from training time ⚠️

This often signals: *Model needs retraining*

### Two Complementary Metrics:

#### 1. **Kolmogorov-Smirnov (KS) Test**
- Tests if two distributions are significantly different
- **Null hypothesis**: Distributions are the same
- **Result**: p-value
  - p < 0.05 → ✅ **Signal of drift** (reject null)
  - p ≥ 0.05 → ❌ No drift

#### 2. **Population Stability Index (PSI)**
- Measures **magnitude** of distributional shift
- Interpretation:
  - PSI < 0.1 → ✅ Stable (no action)
  - PSI 0.1–0.25 → ⚠️ Warning (monitor)
  - PSI ≥ 0.25 → 🔴 Drift (retrain recommended)

**Note:** Only numeric features by default. Encode categorical features manually if needed.

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/my-feature`
3. **Install dev dependencies**: `pip install -e ".[dev]"`
4. **Run tests**: `pytest tests/`
5. **Lint code**: `ruff check mlq/`
6. **Format code**: `black mlq/`
7. **Push & open a PR**

**Before submitting:**
- ✅ All tests pass
- ✅ Code is formatted with `black`
- ✅ No linting errors from `ruff`
- ✅ Docstrings updated
- ✅ Feature documented in README

---

## 🗺️ Roadmap

- [ ] Categorical feature drift detection
- [ ] Custom SHAP visualization plots (force, dependence)
- [ ] Model card generation (ModelCardToolkit)
- [ ] MLflow & Weights & Biases integration
- [ ] Real-time monitoring API
- [ ] Neural network support (DeepExplainer)
- [ ] GPU acceleration for large datasets

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| 🐢 SHAP is slow | Use `--no-shap` flag or reduce reference data size |
| 📦 Model won't load | Verify sklearn version compatibility. Test with `pickle.load()` manually |
| 📊 Drift detection failing | Ensure reference CSV has numeric columns matching model features |
| 🔧 Import errors | Run `pip install --upgrade mlq` and check dependencies |

---

## 📜 License

MIT License — See [LICENSE](LICENSE) for full details.

Free to use, modify, and distribute in commercial and personal projects.

---

## 👨‍💻 Authors

**Michael Chen** & **Sarah Williams** — 2025

Built with ❤️ for ML engineers everywhere.

---

<div align="center">

### 🎯 Inspect faster. Audit smarter. Deploy with confidence.

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/mlq-inspect?style=social)](https://github.com/yourusername/mlq-inspect)
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/mlq-inspect?style=social)](https://github.com/yourusername/mlq-inspect/issues)

</div>
