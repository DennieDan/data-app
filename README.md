## AI-Powered Data Analyzer App 📊
> **To Cyber Sierra interviewers:**
> Thank you so much for reviewing my application
>
> The application is currently in progress.
> 
> Expected completion date and time: 2 April 12 AM 

![fullpage](./images/fullpage.png)

You are finding a faster way to understand your data? This is your solution.

Visit our Data Analyzer App [here](https://dan-data-analyzer.streamlit.app/) and enjoy exploring your data.

### Getting Started
1. **Upload data files:** Drag and drop your data file into the app. Only files of type .csv or .xls are accepted. 
    
    You can upload more than 1 data files.

1. **View data files:** Select the data file, data sheet and number of rows you would like to view in the respective order.
![viewdatafile](./images/viewdatafile.png)

1. Ask your Data Analyzer any questions about your data by typing into the text area.
![chat_piechart](./images/chat_piechart.png)

### Acknowledgments
* OpenAI API Key is provided from **Cyber Sierra (Fort One Technologies Pte Ltd)** 
* Slider (for number of rows) design is adapted from https://discuss.streamlit.io/t/circular-connection-of-slider-and-text-input/11015/4
* First touch of the code including _file uploading_, and _input accepting_ is implemented with the help of OpenAI ChatGPT (GPT 3.5)
* Chat interface is adapted from https://www.youtube.com/watch?v=jpoqXbvP6Co&t=432s
* Store prompting history idea: https://tsjohnnychan.medium.com/a-chatgpt-app-with-streamlit-advanced-version-32b4d4a993fb
* Deploy Streamlit app on Render: https://rosarioogenio.medium.com/deploying-a-streamlit-application-to-render-as-an-alternative-to-heroku-782317a3aa2c

### Warning!!! (To be updated in the future versions)
1. **Security Issues:** The application is currently deployed on a limited resources which limits to 1 user at a time. There is no authentication method; therefore, your prompt can be viewed by the next users. Please kindly ```Clear prompt history``` after finish playing around with the application.
1. **Prompt history:** Even though prompt history is saved, the current file uploaded is not saved between different app launch; therefore, you cannot continue the previous conversation with the agent. The prompt history is only for reference purpose.