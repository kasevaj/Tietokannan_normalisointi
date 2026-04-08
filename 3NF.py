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

# jaetaan talukoihin: 

# KeskusID: primary = id, nimi, perustamisvuosi ja osoite
df_keskus = df[["Keskuksen nimi", "Keskuksen perustamisvuosi", "Keskuksen osoite"]].drop_duplicates()
df_keskus.insert(0,"KeskusID", range(1, len(df_keskus)+1))
df = df.merge(df_keskus[["Keskuksen nimi", "KeskusID"]], on="Keskuksen nimi", how="left")
assert df_keskus["KeskusID"].is_unique

# EläinID: primary = id, nimi, ikä, laji, kiinniottopaikka, kiinniottopvm
df_elain = df[["Eläin", "Eläimen ikä", "Eläimen kiinniottopaikka", "Kiinniottopvm", "Eläimen laji"]].drop_duplicates()
df_elain.insert(0, "EläinID", range(1, len(df_elain)+1))
df = df.merge(df_elain[["Eläin", "EläinID"]], on="Eläin", how="left")
assert df_elain["EläinID"].is_unique


# EläinLelut primary = id + lempilelut
df_lelut = df[["EläinID", "Eläimen lempilelut"]].drop_duplicates()

# HoitajaID: primary=id, nimi, palkka, keskusId
df_hoitaja = df[["Hoitajan nimi", "Hoitajan palkka", "KeskusID"]].drop_duplicates()
df_hoitaja.insert(0, "HoitajaID", range(1, len(df_hoitaja)+1))
df = df.merge(df_hoitaja[["Hoitajan nimi", "HoitajaID"]], on="Hoitajan nimi", how="left")
assert df_hoitaja["HoitajaID"].is_unique

# Toimenpiteet: primary = ToimenpideId, toimenpide
df_toimenpiteet = df[["Toimenpide"]].drop_duplicates()
df_toimenpiteet.insert(0, "ToimenpideID", range(1, len(df_toimenpiteet)+1))
df = df.merge(df_toimenpiteet[["Toimenpide", "ToimenpideID"]], on="Toimenpide", how="left")
assert df_toimenpiteet["ToimenpideID"].is_unique

# Tapahtumat: primary = Eläin + toimenpide + toimenpiteen pvm, hoitajan nimi
df_toimenpideTapahtumat = df[["EläinID", "ToimenpideID", "Toimenpiteen pvm", "HoitajaID"]].drop_duplicates()

# %%
print(df_hoitaja)
# %%
print(df_elain)
# %%
print(df_keskus)
# %%
print(df_lelut)
# %%
print(df_toimenpiteet)

# %%
print(df_toimenpideTapahtumat)