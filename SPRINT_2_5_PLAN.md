# 🎯 Sprint 2.5: Guided Workflows & Help

## Goal
Create an intelligent help system that guides users through statistical analysis with contextual help, assumption checking, and interpretation assistance.

## Features to Implement

### 1. Contextual Help System ⏳
**Priority:** HIGH

**Description:**
- Inline help tooltips throughout the interface
- Explain statistical concepts in plain language
- Show examples and use cases
- Link to detailed documentation

**Implementation:**
- Create `HelpTooltip.tsx` component
- Add help icons (?) next to complex options
- Hover/click to show explanation
- Include "Learn More" links

**Help Topics:**
- Analysis type selection
- Variable selection (dependent vs independent)
- Alpha level (significance threshold)
- Effect sizes
- Assumptions
- Interpretation

---

### 2. Assumption Checking Guide ⏳
**Priority:** HIGH

**Description:**
- Interactive checklist for statistical assumptions
- Visual indicators (✓/✗) for each assumption
- Explanations of what each assumption means
- Recommendations when assumptions violated

**Assumptions to Check:**
- Normality
- Homogeneity of variance
- Independence
- Linearity
- No multicollinearity
- Sphericity (repeated measures)

**Implementation:**
- Create `AssumptionChecker.tsx` component
- Display assumption status in results
- Provide remediation suggestions
- Link to alternative tests

---

### 3. Interpretation Helper ⏳
**Priority:** HIGH

**Description:**
- Plain-language interpretation of results
- Effect size interpretation (small/medium/large)
- Practical significance vs statistical significance
- APA-style reporting templates

**Features:**
- Auto-generated interpretation text
- Copy-to-clipboard for reports
- APA format citation
- Visual aids (icons, badges)

**Example:**
```
"The independent t-test showed a statistically significant 
difference between groups (t(28) = 3.45, p = 0.002). 
The effect size was large (Cohen's d = 0.92), indicating 
a substantial practical difference."
```

---

### 4. Best Practices Panel ⏳
**Priority:** MEDIUM

**Description:**
- Recommendations based on data characteristics
- Common pitfalls to avoid
- Sample size considerations
- Power analysis suggestions

**Recommendations:**
- "Your sample size (n=15) is small. Consider collecting more data."
- "Multiple comparisons detected. Apply Bonferroni correction."
- "High correlation between predictors. Check for multicollinearity."
- "Non-normal data. Consider non-parametric alternative."

---

### 5. Analysis Workflow Wizard ⏳
**Priority:** MEDIUM

**Description:**
- Step-by-step guide for common analyses
- Decision tree for test selection
- Pre-flight checklist
- Progress tracking

**Workflows:**
1. **Compare Two Groups**
   - Check normality → Choose t-test or Mann-Whitney
   - Check variance → Welch's or Student's t-test
   - Interpret results → Report effect size

2. **Compare Multiple Groups**
   - Check normality → ANOVA or Kruskal-Wallis
   - Check variance → Standard or Welch's ANOVA
   - Post-hoc tests → Tukey HSD
   - Interpret results

3. **Predict Outcome**
   - Check linearity → Linear or non-linear regression
   - Check assumptions → Residual plots
   - Interpret coefficients → Effect sizes

---

### 6. Common Mistakes Warnings ⏳
**Priority:** MEDIUM

**Description:**
- Proactive warnings for common errors
- Real-time validation
- Educational messages

**Warnings:**
- "⚠️ Using categorical variable as continuous"
- "⚠️ Sample size too small for reliable results"
- "⚠️ Assumptions violated - consider alternative test"
- "⚠️ Multiple testing without correction"
- "⚠️ Confusing correlation with causation"

---

## Architecture

### Frontend Structure
```
frontend/src/components/
  help/
    HelpTooltip.tsx           # Contextual help tooltips
    AssumptionChecker.tsx     # Assumption checking UI
    InterpretationHelper.tsx  # Plain-language interpretation
    BestPractices.tsx         # Recommendations panel
    WorkflowWizard.tsx        # Step-by-step guide
    WarningBanner.tsx         # Common mistakes warnings
    
  utils/
    helpContent.ts            # Help text database
    interpretations.ts        # Interpretation templates
    recommendations.ts        # Best practices rules
```

### Backend Structure
```
worker/
  help_system.py              # Help content generation
  assumption_checker.py       # Assumption validation logic
  interpretation_generator.py # Auto-generate interpretations
```

---

## Implementation Plan

### Phase 1: Help Components (3-4 hours)
1. Create `HelpTooltip.tsx` component
2. Create help content database
3. Add tooltips to AnalysisSelector
4. Add tooltips to Results display

### Phase 2: Assumption Checker (2-3 hours)
1. Create `AssumptionChecker.tsx` component
2. Enhance assumption checking in worker
3. Display assumption status in results
4. Add remediation suggestions

### Phase 3: Interpretation & Best Practices (2-3 hours)
1. Create `InterpretationHelper.tsx`
2. Create `BestPractices.tsx`
3. Add interpretation generation to worker
4. Add recommendation engine

---

## UI Design

### Help Tooltip:
```
┌─────────────────────────────────────────┐
│ Alpha Level (?)                         │
│   [0.05 ▼]                              │
└─────────────────────────────────────────┘
     ↓ (hover on ?)
┌─────────────────────────────────────────┐
│ 💡 What is Alpha Level?                 │
│                                         │
│ The significance threshold (usually     │
│ 0.05) used to determine if results are │
│ statistically significant.              │
│                                         │
│ • 0.05 = 5% chance of false positive   │
│ • Lower alpha = more conservative      │
│ • Common values: 0.01, 0.05, 0.10      │
│                                         │
│ [Learn More →]                          │
└─────────────────────────────────────────┘
```

### Assumption Checker:
```
┌─────────────────────────────────────────┐
│ 📋 Assumption Checks                    │
├─────────────────────────────────────────┤
│ ✅ Normality                            │
│    Data are approximately normal        │
│    (Shapiro-Wilk: p = 0.234)           │
│                                         │
│ ✅ Equal Variances                      │
│    Variances are equal across groups    │
│    (Levene: p = 0.456)                 │
│                                         │
│ ⚠️ Independence                         │
│    Cannot be tested statistically       │
│    Ensure no repeated measures          │
│                                         │
│ ✅ All major assumptions met            │
│    Results are reliable                 │
└─────────────────────────────────────────┘
```

### Interpretation Helper:
```
┌─────────────────────────────────────────┐
│ 📝 Plain-Language Interpretation        │
├─────────────────────────────────────────┤
│ Your analysis shows:                    │
│                                         │
│ ✓ Statistically significant difference  │
│   (p = 0.002 < 0.05)                   │
│                                         │
│ ✓ Large practical effect                │
│   (Cohen's d = 0.92)                   │
│                                         │
│ This means the treatment had a          │
│ substantial and reliable effect on      │
│ the outcome.                            │
│                                         │
│ [Copy APA Format] [Copy Plain Text]    │
└─────────────────────────────────────────┘
```

### Best Practices Panel:
```
┌─────────────────────────────────────────┐
│ 💡 Recommendations                      │
├─────────────────────────────────────────┤
│ ✓ Sample size adequate (n=50)           │
│                                         │
│ ⚠️ Consider effect size                 │
│    Report Cohen's d along with p-value │
│                                         │
│ ℹ️ Multiple comparisons                 │
│    3 groups detected. Consider post-hoc │
│    tests with Bonferroni correction.   │
│                                         │
│ ✓ Assumptions met                       │
│    Results are reliable                 │
└─────────────────────────────────────────┘
```

---

## Help Content Database

### Example Structure:
```typescript
interface HelpContent {
  id: string;
  title: string;
  shortDescription: string;
  fullDescription: string;
  examples?: string[];
  learnMoreUrl?: string;
}

const helpContent: Record<string, HelpContent> = {
  'alpha-level': {
    id: 'alpha-level',
    title: 'Alpha Level (Significance Threshold)',
    shortDescription: 'The probability threshold for determining statistical significance',
    fullDescription: `
      The alpha level (α) is the probability of rejecting the null hypothesis 
      when it is actually true (Type I error). Common values are 0.05, 0.01, 
      and 0.10.
      
      - α = 0.05: 5% chance of false positive (most common)
      - α = 0.01: 1% chance of false positive (more conservative)
      - α = 0.10: 10% chance of false positive (more liberal)
    `,
    examples: [
      'If p-value < 0.05, reject null hypothesis',
      'Lower alpha = stricter criteria for significance'
    ],
    learnMoreUrl: 'https://en.wikipedia.org/wiki/Statistical_significance'
  },
  // ... more help topics
};
```

---

## Success Metrics

### Functionality:
- ✅ Help tooltips on all complex options
- ✅ Assumption checker displays status
- ✅ Interpretations generated automatically
- ✅ Recommendations based on data

### User Experience:
- ✅ Help is easy to find and access
- ✅ Explanations are clear and concise
- ✅ Recommendations are actionable
- ✅ No jargon without explanation

### Educational Value:
- ✅ Users learn statistical concepts
- ✅ Common mistakes prevented
- ✅ Best practices encouraged
- ✅ Confidence in results increased

---

## Estimated Timeline

**Total: 7-10 hours**

- Phase 1 (Help Components): 3-4 hours
- Phase 2 (Assumption Checker): 2-3 hours
- Phase 3 (Interpretation & Best Practices): 2-3 hours

---

## Next Steps

1. Create help content database
2. Build HelpTooltip component
3. Add tooltips to interface
4. Create AssumptionChecker component
5. Build InterpretationHelper
6. Add BestPractices panel
7. Test with users

**Ready to start implementation!** 🚀
