Insurance Pricing Model — Frequency–Severity GLM

This project implements an actuarial insurance pricing model using a frequency–severity framework.

The model estimates the expected loss cost of insurance policies by modeling:

Claim frequency (number of claims per policy)

Claim severity (size of claims)

The two models are combined to estimate the pure premium, which represents the expected annual claim cost for a policy.

This project demonstrates how actuaries build and validate insurance pricing models using generalized linear models (GLMs).

Model Features

The model includes:

Claim frequency modeling using a Poisson GLM

Claim severity modeling using a Gamma GLM

Pure premium estimation using the frequency–severity framework

Risk relativities derived from model coefficients

Policy-level premium estimation

Decile validation of predicted risk

Lorenz curve analysis for model discrimination

Gini coefficient calculation

Visualization of model diagnostics

Pricing Framework

Insurance pricing is commonly modeled using the frequency–severity decomposition:

Pure Premium = Claim Frequency × Claim Severity

Where:

Frequency = expected number of claims per policy

Severity = expected cost per claim

The model predicts both components using GLMs and multiplies them to estimate the expected loss cost.

Dataset

The dataset contains automobile insurance policy data with policyholder characteristics and claim outcomes.

Key variables include:

Variable	Description
DrivAge	Driver age
VehAge	Vehicle age
BonusMalus	Bonus–malus risk score
Density	Population density
Region	Geographic region
VehBrand	Vehicle brand
VehGas	Fuel type
Area	Urban density category
ClaimNb	Number of claims
ClaimAmount	Claim severity

The dataset includes hundreds of thousands of policies, allowing realistic modeling of insurance risk.

Modeling Approach

Two generalized linear models are estimated.

Frequency Model

Claim frequency is modeled using a Poisson GLM with a log link:

ClaimNb ~ Poisson(λ)

log(λ) = Xβ

This model estimates the expected number of claims per policy.

Severity Model

Claim severity is modeled using a Gamma GLM with a log link:

ClaimAmount ~ Gamma(μ)

log(μ) = Xβ

This model estimates the expected claim size conditional on a claim occurring.

Model Validation

Model performance was evaluated using several techniques.

Decile Validation

Policies were ranked by predicted risk and grouped into risk deciles.

Observed and predicted claim frequencies were compared across deciles to confirm that the model correctly ranks policies from low risk to high risk.

Lorenz Curve

The Lorenz curve evaluates the model’s ability to discriminate between high-risk and low-risk policies.

If the model has predictive power, the curve deviates from the random baseline.

Gini Coefficient

The Gini coefficient summarizes the discriminatory power of the model.

Gini = 1 − 2 ∫ L(p) dp

Model result:

Gini coefficient = 0.31

A value above 0.30 indicates strong risk discrimination for an insurance pricing model.

Sample Policy Quote

The model can generate a premium estimate for a new policy.

Example policy:

Driver Age	Vehicle Age	BonusMalus	Region
40	5	60	R22

Model output:

Predicted Frequency	Predicted Severity	Pure Premium
0.1227	2715	333

This represents the expected annual claim cost for the policy.

Visual Outputs

The program generates the following visualizations:

Observed vs predicted claim frequency

Risk decile validation chart

Predicted pure premium distribution

GLM residual diagnostics

Lorenz curve for model discrimination

Technologies Used

Python

Pandas

NumPy

Statsmodels

Matplotlib

How to Run

Install dependencies:

pip install -r requirements.txt

Run the model:

python exploration.py
Purpose

This project demonstrates actuarial risk modeling techniques used in insurance pricing, including:

frequency–severity modeling

generalized linear models

insurance rating factors

risk discrimination analysis

The goal is to illustrate how actuarial pricing models estimate expected loss costs and evaluate predictive performance.
