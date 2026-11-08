import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Golden Journey Concierge", page_icon="✈", layout="wide")

# --- STYLE (luxury look: dark background, gold accents) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;500;600&display=swap');

    /* Background image with a dark overlay */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.72), rgba(0,0,0,0.78)),
                    url('https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Montserrat', sans-serif;
    }

    /* Gold title */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #d4af37 !important;
        font-size: 4rem !important;
        letter-spacing: 5px !important;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 0 !important;
    }

    /* Hide the Streamlit menu, header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* White text */
    .stMarkdown p, label, .stRadio label p { color: white !important; }
    .subtitle { text-align: center; font-size: 1.15rem; color: #e8e2cf !important; }
    .poles { text-align: center; color: #d4af37 !important; letter-spacing: 4px; font-size: .9rem; text-transform: uppercase; }

    /* Text area */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid #d4af37 !important;
        border-radius: 0 !important;
    }

    /* Gold button */
    .stButton>button {
        background-color: transparent !important;
        color: #d4af37 !important;
        border: 2px solid #d4af37 !important;
        border-radius: 0px !important;
        width: 100%;
        font-weight: bold;
        letter-spacing: 2px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #d4af37 !important;
        color: black !important;
    }

    /* Small data cards */
    .kpi { border: 1px solid rgba(212,175,55,.5); padding: 14px; text-align: center; background: rgba(0,0,0,.45); }
    .kpi b { display: block; color: #d4af37; font-size: 1.6rem; font-family: 'Playfair Display', serif; }
    .kpi span { color: #e8e2cf; font-size: .8rem; }

    /* Answer box */
    .answer { border: 1px solid #d4af37; padding: 24px; margin-top: 20px; background: rgba(0,0,0,0.6); color: white; line-height: 1.7; }
    </style>
    """, unsafe_allow_html=True)


# --- DATA ---
@st.cache_data
def load_data():
    """Load the merged dataset (aviation + automotive + luxury reviews)."""
    return pd.read_csv("master_fusion_golden_journey.csv")


# Customer profiles -> flight classes available in the dataset
PROFILES = {
    "Étudiant · petit budget": ["Eco"],
    "Voyageur · budget moyen": ["Eco Plus", "Eco"],
    "Premium · sans contrainte": ["Business"],
}


def select_context(df, profile, n=6):
    """Keep the packages that match the profile, best comfort scores first, with shortened reviews."""
    subset = df[df["Flight_Class"].isin(PROFILES[profile])].copy()
    subset["Comfort"] = subset["Flight_Wifi_Score"] + subset["Flight_Leg_Room"]
    subset = subset.sort_values("Comfort", ascending=False).head(n)
    rows = []
    for _, r in subset.iterrows():
        rows.append(
            f"- Package {r.Package_ID} | Classe {r.Flight_Class} | Wifi {r.Flight_Wifi_Score}/5 | "
            f"Espace jambes {r.Flight_Leg_Room}/5 | Avis voiture : {str(r.Car_Review)[:220]} | "
            f"Avis soin/luxe : {str(r.Luxe_Review)[:160]}"
        )
    return subset, "\n".join(rows)


# --- AI ---
def pick_model():
    """Pick an available Gemini model that supports text generation (prefers the fast 'flash' models)."""
    models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
    if not models:
        return None
    flash = [m for m in models if "flash" in m and "thinking" not in m and "image" not in m]
    return (flash or models)[0]


def get_ai_response(user_input, profile, context):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model_name = pick_model()
        if not model_name:
            return "Aucun modèle de génération disponible pour cette clé API."
        model = genai.GenerativeModel(model_name)
        prompt = f"""
        Tu es "Golden Journey", un concierge de voyage haut de gamme.
        Tu proposes un parcours complet et cohérent : vol, transfert en voiture, puis moment de soin ou de luxe.
        Profil du client : {profile}
        Packages disponibles (issus de nos données) :
        {context}
        Demande du client : {user_input}
        Choisis le package le plus adapté, cite son numéro, explique ton choix en t'appuyant sur les scores
        et les avis, puis décris le parcours en 3 étapes (Vol, Transfert, Luxe). Ton élégant et précis, en français.
        """
        return model.generate_content(prompt).text
    except KeyError:
        return "Clé API manquante : ajoutez GEMINI_API_KEY dans les secrets de l'application."
    except Exception as e:
        return f"Erreur système : {e}"


# --- INTERFACE ---
st.markdown("<h1>Golden Journey</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>L'excellence du voyage prédite par la Data Science.</p>", unsafe_allow_html=True)
st.markdown("<p class='poles'>Aviation · Automobile · Luxe</p>", unsafe_allow_html=True)

df = load_data()
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    profile = st.radio("Votre profil", list(PROFILES.keys()), horizontal=True)
    subset, context = select_context(df, profile)

    # Quick view of the data behind the recommendation
    k1, k2, k3 = st.columns(3)
    k1.markdown(f"<div class='kpi'><b>{len(df)}</b><span>packages analysés</span></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi'><b>{subset['Flight_Wifi_Score'].mean():.1f}/5</b><span>Wifi · packages retenus</span></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi'><b>{subset['Flight_Leg_Room'].mean():.1f}/5</b><span>Espace · packages retenus</span></div>", unsafe_allow_html=True)

    user_input = st.text_area(
        "Votre demande",
        placeholder="Décrivez vos envies (ex : je suis pressé, je veux du sport et un moment de détente à l'arrivée)...",
    )
    if st.button("ACTIVER LE SYSTÈME PRÉDICTIF"):
        if user_input.strip():
            with st.spinner("Analyse des flux de données..."):
                answer = get_ai_response(user_input, profile, context)
            st.markdown(f"<div class='answer'>{answer}</div>", unsafe_allow_html=True)
        else:
            st.warning("Décrivez d'abord votre demande.")

    with st.expander("Voir les données utilisées pour ce profil"):
        st.dataframe(subset[["Package_ID", "Flight_Class", "Flight_Wifi_Score", "Flight_Leg_Room"]], hide_index=True)
