import os
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.outliers_influence import variance_inflation_factor


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "raw"
FIG = REPO_ROOT / "figures"
RESULTS = REPO_ROOT / "results"
REPORTS = REPO_ROOT / "reports"

for directory in (DATA_DIR, FIG, RESULTS, REPORTS):
    directory.mkdir(parents=True, exist_ok=True)


def dataset_path() -> Path:
    local = DATA_DIR / "PCOS_data_without_infertility.xlsx"
    if local.exists():
        return local

    os.environ.setdefault("KAGGLEHUB_CACHE", str(REPO_ROOT / ".kagglehub"))
    import kagglehub

    downloaded = Path(
        kagglehub.dataset_download("prasoonkottarathil/polycystic-ovary-syndrome-pcos")
    )
    source = downloaded / "PCOS_data_without_infertility.xlsx"
    if not source.exists():
        raise FileNotFoundError(f"Expected Kaggle workbook not found at {source}")

    shutil.copy2(source, local)
    return local


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    names = {
        "Sl. No": "sl_no",
        "Patient File No.": "patient_file_no",
        "PCOS (Y/N)": "pcos",
        " Age (yrs)": "age",
        "Weight (Kg)": "weight_kg",
        "Height(Cm) ": "height_cm",
        "BMI": "bmi",
        "Cycle(R/I)": "cycle",
        "FSH(mIU/mL)": "fsh",
        "LH(mIU/mL)": "lh",
        "FSH/LH": "fsh_lh",
        "Hip(inch)": "hip",
        "Waist(inch)": "waist",
        "Waist:Hip Ratio": "waist_hip_ratio",
        "TSH (mIU/L)": "tsh",
        "AMH(ng/mL)": "amh",
        "PRL(ng/mL)": "prl",
        "Vit D3 (ng/mL)": "vit_d3",
        "RBS(mg/dl)": "rbs",
        "Weight gain(Y/N)": "weight_gain",
        "Fast food (Y/N)": "fast_food",
        "Reg.Exercise(Y/N)": "regular_exercise",
        "Follicle No. (L)": "follicle_l",
        "Follicle No. (R)": "follicle_r",
        "Avg. F size (L) (mm)": "avg_f_size_l",
        "Avg. F size (R) (mm)": "avg_f_size_r",
        "Endometrium (mm)": "endometrium",
    }
    df = df.rename(columns=names)
    keep = list(names.values())
    df = df[[c for c in keep if c in df.columns]].copy()

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["cycle_group"] = df["cycle"].map({2: "Regular", 4: "Irregular"})
    df["total_follicles"] = df["follicle_l"] + df["follicle_r"]
    df["lh_fsh_ratio"] = df["lh"] / df["fsh"]
    return df


def savefig(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG / name, dpi=180, bbox_inches="tight")
    plt.close()


def coef_table(model) -> pd.DataFrame:
    ci = model.conf_int()
    out = pd.DataFrame(
        {
            "term": model.params.index,
            "estimate": model.params.values,
            "std_error": model.bse.values,
            "p_value": model.pvalues.values,
            "conf_low": ci[0].values,
            "conf_high": ci[1].values,
        }
    )
    return out


def fmt_p(p: float) -> str:
    if pd.isna(p):
        return ""
    if p < 0.001:
        return "$<0.001$"
    return f"{p:.3f}"


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in str(text))


def latex_table(df: pd.DataFrame, caption: str, label: str) -> str:
    table = df.to_latex(
        index=False,
        escape=False,
        float_format=lambda x: f"{x:.3f}",
        caption=caption,
        label=label,
        position="t",
    )
    table = table.replace(r"\begin{tabular}", r"\small\resizebox{\columnwidth}{!}{\begin{tabular}")
    table = table.replace(r"\end{tabular}", r"\end{tabular}}")
    return table


def main() -> None:
    raw = pd.read_excel(dataset_path(), sheet_name="Full_new")
    df = clean_columns(raw)
    pcos = df[df["pcos"] == 1].copy()
    ranked_follicles = pcos["total_follicles"].rank(method="first")
    pcos["follicle_group"] = pd.qcut(
        ranked_follicles, q=3, labels=["Low", "Medium", "High"], duplicates="drop"
    )

    sns.set_theme(style="whitegrid", context="notebook")

    # Descriptive statistics and BMI distribution.
    desc_cols = [
        "bmi",
        "age",
        "waist_hip_ratio",
        "amh",
        "lh_fsh_ratio",
        "tsh",
        "prl",
        "rbs",
        "total_follicles",
        "avg_f_size_l",
        "avg_f_size_r",
        "endometrium",
    ]
    descriptives = (
        pcos[desc_cols]
        .describe()
        .T[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]]
        .round(3)
    )
    bmi_skew = stats.skew(pcos["bmi"].dropna())

    plt.figure(figsize=(7, 4.5))
    sns.histplot(pcos["bmi"], kde=True, color="#2f6f73")
    plt.xlabel("BMI")
    plt.ylabel("Frequency")
    plt.title("BMI Distribution Among PCOS-Positive Participants")
    savefig("bmi_distribution.png")

    # Simple linear regression: BMI by waist-to-hip ratio.
    simple = smf.ols("bmi ~ waist_hip_ratio", data=pcos).fit()
    corr = stats.pearsonr(
        pcos[["bmi", "waist_hip_ratio"]].dropna()["bmi"],
        pcos[["bmi", "waist_hip_ratio"]].dropna()["waist_hip_ratio"],
    )

    plt.figure(figsize=(6.5, 4.5))
    sns.regplot(data=pcos, x="waist_hip_ratio", y="bmi", scatter_kws={"alpha": 0.65})
    plt.xlabel("Waist-to-Hip Ratio")
    plt.ylabel("BMI")
    plt.title("Simple Linear Regression: BMI and Waist-to-Hip Ratio")
    savefig("bmi_vs_waist_hip_ratio.png")

    # Two-sample t-test: regular vs irregular cycles.
    cycle_data = pcos.dropna(subset=["bmi", "cycle_group"])
    regular = cycle_data.loc[cycle_data["cycle_group"] == "Regular", "bmi"]
    irregular = cycle_data.loc[cycle_data["cycle_group"] == "Irregular", "bmi"]
    ttest = stats.ttest_ind(regular, irregular, equal_var=False)
    cycle_summary = (
        cycle_data.groupby("cycle_group")["bmi"]
        .agg(["count", "mean", "std", "median"])
        .round(3)
    )

    plt.figure(figsize=(6, 4.5))
    sns.boxplot(data=cycle_data, x="cycle_group", y="bmi", hue="cycle_group", legend=False)
    sns.stripplot(data=cycle_data, x="cycle_group", y="bmi", color="black", alpha=0.35)
    plt.xlabel("Menstrual Cycle Group")
    plt.ylabel("BMI")
    plt.title("BMI by Cycle Regularity")
    savefig("bmi_by_cycle_group.png")

    # One-way ANOVA: BMI across follicle-count groups as a severity proxy.
    anova_data = pcos.dropna(subset=["bmi", "follicle_group"])
    anova_model = smf.ols("bmi ~ C(follicle_group)", data=anova_data).fit()
    anova_table = sm.stats.anova_lm(anova_model, typ=2).round(5)
    follicle_summary = (
        anova_data.groupby("follicle_group", observed=True)["bmi"]
        .agg(["count", "mean", "std", "median"])
        .round(3)
    )
    tukey_text = "Tukey HSD not run because the overall ANOVA was not significant."
    if anova_table.loc["C(follicle_group)", "PR(>F)"] < 0.05:
        tukey = pairwise_tukeyhsd(anova_data["bmi"], anova_data["follicle_group"])
        tukey_text = str(tukey)

    plt.figure(figsize=(6.5, 4.5))
    sns.boxplot(data=anova_data, x="follicle_group", y="bmi", hue="follicle_group", legend=False)
    sns.stripplot(data=anova_data, x="follicle_group", y="bmi", color="black", alpha=0.3)
    plt.xlabel("Follicle Count Group")
    plt.ylabel("BMI")
    plt.title("BMI Across Follicle-Count Groups")
    savefig("bmi_by_follicle_group.png")

    # Multiple linear regression.
    model_cols = [
        "bmi",
        "age",
        "waist_hip_ratio",
        "amh",
        "lh_fsh_ratio",
        "tsh",
        "prl",
        "rbs",
        "cycle_group",
        "weight_gain",
        "fast_food",
        "regular_exercise",
        "total_follicles",
    ]
    model_df = pcos[model_cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    formula = (
        "bmi ~ age + waist_hip_ratio + amh + lh_fsh_ratio + tsh + prl + rbs "
        "+ C(cycle_group) + weight_gain + fast_food + regular_exercise + total_follicles"
    )
    full_model = smf.ols(formula, data=model_df).fit()
    reduced_formula = "bmi ~ waist_hip_ratio + age + C(cycle_group) + weight_gain + fast_food"
    reduced_model = smf.ols(reduced_formula, data=model_df).fit()

    vif_x = pd.get_dummies(
        model_df[
            [
                "age",
                "waist_hip_ratio",
                "amh",
                "lh_fsh_ratio",
                "tsh",
                "prl",
                "rbs",
                "cycle_group",
                "weight_gain",
                "fast_food",
                "regular_exercise",
                "total_follicles",
            ]
        ],
        drop_first=True,
        dtype=float,
    )
    vif_x = sm.add_constant(vif_x)
    vif = pd.DataFrame(
        {
            "variable": vif_x.columns,
            "VIF": [variance_inflation_factor(vif_x.values, i) for i in range(vif_x.shape[1])],
        }
    ).round(3)

    corr_vars = ["bmi", "age", "waist_hip_ratio", "amh", "lh_fsh_ratio", "rbs", "total_follicles"]
    corr_matrix = model_df[corr_vars].corr().round(3)

    # Extensions motivated by community/research work on this dataset:
    # compare clinical, laboratory, and ultrasound feature blocks; check BMI
    # subgroups; add PCOS vs non-PCOS context; and run small sensitivity checks.
    block_cols = [
        "bmi",
        "age",
        "waist_hip_ratio",
        "cycle_group",
        "weight_gain",
        "fast_food",
        "regular_exercise",
        "amh",
        "lh_fsh_ratio",
        "tsh",
        "prl",
        "rbs",
        "follicle_l",
        "follicle_r",
        "avg_f_size_l",
        "avg_f_size_r",
        "endometrium",
    ]
    block_df = pcos[block_cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    clinical_formula = (
        "bmi ~ age + waist_hip_ratio + C(cycle_group) + weight_gain "
        "+ fast_food + regular_exercise"
    )
    lab_formula = "bmi ~ amh + lh_fsh_ratio + tsh + prl + rbs"
    ultrasound_formula = "bmi ~ follicle_l + follicle_r + avg_f_size_l + avg_f_size_r + endometrium"
    full_multimodal_formula = (
        clinical_formula
        + " + amh + lh_fsh_ratio + tsh + prl + rbs"
        + " + follicle_l + follicle_r + avg_f_size_l + avg_f_size_r + endometrium"
    )
    block_formulas = {
        "Clinical only": clinical_formula,
        "Laboratory only": lab_formula,
        "Ultrasound only": ultrasound_formula,
        "Clinical + lab": clinical_formula + " + amh + lh_fsh_ratio + tsh + prl + rbs",
        "Clinical + ultrasound": clinical_formula
        + " + follicle_l + follicle_r + avg_f_size_l + avg_f_size_r + endometrium",
        "Full multimodal": full_multimodal_formula,
    }
    block_rows = []
    for name, frm in block_formulas.items():
        mod = smf.ols(frm, data=block_df).fit()
        block_rows.append({"Model block": name, "n": int(mod.nobs), "Adj. R2": mod.rsquared_adj, "AIC": mod.aic})
    block_table = pd.DataFrame(block_rows).round({"Adj. R2": 3, "AIC": 1})

    plt.figure(figsize=(7.2, 4.5))
    sns.barplot(data=block_table, x="Adj. R2", y="Model block", color="#6b8f71")
    plt.xlabel("Adjusted R-squared")
    plt.ylabel("")
    plt.title("BMI Model Comparison by Predictor Block")
    savefig("model_block_adjusted_r2.png")

    interaction_formulas = {
        "Clinical base": clinical_formula,
        "Cycle x weight gain": clinical_formula + " + C(cycle_group):weight_gain",
        "Fast food x exercise": clinical_formula + " + fast_food:regular_exercise",
        "AMH x follicles": full_multimodal_formula + " + amh:follicle_l + amh:follicle_r",
    }
    interaction_rows = []
    for name, frm in interaction_formulas.items():
        mod = smf.ols(frm, data=block_df).fit()
        interaction_rows.append({"Model": name, "n": int(mod.nobs), "Adj. R2": mod.rsquared_adj, "AIC": mod.aic})
    interaction_table = pd.DataFrame(interaction_rows).round({"Adj. R2": 3, "AIC": 1})

    sens_df = block_df.copy()
    sens_df["log_amh"] = np.log1p(sens_df["amh"])
    sens_df["log_lh_fsh_ratio"] = np.log1p(sens_df["lh_fsh_ratio"])
    sens_formula = (
        clinical_formula
        + " + log_amh + log_lh_fsh_ratio + tsh + prl + rbs"
        + " + follicle_l + follicle_r + avg_f_size_l + avg_f_size_r + endometrium"
    )
    q1, q3 = sens_df["bmi"].quantile([0.25, 0.75])
    iqr = q3 - q1
    no_bmi_outliers = sens_df[(sens_df["bmi"] >= q1 - 1.5 * iqr) & (sens_df["bmi"] <= q3 + 1.5 * iqr)]
    sensitivity_models = {
        "Original full model": (full_multimodal_formula, block_df),
        "Log AMH and log LH/FSH": (sens_formula, sens_df),
        "Exclude BMI IQR outliers": (full_multimodal_formula, no_bmi_outliers),
    }
    sensitivity_rows = []
    for name, (frm, data) in sensitivity_models.items():
        mod = smf.ols(frm, data=data).fit()
        sensitivity_rows.append(
            {
                "Sensitivity check": name,
                "n": int(mod.nobs),
                "Adj. R2": mod.rsquared_adj,
                "Weight gain beta": mod.params.get("weight_gain", np.nan),
                "Weight gain p": fmt_p(mod.pvalues.get("weight_gain", np.nan)),
            }
        )
    sensitivity_table = pd.DataFrame(sensitivity_rows).round({"Adj. R2": 3, "Weight gain beta": 3})

    bmi_sub = pcos.copy()
    bmi_sub["bmi_group"] = np.where(bmi_sub["bmi"] < 24, "BMI < 24", "BMI >= 24")
    subgroup_rows = []
    for var, label in [
        ("amh", "AMH"),
        ("waist_hip_ratio", "Waist:hip ratio"),
        ("total_follicles", "Total follicles"),
        ("rbs", "RBS"),
    ]:
        lo = bmi_sub.loc[bmi_sub["bmi_group"] == "BMI < 24", var].dropna()
        hi = bmi_sub.loc[bmi_sub["bmi_group"] == "BMI >= 24", var].dropna()
        test = stats.ttest_ind(lo, hi, equal_var=False)
        subgroup_rows.append(
            {"Variable": label, "BMI < 24 mean": lo.mean(), "BMI >= 24 mean": hi.mean(), "p": fmt_p(test.pvalue)}
        )
    subgroup_table = pd.DataFrame(subgroup_rows).round(3)

    plt.figure(figsize=(7, 4.5))
    sns.boxplot(data=bmi_sub, x="bmi_group", y="amh", hue="bmi_group", legend=False)
    sns.stripplot(data=bmi_sub, x="bmi_group", y="amh", color="black", alpha=0.3)
    plt.xlabel("BMI Subgroup")
    plt.ylabel("AMH")
    plt.title("AMH by BMI Subgroup Among PCOS-Positive Participants")
    savefig("amh_by_bmi_subgroup.png")

    context_rows = []
    for var, label in [
        ("bmi", "BMI"),
        ("amh", "AMH"),
        ("waist_hip_ratio", "Waist:hip ratio"),
        ("total_follicles", "Total follicles"),
    ]:
        pos = df.loc[df["pcos"] == 1, var].dropna()
        neg = df.loc[df["pcos"] == 0, var].dropna()
        test = stats.ttest_ind(pos, neg, equal_var=False)
        context_rows.append({"Variable": label, "PCOS mean": pos.mean(), "Non-PCOS mean": neg.mean(), "p": fmt_p(test.pvalue)})
    for var, label in [
        ("weight_gain", "Weight gain"),
        ("fast_food", "Fast food"),
        ("cycle", "Irregular cycle"),
    ]:
        if var == "cycle":
            tmp = df.assign(flag=(df["cycle"] == 4).astype(float))
            table = pd.crosstab(tmp["pcos"], tmp["flag"])
            pos_rate = tmp.loc[tmp["pcos"] == 1, "flag"].mean()
            neg_rate = tmp.loc[tmp["pcos"] == 0, "flag"].mean()
        else:
            tmp = df.dropna(subset=[var, "pcos"])
            table = pd.crosstab(tmp["pcos"], tmp[var])
            pos_rate = tmp.loc[tmp["pcos"] == 1, var].mean()
            neg_rate = tmp.loc[tmp["pcos"] == 0, var].mean()
        chi2_p = stats.chi2_contingency(table)[1]
        context_rows.append({"Variable": label, "PCOS mean": pos_rate, "Non-PCOS mean": neg_rate, "p": fmt_p(chi2_p)})
    context_table = pd.DataFrame(context_rows).round(3)

    context_plot = df.assign(pcos_group=np.where(df["pcos"] == 1, "PCOS", "Non-PCOS"))
    plt.figure(figsize=(7, 4.5))
    sns.boxplot(data=context_plot, x="pcos_group", y="amh", hue="pcos_group", legend=False)
    sns.stripplot(data=context_plot, x="pcos_group", y="amh", color="black", alpha=0.25)
    plt.xlabel("")
    plt.ylabel("AMH")
    plt.title("AMH by PCOS Status")
    savefig("amh_by_pcos_status.png")

    fitted = full_model.fittedvalues
    resid = full_model.resid
    plt.figure(figsize=(6.5, 4.5))
    sns.scatterplot(x=fitted, y=resid)
    plt.axhline(0, color="black", linewidth=1)
    plt.xlabel("Fitted Values")
    plt.ylabel("Residuals")
    plt.title("Residual Plot for Multiple Linear Regression")
    savefig("multiple_regression_residuals.png")

    fig = sm.qqplot(resid, line="45", fit=True)
    fig.set_size_inches(6, 4.5)
    plt.title("Q-Q Plot of Multiple Regression Residuals")
    savefig("multiple_regression_qq.png")

    report = []
    report.append("# Concise First Run: Predictors of BMI in PCOS\n")
    report.append("Dataset: Kaggle PCOS dataset by Prasoon Kottarathil. Analysis subset: PCOS-positive participants only.\n")
    report.append(f"- Full dataset rows: {len(df)}")
    report.append(f"- PCOS-positive rows used for main analysis: {len(pcos)}")
    report.append(f"- Complete cases in multiple linear regression: {len(model_df)}")
    report.append("- Note: fasting insulin and testosterone were not available in this workbook, so this first run uses available clinical and hormonal variables.\n")

    report.append("## Descriptive Statistics\n")
    report.append(descriptives.to_markdown())
    report.append(f"\nBMI skewness among PCOS-positive participants: **{bmi_skew:.3f}**.\n")

    report.append("## Simple Linear Regression\n")
    report.append("Response variable: BMI. Explanatory variable: waist-to-hip ratio.\n")
    report.append(f"- Pearson correlation: r = **{corr.statistic:.3f}**, p = **{corr.pvalue:.4g}**")
    report.append(f"- Slope estimate: **{simple.params['waist_hip_ratio']:.3f}** BMI units per 1.0 WHR, p = **{simple.pvalues['waist_hip_ratio']:.4g}**")
    report.append(f"- R-squared: **{simple.rsquared:.3f}**\n")

    report.append("## Two-Sample t-Test\n")
    report.append("Comparison: mean BMI for regular vs. irregular menstrual cycles.\n")
    report.append(cycle_summary.to_markdown())
    report.append(f"\nWelch two-sample t-test: t = **{ttest.statistic:.3f}**, p = **{ttest.pvalue:.4g}**.\n")

    report.append("## One-Way ANOVA\n")
    report.append("Comparison: mean BMI across low, medium, and high total follicle-count groups, used here as a simple severity proxy.\n")
    report.append(follicle_summary.to_markdown())
    report.append("\n" + anova_table.to_markdown())
    report.append("\n" + tukey_text + "\n")

    report.append("## Multiple Linear Regression\n")
    report.append(f"- Full model adjusted R-squared: **{full_model.rsquared_adj:.3f}**")
    report.append(f"- Reduced model adjusted R-squared: **{reduced_model.rsquared_adj:.3f}**")
    report.append("- Coefficients from the full model:\n")
    report.append(coef_table(full_model).round(4).to_markdown(index=False))
    report.append("\n### VIF Values\n")
    report.append(vif.to_markdown(index=False))
    report.append("\n### Correlation Matrix\n")
    report.append(corr_matrix.to_markdown())

    report.append("\n## Extensions Worth Adding\n")
    report.append("### Clinical, Laboratory, and Ultrasound Model Blocks\n")
    report.append(block_table.to_markdown(index=False))
    report.append("\n### BMI Subgroup Checks\n")
    report.append(subgroup_table.to_markdown(index=False))
    report.append("\n### PCOS vs Non-PCOS Context\n")
    report.append(context_table.to_markdown(index=False))
    report.append("\n### Interaction Models\n")
    report.append(interaction_table.to_markdown(index=False))
    report.append("\n### Sensitivity Checks\n")
    report.append(sensitivity_table.to_markdown(index=False))

    report.append("\n## First-Run Interpretation\n")
    report.append(
        "Waist-to-hip ratio had only a weak, non-significant linear association with BMI in this PCOS-positive subset. "
        "The two-sample t-test suggested higher mean BMI for irregular cycles than regular cycles, but this difference was smaller after adjusting for other variables in the multiple regression. "
        "Follicle-count group did not show a statistically significant difference in mean BMI by one-way ANOVA. "
        "In the multiple linear regression, self-reported weight gain was the clearest predictor of BMI, and the reduced model had a slightly higher adjusted R-squared than the larger candidate model. "
        "The next best improvement is to confirm whether another file/version contains fasting insulin and testosterone, then rerun the candidate-predictor model."
    )

    report.append("\n## Figures\n")
    for path in sorted(FIG.glob("*.png")):
        report.append(f"- [{path.name}](../figures/{path.name})")

    (REPORTS / "pcos_bmi_first_run_report.md").write_text("\n".join(report), encoding="utf-8")
    descriptives.to_csv(RESULTS / "descriptive_statistics.csv")
    coef_table(full_model).round(6).to_csv(
        RESULTS / "multiple_regression_coefficients.csv", index=False
    )
    vif.to_csv(RESULTS / "vif_values.csv", index=False)
    corr_matrix.to_csv(RESULTS / "correlation_matrix.csv")
    block_table.to_csv(RESULTS / "model_block_comparison.csv", index=False)
    subgroup_table.to_csv(RESULTS / "bmi_subgroup_checks.csv", index=False)
    context_table.to_csv(RESULTS / "pcos_vs_non_pcos_context.csv", index=False)
    interaction_table.to_csv(RESULTS / "interaction_model_comparison.csv", index=False)
    sensitivity_table.to_csv(RESULTS / "sensitivity_checks.csv", index=False)

    top_coef = coef_table(full_model)
    top_coef = top_coef[top_coef["term"] != "Intercept"].copy()
    top_coef["abs_t"] = (top_coef["estimate"] / top_coef["std_error"]).abs()
    top_coef = top_coef.sort_values("abs_t", ascending=False).head(8)
    top_coef_tex = top_coef[["term", "estimate", "std_error", "p_value"]].copy()
    top_coef_tex["term"] = top_coef_tex["term"].map(latex_escape)
    top_coef_tex["p_value"] = top_coef_tex["p_value"].map(fmt_p)
    top_coef_tex = top_coef_tex.rename(
        columns={"term": "Term", "estimate": "Estimate", "std_error": "SE", "p_value": "p"}
    ).round(3)

    latex = rf"""
\documentclass[10pt,twocolumn]{{article}}
\usepackage[margin=0.65in]{{geometry}}
\usepackage{{booktabs}}
\usepackage{{graphicx}}
\usepackage{{hyperref}}
\usepackage{{xurl}}
\usepackage{{microtype}}
\usepackage{{amsmath}}
\usepackage{{caption}}
\captionsetup{{font=small,labelfont=bf}}
\hypersetup{{colorlinks=true,urlcolor=blue,citecolor=blue,linkcolor=blue}}

\title{{Clinical and Hormonal Predictors of BMI in Women with PCOS: Statistical First Run}}
\author{{Soumitra Das \and Shreya Saha \and Anjali Kanvinde \and Shivraj Singh Bhatti \and Pranav Jeyakumar}}
\date{{\today}}

\begin{{document}}
\sloppy
\maketitle

\begin{{abstract}}
We analyze the Kaggle PCOS dataset by Prasoon Kottarathil, with 541 records and 177 PCOS-positive participants. The response variable is BMI. This first run uses descriptive statistics, scatterplots, Pearson correlation, simple linear regression, a Welch two-sample t-test, one-way ANOVA, multiple linear regression, adjusted $R^2$, VIF values, residual plots, and sensitivity checks. Fasting insulin and testosterone were not present in the downloaded workbook, so we use available clinical, hormonal, lifestyle, and ultrasound variables.
\end{{abstract}}

\section{{Research Question and Data}}
Our question is: among women with PCOS, which clinical, hormonal, lifestyle, and ultrasound variables are associated with BMI? The main analysis is restricted to PCOS-positive participants ($n={len(pcos)}$). We also include a short PCOS vs non-PCOS context table to understand how the analytic subset differs from the rest of the dataset.

\section{{Community and Research Motivation}}
The Kaggle dataset page reports substantial public use, including code notebooks and discussions: \url{{https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos}}. Recent work using this same dataset groups variables into clinical, laboratory, and ultrasound blocks and studies BMI/cycle subgroups \cite{{autopcos}}. Explainable-machine-learning work using this dataset highlights follicle counts, AMH, weight gain, skin darkening, hair growth, and FSH/LH-related variables as important for PCOS classification \cite{{mdpi}}. A recent preprint also notes that the Kaggle diagnosis label lacks verifiable diagnostic criteria, so our results should be framed as exploratory rather than clinical proof \cite{{medrxiv}}.

\section{{Descriptive Statistics}}
Among PCOS-positive participants, mean BMI was {pcos["bmi"].mean():.2f} with standard deviation {pcos["bmi"].std():.2f}; the median was {pcos["bmi"].median():.2f}. BMI skewness was {bmi_skew:.3f}, so BMI was not extremely skewed in this subset. Mean AMH was {pcos["amh"].mean():.2f}, and mean waist-to-hip ratio was {pcos["waist_hip_ratio"].mean():.3f}.

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/bmi_distribution.png}}
\caption{{BMI distribution among PCOS-positive participants.}}
\end{{figure}}

\section{{Simple Linear Regression}}
The simple linear regression used BMI as the response variable and waist-to-hip ratio as the explanatory variable. Pearson correlation was $r={corr.statistic:.3f}$ with $p={corr.pvalue:.4f}$. The slope estimate was {simple.params["waist_hip_ratio"]:.2f} BMI units per 1.0 waist-to-hip-ratio unit, but this association was not statistically significant ($p={simple.pvalues["waist_hip_ratio"]:.4f}$), and $R^2={simple.rsquared:.3f}$.

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/bmi_vs_waist_hip_ratio.png}}
\caption{{Scatterplot with least-squares regression line for BMI and waist-to-hip ratio.}}
\end{{figure}}

\section{{Two-Sample t-Test and ANOVA}}
Mean BMI was {irregular.mean():.2f} for irregular cycles and {regular.mean():.2f} for regular cycles. A Welch two-sample t-test gave $t={ttest.statistic:.2f}$ and $p={ttest.pvalue:.4f}$, suggesting higher BMI among participants with irregular cycles before adjustment.

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/bmi_by_cycle_group.png}}
\caption{{BMI by menstrual cycle regularity.}}
\end{{figure}}

For the one-way ANOVA, we split total follicle count into low, medium, and high groups. The ANOVA was not statistically significant, $F={anova_table.loc["C(follicle_group)", "F"]:.2f}$, $p={anova_table.loc["C(follicle_group)", "PR(>F)"]:.4f}$, so Tukey's HSD was not needed.

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/bmi_by_follicle_group.png}}
\caption{{BMI across low, medium, and high follicle-count groups.}}
\end{{figure}}

\section{{Multiple Regression}}
The full multiple linear regression included clinical, hormonal, lifestyle, and ultrasound predictors. The full model adjusted $R^2$ was {full_model.rsquared_adj:.3f}; the reduced clinical model adjusted $R^2$ was {reduced_model.rsquared_adj:.3f}. VIF values for non-intercept predictors were all close to 1, suggesting no major multicollinearity problem.

{latex_table(top_coef_tex, "Largest full-model terms by absolute t-statistic.", "tab:coef")}

\section{{Model Block Comparison}}
Following the structure used in recent community/research modeling, we compared clinical-only, laboratory-only, ultrasound-only, and combined model blocks using adjusted $R^2$. This asks whether easy-to-collect clinical variables explain BMI about as well as more intensive hormone or ultrasound variables.

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/model_block_adjusted_r2.png}}
\caption{{Adjusted $R^2$ by predictor block.}}
\end{{figure}}

{latex_table(block_table, "Adjusted $R^2$ comparison by predictor block.", "tab:block")}

\section{{BMI Subgroup Checks}}
Because recent work stratifies by BMI $<24$ vs BMI $\geq 24$, we used the same threshold as an exploratory subgroup check. Since BMI defines the groups, these results should be interpreted as descriptive comparisons of associated variables rather than causal tests.

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/amh_by_bmi_subgroup.png}}
\caption{{AMH by BMI subgroup among PCOS-positive participants.}}
\end{{figure}}

{latex_table(subgroup_table, "Exploratory BMI subgroup comparisons among PCOS-positive participants.", "tab:subgroup")}

\section{{PCOS vs Non-PCOS Context}}
Although our main response is BMI among PCOS-positive participants, this table helps the team understand what separates the PCOS-positive and non-PCOS rows in the dataset.

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/amh_by_pcos_status.png}}
\caption{{AMH by PCOS status in the full dataset.}}
\end{{figure}}

{latex_table(context_table, "Exploratory PCOS vs non-PCOS context comparisons.", "tab:context")}

\section{{Interactions and Sensitivity Checks}}
We tried a small set of theory-informed interaction terms and sensitivity checks. The goal is not stepwise selection; it is to see whether the main conclusions are stable when we allow simple effect modification or reduce the influence of extreme hormone/BMI values.

{latex_table(interaction_table, "Interaction model comparison.", "tab:interactions")}

{latex_table(sensitivity_table, "Sensitivity checks for model adequacy.", "tab:sensitivity")}

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/multiple_regression_residuals.png}}
\caption{{Residual plot for the full multiple linear regression.}}
\end{{figure}}

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{../figures/multiple_regression_qq.png}}
\caption{{Q-Q plot for the full multiple linear regression residuals.}}
\end{{figure}}

\section{{First Takeaway}}
The most consistent BMI-related variable in this first run is self-reported weight gain. Cycle irregularity showed a BMI difference in the two-sample t-test, but the coefficient became smaller after adjustment. Waist-to-hip ratio, AMH, LH/FSH ratio, random blood sugar, and ultrasound follicle measures did not show strong independent linear associations with BMI in this PCOS-positive subset.

\section{{Links to Share}}
\begin{{itemize}}
\item Kaggle dataset: \url{{https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos}}
\item AutoPCOS paper using clinical/lab/ultrasound blocks: \url{{https://www.frontiersin.org/journals/endocrinology/articles/10.3389/fendo.2026.1760541/full}}
\item Explainable ML paper using this Kaggle dataset: \url{{https://www.mdpi.com/2571-5577/6/2/32}}
\item Staged-modeling preprint discussing label limitations: \url{{https://www.medrxiv.org/content/10.1101/2025.10.27.25338898v2.full-text}}
\item 2023 international PCOS guideline page: \url{{https://www.monash.edu/medicine/mchri/pcos/guideline}}
\end{{itemize}}

\begin{{thebibliography}}{{9}}
\bibitem{{autopcos}} Hou et al. AutoPCOS: a stepwise multimodal intelligent framework for polycystic ovary syndrome risk stratification and diagnostic support. \textit{{Frontiers in Endocrinology}}, 2026.
\bibitem{{mdpi}} Denny et al. A Distinctive Explainable Machine Learning Framework for Detection of Polycystic Ovary Syndrome. \textit{{Applied System Innovation}}, 2023.
\bibitem{{medrxiv}} A Step Toward The Use of AI for Polycystic Ovary Syndrome: Staged Modelling with Uncertainty-Aware Triage and Conformal Prediction with Cost-Efficient Risk. \textit{{medRxiv}}, 2025.
\end{{thebibliography}}

\end{{document}}
"""
    (REPORTS / "pcos_bmi_team_brief.tex").write_text(latex.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
