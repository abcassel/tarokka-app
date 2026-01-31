import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="The Strahd Ledger", page_icon="🍷", layout="centered")

# --- EDGAR ALLAN POE / STEAMPUNK STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=La+Belle+Aurore&family=Special+Elite&display=swap');

    .stApp {
        background-color: #12100e;
        background-image: url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #c5b358;
    }
    
    .card-box {
        background-color: #e8dcc4; 
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 50px 20px;
        border: 1px solid #3d2b1f;
        outline: 8px double #5d4037;
        outline-offset: -15px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8);
    }

    .card-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 70px;
        color: #1a1a1a;
        line-height: 1;
        margin-bottom: 5px;
        font-weight: 600;
    }

    .card-meta {
        font-family: 'La Belle Aurore', cursive;
        font-size: 32px;
        color: #4a3728;
        margin-top: 0px;
    }

    .lore-container {
        margin-top: 40px;
        padding: 30px;
        background: rgba(20, 15, 10, 0.8);
        border-left: 4px solid #8b0000;
        font-family: 'Special Elite', cursive;
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.5);
    }

    .lore-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 30px;
        color: #8b0000;
        font-style: italic;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 3px;
        border-bottom: 1px solid #3d2b1f;
        display: inline-block;
    }

    .lore-text {
        color: #d4c4a8;
        font-size: 19px;
        line-height: 1.6;
    }

    .stButton>button {
        background: #2c251e !important;
        color: #c5b358 !important;
        border: 1px solid #c5b358 !important;
        font-family: 'Special Elite', cursive !important;
        border-radius: 0px !important;
        transition: 0.3s;
        height: 3em;
        font-size: 18px !important;
    }
    
    .stButton>button:hover {
        background: #c5b358 !important;
        color: #12100e !important;
        box-shadow: 0px 0px 15px #c5b358;
    }
</style>
""", unsafe_allow_html=True)

st.title("🐦‍⬛ The Tarokka")

# --- LOAD DATA ---
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Load and clean headers immediately
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip().lower() for c in df.columns] # Force everything to lowercase and clean
        
        if st.button("Draw a card", use_container_width=True):
            card = df.sample(n=1).iloc[0]
            
            # Extract data using lowercase keys
            name = card.get('card name', 'Unknown Card')
            suit = card.get('suit', 'High Deck')
            
            # This looks specifically for your 'lore' column
            lore_content = card.get('lore', 'The ink has faded from this section of the ledger.')
            
            num = card.get('card number', '')

            # Format "Number of Suit"
            if pd.notna(num) and num != '' and pd.notna(suit) and str(suit).lower() != 'high':
                try:
                    num_val = int(float(num))
                    meta_display = f"{num_val} of {suit}"
                except:
                    meta_display = f"{num} of {suit}"
            else:
                meta_display = f"from the {suit}"

            # 1. Display the Card
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-name">{name}</div>
                    <div class="card-meta">{meta_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 2. Display Lore of Strahd
            st.markdown(f"""
                <div class="lore-container">
                    <div class="lore-title">Lore of Strahd</div>
                    <div class="lore-text">{lore_content}</div>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Uncertainty abounds: {e}")
else:
    st.info("The ledger is empty. Please upload your Tarokka CSV in the sidebar.")
