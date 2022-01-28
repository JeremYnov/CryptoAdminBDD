import streamlit as st
from multiapp import MultiApp
from apps import bitcoin, ethereum, solana
from scripts.cmc_scraping import scrape

app = MultiApp()

st.markdown(
    """
# Database Administration Project
"""
)

app.add_app("Bitcoin", bitcoin.app)
app.add_app("Ethereum", ethereum.app)
app.add_app("Solana", solana.app)

app.run()
