# 📊 Analyse Sectorielle : GAFAM vs Utilities – Performance & Risque

Ce projet vise à comparer deux secteurs – **les Big Tech (GAFAM)** et **les Utilities** – à travers une approche quantitative.

> 🎯 Objectifs :
> - Télécharger des données de marché avec `yfinance` et les manipuler (pandas,numpy)
> - Calculer des indicateurs statistiques : rendement, volatilité, asymétrie (skew), aplatissement (kurtosis), Value at Risk (VaR)
> - Comparer les secteurs via des visualisations (matplotlib) et outils statistiques (scipy.stats) adaptés à la finance de marché

---

## 📁 Contenu du dépôt

- `gafam-vs-utilities-risk-analysis.py`  
  → Script Python détaillé et documenté, structuré par étapes pédagogiques :  
  - Téléchargement de données
  - Analyse des principau indiacteurs statistiques (mean,std,skewness et kurtosis)
  - Calcul de VaR (historique vs normale)
  - Intervalles de confiance
  - Visualisations professionnelles avec `matplotlib`

- `gafam-vs-utilities-risk-analysis_app.py`  
  → Version **interactive** du projet sous **Streamlit**, permettant une exploration plus dynamique.  
  > ℹ️ *Note personnelle 1* : je découvre encore Streamlit, et cette interface a été co-construite avec l'aide d'une IA pour structurer l'expérience utilisateur. L’accent est mis sur l’analyse, pas sur le design technique de l’app.
  > ℹ️ *Note personnelle 2* : Pour executer l'app => ```bash => streamlit run risk_app.py

---

## 🔍 Méthodologie & Indicateurs

| Métrique        | Description                                                                 |
|-----------------|-------------------------------------------------------------------------------|
| `Mean`          | Rendement logarithmique moyen par titre / par secteur                        |
| `Standard Deviation` | Volatilité quotidienne                                                    |
| `Skewness`      | Mesure de l’asymétrie de la distribution                                      |
| `Kurtosis`      | Mesure de l’aplatissement / extrémités                                        |
| `VaR`           | Value at Risk à 95% et 99% – méthode **normale** et **historique**            |
| `Intervalle de confiance` | Zone probable de la moyenne à 95% de certitude                      |

---

## 📈 Visualisations intégrées

- Histogrammes + PDF normale
- Fonctions de répartition (CDF) + lignes de VaR (historique et normale)
- Comparaison directe entre les deux secteurs (GAFAM vs Utilities)


## Ce que ce projet dit de moi : 
Ce projet est plus qu’un simple exercice technique : il reflète ma capacité à mobiliser mes compétences data au service de problématiques financières concrètes. Voici ce qu’il vous montrera de moi :

🎯 Esprit analytique structuré : chaque étape du code est pensée comme un processus d’analyse rigoureuse, reproductible et interprétable.

📊 Solide compréhension des risques financiers : maîtrise des indicateurs clés (volatilité, VaR, distribution des rendements), pertinents pour les secteurs sensibles au risque.

🧠 Autonomie & curiosité : j’ai conçu ce projet seul, en consolidant mes acquis en finance quantitative et en Python via des ressources externes.

💡 Capacité à communiquer des résultats techniques de manière claire : les visualisations et commentaires sont orientés prise de décision, comme en entreprise ou en cabinet.

⚙️ Volonté de monter en compétence rapidement : même si je débute avec Streamlit, j’ai su construire une app interactive en m’appuyant intelligemment sur l’IA, preuve d’agilité.

📌 Si vous cherchez un profil hybride entre finance et data avec un mindset entrepreneurial : ce projet en est un bon reflet.

---

## ▶️ Exécution de l’app Streamlit

```bash
streamlit run risk_app.py
