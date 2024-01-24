# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 23:18:02 2024

@author: alexb
"""

import json
import numpy as np
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import plotly.express as px
import streamlit as st

App_title='Hábitos por niveles de obesidad'
App_subtitle='Source: Bicimad'


def main():
    st.set_page_config(page_title=App_title,
                       page_icon="🍖",
                       layout="wide")
    st.title(App_title)
    st.markdown("**Source: [Dataset for estimation of obesity levels](https://www.sciencedirect.com/science/article/pii/S2352340919306985?via%3Dihub)**")
if __name__ == "__main__":
    main()    