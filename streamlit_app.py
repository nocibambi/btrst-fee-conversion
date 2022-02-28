# %%
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

# %%
data = pd.read_csv("fee_records.csv")
st.write("# Data set")
data.head()
# %%
assert (
    data["batch__name"].str.replace(" Network Fees", "").nunique()
    == data["batch__name"].nunique()
)
# %%
data.loc[
    data["batch__name"] == "Sept 2021 Network Fees", "batch__name"
] = "Sept 16-30 2021 Network Fees"
# %%
data["batch__name"].str.split(" ")
data["batch__name"].unique()
# %%
data["batch__name"].str.split(" ").apply(
    # lambda x: f"{x[2]}-{x[0]}-{x[1].strip('-')}"
    lambda x: f"{x[1].split('-')}"
).unique()
# %%
data["batch_date"] = (
    data["batch__name"]
    .str.split(" ")
    .apply(lambda x: pd.to_datetime(f"{x[2]}-{x[0]}-{x[1].split('-')[0]}"))
    # .unique()
)

# pd.to_datetime(data['batch__name'].str.replace(" Network Fees", ""), format="%M %D-%")
# %%
data.groupby("batch_date")["gross_total"].sum()
# %%
data["employer"] = data["employer_name"].str.replace(" \(.*$", "", regex=True)
# %%
data["employer"].str.replace(" \(.*$", "", regex=True).value_counts()
# %%
# - are Compass Digital Labs and Compass, Inc. the same?
# - "-331", "-453" invoice number and client name are the same
employer_codes = {
    "bad": ["-331", "-453", "917-30"],
    "rename": {"Porsche Digital, Inc.": "Porsche Digital Inc."},
}

data = data.loc[~data["employer"].isin(employer_codes["bad"]), :]
for wrong_name, right_name in employer_codes["rename"].items():
    data.loc[data["employer"] == wrong_name, "employer"] = right_name

# %%
for name in np.sort(data["employer"].unique()):
    print(name)

# %%
# %%
data.groupby("employer")["gross_total"].sum().sort_values(ascending=False)
# %%
data.groupby("employer")["gross_total"].agg(
    ["mean", "std", "count", "sum"]
).sort_values("mean", ascending=False)

# %%
data["job_title"] = data["job_title"].str.rstrip('"').str.lstrip('"')
# %%
for job in np.sort(data["job_title"].unique()):
    print(job)
# %%
data.groupby("job_title")["gross_total"].sum().sort_values(ascending=False)
# %%
data.groupby("job_title")["gross_total"].agg(["mean", "std", "count", "sum"])

# %%
