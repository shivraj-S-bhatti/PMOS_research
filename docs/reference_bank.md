# Reference Bank for Final Literature Review

Target final writeup: **IEEE style, under 6 pages**.

Working paper angle:

> The Kaggle PCOS dataset supports exploratory clinical/lifestyle BMI modeling,
> but it is structurally limited for metabolic mechanism modeling because it
> lacks fasting insulin, fasting glucose, HOMA-IR, and testosterone. This
> limitation is itself informative: available hormone variables in the common
> Kaggle release add little independent BMI signal, while self-reported weight
> gain dominates. A second insulin/glucose dataset can be used as a replication
> and extension.

## 0. PMOS Name-Change Hook

Current terminology:

- In May 2026, PCOS was renamed **polyendocrine metabolic ovarian syndrome
  (PMOS)** through a global consensus process.
- Use careful wording in the final report: "PMOS, formerly PCOS" for the
  medical framing, and "PCOS" when referring to the historical Kaggle labels or
  original dataset fields.
- The new name is useful for our project because it asks whether older public
  PCOS datasets actually measure the endocrine, metabolic, reproductive,
  dermatological, and psychological domains implied by PMOS.

Verified source links:

- Endocrine Society press release, May 12, 2026:
  https://www.endocrine.org/news-and-advocacy/news-room/2026/pcos-name-change
- Monash University press release, May 13, 2026:
  https://www.monash.edu/medicine/news/latest/2026-articles/polyendocrine-metabolic-ovarian-syndrome-new-name-to-improve-diagnosis-and-care-of-condition-affecting-170-million-women-worldwide
- ABC News explainer, May 12, 2026:
  https://www.abc.net.au/news/health/2026-05-12/polyendocrine-metabolic-ovarian-syndrome-pcos-new-name/106668902
- Contemporary OB/GYN summary, May 12, 2026:
  https://www.contemporaryobgyn.net/view/global-consensus-renames-pcos-to-polyendocrine-metabolic-ovarian-syndrome-pmos-

Claims we can safely use:

- The new name was developed through a global patient/professional consensus
  process and was published in The Lancet.
- PMOS emphasizes endocrine, metabolic, reproductive, skin, weight, and mental
  health impacts.
- Implementation is expected to transition into international guideline updates,
  with the Endocrine Society/Monash materials referring to a 2028 guideline
  implementation horizon.
- Diagnostic criteria are not the center of our paper; our angle is dataset
  measurement coverage.

Claims to avoid or qualify:

- Do not imply the Kaggle dataset is invalid because it uses the older PCOS
  name.
- Do not imply our BMI regression proves or disproves PMOS biology.
- Do not write that every source uses identical wording; some popular coverage
  varies, so cite the Endocrine Society/Monash wording for the final name.

Two-report split:

- STAT 501 report: BMI regression and course methods first, PMOS as framing and
  limitation.
- Public value-add brief: PMOS construct coverage and "what the dataset misses"
  first, BMI/classification results as supporting evidence.

## 1. Dataset Structure and Kaggle Audit

### Kaggle Dataset

Source:

- https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos

Actual downloaded files:

- `PCOS_data_without_infertility.xlsx`: 541 rows, 45 columns.
- `PCOS_infertility.csv`: 541 rows, 6 columns.

Audit conclusion:

- These are the same 541 patients, not independent cohorts.
- `Sl. No` and `PCOS (Y/N)` match row-by-row.
- Infertility CSV patient ID equals main workbook patient ID + 10000.
- AMH and beta-HCG mostly duplicate fields already in the main workbook.
- Fasting insulin, testosterone, fasting glucose, and HOMA-IR are not present.

Community-notebook note:

- A Kaggle notebook by Karnika Kapoor, "PCOS Diagnosis", reportedly describes
  preprocessing as merging two files sorted into patients with and without
  infertility.
- Link: https://www.kaggle.com/code/karnikakapoor/pcos-diagnosis
- Important caveat: Kaggle notebooks are not author documentation. Use this as
  supporting community context, not as ground truth. Our row-level audit is
  stronger evidence.

How to cite/use:

- Cite Kaggle as data source.
- Mention community notebooks only if discussing common preprocessing practice.
- In methods, state that we audited both files and normalized the offset ID.

## 2. Main Project Premise Options

### Option A: Stay on Kaggle, Pivot the Question

Question:

> What predicts PCOS status using only low-cost/non-invasive clinical and
> self-reportable variables?

Why this is attractive:

- The Kaggle dataset is more naturally suited for PCOS classification.
- Excluding ultrasound and hormonal features creates a real low-resource
  screening question.
- Methods could include logistic regression, train/test validation, ROC/AUC,
  calibration, and comparison to regularized models.

Risk:

- This drifts away from the original BMI outcome.
- More ML/classification-heavy than the original course proposal.

### Option B: Keep BMI, Add a Second Dataset

Question:

> Does an insulin/glucose dataset show that HOMA-IR or insulin resistance
> explains BMI variance beyond self-reported weight gain?

Why this is stronger:

- The Kaggle run becomes "Run 1: available clinical/lifestyle variables."
- A Mendeley dataset becomes "Run 2: metabolic extension with insulin/glucose."
- The limitation becomes part of the argument rather than a weakness.

Risk:

- Requires another data-access and cleaning pass.
- Need to keep final paper concise and not overbuild.

Recommended path for final project:

- Keep Kaggle analysis as main course deliverable.
- Add a short Run 2 only if Mendeley data downloads cleanly and has usable BMI,
  insulin, glucose, and PCOS status.
- Otherwise, include Mendeley as future work.

## 3. Literature Survey Structure

### Generation 1: Kaggle Classification Work

Core idea:

- Most published/community work uses the Kaggle dataset for PCOS vs non-PCOS
  classification.
- Common models: Random Forest, SVM, gradient boosting, logistic regression,
  explainable AI/feature importance.
- Reported accuracies are often high because variables like follicle counts,
  cycle irregularity, AMH, and symptoms are close to diagnostic criteria.

Useful source leads:

- Kaggle notebook: https://www.kaggle.com/code/karnikakapoor/pcos-diagnosis
- "Polycystic Ovary Syndrome Detection Machine Learning Model Based on
  Optimized Feature Selection and Explainable Artificial Intelligence",
  Diagnostics, 2023. PMID: 37189606; PMCID: PMC10137609.
- PCOS classification/electronic health record modeling preprint:
  https://pubmed.ncbi.nlm.nih.gov/37577593/
- Expert Systems with Applications PCOS ML paper lead:
  https://dl.acm.org/doi/10.1016/j.eswa.2022.117592

How it supports our project:

- Shows the Kaggle dataset is legitimate for classification.
- Also shows why classification is easier than BMI regression: many predictors
  overlap with diagnostic criteria.

### Generation 2: Metabolic Subtyping and Phenotype Heterogeneity

Core idea:

- PCOS is not metabolically uniform.
- BMI, insulin resistance, glucose metabolism, AMH, and androgen features vary
  across phenotypes and subtypes.
- This explains why a single BMI regression over all PCOS-positive Kaggle rows
  can show weak hormone signal.

Useful source leads:

- PCOS phenotype/metabolic heterogeneity source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9832677/
- PCOS insulin-resistance prevalence source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC11229724/
- Insulin-mediated substrate use and role of androgens:
  https://pubmed.ncbi.nlm.nih.gov/34050757/

How it supports our project:

- Helps frame BMI as phenotype-conditional.
- Justifies subgroup/sensitivity analysis.
- Explains why aggregate regression may underperform.

### Generation 3: Causal / Mendelian Randomization Work

Core idea:

- Newer work uses Mendelian Randomization and GWAS summary statistics to reason
  about causal pathways.
- These studies are outside the scope of our course project but useful for
  framing mechanisms: insulin resistance and androgen excess are central.

Useful source leads:

- PubMed lead on body-fat distribution, fasting insulin, testosterone, and PCOS:
  https://pubmed.ncbi.nlm.nih.gov/41031338/
- 2023 international evidence-based PCOS guideline:
  https://pubmed.ncbi.nlm.nih.gov/37580861/
- Guideline technical report / Monash page:
  https://research.monash.edu/en/publications/international-evidence-based-guideline-for-the-assessment-and-man/
- Guideline summary emphasizing AMH and metabolic risk:
  https://academic.oup.com/jcem/article/108/10/2447/7242360

How it supports our project:

- We should avoid causal language.
- Regression on observational data estimates association, not mechanism.
- The missing insulin/testosterone variables are scientifically important.

## 4. What the Literature Agrees On

Working claims to verify/cite in final review:

- PCOS has heterogeneous reproductive, metabolic, and psychological features.
- Insulin resistance is common in PCOS and can occur even in lean patients.
- BMI alone does not reliably detect insulin resistance.
- AMH is increasingly used as an adult diagnostic alternative to ultrasound,
  but it is not the same as insulin-resistance measurement.
- Clinical insulin assays are not always emphasized in routine PCOS diagnosis,
  which partly explains why many clinical datasets omit fasting insulin.
- Observational regression cannot establish causality.

## 5. Gap / Contribution We Can Claim

Conservative contribution:

> We show that, in a commonly used Kaggle PCOS dataset, the available laboratory
> variables add little independent explanatory power for BMI within the
> PCOS-positive subset, while self-reported weight gain dominates. This suggests
> that the public Kaggle release is more suitable for PCOS classification than
> for metabolic BMI mechanism modeling, unless supplemented by a dataset with
> insulin/glucose/androgen measures.

What not to overclaim:

- Do not say insulin causes BMI changes from this dataset.
- Do not say hormones do not matter in PCOS generally.
- Do not say Kaggle is useless.
- Do not call `weight_gain` a validated insulin-resistance proxy; call it a
  crude clinical/self-report signal.

## 6. Candidate Mendeley Run 2 Sources

### `tw34c7hv7z/1`

Link:

- https://data.mendeley.com/datasets/tw34c7hv7z/1

Why useful:

- Case-control PCOS study.
- Blood samples collected on day 3 of menses.
- Description lists testosterone, prolactin, estradiol, insulin, glucose, and
  lipid profile assays.

Potential Run 2:

- Compute HOMA-IR if fasting insulin and glucose are available.
- Regress BMI on HOMA-IR, testosterone, AMH, and clinical covariates.
- Test whether metabolic markers outperform self-reported weight gain if such a
  variable exists.

### `ny225jgpwf/1`

Link:

- https://data.mendeley.com/datasets/ny225jgpwf/1

Why useful:

- Description lists fasting blood insulin (FINS), fasting blood sugar (FBS),
  HOMA-IR, BMI, and PCOS/control groups.
- Smaller case-control dataset: 56 PCOS and 62 controls.

Potential Run 2:

- Good for a small replication/extension.
- More specialized because it includes BuChE and PON1 enzyme activity.

### `mh94mxn3nh/1`

Link:

- https://data.mendeley.com/datasets/mh94mxn3nh/1

Why less suitable:

- Follicular-fluid metabolomics.
- Small sample.
- Better for biomarker discovery than a course-level BMI regression project.

## 7. Six-Page IEEE Literature Review Skeleton

Keep final review tight:

1. **Introduction and Motivation**: PCOS heterogeneity, BMI/metabolic risk, why
   insulin/testosterone matter.
2. **Dataset Context**: Kaggle dataset structure, two-file audit, classification
   suitability vs BMI limitations.
3. **Prior Modeling Work**: Kaggle classification generation, metabolic
   phenotype studies, causal/MR framing.
4. **Our Statistical Framing**: BMI regression, model blocks, diagnostics, why
   this is exploratory.
5. **Gap and Proposed Extension**: missing insulin/HOMA-IR/testosterone; Mendeley
   Run 2 if feasible.
6. **Conclusion**: Kaggle is useful but limited; our project clarifies what the
   available variables can and cannot answer.

Suggested figure/table budget:

- 1 small table: source matrix.
- 1 small table: variables present/missing by dataset.
- No more than 1 figure unless required.
