# %%
import pandas as pd
import numpy as np

df = pd.read_csv("fixed.csv", encoding="utf-8", sep=",")

print(df.columns)

df["Eläimen lempilelut"] = (
    df["Eläimen lempilelut"]
    .str.strip("[]")
    .str.replace("'","")
    .str.split(";")
)
df["Eläimen lempilelut"] = df["Eläimen lempilelut"].apply(
    lambda x: x if isinstance(x, list) and len(x) > 0 else [np.nan]
)

df = df.explode("Eläimen lempilelut")

pd.set_option('display.max_columns', None)
print(df.head())

# %%
df

# %%

# testaaan yhdistelmää

df["Yhdistelmä"] = df["Eläin"].astype(str) + " | " + \
                    df["Eläimen lempilelut"].astype(str) + " | " + \
                    df["Toimenpide"].astype(str)

print(df["Yhdistelmä"])
# %%
if df.duplicated().sum() == 0:
    print("Kaikki rivit ovat uniikkeja")
else:
    print("On duplicate-rivejä → harkitse primary key -yhdistelmää")