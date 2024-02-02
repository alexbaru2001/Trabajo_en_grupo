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
import matplotlib
from plotnine import *

App_title='Hábitos por niveles de obesidad'
App_subtitle='Source: Bicimad'


def mostrar1(obesidad_limpio,columna,paleta):
    return (ggplot(obesidad_limpio[['obesity_type',columna]], aes(x='obesity_type', fill=f'factor({columna})')) + 
        geom_bar(position='dodge') + 
        theme(axis_text_x = element_text(angle = 45, hjust = 1,color = "black"),
              panel_grid_major_x=element_blank(),
              panel_background=element_rect(fill='grey'),
              panel_grid_major_y=element_blank(),
              panel_grid_minor_y=element_blank())+
        labs(x='Niveles de obesidad', y='Cantidad')+
        scale_fill_brewer(palette = paleta,name = f"Nivel de consumo de {columna}")+
        ylim(0, 300)
        )

def boton1(obesidad):
    col1, col2 = st.columns([1, 1])
    with col1:
      plot=mostrar1(obesidad,'vegetables','Greens')
      st.pyplot(ggplot.draw(plot))
      plot=mostrar1(obesidad,'alcohol','YlOrRd')
      st.pyplot(ggplot.draw(plot))
    with col2: 
      plot=mostrar1(obesidad,'water','Blues')
      st.pyplot(ggplot.draw(plot))
      plot=mostrar1(obesidad,'physical_activity','Purples')
      st.pyplot(ggplot.draw(plot))

def main():
    st.set_page_config(page_title=App_title,
                       page_icon="🍖",
                       layout="wide")
    st.title(App_title)
    st.markdown("**Source: [Dataset for estimation of obesity levels](https://www.sciencedirect.com/science/article/pii/S2352340919306985?via%3Dihub)**")
    obesidad = pd.read_csv("obesity_limpio.csv")
    boton1(obesidad)
    st.write(obesidad)
if __name__ == "__main__":
    main()   