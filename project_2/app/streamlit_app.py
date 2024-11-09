import streamlit as st
import requests
import pandas as pd
from datetime import time

mode = st.sidebar.selectbox("Selecciona el modo", ("Usuario", "Desarrollador"))

api_url = "http://127.0.0.1:8000"

def get_data(endpoint):
    response = requests.get(f"{api_url}/{endpoint}/")
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error(f"Error al decodificar la respuesta de {endpoint}")
            return []
    else:
        st.error(f"Error al obtener datos de {endpoint}")
        return []

def create_data(endpoint, data):
    response = requests.post(f"{api_url}/{endpoint}/", json=data)
    if response.status_code == 200:
        st.success("Registro creado exitosamente")
    else:
        st.error("Error al crear el registro")

def delete_data(endpoint):
    response = requests.delete(f"{api_url}/{endpoint}/clear/")
    if response.status_code == 200:
        st.success("Todos los registros eliminados")
    else:
        st.error("Error al eliminar los registros")

def display_table(data, columns=None):
    if columns:
        df = pd.DataFrame(data, columns=columns)
    else:
        df = pd.DataFrame(data)
    
    for col in df.columns:
        if df[col].dtype == 'object' and col.endswith("_time"):
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%H:%M:%S')
    
    st.table(df)

if mode == "Usuario":
    st.title("Interfaz de Usuario")
    
    table_option = st.selectbox("Seleccione la tabla", ["sellers", "outbound", "inbound", "status_time", "commissions", "prices"])
    
    if st.button("Consultar datos"):
        data = get_data(table_option)
        display_table(data)
    
    if table_option == "sellers":
        st.subheader("Crear nuevo vendedor")
        login = st.text_input("Login")
        name = st.text_input("Nombre")
        hiring_date = st.date_input("Fecha de contratación")
        
        if st.button("Crear registro"):
            new_data = {"login": login, "name": name, "hiring_date": hiring_date.isoformat()}
            create_data("sellers", new_data)

    elif table_option in ["outbound", "inbound"]:
        st.subheader(f"Crear nuevo registro en {table_option}")
        login = st.text_input("Login")
        contacts = st.number_input("Contactos", min_value=0, step=1)
        usefull_contacts = st.number_input("Contactos útiles", min_value=0, step=1)
        sales = st.number_input("Ventas", min_value=0, step=1)
        login_time = st.time_input("Hora de inicio de sesión", time(0, 0))
        
        if st.button("Crear registro"):
            new_data = {
                "login": login,
                "contacts": contacts,
                "usefull_contacts": usefull_contacts,
                "sales": sales,
                "login_time": login_time.strftime("%H:%M:%S")
            }
            create_data(table_option, new_data)

    elif table_option == "status_time":
        st.subheader("Crear nuevo registro en Status Time")
        login = st.text_input("Login")
        talk_time = st.time_input("Tiempo de conversación", time(0, 0))
        acw_time = st.time_input("Tiempo de post-llamada (ACW)", time(0, 0))
        avalible_time = st.time_input("Tiempo disponible", time(0, 0))
        
        if st.button("Crear registro"):
            new_data = {
                "login": login,
                "talk_time": talk_time.strftime("%H:%M:%S"),
                "acw_time": acw_time.strftime("%H:%M:%S"),
                "avalible_time": avalible_time.strftime("%H:%M:%S")
            }
            create_data("status_time", new_data)

    elif table_option == "prices":
        st.subheader("Crear nuevo registro en Prices")
        sales = st.number_input("Sales", min_value=0.0, step=0.1)
        insurance = st.number_input("Insurance", min_value=0.0, step=0.1)
        briefcase = st.number_input("Briefcase", min_value=0.0, step=0.1)
        
        if st.button("Crear registro"):
            new_data = {
                "sales": sales,
                "insurance": insurance,
                "briefcase": briefcase
            }
            create_data("prices", new_data)

    if st.button("Eliminar todos los registros"):
        delete_data(table_option)

elif mode == "Desarrollador":
    st.title("Interfaz de Desarrollador")
    st.write("Ingrese las sentencias SQL para modificar la base de datos.")
    
    sql_query = st.text_area("Escribe tu consulta SQL:")
    
    if st.button("Ejecutar SQL"):
        if sql_query.strip():

            response = requests.post(f"{api_url}/execute_sql", json={"query": sql_query})
            if response.status_code == 200:
                result = response.json()
                st.success("Consulta ejecutada exitosamente")

                if "result" in result and isinstance(result["result"], list):
                    display_table(result["result"])
                else:
                    st.write(result)
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Por favor, ingrese una consulta SQL válida.")