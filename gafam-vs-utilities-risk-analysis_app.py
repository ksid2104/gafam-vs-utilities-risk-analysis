#--------------------------------------------------------#
# Streamlit App ( to run the app : "streamlit run gafam-vs-utilities-risk-analysis_app.py")
#--------------------------------------------------------#
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import datetime

# ─────────────────────────────────────────────
# App layout et paramètres
# ─────────────────────────────────────────────
st.set_page_config(layout="wide")
st.title("Analyse sectorielle : GAFAM vs Utilities")
st.markdown("""
On entend souvent dire que les GAFAM sont synonymes de risques élevés, alors que les Utilities représentent un refuge sûr. Mais pourquoi cette réputation ?  
Pour répondre à cette question, cette analyse compare ces deux secteurs sous l’angle du risque et de la performance.  
En observant concrètement leurs données de marché, découvrons ensemble si cette affirmation courante en finance se vérifie vraiment.
""")
st.sidebar.header("Paramètres")
start_date = st.sidebar.date_input("Date de début", value=pd.to_datetime("2000-05-31"))
end_date = st.sidebar.date_input("Date de fin", value=datetime.date.today())

# ─────────────────────────────────────────────
# Téléchargement des données et rendements log
# ─────────────────────────────────────────────
st.header("1. Données de marché & Rendements log")
tickers = ["AAPL", "MSFT", "META", "GOOG", "AMZN", "NEE", "DUK", "SO", "D", "AEP"]

def download_clean_log_returns(tickers, start_date, end_date):
    df = yf.download(tickers, start=start_date, end=end_date)["Close"]
    log_return = np.log(df / df.shift(1)).dropna()
    return log_return

log_return = download_clean_log_returns(tickers, start_date, end_date)
st.dataframe(log_return.tail(), use_container_width=True)
st.markdown("ℹ️ **Insight :** Les rendements journaliers logarithmiques permettent de comparer de manière homogène les variations de prix entre les GAFAM et Utilities.")

def clean_outliers(df, n_std=3):
    return df[(np.abs((df - df.mean()) / df.std()) < n_std).all(axis=1)]

log_return_clean = clean_outliers(log_return)

# ─────────────────────────────────────────────
# Statistiques descriptives
# ─────────────────────────────────────────────
st.header("2. Statistiques descriptives")

# Stats individuelles
Gafam = pd.DataFrame({
    "Mean": log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].mean(),
    "Std": log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].std(),
    "Skewness": log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].skew(),
    "Kurtosis": log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].kurtosis()
})

Utilities = pd.DataFrame({
    "Mean": log_return[["NEE", "DUK", "SO", "D", "AEP"]].mean(),
    "Std": log_return[["NEE", "DUK", "SO", "D", "AEP"]].std(),
    "Skewness": log_return[["NEE", "DUK", "SO", "D", "AEP"]].skew(),
    "Kurtosis": log_return[["NEE", "DUK", "SO", "D", "AEP"]].kurtosis()
})

st.subheader("GAFAM")
st.dataframe(Gafam)
st.subheader("Utilities")
st.dataframe(Utilities)
st.markdown("ℹ️ **Insight :** Les GAFAM affichent des rendements journaliers moyens plus élevés que les Utilities, mais avec une dispersion plus marquée autour de cette moyenne, traduisant une volatilité plus accru à court terme.")

# Agrégation secteur
Gafam_sector = log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].stack()
Utilities_sector = log_return[["NEE", "DUK", "SO", "D", "AEP"]].stack()

gafam_stat = pd.DataFrame({
    "Mean": [Gafam_sector.mean()],
    "Std": [Gafam_sector.std()],
    "Skewness": [Gafam_sector.skew()],
    "Kurtosis": [Gafam_sector.kurtosis()]
}, index=["GAFAM"])

utilities_stat = pd.DataFrame({
    "Mean": [Utilities_sector.mean()],
    "Std": [Utilities_sector.std()],
    "Skewness": [Utilities_sector.skew()],
    "Kurtosis": [Utilities_sector.kurtosis()]
}, index=["Utilities"])

st.subheader("Agrégation par secteur")
st.dataframe(pd.concat([gafam_stat, utilities_stat]))
st.markdown("ℹ️ **Insight :** L’agrégation confirme ce qui appraissaient à l'échelle individuelle (rendements moyens quotidiens plus élévés,plus volatile). Toutefois, la skewness et le kurtosis sectoriel élévé nous permettent de compléter notre analyse en comprenant que la meilleure performance moyenne des GAFAM est en partie due à des hausses extrêmes qui sont rares, mais néanmmoins plus fréquentes que pour les Utilities. Leur rendement est donc plus irrégulier mais potentiellement plus explosif que celui des Utilities, qui affichent une performance plus stable.")
# ─────────────────────────────────────────────
# Value at Risk (VaR) - normale et empirique
# ─────────────────────────────────────────────
st.header("3. Value at Risk (VaR)")

# VaR normale théorique
gafam_stat["VaR à 95%"] = norm.ppf(0.05, gafam_stat["Mean"], gafam_stat["Std"])
gafam_stat["VaR à 99%"] = norm.ppf(0.01, gafam_stat["Mean"], gafam_stat["Std"])
utilities_stat["VaR à 95%"] = norm.ppf(0.05, utilities_stat["Mean"], utilities_stat["Std"])
utilities_stat["VaR à 99%"] = norm.ppf(0.01, utilities_stat["Mean"], utilities_stat["Std"])

# VaR empirique (historique)
gafam_VaR_95_emp = np.percentile(Gafam_sector, 5)
gafam_VaR_99_emp = np.percentile(Gafam_sector, 1)
utilities_VaR_95_emp = np.percentile(Utilities_sector, 5)
utilities_VaR_99_emp = np.percentile(Utilities_sector, 1)

# DataFrame combinée VaR normale et historique
VaR_comparative = pd.DataFrame({
    "VaR 95% Normale": [gafam_stat["VaR à 95%"].values[0], utilities_stat["VaR à 95%"].values[0]],
    "VaR 95% Historique": [gafam_VaR_95_emp, utilities_VaR_95_emp],
    "VaR 99% Normale": [gafam_stat["VaR à 99%"].values[0], utilities_stat["VaR à 99%"].values[0]],
    "VaR 99% Historique": [gafam_VaR_99_emp, utilities_VaR_99_emp]
}, index=["GAFAM", "Utilities"])

st.subheader("Comparaison VaR normale vs historique")
st.dataframe(VaR_comparative)


st.markdown("""
ℹ️ **Insight :**  
- La VaR empirique prend en compte la distribution réelle des rendements passés et peut différer de la VaR calculée sous hypothèse que les rendements suivent une distribution normale.  
- Pour un même niveau de risque, les Utilities affichent une Value at Risk (VaR) moins extrême que les GAFAM. En cas de choc de marché, les pertes maximales attendues sont plus importantes pour les GAFAM. Cela confirme leur nature plus risquée en situation extrême.""")

# ─────────────────────────────────────────────
# Intervalle de confiance
# ─────────────────────────────────────────────
st.header("4. Intervalle de confiance sur la moyenne")

def get_confidence_interval(mean, std, n, alpha=0.05):
    z = norm.ppf(1 - alpha/2)
    margin_error = z * (std / np.sqrt(n))
    return mean - margin_error, mean + margin_error, margin_error

ic_gafam = get_confidence_interval(gafam_stat["Mean"].values[0], gafam_stat["Std"].values[0], Gafam_sector.shape[0])
ic_utilities = get_confidence_interval(utilities_stat["Mean"].values[0], utilities_stat["Std"].values[0], Utilities_sector.shape[0])

st.write(f"Intervalle de confiance GAFAM (95%) : [{ic_gafam[0]:.6f} ; {ic_gafam[1]:.6f}]")
st.write(f"Intervalle de confiance Utilities (95%) : [{ic_utilities[0]:.6f} ; {ic_utilities[1]:.6f}]")
st.markdown("ℹ️ **Insight :** Malgré leur volatilité individuelle, les GAFAM présentent un intervalle de confiance plus resserré. Cela indique que, collectivement, leur moyenne de rendement est estimée avec une incertitude plus faible que celle des Utilities et traduit une meilleure stabilité moyenne dans la performance agrégée.")
# ─────────────────────────────────────────────
# Histogrammes et distributions
# ─────────────────────────────────────────────
st.header("5. Visualisation des distributions")

fig, ax = plt.subplots(2, 2, figsize=(12, 8))

dens_gafam = np.arange(Gafam_sector.min() - 0.001, Gafam_sector.max() + 0.001, 0.001)
dens_util = np.arange(Utilities_sector.min() - 0.001, Utilities_sector.max() + 0.001, 0.001)

# Histogrammes + PDF
ax[0, 0].hist(Gafam_sector, bins=100, density=True, color='skyblue', alpha=0.6, label="Rendements GAFAM")
ax[0, 0].plot(dens_gafam, norm.pdf(dens_gafam, gafam_stat["Mean"], gafam_stat["Std"]), color="blue", label="PDF Normale")
ax[0, 0].set_title("Histogramme GAFAM")
ax[0, 0].set_xlabel("Rendement Logarithmique")
ax[0, 0].set_ylabel("Densité")
ax[0, 0].legend()

ax[0, 1].hist(Utilities_sector, bins=100, density=True, color='skyblue', alpha=0.6, label="Rendements Utilities")
ax[0, 1].plot(dens_util, norm.pdf(dens_util, utilities_stat["Mean"], utilities_stat["Std"]), color="green", label="PDF Normale")
ax[0, 1].set_title("Histogramme Utilities")
ax[0, 1].set_xlabel("Rendement Logarithmique")
ax[0, 1].set_ylabel("Densité")
ax[0, 1].legend()

# CDF + VaR normale + VaR empirique
ax[1, 0].plot(dens_gafam, norm.cdf(dens_gafam, gafam_stat["Mean"], gafam_stat["Std"]), color="blue", label="CDF GAFAM")
ax[1, 0].axvline(gafam_stat["VaR à 95%"].values[0], color="orange", linestyle="--", label="VaR Normale 95%")
ax[1, 0].axvline(gafam_stat["VaR à 99%"].values[0], color="red", linestyle="--", label="VaR Normale 99%")
ax[1, 0].axvline(gafam_VaR_95_emp, color="orange", linestyle="-.", label="VaR Empirique 95%")
ax[1, 0].axvline(gafam_VaR_99_emp, color="red", linestyle="-.", label="VaR Empirique 99%")
ax[1, 0].set_title("CDF GAFAM avec VaR")
ax[1, 0].set_xlabel("Rendement Logarithmique")
ax[1, 0].set_ylabel("Probabilité cumulée")
ax[1, 0].legend()

ax[1, 1].plot(dens_util, norm.cdf(dens_util, utilities_stat["Mean"], utilities_stat["Std"]), color="green", label="CDF Utilities")
ax[1, 1].axvline(utilities_stat["VaR à 95%"].values[0], color="orange", linestyle="--", label="VaR Normale 95%")
ax[1, 1].axvline(utilities_stat["VaR à 99%"].values[0], color="red", linestyle="--", label="VaR Normale 99%")
ax[1, 1].axvline(utilities_VaR_95_emp, color="orange", linestyle="-.", label="VaR Empirique 95%")
ax[1, 1].axvline(utilities_VaR_99_emp, color="red", linestyle="-.", label="VaR Empirique 99%")
ax[1, 1].set_title("CDF Utilities avec VaR")
ax[1, 1].set_xlabel("Rendement Logarithmique")
ax[1, 1].set_ylabel("Probabilité cumulée")
ax[1, 1].legend()

plt.tight_layout()
st.pyplot(fig)

st.markdown("ℹ️ **Insight :** Les histogrammes et courbes de densité confirment les résultats précédents : les Utilities présentent une distribution plus concentrée autour de leur moyenne, tandis que les GAFAM montrent une queue gauche plus longue confirmant leur plus grande probabilité de pertes extrêmes.")
# ─────────────────────────────────────────────
# Conclusion synthétique
# ─────────────────────────────────────────────
st.header("Conclusion finale")
st.markdown("""
**En résumé :**

- Les GAFAM délivrent de meilleures performances moyennes, mais avec une plus grande dispersion.
- Leur profil de distribution est marqué par une forte asymétrie positive et une kurtosis élevée : des rendements extrêmes, positifs comme négatifs, surviennent plus souvent.
- En cas de scénario de crise, les pertes extrêmes (VaR à 99 %) sont plus importantes que celles des Utilities.
- Les Utilities confirment leur statut de valeur refuge : moins de volatilité, moins d’asymétrie, et des pertes maximales plus limitées.

---

**Analyse finale :**

Cette étude illustre la complexité du risque. Le secteur technologique ne peut pas être réduit à sa seule volatilité : il combine à la fois des opportunités de rendement élevées et une exposition aux pertes extrêmes.

À l’inverse, les Utilities sont cohérentes avec leur image défensive : elles protègent mieux en période de stress, mais offrent un potentiel de gain plus faible.

**Conclusion :**
Les investisseurs doivent arbitrer selon leur tolérance au risque, leurs objectifs de rendement, et leur horizon temporel. Ici, chaque secteur a son intérêt : explosivité mesurée (GAFAM) vs stabilité rassurante (Utilities).
""")
