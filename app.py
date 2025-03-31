import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from lida import Manager, TextGenerationConfig
import matplotlib.pyplot as plt

# Initialize LIDA
openai_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(api_token=openai_key)
manager = Manager()

# Streamlit UI
st.title("AI-Powered Data Analyzer 📊")

# Side bar

with st.sidebar:
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Select a sheet", xls.sheet_names)
            df = pd.read_excel(xls, sheet_name=sheet_name)

        # Get basic data
        df_nrows = len(df)
        # Create SmartDataFrame with LLM
        sdf = SmartDataframe(df, config={"llm": llm, "save_charts": False})

        # Display top N rows
        def update_slider():
            st.session_state.slider = st.session_state.numeric
        def update_numin():
            st.session_state.numeric = st.session_state.slider
        
        val = st.sidebar.number_input("Select the number of rows to display", value = 0, key = "numeric", on_change=update_slider)
        n_rows = st.sidebar.slider("Slide to select", value = val, key = 'slider', 
                        min_value=0, max_value=df_nrows,
                        on_change=update_numin)
        st.sidebar.dataframe(df.head(n_rows))

# Input Analysis
if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Ask a question about the data:", key="user_query")

if query:
    if not uploaded_file:
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": "No data available for analysis. Please upload your data."})
    else:
        with st.spinner("Analyzing..."):
            response = sdf.chat(query)
            st.write(isinstance(response, plt.Figure))

            # Append user query
            st.session_state.messages.append({"role": "user", "content": query})

            # Check if PandasAI generated a plot
            if isinstance(response, str) and response.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                st.session_state.messages.append({"role": "assistant", "content": response, "type": "image"})
            else:
                st.session_state.messages.append({"role": "assistant", "content": response, "type": "text"})

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("type") == "image":
                st.image(message["content"])  # Display as image
            else:
                st.markdown(message["content"])  # Display as text 