# Clinical and Hormonal Predictors of BMI in PCOS

This repository contains a first-run statistical analysis for the project:

**Clinical and Hormonal Predictors of BMI in Women with Polycystic Ovary Syndrome (PCOS)**.

The analysis uses the public Kaggle PCOS dataset and focuses on BMI among
PCOS-positive participants. It includes descriptive statistics, simple linear
regression, Welch two-sample t-tests, one-way ANOVA, multiple regression,
adjusted R-squared model comparisons, VIF checks, residual diagnostics,
BMI subgroup checks, interaction models, and sensitivity checks.

## Repository Layout

- `src/pcos_bmi_analysis.py` - reproducible analysis script
- `reports/pcos_bmi_first_run_report.md` - concise generated analysis report
- `reports/pcos_bmi_team_brief.tex` - two-column LaTeX team brief
- `reports/pcos_bmi_team_brief.pdf` - compiled team brief
- `figures/` - generated analysis plots
- `results/` - generated CSV result tables
- `data/README.md` - data source notes
- `docs/reference_bank.md` - literature leads, project framing, and final
  IEEE-style paper outline
- `docs/dataset_audit_and_followup.md` - audit of the two Kaggle files and
  follow-up dataset leads
- `docs/team_review_plan.md` - teammate review checklist and next experiments
- `docs/stats_learning_cheatsheet.md` - compact personal STAT 501 method picker

## Data Source

Kaggle dataset:

https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos

Raw data is not committed. The script downloads the workbook through
`kagglehub` and caches it locally under `data/raw/`.

## Reproduce the Analysis

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/pcos_bmi_analysis.py
```

To compile the LaTeX brief:

```bash
cd reports
tectonic pcos_bmi_team_brief.tex
```

## First-Run Notes

- The downloaded Kaggle workbook contains 541 records.
- The main BMI analysis is restricted to 177 PCOS-positive participants.
- Fasting insulin and testosterone were mentioned in the original proposal but
  are not present in this workbook, so the first run uses available clinical,
  hormonal, lifestyle, and ultrasound variables.
- The second Kaggle infertility CSV was audited. It appears to contain the same
  541 patients with patient file numbers offset by 10000 and duplicate
  AMH/beta-HCG fields; it does not add insulin or testosterone.
- Results are exploratory and should not be interpreted as causal or clinical
  proof.
