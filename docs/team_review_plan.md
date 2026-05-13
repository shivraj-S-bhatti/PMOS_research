# Team Review Plan and Ask

Use this when teammates ask what they can review or help with.

## Quick Message to Send

Hey, I pushed the current project repo here:

https://github.com/shivraj-S-bhatti/PMOS_research

The main files to review are:

- `docs/team_first_run_reference.md`
- `reports/pcos_bmi_team_brief.pdf`
- `reports/pcos_bmi_team_brief.tex`
- `src/pcos_bmi_analysis.py`
- `docs/dataset_audit_and_followup.md`
- `docs/reference_bank.md`

Can you each take one review lane below and leave comments/suggestions?

## Review Lanes

### 1. Dataset / Variables Review

Goal:

- Confirm the Kaggle variables we use are named and interpreted correctly.
- Check that the note about missing insulin/testosterone is clear.
- Review the two-file audit: same 541 patients, patient IDs offset by 10000,
  infertility CSV only duplicates AMH and beta-HCG.

Questions:

- Is our explanation of the two-file structure clear enough?
- Should we include the second CSV audit in the final paper, or only in
  limitations?
- Do we need a variable dictionary/table in the final report?

### 2. Statistics / Methods Review

Goal:

- Check whether each method matches the proposal and course expectations.

Methods included:

- Descriptive statistics
- BMI histogram/skewness
- Pearson correlation
- Simple linear regression
- Welch two-sample t-test
- One-way ANOVA
- Multiple linear regression
- Adjusted R-squared model comparison
- VIF
- Residual plot and Q-Q plot
- Sensitivity checks

Questions:

- Is the methods section too broad?
- Should model block comparison stay in the main paper or appendix?
- Should we remove interaction models if page count is tight?

### 3. Literature Review Review

Goal:

- Help turn `docs/reference_bank.md` into a concise IEEE-style literature review.

Questions:

- Which references are strongest?
- Which claims need exact citations?
- Should the final review focus more on Kaggle classification work, PCOS
  metabolic heterogeneity, or missing insulin/HOMA-IR?

### 4. Run 2 / Extra Experiment Review

Goal:

- Decide whether to add a Mendeley extension or leave it as future work.

Candidate datasets:

- https://data.mendeley.com/datasets/tw34c7hv7z/1
- https://data.mendeley.com/datasets/ny225jgpwf/1

Questions:

- Can someone download/check these files and list columns?
- Do they include BMI, fasting insulin, fasting glucose, testosterone, and PCOS
  status?
- If yes, should we run a small second analysis with HOMA-IR?

## Experiments to Run After Review

Minimum final paper:

1. Keep current Kaggle BMI analysis.
2. Tighten limitation language.
3. Add dataset audit note.
4. Keep paper under 6 pages.

Optional extension:

1. Download Mendeley `tw34c7hv7z/1`.
2. Inspect variables and missingness.
3. Compute HOMA-IR if fasting glucose and insulin are present.
4. Run a small BMI regression:

   `BMI ~ HOMA_IR + testosterone + AMH + age + PCOS_status`

5. Compare to Kaggle result:

   - Kaggle: self-reported weight gain dominates.
   - Mendeley: test whether direct metabolic markers explain BMI better.

## Suggested Division of Work

- Person A: read the PDF and check narrative clarity.
- Person B: check code and reproducibility.
- Person C: verify references and build IEEE bibliography.
- Person D: inspect Mendeley dataset availability.
- Person E: help trim final paper to <= 6 pages.
