
# Importar librerías de trabajo
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import os

# Definir las opciones de pandas para visualizar todos los registros y columnas
pd.options.display.max_rows = None
pd.options.display.max_columns = None

# Importar información
data = pd.read_csv('https://raw.githubusercontent.com/miguellosoyo/phd_tesis/main/Base%201.csv', encoding='latin')

# Integrar a la barra lateral la selección de concesionarios y tipo de reporte
with st.sidebar:

  # Definir un menú de selección para los concesionarios
  st.subheader('Pacientes')
  names = sorted(data['Nombre'].tolist())
  name = st.selectbox(label='Selección del Paciente', options=names)

# Definir elementos de la página
st.title('Registro de Análisis')  

st.write(f'Evolución del Comportamiento de Consumo: {name}')

# Filtrar información por paciente
df = data[data['Nombre']==name].melt(id_vars=['ID', 'Nombre'], var_name='Semana', value_name='Cigarros').copy()

# Crear la gráfica de líneas
line = alt.Chart(df).mark_line(point=True).encode(
       x=alt.X('Semana:O', title='Semanas'),
       y='Cigarros:Q',
       color='Nombre:N',
       ).properties(
           title=f'Consumo de Cigarros {name}',
           width=600,
           height=250,
           )

# Integrar la gráfica del paciente
st.altair_chart(line, use_container_width=True)
