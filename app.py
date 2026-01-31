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
st.write("Draw a card to reveal its name.")

# --- LOAD DATA ---
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Load the dataframe
        df = pd.read_csv(uploaded_file)
        
        # CLEANING STEP: Remove hidden spaces from column names
        df.columns = [c.strip() for c in df.columns]
        
        if st.button("🎴 DRAW A CARD", use_container_width=True):
            # Pick a random card
            card = df.sample(n=1).iloc[0]
            
            # Use .get() to avoid KeyErrors if a column is missing
            name = card.get('Card Name', 'Unknown Card')
            suit = card.get('Suit', 'High Deck')
            prompt = card.get('Image Prompt', 'No description available.')
            num = card.get('Card Number', '')
            
            # Format Suit text
            suit_display = f"{suit}" if pd.notna(suit) else "High Deck"
            num_display = f" ({int(num)})" if pd.notna(num) and num != '' else ""

            # Display the "Card"
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-name">{name}</div>
                    <div class="card-suit">{suit_display}{num_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Show the flavor text/prompt below
            with st.expander("View Card Description"):
                st.write(prompt)

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload your Tarokka CSV file in the sidebar to begin.")
