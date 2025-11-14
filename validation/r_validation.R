# GradStat R Validation Script
# Spot-check GradStat results against R (gold standard)

library(tidyverse)
library(broom)

# Create output directory
dir.create("validation/r_results", showWarnings = FALSE)

cat("=" , rep("=", 59), "\n", sep = "")
cat("GradStat R Validation - Spot Check\n")
cat("=" , rep("=", 59), "\n\n", sep = "")

# ============================================================================
# Test 1: Independent T-Test
# ============================================================================
cat("Test 1: Independent Samples T-Test\n")
cat("-----------------------------------\n")

# Student's sleep data
group1 <- c(0.7, -1.6, -0.2, -1.2, -0.1, 3.4, 3.7, 0.8, 0.0, 2.0)
group2 <- c(1.9, 0.8, 1.1, 0.1, -0.1, 4.4, 5.5, 1.6, 4.6, 3.4)

# Run t-test
ttest_result <- t.test(group1, group2, var.equal = TRUE)

cat("Group 1 mean:", mean(group1), "\n")
cat("Group 2 mean:", mean(group2), "\n")
cat("t-statistic:", ttest_result$statistic, "\n")
cat("p-value:", ttest_result$p.value, "\n")
cat("df:", ttest_result$parameter, "\n")
cat("95% CI:", ttest_result$conf.int[1], "to", ttest_result$conf.int[2], "\n")

# Save data for GradStat
df_ttest <- data.frame(
  group = c(rep("A", 10), rep("B", 10)),
  value = c(group1, group2)
)
write.csv(df_ttest, "validation/data/r_ttest_independent.csv", row.names = FALSE)

cat("\n✅ Expected GradStat results:\n")
cat("   t = ", round(ttest_result$statistic, 3), "\n", sep = "")
cat("   p = ", round(ttest_result$p.value, 4), "\n", sep = "")
cat("\n")

# ============================================================================
# Test 2: Paired T-Test
# ============================================================================
cat("Test 2: Paired Samples T-Test\n")
cat("------------------------------\n")

before <- c(5.2, 6.1, 5.8, 4.9, 6.3, 5.7, 6.0, 5.4, 5.9, 6.2)
after <- c(6.1, 7.2, 6.5, 5.8, 7.1, 6.4, 6.8, 6.2, 6.7, 7.0)

paired_result <- t.test(before, after, paired = TRUE)

cat("Before mean:", mean(before), "\n")
cat("After mean:", mean(after), "\n")
cat("Mean difference:", mean(after - before), "\n")
cat("t-statistic:", paired_result$statistic, "\n")
cat("p-value:", paired_result$p.value, "\n")
cat("df:", paired_result$parameter, "\n")

df_paired <- data.frame(
  subject_id = 1:10,
  before = before,
  after = after
)
write.csv(df_paired, "validation/data/r_ttest_paired.csv", row.names = FALSE)

cat("\n✅ Expected GradStat results:\n")
cat("   t = ", round(paired_result$statistic, 3), "\n", sep = "")
cat("   p = ", round(paired_result$p.value, 4), "\n", sep = "")
cat("\n")

# ============================================================================
# Test 3: One-Way ANOVA
# ============================================================================
cat("Test 3: One-Way ANOVA\n")
cat("---------------------\n")

# Fisher's Iris data (subset)
setosa <- c(5.1, 4.9, 4.7, 4.6, 5.0, 5.4, 4.6, 5.0, 4.4, 4.9)
versicolor <- c(7.0, 6.4, 6.9, 5.5, 6.5, 5.7, 6.3, 4.9, 6.6, 5.2)
virginica <- c(6.3, 5.8, 7.1, 6.3, 6.5, 7.6, 4.9, 7.3, 6.7, 7.2)

df_anova <- data.frame(
  species = c(rep("setosa", 10), rep("versicolor", 10), rep("virginica", 10)),
  sepal_length = c(setosa, versicolor, virginica)
)

anova_result <- aov(sepal_length ~ species, data = df_anova)
anova_summary <- summary(anova_result)

cat("Setosa mean:", mean(setosa), "\n")
cat("Versicolor mean:", mean(versicolor), "\n")
cat("Virginica mean:", mean(virginica), "\n")
cat("F-statistic:", anova_summary[[1]]$`F value`[1], "\n")
cat("p-value:", anova_summary[[1]]$`Pr(>F)`[1], "\n")

write.csv(df_anova, "validation/data/r_anova_oneway.csv", row.names = FALSE)

cat("\n✅ Expected GradStat results:\n")
cat("   F = ", round(anova_summary[[1]]$`F value`[1], 3), "\n", sep = "")
cat("   p = ", format(anova_summary[[1]]$`Pr(>F)`[1], scientific = FALSE), "\n", sep = "")
cat("\n")

# ============================================================================
# Test 4: Linear Regression
# ============================================================================
cat("Test 4: Linear Regression\n")
cat("-------------------------\n")

# Anscombe's quartet - dataset I
x <- c(10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5)
y <- c(8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68)

lm_result <- lm(y ~ x)
lm_summary <- summary(lm_result)

cat("Slope:", coef(lm_result)[2], "\n")
cat("Intercept:", coef(lm_result)[1], "\n")
cat("R-squared:", lm_summary$r.squared, "\n")
cat("p-value:", lm_summary$coefficients[2, 4], "\n")

df_regression <- data.frame(x = x, y = y)
write.csv(df_regression, "validation/data/r_regression_linear.csv", row.names = FALSE)

cat("\n✅ Expected GradStat results:\n")
cat("   Slope = ", round(coef(lm_result)[2], 4), "\n", sep = "")
cat("   R² = ", round(lm_summary$r.squared, 4), "\n", sep = "")
cat("\n")

# ============================================================================
# Test 5: Pearson Correlation
# ============================================================================
cat("Test 5: Pearson Correlation\n")
cat("---------------------------\n")

# mtcars data (subset)
mpg <- c(21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2)
wt <- c(2.620, 2.875, 2.320, 3.215, 3.440, 3.460, 3.570, 3.190, 3.150, 3.440)

cor_result <- cor.test(mpg, wt)

cat("Correlation coefficient:", cor_result$estimate, "\n")
cat("p-value:", cor_result$p.value, "\n")
cat("95% CI:", cor_result$conf.int[1], "to", cor_result$conf.int[2], "\n")

df_correlation <- data.frame(mpg = mpg, weight = wt)
write.csv(df_correlation, "validation/data/r_correlation_pearson.csv", row.names = FALSE)

cat("\n✅ Expected GradStat results:\n")
cat("   r = ", round(cor_result$estimate, 4), "\n", sep = "")
cat("   p = ", round(cor_result$p.value, 4), "\n", sep = "")
cat("\n")

# ============================================================================
# Summary
# ============================================================================
cat("=" , rep("=", 59), "\n", sep = "")
cat("SUMMARY\n")
cat("=" , rep("=", 59), "\n", sep = "")
cat("\n")
cat("✅ Generated 5 test datasets with known R results\n")
cat("✅ All CSV files saved to validation/data/\n")
cat("✅ Compare GradStat results to values above\n")
cat("\n")
cat("Next steps:\n")
cat("1. Upload each CSV to GradStat\n")
cat("2. Run the corresponding analysis\n")
cat("3. Compare results to R values above\n")
cat("4. Tolerance: ±0.01 for statistics, ±0.001 for p-values\n")
cat("\n")
cat("=" , rep("=", 59), "\n", sep = "")

# Save summary to file
sink("validation/r_results/R_VALIDATION_SUMMARY.txt")
cat("GradStat R Validation Summary\n")
cat("Generated:", Sys.time(), "\n\n")

cat("Test 1: Independent T-Test\n")
cat("  t =", ttest_result$statistic, "\n")
cat("  p =", ttest_result$p.value, "\n\n")

cat("Test 2: Paired T-Test\n")
cat("  t =", paired_result$statistic, "\n")
cat("  p =", paired_result$p.value, "\n\n")

cat("Test 3: One-Way ANOVA\n")
cat("  F =", anova_summary[[1]]$`F value`[1], "\n")
cat("  p =", anova_summary[[1]]$`Pr(>F)`[1], "\n\n")

cat("Test 4: Linear Regression\n")
cat("  Slope =", coef(lm_result)[2], "\n")
cat("  R² =", lm_summary$r.squared, "\n\n")

cat("Test 5: Pearson Correlation\n")
cat("  r =", cor_result$estimate, "\n")
cat("  p =", cor_result$p.value, "\n")

sink()

cat("📄 Summary saved to: validation/r_results/R_VALIDATION_SUMMARY.txt\n")
