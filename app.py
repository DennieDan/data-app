import streamlit as st
import pandas as pd
import json
import os
from pandasai import SmartDatalake, Agent
from pandasai.llm.openai import OpenAI

SAVE_DIR = "/opt/render/project/tmp/"
DB_FILE = os.path.join(SAVE_DIR, "db.json")
NO_DATA_RESPONSE = "No data available for analysis. Please upload your data."
# Initialize llm
openai_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_token=openai_key)

# Streamlit UI
st.title("AI-Powered Data Analyzer 📊")

# Load chat history from db.json
os.makedirs(SAVE_DIR, exist_ok=True)
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r") as chat:
            db = json.load(chat)
            st.session_state.messages = db.get('chat_history', [])
    except (json.JSONDecodeError, IOError):
        st.session_state.messages = []  # Handle corrupt or unreadable file
else:
    st.session_state.messages = []  # File doesn't exist, start fresh

# Display messages
def display_text(message):
    if message.get("type") == "image":
        st.image(message["content"])
    else:
        st.markdown(message["content"])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        display_text(message)


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
agent = Agent(dfs, config={"llm": llm, "save_charts": True, "save_charts_path": SAVE_DIR, "open_charts": False})

# Input Analysis 
if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Ask a question about the data:", key="user_query")

if query:
    # Append user query
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    if not uploaded_files:
        st.session_state.messages.append({"role": "assistant", "content": NO_DATA_RESPONSE})
        with st.chat_message("assistant"):
            st.markdown(NO_DATA_RESPONSE)
    else:
        with st.spinner("Analyzing..."):
            response = agent.chat(query)

            temp_res = None
            # Check if PandasAI generated a plot
            if isinstance(response, str) and response.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                temp_res = {"role": "assistant", "content": response, "type": "image"}
            else:
                temp_res = {"role": "assistant", "content": response, "type": "text"}
            st.session_state.messages.append(temp_res)
            explanation = agent.explain()
            temp_exp = {"role": "assistant", "content": explanation, "type": "text"}
            st.session_state.messages.append(temp_exp)
        
        with st.chat_message("assistant"):
            display_text(temp_res)
            display_text(temp_exp)
    
    # Store chat into db.json
    db = {"chat_history": st.session_state.messages}
    with open(DB_FILE, 'w') as chat:
        json.dump(db, chat, indent=4)