import streamlit as st
import pandas as pd
from pandasai import SmartDatalake, Agent
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
    uploaded_files = st.file_uploader("Upload CSV or Excel file", accept_multiple_files=True, type=["csv", "xlsx"])

data_frames = {}

if uploaded_files:
    for file in uploaded_files:
        file_extension = file.name.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(file)
        else:
            xls = pd.ExcelFile(file)
            sheet_name = st.selectbox("Select a sheet", xls.sheet_names)
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
        data_frames[file.name] = df

if data_frames:
    selected_file = st.sidebar.selectbox("Select a file to view", list(data_frames.keys()))
    # Get basic data
    df = data_frames[selected_file]
    df_nrows = len(df)

    # Display top N rows
    def update_slider():
        st.session_state.slider = st.session_state.numeric
    def update_numin():
        st.session_state.numeric = st.session_state.slider
    
    val = st.sidebar.number_input("Select the number of rows to display", value = 0, key = "numeric", on_change=update_slider)
    n_rows = st.sidebar.slider("Slide to select", value = val, key = 'slider', 
                    min_value=0, max_value=df_nrows,
                    on_change=update_numin)
    st.sidebar.write(f"### Viewing: {selected_file}")
    st.sidebar.dataframe(df.head(n_rows))

# SmartDatalake
agent = Agent(list(data_frames.values()), config={"llm": llm, "save_charts": False, "open_charts": False})

# Input Analysis 
if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Ask a question about the data:", key="user_query")

if query:
    if not uploaded_files:
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": "No data available for analysis. Please upload your data."})
    else:
        with st.spinner("Analyzing..."):
            response = agent.chat(query)

            # Append user query
            st.session_state.messages.append({"role": "user", "content": query})

            # Check if PandasAI generated a plot
            if isinstance(response, str) and response.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                st.session_state.messages.append({"role": "assistant", "content": response, "type": "image"})
            else:
                st.session_state.messages.append({"role": "assistant", "content": response, "type": "text"})

            explanation = agent.explain()
            st.session_state.messages.append({"role": "assistant", "content": explanation, "type": "text"})

    # Display messages
    def display_text(message):
        if message.get("type") == "image":
            st.image(message["content"])
        else:
            st.markdown(message["content"])

    for i in range(len(st.session_state.messages)):
        message = st.session_state.messages[i]
        if i > 0 and message["role"] == st.session_state.messages[i - 1]["role"]:
            display_text(message)
        else:
            with st.chat_message(message["role"]):
                display_text(message)