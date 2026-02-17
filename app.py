import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIGURATION INITIALE ---
st.set_page_config(page_title="Golden Journey Concierge", layout="wide")

# --- INJECTION CSS (Le "Maquillage" de l'interface) ---
st.markdown("""
    <style>
    /* Import de la police Luxe */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

    /* Fond d'écran et style général */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80');
        background-size: cover;
    }

    /* Titre Doré */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #d4af37 !important;
        font-size: 4rem !important;
        letter-spacing: 5px !important;
        text-transform: uppercase;
        text-align: center;
    }

    /* Cacher le menu Streamlit en haut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Style du texte blanc */
    .stMarkdown p {
        color: white !important;
        font-size: 1.2rem;
        text-align: center;
    }

    /* Personnalisation du champ de texte */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid #d4af37 !important;
    }

    /* Bouton Doré */
    .stButton>button {
        background-color: transparent !important;
        color: #d4af37 !important;
        border: 2px solid #d4af37 !important;
        border-radius: 0px !important;
        width: 100%;
        font-weight: bold;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #d4af37 !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE IA ---
def get_ai_response(user_input):
    try:
        # 1. Chargement des données
        df_context = pd.read_csv("master_fusion_golden_journey.csv").head(5).to_string()
        
        # 2. Configuration
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 3. Liste des modèles à tester par ordre de préférence
        model_names = ['gemini-1.5-flash', 'gemini-pro']
        
        model = None
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                # Test rapide pour voir si le modèle répond
                test_prompt = "Dis ok"
                model.generate_content(test_prompt)
                break # Si ça marche, on garde celui-là
            except:
                continue
        
        if model is None:
            return "Erreur : Aucun modèle IA n'est accessible avec cette clé API."

        # 4. Le vrai Prompt
        prompt = f"""
        Tu es l'IA de luxe "Golden Journey". 
        Ton rôle est de créer une expérience fluide entre Vol, Voiture et Soin.
        
        DONNÉES : {df_context}
        
        CLIENT : {user_input}
        
        INSTRUCTIONS :
        - Analyse si le client est pressé, fatigué ou en quête de sportivité.
        - Propose une Audi spécifique et un soin spécifique tirés des données.
        - Ton : Très haut de gamme, court et efficace.
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Note du Concierge : Nous rencontrons une maintenance technique. (Détails : {str(e)})"

# --- INTERFACE ---
st.markdown("<h1>Golden Journey</h1>", unsafe_allow_html=True)
st.markdown("<p>L'excellence du voyage prédite par la Data Science.<br>Aviation | Audi | Luxe</p>", unsafe_allow_html=True)

# Centrage du contenu
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    user_input = st.text_area("", placeholder="Décrivez vos envies (ex: Je suis pressé, je veux du sport)...")
    if st.button("ACTIVER LE SYSTÈME PRÉDICTIF"):
        if user_input:
            with st.spinner("Analyse des flux de données..."):
                answer = get_ai_response(user_input)
                st.markdown(f"<div style='border: 1px solid #d4af37; padding: 20px; margin-top: 20px; background: rgba(0,0,0,0.5);'>{answer}</div>", unsafe_allow_html=True)
