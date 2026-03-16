# Insurance Pricing Model — Frequency–Severity GLM

This project implements an actuarial insurance pricing model using a frequency–severity framework.

The model estimates the expected loss cost of insurance policies by modeling:

- Claim frequency (number of claims per policy)
- Claim severity (size of claims)

The two models are combined to estimate the pure premium, which represents the expected annual claim cost for a policy.

This project demonstrates how actuaries build and validate insurance pricing models using generalized linear models (GLMs).

---

## Model Features

The model includes:

- Claim frequency modeling using a Poisson GLM
- Claim severity modeling using a Gamma GLM
- Pure premium estimation using the frequency–severity framework
- Risk relativities derived from model coefficients
- Policy-level premium estimation
- Decile validation of predicted risk
- Lorenz curve analysis for model discrimination
- Gini coefficient calculation
- Visualization of model diagnostics

---

## Pricing Framework

Insurance pricing is commonly modeled using the frequency–severity decomposition:


Pure Premium = Claim Frequency × Claim Severity


Where:

- Frequency = expected number of claims per policy
- Severity = expected cost per claim

The model predicts both components using GLMs and multiplies them to estimate the expected loss cost.

---

## Dataset

The dataset contains automobile insurance policy data with policyholder characteristics and claim information.

### Key Variables

| Variable | Description |
|---------|-------------|
| DrivAge | Driver age |
| VehAge | Vehicle age |
| BonusMalus | Bonus–malus risk score |
| Density | Population density |
| Region | Geographic region |
| VehBrand | Vehicle brand |
| VehGas | Fuel type |
| Area | Urban density category |
| ClaimNb | Number of claims |
| ClaimAmount | Claim severity |

The dataset includes hundreds of thousands of policies, enabling realistic modeling of insurance risk.

---

## Modeling Approach

Two generalized linear models are estimated.

### Frequency Model

The claim frequency model estimates the expected number of claims.

Model specification:


ClaimNb ~ Poisson(λ)
log(λ) = Xβ


Key features:

- Poisson GLM
- Exposure adjustment
- Log link function
- Policy-level predictors

This model estimates the expected claim frequency for each policy.

---

### Severity Model

The claim severity model estimates the expected claim cost.

Model specification:


ClaimAmount ~ Gamma(μ)
log(μ) = Xβ


Key features:

- Gamma GLM
- Log link
- Policy characteristics as predictors

This model estimates the expected claim size conditional on a claim occurring.

---

## Pure Premium Estimation

The expected annual loss cost for a policy is calculated as:


Pure Premium = Predicted Frequency × Predicted Severity


Example output from the model:

| Predicted Frequency | Predicted Severity | Pure Premium |
|--------------------|-------------------|-------------|
| 0.1227 | 2715 | 333 |

This represents the expected annual loss cost for the policy.

---

## Model Validation

Several techniques were used to evaluate model performance.

### Decile Validation

Policies were sorted by predicted risk and grouped into risk deciles.

Observed and predicted claim frequencies were compared across deciles.

This evaluates whether the model correctly ranks policies from low risk to high risk.

Example validation output:

| Risk Decile | Observed Frequency | Predicted Frequency |
|-------------|-------------------|--------------------|
| 1 | Low | Low |
| ... | ... | ... |
| 10 | High | High |

---

### Lorenz Curve

The Lorenz curve evaluates the model’s ability to discriminate between high-risk and low-risk policies.

The curve compares:

- cumulative share of policies
- cumulative share of claims

If the model has predictive power, the curve will deviate from the random baseline.

---

### Gini Coefficient

The Gini coefficient summarizes the discriminatory power of the model.


Gini = 1 − 2 ∫₀¹ L(p) dp


Where **L(p)** is the Lorenz curve.

**Model result**


Gini coefficient = 0.31


Interpretation:

- 0 = no predictive power
- 0.3+ = strong discrimination for insurance pricing models

---

## Rating Factors

Model coefficients were converted into risk relativities used in insurance rating.

Example:

| Factor | Level | Relativity |
|------|------|------|
| Area | F | 1.25 |
| Region | R74 | 1.20 |
| Vehicle Brand | B12 | 1.18 |

These factors represent multiplicative adjustments to the base premium.

---

## Sample Policy Quote

The model can generate a premium estimate for a new policy.

Example policy:

| Driver Age | Vehicle Age | BonusMalus | Region |
|------------|-------------|------------|--------|
| 40 | 5 | 60 | R22 |

Model output:

| Predicted Frequency | Predicted Severity | Pure Premium |
|--------------------|-------------------|-------------|
| 0.1227 | 2715 | 333 |

This represents the expected annual loss cost.

---

## Visualizations

The project includes several diagnostic plots:

- Observed vs Predicted Frequency
- Risk Decile Validation
- Pure Premium Distribution
- GLM Residual Diagnostics
- Lorenz Curve

---

## Technologies Used

- Python
- Pandas
- NumPy
- Statsmodels
- Matplotlib

---

## Project Structure

```
insurance-pricing-glm
│
├── data
│
├── src
│   └── exploration.py
│
├── outputs
│   ├── lorenz_curve.png
│   └── observed_vs_predicted_decile.png
│
└── README.md
```


---

## Possible Extensions

Future improvements could include:

- regularized GLMs
- gradient boosting models
- feature engineering
- out-of-sample validation
- credibility adjustments
- full premium calculation including expenses and profit loading
