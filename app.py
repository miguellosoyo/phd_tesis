# Importar librerías de trabajo
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

# Definir una función para dar formato a las tablas ANOVA
def anova_table(s, props=''):
  return np.where(s<0.05, props, '')

# ===============================================================================================================================================
# Tratamiento de la Información
# ===============================================================================================================================================

# Importar información
data = pd.read_csv('https://raw.githubusercontent.com/miguellosoyo/phd_tesis/main/Base%201.csv', encoding='latin')
affections = pd.read_csv('https://raw.githubusercontent.com/miguellosoyo/phd_tesis/main/Afectos.csv', encoding='latin')

# Integrar a la barra lateral la selección de concesionarios y tipo de reporte
# with st.sidebar:

# Definir un menú de selección para los concesionarios
st.subheader('Usuarios')
names = sorted(data['Usuario'].tolist())
name = st.selectbox(label='Selección del Usuario', options=names)

# Filtrar información por paciente para el caso de consumo de tabaco
data_users = data.melt(id_vars=['ID', 'Nombre', 'Usuario'], var_name='Semana', value_name='Cigarros').copy()
df = data[data['Usuario']==name].melt(id_vars=['ID', 'Nombre', 'Usuario'], var_name='Semana', value_name='Cigarros').copy()
data_users['Semana'] = data_users['Semana'].astype(int)
df['Semana'] = df['Semana'].astype(int)

# Seleccionar hasta el 15vo usuario
# df = df[df['ID'].astype(int)<=15].copy()
# data_users = data_users[data_users['ID'].astype(int)<=15].copy()

# Filtrar información por paciente para los casos de afecto
df_affections = affections[affections['Usuario']==name].melt(id_vars=['ID', 'Nombre', 'Usuario', 'Tipo'], var_name='Semana', value_name='Nivel de Afecto').copy()

# Seleccionar hasta el 15vo usuario
# df_affections = df_affections[df_affections['ID'].astype(int)<=15].copy()

# ===============================================================================================================================================
# Calcular NAP
# ===============================================================================================================================================

# Obtener los puntos de referencia de consumo de tabaco de la línea base
k1, k2, k3, k4 = df[df['Semana'].isin(range(1,5))]['Cigarros'].tolist()[:]

# Definir un nuevo DataFrame para comparar las referencias de la línea base
user = df[(df['Semana'].isin(range(5,33)))].copy()

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
# Crear la gráfica de líneas de consumo y afecto
# ===============================================================================================================================================

# Definir límites del eje x e y
x_lim = [1, df['Semana'].max()]
y_lim = [0, int(1.1*df['Cigarros'].max())+1]

# Definir un DataFrame para las etiquetas de las secciones
sections = pd.DataFrame([
                        {'Semana':4, 'Cigarros':y_lim[-1]-9, 'Etiqueta':''},
                        {'Semana':8, 'Cigarros':y_lim[-1]-9, 'Etiqueta':''},
                        {'Semana':2, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'LB'},
                        {'Semana':6, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'Trat'},
                        {'Semana':10, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'Seg 1'},
                        {'Semana':12, 'Cigarros':y_lim[-1]-9, 'Etiqueta':''},
                        {'Semana':16, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'Seg 2'},
                        {'Semana':20, 'Cigarros':y_lim[-1]-9, 'Etiqueta':''},
                        {'Semana':28, 'Cigarros':y_lim[-1]-9, 'Etiqueta':'Seg 3'},
                        {'Semana':32, 'Cigarros':y_lim[-1]-9, 'Etiqueta':''},
                        ])

# Crear la gráfica de líneas
line = alt.Chart(df).mark_line(point=True, color='steelblue').encode(
      x=alt.X('Semana:Q', title='Semanas', axis=alt.Axis(tickCount=df.shape[0], grid=False), scale=alt.Scale(domain=x_lim, nice=False)),
      y=alt.Y('Cigarros:Q', scale=alt.Scale(domain=y_lim), axis=alt.Axis(grid=False, tickCount=len(range(y_lim[0], y_lim[-1]+2)))),
      )

# Aplicar la regla de división por sección de Línea Base, Tratamiento y Seguimiento
rule = alt.Chart(sections).mark_rule(
    color='red',
    strokeWidth=1
).encode(
    x=alt.X('Semana:Q', scale=alt.Scale(domain=x_lim, nice=False))
).transform_filter((alt.datum.Semana == 4) | (alt.datum.Semana == 8) | (alt.datum.Semana == 12) | (alt.datum.Semana == 20) | (alt.datum.Semana == 32))

# Integrar textos, usando el DataFrame de secciones
text = alt.Chart(sections).mark_text(
    align='right',
    baseline='middle',
    fontWeight=alt.FontWeight('bold'),
    dy=-83,
    dx=12,
    size=12
).encode(x=alt.X('Semana:Q', scale=alt.Scale(domain=x_lim, nice=False)), 
        #  y=alt.Y('Cigarros:Q', scale=alt.Scale(domain=y_lim, nice=False)), 
        text='Etiqueta',
        color=alt.value('#000000'))

# Integrar todos los elementos en una sola gráfica
plot_1 = (rule + line + text).properties(
    width=350,
    height=175,
    title=f'Consumo de Cigarros Semanales. {name}'
)

# Definir límites del eje y
y_lim = [int(df_affections['Nivel de Afecto'].min()-1), int(df_affections['Nivel de Afecto'].max()+1)]

# Asignar color a cada tipo de afecto
domain_c = ['Media Positivo', 'Positivo', 'Negativo', 'Media Negativo']
range_c = ['green', 'steelblue', 'firebrick', 'black']

# Seleccionar hasta la semana 12
df_affections = df_affections[df_affections['Semana'].astype(int).isin([4, 5, 6, 7, 8, 12, 20, 32])]

# Crear la gráfica de líneas
weeks = df_affections['Semana'].unique().tolist()
line = alt.Chart(df_affections).mark_line().encode(
    x=alt.X('Semana:O', title='Semanas de Evaluación', axis=alt.Axis(tickCount=df_affections.shape[0], grid=False), sort=weeks),
    y=alt.Y('Nivel de Afecto:Q', title='Niveles de Afecto', scale=alt.Scale(domain=y_lim), axis=alt.Axis(grid=False, tickCount=len(range(y_lim[0], y_lim[-1])))),
    color=alt.Color('Tipo', legend=alt.Legend(title='Tipo y Nivel de Afecto'), scale=alt.Scale(domain=domain_c, range=range_c)),
    strokeWidth=alt.condition(
        "(datum.Tipo == 'Media Negativo') | (datum.Tipo == 'Media Positivo')",
        alt.value(2),
        alt.value(4)
    ),
    )

# Integrar todos los elementos en una sola gráfica
plot_2 = (line).properties(
    width=350,
    height=175,
    title=f'Niveles de Afecto. {name}'
)

# Definir límites del eje x e y
x_lim = [1, data_users['Semana'].max()]
y_lim = [0, int(1.1*data_users['Cigarros'].max())+10]

# Crear la gráfica de área
area = alt.Chart(data_users).mark_area().encode(
    x=alt.X('Semana:O', title='Semanas', axis=alt.Axis(grid=False)),
    y=alt.Y('Cigarros:Q', axis=alt.Axis(grid=False)),
    color='Usuario:N'
)

# Aplicar la regla de división por sección de Línea Base, Tratamiento y Seguimiento
rule = alt.Chart(sections).mark_rule(
    color='red',
    strokeWidth=1
).encode(
    x=alt.X('Semana:O',)
).transform_filter((alt.datum.Semana == 4) | (alt.datum.Semana == 8) | (alt.datum.Semana == 12) | (alt.datum.Semana == 20) | (alt.datum.Semana == 32))

# Integrar textos, usando el DataFrame de secciones
text = alt.Chart(sections).mark_text(
    align='right',
    baseline='middle',
    fontWeight=alt.FontWeight('bold'),
    dy=-90, # -132
    size=12
).encode(x=alt.X('Semana:O',),
        text='Etiqueta',
        color=alt.value('#000000'))

plot_3 = (area + rule + text).properties(
    width=1550,
    height=650,
    title=f'Consumo de Cigarros Semanales. Todos los Usuarios'
)

# Insertar gráfica
st.altair_chart((plot_1 | plot_2).configure_axisX(labelAngle=0))
st.altair_chart(plot_3.configure_axisX(labelAngle=0))

# ===============================================================================================================================================
# Integrar tablas con los resultados de ANOVAS
# ===============================================================================================================================================

# Definir formato CSS para eliminar los índices de la tabla, centrar encabezados, aplicar líneas de separación y cambiar tipografía
hide_table_row_index = """
                        <style>
                        tbody th {display:none;}
                        .blank {display:none;}
                        .col_heading {font-family: monospace; border: 3px solid white; text-align: center !important;}
                        </style>
                       """

# Integrar el CSS con Markdown
# st.markdown(hide_table_row_index, unsafe_allow_html=True)

# Importar información de ANOVAS y Bonferroni
anova_df = pd.read_csv('https://raw.githubusercontent.com/miguellosoyo/phd_tesis/main/ANOVAS.csv', encoding='latin')
bonferroni_df = pd.read_csv('https://raw.githubusercontent.com/miguellosoyo/phd_tesis/main/Post%20Hoc%20Bonferroni.csv', encoding='latin')

st.subheader('ANOVA del Consumo de Tabaco')
anova_consumption = anova_df[anova_df['Escenario']=='Consumo'].copy()
st.table(anova_consumption)

st.subheader('Contraste Post Hoc de Bonferroni para el Consumo de Tabaco')
bonferroni_consumption = bonferroni_df[bonferroni_df['Escenario']=='Consumo'].copy()
st.table(bonferroni_consumption)

st.subheader('ANOVA sobre el Afecto Positivo')
anova_positive = anova_df[anova_df['Escenario']=='Afecto Positivo'].copy()
st.table(anova_positive)

st.subheader('Contraste Post Hoc de Bonferroni para el Afecto Positivo')
bonferroni_positive = bonferroni_df[bonferroni_df['Escenario']=='Afecto Positivo'].copy()
st.table(bonferroni_positive)

st.subheader('ANOVA sobre el Afecto Negativo')
anova_negative = anova_df[anova_df['Escenario']=='Afecto Negativo'].copy()
st.table(anova_negative)

st.subheader('Contraste Post Hoc de Bonferroni para el Afecto Negativo')
bonferroni_negative = bonferroni_df[bonferroni_df['Escenario']=='Afecto Negativo'].copy()
st.table(bonferroni_negative)
