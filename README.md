# Estudio Clínico sobre Consumo del Tabaco

El presente repositorio contiene información sobre un estudio realizado a 21 pacientes. Los nombres que aparecen en los archivos disponibles son pseudónimos para mantener sus identidades. Para evaluar los efectos clínicos de una serie de intervenciones terapéuticas cognitivo-conductuales, se revisa el consumo de cigarros semanales de cada paciente (**Base 1.csv**), así como el nivel de afecto (**Afectos.csv**).

Para validar los efectos de las intervenciones, se emplea el Nonovelap of All Pairs (NAP) como técnica de validación clínica. Cabe mencionar que las mediciones para cada paciente abarcan un rango total de 32 semanas de tratamiento, lo cual permite alcanzar un nivel aceptable en la validación de los resultados. Adicional a esta métrica para la validación de cambios individuales, se efectua un análisis de varianza (ANOVA) para confirmar (o descartar) la presencia de un cambio en el consumo global de todos los pacientes involucrados en el estudio. El cálculo de los ANOVA se realizó con R, es por ello que los resultados se encuentran precargados en los archivos **ANOVAS.csv** y **Post Hoc Bonferroni.csv**

Con el fin de observar los resultados, métricas y tablas de forma visual para cada uno de los pacientes, así como para el grupo en general, se ha desplegado un <a href="https://consumotabaco.streamlit.app/">sitio web</a> desde el que se pueden revisar cada uno de estos elementos de forma interactiva.
