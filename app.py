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
        # 1. Configuration
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 2. CHARGEMENT DES DONNÉES
        try:
            df_context = pd.read_csv("master_fusion_golden_journey.csv").head(5).to_string()
        except:
            df_context = "Données indisponibles."

        # 3. AUTO-DÉTECTION DU MODÈLE (La solution au bug 404)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return "Aucun modèle de génération trouvé pour cette clé API."
        
        # On choisit le meilleur modèle disponible (Flash 1.5 de préférence, sinon le premier de la liste)
        selected_model_name = next((m for m in available_models if "1.5-flash" in m), available_models[0])
        
        model = genai.GenerativeModel(selected_model_name)

        # 4. LE PROMPT
        prompt = f"""
        Tu es l'IA de luxe "Golden Journey". 
        Ton rôle est de créer une expérience fluide entre Vol, Voiture et Soin.
        DONNÉES : {df_context}
        CLIENT : {user_input}
        Réponds avec élégance, luxe et précision.
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Erreur système (Modèle utilisé: {selected_model_name if 'selected_model_name' in locals() else 'Aucun'}) : {str(e)}"

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
