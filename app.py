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
            data_frames[file.name] = {"Sheet1": df}
        else:
            xls = pd.ExcelFile(file)
            sheet_name = xls.sheet_names[0]
            # df = pd.read_excel(xls, sheet_name=sheet_name)
            data_frames[file.name] = {str(sheet): pd.read_excel(xls, sheet) for sheet in xls.sheet_names} 
        

if data_frames:
    selected_file = st.sidebar.selectbox("Select a file to view", list(data_frames.keys()))
    selected_sheet = None

    if len(data_frames[selected_file]) > 1:
        selected_sheet = st.sidebar.selectbox("Select a sheet for Excel file", list(data_frames[selected_file].keys()))
    else:
        selected_sheet = list(data_frames[selected_file].keys())[0] 

    # Get basic data
    df = data_frames[selected_file][selected_sheet]
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
    st.sidebar.write(f"### Viewing: {selected_file} - {selected_sheet}")
    st.sidebar.dataframe(df.head(n_rows))

# Panda AI Agent
dfs = [df for inner_dict in data_frames.values() for df in inner_dict.values()]
# Convert column name to str
for data in dfs:
    data.columns = data.columns.astype(str)
agent = Agent(dfs, config={"llm": llm, "save_charts": False, "open_charts": False})

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

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            display_text(message)