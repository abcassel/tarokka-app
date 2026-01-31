import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Tarokka Dealer", page_icon="🔮", layout="centered")

# --- GOTHIC & SCARY STYLING ---
# We import 'Creepster' from Google Fonts for that horror look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');

    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    
    .card-box {
        background-color: #1a1a1a;
        padding: 60px 20px;
        border-radius: 10px;
        border: 1px solid #444;
        border-left: 5px solid #8b0000; /* Blood red accent */
        text-align: center;
        margin-top: 30px;
        box-shadow: 0px 0px 25px 5px rgba(139,0,0,0.2);
    }

    .card-name {
        font-family: 'Creepster', system-ui;
        font-size: 80px;
        color: #ff4b4b;
        text-shadow: 4px 4px 8px #000000;
        line-height: 1.1;
        margin-bottom: 20px;
    }

    .card-meta {
        font-family: 'Courier New', Courier, monospace;
        font-size: 22px; /* Unified size for Suit and Number */
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* Styling the button to look more ritualistic */
    .stButton>button {
        background-color: #8b0000 !important;
        color: white !important;
        border: none !important;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔮 The Tarokka Oracle")
st.write("Draw a card to seal your fate...")

# --- LOAD DATA ---
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip() for c in df.columns]
        
        if st.button("🎴 REVEAL THE CARD", use_container_width=True):
            card = df.sample(n=1).iloc[0]
            
            # Extract data
            name = card.get('Card Name', 'Unknown')
            suit = card.get('Suit', 'High Deck')
            prompt = card.get('Image Prompt', 'The mists reveal nothing.')
            num = card.get('Card Number', '')

            # Logic for clean display
            suit_text = str(suit) if pd.notna(suit) else "High Deck"
            
            # Format number and suit together
            if pd.notna(num) and num != '':
                # If it's a whole number like 1.0, convert to 1
                try:
                    num_val = int(float(num))
                    meta_display = f"{suit_text} — {num_val}"
                except:
                    meta_display = f"{suit_text} — {num}"
            else:
                meta_display = f"{suit_text}"

            # Display the "Card"
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-name">{name}</div>
                    <div class="card-meta">{meta_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Flavor text
            with st.expander("Interpret the Omen"):
                st.markdown(f"*{prompt}*")

    except Exception as e:
        st.error(f"The mists are clouded: {e}")

else:
    st.info("The deck is empty. Upload your Tarokka CSV to begin the reading.")
