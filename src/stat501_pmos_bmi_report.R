cmd_args <- commandArgs(trailingOnly = FALSE)
file_arg <- sub("^--file=", "", cmd_args[grepl("^--file=", cmd_args)])
script_dir <- if (length(file_arg) > 0) dirname(normalizePath(file_arg[1])) else "src"
repo_root <- normalizePath(file.path(script_dir, ".."))
if (!dir.exists(file.path(repo_root, "reports"))) repo_root <- normalizePath(".")

data_path <- file.path(repo_root, "data", "raw", "PCOS_data_without_infertility.xlsx")
fig_dir <- file.path(repo_root, "figures")
results_dir <- file.path(repo_root, "results")
reports_dir <- file.path(repo_root, "reports")
dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(results_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(reports_dir, showWarnings = FALSE, recursive = TRUE)

if (!requireNamespace("readxl", quietly = TRUE)) {
  stop("Package 'readxl' is required. Install with: install.packages('readxl')")
}

num <- function(x) suppressWarnings(as.numeric(x))
fmt <- function(x, digits = 3) formatC(x, digits = digits, format = "f")
fmtp <- function(p) ifelse(is.na(p), "", ifelse(p < 0.001, "$p<0.001$", paste0("$p=", fmt(p, 4), "$")))

raw <- as.data.frame(readxl::read_excel(data_path, sheet = "Full_new"))

df <- data.frame(
  pcos = num(raw[["PCOS (Y/N)"]]),
  age = num(raw[["Age (yrs)"]]),
  bmi = num(raw[["BMI"]]),
  cycle = num(raw[["Cycle(R/I)"]]),
  cycle_length = num(raw[["Cycle length(days)"]]),
  fsh = num(raw[["FSH(mIU/mL)"]]),
  lh = num(raw[["LH(mIU/mL)"]]),
  waist_hip_ratio = num(raw[["Waist:Hip Ratio"]]),
  tsh = num(raw[["TSH (mIU/L)"]]),
  amh = num(raw[["AMH(ng/mL)"]]),
  prl = num(raw[["PRL(ng/mL)"]]),
  vit_d3 = num(raw[["Vit D3 (ng/mL)"]]),
  prg = num(raw[["PRG(ng/mL)"]]),
  rbs = num(raw[["RBS(mg/dl)"]]),
  weight_gain = num(raw[["Weight gain(Y/N)"]]),
  fast_food = num(raw[["Fast food (Y/N)"]]),
  regular_exercise = num(raw[["Reg.Exercise(Y/N)"]]),
  follicle_l = num(raw[["Follicle No. (L)"]]),
  follicle_r = num(raw[["Follicle No. (R)"]]),
  avg_f_size_l = num(raw[["Avg. F size (L) (mm)"]]),
  avg_f_size_r = num(raw[["Avg. F size (R) (mm)"]]),
  endometrium = num(raw[["Endometrium (mm)"]])
)
df$cycle_group <- factor(ifelse(df$cycle == 4, "Irregular", "Regular"), levels = c("Regular", "Irregular"))
df$total_follicles <- df$follicle_l + df$follicle_r
df$lh_fsh_ratio <- df$lh / df$fsh

pcos <- df[df$pcos == 1, ]
pcos <- pcos[!is.na(pcos$bmi), ]
ranked <- rank(pcos$total_follicles, ties.method = "first", na.last = "keep")
pcos$follicle_group <- cut(
  ranked,
  breaks = quantile(ranked, probs = seq(0, 1, length.out = 4), na.rm = TRUE),
  include.lowest = TRUE,
  labels = c("Low", "Medium", "High")
)

bmi_mean <- mean(pcos$bmi, na.rm = TRUE)
bmi_sd <- sd(pcos$bmi, na.rm = TRUE)
bmi_n <- sum(!is.na(pcos$bmi))
bmi_skew <- mean((pcos$bmi - bmi_mean)^3, na.rm = TRUE) / bmi_sd^3
bmi_ci <- t.test(pcos$bmi)$conf.int

simple_df <- pcos[complete.cases(pcos[, c("bmi", "waist_hip_ratio")]), ]
simple_model <- lm(bmi ~ waist_hip_ratio, data = simple_df)
simple_cor <- cor.test(simple_df$bmi, simple_df$waist_hip_ratio)

cycle_df <- pcos[complete.cases(pcos[, c("bmi", "cycle_group")]), ]
cycle_test <- t.test(bmi ~ cycle_group, data = cycle_df, var.equal = FALSE)
cycle_means <- tapply(cycle_df$bmi, cycle_df$cycle_group, mean)
cycle_ns <- tapply(cycle_df$bmi, cycle_df$cycle_group, length)
cycle_diff <- unname(cycle_means["Irregular"] - cycle_means["Regular"])
cycle_ci_irregular_minus_regular <- -rev(cycle_test$conf.int)

anova_df <- pcos[complete.cases(pcos[, c("bmi", "follicle_group")]), ]
anova_model <- lm(bmi ~ follicle_group, data = anova_df)
anova_out <- anova(anova_model)

model_df <- pcos[complete.cases(pcos[, c(
  "bmi", "age", "waist_hip_ratio", "amh", "lh_fsh_ratio", "tsh", "prl", "rbs",
  "cycle_group", "weight_gain", "fast_food", "regular_exercise", "total_follicles",
  "follicle_l", "follicle_r", "avg_f_size_l", "avg_f_size_r", "endometrium"
)]), ]

full_model <- lm(
  bmi ~ age + waist_hip_ratio + amh + lh_fsh_ratio + tsh + prl + rbs +
    cycle_group + weight_gain + fast_food + regular_exercise + total_follicles,
  data = model_df
)
clinical_model <- lm(
  bmi ~ age + waist_hip_ratio + cycle_group + weight_gain + fast_food + regular_exercise,
  data = model_df
)

vif_manual <- function(model) {
  x <- model.matrix(model)
  x <- x[, colnames(x) != "(Intercept)", drop = FALSE]
  out <- numeric(ncol(x))
  for (i in seq_len(ncol(x))) {
    r2 <- summary(lm(x[, i] ~ x[, -i, drop = FALSE]))$r.squared
    out[i] <- 1 / (1 - r2)
  }
  data.frame(variable = colnames(x), VIF = round(out, 3))
}
vif_table <- vif_manual(full_model)

block_df <- model_df
block_models <- list(
  "Clinical only" = clinical_model,
  "Laboratory only" = lm(bmi ~ amh + lh_fsh_ratio + tsh + prl + rbs, data = block_df),
  "Ultrasound only" = lm(bmi ~ follicle_l + follicle_r + avg_f_size_l + avg_f_size_r + endometrium, data = block_df),
  "Clinical + lab" = lm(
    bmi ~ age + waist_hip_ratio + cycle_group + weight_gain + fast_food + regular_exercise +
      amh + lh_fsh_ratio + tsh + prl + rbs,
    data = block_df
  ),
  "Clinical + ultrasound" = lm(
    bmi ~ age + waist_hip_ratio + cycle_group + weight_gain + fast_food + regular_exercise +
      follicle_l + follicle_r + avg_f_size_l + avg_f_size_r + endometrium,
    data = block_df
  ),
  "Full multimodal" = lm(
    bmi ~ age + waist_hip_ratio + cycle_group + weight_gain + fast_food + regular_exercise +
      amh + lh_fsh_ratio + tsh + prl + rbs +
      follicle_l + follicle_r + avg_f_size_l + avg_f_size_r + endometrium,
    data = block_df
  )
)
block_table <- data.frame(
  Model = names(block_models),
  n = sapply(block_models, nobs),
  AdjR2 = sapply(block_models, function(m) summary(m)$adj.r.squared),
  AIC = sapply(block_models, AIC),
  row.names = NULL
)

key_results <- data.frame(
  Analysis = c("BMI mean CI", "Simple regression", "Welch t-test", "One-way ANOVA", "Clinical model"),
  Result = c(
    paste0("Mean ", fmt(bmi_mean, 2), ", 95\\% CI (", fmt(bmi_ci[1], 2), ", ", fmt(bmi_ci[2], 2), ")"),
    paste0("WHR slope ", fmt(coef(simple_model)[2], 2), ", r=", fmt(simple_cor$estimate, 3), ", p=", fmt(simple_cor$p.value, 4)),
    paste0("Irregular - regular mean diff ", fmt(cycle_diff, 2), ", 95\\% CI (", fmt(cycle_ci_irregular_minus_regular[1], 2), ", ", fmt(cycle_ci_irregular_minus_regular[2], 2), "), p=", fmt(cycle_test$p.value, 4)),
    paste0("Follicle group F=", fmt(anova_out$`F value`[1], 2), ", p=", fmt(anova_out$`Pr(>F)`[1], 4)),
    paste0("Adjusted R2=", fmt(summary(clinical_model)$adj.r.squared, 3), "; weight gain ", fmtp(summary(clinical_model)$coefficients["weight_gain", "Pr(>|t|)"]))
  )
)
write.csv(key_results, file.path(results_dir, "stat501_key_results_r.csv"), row.names = FALSE)
write.csv(vif_table, file.path(results_dir, "stat501_vif_values_r.csv"), row.names = FALSE)
write.csv(block_table, file.path(results_dir, "stat501_model_blocks_r.csv"), row.names = FALSE)

png(file.path(fig_dir, "stat501_core_plots.png"), width = 1800, height = 1250, res = 180)
par(mfrow = c(2, 2), mar = c(4.2, 4.2, 2.6, 1), oma = c(0, 0, 1.4, 0), bg = "white")
hist(pcos$bmi, breaks = 18, col = "#2f6f73", border = "white", main = "BMI Distribution", xlab = "BMI")
abline(v = bmi_mean, col = "black", lwd = 2)
hist(simple_df$waist_hip_ratio, breaks = 16, col = "#7a9e7e", border = "white", main = "Waist-to-Hip Ratio", xlab = "Waist-to-hip ratio")
plot(simple_df$waist_hip_ratio, simple_df$bmi, pch = 19, col = rgb(47, 111, 115, 150, maxColorValue = 255),
     main = "BMI vs Waist-to-Hip Ratio", xlab = "Waist-to-hip ratio", ylab = "BMI")
abline(simple_model, col = "#9a4a44", lwd = 2)
boxplot(bmi ~ cycle_group, data = cycle_df, col = c("#b9c8a8", "#d49a3a"), border = "#333333",
        main = "BMI by Cycle Regularity", xlab = "Cycle group", ylab = "BMI")
stripchart(bmi ~ cycle_group, data = cycle_df, vertical = TRUE, method = "jitter", pch = 19,
           col = rgb(0, 0, 0, 80, maxColorValue = 255), add = TRUE)
mtext("BMI and Clinical Predictors", outer = TRUE, font = 2, cex = 1.1)
dev.off()

png(file.path(fig_dir, "stat501_anova_and_diagnostics.png"), width = 1800, height = 850, res = 180)
par(mfrow = c(1, 3), mar = c(4.2, 4.2, 2.8, 1), bg = "white")
boxplot(bmi ~ follicle_group, data = anova_df, col = c("#b9c8a8", "#d7c46a", "#d49a3a"),
        border = "#333333", main = "ANOVA: BMI by Follicle Group", xlab = "Follicle group", ylab = "BMI")
plot(fitted(full_model), resid(full_model), pch = 19, col = rgb(47, 111, 115, 150, maxColorValue = 255),
     main = "Regression Residuals", xlab = "Fitted BMI", ylab = "Residuals")
abline(h = 0, lwd = 2)
qqnorm(resid(full_model), pch = 19, col = rgb(47, 111, 115, 150, maxColorValue = 255),
       main = "Normal Q-Q")
qqline(resid(full_model), col = "#9a4a44", lwd = 2)
dev.off()

png(file.path(fig_dir, "stat501_model_block_r2.png"), width = 1200, height = 800, res = 180)
par(mar = c(4.2, 8.2, 2.8, 1), bg = "white")
ord <- order(block_table$AdjR2)
barplot(block_table$AdjR2[ord], names.arg = block_table$Model[ord], horiz = TRUE, las = 1,
        col = "#6b8f71", border = NA, xlab = "Adjusted R-squared",
        main = "BMI Model Comparison by Predictor Block")
abline(v = 0, lwd = 1)
dev.off()

latex_block_rows <- paste(
  sprintf(
    "%s & %d & %s & %s \\\\",
    block_table$Model, block_table$n, fmt(block_table$AdjR2, 3), fmt(block_table$AIC, 1)
  ),
  collapse = "\n"
)

latex_key_rows <- paste(
  sprintf("%s & %s \\\\", key_results$Analysis, key_results$Result),
  collapse = "\n"
)

vif_max <- max(vif_table$VIF, na.rm = TRUE)

tex <- paste0(
"\\documentclass[10pt,twocolumn]{article}
\\usepackage[margin=0.68in]{geometry}
\\usepackage{booktabs}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{xurl}
\\usepackage{microtype}
\\usepackage{amsmath}
\\usepackage{array}
\\usepackage{caption}
\\usepackage{float}
\\usepackage{xcolor}
\\usepackage{enumitem}
\\usepackage{cuted}
\\captionsetup{font=small,labelfont=bf}
\\hypersetup{colorlinks=true,urlcolor=blue,citecolor=blue,linkcolor=blue}
\\definecolor{cardbg}{HTML}{F2F7F5}
\\definecolor{cardline}{HTML}{2F6F73}
\\setlist[itemize]{leftmargin=*, itemsep=1pt, topsep=2pt}
\\newcommand{\\infocard}[2]{\\vspace{0.35em}\\noindent\\fcolorbox{cardline}{cardbg}{\\begin{minipage}{0.94\\columnwidth}\\textbf{#1}\\par\\vspace{0.2em}#2\\end{minipage}}\\vspace{0.45em}}
\\newcommand{\\snapshot}[1]{\\begin{strip}\\vspace{-0.8em}\\noindent\\fcolorbox{cardline}{cardbg}{\\begin{minipage}{0.965\\textwidth}#1\\end{minipage}}\\vspace{-0.4em}\\end{strip}}

\\title{Clinical Predictors of BMI in PCOS/PMOS}
\\author{Soumitra Das \\and Shreya Saha \\and Anjali Kanvinde \\and Shivraj Singh Bhatti \\and Pranav Jeyakumar}
\\date{May 2026}

\\begin{document}
\\sloppy
\\maketitle

\\begin{abstract}
We analyze a public Kaggle dataset on polycystic ovary syndrome, now more precisely framed as polyendocrine metabolic ovarian syndrome (PMOS), to ask which measured clinical and hormonal variables are associated with BMI among PCOS-positive participants. The analysis uses descriptive statistics, confidence intervals, correlation, simple linear regression, Welch's two-sample t-test, one-way ANOVA, and linear-model diagnostics. The key finding is that self-reported weight gain is the strongest BMI-related variable, while the available laboratory variables explain little BMI variation because direct metabolic biosignals such as fasting insulin and HOMA-IR are absent.
\\end{abstract}

\\snapshot{\\textbf{Study Snapshot}\\vspace{0.25em}
\\begin{itemize}
\\item \\textbf{Research question:} among PCOS-positive participants, which measured variables are associated with BMI?
\\item \\textbf{Unit and response:} one patient record; BMI is the numerical response variable.
\\item \\textbf{Key explanatory variables:} waist-to-hip ratio, cycle regularity, follicle-count group, self-reported weight gain, and available laboratory measures such as AMH, LH/FSH ratio, TSH, PRL, and random blood sugar.
\\item \\textbf{Statistical approach:} descriptive statistics, 95\\% confidence intervals, correlation, simple linear regression, Welch's two-sample t-test, one-way ANOVA, and linear-model diagnostics.
\\item \\textbf{Interpretation:} results are associations from an observational dataset, not causal effects.
\\end{itemize}}

\\section{Introduction}
PCOS was renamed PMOS in 2026 to emphasize that the condition is not only ovarian but also endocrine and metabolic \\cite{endocrine,monash}. Our research question is: \\textbf{among PCOS-positive participants, which measured variables are associated with BMI?} This matters statistically and clinically because BMI is related to metabolic risk, but the public dataset may not contain the direct metabolic variables needed to explain it.

\\section{Data}
The Kaggle workbook by Kottarathil contains 541 rows and 45 columns \\cite{kaggle}. We restricted the main analysis to the 177 PCOS-positive participants. The BMI distribution was mildly right-skewed (skewness ", fmt(bmi_skew, 3), "), with mean ", fmt(bmi_mean, 2), " and SD ", fmt(bmi_sd, 2), ". A 95\\% confidence interval for the mean BMI is (", fmt(bmi_ci[1], 2), ", ", fmt(bmi_ci[2], 2), "). The second Kaggle infertility file was audited separately; it appears to contain the same patients with offset IDs and duplicate AMH/beta-HCG fields, so it does not add fasting insulin, testosterone, fasting glucose, or HOMA-IR.

\\begin{figure*}[t]
\\centering
\\includegraphics[width=0.94\\textwidth]{../figures/stat501_core_plots.png}
\\caption{Distributions of BMI and waist-to-hip ratio, scatterplot for simple regression, and side-by-side BMI boxplots by cycle regularity.}
\\label{fig:core}
\\end{figure*}

\\section{Analysis}
\\begin{table}[H]
\\caption{Primary statistical results, with interpretation in context.}
\\label{tab:key}
\\small\\resizebox{\\columnwidth}{!}{\\begin{tabular}{ll}
\\toprule
Analysis & Result \\\\
\\midrule
", latex_key_rows, "
\\bottomrule
\\end{tabular}}
\\end{table}

For the simple linear regression, the scatterplot does not show a strong linear trend. The estimated slope is ", fmt(coef(simple_model)[2], 2), ", meaning a 1.0 increase in waist-to-hip ratio is associated with about ", fmt(coef(simple_model)[2], 2), " BMI units, but this effect is not statistically significant ($p=", fmt(simple_cor$p.value, 4), "$). The correlation is weak ($r=", fmt(simple_cor$estimate, 3), "$), so waist-to-hip ratio alone is not a useful BMI predictor in this subset.

The Welch t-test compares two independent groups: regular versus irregular menstrual cycles. Mean BMI is ", fmt(cycle_means["Regular"], 2), " for regular cycles and ", fmt(cycle_means["Irregular"], 2), " for irregular cycles. The estimated irregular-minus-regular difference is ", fmt(cycle_diff, 2), " BMI units, with 95\\% CI (", fmt(cycle_ci_irregular_minus_regular[1], 2), ", ", fmt(cycle_ci_irregular_minus_regular[2], 2), ") and $p=", fmt(cycle_test$p.value, 4), "$. This suggests higher BMI among irregular-cycle participants before adjusting for other variables.

The ANOVA compares mean BMI across low, medium, and high follicle-count groups. The group means are very similar, and the ANOVA is not significant ($F=", fmt(anova_out$`F value`[1], 2), "$, $p=", fmt(anova_out$`Pr(>F)`[1], 4), "$). Since the overall ANOVA is not significant, Tukey multiple comparisons are not needed.

\\begin{figure*}[t]
\\centering
\\includegraphics[width=0.94\\textwidth]{../figures/stat501_anova_and_diagnostics.png}
\\caption{ANOVA boxplot and regression diagnostic plots. The residual plot shows no strong curved pattern, and the Q-Q plot is acceptable with some tail departures.}
\\label{fig:diagnostics}
\\end{figure*}

As an exploratory linear-model extension, we compared predictor blocks using adjusted $R^2$. The clinical block has adjusted $R^2=", fmt(summary(clinical_model)$adj.r.squared, 3), "$, while the laboratory-only block has adjusted $R^2=", fmt(block_table$AdjR2[block_table$Model == "Laboratory only"], 3), "$. The maximum non-intercept VIF in the full model is ", fmt(vif_max, 2), ", so multicollinearity is not driving the result.

\\begin{table}[H]
\\caption{Linear-model block comparison for BMI.}
\\label{tab:block}
\\small\\resizebox{\\columnwidth}{!}{\\begin{tabular}{lrrr}
\\toprule
Model block & n & Adj. $R^2$ & AIC \\\\
\\midrule
", latex_block_rows, "
\\bottomrule
\\end{tabular}}
\\end{table}

\\section{Conclusions}
The strongest BMI-related signal in this dataset is self-reported weight gain. Cycle irregularity is associated with higher BMI in the two-sample comparison, but follicle-count group and waist-to-hip ratio do not show strong independent evidence. The most important data concern is measurement coverage: the dataset is strong on reproductive and ovarian variables but weak on the metabolic biosignals emphasized by PMOS. It lacks fasting insulin, fasting glucose, HOMA-IR, lipids, OGTT, and testosterone. If we could collect our own data, we would design a prospective PMOS study with fasting metabolic labs, androgen assays, blood pressure, validated mental-health scales, and longitudinal follow-up. Therefore, our null laboratory-block result should be read as a data limitation, not as evidence that metabolic mechanisms do not matter.

\\begin{thebibliography}{9}
\\bibitem{endocrine} Endocrine Society, ``Polyendocrine Metabolic Ovarian Syndrome: New name to improve diagnosis and care,'' May 12, 2026. \\url{https://www.endocrine.org/news-and-advocacy/news-room/2026/pcos-name-change}
\\bibitem{monash} Monash University, ``Polyendocrine Metabolic Ovarian Syndrome: New name to improve diagnosis and care,'' May 13, 2026. \\url{https://www.monash.edu/medicine/news/latest/2026-articles/polyendocrine-metabolic-ovarian-syndrome-new-name-to-improve-diagnosis-and-care-of-condition-affecting-170-million-women-worldwide}
\\bibitem{kaggle} P. Kottarathil, ``Polycystic ovary syndrome (PCOS),'' Kaggle dataset. \\url{https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos}
\\bibitem{guideline} H. J. Teede et al., ``Recommendations from the 2023 international evidence-based guideline for the assessment and management of polycystic ovary syndrome,'' \\textit{J. Clin. Endocrinol. Metab.}, 2023.
\\end{thebibliography}

\\end{document}
")

writeLines(sub("\\n+$", "", tex), file.path(reports_dir, "stat501_pmos_bmi_final.tex"))
capture.output(sessionInfo(), file = file.path(results_dir, "stat501_r_session_info.txt"))
