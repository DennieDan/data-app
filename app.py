import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from lida import Manager, TextGenerationConfig
import matplotlib.pyplot as plt

# Initialize LIDA
openai_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(api_token=openai_key)
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

    # Get basic data
    df_nrows = len(df)
    # Create SmartDataFrame with LLM
    sdf = SmartDataframe(df, config={"llm": llm})

    # Display top N rows
    def update_slider():
        st.session_state.slider = st.session_state.numeric
    def update_numin():
        st.session_state.numeric = st.session_state.slider
    
    val = st.number_input('Input', value = 0, key = 'numeric', on_change=update_slider)
    n_rows = st.slider("Select number of rows to display", value = val, key = 'slider', 
                       min_value=0, max_value=df_nrows,
                       on_change=update_numin)
    st.dataframe(df.head(n_rows))

    # **LIDA AI Analysis**

    with st.form(key="query_form"):
        query = st.text_input("Ask a question about the data:", key="user_query")
        submit_button = st.form_submit_button(label="Analyze")

    if submit_button and query:
        with st.spinner("Analyzing..."):
                response = sdf.chat(query)
                st.subheader("Response:")
                st.write(response)
        
        # with st.spinner("Generating visualization..."):
        #     insights = manager.visualize(df, query)
        #     fig, ax = plt.subplots()
        #     insights.render(ax=ax)
        #     st.pyplot(fig)
    