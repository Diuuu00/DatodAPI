import streamlit as st
import requests
import pandas as pd

BASE = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes"

st.set_page_config(page_title="Carburantes España", layout="wide")
st.title("Consulta de Carburantes en  España")

tab1, tab2, tab3 = st.tabs([
    "Estaciones por CCAA",
    "Postes Marítimos",
    "Precios por Provincia y Fecha"
])

# ── TAB 1: Estaciones por CCAA ──────────────────────────────────────────────
with tab1:
    st.header("Estaciones de Servicio por Comunidad Autónoma")

    @st.cache_data
    def get_ccaa():
        r = requests.get(f"{BASE}/Listados/ComunidadesAutonomas/")
        return r.json()

    @st.cache_data
    def get_estaciones_ccaa(id_ccaa):
        r = requests.get(f"{BASE}/EstacionesTerrestres/FiltroCCAA/{id_ccaa}")
        return r.json()

    ccaa_data = get_ccaa()
    ccaa_dict = {c["IDCCAA"]: c["CCAA"] for c in ccaa_data}
    ccaa_sel = st.selectbox("Selecciona una Comunidad Autónoma",
                            options=list(ccaa_dict.keys()),
                            format_func=lambda x: ccaa_dict[x])

    if st.button("Buscar estaciones", key="btn1"):
        with st.spinner("Cargando..."):
            datos = get_estaciones_ccaa(ccaa_sel)
            lista = datos.get("ListaEESSPrecio", [])
            if lista:
                df = pd.DataFrame(lista)
                st.success(f"{len(df)} estaciones encontradas")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No se encontraron estaciones.")

# ── TAB 2: Postes Marítimos ─────────────────────────────────────────────────
with tab2:
    st.header("Postes Marítimos por Provincia")

    @st.cache_data
    def get_provincias():
        r = requests.get(f"{BASE}/Listados/Provincias/")
        return r.json()

    @st.cache_data
    def get_maritimos_provincia(id_prov):
        r = requests.get(f"{BASE}/PostesMaritimos/FiltroProvincia/{id_prov}")
        return r.json()

    provincias = get_provincias()
    prov_dict = {p["IDPovincia"]: p["Provincia"] for p in provincias}
    prov_sel = st.selectbox("Selecciona una Provincia",
                            options=list(prov_dict.keys()),
                            format_func=lambda x: prov_dict[x])

    if st.button("Buscar postes marítimos", key="btn2"):
        with st.spinner("Cargando..."):
            datos = get_maritimos_provincia(prov_sel)
            lista = datos.get("ListaEESSPrecio", [])
            if lista:
                df = pd.DataFrame(lista)
                st.success(f"{len(df)} postes encontrados")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No se encontraron postes marítimos para esta provincia.")

# ── TAB 3: Precios por Provincia, Fecha y Carburante ───────────────────────
with tab3:
    st.header("Precios de Carburantes por Provincia, Fecha y Tipo")

    @st.cache_data
    def get_productos():
        r = requests.get(f"{BASE}/Listados/ProductosPetroliferos/")
        return r.json()

    @st.cache_data

    def get_precios_fecha_provincia(fecha, id_prov, id_prod):
        r = requests.get(
            f"{BASE}/EstacionesTerrestresHist/FiltroProvinciaProducto/{fecha}/{id_prov}/{id_prod}",
            headers={"Accept": "application/json; charset=utf-8"}
        )
        r.encoding = "utf-8-sig"
        return r.json()
    col1, col2, col3 = st.columns(3)

    with col1:
        provincias2 = get_provincias()
        prov_dict2 = {p["IDPovincia"]: p["Provincia"] for p in provincias2}
        prov_sel2 = st.selectbox("Provincia",
                                 options=list(prov_dict2.keys()),
                                 format_func=lambda x: prov_dict2[x])
    with col2:
        fecha_sel = st.date_input("Fecha")

    with col3:
        productos = get_productos()
        prod_dict = {p["IDProducto"]: p["NombreProducto"] for p in productos}
        prod_sel = st.selectbox("Carburante",
                                options=list(prod_dict.keys()),
                                format_func=lambda x: prod_dict[x])

    if st.button("Buscar precios", key="btn3"):
        with st.spinner("Cargando..."):
            fecha_str = fecha_sel.strftime("%d-%m-%Y")
            datos = get_precios_fecha_provincia(fecha_str, prov_sel2, prod_sel)
            lista = datos.get("ListaEESSPrecio", [])
            if lista:
                df = pd.DataFrame(lista)
                st.success(f"{len(df)} estaciones encontradas")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No se encontraron datos para esa combinación.")







