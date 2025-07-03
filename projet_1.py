





# Faire Var hsitorique vs Var theorisque (normale)

# ─────────────────────────────────────────────────────────────────
# PROJET : Analyse de performance et de risque sectorielle (GAFAM vs Utilities)
# Objectifs : 
# - Manipuler des données de marché, 
# - Calculer des indicateurs clés (rendements, volatilité, skew, kurtosis, VaR), 
# - Comparer des secteurs avec rigueur statistique.
# ──────────────────────────────────────────────────────────────


# ────────────────────────────────────────────────────────────────  
# 1. IMPORT DES LIBRAIRIES  
# ────────────────────────────────────────────────────────────────  
import matplotlib.pyplot as plt    # Pour la visualisation graphique  
import yfinance as yf              # Pour récupérer les données financières  
import numpy as np                # Manipulations numériques avancées  
import pandas as pd               # Manipulations de données tabulaires  
from scipy.stats import norm, skew, kurtosis  # Statistiques descriptives et distributions  
from sklearn.linear_model import LinearRegression  # (non utilisé ici mais importé)

# ────────────────────────────────────────────────────────────────  
# 2. TÉLÉCHARGEMENT DES DONNÉES & CALCUL DES RENDEMENTS LOGARITHMIQUES  
# ────────────────────────────────────────────────────────────────  
def download_period(start_date, end_date):
    tickers = ["AAPL", "MSFT", "META", "GOOG", "AMZN", 
               "NEE", "DUK", "SO", "D", "AEP"]
    log_return = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        data["Log_Return"] = np.log(data["Close"]/data["Close"].shift(1))
        log_return[ticker] = data["Log_Return"].dropna()
    return log_return

start_date = input("📅 Date de début (format YYYY-MM-DD) : ")
end_date   = input("📅 Date de fin   (format YYYY-MM-DD) : ")
log_return = download_period(start_date, end_date)

# ────────────────────────────────────────────────────────────────  
# 3. STATISTIQUES DESCRIPTIVES PAR TITRE ET SECTEUR  
# ────────────────────────────────────────────────────────────────  

# Statistiques par action dans le secteur GAFAM  
Gafam = pd.DataFrame()
Gafam["Mean"]     = log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].mean()
Gafam["Std"]      = log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].std()
Gafam["Skewness"] = log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].skew()
Gafam["Kurtosis"] = log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].kurtosis()

# Statistiques par action dans le secteur Utilities  
Utilities = pd.DataFrame()
Utilities["Mean"]     = log_return[["NEE", "DUK", "SO", "D", "AEP"]].mean()
Utilities["Std"]      = log_return[["NEE", "DUK", "SO", "D", "AEP"]].std()
Utilities["Skewness"] = log_return[["NEE", "DUK", "SO", "D", "AEP"]].skew()
Utilities["Kurtosis"] = log_return[["NEE", "DUK", "SO", "D", "AEP"]].kurtosis()

# Statistiques agrégées par secteur  
gafam_total_log_return = log_return[["AAPL", "MSFT", "META", "GOOG", "AMZN"]].stack()
Gafam_sector = pd.DataFrame({
    "Mean":     [gafam_total_log_return.mean()],
    "Std":      [gafam_total_log_return.std()],
    "Skewness": [gafam_total_log_return.skew()],
    "Kurtosis": [gafam_total_log_return.kurtosis()]
}, index=["Gafam_sector"])

Utilities_total_log_return = log_return[["NEE", "DUK", "SO", "D", "AEP"]].stack()
Utilities_sector = pd.DataFrame({
    "Mean":     [Utilities_total_log_return.mean()],
    "Std":      [Utilities_total_log_return.std()],
    "Skewness": [Utilities_total_log_return.skew()],
    "Kurtosis": [Utilities_total_log_return.kurtosis()]
}, index=["Utilities"])

# ────────────────────────────────────────────────────────────────  
# 4. CALCUL DE LA VaR (Value at Risk)  
# ────────────────────────────────────────────────────────────────  

# VaR à 95% et 99% pour chaque secteur, basée sur la distribution normale
Gafam_sector["VaR (normale) à 95%"] = norm.ppf(0.05, Gafam_sector["Mean"], Gafam_sector["Std"])
Gafam_sector["VaR (normale) à 99%"] = norm.ppf(0.01, Gafam_sector["Mean"], Gafam_sector["Std"])
Utilities_sector["VaR (normale) à 95%"] = norm.ppf(0.05, Utilities_sector["Mean"], Utilities_sector["Std"])
Utilities_sector["VaR (normale) à 99%"] = norm.ppf(0.01, Utilities_sector["Mean"], Utilities_sector["Std"])
# Calcul VaR historique Utilities 95% et 99% 
Gafam_sector["VaR (historique) à 95%"] = -np.percentile(gafam_total_log_return, 5)
Gafam_sector["VaR (historique) à 99%"] = -np.percentile(gafam_total_log_return, 1)
Utilities_sector["VaR (historique) à 95%"] = -np.percentile(Utilities_total_log_return, 5)
Utilities_sector["VaR (historique) à 99%"] = -np.percentile(Utilities_total_log_return, 1)



# ────────────────────────────────────────────────────────────────  
# 5. INTERVALLES DE CONFIANCE SUR LA MOYENNE  
# ────────────────────────────────────────────────────────────────  

alpha = 0.05  # niveau de confiance 95%
z = norm.ppf(1 - alpha/2)  # quantile de la loi normale

# Gafam  
mean_gafam = Gafam_sector["Mean"].values[0]
std_gafam = Gafam_sector["Std"].values[0]
n_gafam = gafam_total_log_return.shape[0]
margin_error_gafam = z * (std_gafam / (n_gafam**0.5))
IC_left_gafam = mean_gafam - margin_error_gafam
IC_right_gafam = mean_gafam + margin_error_gafam
print(f"Intervalle de confiance à 95% Gafam : [{IC_left_gafam:.6f} ; {IC_right_gafam:.6f}]")
print(f"Marge d'erreur Gafam : {margin_error_gafam:.6f}")

# Utilities  
mean_utilities = Utilities_sector["Mean"].values[0]
std_utilities = Utilities_sector["Std"].values[0]
n_utilities = Utilities_total_log_return.shape[0]
margin_error_utilities = z * (std_utilities / (n_utilities**0.5))
IC_left_utilities = mean_utilities - margin_error_utilities
IC_right_utilities = mean_utilities + margin_error_utilities
print(f"Intervalle de confiance à 95% Utilities : [{IC_left_utilities:.6f} ; {IC_right_utilities:.6f}]")
print(f"Marge d'erreur Utilities : {margin_error_utilities:.6f}")

# ────────────────────────────────────────────────────────────────  
# 6. VISUALISATIONS : DISTRIBUTIONS & VaR  
# ────────────────────────────────────────────────────────────────  

density_gafam = np.arange(gafam_total_log_return.min() - 0.001, gafam_total_log_return.max() + 0.001, 0.001)
density_utilities = np.arange(Utilities_total_log_return.min() - 0.001, Utilities_total_log_return.max() + 0.001, 0.001)

gafam_pdf = norm.pdf(density_gafam, Gafam_sector["Mean"], Gafam_sector["Std"])
gafam_cdf = norm.cdf(density_gafam, Gafam_sector["Mean"], Gafam_sector["Std"])
utilities_pdf = norm.pdf(density_utilities, Utilities_sector["Mean"], Utilities_sector["Std"])
utilities_cdf = norm.cdf(density_utilities, Utilities_sector["Mean"], Utilities_sector["Std"])

plt.figure(figsize=(10, 5))

# Histogramme des rendements GAFAM avec PDF normale
plt.subplot(2, 2, 1)
plt.hist(gafam_total_log_return, bins=100, density=True, color="skyblue", alpha=0.6, label="Rendements GAFAM")
plt.plot(density_gafam, gafam_pdf, label="PDF Normale", color="blue")
plt.title("Histogramme & PDF des Rendements GAFAM")
plt.xlabel("Rendement Logarithmique")
plt.ylabel("Densité")
plt.legend()

# Histogramme des rendements Utilities avec PDF normale
plt.subplot(2, 2, 2)
plt.hist(Utilities_total_log_return, bins=100, density=True, color="skyblue", alpha=0.6, label="Rendements Utilities")
plt.plot(density_utilities, utilities_pdf, label="PDF Normale", color="green")
plt.title("Histogramme & PDF des Rendements Utilities")
plt.xlabel("Rendement Logarithmique")
plt.ylabel("Densité")
plt.legend()

# CDF des rendements GAFAM avec lignes VaR 95% et 99% (normale + historique)
plt.subplot(2, 2, 3)
plt.plot(density_gafam, gafam_cdf, label="CDF GAFAM", color="blue")
plt.axvline(Gafam_sector["VaR (normale) à 95%"].values[0], color="orange", linestyle="--", label="VaR Normale 95%")
plt.axvline(Gafam_sector["VaR (normale) à 99%"].values[0], color="red", linestyle="--", label="VaR Normale 99%")
plt.axvline(-Gafam_sector["VaR (historique) à 95%"].values[0], color="orange", linestyle=":", label="VaR Historique 95%")
plt.axvline(-Gafam_sector["VaR (historique) à 99%"].values[0], color="red", linestyle=":", label="VaR Historique 99%")
plt.title("Fonction de Répartition (CDF) GAFAM avec VaR")
plt.xlabel("Rendement Logarithmique")
plt.ylabel("Probabilité cumulée")
plt.legend()

# CDF des rendements Utilities avec lignes VaR 95% et 99% (normale + historique)
plt.subplot(2, 2, 4)
plt.plot(density_utilities, utilities_cdf, label="CDF Utilities", color="green")
plt.axvline(Utilities_sector["VaR (normale) à 95%"].values[0], color="orange", linestyle="--", label="VaR Normale 95%")
plt.axvline(Utilities_sector["VaR (normale) à 99%"].values[0], color="red", linestyle="--", label="VaR Normale 99%")
plt.axvline(-Utilities_sector["VaR (historique) à 95%"].values[0], color="orange", linestyle=":", label="VaR Historique 95%")
plt.axvline(-Utilities_sector["VaR (historique) à 99%"].values[0], color="red", linestyle=":", label="VaR Historique 99%")
plt.title("Fonction de Répartition (CDF) Utilities avec VaR")
plt.xlabel("Rendement Logarithmique")
plt.ylabel("Probabilité cumulée")
plt.legend()

plt.tight_layout()
plt.show()


# ────────────────────────────────────────────────────────────────  
# 7. COMPARAISON DIRECTE DES VaR 95% et 99% ENTRE SECTEURS  
# ────────────────────────────────────────────────────────────────  

plt.figure(figsize=(10, 5))

plt.plot(density_gafam, gafam_cdf, label="CDF GAFAM", color="purple")
plt.axvline(Gafam_sector["VaR (normale) à 99%"].values[0], color="purple", linestyle="--", label="VaR Normale 99% GAFAM")
plt.axvline(-Gafam_sector["VaR (historique) à 99%"].values[0], color="purple", linestyle=":", label="VaR Historique 99% GAFAM")
plt.axvline(Gafam_sector["VaR (normale) à 95%"].values[0], color="orange", linestyle="--", label="VaR Normale 95% GAFAM")
plt.axvline(-Gafam_sector["VaR (historique) à 95%"].values[0], color="orange", linestyle=":", label="VaR Historique 95% GAFAM")

plt.plot(density_utilities, utilities_cdf, label="CDF Utilities", color="green")
plt.axvline(Utilities_sector["VaR (normale) à 99%"].values[0], color="green", linestyle="--", label="VaR Normale 99% Utilities")
plt.axvline(-Utilities_sector["VaR (historique) à 99%"].values[0], color="green", linestyle=":", label="VaR Historique 99% Utilities")
plt.axvline(Utilities_sector["VaR (normale) à 95%"].values[0], color="red", linestyle="--", label="VaR Normale 95% Utilities")
plt.axvline(-Utilities_sector["VaR (historique) à 95%"].values[0], color="red", linestyle=":", label="VaR Historique 95% Utilities")

plt.title("Comparaison des VaR Normale & Historique (95% & 99%) entre GAFAM et Utilities")
plt.xlabel("Rendement Logarithmique")
plt.ylabel("Probabilité cumulée")
plt.legend()
plt.grid(True)
plt.show()



print( Gafam_sector["VaR (historique) à 95%"] )