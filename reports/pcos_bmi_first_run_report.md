# Concise First Run: Predictors of BMI in PCOS

Dataset: Kaggle PCOS dataset by Prasoon Kottarathil. Analysis subset: PCOS-positive participants only.

- Full dataset rows: 541
- PCOS-positive rows used for main analysis: 177
- Complete cases in multiple linear regression: 176
- Note: fasting insulin and testosterone were not available in this workbook, so this first run uses available clinical and hormonal variables.

## Descriptive Statistics

|                 |   count |    mean |    std |    min |    25% |     50% |     75% |     max |
|:----------------|--------:|--------:|-------:|-------:|-------:|--------:|--------:|--------:|
| bmi             |     177 |  25.471 |  4.396 | 12.418 | 23.011 |  25.1   |  28.3   |  38.9   |
| age             |     177 |  30.124 |  5.292 | 21     | 27     |  29     |  33     |  47     |
| waist_hip_ratio |     177 |   0.893 |  0.046 |  0.756 |  0.864 |   0.897 |   0.927 |   0.979 |
| amh             |     177 |   7.845 |  7.791 |  0.1   |  2.6   |   5.9   |  10.2   |  66     |
| lh_fsh_ratio    |     177 |   3.271 | 34.986 |  0.003 |  0.3   |   0.491 |   0.928 | 466.051 |
| tsh             |     177 |   2.927 |  2.823 |  0.05  |  1.57  |   2.31  |   3.51  |  22.59  |
| prl             |     177 |  24.432 | 13.887 |  3.64  | 14.13  |  22.9   |  30.33  | 111.74  |
| rbs             |     177 | 101.137 | 23.633 | 70     | 92     | 100     | 107     | 350     |
| total_follicles |     177 |  20.548 |  7.584 |  2     | 16     |  20     |  25     |  41     |
| avg_f_size_l    |     177 |  15.698 |  2.731 |  5     | 14     |  16     |  18     |  24     |
| avg_f_size_r    |     177 |  15.916 |  3.089 |  0.17  | 14     |  16     |  18     |  23     |
| endometrium     |     177 |   8.807 |  1.924 |  4.5   |  7.6   |   8.9   |  10     |  15     |

BMI skewness among PCOS-positive participants: **0.232**.

## Simple Linear Regression

Response variable: BMI. Explanatory variable: waist-to-hip ratio.

- Pearson correlation: r = **0.084**, p = **0.2678**
- Slope estimate: **7.928** BMI units per 1.0 WHR, p = **0.2678**
- R-squared: **0.007**

## Two-Sample t-Test

Comparison: mean BMI for regular vs. irregular menstrual cycles.

| cycle_group   |   count |   mean |   std |   median |
|:--------------|--------:|-------:|------:|---------:|
| Irregular     |      94 | 26.282 | 4.583 |   25.591 |
| Regular       |      82 | 24.53  | 4.025 |   24.4   |

Welch two-sample t-test: t = **-2.700**, p = **0.007612**.

## One-Way ANOVA

Comparison: mean BMI across low, medium, and high total follicle-count groups, used here as a simple severity proxy.

| follicle_group   |   count |   mean |   std |   median |
|:-----------------|--------:|-------:|------:|---------:|
| Low              |      59 | 25.354 | 4.352 |   25.236 |
| Medium           |      59 | 25.682 | 4.521 |   26.023 |
| High             |      59 | 25.377 | 4.381 |   24.6   |

|                   |     sum_sq |   df |         F |    PR(>F) |
|:------------------|-----------:|-----:|----------:|----------:|
| C(follicle_group) |    3.94963 |    2 |   0.10114 |   0.90386 |
| Residual          | 3397.4     |  174 | nan       | nan       |

Tukey HSD not run because the overall ANOVA was not significant.

## Multiple Linear Regression

- Full model adjusted R-squared: **0.237**
- Reduced model adjusted R-squared: **0.260**
- Coefficients from the full model:

| term                      |   estimate |   std_error |   p_value |   conf_low |   conf_high |
|:--------------------------|-----------:|------------:|----------:|-----------:|------------:|
| Intercept                 |     9.3547 |      6.2831 |    0.1385 |    -3.0521 |     21.7615 |
| C(cycle_group)[T.Regular] |    -0.653  |      0.6167 |    0.2912 |    -1.8708 |      0.5647 |
| age                       |     0.0722 |      0.0608 |    0.2371 |    -0.0479 |      0.1923 |
| waist_hip_ratio           |    11.3414 |      6.9687 |    0.1056 |    -2.4192 |     25.1021 |
| amh                       |     0.0163 |      0.0392 |    0.6788 |    -0.0611 |      0.0936 |
| lh_fsh_ratio              |     0.0036 |      0.0085 |    0.6712 |    -0.0132 |      0.0205 |
| tsh                       |     0.1016 |      0.1042 |    0.3308 |    -0.1041 |      0.3073 |
| prl                       |     0.0073 |      0.0219 |    0.7403 |    -0.0359 |      0.0504 |
| rbs                       |     0.0009 |      0.0126 |    0.941  |    -0.0239 |      0.0257 |
| weight_gain               |     4.3214 |      0.6858 |    0      |     2.9671 |      5.6756 |
| fast_food                 |     0.9653 |      0.7697 |    0.2116 |    -0.5546 |      2.4851 |
| regular_exercise          |    -0.3525 |      0.6975 |    0.614  |    -1.7298 |      1.0248 |
| total_follicles           |    -0.0107 |      0.0389 |    0.7844 |    -0.0875 |      0.0662 |

### VIF Values

| variable            |     VIF |
|:--------------------|--------:|
| const               | 468.514 |
| age                 |   1.218 |
| waist_hip_ratio     |   1.231 |
| amh                 |   1.105 |
| lh_fsh_ratio        |   1.059 |
| tsh                 |   1.023 |
| prl                 |   1.092 |
| rbs                 |   1.046 |
| weight_gain         |   1.199 |
| fast_food           |   1.19  |
| regular_exercise    |   1.188 |
| total_follicles     |   1.032 |
| cycle_group_Regular |   1.123 |

### Correlation Matrix

|                 |    bmi |    age |   waist_hip_ratio |    amh |   lh_fsh_ratio |    rbs |   total_follicles |
|:----------------|-------:|-------:|------------------:|-------:|---------------:|-------:|------------------:|
| bmi             |  1     |  0.118 |             0.083 |  0.033 |         -0.042 |  0.095 |            -0.01  |
| age             |  0.118 |  1     |             0.262 | -0.166 |          0.023 |  0.105 |             0.065 |
| waist_hip_ratio |  0.083 |  0.262 |             1     |  0.012 |         -0.006 |  0.055 |            -0.032 |
| amh             |  0.033 | -0.166 |             0.012 |  1     |          0.002 | -0.023 |            -0.084 |
| lh_fsh_ratio    | -0.042 |  0.023 |            -0.006 |  0.002 |          1     | -0.026 |            -0.078 |
| rbs             |  0.095 |  0.105 |             0.055 | -0.023 |         -0.026 |  1     |             0.031 |
| total_follicles | -0.01  |  0.065 |            -0.032 | -0.084 |         -0.078 |  0.031 |             1     |

## Extensions Worth Adding

### Clinical, Laboratory, and Ultrasound Model Blocks

| Model block           |   n |   Adj. R2 |    AIC |
|:----------------------|----:|----------:|-------:|
| Clinical only         | 176 |     0.257 |  976.2 |
| Laboratory only       | 176 |    -0.008 | 1029   |
| Ultrasound only       | 176 |     0.046 | 1019.3 |
| Clinical + lab        | 176 |     0.241 |  984.7 |
| Clinical + ultrasound | 176 |     0.269 |  978   |
| Full multimodal       | 176 |     0.255 |  986   |

### BMI Subgroup Checks

| Variable        |   BMI < 24 mean |   BMI >= 24 mean |     p |
|:----------------|----------------:|-----------------:|------:|
| AMH             |           8.265 |            7.618 | 0.637 |
| Waist:hip ratio |           0.89  |            0.894 | 0.523 |
| Total follicles |          21.226 |           20.183 | 0.399 |
| RBS             |          99.242 |          102.158 | 0.356 |

### PCOS vs Non-PCOS Context

| Variable        |   PCOS mean |   Non-PCOS mean | p        |
|:----------------|------------:|----------------:|:---------|
| BMI             |      25.471 |          23.747 | $<0.001$ |
| AMH             |       7.845 |           4.541 | $<0.001$ |
| Waist:hip ratio |       0.893 |           0.891 | 0.774    |
| Total follicles |      20.548 |           8.989 | $<0.001$ |
| Weight gain     |       0.684 |           0.228 | $<0.001$ |
| Fast food       |       0.785 |           0.383 | $<0.001$ |
| Irregular cycle |       0.531 |           0.154 | $<0.001$ |

### Interaction Models

| Model                |   n |   Adj. R2 |   AIC |
|:---------------------|----:|----------:|------:|
| Clinical base        | 176 |     0.257 | 976.2 |
| Cycle x weight gain  | 176 |     0.261 | 976.2 |
| Fast food x exercise | 176 |     0.265 | 975.3 |
| AMH x follicles      | 176 |     0.264 | 985.7 |

### Sensitivity Checks

| Sensitivity check        |   n |   Adj. R2 |   Weight gain beta | Weight gain p   |
|:-------------------------|----:|----------:|-------------------:|:----------------|
| Original full model      | 176 |     0.255 |              4.195 | $<0.001$        |
| Log AMH and log LH/FSH   | 176 |     0.258 |              4.154 | $<0.001$        |
| Exclude BMI IQR outliers | 171 |     0.24  |              3.441 | $<0.001$        |

## First-Run Interpretation

Waist-to-hip ratio had only a weak, non-significant linear association with BMI in this PCOS-positive subset. The two-sample t-test suggested higher mean BMI for irregular cycles than regular cycles, but this difference was smaller after adjusting for other variables in the multiple regression. Follicle-count group did not show a statistically significant difference in mean BMI by one-way ANOVA. In the multiple linear regression, self-reported weight gain was the clearest predictor of BMI, and the reduced model had a slightly higher adjusted R-squared than the larger candidate model. The next best improvement is to confirm whether another file/version contains fasting insulin and testosterone, then rerun the candidate-predictor model.

## Figures

- [amh_by_bmi_subgroup.png](../figures/amh_by_bmi_subgroup.png)
- [amh_by_pcos_status.png](../figures/amh_by_pcos_status.png)
- [bmi_by_cycle_group.png](../figures/bmi_by_cycle_group.png)
- [bmi_by_follicle_group.png](../figures/bmi_by_follicle_group.png)
- [bmi_distribution.png](../figures/bmi_distribution.png)
- [bmi_vs_waist_hip_ratio.png](../figures/bmi_vs_waist_hip_ratio.png)
- [model_block_adjusted_r2.png](../figures/model_block_adjusted_r2.png)
- [multiple_regression_qq.png](../figures/multiple_regression_qq.png)
- [multiple_regression_residuals.png](../figures/multiple_regression_residuals.png)