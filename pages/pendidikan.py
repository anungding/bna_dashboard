import streamlit as st
from controllers.pendidikan_controller import df_pendidikan_smk

st.title("DATA PENDIDIKAN BNA")

st.markdown("""
##### DATA SMK BANJARNEGARA 2023
###### Sumber: BPS BANJARNEGARA 2023
""")
st.dataframe(df_pendidikan_smk)


