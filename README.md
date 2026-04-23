<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;900&display=swap');

.mlq-hero {
  background: linear-gradient(135deg, #001F3F 0%, #000000 50%, #001F3F 100%);
  padding: 60px 40px;
  border-radius: 12px;
  text-align: center;
  margin: 30px 0;
  box-shadow: 0 8px 32px rgba(255, 0, 0, 0.2);
  overflow: hidden;
  position: relative;
}

.mlq-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 0, 0, 0.1), transparent);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

@keyframes glow-pulse {
  0%, 100% { text-shadow: 0 0 10px rgba(255, 0, 0, 0.5), 0 0 20px rgba(255, 0, 0, 0.3); }
  50% { text-shadow: 0 0 20px rgba(255, 0, 0, 0.8), 0 0 40px rgba(255, 0, 0, 0.5); }
}

@keyframes slide-in {
  0% { transform: translateX(-100%); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}

@keyframes type {
  0% { width: 0; }
  100% { width: 100%; }
}

.mlq-title {
  font-family: 'Poppins', sans-serif;
  font-size: 48px;
  font-weight: 900;
  color: #FF0000;
  margin: 0;
  animation: glow-pulse 2s ease-in-out infinite;
  letter-spacing: 2px;
  text-transform: uppercase;
  z-index: 1;
  position: relative;
}

.mlq-subtitle {
  font-family: 'Poppins', sans-serif;
  color: #E8E8E8;
  font-size: 18px;
  margin-top: 15px;
  font-weight: 300;
  animation: slide-in 0.8s ease-out;
}

.mlq-badges {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
  animation: slide-in 1.2s ease-out;
  z-index: 1;
  position: relative;
}

.mlq-badge {
  background: rgba(255, 0, 0, 0.15);
  border: 2px solid #FF0000;
  color: #FF0000;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.mlq-cta {
  background: linear-gradient(135deg, #FF0000, #B30000);
  color: white;
  padding: 14px 32px;
  border-radius: 8px;
  font-weight: 700;
  display: inline-block;
  margin-top: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  text-transform: uppercase;
  font-size: 14px;
  letter-spacing: 1px;
  animation: slide-in 1.4s ease-out;
  z-index: 1;
  position: relative;
}

.mlq-cta:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 24px rgba(255, 0, 0, 0.4);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 40px;
  margin-bottom: 20px;
}

.section-icon {
  width: 32px;
  height: 32px;
  background: #FF0000;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
}

.section-title {
  color: #001F3F;
  font-family: 'Poppins', sans-serif;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  letter-spacing: 0.5px;
}

.code-block {
  background: #0D0D0D;
  border-left: 4px solid #FF0000;
  color: #00FF41;
  padding: 16px;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  margin: 15px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.feature-card {
  background: linear-gradient(135deg, rgba(0, 31, 63, 0.1) 0%, rgba(0, 0, 0, 0.05) 100%);
  border: 2px solid rgba(255, 0, 0, 0.2);
  padding: 24px;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.feature-card:hover {
  border-color: #FF0000;
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(255, 0, 0, 0.15);
}

.feature-card h4 {
  color: #FF0000;
  margin-top: 0;
  font-family: 'Poppins', sans-serif;
}

.feature-card p {
  color: #333;
  margin-bottom: 0;
  line-height: 1.6;
}

.divider {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, #001F3F, #FF0000, #001F3F);
  margin: 40px 0;
}

.stat-box {
  background: #001F3F;
  color: #FF0000;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  margin: 15px 0;
  border: 2px solid #FF0000;
}

strong {
  color: #001F3F;
}

code {
  background: rgba(255, 0, 0, 0.1);
  color: #FF0000;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

a {
  color: #001F3F;
  text-decoration: none;
  border-bottom: 2px solid #FF0000;
  transition: all 0.3s;
}

a:hover {
  color: #FF0000;
}
</style>

<div class="mlq-hero">
  <h1 class="mlq-title">⚡ MLQ</h1>
  <p class="mlq-subtitle">ML Model Inspector CLI — Inspect, Explain & Audit in One Command</p>
  <div class="mlq-badges">
    <span class="mlq-badge">v0.1.0</span>
    <span class="mlq-badge">Python 3.10+</span>
    <span class="mlq-badge">MIT License</span>
  </div>
</div>

**mlq** is a production-quality Python CLI tool that lets any ML engineer inspect, explain, and audit a trained sklearn-compatible model from the terminal in one command. No Jupyter. No boilerplate. Just raw power:

<div class="code-block">$ mlq inspect model.pkl</div>

<hr class="divider">

<div class="section-header">
  <div class="section-icon">📦</div>
  <h2 class="section-title">Installation</h2>
</div>

**Install from PyPI:**

<div class="code-block">pip install mlq</div>

**Or from source with dev dependencies:**

<div class="code-block">git clone https://github.com/yourusername/mlq.git
cd mlq
pip install -e ".[dev]"</div>

<hr class="divider">

<div class="section-header">
  <div class="section-icon">🚀</div>
  <h2 class="section-title">Quick Start</h2>
</div>

<div class="feature-grid">
  <div class="feature-card">
    <h4>📊 Inspect a Model</h4>
    <div class="code-block">mlq inspect model.pkl</div>
    <p>Load any sklearn model and get instant feature importance, metadata, and predictions.</p>
  </div>

  <div class="feature-card">
    <h4>🔍 Check Data Drift</h4>
    <div class="code-block">mlq inspect model.pkl \
  --ref training_data.csv \
  --target target_col</div>
    <p>Detect distribution shifts. KS-test + PSI metrics per feature.</p>
  </div>

  <div class="feature-card">
    <h4>⚖️ Compare Models</h4>
    <div class="code-block">mlq compare model_v1.pkl \
  model_v2.pkl</div>
    <p>Side-by-side: features, classes, and top-5 SHAP importance.</p>
  </div>

  <div class="feature-card">
    <h4>📄 Generate Reports</h4>
    <div class="code-block">mlq report model.pkl \
  --output report.html</div>
    <p>Standalone HTML with embedded SHAP charts and full model analysis.</p>
  </div>

  <div class="feature-card">
    <h4>🔗 Version Check</h4>
    <div class="code-block">mlq version</div>
    <p>View MLQ, Python, and dependency versions instantly.</p>
  </div>

  <div class="feature-card">
    <h4>⚡ Production Ready</h4>
    <p>Optimized sklearn support. Automatic explainer selection.</p>
  </div>
</div>

**Example Output:**

<div class="code-block">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃              RandomForestClassifier           ┃
┃  📌 Features: 10  📌 Classes: 2  📌 Trees: 100┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Feature Importance (SHAP - Top 10)
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Feature       ┃ Mean SHAP ┃ Importance     ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ feature_3     │ 0.4215    │ ████████████   │
│ feature_7     │ 0.3184    │ █████████      │
│ feature_1     │ 0.2456    │ ███████        │
└───────────────┴───────────┴────────────────┘</div>

<hr class="divider">

## Command Reference

### `mlq inspect <model_path>`

**Primary command.** Loads a model and prints its full inspection report.

**Options:**
- `--ref PATH` — Path to reference CSV for drift check (optional)
- `--target TEXT` — Target column name in CSV (default: `"target"`)
- `--output PATH` — Save report as `.md` or `.html` (auto-detects by extension)
- `--no-shap` — Skip SHAP computation for large models

<div class="stat-box">
  Estimator Auto-Detection: Tree-based ➜ TreeExplainer | Linear ➜ LinearExplainer | Other ➜ KernelExplainer
</div>

### `mlq compare <model_a> <model_b>`

Side-by-side model comparison in rich tables.

**Options:**
- `--ref PATH` — Reference CSV for metric comparison
- `--target TEXT` — Target column name (default: `"target"`)

### `mlq report <model_path>`

Generate standalone HTML or Markdown reports.

**Options:**
- `--output PATH` — (required) e.g., `report.html` or `report.md`
- `--ref PATH` — Reference data for drift analysis
- `--target TEXT` — Target column name

### `mlq version`

Print MLQ, Python, and dependency versions.

<hr class="divider">

<div class="section-header">
  <div class="section-icon">🧠</div>
  <h2 class="section-title">How SHAP Explainability Works</h2>
</div>

[SHAP (SHapley Additive exPlanations)](https://github.com/slundberg/shap) is a game-theoretic approach to explaining ML predictions. It computes **Shapley values**, representing each feature's fair contribution to predictions.

<div class="stat-box">
  🎯 Auto-Selects Best Explainer Based on Model Type
</div>

1. **Tree-based** → `TreeExplainer` (C++ optimized, fastest)
2. **Linear** → `LinearExplainer` (fast closedform)
3. **Other** → `KernelExplainer` (model-agnostic, slower)

**Result:** Mean absolute SHAP value per feature, ranked by importance. For multiclass: SHAP values averaged across all classes.

<hr class="divider">

<div class="section-header">
  <div class="section-icon">📡</div>
  <h2 class="section-title">How Drift Detection Works</h2>
</div>

Detect when input/output distributions shift compared to reference data (e.g., training set). Early warning that retraining may be needed.

**Two Metrics Per Feature:**

1. **Kolmogorov-Smirnov (KS) Test** — Non-parametric two-sample test  
   - p-value < 0.05 → ⚠ Signal of drift

2. **Population Stability Index (PSI)** — Magnitude of shift  
   - PSI < 0.1 → ✅ No drift  
   - PSI 0.1–0.25 → ⚠ Warning  
   - PSI ≥ 0.25 → 🔴 Significant drift

*Numeric features only by default. Categorical features can be manually encoded.*

<hr class="divider">

<div class="section-header">
  <div class="section-icon">🤝</div>
  <h2 class="section-title">Contributing</h2>
</div>

Contributions welcome! Follow these steps:

<div class="code-block">git checkout -b feature/my-feature
pip install -e ".[dev]"
pytest tests/
ruff check mlq/
black mlq/</div>

Then open a pull request. **Before submitting:**
- ✅ All tests pass
- ✅ Code linted with ruff
- ✅ Code formatted with black
- ✅ Feature documented

<hr class="divider">

<div class="section-header">
  <div class="section-icon">📜</div>
  <h2 class="section-title">License & Roadmap</h2>
</div>

**License:** MIT — See [LICENSE](LICENSE)

**🗺️ Future Features:**
- [ ] Categorical feature drift support
- [ ] Custom SHAP plots (force, dependence)
- [ ] Model card generation
- [ ] MLflow/W&B integration
- [ ] Streaming data monitoring
- [ ] Neural network support (DeepExplainer)

<hr class="divider">

<div class="section-header">
  <div class="section-icon">❓</div>
  <h2 class="section-title">Troubleshooting</h2>
</div>

**❌ SHAP computation is slow**  
→ Use `--no-shap` flag or reduce reference data size

**❌ Model won't load**  
→ Check sklearn version compatibility. Try `pickle.load()` manually.

**❌ Drift detection fails**  
→ Ensure reference CSV has numeric columns matching model features

<hr class="divider">

<div style="text-align: center; padding: 40px; background: linear-gradient(135deg, rgba(0,31,63,0.05) 0%, rgba(0,0,0,0.02) 100%); border-radius: 12px; margin-top: 50px;">
  <h3 style="color: #001F3F; font-family: 'Poppins', sans-serif; margin-top: 0;">👨‍💻 Built by ML Engineers, for ML Engineers</h3>
  <p style="color: #666; margin: 0;">Made with ❤️ by Michael Chen, Sarah Williams — 2025</p>
  <p style="color: #999; font-size: 12px; margin-top: 15px;">Inspect faster. Audit smarter. Deploy with confidence.</p>
</div>
