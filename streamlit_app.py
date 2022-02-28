# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns

# %%
# Data Load
data = pd.read_csv("fee_records.csv")
# %% [markdown]
# # Data Cleaning
# %%
## Batch dates
# - Are the September fees belong to a two-week period?
assert (
    data["batch__name"].str.replace(" Network Fees", "").nunique()
    == data["batch__name"].nunique()
)

data.loc[
    data["batch__name"] == "Sept 2021 Network Fees", "batch__name"
] = "Sept 16-30 2021 Network Fees"

data["batch_date"] = (
    data["batch__name"]
    .str.split(" ")
    .apply(lambda x: pd.to_datetime(f"{x[2]}-{x[0]}-{x[1].split('-')[0]}"))
)

data = data.sort_values("batch_date")
# %%
## Employer names
# - are Compass Digital Labs and Compass, Inc. the same?
# - "-331", "-453" invoice number and client name are the same

data["employer"] = data["employer_name"].str.replace(" \(.*$", "", regex=True)
employer_codes = {
    "bad": ["-331", "-453", "917-30"],
    "rename": {"Porsche Digital, Inc.": "Porsche Digital Inc."},
}

data = data.loc[~data["employer"].isin(employer_codes["bad"]), :]
for wrong_name, right_name in employer_codes["rename"].items():
    data.loc[data["employer"] == wrong_name, "employer"] = right_name

for name in np.sort(data["employer"].unique()):
    print(name)
# %%
## Job titles
data["job_title"] = data["job_title"].str.rstrip('"').str.lstrip('"')
for job in np.sort(data["job_title"].unique()):
    print(job)
# %% [markdown]
# # General stats
# %%
st.write("# General stats")
# %%
# Batch date
def_btrst = 3.37
btrst_price = st.slider("BTRST/USD", value=def_btrst, min_value=1e-10, max_value=100.0)

date_fees = (
    data.groupby(data["batch_date"].astype(str))["gross_total"]
    .sum()
    .rename("Fees Paid")
    .to_frame()
).assign(BTRST_price=def_btrst)


date_fees = pd.concat(
    [
        date_fees,
        (date_fees["Fees Paid"] / def_btrst * btrst_price)
        .to_frame()
        .assign(BTRST_price=btrst_price),
    ]
)


st.write("## Converted fee amount by invoice periods", date_fees)

fig, axes = plt.subplots(1, 1)
g = sns.barplot(
    data=date_fees, x=date_fees.index, y="Fees Paid", hue="BTRST_price", axes=axes
).set_title("Fees Paid")

st.write(fig)
# %%
# Employer
# st.write(
#     "## Contracts by employers",
#     data["employer"].str.replace(" \(.*$", "", regex=True).value_counts(),
# )

# %%
fee_employees = (
    data.groupby("employer")["gross_total"]
    .agg(["sum", "mean", "std"])
    .rename(
        columns={
            "sum": "Total",
            # "count": "#",
            "std": "STD",
            "mean": "Mean",
        }
    )
    .sort_values("Total", ascending=False)
)

st.write("## Contracts by employers", fee_employees)

fig, axes = plt.subplots(1, 1)
fee_employees_tochart = fee_employees["Total"].sort_values(ascending=True)
sns.barplot(
    # data=fee_employees_tochart,
    axes=axes,
    x=fee_employees_tochart.index,
    y=fee_employees_tochart,
)
# fee_employees["Total"].sort_values(ascending=True).plot(kind="bar", axes=axes)
axes.set_xticklabels([])
axes.set_xlabel("Fees paid by employees")
st.write(fig)

# %%

# %%
fee_jobs = (
    data.groupby("job_title")["gross_total"]
    .agg(["sum", "mean", "std"])
    .rename(
        columns={
            "sum": "Total",
            # "count": "#",
            "std": "STD",
            "mean": "Mean",
        }
    )
    .sort_values("Total", ascending=False)
)

st.write("## Fees paid by job title", fee_jobs)
fig, axes = plt.subplots(1, 1)
# fee_jobs["Total"].sort_values(ascending=True).plot(kind="bar", axes=axes)
fee_jobs_tochart = fee_employees["Total"].sort_values(ascending=True)
sns.barplot(
    # data=fee_jobs_tochart,
    axes=axes,
    x=fee_jobs_tochart.index,
    y=fee_jobs_tochart,
)
axes.set_xticklabels([])
axes.set_xlabel("Fees by job title")
st.write(fig)


# %%
