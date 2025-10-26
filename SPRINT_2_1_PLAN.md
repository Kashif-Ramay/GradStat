# 🚀 Sprint 2.1: Expand Test Advisor to All Research Questions

## Goal
Support all 7 research question types with smart pre-analysis and enhanced wizards

**Time Estimate:** 8-10 hours

---

## Current State Analysis

### ✅ Fully Implemented (with pre-analysis):
1. **Compare Groups** - 4 questions, full pre-analysis
2. **Find Relationships** - 2-3 questions, full pre-analysis
3. **Predict Outcome** - 2 questions, full pre-analysis

### ⚠️ Partially Implemented:
4. **Survival Analysis** - Basic wizard exists, NO pre-analysis
5. **Describe Data** - Auto-fetch only, no wizard
6. **Reduce Dimensions** - Auto-fetch only, no wizard
7. **Find Groups** - Auto-fetch only, no wizard

---

## 📋 Tasks Breakdown

### Task 1: Add Survival Analysis Pre-Analysis (3-4 hours)

#### 1.1 Worker: Detection Functions (2h)

**File:** `worker/test_advisor.py`

Add detection functions:

```python
def detect_time_event_columns(df: pd.DataFrame) -> Dict:
    """
    Detect time-to-event and censoring columns
    
    Returns:
        {
            'time_column': str or None,
            'event_column': str or None,
            'has_groups': bool,
            'group_column': str or None,
            'has_covariates': bool,
            'covariate_columns': list,
            'confidence': {
                'time_column': 'high'|'medium'|'low',
                'event_column': 'high'|'medium'|'low',
                'has_groups': 'high'|'medium'|'low'
            }
        }
    """
    # Logic:
    # 1. Time column: numeric, name contains 'time', 'duration', 'days', 'months'
    # 2. Event column: binary (0/1), name contains 'event', 'status', 'censored', 'death'
    # 3. Groups: categorical columns (2-5 unique values)
    # 4. Covariates: remaining numeric columns
    pass

def detect_censoring_type(df: pd.DataFrame, event_col: str) -> Dict:
    """
    Detect censoring type and percentage
    
    Returns:
        {
            'censoring_type': 'right'|'left'|'interval',
            'censoring_pct': float,
            'confidence': 'high'|'medium'|'low'
        }
    """
    # Logic:
    # 1. Right censoring: event=0 means censored (most common)
    # 2. Calculate percentage of censored observations
    pass
```

#### 1.2 Worker: Update Comprehensive Analysis (30min)

**File:** `worker/test_advisor.py`

Update `analyze_dataset_comprehensive()`:

```python
# Add survival analysis detection
survival_info = detect_time_event_columns(df)
results['survival'] = survival_info

# Add to confidence dict
confidence['hasTimeColumn'] = survival_info['confidence']['time_column']
confidence['hasEventColumn'] = survival_info['confidence']['event_column']
confidence['hasGroups'] = survival_info['confidence']['has_groups']
```

#### 1.3 Frontend: Auto-Fill Survival Questions (1h)

**File:** `frontend/src/components/TestAdvisor.tsx`

Update `analyzeDataset()` to handle survival analysis:

```typescript
// Survival Analysis answers
if (response.data.survival) {
  if (response.data.survival.has_groups !== null) {
    newAnswers.hasGroups = response.data.survival.has_groups;
  }
  if (response.data.survival.has_covariates !== null) {
    newAnswers.hasCovariates = response.data.survival.has_covariates;
  }
}
```

Add visual indicators to survival questions (badges, sparkles).

#### 1.4 Test Data (30min)

Create `test-data/survival-data.csv`:
```csv
patient_id,treatment,age,gender,time_to_event,event_occurred
1,A,45,M,120,1
2,A,52,F,90,0
3,B,38,M,150,1
...
```

---

### Task 2: Add Reduce Dimensions Wizard (2 hours)

#### 2.1 Worker: PCA Detection (1h)

**File:** `worker/test_advisor.py`

```python
def detect_pca_options(df: pd.DataFrame) -> Dict:
    """
    Detect optimal PCA settings
    
    Returns:
        {
            'n_numeric_vars': int,
            'suggested_components': int,  # Rule: sqrt(n_vars) or 80% variance
            'scaling_needed': bool,  # Check variance differences
            'correlation_strength': 'high'|'medium'|'low',
            'confidence': {
                'n_components': 'high'|'medium'|'low',
                'scaling': 'high'|'medium'|'low'
            }
        }
    """
    # Logic:
    # 1. Count numeric variables
    # 2. Suggest components: min(sqrt(n_vars), n_vars/2)
    # 3. Check if scaling needed (variance ratio > 10)
    # 4. Calculate correlation matrix strength
    pass
```

#### 2.2 Frontend: PCA Wizard (1h)

**File:** `frontend/src/components/TestAdvisor.tsx`

Add Step 2 for `reduce_dimensions`:

```typescript
if (step === 2 && answers.researchQuestion === 'reduce_dimensions') {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2>Reduce Dimensions (PCA)</h2>
      
      {/* Question 1: Number of components */}
      <div>
        <h3>How many components do you want?</h3>
        <input 
          type="number" 
          value={answers.nComponents}
          onChange={(e) => handleAnswer('nComponents', e.target.value)}
        />
        {/* Show suggestion from pre-analysis */}
      </div>
      
      {/* Question 2: Scaling */}
      <div>
        <h3>Should we scale your variables?</h3>
        <button onClick={() => handleAnswer('scaling', true)}>Yes</button>
        <button onClick={() => handleAnswer('scaling', false)}>No</button>
      </div>
      
      {/* Question 3: Visualization */}
      <div>
        <h3>What visualization do you want?</h3>
        <button onClick={() => handleAnswer('vizType', 'biplot')}>Biplot</button>
        <button onClick={() => handleAnswer('vizType', 'scree')}>Scree Plot</button>
        <button onClick={() => handleAnswer('vizType', 'both')}>Both</button>
      </div>
    </div>
  );
}
```

---

### Task 3: Add Find Groups Wizard (2 hours)

#### 3.1 Worker: Clustering Detection (1h)

**File:** `worker/test_advisor.py`

```python
def detect_clustering_options(df: pd.DataFrame) -> Dict:
    """
    Detect optimal clustering settings
    
    Returns:
        {
            'n_numeric_vars': int,
            'suggested_k': int,  # Elbow method or silhouette
            'suggested_algorithm': 'kmeans'|'hierarchical'|'dbscan',
            'scaling_needed': bool,
            'has_outliers': bool,
            'confidence': {
                'n_clusters': 'high'|'medium'|'low',
                'algorithm': 'high'|'medium'|'low'
            }
        }
    """
    # Logic:
    # 1. Count numeric variables
    # 2. Quick elbow method for k (2-10)
    # 3. Suggest algorithm:
    #    - K-means: if no outliers, spherical clusters
    #    - Hierarchical: if small dataset (<1000 rows)
    #    - DBSCAN: if outliers detected
    # 4. Check scaling needed
    pass
```

#### 3.2 Frontend: Clustering Wizard (1h)

**File:** `frontend/src/components/TestAdvisor.tsx`

Add Step 2 for `find_groups`:

```typescript
if (step === 2 && answers.researchQuestion === 'find_groups') {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2>Find Natural Groups (Clustering)</h2>
      
      {/* Question 1: Number of clusters */}
      <div>
        <h3>How many groups do you expect?</h3>
        <input 
          type="number" 
          value={answers.nClusters}
          onChange={(e) => handleAnswer('nClusters', e.target.value)}
        />
        {/* Show suggestion */}
      </div>
      
      {/* Question 2: Algorithm */}
      <div>
        <h3>Which clustering method?</h3>
        <button onClick={() => handleAnswer('algorithm', 'kmeans')}>
          K-Means (fast, spherical)
        </button>
        <button onClick={() => handleAnswer('algorithm', 'hierarchical')}>
          Hierarchical (dendrogram)
        </button>
        <button onClick={() => handleAnswer('algorithm', 'dbscan')}>
          DBSCAN (handles outliers)
        </button>
      </div>
      
      {/* Question 3: Distance metric */}
      <div>
        <h3>Distance metric?</h3>
        <button onClick={() => handleAnswer('metric', 'euclidean')}>
          Euclidean (default)
        </button>
        <button onClick={() => handleAnswer('metric', 'manhattan')}>
          Manhattan
        </button>
      </div>
    </div>
  );
}
```

---

### Task 4: Enhance Describe Data Wizard (1 hour)

#### 4.1 Frontend: Descriptive Stats Wizard (1h)

**File:** `frontend/src/components/TestAdvisor.tsx`

Add Step 2 for `describe_data`:

```typescript
if (step === 2 && answers.researchQuestion === 'describe_data') {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2>Describe Your Data</h2>
      
      {/* Question 1: What to include */}
      <div>
        <h3>What statistics do you want?</h3>
        <label>
          <input type="checkbox" checked={answers.includeBasic} 
                 onChange={(e) => handleAnswer('includeBasic', e.target.checked)} />
          Basic stats (mean, median, SD)
        </label>
        <label>
          <input type="checkbox" checked={answers.includeDistribution} 
                 onChange={(e) => handleAnswer('includeDistribution', e.target.checked)} />
          Distribution analysis
        </label>
        <label>
          <input type="checkbox" checked={answers.includeOutliers} 
                 onChange={(e) => handleAnswer('includeOutliers', e.target.checked)} />
          Outlier detection
        </label>
      </div>
      
      {/* Question 2: Grouping */}
      <div>
        <h3>Do you want to group by a variable?</h3>
        <button onClick={() => handleAnswer('hasGrouping', false)}>
          No grouping
        </button>
        <button onClick={() => handleAnswer('hasGrouping', true)}>
          Yes, group by...
        </button>
        {answers.hasGrouping && (
          <select onChange={(e) => handleAnswer('groupBy', e.target.value)}>
            {/* Populate from categorical columns */}
          </select>
        )}
      </div>
      
      {/* Question 3: Visualizations */}
      <div>
        <h3>What visualizations?</h3>
        <label>
          <input type="checkbox" checked={answers.showHistograms} 
                 onChange={(e) => handleAnswer('showHistograms', e.target.checked)} />
          Histograms
        </label>
        <label>
          <input type="checkbox" checked={answers.showBoxplots} 
                 onChange={(e) => handleAnswer('showBoxplots', e.target.checked)} />
          Box plots
        </label>
      </div>
    </div>
  );
}
```

---

### Task 5: Update Backend & Worker Routes (1 hour)

#### 5.1 Worker: Add New Endpoints (30min)

**File:** `worker/analyze.py`

```python
@app.post("/test-advisor/detect-survival")
async def detect_survival_options(file: UploadFile = File(...)):
    """Detect survival analysis options"""
    df = await load_dataframe(file)
    result = detect_time_event_columns(df)
    return result

@app.post("/test-advisor/detect-pca")
async def detect_pca_options_endpoint(file: UploadFile = File(...)):
    """Detect PCA options"""
    df = await load_dataframe(file)
    result = detect_pca_options(df)
    return result

@app.post("/test-advisor/detect-clustering")
async def detect_clustering_options_endpoint(file: UploadFile = File(...)):
    """Detect clustering options"""
    df = await load_dataframe(file)
    result = detect_clustering_options(df)
    return result
```

#### 5.2 Backend: Forward Requests (30min)

**File:** `backend/server.js`

Add forwarding for new endpoints (similar to existing pattern).

---

### Task 6: Testing & Documentation (1 hour)

#### 6.1 Create Test Data (30min)

Create test datasets:
- `test-data/survival-data.csv` - Time-to-event data
- `test-data/pca-data.csv` - Many correlated variables
- `test-data/clustering-data.csv` - Natural groups

#### 6.2 Test All Flows (30min)

Test each research question:
1. Upload data
2. Verify pre-analysis
3. Complete wizard
4. Check recommendations

---

## 📊 Expected Outcomes

### Coverage:
- **Before:** 3/7 research questions with pre-analysis (43%)
- **After:** 7/7 research questions with pre-analysis (100%)

### New Detection Functions:
1. `detect_time_event_columns()` - Survival analysis
2. `detect_censoring_type()` - Censoring info
3. `detect_pca_options()` - PCA settings
4. `detect_clustering_options()` - Clustering settings

### New Wizards:
1. Survival Analysis - Enhanced with pre-analysis
2. Reduce Dimensions - New wizard with options
3. Find Groups - New wizard with options
4. Describe Data - New wizard with customization

### Questions Answered Automatically:
- Survival: 2-3 questions (hasGroups, hasCovariates, time/event columns)
- PCA: 2 questions (nComponents, scaling)
- Clustering: 2 questions (nClusters, algorithm)
- Descriptive: 1 question (grouping)

**Total:** 14-16 questions answered across all research types!

---

## 🎯 Success Metrics

- ✅ All 7 research questions have wizards
- ✅ All 7 have smart pre-analysis
- ✅ 14-16 questions auto-answered
- ✅ Visual indicators on all questions
- ✅ Confidence badges everywhere
- ✅ Test data for all types

---

## 📝 Implementation Order

1. **Survival Analysis** (3-4h) - Most complex, highest value
2. **Find Groups** (2h) - Medium complexity
3. **Reduce Dimensions** (2h) - Medium complexity
4. **Describe Data** (1h) - Simplest
5. **Testing** (1h) - Verify everything works

**Total: 8-10 hours**

---

## 🚀 Ready to Start?

Let's begin with **Survival Analysis** - the most impactful addition!

**Next step:** Implement `detect_time_event_columns()` in `worker/test_advisor.py`
