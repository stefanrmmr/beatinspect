# DESIGN CHOICES
import streamlit as st

def design_setup():
    # get primaryColor from streamlit
    primary_color = st.get_option("theme.primaryColor")
    # Design page layout and browser window details
    st.set_page_config(layout="centered",
                       page_icon="resources/rs_logo_transparent_yellow.png",
                       page_title="beat inspect")
    # Design hide top header line
    hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
    # Design change spinner color to primary color
    st.markdown('''<style>.stSpinner > div > div {border-top-color: #e3fc03;}</style>''',
        unsafe_allow_html=True)
    # Design change stMetricsValue to primary color via specific css-element
    st.markdown('''<style>.css-1xarl3l.e16fv1kl1 {color: #e3fc03;}</style>''',
        unsafe_allow_html=True)
    # Design change radio button inner point to be dark grey via custom css
    st.markdown('''<style>.st-d9 {background-color: black;}</style>''',
        unsafe_allow_html=True)
    st.markdown('''<style>.st-db {height: 8px; width: 8px;}</style>''',
        unsafe_allow_html=True)
    st.markdown('''<style>.st-da {height: 8px; width: 8px;}</style>''',
        unsafe_allow_html=True)
