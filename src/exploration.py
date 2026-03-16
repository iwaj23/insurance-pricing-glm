import pandas as pd
import openml
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt

freq_ds = openml.datasets.get_dataset(41214)
sev_ds = openml.datasets.get_dataset(41215)


freq, *_ = freq_ds.get_data(dataset_format= "dataframe")
sev, *_ =  sev_ds.get_data(dataset_format = "dataframe")

sev = sev[sev["ClaimAmount"]>0].copy()

sev_model_data = sev.merge(
    freq[["IDpol","DrivAge","VehAge","BonusMalus","Density","Region","VehBrand","VehGas","Area"]],
    on="IDpol",
    how="left"
)

sev_model_data = sev_model_data[["ClaimAmount","DrivAge","VehAge","BonusMalus","Density","Region","VehBrand","VehGas","Area"]].dropna()

print(sev_model_data.columns.tolist())
print(sev_model_data.columns)
print(sev_model_data.head())

severity_model = smf.glm(
    formula="""
    ClaimAmount~ DrivAge 
        + VehAge
        + BonusMalus 
        + Density
        +C(Region)
        +C(VehBrand)
        +C(VehGas)
        +C(Area)
        """,
    data=sev_model_data,
    family=sm.families.Gamma(sm.families.links.Log())
).fit()

print(severity_model.summary())

sev_model_data["PredictedSeverity"] = severity_model.predict(sev_model_data)

freq["PredictedSeverity"] = severity_model.predict(freq)


freq=freq[freq["Exposure"]>0].copy()
freq["ClaimFrequency"] = freq["ClaimNb"] / freq["Exposure"]


freq.to_csv("../data/frequency_data.csv",index=False)
sev.to_csv("../data/severity_data.csv",index=False)

# print(freq.columns)

model = smf.glm(
    formula="""
        ClaimNb ~ DrivAge
                + VehAge
                + BonusMalus
                + Density
                + C(Region)
                + C(VehBrand)
                + C(VehGas)
                + C(Area)
        """,
    data=freq,
    family=sm.families.Poisson(),
    offset=np.log(freq["Exposure"])
).fit()

print(model.summary())

coef_table = pd.DataFrame({
    "Variable": model.params.index,
    "Coefficient": model.params.values,
    "Relativity": np.exp(model.params.values)
})

print("\nFrequency Model Relativities")
print(coef_table)

freq["PredictedClaims"] = model.predict(freq)
freq["PredictedFrequency"] = freq["PredictedClaims"] / freq["Exposure"]



# Sort policies by predicted risk
lorenz = freq.sort_values("PredictedFrequency")

# Cumulative exposuire and claims
lorenz["CumExposure"] = lorenz["Exposure"].cumsum() / lorenz["Exposure"].sum()
lorenz["CumClaims"] = lorenz["ClaimNb"].cumsum() / lorenz["ClaimNb"].sum()

#gini coefficient
gini = 1-2* np.trapezoid(lorenz["CumClaims"], lorenz["CumExposure"])

print("\nModel Gini Coefficient:", round(gini,4))

# plot lorenz curve
plt.figure(figsize=(7,6))

plt.plot(lorenz["CumExposure"], lorenz["CumClaims"], label="Model")

plt.plot([0,1],[0,1], linestyle="--",color="gray", label="Random")

plt.xlabel("Cumulative Share of Exposure")
plt.ylabel("Cumulative Share of Claims")
plt.title("Lorenz Curve = Model Discrimination")

plt.legend()
plt.tight_layout()
plt.savefig("../outputs/lorenz_curve.png",dpi=300)

# Expected annual loss
freq["PurePremium"] = freq["PredictedFrequency"] * freq["PredictedSeverity"]


freq["decile"] = pd.qcut(freq["PredictedFrequency"],10,duplicates="drop")

validation = freq.groupby("decile", observed=True).agg(
    Observed=("ClaimNb","sum"),
    Exposure=("Exposure","sum"),
    Predicted=("PredictedClaims","sum")
)
# Sample policy
sample_policy = pd.DataFrame([{
    "DrivAge": 40,
    "VehAge": 5,
    "BonusMalus": 60,
    "Density": 500,
    "Region": "R24",
    "VehBrand": "B12",
    "VehGas": "Regular",
    "Area": "C",
    "Exposure": 1.0
}])
# Predict frequency, severity, and premium
sample_policy["PredictedClaims"] = model.predict(sample_policy)
sample_policy["PredictedFrequency"] = sample_policy["PredictedClaims"] / sample_policy["Exposure"]

sample_policy["PredictedSeverity"] = severity_model.predict(sample_policy)

sample_policy["PredictedPurePremium"] = (
    sample_policy["PredictedFrequency"] * sample_policy["PredictedSeverity"]
)

# Output table
print("\n Sample Policy Premium Estimate")
print(sample_policy[[
    "DrivAge",
    "VehAge",
    "BonusMalus",
    "Region",
    "VehBrand",
    "VehGas",
    "Area",
    "Exposure",
    "PredictedFrequency",
    "PredictedSeverity",
    "PredictedPurePremium"
]])



# Pricing Factor table
rel= np.exp(model.params)
relativities = pd.DataFrame({
    "Variable": rel.index,
    "Relativity": rel.values
})

def price_policy(
        drive_age,
        veh_age,
        bonus_malus,
        density,
        region,
        veh_brand,
        veh_gas,
        area,
        exposure=1.0
):
    policy = pd.DataFrame([{
        "DrivAge": drive_age,
        "VehAge": veh_age,
        "BonusMalus": bonus_malus,
        "Density": density,
        "Region": region,
        "VehBrand": veh_brand,
        "VehGas": veh_gas,
        "Area":area,
        "Exposure": exposure
    }])
    # Frequency prediction
    policy["PredictedFrequency"] = model.predict(policy)

    # policy["PredictedClaims"] = model.predict(policy)
    policy["PredictedSeverity"] = severity_model.predict(policy)
    policy["PredictedPurePremium"] = (
        policy["PredictedFrequency"] * policy["PredictedSeverity"]
    )

    return policy

quoted_policy = price_policy(
    drive_age=40,
    veh_age=5,
    bonus_malus=60,
    density=500,
    region="R24",
    veh_brand="B12",
    veh_gas="Regular",
    area="C",
    exposure=-1.0
)

print("\nQuoted Policy")
print(quoted_policy[[
    "PredictedFrequency",
    "PredictedSeverity",
    "PredictedPurePremium"
]])

rating_table = relativities[
    relativities["Variable"].str.contains("Area|Region|VehBrand|VehGas")
].copy()

print("\nRating Factors")
print(rating_table)

rating_table["Factor"]= rating_table["Variable"].str.extract(r"C\((.*?)\)")
rating_table["Level"] = rating_table["Variable"].str.extract(r"T\.(.*)\]")

print("\nClean Rating Table")
print(rating_table.sort_values(["Factor", "Relativity"]))

validation["ObservedFreq"] = validation["Observed"] / validation["Exposure"]
validation["PredictedFreq"] = validation["Predicted"] / validation["Exposure"]

# Scatter Plot
plt.figure(figsize=(8,6))
plt.scatter(freq["ClaimFrequency"], freq["PredictedFrequency"], alpha=0.2)

max_freq=max(freq["ClaimFrequency"].max(), freq["PredictedFrequency"].max())
plt.plot(
    [0, max(freq["ClaimFrequency"])],
    [0,max(freq["ClaimFrequency"])],
    color= "red"
)

plt.xlabel("Observed Claim Frequency")
plt.ylabel("Predicted Claim Frequency")
plt.title("Observed vs Predicted Claim Frequency")

plt.figure(figsize=(8,5))

x = range(1,len(validation)+1)

plt.plot(x, validation["ObservedFreq"].values, marker="o", label="Observed")
plt.plot(x, validation["PredictedFreq"].values, marker="o", label="Predicted")

plt.title("Observed vs Predicted Claim Frequency by Decile")
plt.xlabel("Risk Decile")
plt.ylabel("Claim Frequency")
plt.xticks(x)
plt.legend()

plt.figure(figsize=(8,5))

plt.hist(freq["PurePremium"], bins=50)

plt.title("Predicted Pure Premium Distribution")
plt.xlabel("Expected Loss Cost")
plt.ylabel("Number of Policies")

print(validation[["Observed", "Exposure", "ObservedFreq", "PredictedFreq"]])

print("\nExposure by Decile:")
print(validation["Exposure"])

plt.tight_layout()
plt.savefig("../outputs/observed_vs_predicted_decile.png", dpi=300)

freq["DevianceResidual"] = model.resid_deviance
plt.figure(figsize=(8,5))
plt.scatter(freq["PredictedFrequency"], freq["DevianceResidual"], alpha=0.2)
plt.xlabel("Predicted Frequency")
plt.ylabel("Deviance Residual")
plt.title("GLM Residual Diagnostics")

rel = np.exp(model.params).drop("Intercept")

#measure how far each factor is from neutral risk (1.0)
importance = (rel -1).abs()

top = importance.sort_values(ascending=False).head(12).index
rel_top = rel.loc[top].sort_values()

plt.figure(figsize=(7,5))

rel_top.plot(kind="barh")

plt.title("Top Frequency Model Risk Relativities")
plt.xlabel("Risk Multiplier")
plt.ylabel("Variable")

plt.tight_layout()
plt.yticks(fontsize=9)
plt.show()