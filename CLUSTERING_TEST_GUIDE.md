# Enhanced Clustering Test Guide 🧪

**Date:** October 22, 2025  
**Status:** Ready to Test

---

## Quick Test Steps

### Test 1: K-Means with Elbow Method ⭐ (RECOMMENDED FIRST)

1. **Open GradStat:** http://localhost:3000

2. **Upload Data:**
   - Click "Choose File"
   - Select: `example-data/health_exercise_study.csv`
   - Wait for preview to load

3. **Configure Analysis:**
   - Analysis Type: **Clustering**
   - Clustering Method: **K-Means Clustering**
   - Number of Clusters: **3**
   - ✅ **Show elbow method & silhouette analysis** (checked)

4. **Run Analysis:**
   - Click "Run Analysis"
   - Wait 5-10 seconds

5. **Expected Results:**
   - ✅ **4 plots:**
     1. **Optimal Clusters Analysis** (elbow + silhouette scores)
     2. **Silhouette Plot** (colored bars)
     3. **Cluster Visualization** (scatter with red X centroids)
   
   - ✅ **Test Results showing:**
     - N_Clusters: 3
     - Clustering Method: K-Means
     - Silhouette Score: ~0.40-0.60 (highlighted if > 0.5)
     - Inertia: ~200-300
     - Number of Samples: 180
     - Number of Features: 11
   
   - ✅ **Interpretation:**
     - "Kmeans clustering identified 3 distinct groups..."
     - "Silhouette score of X.XXX indicates [quality]..."
     - "Cluster sizes range from X to Y members"
   
   - ✅ **Recommendations:**
     - Suggestions based on silhouette score
     - Try hierarchical clustering
     - Examine cluster characteristics

---

### Test 2: Hierarchical Clustering 🌳

1. **Same dataset** (already uploaded)

2. **Change Settings:**
   - Clustering Method: **Hierarchical Clustering**
   - Number of Clusters: **3**
   - ✅ **Show elbow method** (keep checked)

3. **Run Analysis**

4. **Expected Results:**
   - ✅ **5 plots:**
     1. **Optimal Clusters Analysis** (elbow + silhouette)
     2. **Dendrogram** (tree structure with red cut line)
     3. **Silhouette Plot**
     4. **Cluster Visualization** (scatter, no centroids)
   
   - ✅ **Test Results showing:**
     - Clustering Method: Hierarchical
     - Silhouette Score: Similar to K-means
     - No Inertia (hierarchical doesn't use it)

---

### Test 3: Different k Values 🔢

1. **Try k=2:**
   - Change Number of Clusters to **2**
   - Run analysis
   - Check silhouette score

2. **Try k=4:**
   - Change Number of Clusters to **4**
   - Run analysis
   - Check silhouette score

3. **Try k=5:**
   - Change Number of Clusters to **5**
   - Run analysis
   - Check silhouette score

4. **Compare:**
   - Which k gives the best silhouette score?
   - Does the elbow plot suggest the same k?
   - Look for the "elbow" in the curve

---

### Test 4: Fast Mode (No Elbow) ⚡

1. **Uncheck** "Show elbow method & silhouette analysis"

2. **Run Analysis**

3. **Expected Results:**
   - ✅ Faster execution (~2-3 seconds vs 5-10 seconds)
   - ✅ Only 2 plots:
     1. Silhouette Plot
     2. Cluster Visualization
   - ✅ No elbow/silhouette comparison plot

---

## What to Look For

### ✅ Success Indicators:

1. **Elbow Plot:**
   - Shows curve from k=2 to k=10
   - Has an "elbow" point (where curve bends)
   - Red vertical line at your selected k

2. **Silhouette Score Plot:**
   - Shows scores from k=2 to k=10
   - Green horizontal line at 0.5 (good threshold)
   - Red vertical line at your selected k
   - Peak indicates optimal k

3. **Silhouette Plot:**
   - Colored horizontal bars for each cluster
   - Red dashed line shows average
   - Wider bars = better clusters
   - Most bars should extend past average

4. **Cluster Scatter:**
   - Points colored by cluster
   - Clear separation between clusters
   - Red X marks (K-means only) at cluster centers

5. **Dendrogram (Hierarchical):**
   - Tree structure showing merges
   - Red horizontal line showing cut point
   - Taller branches = more distinct clusters

### ❌ Issues to Watch For:

1. **No elbow plot showing:**
   - Check if "Show elbow method" is checked
   - Check browser console for errors

2. **Silhouette score very low (< 0.25):**
   - This is actually CORRECT behavior!
   - Health data may not have strong natural clusters
   - Recommendation should suggest trying different k

3. **Plots not rendering:**
   - Check worker is running (port 8001)
   - Check browser console for errors
   - Try refreshing page

4. **Error messages:**
   - "Need at least 2 numeric columns" - dataset issue
   - Check that CSV loaded correctly

---

## Expected Silhouette Scores

For the health dataset with different k:

| k | Expected Silhouette | Quality |
|---|---------------------|---------|
| 2 | 0.45-0.55 | Reasonable |
| 3 | 0.40-0.50 | Reasonable |
| 4 | 0.35-0.45 | Weak |
| 5 | 0.30-0.40 | Weak |
| 6+ | 0.25-0.35 | Poor |

**Note:** Health data doesn't have strong natural clusters, so moderate scores are expected!

---

## Interpretation Guide

### Silhouette Score Meanings:

- **0.71-1.00:** 🟢 Strong, well-separated clusters
- **0.51-0.70:** 🟡 Reasonable cluster structure
- **0.26-0.50:** 🟠 Weak cluster structure
- **< 0.25:** 🔴 Poor clustering - try different k

### Elbow Method:

Look for the "elbow" where:
- Inertia stops decreasing rapidly
- Adding more clusters gives diminishing returns
- Usually between k=3 and k=5 for most datasets

### Cluster Sizes:

- **Balanced:** All clusters similar size (good)
- **Unbalanced:** One cluster much larger (may indicate outliers)
- **Very small cluster:** < 5% of data (may be outliers)

---

## Troubleshooting

### Issue: Worker not responding
**Solution:**
```bash
cd worker
python main.py
```

### Issue: Frontend not loading
**Solution:**
```bash
cd frontend
npm start
```

### Issue: Plots not showing
**Solution:**
1. Open browser console (F12)
2. Look for errors
3. Check Network tab for failed requests
4. Refresh page

### Issue: Analysis takes too long
**Solution:**
- Uncheck "Show elbow method" for faster results
- Elbow method runs clustering 9 times (k=2 to k=10)

---

## Screenshots to Take

For documentation, capture:

1. **Optimal Clusters Analysis plot** (elbow + silhouette)
2. **Silhouette Plot** (colored bars)
3. **Dendrogram** (hierarchical only)
4. **Test Results cards** (showing metrics)
5. **Interpretation section**
6. **Recommendations section**

---

## Performance Benchmarks

Expected execution times:

| Configuration | Time | Plots |
|--------------|------|-------|
| K-means with elbow | 5-10s | 3 |
| K-means without elbow | 2-3s | 2 |
| Hierarchical with elbow | 6-12s | 4 |
| Hierarchical without elbow | 3-5s | 3 |

---

## Next Steps After Testing

### If Everything Works ✅:
1. Mark test as complete
2. Move to Power Analysis implementation
3. Document any observations

### If Issues Found ❌:
1. Note the specific error
2. Check browser console
3. Check worker logs
4. Report issue for fixing

---

## Success Criteria

Test is successful if:

- ✅ All 4 test scenarios run without errors
- ✅ Elbow plot shows for k=2 to k=10
- ✅ Silhouette scores calculated correctly
- ✅ Silhouette plot renders with colored bars
- ✅ Dendrogram shows for hierarchical
- ✅ Cluster scatter shows with proper colors
- ✅ Centroids show for K-means (red X marks)
- ✅ Test results display all metrics
- ✅ Interpretation text is meaningful
- ✅ Recommendations are relevant
- ✅ Download report works

---

## Test Results Template

```
Date: [DATE]
Tester: [NAME]

Test 1: K-Means with Elbow
- Status: [ ] Pass [ ] Fail
- Silhouette Score: _____
- Notes: _____________________

Test 2: Hierarchical Clustering
- Status: [ ] Pass [ ] Fail
- Silhouette Score: _____
- Notes: _____________________

Test 3: Different k Values
- k=2: Silhouette = _____
- k=4: Silhouette = _____
- k=5: Silhouette = _____
- Optimal k: _____

Test 4: Fast Mode
- Status: [ ] Pass [ ] Fail
- Execution Time: _____ seconds
- Notes: _____________________

Overall: [ ] All Tests Pass [ ] Some Issues
```

---

**Ready to test!** Open http://localhost:3000 and follow Test 1! 🚀
