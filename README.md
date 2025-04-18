# AI-Powered Data Analyzer App 📊
![fullpage](./images/fullpage.png)

You are finding a faster way to understand your data? This is your solution.

Visit our Data Analyzer App and enjoy exploring your data. Currently there are 2 versions:
* **_Non-prompting storage version_** (Deployed on Streamlit Cloud): [https://dan-data-analyzer.streamlit.app/](https://dan-data-analyzer.streamlit.app/)

    If you prefer a fast and handy application and do not require to store your prompting history, this version is for you. Your privacy is prioritised.

* **_Prompting storage version_** (Deployed on Render): [https://data-analyzer-ybzy.onrender.com/](https://data-analyzer-ybzy.onrender.com/)

    Your prompting history including prompts and responses from the app is saved on the cloud. Kindly navigate to [Warning](#warning-to-be-updated-in-the-future-versions) for security issues.

## Getting Started
1. **Upload data files:** Drag and drop your data file into the app. Only files of type .csv or .xls are accepted. 
    
    You can upload more than 1 data files.

1. **View data files:** Select the data file, data sheet and number of rows you would like to view in the respective order.
![viewdatafile](./images/viewdatafile.png)

1. Ask your Data Analyzer any questions about your data by typing into the text area.
![chat_piechart](./images/chat_piechart.png)

> [!TIP]
>
> 1. As you are able to upload multiple datasets, you are suggested to refer to the specific datasets for each prompt for more accurate and relevant response from our agent. 
>
>       Currently, each sheet in an excel file is considered as a separate dataset and you can refer to each dataset by the **ordinal number** according to the order of being uploaded. Kindly refer to the image for clarification.
> ![tips1](./images/tips1.png)


## Acknowledgements
* OpenAI API Key is provided from **Cyber Sierra (Fort One Technologies Pte Ltd)** 
* Slider (for number of rows) design is adapted from https://discuss.streamlit.io/t/circular-connection-of-slider-and-text-input/11015/4
* First touch of the code including _file uploading_, and _input accepting_ is implemented with the help of OpenAI ChatGPT (GPT 3.5)
* Chat interface is adapted from https://www.youtube.com/watch?v=jpoqXbvP6Co&t=432s
* Store prompting history idea: https://tsjohnnychan.medium.com/a-chatgpt-app-with-streamlit-advanced-version-32b4d4a993fb
* Deploy Streamlit app on Render: https://rosarioogenio.medium.com/deploying-a-streamlit-application-to-render-as-an-alternative-to-heroku-782317a3aa2c

## Warning!!! (To be updated in the future versions)
1. **Security Issues:** The application is currently deployed on a limited resources which limits to 1 user at a time. There is no authentication method; therefore, your prompt can be viewed by the next users. Please kindly ```Clear prompt history``` after finish playing around with the application.
1. **Prompt history:** Even though prompt history is saved, the current file uploaded is not saved between different app launch; therefore, you cannot continue the previous conversation with the agent. The prompt history is only for reference purpose.
