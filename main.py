import streamlit as st

st.title("Aplicación de Streamlit con 2 Pestañas")

# Crea las pestañas
tab1, tab2 = st.tabs(["Pestaña 1", "Pestaña 2"])

# Contenido de la Pestaña 1
with tab1:
    st.header("Bienvenido a la Pestaña 1")
    st.write("Este es el contenido de la primera pestaña.")
    st.image("https://via.placeholder.com/300", caption="Imagen de ejemplo")

# Contenido de la Pestaña 2
with tab2:
    st.header("Bienvenido a la Pestaña 2")
    st.write("Este es el contenido de la segunda pestaña.")
    st.line_chart({"data": [1, 5, 2, 6, 8, 3]})
