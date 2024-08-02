import streamlit as st
import requests

st.set_page_config(page_title="Clasificador de Texto", page_icon="📚")
st.title("Clasificador de Texto")

codigo = st.number_input("Ingrese el código:", min_value=1)
texto = st.text_area("Ingrese el texto a clasificar:", height=200)

if st.button("Clasificar"):
    if texto:
        response = requests.post('http://localhost:8008/clasificar', json={'codigo': codigo, 'valor': texto})

        if response.status_code == 200:
            data = response.json()
            st.subheader(f"Resultados de la clasificación para el código {data['codigo']}:")
            for label, score in zip(data['labels'], data['scores']):
                st.write(f"{label}: {score:.2f}%")
            
            st.markdown("---")
            highest_label = data['highest']['label']
            highest_score = data['highest']['score']
            if highest_score > 70:
                st.success(f"Clasificación principal: {highest_label}")
                st.info(f"Puntaje más alto: {highest_score:.2f}%")
            else:
                st.warning("No fue posible clasificar el texto con un puntaje mayor al 70%")
        else:
            st.error("Error al clasificar el texto.")
    else:
        st.error("Por favor, ingrese un texto para clasificar.")

st.markdown("---")
st.subheader("Historial de Clasificaciones")

historial_response = requests.get("http://localhost:8008/historial")
if historial_response.status_code == 200:
    historial = historial_response.json()
    for item in historial:
        st.write(f"Código: {item['codigo']}, Clasificación: {item['highest']['label']} ({item['highest']['score']}%)")
else:
    st.error("Error al obtener el historial.")

st.markdown("---")
st.markdown("CREADO POR: ERICK HUMBERTO BONILLA PERUGACHI")



            
        





