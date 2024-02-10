# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 23:18:02 2024

@author: alexb
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from plotnine import *

#Carga y procesado de los datos#############################
#Los datos ya han sido limpiados en el notebook, de manera que se guarda el resultado en 
#obesidad_limpio.csv, sin embargo no se guarda la categorizacion de las variables.
#Por tanto, es necesario dársela
def procesado_datos(obesidad):
    #Para tipos de obesidad
    orden_categorias = ['Insufficient_Weight','Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II',
           'Obesity_Type_III']
    obesidad['obesity_type'] = pd.Categorical(obesidad['obesity_type'], categories=orden_categorias, ordered=True)
    #Para comidas, ¿comes entre comidas?
    orden_categorias = ['no', 'Sometimes', 'Frequently', 'Always']
    obesidad['CAEC'] = pd.Categorical(obesidad['CAEC'], categories=orden_categorias, ordered=True)
    #Para alcohol, ¿bebes alcohol?
    orden_categorias = ['no', 'Sometimes', 'Frequently', 'Always']
    obesidad['alcohol'] = pd.Categorical(obesidad['alcohol'], categories=orden_categorias, ordered=True)
    #Para vegetables, ¿comes verduras?
    orden_categorias = ["Nunca","Algunas veces","Siempre"]
    obesidad['vegetables'] = pd.Categorical(obesidad['vegetables'], categories=orden_categorias, ordered=True)
    #Para NCP, ¿cuantas comidas realizas?
    orden_categorias = ["Entre 1 y 2","Tres","Más de tres"]
    obesidad['comidas'] = pd.Categorical(obesidad['comidas'], categories=orden_categorias, ordered=True)    
    #Para CH2O, ¿Cuanto agua bebes en un día?
    orden_categorias = ["Menos de 1L","1L-2L","Más de 2L"]
    obesidad['water'] = pd.Categorical(obesidad['water'], categories=orden_categorias, ordered=True)
    #Para FAF, ¿Cuanto ejercicio realizas en una semana? 
    orden_categorias = ["No hago","1d-2d","2d-4d","4d-5d"]
    obesidad['physical_activity'] = pd.Categorical(obesidad['physical_activity'], categories=orden_categorias, ordered=True)
    #Para TUE, ¿Cuanto tiempo consumes dispositivos electrónicos en un día? 
    orden_categorias = ["0-2h","3-5h","Más de 5h"]
    obesidad['electronica'] = pd.Categorical(obesidad['electronica'], categories=orden_categorias, ordered=True)
    #Creamos un conjunto de condiciones que nos permiten determinar una dieta sana
    dieta_sana_condiciones = (
        (obesidad['water'].isin(['1L-2L','Más de 2L'])) &
        (obesidad['physical_activity'].isin(['4d-5d', '2d-4d'])) &
        (obesidad['comidas']=="Tres") &
        (obesidad['FAVC'] == 'no') &
        (obesidad['SMOKE'] == 'no') &
        (obesidad['electronica']=='0-2h') &
        (obesidad['alcohol'].isin(['no', 'Sometimes'])) &
        (obesidad['CAEC'].isin(['no', 'Sometimes'])))
    #Creamos la columna 'Salud'
    obesidad['Salud']='NA'
    obesidad.loc[dieta_sana_condiciones,'Salud']='Se cuida'
    #Creamos un conjunto de condiciones que nos permiten determinar una dieta no sana
    dieta_no_sana_condiciones=(~dieta_sana_condiciones) & ((obesidad['water'].isin(['Menos de 1L','Más de 2L'])) &
        (obesidad['physical_activity'].isin(['No hago',])) &
        (obesidad['comidas'].isin(['Entre 1 y 2', 'Más de tres'])) &
        (obesidad['FAVC'] == 'yes')  &
        (obesidad['electronica']=='Más de 5h') &
        (obesidad['alcohol'].isin(['Frequently', 'Always'])) &
        (obesidad['CAEC'].isin(['Frequently', 'Always']))|
        (obesidad['SMOKE'] == 'yes'))
    obesidad.loc[dieta_no_sana_condiciones,'Salud']='No se cuida'
    #Cuando no se cumple ninguna de las anteriores se denota 'Se cuida poco'
    obesidad.loc[(~dieta_no_sana_condiciones)&(~dieta_sana_condiciones),'Salud']='Se cuida poco'
    return obesidad
 
#Insights#######################################    

#Primer Insight
def Insight1(obesidad_limpio,columna,paleta):
    '''
    Se van a estudiar 4 tipos de campos, cada uno con sus etiquetas por ello es preciso asignar como debe de
    ser la etiqueta según la variable
    '''
    if columna == 'vegetables':
        nombre = 'Consumo de vegetales'
        etiquetas = {'Nunca': 'Nunca', 'Algunas veces':'Algunas Veces', 'Siempre': 'Siempre'}
    elif columna == 'water':
        nombre = 'Consumo de agua'
        etiquetas = {'Menos de 1L':'Menos de 1L', '1L-2L':'Entre 1L y 2L','Más de 2L':'Más de 2L'}
    elif columna == 'physical_activity':
        nombre = 'Actividad física'
        etiquetas = {'No hago':'Sedentario', '1d-2d':'1 o 2 días','2d-4d':'3 o 4 días', '4d-5d':'Más de 4 días'}
    else:
        nombre = 'Consumo de alcohol'
        etiquetas = {'no':'Nunca','Sometimes':'A veces', 'Frequently':'Frecuentemente', 'Always':'Siempre'}
    return (ggplot(obesidad_limpio[['obesity_type',columna]], aes(x='obesity_type', fill=f'factor({columna})')) + 
        geom_bar(position='dodge') + 
        labs(title=f'Evolución por obesidad según el c{nombre[1:]}',y='Personas')+ 
        theme(panel_grid_major_x=element_blank(),
              panel_background=element_rect(fill='grey'),
              panel_grid_major_y=element_blank(),
              panel_grid_minor_y=element_blank(),
              #Se añade tanta inclinación porque el texto no entra de otra manera
              axis_text_x = element_text(angle = 70, hjust = 1),
              plot_title = element_text(hjust = 0.5, size = 12,weight='bold'),
              legend_text=element_text(size=8),
              legend_title=element_text(size=10,weight='bold'))+
              scale_x_discrete(name = "Tipo de Obesidad",
        limits = ("Insufficient_Weight","Normal_Weight","Overweight_Level_I","Overweight_Level_II","Obesity_Type_I","Obesity_Type_II","Obesity_Type_III"),
        labels = ("Peso Insuficiente","Peso Normal","Sobrepeso nivel I","Sobrepeso nivel II","Obesidad Tipo I","Obesidad Tipo II","Obesidad Tipo III"))+
        scale_fill_brewer(palette = paleta,name = f"{nombre}",labels =etiquetas)+
        ylim(0, 330)
        )

#Insight 2
def Insight2(obesidad, scatter=False):
    obesidad_filtrado = obesidad[obesidad['Salud'].isin(['Se cuida', 'No se cuida'])]
    
    if scatter==False:
        fig = px.bar(obesidad_filtrado, x='obesity_type', color='Salud', title='Salud de las personas por tipo de obesidad',
                     labels={'obesity_type': 'Tipo de Obesidad',"count":"Personas"}, 
                     category_orders={'obesity_type': ['Insufficient_Weight','Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']},
                     barmode="group",
                     color_discrete_map={'Se cuida': '#90ee90', 'No se cuida': '#636efa'})  
        fig.update_xaxes(tickangle=-25)
        
        fig.update_layout(title_font=dict(size=30,color='black'),
                          xaxis=dict(tickvals=['Insufficient_Weight','Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III'],
                                     ticktext=["Peso Insuficiente","Peso Normal","Sobrepeso nivel I","Sobrepeso nivel II","Obesidad Tipo I","Obesidad Tipo II","Obesidad Tipo III"]))

    elif scatter=='Si':
        fig = px.scatter(obesidad, x='weight', y='height', color='Salud', size='age',
                 labels={'weight': 'Peso (kg)', 'height': 'Altura (m)'},
                 title='Relación entre Peso y Altura')
        # Modificar el título
        fig.update_layout(title_font=dict(size=30,color='black'))
    else:
        m, c = np.polyfit(obesidad['weight'], obesidad['height'], 1) #esto utiliza el MSE para pintar la linea de regresión,hacen falta mas componentes en vd

        fig = px.scatter(obesidad, x='weight', y='height', color='Salud',
                         title='Relación entre Peso y Altura',
                         labels={'weight': 'Peso (kg)', 'height': 'Altura (m)'})
        fig.update_layout(title_font=dict(size=30,color='black'))
        # Añade la línea de regresión al gráfico
        fig.add_traces(px.line(x=obesidad['weight'], y=m*obesidad['weight']+c).data)
    
    return fig

#Insight 3
def Insight3(obesidad, jitter=False):
    if not jitter:
        fig = px.density_heatmap(obesidad, x='electronica', y='physical_activity', 
                             title='',
                             category_orders={"physical_activity":['4d-5d', '2d-4d', '1d-2d', 'No hago'],"electronica":['0-2h', '3-5h','Más de 5h']},
                             labels={'electronica': 'Actividad electrónica', 'physical_activity': 'Actividad física', 'obesity_type': 'Tipo de Obesidad'},
                             color_continuous_scale='RdBu_r')
    else:
        fig=(ggplot(obesidad, aes(x='electronica', y='physical_activity', fill='obesity_type')) + 
             geom_jitter() +
             scale_fill_brewer(type='diverging',
                               palette='RdYlBu',
                               direction=-1,
                               name = "Tipos de obesidad",
                               labels = ("Peso Insuficiente","Peso Normal","Sobrepeso nivel I","Sobrepeso nivel II","Obesidad Tipo I","Obesidad Tipo II","Obesidad Tipo III")) +
             labs(x="Actividad electrónica",
                  y='Actividad física',
                  title='')+
             theme(panel_background=element_blank(),
                   axis_ticks=element_blank(),
                   panel_grid_major=element_blank(),
                   panel_grid_minor=element_blank(),
                   plot_title = element_text(hjust = 0.5, size = 12,weight='bold'),
                   legend_text=element_text(size=8),
                   legend_title=element_text(size=10,weight='bold')))

    return fig

#Insight 4

def Insight4(obesidad):
    '''
    Creamos una columna que sean los rangos de edad para poder realizar 
    una buena visualización
    '''
    def crear_lista(paso):
        limite_inicial = 14
        limite_final = 40
        return list(zip(np.arange(limite_inicial, limite_final, paso), np.arange(limite_inicial + paso, limite_final + paso, paso)))
    
    def encontrar_intervalo( elemento,lista_tuplas=crear_lista(5)):
        resultado = next((tupla for tupla in lista_tuplas if elemento >= tupla[0] and elemento < tupla[1]), None)
        return f'{resultado[0]}-{resultado[1]}'
    obesidad['Intervalos_de_edad']=obesidad['age'].apply(encontrar_intervalo)
    
    fig=(ggplot(obesidad, aes(x='Intervalos_de_edad', fill='alcohol')) + 
         geom_bar(position='fill')+
         labs(title = 'Consumo de alcohol por edad',x = 'Grupos de edad') + 
         scale_fill_brewer(name = 'Consumo de Alcohol',
                           type ='diverging',palette='RdYlBu',
                           direction = -1,
                           labels = {'no':'Nunca','Sometimes':'A veces', 'Frequently':'Frecuentemente', 'Always':'Siempre'}) + 
         theme(plot_title=element_text(hjust=0.5, size = 12,weight='bold'),
               legend_text=element_text(size=8),
               legend_title=element_text(size=10,weight='bold'),
               axis_title_y = element_blank(),
               panel_background=element_blank(),
               axis_ticks=element_blank())
        )
    return fig

#Insight 5
def Insight5(obesidad):
    obesidad_genero = obesidad.loc[:,['gender','obesity_type']].groupby('gender').value_counts()
    obesidad_genero = pd.DataFrame(obesidad_genero).reset_index()
    fig=(ggplot(obesidad_genero.loc[obesidad_genero['obesity_type'].isin(["Insufficient_Weight","Normal_Weight","Overweight_Level_I","Overweight_Level_II","Obesity_Type_I"])],aes(x = 'obesity_type',y = 'count',fill = 'gender')) +
            geom_col(position='dodge') + 
            labs(title='Distribución obesidad por sexo',y='Personas')+
            scale_fill_discrete(name = 'Sexo',labels={'Female': 'Femenino', 'Male': 'Masculino'})+
            theme(panel_background=element_rect(fill='white'),
                  panel_grid_major_y=element_blank(),
                  panel_grid_minor_y=element_blank(),
                  axis_text_x = element_text(angle = 70, hjust = 1),
                  plot_title = element_text(hjust = 0.5, size = 12,weight='bold'),
                  legend_text=element_text(size=8),
                  legend_title=element_text(size=10,weight='bold'))+
            scale_x_discrete(name = "Tipo de Obesidad",
                             limits = ("Insufficient_Weight","Normal_Weight","Overweight_Level_I","Overweight_Level_II","Obesity_Type_I"),
                             labels = ("Peso Insuficiente","Peso Normal","Sobrepeso nivel I","Sobrepeso nivel II","Obesidad Tipo I"))
        )
    return fig
   

#Insight 6

#Este insight nos puede devolver tres gráficas dependiendo de lo que deseemos obtenemos una u otra
def Insight6(obesidad, opcion,historia_familiar='no'):
    if opcion=='porcentaje':
        fig= (ggplot(obesidad, aes(x='Salud', fill='family_history_with_overweight')) + 
                geom_bar(position='fill')+
                scale_fill_manual(values=["#F2A84A", "#D9560C"],
                                  name="Familiares con sobrepeso")+
                labs(y="",
                     title="Personas con antecedentes familiares \nsegún estilo de vida")+
                theme(panel_background = element_blank(),
                      axis_ticks=element_blank(),
                      plot_title = element_text(hjust = 0.5, size = 12,weight='bold'),
                      legend_text=element_text(size=8),
                      legend_title=element_text(size=10,weight='bold'))
               )
    else:
        def historial_familiar(obesidad, historial, col):
            if historial=='yes':
                texto='con'
            else:
                texto='sin'
            obesidad_historial = obesidad.loc[obesidad['family_history_with_overweight'] == historial].groupby("obesity_type").size().reset_index(name='count')
            
            fig = go.Figure(data=[go.Bar(x=obesidad_historial['obesity_type'], y=obesidad_historial['count'], marker_color=col)])
            
            fig.update_layout(
                xaxis=dict(title='Tipo de Obesidad',
                           tickvals=['Insufficient_Weight','Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III'],
                           ticktext=["Peso Insuficiente","Peso Normal","Sobrepeso nivel I","Sobrepeso nivel II","Obesidad Tipo I","Obesidad Tipo II","Obesidad Tipo III"]),
                yaxis=dict(title='Personas'),
                title=f'Personas por tipo de obesidad {texto} historial familiar',
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=30, color='black'),
                font=dict(color='black')
            )
            return fig
        if historia_familiar=='no':
           fig=historial_familiar(obesidad,'no',"#F2A84A")
        else:
           fig=historial_familiar(obesidad,'yes','#D9560C')
    return fig

#Insight 7

def Insight7(obesidad):
    obesidad_tipo3=obesidad.loc[obesidad['obesity_type']=='Obesity_Type_III'][['family_history_with_overweight','FAVC','vegetables','comidas','CAEC','SMOKE','alcohol','water','SCC','physical_activity']].value_counts().reset_index()
    return obesidad_tipo3


#Insight 8

def Insight8(obesidad):
    fig= (ggplot(obesidad, aes(x='MTRANS', fill='obesity_type')) + 
          geom_bar(position='fill')+
          scale_fill_brewer(type ='diverging',
                            palette='PuOr',
                            direction = -1,
                            name="Tipos de obesidad",
                            labels = ("Peso Insuficiente","Peso Normal","Sobrepeso nivel I","Sobrepeso nivel II","Obesidad Tipo I","Obesidad Tipo II","Obesidad Tipo III"))+
          labs(title="Medios de transporte por tipos de obesidad",
               y='',
               x='Medios de transporte')+
          theme(panel_background = element_blank(),
                axis_ticks=element_blank(),
                axis_text_x=element_text(rotation=55,hjust=1),
                axis_ticks_major_y = element_blank(),
                plot_title = element_text(hjust = 0.5, size = 12,weight='bold'),
                legend_text=element_text(size=8),
                legend_title=element_text(size=10,weight='bold'))
         )
    return fig
        


#Botones

def boton_insight1(obesidad):
    col1, col2 = st.columns([1, 1])
    with col1:
      plot=Insight1(obesidad,'water','Blues')
      st.pyplot(ggplot.draw(plot))
      st.write('')
      plot=Insight1(obesidad,'vegetables','Greens')
      st.pyplot(ggplot.draw(plot))
    with col2: 
      plot=Insight1(obesidad,'physical_activity','Purples')+labs(title='Evolución por obesidad según la actividad física')
      st.pyplot(ggplot.draw(plot))
      plot=Insight1(obesidad,'alcohol','YlOrRd')
      st.pyplot(ggplot.draw(plot))
      
      
def boton_insight2(obesidad):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.header("Opciones")
        opciones= st.selectbox('',
             ('Personas que se cuidan por tipo de obesidad',"Relacion peso altura", "Relacion peso altura con recta de regresion"))
    with col2:
        if opciones=='Personas que se cuidan por tipo de obesidad':
           st.plotly_chart(Insight2(obesidad))
        elif opciones=="Relacion peso altura":
            st.plotly_chart(Insight2(obesidad,'Si'))    
        else:
            st.plotly_chart(Insight2(obesidad,'No'))

def boton_insight3(obesidad):
    st.header("Relación entre uso de electrónica y actividad física")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(Insight3(obesidad))
    with col2:
        plot=Insight3(obesidad,True)
        st.pyplot(ggplot.draw(plot))

def boton_insight4(obesidad):
    col1, col2,col3 = st.columns([1, 2, 1])
    with col2:
        plot=Insight4(obesidad)
        st.pyplot(ggplot.draw(plot))
        
def boton_insight5(obesidad):
    col1, col2,col3 = st.columns([1, 2, 1])
    with col2:
        plot=Insight5(obesidad)
        st.pyplot(ggplot.draw(plot))

def boton_insight6(obesidad):
    col1, col2 = st.columns([1, 1])
    with col1:
        plot=Insight6(obesidad,'porcentaje')
        st.pyplot(ggplot.draw(plot))
    with col2:
        st.header("Opciones")
        opciones= st.selectbox('',
             ('Con historial familiar','Sin historial familiar'))
        if opciones=='Sin historial familiar':
            st.plotly_chart(Insight6(obesidad,'','no'))
        else:
            st.plotly_chart(Insight6(obesidad,'','yes'))

def boton_insight7(obesidad):
    st.header("¿Qué patrones son los más comunes en las persona con obesidad de tipo III?")
    obsidad_insight7=obesidad.loc[obesidad['obesity_type']=='Obesity_Type_III'][['family_history_with_overweight','FAVC','vegetables','comidas','CAEC','SMOKE','alcohol','water','SCC','physical_activity']].value_counts().reset_index()
    st.dataframe(obsidad_insight7)

def boton_insight8(obesidad):
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        plot=Insight8(obesidad)
        st.pyplot(ggplot.draw(plot))

def download_csv(obesidad):
    #Informacion obtenida de https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv
    @st.cache_data
    def convert_df(obesidad):
       return obesidad.to_csv(index=False).encode('utf-8')
    
    
    csv = convert_df(obesidad)
    
    st.download_button(
       "Haz click para descargar",
       csv,
       "obesidad.csv",
       "text/csv",
       key='download-csv'
    )
    


App_title='Hábitos por niveles de obesidad'
   
    
def main():
    st.set_page_config(page_title=App_title,
                       page_icon="🍖",
                       layout="wide")
    st.title(App_title)
    st.markdown("**Source: [Dataset for estimation of obesity levels](https://www.sciencedirect.com/science/article/pii/S2352340919306985?via%3Dihub)**")
    obesidad = pd.read_csv("obesity_limpio.csv")
    obesidad=procesado_datos(obesidad)
    opciones=st.sidebar.radio('', ['Introducción','Insights'])
    if opciones=='Introducción': 
        st.dataframe(obesidad)
        download_csv(obesidad)
    else:
        opciones_selectbox=st.sidebar.selectbox("Elige qué insight ver",
                                               ['Primer Insight','Segundo Insight','Tercer Insight',
                                               'Cuarto Insight','Quinto Insight','Sexto Insight',
                                               'Séptimo Insight','Octavo Insight'])
        
        if opciones_selectbox == 'Primer Insight':
            boton_insight1(obesidad)
        elif opciones_selectbox == 'Segundo Insight':
            boton_insight2(obesidad)
        elif opciones_selectbox == 'Tercer Insight':
            boton_insight3(obesidad)
        elif opciones_selectbox == 'Cuarto Insight':
            boton_insight4(obesidad)
        elif opciones_selectbox == 'Quinto Insight':
            boton_insight5(obesidad)
        elif opciones_selectbox == 'Sexto Insight':
            boton_insight6(obesidad)
        elif opciones_selectbox == 'Séptimo Insight':
            boton_insight7(obesidad)
        elif opciones_selectbox == 'Octavo Insight':
            boton_insight8(obesidad)

if __name__ == "__main__":
    main()   