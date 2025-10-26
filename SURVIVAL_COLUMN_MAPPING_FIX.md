# 🔧 Survival Analysis Column Mapping Fix

## Problem
Analysis was failing with error:
```
Unable to parse string "A" at position 0
```

This occurred because the wrong columns were being mapped:
- `eventColumn` was set to `'treatment'` (contains "A", "B") ❌
- Should have been `'event_occurred'` (contains 0, 1) ✅

## Root Cause
The Test Advisor recommendations had placeholder values in `gradstat_options`:
```javascript
{
  durationColumn: '<time>',
  eventColumn: '<event>',
  groupColumn: '<group>'
}
```

These placeholders were never replaced with the actual detected column names from the pre-analysis.

## Solution
Updated the flow to pass detected column names from pre-analysis to recommendations.

### Changes Made

#### 1. Worker: `test_advisor.py`
Updated `_recommend_for_survival()` to use detected column names:

```python
def _recommend_for_survival(answers: Dict) -> List[Dict]:
    # Get detected column names from answers
    survival_data = answers.get('_survivalData', {})
    time_column = survival_data.get('time_column')
    event_column = survival_data.get('event_column')
    group_column = survival_data.get('group_column')
    covariate_columns = survival_data.get('covariate_columns', [])
    
    # Fill in detected column names in gradstat_options
    recommendations[0]['gradstat_options']['durationColumn'] = time_column
    recommendations[0]['gradstat_options']['eventColumn'] = event_column
    # ... etc for all recommendations
```

#### 2. Frontend: `TestAdvisor.tsx`
Updated `getRecommendations()` to include survival data:

```typescript
const getRecommendations = async () => {
  // Include survival data in answers if available
  const answersWithData = { ...answers };
  if (preAnalysisResults?.survival && answers.researchQuestion === 'survival_analysis') {
    answersWithData._survivalData = preAnalysisResults.survival;
  }
  
  const response = await axios.post('/api/test-advisor/recommend', answersWithData);
  // ...
};
```

## How It Works

### Flow:
1. User uploads file in Test Advisor ✅
2. Pre-analysis detects columns:
   - `time_column`: "time_to_event"
   - `event_column`: "event_occurred"
   - `group_column`: "treatment"
   - `covariate_columns`: ["age", "gender"]
3. User answers questions ✅
4. Frontend sends answers + `_survivalData` to backend ✅
5. Backend fills placeholders with actual column names ✅
6. Recommendations have correct `gradstat_options` ✅
7. User clicks "Use This Test" ✅
8. Analysis runs with correct columns! 🎉

### Before Fix:
```javascript
gradstat_options: {
  analysisType: 'survival',
  durationColumn: '<time>',      // ❌ Placeholder
  eventColumn: '<event>',         // ❌ Placeholder
  groupColumn: '<group>'          // ❌ Placeholder
}
```

### After Fix:
```javascript
gradstat_options: {
  analysisType: 'survival',
  durationColumn: 'time_to_event',    // ✅ Actual column
  eventColumn: 'event_occurred',      // ✅ Actual column
  groupColumn: 'treatment',           // ✅ Actual column
  covariates: ['age', 'gender']       // ✅ Actual columns
}
```

## Files Modified
- ✅ `worker/test_advisor.py` - Updated `_recommend_for_survival()`
- ✅ `frontend/src/components/TestAdvisor.tsx` - Updated `getRecommendations()`

## Testing

### Test Survival Analysis:
1. Upload `test-data/survival-data.csv`
2. Select "Survival/time-to-event"
3. Answer questions (or use pre-filled)
4. Get recommendations
5. **Verify:** Recommendations show correct column names
6. Click "Use This Test"
7. **Verify:** Analysis options show:
   - Duration: time_to_event ✅
   - Event: event_occurred ✅
   - Group: treatment ✅
8. Run analysis
9. **Verify:** Analysis completes successfully! 🎉

---

**Status:** ✅ FIXED
**Survival analysis should now work with correct column mapping!**
