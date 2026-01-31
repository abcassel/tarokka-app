import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Tarokka Dealer", page_icon="🃏", layout="centered")

# --- GOTHIC STYLING ---
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    .card-box {
        background-color: #2d2d2d;
        padding: 50px;
        border-radius: 15px;
        border: 2px solid #ff4b4b;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .card-name {
        font-family: 'Georgia', serif;
        font-size: 60px;
        font-weight: bold;
        color: #ff4b4b;
        text-transform: uppercase;
        letter-spacing: 5px;
    }
    .card-suit {
        font-size: 24px;
        color: #888888;
        font-style: italic;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔮 Tarokka Card Dealer")
st.write("Click the button below to draw a card from the deck.")

# --- LOAD DATA ---
# This looks for the file you uploaded to GitHub or the one you provide via uploader
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if st.button("🎴 DRAW A CARD", use_container_width=True):
        # Pick a random card
        card = df.sample(n=1).iloc[0]
        
        # Determine labels
        name = card['Card Name']
        suit = card['Suit'] if pd.notna(card['Suit']) else "High Deck"
        num = f" ({int(card['Card Number'])})" if pd.notna(card['Card Number']) else ""

        # Display the "Card"
        st.markdown(f"""
            <div class="card-box">
                <div class="card-name">{name}</div>
                <div class="card-suit">{suit}{num}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Optional: Show the prompt as a sub-text for flavor
        with st.expander("View Card Description"):
            st.write(card['Image Prompt'])

else:
    st.info("Please upload your Tarokka CSV file in the sidebar to begin.")
