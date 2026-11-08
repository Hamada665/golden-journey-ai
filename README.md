# Golden Journey AI

Projet data science (EST Salé) : un concierge de voyage qui recommande un parcours complet (vol, transfert, luxe) selon le profil du client.

- Données : 3 jeux de données Kaggle (aviation, automobile, luxe) nettoyés et fusionnés sous Google Colab (`master_fusion_golden_journey.csv`, 500 packages).
- Recommandation : sélection des packages selon le profil, puis génération de la réponse avec l'API Gemini.
- Interface : Streamlit.

Lancer en local : `pip install -r requirements.txt`, puis créer `.streamlit/secrets.toml` avec `GEMINI_API_KEY = "..."`, puis `streamlit run app.py`.
