import streamlit as st
import eda
import prediction
import streamlit as st

nav = st.sidebar.selectbox('Pilih halaman:', ('EDA', 'Predict Rainfall'))

if nav == 'EDA':
    eda.run()
else:
    prediction.run()

