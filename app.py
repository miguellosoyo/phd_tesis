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
x_lim = [1, df['Semana'].max()]
y_lim = [0, df['Cigarros'].max()+4]
line = alt.Chart(df).mark_line(point=True).encode(
       x=alt.X('Semana:Q', title='Semanas', axis=alt.Axis(tickCount=df.shape[0]), scale=alt.Scale(domain=x_lim, nice=False)),
       y=alt.Y('Cigarros:Q', scale=alt.Scale(domain=y_lim)),
       color='Usuario:N',
       )

# Definir líneas de separación para segmentos de línea Base y Tratamiento
line_base = pd.DataFrame({'x':[4]})
treatment = pd.DataFrame({'x':[8]})
vline_1 = alt.Chart(line_base).mark_rule(color='red', strokeWidth=1.3).encode(x=alt.X('x:Q', scale=alt.Scale(domain=x_lim, nice=False)))
vline_2 = alt.Chart(treatment).mark_rule(color='red', strokeWidth=1.3).encode(x=alt.X('x:Q', scale=alt.Scale(domain=x_lim, nice=False)))

# Definir texto de secciones
text1 = alt.Chart({'values':[{'x': 2.5, 'Cigarros':df['Cigarros'].max()+2.5}]}).mark_text(
    text='Linea Base', angle=0, fontWeight=alt.FontWeight('bold')).encode(x='x:Q', y='Cigarros:Q')

text2 = alt.Chart({'values':[{'x': 6, 'Cigarros':df['Cigarros'].max()+2.5}]}).mark_text(
    text='Tratamiento', angle=0, fontWeight=alt.FontWeight('bold')).encode(x='x:Q', y='Cigarros:Q')

text3 = alt.Chart({'values':[{'x':21, 'Cigarros':df['Cigarros'].max()+2.5}]}).mark_text(
    text='Seguimiento', angle=0, fontWeight=alt.FontWeight('bold')).encode(x='x:Q', y='Cigarros:Q')

# Integrar el gráfico completo
plot = alt.layer(vline_1, vline_2, line, text1, text2, text3).properties(
    title=f'Consumo de Cigarros Semanales. {name}',
    width=750,
    height=250,
    )

# Integrar la gráfica del paciente
st.altair_chart(plot, use_container_width=True)
