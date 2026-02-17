import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Golden Journey | Luxury Concierge",
    page_icon="✨",
    layout="wide"
)

# --- STYLE CSS (Pour faire "Luxe") ---
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    h1 {color: #D4AF37; font-family: 'Helvetica Neue', sans-serif;} /* Couleur Or */
    .stButton>button {background-color: #D4AF37; color: white; border-radius: 5px;}
    .stTextInput>div>div>input {color: white;}
</style>
""", unsafe_allow_html=True)

# --- FONCTION : CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    # On charge le Master Dataset
    try:
        df = pd.read_csv("master_fusion_golden_journey.csv")
        return df
    except:
        return None

# --- FONCTION : L'INTELLIGENCE DU CHATBOT ---
def get_concierge_response(user_input, data_context, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # Modèle rapide et gratuit
        
        # Le Prompt (Les consignes données à l'IA)
        prompt = f"""
        Tu es "Aura", le concierge IA ultra-luxe du projet "Golden Journey".
        
        CONTEXTE :
        Nous créons une expérience fluide : Vol (Karima) -> Voiture Audi (Hajar) -> Soin (Malak).
        Voici un extrait de nos données combinées (Profils types) :
        {data_context}
        
        L'UTILISATEUR DIT : "{user_input}"
        
        TA MISSION :
        1. Analyse la demande (Humeur, besoin de calme, urgence ?).
        2. Propose un trajet complet (Type de vol, Modèle Audi, Type de soin).
        3. Si l'utilisateur est pressé/stressé : Propose du calme, une Audi autonome/silencieuse, un soin apaisant.
        4. Si l'utilisateur est énergique/business : Propose de l'efficacité, une Audi sportive (SQ5/TTS), un soin énergisant.
        5. Ton : Distingué, bref, empathique. Pas de phrases trop longues.
        
        Réponds directement au client maintenant.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erreur de connexion IA : {str(e)}"

# --- INTERFACE PRINCIPALE ---
def main():
    # En-tête avec logo (emoji pour l'instant)
    st.title("✨ THE GOLDEN JOURNEY")
    st.markdown("*L'Alliance de l'Aviation, de l'Automobile et du Soin.*")
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Votre Profil Voyageur")
        user_query = st.text_area("Dites-nous tout...", 
                                  "Ex: Je suis un businessman, je ne veux pas tarder et je déteste le calme. Je veux de la puissance.")
        
        launch_btn = st.button("Générer mon Expérience Golden")

        # Aperçu des données (pour montrer au prof que ça marche)
        with st.expander("Voir les données brutes (Debug)"):
            df = load_data()
            if df is not None:
                st.dataframe(df.head(3))
            else:
                st.error("Fichier CSV introuvable !")

    with col2:
        st.subheader("Votre Concierge IA")
        
        if launch_btn and user_query:
            # Récupération de la clé API depuis les "Secrets" de Streamlit
            api_key = st.secrets["GEMINI_API_KEY"]
            
            if not api_key:
                st.error("Clé API manquante dans les secrets.")
            else:
                with st.spinner('Analyse de vos biorythmes et préférences...'):
                    # On prend un échantillon de données pour le contexte
                    data_sample = load_data().head(5).to_string() if load_data() is not None else "Pas de données"
                    
                    # Appel IA
                    reponse = get_concierge_response(user_query, data_sample, api_key)
                    
                    # Affichage du résultat
                    st.success("Itinéraire prêt.")
                    st.markdown(f"**Aura :** {reponse}")
                    st.image("https://images.unsplash.com/photo-1563720223185-11003d516935", caption="Votre Audi vous attend.")

if __name__ == "__main__":
    main()
