# COVID-19 Early Warning Score
# Date: 3/20/2020
# Contact: ganaya@buffalo.edu

from functools import reduce
from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import streamlit as st
#import plotly.graph_objects as go
#import ipywidgets as widgets
#from ipywidgets import AppLayout, Button
#from IPython.display import HTML, display, Markdown
#from bqplot import pyplot as plt
#import ipyvuetify as v
#from traitlets import Unicode, List

#matplotlib.use("Agg")
#import matplotlib.pyplot as plt

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Parameters

# Age
age = st.sidebar.radio("Age > 44?", ('Yes', 'No'))
if age == 'Yes': 
    age = 1
else: 
    age = 0

# Sex
sex = st.sidebar.radio("Sex", ('Male', 'Female'))
if sex == 'Male': 
    sex = 1
else: 
    sex = 0

# CT Findings
CT = st.sidebar.radio(
    "Signs of Pneumonia on CT?", ('Yes', 'No'))
if CT == 'Yes': 
    CT_score = 5
else: 
    CT_score = 0
if CT == 'Yes': 
    CT_val = 1
else: 
    CT_val = 0

# Exposure
exposure = st.sidebar.radio(
    "Has the patient been in close contact with a confirmed COVID-19 case?", ('Yes', 'No'))
if exposure == 'Yes': 
    exposure_score = 5
else: 
    exposure_score = 0
if exposure == 'Yes': 
    exposure_val = 1
else: 
    exposure_val = 0

# Fever
tmax = 0
fever = st.sidebar.radio("Fever?", ('Yes', 'No'))

if fever == 'Yes':
    tmax = (st.sidebar.number_input("TMax", 35.0, 45.0, value=36.5, step=0.1, format="%f"))

if fever == 'Yes': 
    fever = 1
else: 
    fever = 0

if tmax > 37.8: 
    tmax = 1
else:
    tmax = 0

# Respiratory Symptoms
resp_symp = 0
resp_symp = st.sidebar.multiselect('Any respiratory symptoms?',
                         ('Cough', 'Expectoration', 'Dyspnea'))
resp_symp = len(resp_symp)
if resp_symp >= 1:
    resp_symp = 1
else:
    resp_symp = 0

# NLR
abs_lym = (st.sidebar.number_input("Absolute Lymphocytes", 0.1, 10.0, value=3.0, step=0.1, format="%f"))
abs_neu = (st.sidebar.number_input("Absolute Neutrophils", 0.1, 10.0, value=3.0, step=0.1, format="%f"))

nlr = abs_neu/abs_lym
nlr_value = nlr

if nlr > 3.13:
    nlr = 1
else: nlr = 0

st.title("COVID-19 Early Warning Score")
st.markdown(
    """*This tool is intended for .... 

For questions about this page, contact ganaya@buffalo.edu. 
""")

def ews(age, sex, CT_score, exposure_score, fever, tmax, resp_symp, nlr):
    values = age, sex, CT_score, exposure_score, fever, tmax, resp_symp, nlr
    score = np.sum(values)
    #covid19 =  1 / 1 + exp - [ -9.106 + (2.79 * fever) + (4.58 * exposure) + (5.10 * CT) + (0.97 * NLR) + (0.94 * tmax) + (0.90 x Sex)] 
    return score

bin_dict = dict({1:'Yes', 0:'No'})
age_dict = dict({1:'Age>44', 0:'Age<44'})
sex_dict = dict({1:'Male', 0:'Female'})
tmax_dict = dict({1:'Tmax>37.8', 0:'Tmax<37.8'})
resp_dict = dict({1:'At least one respiratory symptom', 0: 'No respiratory symptoms'})
nlr_dict = dict({1:'NLR>3.13', 0:'NLR<3.13'})

early_warning_score = ews(age, sex, CT_score, exposure_score, fever, tmax, resp_symp, nlr)

data = {
    'Parameters': ['Signs of Pneumonia on CT', 'History of close contact with confirmed COVID-19 patient',
                  'Fever', 'Tmax', 'Age', 'Sex','Respiratory Symptoms', 'Neutrophyl/Lymphocyte Ratio (NLR)', ''],
    'Assessment': [bin_dict[CT_val], bin_dict[exposure_val], bin_dict[fever], tmax_dict[tmax], age_dict[age], sex_dict[sex], 
                   resp_dict[resp_symp], nlr_dict[nlr], 'Total Score'],
    'Score': [CT_score, exposure_score, fever, tmax, age, sex, resp_symp, nlr, early_warning_score]
}

df = pd.DataFrame(data)

st.subheader("COVID-19 Early Warning Calculator")

st.table(df)

st.markdown("""The COVID-19 Early Warning Score is **{early_warning_score:.0f}**, a score of more than 10 indicates...""".format(
        early_warning_score=early_warning_score)
)
st.markdown("""The calculated Neutrophyl/Lymphocyte Ratio is **{nlr_value:.2f}**.""".format(
        nlr_value=nlr_value)
)

#    """Erie county has reported **{cases_erie:.2f}** cases of COVID-19.""".format(
#        cases_erie=cases_erie
#    )

if st.checkbox("Show Additional Information"):
    st.subheader("COVID-19 Early Warning Score Methodology")

    st.markdown(
        """* **Hospitalized.
        * **Currently 
        * **Regional . 
        """)
        

st.subheader("References & Acknowledgements")
st.markdown(
    """
    https://www.medrxiv.org/content/10.1101/2020.03.05.20031906v1.full.pdf
    """
)