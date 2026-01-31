import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="The Strahd Ledger", page_icon="🍷", layout="centered")

# --- STYLING: UNIFIED EDGAR ALLAN POE + STEAMPUNK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=La+Belle+Aurore&family=Special+Elite&display=swap');

    /* Main Page Background */
    .stApp {
        background-color: #12100e;
        background-image: url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #c5b358;
    }
    
    /* Shared Box Style for Card and Lore */
    .ledger-box {
        background-color: #e8dcc4; 
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 40px 25px;
        border: 1px solid #3d2b1f;
        outline: 8px double #5d4037;
        outline-offset: -15px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8);
    }

    /* Card Section Specifics */
    .card-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 65px;
        color: #1a1a1a;
        line-height: 1;
        margin-bottom: 5px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .card-meta {
        font-family: 'La Belle Aurore', cursive;
        font-size: 34px;
        color: #4a3728;
        font-weight: bold;
    }

    /* Lore Section Specifics */
    .lore-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 35px;
        color: #8b0000; /* Dried Blood Red */
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 15px;
        border-bottom: 1px solid #3d2b1f;
        display: inline-block;
    }

    .lore-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 22px;
        color: #2e1a05; /* Ink color */
        line-height: 1.4;
        font-style: italic;
        text-align: center;
        padding: 0 20px;
    }

    /* Steampunk Button */
    .stButton>button {
        background: #2c251e !important;
        color: #c5b358 !important;
        border: 1px solid #c5b358 !important;
        font-family: 'Special Elite', cursive !important;
        border-radius: 0px !important;
        transition: 0.3s;
        height: 3.5em;
        font-size: 18px !important;
        width: 100%;
        margin-top: 20px;
    }
    
    .stButton>button:hover {
        background: #c5b358 !important;
        color: #12100e !important;
        box-shadow: 0px 0px 15px #c5b358;
    }
</style>
""", unsafe_allow_html=True)

st.title("🐦‍⬛ The Tarokka")

# --- DATA PROCESSING ---
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip().lower() for c in df.columns]
        
        if st.button("Draw a card..."):
            card = df.sample(n=1).iloc[0]
            
            # Fetch data
            name = card.get('card name', 'Unknown Card')
            suit = card.get('suit', 'High Deck')
            lore_text = card.get('lore', 'The ink has faded from this section...')
            num = card.get('card number', '')

            # Logic for "X of Y"
            if pd.notna(num) and str(num).strip() != '' and str(suit).lower() != 'high':
                try:
                    num_val = int(float(num))
                    meta_display = f"{num_val} of {suit}"
                except:
                    meta_display = f"{num} of {suit}"
            else:
                meta_display = f"from the {suit}"

            # 1. Display the Card Information
            st.markdown(f"""
                <div class="ledger-box">
                    <div class="card-name">{name}</div>
                    <div class="card-meta">{meta_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 2. Display Lore Section (Same Box Style)
            st.markdown(f"""
                <div class="ledger-box">
                    <div class="lore-title">Lore of Strahd</div>
                    <div class="lore-text">"{lore_text}"</div>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"A mechanical gear has snapped: {e}")
else:
    st.info("The ledger is empty. Upload your Tarokka CSV in the sidebar.")
