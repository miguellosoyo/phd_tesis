# Importar librerías de trabajo
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
  st.subheader('Usuarios')
  names = sorted(data['Usuario'].tolist())
  name = st.selectbox(label='Selección del Usuario', options=names)

# Definir elementos de la página
st.title('Registro de Análisis')  

st.write(f'Evolución del Comportamiento de Consumo: {name}')

# Filtrar información por paciente
df = data[data['Usuario']==name].melt(id_vars=['ID', 'Nombre', 'Usuario'], var_name='Semana', value_name='Cigarros').copy()
df['Semana'] = df['Semana'].astype(int)


# Crear la gráfica de líneas
line = alt.Chart(df).mark_line(point=True).encode(
       x=alt.X('Semana:Q', title='Semanas'),
       y='Cigarros:Q',
       color='Usuario:N',
       ).properties(
           title=f'Consumo de Cigarros {name}',
           width=600,
           height=250,
           )

# Definir líneas de separación para segmentos de línea Base y Tratamiento
line_base = pd.DataFrame({'x':[4]})
treatment = pd.DataFrame({'x':[8]})
vline_1 = alt.Chart(line_base).mark_rule(color='red', strokeWidth=3).encode(x='x:Q')
vline_2 = alt.Chart(treatment).mark_rule(color='red', strokeWidth=3).encode(x='x:Q')

# Integrar el gráfico completo
plot = alt.layer(vline_1, vline_2, line)

# Integrar la gráfica del paciente
st.altair_chart(plot, use_container_width=True)
