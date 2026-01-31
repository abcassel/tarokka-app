import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="The Strahd Ledger", page_icon="🍷", layout="centered")

# --- STYLING: POE + STEAMPUNK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=La+Belle+Aurore&family=Special+Elite&display=swap');

    .stApp {
        background-color: #12100e;
        background-image: url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #c5b358;
    }
    
    .ledger-box {
        background-color: #e8dcc4; 
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 30px 25px;
        border: 1px solid #3d2b1f;
        outline: 8px double #5d4037;
        outline-offset: -15px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8);
    }

    /* Victorian Daguerreotype Frame for Top Image */
    .image-container {
        border: 12px double #8b5a2b;
        padding: 10px;
        background-color: #2c251e;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.9);
        margin-bottom: 25px;
    }

    .card-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 60px;
        color: #1a1a1a;
        line-height: 1.1;
        font-weight: 600;
        text-transform: uppercase;
    }

    .card-meta {
        font-family: 'La Belle Aurore', cursive;
        font-size: 34px;
        color: #4a3728;
        font-weight: bold;
    }

    .lore-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 32px;
        color: #8b0000;
        text-transform: uppercase;
        letter-spacing: 4px;
        border-bottom: 1px solid #3d2b1f;
        display: inline-block;
        margin-bottom: 15px;
    }

    .lore-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 22px;
        color: #2e1a05;
        line-height: 1.5;
        font-style: italic;
    }

    .stButton>button {
        background: #2c251e !important;
        color: #c5b358 !important;
        border: 1px solid #c5b358 !important;
        font-family: 'Special Elite', cursive !important;
        border-radius: 0px !important;
        height: 4em;
        width: 100%;
        font-size: 18px !important;
        letter-spacing: 2px;
    }
    
    .stButton>button:hover {
        background: #c5b358 !important;
        color: #12100e !important;
        box-shadow: 0px 0px 15px #c5b358;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍷 The Tarokka Ledger")

# --- DATA PROCESSING ---
uploaded_file = st.sidebar.file_uploader("Upload Tarokka CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip().lower() for c in df.columns]
        
        if st.button("CONSULT THE MECHANICAL ORACLE"):
            card = df.sample(n=1).iloc[0]
            
            # Fetch data
            name = card.get('card name', 'Unknown Card')
            suit = card.get('suit', 'High Deck')
            lore_text = card.get('lore', 'The ink has faded from this section...')
            num = card.get('card number', '')
            # Column F is index 5
            image_val = card.iloc[5] if len(card) >= 6 else None

            # 1. DISPLAY IMAGE AT THE VERY TOP
            if pd.notna(image_val) and str(image_val).strip() != "":
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(image_val, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # 2. DISPLAY CARD NAME & NUMBER
            if pd.notna(num) and str(num).strip() != '' and str(suit).lower() != 'high':
                try:
                    num_val = int(float(num))
                    meta_display = f"{num_val} of {suit}"
                except:
                    meta_display = f"{num} of {suit}"
            else:
                meta_display = f"from the {suit}"

            st.markdown(f"""
                <div class="ledger-box">
                    <div class="card-name">{name}</div>
                    <div class="card-meta">{meta_display}</div>
                </div>
            """, unsafe_allow_html=True)

            # 3. DISPLAY LORE OF STRAHD
            st.markdown(f"""
                <div class="ledger-box">
                    <div class="lore-title">Lore of Strahd</div>
                    <div class="lore-text">"{lore_text}"</div>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"The brass gears have failed: {e}")
else:
    st.info("The ledger is empty. Upload your Tarokka CSV in the sidebar.")
