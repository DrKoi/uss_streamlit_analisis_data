import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Solemne 2", layout="wide")
st.title("Solemne 2 - Datos API")

URL = "https://datos.gob.cl/api/3/action/datastore_search"
RID = "b8cb0fbb-3750-4256-ac03-3cd8d50aec9a"

@st.cache_data
def get_d(limit=1000):
    r = requests.get(URL, params={"resource_id": RID, "limit": limit})
    if r.status_code == 200:
        return pd.DataFrame(r.json()["result"]["records"])
    return pd.DataFrame()

df = get_d()

if not df.empty:
    st.subheader("Vista Previa de los datos")
    st.dataframe(df.head())

    st.write("Columnas:", list(df.columns))

    if "A1" in df.columns:
        a = df["A1"].dropna().unique()
        a_sel = st.sidebar.selectbox("Actividad", sorted(a))
        df2 = df[df["A1"] == a_sel]

        st.markdown(f"### Resultados: **{a_sel}**")
        st.dataframe(df2)

        if "A2_1" in df2.columns:
            st.markdown("#### Subcategorías A2_1")
            c = df2["A2_1"].value_counts()
            fig, ax = plt.subplots(figsize=(8, 0.4 * len(c)))  #alto dinámico
            ax.barh(c.index, c.values, color='orange')
            ax.set_title("Subcategorías", fontsize=14)
            ax.set_xlabel("Frecuencia")
            ax.tick_params(axis='y', labelsize=8)  #font más pequeña
            plt.tight_layout()
            st.pyplot(fig)

        if "A4_1" in df2.columns:
            st.markdown("#### Otros valores A4_1")
            st.line_chart(df2["A4_1"].value_counts())
    else:
        st.warning("No hay columna A1")
else:
    st.error("Sin datos")
