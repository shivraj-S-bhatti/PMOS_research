# Personal Stats Cheat Sheet

This is a practical "I skimmed the course, what do I do?" guide.

## 1. The Core Question

Almost every stats problem starts with:

1. What is the response/outcome?
2. What type is the response: numerical or categorical?
3. What are the explanatory variables?
4. How many groups/conditions are being compared?
5. Are observations independent or paired/repeated?
6. Is the goal estimation, hypothesis testing, prediction, or explanation?

## 2. Big Method Families

### Descriptive Statistics

Use when:

- You need to summarize data before inference.

Examples:

- Mean, median, standard deviation, five-number summary.
- Histogram, boxplot, scatterplot, bar chart.

Intuition:

- Before testing anything, look at shape, center, spread, outliers, and sample
  size.

### Confidence Intervals

Use when:

- You want a plausible range for a population value.

Examples:

- Mean exam score in a class.
- Difference in average grades between two classes.
- Proportion of students who passed.

Intuition:

- Estimate +/- margin of error.
- Wider interval = more uncertainty.
- Larger sample size = narrower interval.

### Hypothesis Tests

Use when:

- You want to decide whether data provide enough evidence against a default
  claim.

Common setup:

- Null hypothesis: no difference, no association, no effect.
- Alternative hypothesis: difference/association/effect exists.

Decision:

- If p-value < alpha, reject null.
- If p-value >= alpha, fail to reject null.

Important:

- Failing to reject is not proof that null is true.
- p-value is not the probability the null is true.

### Regression / Prediction

Use when:

- Response is numerical and you want to explain or predict it from one or more
  variables.

Examples:

- Predict BMI from waist-to-hip ratio and hormones.
- Predict rainfall from temperature.
- Predict grade from hours studied.

Intuition:

- Fit a line/plane that minimizes residuals.
- Residual = observed - predicted.

### Classification

Use when:

- Response is categorical, often binary.

Examples:

- PCOS yes/no.
- Pass/fail.
- Which output did humans prefer?

Methods:

- Logistic regression.
- Chi-square tests for association.
- ML classifiers if course/project allows.

## 3. Variation Intuition

Variation is the whole reason statistics exists.

If two classes have average grades 82 and 85, is that a real difference or just
random variation?

You need:

- Difference in means.
- Spread within groups.
- Sample size.

Signal-to-noise idea:

```text
test statistic = signal / noise
```

Examples:

- t statistic = difference in means / standard error.
- z statistic = difference in proportions / standard error.
- F statistic = between-group variation / within-group variation.

If within-group variation is huge, even a visible difference in means might not
be statistically convincing.

## 4. Parametric vs Nonparametric

### Parametric Tests

Assume a specific model/distribution, usually normality or large-sample
approximation.

Examples:

- t-test
- ANOVA
- linear regression
- z-test for proportions

Pros:

- More powerful when assumptions are reasonable.
- Gives clean estimates and confidence intervals.

Cons:

- Can mislead if assumptions are badly violated.

### Nonparametric Tests

Use ranks/counts instead of assuming normal numerical data.

Examples:

- Mann-Whitney/Wilcoxon rank-sum: two independent groups, numerical/ordinal.
- Wilcoxon signed-rank: paired data.
- Kruskal-Wallis: three or more independent groups.
- Chi-square: categorical association.
- Sign test: paired direction only.

Pros:

- Robust to skew/outliers.
- Useful for ordinal rankings.

Cons:

- Often tests distribution/rank differences, not exactly mean differences.
- Can be less powerful.

## 5. Method Picker

| Situation | Response | Groups/Predictors | Method |
|---|---|---|---|
| One numerical sample vs known value | numerical | 1 group | One-sample t-test |
| One proportion vs known value | categorical yes/no | 1 group | One-proportion z-test |
| Two independent group means | numerical | 2 groups | Welch two-sample t-test |
| Two paired means | numerical | same/matched units | Paired t-test |
| 3+ independent group means | numerical | 3+ groups | One-way ANOVA |
| 2 categorical variables | categorical | contingency table | Chi-square test |
| Numerical response, one numerical predictor | numerical | 1 numeric X | Simple linear regression |
| Numerical response, several predictors | numerical | multiple Xs | Multiple regression |
| Binary response, predictors | yes/no | one or more Xs | Logistic regression |
| Humans rank outputs | ordinal/ranks | paired or repeated rankings | Sign test, Wilcoxon, Friedman, or rank aggregation |

## 6. Test Details You Keep Forgetting

### One-Sample t-test

Question:

- Is the population mean different from a known value?

Example:

- Is average class score different from 75?

Formula idea:

```text
t = (sample mean - hypothesized mean) / SE
SE = s / sqrt(n)
```

### Welch Two-Sample t-test

Question:

- Are two independent group means different?

Example:

- Do Class A and Class B have different average exam grades?

Use Welch by default unless professor specifically asks pooled.

Why:

- Welch does not assume equal variances.

### Paired t-test

Question:

- Is the average difference within pairs different from 0?

Examples:

- Same students before/after tutoring.
- Same gas stations on Wednesday and Saturday.
- Matched students with similar starting weights.

Trick:

- Compute differences first, then do a one-sample t-test on differences.

### ANOVA

Question:

- Are 3+ group means all equal?

Example:

- Compare average grades across 4 high school classes.

Hypotheses:

```text
H0: all means equal
HA: at least one mean differs
```

Intuition:

```text
F = between-group variation / within-group variation
```

If F is large, group means are separated relative to noise.

After significant ANOVA:

- Use Tukey HSD to find which pairs differ.

Do not:

- Run many pairwise t-tests without correction.

### Chi-square Test of Independence

Question:

- Are two categorical variables related?

Example:

- Is vehicle size related to region?
- Is pass/fail related to teaching method?

Needs:

- Counts in categories, not means.

### Simple Linear Regression

Question:

- Does X linearly predict numerical Y?

Example:

- Does temperature predict rainfall?

Line:

```text
yhat = b0 + b1*x
```

Slope:

- Expected change in Y for 1-unit increase in X.

R-squared:

- Percent of variation in Y explained by the model.

Residual:

- Error = observed - predicted.

### Multiple Regression

Question:

- Which predictors explain numerical Y after adjusting for others?

Example:

- BMI predicted by age, waist-to-hip ratio, AMH, cycle regularity, etc.

Watch:

- VIF for multicollinearity.
- Residual plot for linearity/constant variance.
- Q-Q plot for residual normality.
- Adjusted R-squared for comparing models with different numbers of predictors.

## 7. How to Read Plots

### Histogram

Look for:

- Shape: normal, skewed, bimodal.
- Outliers.
- Center/spread.

### Boxplot

Look for:

- Median line.
- IQR box.
- Whiskers.
- Outliers.
- Group differences.

### Scatterplot

Look for:

- Direction: positive/negative.
- Form: linear/curved.
- Strength: tight/cloudy.
- Outliers.

### Residual Plot

Good:

- Random scatter around 0.

Bad:

- Curve: relationship not linear.
- Fan shape: nonconstant variance.
- Isolated point: outlier/influential point.

### Q-Q Plot

Good:

- Points near diagonal line.

Bad:

- S-shaped or big tail departures.

For regression:

- Q-Q plot is about residuals, not raw Y.

## 8. Case Study: Comparing High School Classes

### Situation A

You have final exam scores from Class A, B, C, and D.

Response:

- Score, numerical.

Groups:

- 4 independent classes.

Method:

- One-way ANOVA.

Why:

- More than two independent means.

If ANOVA significant:

- Tukey HSD to see which classes differ.

If scores are extremely nonnormal or ordinal:

- Kruskal-Wallis as nonparametric alternative.

### Situation B

Same students take a pre-test and post-test.

Response:

- Score difference.

Groups:

- Paired/repeated.

Method:

- Paired t-test.

If only direction improved/worsened is reliable:

- Sign test.

### Situation C

You only know pass/fail by class.

Response:

- Categorical pass/fail.

Method:

- Chi-square test of independence.

Why:

- Class and pass/fail are categorical.

## 9. Case Study: Comparing Two Knowledge-Pipeline Outputs

### Situation A: Humans Pick Winner A vs B

You show the same prompts to both pipelines and humans choose which output is
better.

Response:

- Paired binary preference: A wins or B wins.

Method:

- Sign test or exact binomial test.

Example:

- A wins 63 out of 100 paired comparisons.
- Test whether win probability is greater than 0.5.

### Situation B: Humans Rank Several Outputs

Each human ranks outputs from 1 to k.

Response:

- Ordinal ranks.

Methods:

- Friedman test if the same judges rank all systems.
- Kruskal-Wallis if independent judges rate different systems.
- Mean/median rank as descriptive summary.

### Situation C: Humans Give 1-5 Ratings

If treating ratings as numerical:

- Paired t-test for two systems rated by same judges.
- Repeated-measures ANOVA for 3+ systems.

If treating ratings as ordinal:

- Wilcoxon signed-rank for two paired systems.
- Friedman test for 3+ paired systems.

### Situation D: Only Aggregate Human Rankings Are Available

If you only have final ordered lists and not raw judge-level data:

- You cannot do strong inference.
- Use descriptive rank comparison.
- Use Kendall tau or Spearman correlation to compare rankings.
- Be explicit that raw paired ratings are needed for a formal test.

## 10. What to Include / Exclude

Include:

- Problem category.
- Variables and types.
- Hypotheses.
- Assumptions.
- Test statistic/p-value/CI.
- Plain-language conclusion.

Exclude:

- Causal claims from observational data.
- Stepwise model fishing unless required.
- Too many unplanned tests without correction.
- Accuracy-only claims for classification; include validation/calibration if
  possible.

## 11. Quick Decision Tree

1. Is Y numerical?
   - Yes: t-test/ANOVA/regression.
   - No: chi-square/logistic/proportion test.

2. How many groups?
   - 1: one-sample test.
   - 2 independent: Welch t-test.
   - 2 paired: paired t-test.
   - 3+: ANOVA.

3. Is X numerical and Y numerical?
   - Use correlation/regression.

4. Are both variables categorical?
   - Use chi-square.

5. Are observations ranked/ordinal?
   - Use rank-based/nonparametric methods.

6. Are data observational?
   - Say "associated with", not "caused".

