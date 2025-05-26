import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Pestaña de navegación
st.set_page_config(page_title="Simulador y Calculadora de Colesterol")

menu = ["Simulador", "Calculadora"]
choice = st.sidebar.selectbox("Selecciona una opción", menu)

# =========================
# SECCIÓN 1: SIMULADOR
# =========================
if choice == "Simulador":
    st.title("Simulador de Colesterol")
    st.markdown("""
    Este simulador permite observar cómo evolucionan los niveles de colesterol total, LDL y HDL a lo largo del tiempo,
    según hábitos saludables o no saludables.
    """)

    # Entradas del usuario
    semanas = st.slider("Número de semanas a simular", min_value=4, max_value=52, step=1, value=12)
    colesterol_inicial = st.number_input("Colesterol total inicial (mg/dL)", min_value=100.0, max_value=400.0, value=200.0)
    ldl_inicial = st.number_input("LDL inicial (mg/dL)", min_value=50.0, max_value=300.0, value=130.0)
    hdl_inicial = st.number_input("HDL inicial (mg/dL)", min_value=20.0, max_value=100.0, value=50.0)

    estilo_vida = st.selectbox("Estilo de vida", ["Saludable", "No saludable"])

    # Cálculo de variaciones semanales
    if estilo_vida == "Saludable":
        delta_colesterol = -0.5
        delta_ldl = -0.7
        delta_hdl = 0.2
    else:
        delta_colesterol = 0.6
        delta_ldl = 0.8
        delta_hdl = -0.2

    # Simulación
    semanas_array = np.arange(semanas)
    colesterol = colesterol_inicial + delta_colesterol * semanas_array
    ldl = ldl_inicial + delta_ldl * semanas_array
    hdl = hdl_inicial + delta_hdl * semanas_array

    # Gráficas
    fig, ax = plt.subplots()
    ax.plot(semanas_array, colesterol, label="Colesterol Total", color='orange')
    ax.plot(semanas_array, ldl, label="LDL", color='red')
    ax.plot(semanas_array, hdl, label="HDL", color='green')
    ax.set_xlabel("Semanas")
    ax.set_ylabel("Nivel (mg/dL)")
    ax.set_title("Evolución del colesterol")
    ax.legend()
    st.pyplot(fig)

# =========================
# SECCIÓN 2: CALCULADORA
# =========================
elif choice == "Calculadora":
    st.title("Calculadora de Colesterol LDL")
    st.markdown("""
    Utiliza la fórmula de Friedewald para estimar el colesterol LDL:

    **LDL = Colesterol Total - HDL - (Triglicéridos / 5)**

    Asegúrate de ingresar los valores en mg/dL.
    """)

    colesterol_total = st.number_input("Colesterol Total (mg/dL)", min_value=100.0, max_value=400.0, value=200.0)
    hdl = st.number_input("HDL (mg/dL)", min_value=20.0, max_value=100.0, value=50.0)
    trigliceridos = st.number_input("Triglicéridos (mg/dL)", min_value=50.0, max_value=500.0, value=150.0)

    if st.button("Calcular LDL"):
        ldl = colesterol_total - hdl - (trigliceridos / 5)
        st.success(f"El colesterol LDL estimado es: {ldl:.2f} mg/dL")
