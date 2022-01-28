import streamlit as st
from multiapp import MultiApp
from apps import bitcoin, ethereum, solana

app = MultiApp()

st.markdown(
    """
# Database Administration Project
"""
)

# Every app is a page on interface
app.add_app("Bitcoin", bitcoin.app)
app.add_app("Ethereum", ethereum.app)
app.add_app("Solana", solana.app)

# Run the app
app.run()
