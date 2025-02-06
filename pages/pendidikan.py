import streamlit as st
from controllers.pendidikan_controller import df_pendidikan_smk

st.title("DATA PENDIDIKAN BNA")


st.dataframe(df_pendidikan_smk)


