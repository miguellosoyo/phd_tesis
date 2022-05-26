# ===============================================================================================================================================
# Selección de Librerías
# ===============================================================================================================================================

# Importar librerías de trabajo
from statsmodels.graphics.factorplots import interaction_plot
import streamlit as st
import altair as alt
import pandas as pd
# import pingouin as pg

# ===============================================================================================================================================
# Tratamiento de la Información
# ===============================================================================================================================================

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

# ===============================================================================================================================================
# Calcular NAP
# ===============================================================================================================================================

# Obtener los puntos de referencia de consumo de tabaco de la línea base
k1, k2, k3, k4 = df[df['Semana'].isin(range(1,5))]['Cigarros']

# Definir un nuevo DataFrame para comparar las referencias de la línea base
user = df[(df['Semana'].isin(range(5,33)))]

# Contar los solapamientos (overlaps), empates (ties), no solapamientos (nonoverlaps) y el total de pares (all_pairs)
overlaps = sum(user['Cigarros']>k1) + sum(user['Cigarros']>k2) + sum(user['Cigarros']>k3) + sum(user['Cigarros']>k4)
ties = sum(user['Cigarros']==k1) + sum(user['Cigarros']==k2) + sum(user['Cigarros']==k3) + sum(user['Cigarros']==k4)
all_pairs = len(user)*4
nonoverlaps = all_pairs - overlaps

# Calcular el Nonovelap of All Pairs (NAP)
NAP = round(((nonoverlaps+(0.5*ties))/all_pairs)*100,2)

# Integrar métrica a la aplicación de Altair
st.metric(label='NAP', value=f'{NAP}%')

# ===============================================================================================================================================
# Crear la gráfica de líneas
# ===============================================================================================================================================

# Definir los límites de la gráfica
x_lim = [1, df['Semana'].max()]
y_lim = [0, int(1.1*df['Cigarros'].max())+1]

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
    fontWeight=alt.FontWeight('bold'),
    dy=-133,
    size=10
).encode(x=alt.X('Semana:Q', scale=alt.Scale(domain=x_lim, nice=False)), 
         text='Etiqueta',
         color=alt.value('#000000'),
        )

# Integrar todos los elementos en una sola gráfica
plot = (rule + line + text).properties(
        width=750,
        height=350,
        title=f'Consumo de Cigarros Semanales. {name}'
)

# Insertar gráfica
st.altair_chart(plot)

# ===============================================================================================================================================
# Calculo de ANOVA
# ===============================================================================================================================================

