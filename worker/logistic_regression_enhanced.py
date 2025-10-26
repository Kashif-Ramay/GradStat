"""
Enhanced Logistic Regression Analysis with ROC, Confusion Matrix, and Classification Metrics
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, roc_auc_score,
    accuracy_score, precision_score, recall_score, f1_score
)
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Dict, Any


def plot_to_base64(fig) -> str:
    """Convert matplotlib figure to base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img_base64


def logistic_regression_analysis(df: pd.DataFrame, opts: Dict) -> Dict[str, Any]:
    """
    Perform enhanced logistic regression with ROC curve, confusion matrix, and classification metrics
    
    Parameters:
    - target_column: Binary target variable (0/1 or categorical with 2 classes)
    - predictor_columns: List of predictor variables
    - test_size: Proportion of data for testing (default 0.3)
    - random_state: Random seed for reproducibility (default 42)
    """
    
    target_col = opts.get('targetColumn')
    predictor_cols = opts.get('predictorColumns', [])
    test_size = float(opts.get('testSize', 0.3))
    random_state = int(opts.get('randomState', 42))
    
    if not target_col or not predictor_cols:
        raise ValueError("Target column and at least one predictor column are required")
    
    # Prepare data
    X = df[predictor_cols].copy()
    y = df[target_col].copy()
    
    # Handle missing values
    X = X.dropna()
    y = y[X.index]
    
    # Convert target to binary if categorical
    if y.dtype == 'object' or y.dtype.name == 'category':
        unique_vals = y.unique()
        if len(unique_vals) != 2:
            raise ValueError(f"Target must be binary. Found {len(unique_vals)} unique values")
        y = (y == unique_vals[1]).astype(int)
        class_names = [str(unique_vals[0]), str(unique_vals[1])]
    else:
        unique_vals = y.unique()
        if len(unique_vals) != 2:
            raise ValueError(f"Target must be binary. Found {len(unique_vals)} unique values")
        class_names = [str(int(v)) for v in sorted(unique_vals)]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Train logistic regression model
    model = LogisticRegression(random_state=random_state, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    # Find optimal threshold (Youden's J statistic)
    j_scores = tpr - fpr
    optimal_idx = np.argmax(j_scores)
    optimal_threshold = thresholds[optimal_idx]
    
    # Plots
    plots = []
    
    # 1. ROC Curve
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc_score:.3f})')
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    ax.scatter(fpr[optimal_idx], tpr[optimal_idx], marker='o', color='red', s=100, 
               label=f'Optimal Threshold = {optimal_threshold:.3f}', zorder=3)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=12)
    ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=12)
    ax.set_title('Receiver Operating Characteristic (ROC) Curve', fontsize=14, fontweight='bold')
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, alpha=0.3)
    plots.append({
        "title": "ROC Curve",
        "type": "line",
        "base64": plot_to_base64(fig)
    })
    
    # 2. Confusion Matrix Heatmap
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True, 
                xticklabels=class_names, yticklabels=class_names, ax=ax,
                annot_kws={'size': 14, 'weight': 'bold'})
    ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
    ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    
    # Add text annotations for clarity
    ax.text(0.5, -0.15, f'TN={tn}  FP={fp}  FN={fn}  TP={tp}', 
            ha='center', transform=ax.transAxes, fontsize=10, style='italic')
    
    plots.append({
        "title": "Confusion Matrix",
        "type": "heatmap",
        "base64": plot_to_base64(fig)
    })
    
    # 3. Feature Importance (Coefficients)
    coefficients = pd.DataFrame({
        'Feature': predictor_cols,
        'Coefficient': model.coef_[0],
        'Abs_Coefficient': np.abs(model.coef_[0])
    }).sort_values('Abs_Coefficient', ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, max(6, len(predictor_cols) * 0.4)))
    colors = ['green' if c > 0 else 'red' for c in coefficients['Coefficient']]
    ax.barh(coefficients['Feature'], coefficients['Coefficient'], color=colors, alpha=0.7)
    ax.set_xlabel('Coefficient Value', fontsize=12, fontweight='bold')
    ax.set_ylabel('Features', fontsize=12, fontweight='bold')
    ax.set_title('Feature Importance (Logistic Regression Coefficients)', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax.grid(True, alpha=0.3, axis='x')
    plots.append({
        "title": "Feature Importance",
        "type": "bar",
        "base64": plot_to_base64(fig)
    })
    
    # 4. Prediction Probability Distribution
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(y_pred_proba[y_test == 0], bins=30, alpha=0.6, label=f'Class {class_names[0]}', color='blue')
    ax.hist(y_pred_proba[y_test == 1], bins=30, alpha=0.6, label=f'Class {class_names[1]}', color='orange')
    ax.axvline(x=0.5, color='red', linestyle='--', linewidth=2, label='Default Threshold (0.5)')
    ax.axvline(x=optimal_threshold, color='green', linestyle='--', linewidth=2, 
               label=f'Optimal Threshold ({optimal_threshold:.3f})')
    ax.set_xlabel('Predicted Probability', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Predicted Probabilities', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plots.append({
        "title": "Probability Distribution",
        "type": "histogram",
        "base64": plot_to_base64(fig)
    })
    
    # Test results
    test_results = {
        "model_type": "Logistic Regression",
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "n_predictors": len(predictor_cols),
        "target_variable": target_col,
        "predictor_variables": predictor_cols,
        "class_names": class_names,
        
        # Classification Metrics
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "specificity": float(specificity),
        "auc_score": float(auc_score),
        
        # Confusion Matrix
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        
        # Thresholds
        "default_threshold": 0.5,
        "optimal_threshold": float(optimal_threshold),
        
        # Model Coefficients
        "intercept": float(model.intercept_[0]),
        "coefficients": {col: float(coef) for col, coef in zip(predictor_cols, model.coef_[0])}
    }
    
    # Interpretation
    interpretation = f"""
**Model Performance Summary:**

The logistic regression model achieved an **accuracy of {accuracy*100:.1f}%** on the test set ({len(X_test)} observations).

**Key Metrics:**
- **AUC-ROC**: {auc_score:.3f} - {'Excellent' if auc_score >= 0.9 else 'Good' if auc_score >= 0.8 else 'Fair' if auc_score >= 0.7 else 'Poor'} discrimination ability
- **Precision**: {precision*100:.1f}% - Of predicted positives, {precision*100:.1f}% were actually positive
- **Recall (Sensitivity)**: {recall*100:.1f}% - Detected {recall*100:.1f}% of actual positives
- **Specificity**: {specificity*100:.1f}% - Correctly identified {specificity*100:.1f}% of actual negatives
- **F1-Score**: {f1:.3f} - Balanced measure of precision and recall

**Confusion Matrix:**
- True Positives (TP): {tp} - Correctly predicted positive cases
- True Negatives (TN): {tn} - Correctly predicted negative cases
- False Positives (FP): {fp} - Incorrectly predicted as positive (Type I error)
- False Negatives (FN): {fn} - Incorrectly predicted as negative (Type II error)

**Optimal Threshold:** {optimal_threshold:.3f} (vs. default 0.5)
Using this threshold maximizes the balance between sensitivity and specificity.
"""
    
    # Recommendations
    recommendations = []
    
    if auc_score < 0.7:
        recommendations.append("⚠️ Low AUC score suggests poor model performance. Consider:")
        recommendations.append("  - Adding more relevant features")
        recommendations.append("  - Checking for data quality issues")
        recommendations.append("  - Trying different algorithms (Random Forest, XGBoost)")
    elif auc_score < 0.8:
        recommendations.append("Model shows fair performance. Consider feature engineering to improve results.")
    else:
        recommendations.append("✅ Model shows good discrimination ability.")
    
    if precision < 0.7:
        recommendations.append("⚠️ Low precision - many false positives. Consider:")
        recommendations.append("  - Increasing classification threshold")
        recommendations.append("  - Balancing the dataset if imbalanced")
    
    if recall < 0.7:
        recommendations.append("⚠️ Low recall - missing many positive cases. Consider:")
        recommendations.append("  - Decreasing classification threshold")
        recommendations.append("  - Collecting more positive examples")
    
    if abs(len(y_train[y_train==1]) / len(y_train) - 0.5) > 0.3:
        recommendations.append("⚠️ Class imbalance detected. Consider using class weights or resampling techniques.")
    
    recommendations.append(f"💡 Use optimal threshold ({optimal_threshold:.3f}) for better balanced predictions.")
    recommendations.append("📊 Review feature coefficients to understand variable importance.")
    
    # Code snippet
    code_snippet = f"""
# Logistic Regression with ROC and Confusion Matrix
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

# Prepare data
X = df[{predictor_cols}]
y = df['{target_col}']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size={test_size}, random_state={random_state}, stratify=y
)

# Train model
model = LogisticRegression(random_state={random_state}, max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluate
auc = roc_auc_score(y_test, y_pred_proba)
cm = confusion_matrix(y_test, y_pred)
print(f"AUC-ROC: {{auc:.3f}}")
print("\\nConfusion Matrix:")
print(cm)
print("\\nClassification Report:")
print(classification_report(y_test, y_pred))
"""
    
    result = {
        "analysis_type": "logistic_regression",
        "summary": f"Logistic Regression: Accuracy = {accuracy*100:.1f}%, AUC = {auc_score:.3f}",
        "test_results": test_results,
        "plots": plots,
        "interpretation": interpretation.strip(),
        "code_snippet": code_snippet.strip(),
        "recommendations": recommendations,
        "conclusion": f"The logistic regression model achieved {accuracy*100:.1f}% accuracy with an AUC of {auc_score:.3f}, indicating {'excellent' if auc_score >= 0.9 else 'good' if auc_score >= 0.8 else 'fair' if auc_score >= 0.7 else 'poor'} predictive performance."
    }
    
    return result
