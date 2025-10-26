# 📖 GradStat User Guide

> **Complete guide to using GradStat for statistical analysis**

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Uploading Data](#uploading-data)
3. [Using Test Advisor](#using-test-advisor)
4. [Running Analyses](#running-analyses)
5. [Understanding Results](#understanding-results)
6. [Interactive Visualizations](#interactive-visualizations)
7. [Getting Help](#getting-help)
8. [Common Workflows](#common-workflows)
9. [Tips & Best Practices](#tips--best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Time Setup

1. **Open GradStat** at `http://localhost:3000`
2. **Familiarize yourself** with the interface:
   - **Header**: Navigation and mode switching
   - **Upload Area**: Drag-and-drop or click to upload
   - **Analysis Selector**: Choose your analysis type
   - **Results Area**: View outputs and visualizations

### Interface Overview

```
┌─────────────────────────────────────────────────┐
│  GradStat  [Test Advisor] [Power Analysis]     │  ← Header
├─────────────────────────────────────────────────┤
│  📁 Upload Your Data                            │  ← Upload Area
│  [Choose File] or drag and drop                 │
├─────────────────────────────────────────────────┤
│  📊 Data Preview                                │  ← Preview
│  [Table showing your data]                      │
├─────────────────────────────────────────────────┤
│  🔍 Analysis Options                            │  ← Analysis Selector
│  Analysis Type: [Dropdown]                      │
│  Variables: [Selectors]                         │
│  [Analyze Button]                               │
├─────────────────────────────────────────────────┤
│  📈 Results                                     │  ← Results Area
│  [Visualizations, Statistics, Interpretation]   │
└─────────────────────────────────────────────────┘
```

---

## Uploading Data

### Supported File Formats

- **CSV** (.csv) - Comma-separated values
- **Excel** (.xlsx, .xls) - Microsoft Excel files
- **TSV** (.tsv) - Tab-separated values

### Data Requirements

✅ **Good Data Structure:**
```
subject_id,group,outcome,age
1,control,75,25
2,treatment,82,27
3,control,71,24
```

❌ **Avoid:**
- Merged cells
- Multiple header rows
- Empty columns
- Special characters in column names
- Mixed data types in same column

### Upload Process

1. **Click "Choose File"** or drag-and-drop your file
2. **Wait for preview** (usually < 2 seconds)
3. **Review data quality** score and recommendations
4. **Check column types** (numeric, categorical, date)
5. **Proceed to analysis** or fix data issues

### Data Quality Checks

GradStat automatically checks for:

| Check | What It Looks For | Recommendation |
|-------|-------------------|----------------|
| **Missing Data** | Cells with no value | Remove or impute |
| **Outliers** | Extreme values (>3 SD) | Investigate or remove |
| **Data Types** | Correct type inference | Verify numeric columns |
| **Sample Size** | Adequate n for analysis | Collect more data if needed |
| **Distribution** | Normality for parametric tests | Consider transformations |
| **Correlation** | High correlations (>0.9) | Check for multicollinearity |

**Quality Score Interpretation:**
- **90-100**: Excellent - ready for analysis
- **70-89**: Good - minor issues
- **50-69**: Fair - address warnings
- **< 50**: Poor - fix critical issues first

---

## Using Test Advisor

### When to Use Test Advisor

✅ **Use Test Advisor if:**
- You're unsure which statistical test to use
- You want to learn about appropriate tests
- You need guidance on test selection
- You're new to statistical analysis

### How It Works

1. **Click "Test Advisor"** button in header
2. **Choose research question type:**
   - Compare Groups
   - Find Relationships
   - Predict Outcome
3. **Answer simple questions** about your research
4. **Let GradStat auto-detect** data characteristics
5. **Get personalized recommendation** with confidence level

### Research Question Types

#### 1. Compare Groups
**Example:** "Does treatment improve outcomes?"

**Questions:**
- Is your data normally distributed?
- How many groups are you comparing?
- Are observations paired/repeated?
- Is your outcome continuous or categorical?

**Possible Tests:**
- Independent t-test
- Paired t-test
- One-way ANOVA
- Repeated Measures ANOVA
- Mann-Whitney U
- Kruskal-Wallis H
- Chi-square test

#### 2. Find Relationships
**Example:** "Is age related to blood pressure?"

**Questions:**
- What types of variables do you have?
- How many predictors?

**Possible Tests:**
- Pearson correlation
- Spearman correlation
- Kendall's tau
- Chi-square test
- Simple linear regression

#### 3. Predict Outcome
**Example:** "Can we predict sales from advertising?"

**Questions:**
- Is your outcome continuous or binary?
- How many predictors do you have?

**Possible Tests:**
- Simple linear regression
- Multiple linear regression
- Logistic regression

### Auto-Detection Feature

**What Gets Auto-Detected:**
- ✅ Normality (Shapiro-Wilk test)
- ✅ Number of groups (unique values in categorical columns)
- ✅ Paired structure (ID + time columns)
- ✅ Outcome type (continuous vs categorical)
- ✅ Variable types (numeric vs categorical)
- ✅ Number of predictors

**Confidence Levels:**
- 🟢 **HIGH**: Very confident (>90%)
- 🟡 **MEDIUM**: Moderately confident (70-90%)
- 🔴 **LOW**: Less confident (<70%)

**You can always override** auto-detected values!

---

## Running Analyses

### Step-by-Step Process

1. **Select Analysis Type** from dropdown
2. **Choose Variables:**
   - Dependent variable (outcome)
   - Independent variable(s) (predictors)
   - Group variable (if comparing groups)
3. **Adjust Options:**
   - Alpha level (usually 0.05)
   - Test type (if multiple options)
   - Additional parameters
4. **Click "Analyze"** button
5. **Wait for results** (usually 2-10 seconds)

### Analysis Types Guide

#### Descriptive Statistics
**When to use:** Summarize and explore your data

**Variables needed:**
- Select columns to analyze

**Output:**
- Mean, median, standard deviation
- Min, max, quartiles
- Histograms and box plots
- Outlier detection

#### Independent t-test
**When to use:** Compare means of 2 independent groups

**Variables needed:**
- Dependent: Continuous outcome
- Group: Categorical (2 groups)

**Output:**
- t-statistic, p-value
- Cohen's d (effect size)
- Group means and SDs
- Assumption checks

#### Paired t-test
**When to use:** Compare means of 2 related measurements

**Variables needed:**
- Two continuous variables (before/after)

**Output:**
- t-statistic, p-value
- Cohen's d
- Mean difference
- Assumption checks

#### One-way ANOVA
**When to use:** Compare means of 3+ independent groups

**Variables needed:**
- Dependent: Continuous outcome
- Group: Categorical (3+ groups)

**Output:**
- F-statistic, p-value
- Eta-squared (effect size)
- Group means
- Post-hoc tests (Tukey HSD)
- Assumption checks

#### ANCOVA
**When to use:** Compare groups while controlling for covariates

**Variables needed:**
- Dependent: Continuous outcome
- Group: Categorical
- Covariate(s): Continuous control variables

**Output:**
- F-statistics, p-values
- Adjusted means
- Effect sizes
- Assumption checks

#### Simple Linear Regression
**When to use:** Predict outcome from one predictor

**Variables needed:**
- Dependent: Continuous outcome
- Independent: Continuous predictor

**Output:**
- R², adjusted R²
- Regression coefficients
- p-values
- Scatter plot with regression line
- Residual plots
- Assumption checks

#### Multiple Linear Regression
**When to use:** Predict outcome from multiple predictors

**Variables needed:**
- Dependent: Continuous outcome
- Independents: Multiple continuous predictors

**Output:**
- R², adjusted R²
- Regression coefficients
- VIF scores (multicollinearity)
- p-values
- Actual vs predicted plot
- Correlation heatmap
- Residual plots

#### Logistic Regression
**When to use:** Predict binary outcome

**Variables needed:**
- Target: Binary outcome (0/1)
- Predictors: Continuous or categorical

**Output:**
- Accuracy, precision, recall, F1
- AUC-ROC
- ROC curve
- Confusion matrix
- Feature importance
- Probability distribution

#### Correlation Analysis
**When to use:** Measure relationship strength

**Variables needed:**
- Two or more continuous variables

**Output:**
- Correlation coefficient (r)
- p-value
- Scatter plot
- Correlation matrix heatmap

#### Non-parametric Tests
**When to use:** Data violates normality assumption

**Tests available:**
- Mann-Whitney U (2 groups)
- Wilcoxon Signed-Rank (paired)
- Kruskal-Wallis H (3+ groups)

#### Chi-square Test
**When to use:** Test independence of categorical variables

**Variables needed:**
- Two categorical variables

**Output:**
- Chi-square statistic
- p-value
- Contingency table
- Expected frequencies

#### Power Analysis
**When to use:** Plan sample size or evaluate power

**No file needed!**

**Options:**
- Calculation type (sample size, power, effect size)
- Test type (t-test, ANOVA, correlation)
- Parameters (alpha, power, effect size)

---

## Understanding Results

### Results Sections

Every analysis includes:

1. **📊 Visualizations** - Interactive charts
2. **📈 Test Results** - Statistical tests and p-values
3. **📝 Interpretation** - Plain-language explanation
4. **✅ Assumptions** - Checks for statistical assumptions
5. **💡 Recommendations** - What to do next

### Reading Test Results

#### P-value
**What it means:** Probability of seeing your results if there's no real effect

**Interpretation:**
- **p < 0.001**: Very strong evidence (***) 
- **p < 0.01**: Strong evidence (**)
- **p < 0.05**: Moderate evidence (*)
- **p ≥ 0.05**: Insufficient evidence

⚠️ **Remember:** p-value alone doesn't tell the whole story!

#### Effect Size
**What it means:** How large or important the effect is

**Cohen's d (for t-tests):**
- **Small**: 0.2
- **Medium**: 0.5
- **Large**: 0.8

**Eta-squared (for ANOVA):**
- **Small**: 0.01 (1% variance explained)
- **Medium**: 0.06 (6% variance explained)
- **Large**: 0.14 (14% variance explained)

**Correlation (r):**
- **Small**: 0.1
- **Medium**: 0.3
- **Large**: 0.5

### Plain-Language Interpretation

GradStat automatically generates interpretations that explain:

✅ **Statistical Significance:**
- Whether results are significant
- What the p-value means

✅ **Practical Significance:**
- Effect size magnitude
- Real-world importance

✅ **Recommendations:**
- What results mean for your research
- Next steps to consider

### APA Format

**One-click copy** of properly formatted results:

**Example:**
> "An independent-samples t-test was conducted. Results showed a significant difference, t(28) = 3.45, p = .002, d = 0.92."

Ready to paste into your research paper!

---

## Interactive Visualizations

### Features

All visualizations are **fully interactive**:

- **🔍 Zoom**: Click and drag to zoom in
- **🖱️ Pan**: Hold shift and drag to pan
- **ℹ️ Hover**: See exact values on hover
- **📥 Export**: Download as PNG (800x600, high quality)
- **🎨 Themes**: 5 professional color schemes

### Visualization Types

#### Scatter Plot
- Shows relationship between variables
- Regression line (if applicable)
- Hover for exact coordinates

#### Box Plot
- Shows distribution by group
- Median, quartiles, outliers
- Hover for statistics

#### Line Plot
- Shows trends over time
- Error bars (if applicable)
- Multiple lines for groups

#### Histogram
- Shows distribution
- Hover for bin ranges and counts

#### Bar Chart
- Shows group comparisons
- Hover for exact values

#### Heatmap
- Shows correlation matrix
- Color intensity = strength
- Hover for exact correlations

#### Q-Q Plot
- Checks normality assumption
- Points should follow diagonal line

### Themes

Choose from 5 professional themes:

1. **Default** - Blue/orange professional
2. **Colorblind** - Okabe-Ito palette (accessible)
3. **Grayscale** - Black to gray (print-friendly)
4. **Vibrant** - High contrast colors
5. **Scientific** - Muted professional

---

## Getting Help

### Contextual Help Tooltips

Look for the **💡 help icon** next to:
- Analysis types
- Variable selectors
- Statistical concepts
- Options and parameters

**Hover or click** to see:
- Clear explanation
- Real-world examples
- Practical tips
- Links to learn more

### Help Topics Available

1. **Analysis Type** - Which test to choose
2. **Dependent Variable** - What it is and how to select
3. **Independent Variable** - Predictors explained
4. **Group Variable** - Categorical grouping
5. **Alpha Level** - Significance threshold
6. **P-value** - What it means
7. **Effect Size** - Practical significance
8. **Normality** - Distribution assumption
9. **Homogeneity of Variance** - Equal variance assumption
10. **Independence** - Observation independence
11. **Correlation Methods** - Pearson vs Spearman vs Kendall
12. **Post-hoc Tests** - Multiple comparisons
13. **Power Analysis** - Sample size planning
14. And more!

---

## Common Workflows

### Workflow 1: Comparing Treatment Groups

**Scenario:** Clinical trial with treatment and control groups

```
1. Upload data: [subject_id, group, outcome, age, baseline]
2. Click "Test Advisor"
3. Select "Compare Groups"
4. Auto-detect: 2 groups, continuous outcome, normal data
5. Recommendation: Independent t-test
6. Run analysis
7. View results:
   - t(48) = 2.87, p = .006, d = 0.81 (large effect)
8. Interpretation: Treatment significantly improved outcomes
9. Copy APA format for paper
```

### Workflow 2: Correlation Study

**Scenario:** Relationship between study hours and exam scores

```
1. Upload data: [student_id, study_hours, exam_score]
2. Select "Correlation Analysis"
3. Choose variables: study_hours, exam_score
4. Select Pearson correlation
5. Run analysis
6. View results:
   - r = 0.67, p < .001 (strong positive correlation)
7. Interpretation: More study hours → higher scores
8. Export scatter plot for presentation
```

### Workflow 3: Multiple Regression

**Scenario:** Predicting house prices from multiple features

```
1. Upload data: [price, sqft, bedrooms, bathrooms, age]
2. Select "Multiple Linear Regression"
3. Dependent: price
4. Independents: sqft, bedrooms, bathrooms, age
5. Run analysis
6. View results:
   - R² = 0.82 (82% variance explained)
   - Check VIF scores for multicollinearity
   - All predictors significant
7. Interpretation: Model explains 82% of price variation
8. Check residual plots for assumptions
```

---

## Tips & Best Practices

### Data Preparation

✅ **Do:**
- Clean data before uploading
- Use clear column names
- Check for missing values
- Remove duplicate rows
- Verify data types

❌ **Don't:**
- Use special characters in names
- Mix data types in columns
- Include empty rows/columns
- Use merged cells
- Have multiple header rows

### Analysis Selection

✅ **Do:**
- Use Test Advisor if unsure
- Check assumptions before analysis
- Consider effect sizes, not just p-values
- Report confidence intervals
- Use appropriate test for data type

❌ **Don't:**
- P-hack (run multiple tests until significant)
- Ignore violated assumptions
- Rely solely on p < 0.05
- Confuse correlation with causation
- Use parametric tests on non-normal data

### Interpretation

✅ **Do:**
- Report both statistical and practical significance
- Describe effect sizes
- Acknowledge limitations
- Consider alternative explanations
- Use plain language

❌ **Don't:**
- Say "proves" (use "suggests" or "indicates")
- Ignore non-significant results
- Over-interpret small effects
- Claim causation from correlation
- Cherry-pick results

### Reporting Results

✅ **Do:**
- Use APA format
- Report exact p-values
- Include effect sizes
- Describe assumptions
- Show visualizations

❌ **Don't:**
- Just report "p < 0.05"
- Omit effect sizes
- Hide assumption violations
- Use jargon without explanation

---

## Troubleshooting

### Common Issues

#### "File upload failed"
**Causes:**
- File too large (>50MB)
- Unsupported format
- Corrupted file

**Solutions:**
- Reduce file size
- Convert to CSV
- Check file integrity

#### "Analysis failed: Variable not found"
**Causes:**
- Column name mismatch
- Variable not selected
- Empty column

**Solutions:**
- Check column names
- Verify variable selection
- Remove empty columns

#### "Assumptions violated"
**Causes:**
- Non-normal data
- Unequal variances
- Outliers

**Solutions:**
- Use non-parametric test
- Transform data (log, sqrt)
- Remove outliers
- Use robust methods

#### "Sample size too small"
**Causes:**
- Not enough data for test
- Too many missing values

**Solutions:**
- Collect more data
- Use simpler model
- Run power analysis

#### "Multicollinearity detected"
**Causes:**
- Highly correlated predictors
- Redundant variables

**Solutions:**
- Remove correlated predictors
- Use PCA
- Check VIF scores

---

## Need More Help?

### Resources

- **Documentation**: See README.md
- **Examples**: Check example-data/ folder
- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions on GitHub Discussions

### Contact

- **GitHub**: [github.com/yourusername/gradstat](https://github.com/yourusername/gradstat)
- **Email**: support@gradstat.com (coming soon)

---

<div align="center">

**Happy Analyzing! 📊**

Made with ❤️ for researchers

</div>
