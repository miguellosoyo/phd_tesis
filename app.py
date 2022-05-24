# Importar librerías de trabajo
import streamlit as st
import altair as alt
import pandas as pd

# Importar información
data = pd.read_csv('https://raw.githubusercontent.com/miguellosoyo/phd_tesis/main/Base%201.csv', encoding='latin')

# Integrar a la barra lateral la selección de concesionarios y tipo de reporte
with st.sidebar:

  # Definir un menú de selección para los concesionarios
  st.subheader('Usuarios')
  names = sorted(data['Usuario'].tolist())
  name = st.selectbox(label='Selección del Usuario', options=names)

# Filtrar información por paciente
df = data[data['Usuario']==name].melt(id_vars=['ID', 'Nombre', 'Usuario'], var_name='Semana', value_name='Cigarros').copy()
df['Semana'] = df['Semana'].astype(int)

# Crear la gráfica de líneas
x_lim = [1, df['Semana'].max()]
y_lim = [0, df['Cigarros'].max()+2]

# Definir un DataFrame para las etiquetas de las secciones
sections = pd.DataFrame([
                         {'Semana':4, 'Cigarros':y_lim[-1]-9, 'Etiqueta':''},
                         {'Semana':8, 'Cigarros':y_lim[-1]-9, 'Etiqueta':''},
                         {'Semana':3.8, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'Linea Base'},
                         {'Semana':7.3, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'Tratamiento'},
                         {'Semana':21, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'Seguimiento'},
                         ])

# Crear la gráfica de líneas
line = alt.Chart(df).mark_line(point=True).encode(
       x=alt.X('Semana:Q', title='Semanas', axis=alt.Axis(tickCount=df.shape[0]), scale=alt.Scale(domain=x_lim, nice=False)),
       y=alt.Y('Cigarros:Q', scale=alt.Scale(domain=y_lim), axis=alt.Axis(tickCount=len(range(y_lim[0], y_lim[-1]+2)))),
       color='Usuario:N',
       )

# Aplicar la regla de división por sección de Línea Base, Tratamiento y Seguimiento
rule = alt.Chart(sections).mark_rule(
    color='red',
    strokeWidth=2
).encode(
    x=alt.X('Semana:Q', scale=alt.Scale(domain=x_lim, nice=False))
).transform_filter((alt.datum.Semana == 4) | (alt.datum.Semana == 8))

# Integrar textos, usando el DataFrame de secciones
text = alt.Chart(sections).mark_text(
    align='right',
    baseline='middle',
    # dx=7,
    dy=-140,
    size=10
).encode(x=alt.X('Semana:Q', scale=alt.Scale(domain=x_lim, nice=False)), 
        #  y=alt.Y('Cigarros:Q', scale=alt.Scale(domain=y_lim, nice=False)), 
         text='Etiqueta',
         color=alt.value('#000000'))

# Integrar todos los elementos en una sola gráfica
plot = (rule + line + text).properties(
        width=750,
        height=350,
        title=f'Consumo de Cigarros Semanales. {name}'
)

# Insertar gráfica
st.altair_chart(plot)
