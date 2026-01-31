import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# --- CONFIGURATION ---
# In a real app, you would store this in Streamlit Secrets, not paste it directly.
# For now, the app will ask the user to input it for safety.
st.set_page_config(page_title="Tarokka Oracle", page_icon="🔮", layout="centered")

# --- CSS STYLING (Gothic Vibe) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #c9c9c9;
    }
    h1 {
        font-family: 'Courier New', Courier, monospace;
        color: #ff4b4b;
        text-align: center;
    }
    .card-title {
        font-size: 30px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
    }
    .card-info {
        font-size: 18px;
        color: #888888;
        text-align: center;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# --- APP LOGIC ---
def main():
    st.title("🔮 The Tarokka Oracle")
    st.write("Draw a card from the mists of Barovia and reveal its visage.")

    # 1. API Key Input (Sidebar)
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    
    # 2. File Uploader
    uploaded_file = st.sidebar.file_uploader("Upload your Tarokka CSV", type=["csv", "xlsx"])

    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to begin.")
        return

    if uploaded_file is None:
        st.info("Please upload the 'tarokka_deck.csv' file to the sidebar.")
        return

    # 3. Load Data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    # 4. The Draw Button
    if st.button("🎴 Draw a Card from the Deck", use_container_width=True):
        
        # Pick a random row
        card = df.sample(n=1).iloc[0]
        
        # Extract details
        card_name = card['Card Name']
        suit = card['Suit'] if pd.notna(card['Suit']) else "High Deck"
        prompt = card['Image Prompt']
        
        # Display Text Info
        st.markdown("---")
        st.markdown(f"<div class='card-title'>{card_name}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-info'>{suit}</div>", unsafe_allow_html=True)
        
        # 5. Generate Image
        client = OpenAI(api_key=api_key)
        
        with st.spinner(f"Summoning the image of the {card_name}..."):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = response.data[0].url
                st.image(image_url, caption=prompt, use_column_width=True)
                
            except Exception as e:
                st.error(f"The mists are too thick (API Error): {e}")

if __name__ == "__main__":
    main()
