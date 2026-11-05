"""Synthetic-only demonstration of selective risk and abstention (not a clinical tool)."""
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SAFE-GAIT | Research Lab", page_icon="🧠", layout="wide")
st.title("SAFE-GAIT | Trustworthy Movement AI")
st.caption("Research interface • synthetic signals only • not a diagnostic or medical alert system")
st.warning("DEMONSTRATION: Data and probabilities are generated for illustration and are not model predictions on patient data.")

rng = np.random.default_rng(42)
sample_count = 1000
latent = rng.beta(1.2, 5.0, sample_count)
labels = rng.binomial(1, latent)
uncertainty = rng.uniform(0, 0.4, sample_count)
scores = np.clip(latent + rng.normal(0, 0.16, sample_count), 0.001, 0.999)

left, right = st.columns(2)
with left:
    threshold = st.slider("Alert probability threshold", 0.05, 0.95, 0.50, 0.05)
with right:
    abstention = st.slider("Abstain when uncertainty exceeds", 0.05, 0.40, 0.20, 0.01)

accepted = uncertainty <= abstention
decisions = scores >= threshold
errors = decisions != labels
coverage = float(accepted.mean())
selective_risk = float(errors[accepted].mean()) if accepted.any() else float("nan")
false_positive = int(np.sum(accepted & decisions & (labels == 0)))
false_negative = int(np.sum(accepted & ~decisions & (labels == 1)))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Automated coverage", f"{coverage:.1%}")
c2.metric("Error among automated decisions", f"{selective_risk:.1%}" if accepted.any() else "N/A")
c3.metric("False positives", false_positive)
c4.metric("False negatives", false_negative)

display = pd.DataFrame({"Synthetic probability": scores, "Uncertainty": uncertainty,
                        "Decision": np.where(~accepted, "Abstain", np.where(decisions, "Alert", "No alert"))})
st.subheader("Synthetic prediction landscape")
st.scatter_chart(display, x="Synthetic probability", y="Uncertainty", color="Decision", height=370)
st.info("The display illustrates a tradeoff, not an evaluated safety benefit. Real experiments must assess event sensitivity, calibration, alert rate and subject-level uncertainty.")
