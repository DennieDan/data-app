import streamlit as st
import pandas as pd
from lida import Manager, TextGenerationConfig
import os

# Initialize LIDA
openai_key = st.secrets["OPENAI_API_KEY"]
manager = Manager(TextGenerationConfig(model="gpt-4", api_key=openai_key))

# Streamlit UI
st.title("AI-Powered Data Viewer 📊")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Select a sheet", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=sheet_name)

    # Display top N rows
    n_rows = st.slider("Select number of rows to display", min_value=5, max_value=50, value=10)
    st.dataframe(df.head(n_rows))

    # **LIDA AI Analysis**
    st.subheader("LIDA AI Insights")
    query = st.text_input("Ask a question about the data:")
    
    if st.button("Analyze"):
        insight = manager.summarize(df, query)
        st.write(insight)
