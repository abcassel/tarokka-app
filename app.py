import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Tarokka Automaton", page_icon="⚙️", layout="centered")

# --- STEAMPUNK VICTORIAN STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Special+Elite&display=swap');

    /* Background: Deep Charcoal/Leather */
    .stApp {
        background-color: #1b1713;
        background-image: radial-gradient(#2c251e 1px, transparent 1px);
        background-size: 20px 20px;
        color: #d4af37; /* Brass Gold */
    }
    
    /* The Card Container: Parchment with Brass Border */
    .card-box {
        background-color: #f4e4bc; /* Aged Paper */
        background-image: url("https://www.transparenttextures.com/patterns/pinstriped-dark.png");
        padding: 50px 20px;
        border-radius: 5px;
        border: 8px double #8b5a2b; /* Bronze Double Border */
        text-align: center;
        margin-top: 30px;
        box-shadow: 0px 0px 20px 2px rgba(0,0,0,0.8), inset 0px 0px 50px rgba(139,90,43,0.3);
    }

    /* Gothic Victorian Card Name */
    .card-name {
        font-family: 'UnifrakturMaguntia', serif;
        font-size: 75px;
        color: #2e1a05; /* Deep Ink */
        line-height: 1;
        margin-bottom: 15px;
    }

    /* Steampunk Metadata (Typewriter style) */
    .card-meta {
        font-family: 'Special Elite', cursive;
        font-size: 24px;
        color: #5d4037;
        text-transform: uppercase;
        border-top: 1px solid #8b5a2b;
        display: inline-block;
        padding-top: 10px;
        margin-top: 5px;
    }

    /* Steampunk Button: Brass/Copper */
    .stButton>button {
        background: linear-gradient(180deg, #b8860b 0%, #8b5a2b 100%) !important;
        color: #fff !important;
        border: 2px solid #5d4037 !important;
        font-family: 'Special Elite', cursive !important;
        font-size: 20px !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #000;
    }
    
    .stButton>button:active {
        box-shadow: 0px 0px 0px #000 !important;
        transform: translateY(2px);
    }

    h1 {
        font-family: 'UnifrakturMaguntia', serif;
        color: #d4af37;
        text-align: center;
        font-size: 50px;
    }
</style>
""", unsafe_allow_html=True)

st.title("The Tarokka")
st.write("Fortune has a message for you...")

# --- LOAD DATA ---
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip() for c in df.columns]
        
        if st.button("DRAW A CARD", use_container_width=True):
            card = df.sample(n=1).iloc[0]
            
            # Extract data
            name = card.get('Card Name', 'Unknown')
            suit = card.get('Suit', 'High Deck')
            prompt = card.get('Image Prompt', 'The automaton remains silent.')
            num = card.get('Card Number', '')

            # Logic for clean display
            suit_text = str(suit) if pd.notna(suit) else "High Deck"
            
            # Format number and suit together
            if pd.notna(num) and num != '':
                try:
                    num_val = int(float(num))
                    meta_display = f"{suit_text} • No. {num_val}"
                except:
                    meta_display = f"{suit_text} • {num}"
            else:
                meta_display = f"{suit_text}"

            # Display the "Card"
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-name">{name}</div>
                    <div class="card-meta">{meta_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Steampunk style expander
            with st.expander("Read the Brass Plates"):
                st.markdown(f"***{prompt}***")

    except Exception as e:
        st.error(f"Mechanical failure: {e}")

else:
    st.info("The apparatus requires a data input. Upload your Tarokka CSV.")
