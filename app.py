import streamlit as st
import matplotlib.pyplot as plt
from modelo_colesterol import ModeloColesterol

# Título
st.title("Simulador de Niveles de Colesterol")

# Instanciar modelo
modelo = ModeloColesterol()

# Sidebar con controles interactivos
st.sidebar.header("Parámetros")

tipo_dieta = st.sidebar.selectbox(
    "Tipo de dieta:",
    options=[("Baja en grasas", 0.5), ("Normal", 1.0), ("Alta en grasas", 1.5)],
    index=1
)[1]

suplemento_dieta = st.sidebar.slider(
    "Suplemento dietético (mg/dL):", min_value=-200, max_value=200, step=10, value=0
)

ejercicio = st.sidebar.radio("Ejercicio regular:", options=[False, True], index=0)
medicamento = st.sidebar.radio("Toma medicamento:", options=[False, True], index=0)

mostrar_guia = st.sidebar.checkbox("Mostrar guía interpretativa", value=True)

# Ejecutar simulación con parámetros
dias, C_normal = modelo.simular(H=1, ejercicio=False, medicamento=False)
_, C_actual = modelo.simular(H=tipo_dieta, E_extra=suplemento_dieta,
                            ejercicio=ejercicio, medicamento=medicamento)

# Graficar resultados
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dias, C_normal, 'b-', label='Escenario normal', alpha=0.5)
ax.plot(dias, C_actual, 'r-', label='Escenario actual', linewidth=2)
ax.axhline(modelo.Cn, color='g', linestyle='--', label='Nivel normal (Cn)')
ax.set_title('Evolución de los Niveles de Colesterol')
ax.set_xlabel('Días')
ax.set_ylabel('Colesterol (mg/dL)')
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Mostrar información clave
st.markdown(f"""
**RESULTADOS CLAVE:**

- Nivel inicial: {modelo.C0} mg/dL  
- Nivel final: {C_actual[-1]:.1f} mg/dL  
- Diferencia con nivel normal: {C_actual[-1]-modelo.Cn:.1f} mg/dL  
- Máximo alcanzado: {max(C_actual):.1f} mg/dL  

**PARÁMETROS ACTUALES:**

- Factor dieta: {tipo_dieta} {'(alta en grasas)' if tipo_dieta>1 else '(baja en grasas)' if tipo_dieta<1 else '(normal)'}  
- Suplemento dietético: {suplemento_dieta} mg/dL  
- Ejercicio: {"Sí" if ejercicio else "No"}  
- Medicamento: {"Sí" if medicamento else "No"}  
""")

# Guía interpretativa
if mostrar_guia:
    st.markdown("### Guía de interpretación:")
    if C_actual[-1] < 180:
        st.success("✅ Nivel óptimo de colesterol (por debajo de 180 mg/dL)")
    elif 180 <= C_actual[-1] < 200:
        st.warning("⚠ Nivel limítrofe alto (entre 180-200 mg/dL)")
    elif 200 <= C_actual[-1] < 240:
        st.error("❌ Nivel alto (entre 200-240 mg/dL)")
    else:
        st.error("❗❗ Nivel muy alto (240 mg/dL o más) - Consultar con médico")

    if C_actual[-1] > 200:
        st.markdown("""
        **Recomendaciones:**
        - Considerar reducir ingesta de grasas saturadas  
        - Aumentar la actividad física regular  
        - Consultar sobre medicamentos con un profesional
        """)
    elif C_actual[-1] < 160:
        st.markdown("**Recomendaciones:** Nivel saludable, mantener hábitos actuales.")
