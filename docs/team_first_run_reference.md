# Team First-Run Reference

Start here if you are reviewing the first PCOS/PMOS BMI analysis.

## Main Files

- Team PDF: `reports/pcos_bmi_team_brief.pdf`
- Team LaTeX: `reports/pcos_bmi_team_brief.tex`
- Full generated first-run notes: `reports/pcos_bmi_first_run_report.md`
- Reproducible analysis code: `src/pcos_bmi_analysis.py`
- R-only STAT 501 report code: `src/stat501_pmos_bmi_report.R`
- Professor-facing final draft: `reports/stat501_pmos_bmi_final.pdf`
- Public PMOS value-add brief: `reports/pmos_public_value_brief.pdf`

## First-Run Question

Among PCOS-positive participants in the Kaggle PCOS dataset, which measured
clinical, hormonal, lifestyle, and ultrasound variables are associated with BMI?

## Core Results

- Full Kaggle workbook: 541 rows.
- Main BMI subset: 177 PCOS-positive participants.
- BMI distribution: mean 25.47, SD 4.40, skewness 0.232.
- Simple regression: waist-to-hip ratio was not a significant BMI predictor
  (`r = 0.084`, `p = 0.2678`, `R2 = 0.007`).
- Welch t-test: irregular-cycle group had higher mean BMI than regular-cycle
  group before adjustment (`p = 0.0076`).
- One-way ANOVA: BMI did not differ significantly across low/medium/high
  follicle-count groups (`p = 0.9039`).
- Multiple regression: self-reported weight gain was the strongest BMI-related
  predictor (`p < 0.001`).
- Model blocks: clinical-only adjusted `R2 = 0.257`; laboratory-only adjusted
  `R2 = -0.008`; full multimodal adjusted `R2 = 0.255`.

## PMOS-Era Interpretation

The result is not that hormones or metabolism do not matter. The result is that
this public Kaggle dataset is weak for metabolic mechanism modeling because it
does not include fasting insulin, fasting glucose, HOMA-IR, lipids, OGTT, or
testosterone. It is stronger for reproductive/ovarian and symptom-based
questions than for direct PMOS metabolic biosignal analysis.

## Figures to Review First

- `figures/bmi_distribution.png`
- `figures/bmi_by_cycle_group.png`
- `figures/model_block_adjusted_r2.png`
- `figures/multiple_regression_diagnostics.png`
- `figures/pmos_construct_coverage.png`

## Result Tables to Review First

- `results/descriptive_statistics.csv`
- `results/model_block_comparison.csv`
- `results/multiple_regression_coefficients.csv`
- `results/vif_values.csv`
- `results/pmos_coverage_table.csv`

## What Teammates Should Check

- Are the statistical methods aligned with STAT 501 expectations?
- Are the conclusions framed as association, not causation?
- Is the missing-insulin/testosterone limitation clear?
- Should the final paper keep the PMOS coverage audit as a small table or move
  more of it into discussion?
- Are any variable names or clinical interpretations confusing?

## Reproduce

From the repo root:

```bash
Rscript src/stat501_pmos_bmi_report.R
python src/pcos_bmi_analysis.py
cd reports
tectonic pcos_bmi_team_brief.tex
tectonic stat501_pmos_bmi_final.tex
tectonic pmos_public_value_brief.tex
```
