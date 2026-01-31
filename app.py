import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="The Raven's Deck", page_icon="✒️", layout="centered")

# --- EDGAR ALLAN POE / VICTORIAN STEAMPUNK STYLING ---
st.markdown("""
<style>
    /* Importing fonts: IM Fell for old book feel, La Belle Aurore for quill handwriting */
    @import url('https://fonts.googleapis.com/css2?family=IM+Fell+English+SC&family=La+Belle+Aurore&family=Special+Elite&display=swap');

    .stApp {
        background-color: #12100e;
        background-image: url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #c5b358; /* Aged Gold */
    }
    
    .card-box {
        background-color: #e8dcc4; /* Tea-stained paper */
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 60px 20px;
        border-radius: 2px;
        border: 2px solid #3d2b1f;
        outline: 10px double #5d4037; /* Ornate outer frame */
        outline-offset: -20px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.7);
    }

    /* Poe-esque Card Name: Elegant but haunting old book font */
    .card-name {
        font-family: 'IM Fell English SC', serif;
        font-size: 65px;
        color: #1a1a1a;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }

    /* Handwriting style for "Number of Suit" */
    .card-meta {
        font-family: 'IM Fell English SC', bold;
        font-size: 32px;
        color: #4a3728;
        margin-top: 0px;
    }

    /* Steampunk Operative Button */
    .stButton>button {
        background: #2c251e !important;
        color: #c5b358 !important;
        border: 1px solid #c5b358 !important;
        font-family: 'Special Elite', cursive !important;
        border-radius: 0px !important;
        padding: 10px 25px !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background: #c5b358 !important;
        color: #12100e !important;
    }

    h1 {
        font-family: 'IM Fell English SC', serif;
        color: #c5b358;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("✒️ The Tarokka Ledger")
st.write("Consult the mechanical oracle to reveal your dark reflection...")

# --- LOAD DATA ---
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip() for c in df.columns]
        
        if st.button("CONSULT THE VOID", use_container_width=True):
            card = df.sample(n=1).iloc[0]
            
            # Extract data
            name = card.get('Card Name', 'Unknown')
            suit = card.get('Suit', 'High Deck')
            prompt = card.get('Image Prompt', 'The pages are blank...')
            num = card.get('Card Number', '')

            # Logic for "Number of Suit" or "High Deck"
            if pd.notna(num) and num != '' and pd.notna(suit):
                try:
                    num_val = int(float(num))
                    meta_display = f"{num_val} of {suit}"
                except:
                    meta_display = f"{num} of {suit}"
            else:
                # For High Deck cards which usually don't have numbers
                meta_display = f"from the {suit}"

            # Display the "Card"
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-name">{name}</div>
                    <div class="card-meta">{meta_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Descriptive text in a typewriter style
            with st.expander("The Prophet's Notes"):
                st.markdown(f"<div style='font-family:\"Special Elite\"; color:#d4af37;'>{prompt}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"The gears have jammed: {e}")

else:
    st.info("The ledger is empty. Please provide the Tarokka CSV.")
