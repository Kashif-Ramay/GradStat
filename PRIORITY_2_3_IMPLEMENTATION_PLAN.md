# Priority 2 & 3 Features Implementation Plan

**Date:** October 22, 2025  
**Status:** 🟡 Planning Phase

---

## Overview

After successfully implementing Priority 1 features (Multiple Regression, Non-parametric Tests, Categorical Analysis), we now move to Priority 2 (Moderate Impact) and Priority 3 (Advanced Features).

**Current Coverage:** ~85%  
**Target Coverage:** ~95%

---

## Priority 2: Moderate Impact Features

### 1. ✅ Enhanced Clustering (EASIEST - START HERE!)

**Impact:** High for unsupervised learning research  
**Difficulty:** Low  
**Time Estimate:** 2-3 hours

#### Features to Add:
- **Elbow Method Plot** - Determine optimal number of clusters
- **Silhouette Score** - Measure cluster quality
- **Hierarchical Clustering** - Dendrogram visualization
- **Multiple Distance Metrics** - Euclidean, Manhattan, Cosine

#### Implementation:
```python
# In analysis_functions.py
def enhanced_clustering(df, opts):
    # Elbow method
    inertias = []
    silhouette_scores = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))
    
    # Plot elbow curve
    # Plot silhouette scores
    
    # Hierarchical clustering
    from scipy.cluster.hierarchy import dendrogram, linkage
    linkage_matrix = linkage(X, method='ward')
    # Plot dendrogram
```

#### Frontend Changes:
- Add "Clustering Method" dropdown: K-Means, Hierarchical
- Add "Show Elbow Plot" checkbox
- Add "Distance Metric" selector

---

### 2. ✅ Enhanced Logistic Regression (MEDIUM)

**Impact:** High for classification research  
**Difficulty:** Medium  
**Time Estimate:** 3-4 hours

#### Features to Add:
- **Odds Ratios** with confidence intervals
- **Confusion Matrix** visualization
- **ROC Curve** with AUC
- **Classification Report** (precision, recall, F1)
- **Hosmer-Lemeshow Test** for goodness of fit

#### Implementation:
```python
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from sklearn.linear_model import LogisticRegression

def enhanced_classification(df, opts):
    # Fit logistic regression
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Odds ratios
    odds_ratios = np.exp(model.coef_[0])
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    # Plot confusion matrix heatmap
    # Plot ROC curve
```

#### Frontend Changes:
- Rename "Classification" to "Logistic Regression"
- Add target variable selector
- Add train/test split ratio slider

---

### 3. ⚠️ Enhanced Time Series (COMPLEX)

**Impact:** High for longitudinal research  
**Difficulty:** High  
**Time Estimate:** 6-8 hours

#### Features to Add:
- **ARIMA/SARIMA Models** - Forecasting
- **Seasonal Decomposition** - Trend, seasonal, residual
- **Stationarity Tests** - ADF test, KPSS test
- **ACF/PACF Plots** - Autocorrelation analysis
- **Forecasting** with confidence intervals

#### Implementation:
```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss

def enhanced_time_series(df, opts):
    # Stationarity tests
    adf_result = adfuller(ts)
    kpss_result = kpss(ts)
    
    # Seasonal decomposition
    decomposition = seasonal_decompose(ts, model='additive', period=12)
    
    # ARIMA model
    model = ARIMA(ts, order=(1,1,1))
    fitted = model.fit()
    
    # Forecast
    forecast = fitted.forecast(steps=12)
    
    # Plot decomposition
    # Plot ACF/PACF
    # Plot forecast with confidence intervals
```

#### Frontend Changes:
- Add "Time Series Method" dropdown: Basic, ARIMA, Decomposition
- Add "Date Column" selector
- Add "Frequency" selector: Daily, Weekly, Monthly, Yearly
- Add "Forecast Periods" input

---

## Priority 3: Advanced Features

### 4. ⚠️ Mixed-Effects Models (VERY COMPLEX)

**Impact:** High for hierarchical/nested data  
**Difficulty:** Very High  
**Time Estimate:** 8-10 hours

#### Features to Add:
- **Linear Mixed Models (LMM)** - Random effects
- **Generalized Linear Mixed Models (GLMM)**
- **Random intercepts and slopes**
- **ICC calculation** - Intraclass correlation

#### Implementation:
```python
from statsmodels.regression.mixed_linear_model import MixedLM

def mixed_effects_model(df, opts):
    # Fit mixed model
    model = MixedLM(y, X, groups=groups)
    result = model.fit()
    
    # Calculate ICC
    # Extract random effects
    # Plot random effects
```

#### Frontend Changes:
- Add "Mixed-Effects Model" analysis type
- Add "Grouping Variable" selector
- Add "Random Effects" multi-select

---

### 5. ✅ Power Analysis (MEDIUM)

**Impact:** High for study design  
**Difficulty:** Medium  
**Time Estimate:** 4-5 hours

#### Features to Add:
- **Sample Size Calculation** - For t-tests, ANOVA, regression
- **Power Calculation** - Given sample size and effect size
- **Effect Size Estimation** - From pilot data
- **Power Curves** - Visualization

#### Implementation:
```python
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower

def power_analysis(opts):
    # T-test power
    power_analysis = TTestIndPower()
    sample_size = power_analysis.solve_power(
        effect_size=0.5,
        alpha=0.05,
        power=0.8
    )
    
    # Plot power curve
```

#### Frontend Changes:
- Add "Power Analysis" analysis type
- Add inputs: effect size, alpha, power, sample size
- Add "Calculate" dropdown: Sample Size, Power, Effect Size

---

### 6. ❌ Survival Analysis (VERY COMPLEX - SKIP FOR NOW)

**Impact:** High for medical research  
**Difficulty:** Very High  
**Time Estimate:** 10-12 hours

**Recommendation:** Skip for now, implement in future version

---

### 7. ❌ Bayesian Methods (VERY COMPLEX - SKIP FOR NOW)

**Impact:** Moderate for advanced research  
**Difficulty:** Very High  
**Time Estimate:** 12-15 hours

**Recommendation:** Skip for now, implement in future version

---

## Recommended Implementation Order

### Phase 1: Quick Wins (Week 1)
1. ✅ **Enhanced Clustering** (2-3 hours) - Elbow, Silhouette, Hierarchical
2. ✅ **Power Analysis** (4-5 hours) - Sample size calculations

**Total Time:** 6-8 hours  
**Coverage Increase:** +5%

---

### Phase 2: High-Value Features (Week 2)
3. ✅ **Enhanced Logistic Regression** (3-4 hours) - Odds ratios, ROC, Confusion matrix
4. ⚠️ **Enhanced Time Series** (6-8 hours) - ARIMA, Decomposition

**Total Time:** 9-12 hours  
**Coverage Increase:** +8%

---

### Phase 3: Advanced Features (Week 3+)
5. ⚠️ **Mixed-Effects Models** (8-10 hours) - If needed
6. ❌ **Survival Analysis** (10-12 hours) - Future version
7. ❌ **Bayesian Methods** (12-15 hours) - Future version

**Total Time:** 8-10 hours (if doing mixed-effects only)  
**Coverage Increase:** +2%

---

## Expected Outcomes

### After Priority 2 Implementation:
- **Coverage:** 85% → 93%
- **Accuracy Score:** 92/100 → 95/100
- **Research Field Coverage:**
  - Psychology/Social Sciences: 90% → 95%
  - Health/Medical Research: 80% → 88%
  - Education Research: 95% → 98%
  - Biology/Ecology: 85% → 92%
  - Economics/Business: 60% → 75%

### After Priority 3 (Partial) Implementation:
- **Coverage:** 93% → 95%
- **Accuracy Score:** 95/100 → 97/100

---

## Technical Requirements

### New Python Dependencies:
```python
# Already have:
# - scipy
# - statsmodels
# - scikit-learn
# - pandas
# - numpy

# May need to add:
# - pmdarima (for auto-ARIMA)
# - lifelines (for survival analysis - if implementing)
# - pymc (for Bayesian - if implementing)
```

### Frontend Updates:
- Add 3-4 new analysis types
- Update existing analysis types (clustering, classification)
- Add new parameter inputs
- Update results display for new outputs

---

## Detailed Implementation: Phase 1 (START HERE!)

### 1. Enhanced Clustering

#### Backend Changes:

**File:** `worker/analysis_functions.py`

```python
def enhanced_clustering_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Enhanced clustering with elbow method and silhouette analysis"""
    from sklearn.cluster import KMeans, AgglomerativeClustering
    from sklearn.metrics import silhouette_score, silhouette_samples
    from scipy.cluster.hierarchy import dendrogram, linkage
    
    n_clusters = opts.get('nClusters', 3)
    method = opts.get('method', 'kmeans')  # 'kmeans' or 'hierarchical'
    show_elbow = opts.get('showElbow', True)
    
    # Prepare data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    X = df[numeric_cols].dropna().values
    X_scaled = StandardScaler().fit_transform(X)
    
    plots = []
    
    # Elbow method
    if show_elbow:
        inertias = []
        silhouette_scores = []
        K_range = range(2, min(11, len(X)))
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
        
        # Plot elbow curve
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        ax1.plot(K_range, inertias, 'bo-')
        ax1.set_xlabel('Number of Clusters (k)')
        ax1.set_ylabel('Inertia (Within-cluster sum of squares)')
        ax1.set_title('Elbow Method')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(K_range, silhouette_scores, 'ro-')
        ax2.set_xlabel('Number of Clusters (k)')
        ax2.set_ylabel('Silhouette Score')
        ax2.set_title('Silhouette Analysis')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plots.append({
            "title": "Optimal Clusters Analysis",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
    
    # Perform clustering
    if method == 'kmeans':
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = model.fit_predict(X_scaled)
        centers = model.cluster_centers_
    else:  # hierarchical
        model = AgglomerativeClustering(n_clusters=n_clusters)
        labels = model.fit_predict(X_scaled)
        
        # Create dendrogram
        fig, ax = plt.subplots(figsize=(12, 6))
        linkage_matrix = linkage(X_scaled, method='ward')
        dendrogram(linkage_matrix, ax=ax)
        ax.set_title('Hierarchical Clustering Dendrogram')
        ax.set_xlabel('Sample Index')
        ax.set_ylabel('Distance')
        plots.append({
            "title": "Dendrogram",
            "type": "dendrogram",
            "base64": plot_to_base64(fig)
        })
    
    # Calculate silhouette score for chosen k
    silhouette_avg = silhouette_score(X_scaled, labels)
    silhouette_vals = silhouette_samples(X_scaled, labels)
    
    # Silhouette plot
    fig, ax = plt.subplots(figsize=(10, 6))
    y_lower = 10
    for i in range(n_clusters):
        cluster_silhouette_vals = silhouette_vals[labels == i]
        cluster_silhouette_vals.sort()
        
        size_cluster_i = cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i
        
        color = plt.cm.nipy_spectral(float(i) / n_clusters)
        ax.fill_betweenx(np.arange(y_lower, y_upper),
                         0, cluster_silhouette_vals,
                         facecolor=color, edgecolor=color, alpha=0.7)
        
        ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10
    
    ax.set_title(f'Silhouette Plot (avg = {silhouette_avg:.3f})')
    ax.set_xlabel('Silhouette Coefficient')
    ax.set_ylabel('Cluster')
    ax.axvline(x=silhouette_avg, color="red", linestyle="--", label='Average')
    ax.legend()
    plots.append({
        "title": "Silhouette Plot",
        "type": "silhouette",
        "base64": plot_to_base64(fig)
    })
    
    # ... rest of clustering visualization (existing code)
    
    test_results = {
        "n_clusters": n_clusters,
        "method": method,
        "silhouette_score": float(silhouette_avg),
        "cluster_sizes": {f"Cluster {i}": int(np.sum(labels == i)) for i in range(n_clusters)}
    }
    
    if method == 'kmeans':
        test_results["inertia"] = float(model.inertia_)
    
    interpretation = f"{method.title()} clustering identified {n_clusters} distinct groups. "
    interpretation += f"Silhouette score of {silhouette_avg:.3f} indicates "
    if silhouette_avg > 0.7:
        interpretation += "strong cluster structure."
    elif silhouette_avg > 0.5:
        interpretation += "reasonable cluster structure."
    elif silhouette_avg > 0.25:
        interpretation += "weak cluster structure."
    else:
        interpretation += "poor cluster structure. Consider different number of clusters."
    
    result = {
        "analysis_type": "clustering",
        "summary": f"{method.title()} clustering with k={n_clusters} (Silhouette = {silhouette_avg:.3f})",
        "test_results": test_results,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("clustering", opts),
        "recommendations": [
            f"Optimal k suggested by elbow method: Check the elbow plot",
            f"Silhouette score: {silhouette_avg:.3f} ({'good' if silhouette_avg > 0.5 else 'consider adjusting k'})"
        ]
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)
```

#### Frontend Changes:

**File:** `frontend/src/components/AnalysisSelector.tsx`

```typescript
{analysisType === 'clustering' && (
  <>
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Clustering Method
      </label>
      <select
        value={options.method || 'kmeans'}
        onChange={(e) => updateOption('method', e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
      >
        <option value="kmeans">K-Means</option>
        <option value="hierarchical">Hierarchical</option>
      </select>
    </div>
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Number of Clusters
      </label>
      <input
        type="number"
        min="2"
        max="10"
        value={options.nClusters || 3}
        onChange={(e) => updateOption('nClusters', parseInt(e.target.value))}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
      />
    </div>
    <div className="mb-4">
      <label className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={options.showElbow !== false}
          onChange={(e) => updateOption('showElbow', e.target.checked)}
          className="rounded border-gray-300"
        />
        <span className="text-sm text-gray-700">Show elbow method analysis</span>
      </label>
    </div>
  </>
)}
```

---

### 2. Power Analysis

#### Backend Changes:

**File:** `worker/analysis_functions.py`

```python
def power_analysis(opts: Dict) -> Dict:
    """Perform power analysis for sample size or power calculation"""
    from statsmodels.stats.power import TTestIndPower, FTestAnovaPower, FTestPower
    
    analysis_type = opts.get('powerAnalysisType', 't-test')  # 't-test', 'anova', 'regression'
    calculate = opts.get('calculate', 'sample_size')  # 'sample_size', 'power', 'effect_size'
    
    effect_size = opts.get('effectSize', 0.5)
    alpha = opts.get('alpha', 0.05)
    power = opts.get('power', 0.8)
    sample_size = opts.get('sampleSize', 30)
    
    plots = []
    
    if analysis_type == 't-test':
        power_analysis = TTestIndPower()
        
        if calculate == 'sample_size':
            result_value = power_analysis.solve_power(
                effect_size=effect_size,
                alpha=alpha,
                power=power,
                ratio=1.0,
                alternative='two-sided'
            )
            result_label = "Required Sample Size per Group"
        elif calculate == 'power':
            result_value = power_analysis.solve_power(
                effect_size=effect_size,
                nobs1=sample_size,
                alpha=alpha,
                ratio=1.0,
                alternative='two-sided'
            )
            result_label = "Statistical Power"
        else:  # effect_size
            result_value = power_analysis.solve_power(
                nobs1=sample_size,
                alpha=alpha,
                power=power,
                ratio=1.0,
                alternative='two-sided'
            )
            result_label = "Detectable Effect Size (Cohen's d)"
        
        # Power curve
        fig, ax = plt.subplots(figsize=(10, 6))
        sample_sizes = np.arange(10, 200, 5)
        powers = [power_analysis.solve_power(effect_size=effect_size, nobs1=n, alpha=alpha) 
                  for n in sample_sizes]
        
        ax.plot(sample_sizes, powers, 'b-', linewidth=2)
        ax.axhline(y=0.8, color='r', linestyle='--', label='Power = 0.80')
        ax.axhline(y=power, color='g', linestyle='--', label=f'Target Power = {power}')
        ax.set_xlabel('Sample Size per Group')
        ax.set_ylabel('Statistical Power')
        ax.set_title(f'Power Curve (Effect Size = {effect_size}, α = {alpha})')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plots.append({
            "title": "Power Curve",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
    
    test_results = {
        "analysis_type": analysis_type,
        "calculate": calculate,
        "result_value": float(result_value),
        "result_label": result_label,
        "effect_size": effect_size,
        "alpha": alpha,
        "power": power if calculate != 'power' else result_value,
        "sample_size": sample_size if calculate != 'sample_size' else result_value
    }
    
    interpretation = f"For a {analysis_type} with effect size = {effect_size}, α = {alpha}: "
    if calculate == 'sample_size':
        interpretation += f"You need approximately {int(np.ceil(result_value))} participants per group to achieve {power*100:.0f}% power."
    elif calculate == 'power':
        interpretation += f"With {sample_size} participants per group, you have {result_value*100:.1f}% power to detect the effect."
    else:
        interpretation += f"With {sample_size} participants per group and {power*100:.0f}% power, you can detect an effect size of {result_value:.3f} or larger."
    
    result = {
        "analysis_type": "power_analysis",
        "summary": f"Power Analysis: {result_label} = {result_value:.2f}",
        "test_results": test_results,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_power_analysis_code(opts),
        "recommendations": [
            "Consider pilot studies to estimate effect sizes",
            "Account for dropout rates in sample size calculations",
            "Higher power (0.90) recommended for critical studies"
        ]
    }
    result["conclusion"] = f"Based on power analysis, {interpretation}"
    return convert_to_python_types(result)
```

---

## Summary

### Immediate Next Steps:

1. **✅ Implement Enhanced Clustering** (2-3 hours)
   - Elbow method
   - Silhouette analysis
   - Hierarchical clustering

2. **✅ Implement Power Analysis** (4-5 hours)
   - Sample size calculations
   - Power curves
   - Effect size estimation

3. **✅ Implement Enhanced Logistic Regression** (3-4 hours)
   - Odds ratios
   - ROC curves
   - Confusion matrix

4. **⚠️ Consider Enhanced Time Series** (6-8 hours)
   - ARIMA models
   - Seasonal decomposition
   - Forecasting

**Total Estimated Time:** 15-20 hours for Priority 2  
**Expected Coverage Increase:** 85% → 93%

---

**Ready to start with Enhanced Clustering?** It's the quickest win! 🚀
