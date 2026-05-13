# Dataset Audit and Follow-up Notes

This note records a useful critique of the first-run analysis and the checks we
ran against the actual Kaggle files used in this repository.

## Are the Two Kaggle Files Different Patients?

No. In the Kaggle version downloaded for this project, the two files appear to
represent the same 541 patients, not different people.

Evidence from row-level audit:

- `PCOS_data_without_infertility.xlsx`, sheet `Full_new`: 541 rows, 45 columns.
- `PCOS_infertility.csv`: 541 rows, 6 columns.
- `Sl. No` is identical row-by-row in both files.
- `PCOS (Y/N)` is identical row-by-row in both files.
- `Patient File No.` in the infertility CSV equals the main workbook's
  `Patient File No.` plus 10000.
- AMH values match row-by-row.
- beta-HCG I values match row-by-row.

So the offset patient IDs are a data artifact. A direct merge on
`Patient File No.` fails because the IDs are `1..541` in the main workbook and
`10001..10541` in the infertility CSV. If the infertility IDs are normalized by
subtracting 10000, the files align row-by-row.

## What the Second Kaggle File Adds

The second Kaggle file does **not** add fasting insulin, testosterone, fasting
glucose, HOMA-IR, RBC, or a broader endocrine panel in this downloaded version.

It only contains:

- `Sl. No`
- `Patient File No.`
- `PCOS (Y/N)`
- `I beta-HCG(mIU/mL)`
- `II beta-HCG(mIU/mL)`
- `AMH(ng/mL)`

Those fields are already present in the main workbook, except for the offset
patient identifier. Therefore, merging the two Kaggle files does not materially
change the BMI regression analysis.

## Implication for the BMI Project

The first-run analysis is not useless. It is a valid exploratory statistical
analysis of BMI among PCOS-positive patients using the available Kaggle
variables. However, it is structurally limited for the specific biological
question of BMI dysregulation in PCOS because the Kaggle dataset lacks key
metabolic/endocrine variables:

- fasting insulin
- fasting glucose
- HOMA-IR
- testosterone / androgen panel

This matters because the first-run model finds self-reported `weight_gain` as
the dominant BMI-related predictor. That result is interpretable, but it is also
likely standing in for metabolic information that the dataset cannot directly
measure.

Recommended language for the report:

> We audited the second Kaggle infertility file and found that it contains the
> same patients with an offset patient identifier, plus duplicate AMH and
> beta-HCG fields. It does not contain fasting insulin or testosterone. Thus,
> fasting insulin, HOMA-IR, and testosterone remain unavailable and should be
> treated as a key limitation of the BMI-focused analysis.

## What the Kaggle Dataset Is Better Suited For

The Prasoon Kottarathil Kaggle PCOS dataset is more naturally suited for
PCOS-vs-non-PCOS classification than for mechanistic BMI regression within the
PCOS-positive subset. Many community notebooks and papers use it that way.

For our course project, keeping the focus on BMI is still acceptable, but the
limitations should be explicit:

- observational data, not causal inference
- PCOS-positive subset is only 177 rows
- key insulin-resistance and androgen variables are missing
- available "laboratory" variables are limited to AMH, LH/FSH, TSH, PRL, vitamin
  D3, PRG, RBS, Hb, and beta-HCG

## Follow-up Dataset Leads

If the team wants a second dataset for a "Run 2" or extension, these Mendeley
datasets are worth checking.

### Mendeley `tw34c7hv7z/1`

Link: https://data.mendeley.com/datasets/tw34c7hv7z/1

Why promising:

- Case-control PCOS study.
- Blood analysis collected on day 3 of menses.
- Description explicitly lists testosterone, prolactin, estradiol, insulin,
  glucose, and lipid profile assays.

This is the most promising lead if we want fasting insulin/glucose and a
possible HOMA-IR extension.

### Mendeley `ny225jgpwf/1`

Link: https://data.mendeley.com/datasets/ny225jgpwf/1

Why promising:

- Description explicitly mentions fasting blood insulin, fasting blood sugar,
  HOMA-IR, BMI, and PCOS/control groups.
- Smaller case-control dataset: 56 PCOS and 62 non-PCOS in the description.
- Also includes BuChE and PON1 enzyme activity, which may be more specialized
  than our current course project needs.

### Mendeley `mh94mxn3nh/1`

Link: https://data.mendeley.com/datasets/mh94mxn3nh/1

Why less suitable:

- Untargeted metabolomic survey in follicular fluid.
- Small sample: 35 PCOS and 37 controls.
- More specialized than needed for a BMI regression course project.

## Recommended Project Framing

Keep the Kaggle analysis as the main course deliverable because it is clean,
reproducible, and already aligned with the course methods:

- descriptive statistics
- simple linear regression
- Welch two-sample t-test
- one-way ANOVA
- multiple linear regression
- adjusted R-squared comparison
- VIF and residual diagnostics

Add a limitation/future-work paragraph:

> The Kaggle dataset is useful for exploratory PCOS classification and clinical
> comparison, but it is limited for BMI mechanism modeling because it lacks
> fasting insulin, fasting glucose, HOMA-IR, and testosterone. A follow-up
> analysis using a Mendeley PCOS dataset with insulin/glucose assays would allow
> us to test whether insulin-resistance markers explain BMI variance beyond
> self-reported weight gain.

## Sources

- Kaggle PCOS dataset:
  https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos
- Public RStudio writeup showing the same 6-column + 45-column Kaggle structure:
  https://rstudio-pubs-static.s3.amazonaws.com/957255_923a5ba8e2ef411591c975f0edb26307.html
- Mendeley PCOS dataset with insulin/glucose/testosterone description:
  https://data.mendeley.com/datasets/tw34c7hv7z/1
- Mendeley PCOS dataset with FINS/FBS/HOMA-IR description:
  https://data.mendeley.com/datasets/ny225jgpwf/1
- Mendeley metabolomics PCOS dataset:
  https://data.mendeley.com/datasets/mh94mxn3nh/1

