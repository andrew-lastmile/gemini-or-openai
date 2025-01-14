import streamlit as st
import requests
import json
import os

# Configuration
API_URL = "https://lastmileai.dev/api/2/auto_eval/evaluation/evaluate"  # LastMile AI Inference URL
LASTMILE_API_TOKEN = st.secrets["LASTMILE_API_TOKEN"]  # Replace with your API token
MODEL_ID = st.secrets["MODEL_ID"] # Replace with you autoeval model id
TIMEOUT = 30  # Timeout for each request in seconds
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {LASTMILE_API_TOKEN}'
}
THRESHOLD = 0.5525525525525525

def create_bar(score, label, color):
    # Truncate to 2 decimal places
    truncated_score = f"{score:.2f}"

    # Create the HTML for the progress bar
    bar_html = f"""
    <div style="
        width: 100%;
        background-color: #e0e0e0;
        padding: 3px;
        border-radius: 5px;
        ">
        <div style="
            width: 100%;
            height: 24px;
            display: flex;
            ">
            <div style="
                width: {score * 100}%;
                background-color: {color};
                border-radius: 3px 0 0 3px;
                text-align: center;
                line-height: 24px;
                color: white;
                ">
                {truncated_score} {label}
            </div>
        </div>
        <div style="
            position: absolute;
            left: 55%;
            top: -25px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        ">
            <span style="
                font-size: 12px;
                color: #333;
                margin-bottom: 4px;
            ">
                Threshold
            </span>
            <div style="
                height: 32px;
                width: 2px;
                background-color: grey;
            "></div>
        </div>
    </div>
    """

    # Use st.markdown to render the HTML
    st.markdown(bar_html, unsafe_allow_html=True)
    st.write("\n")

# Streamlit App
st.title("🕵️‍♂️ OpenAI or Gemini?")
st.caption("by [LastMile AI](%s)" % "https://www.lastmileai.dev")
st.markdown('''
:blue-background[Write your question and answer (the LLM response) and the model will predict whether the response is OpenAI or Gemini.]  The model was fine-tuned on the alBERTa model from LastMile AI.
''')
st.markdown('''```
Example: 
    Question - who sings in cry baby for johnny depp
    OpenAI Answer - In the film "Cry Baby," which stars Johnny Depp, the character "Wade "Cry Baby" Walker" typically does not sing in the traditional sense. Instead, various musical performances in the film feature a number of artists from the 1950s rock and roll era, specifically the character's band and other vocal performances. The music was produced primarily by composer and musician John Waters, the director of the film. However, the character played by Johnny Depp performs a song called "Cry Baby,"
    Gemini Answer - Melanie Martinez sings in the music video for her song "Cry Baby," which features Johnny Depp. He doesn't sing, he only acts in the video.
```''')
with st.expander("See explanation"):
    st.write('''
        1. The training dataset is composed of 800 natural language question and answers. All questions were sampled from https://ai.google.com/research/NaturalQuestions.
        2. Data cleaning of the natural questions and standardizing on the format
        3. Ran all 800 natural language questions in OpenAI (model=gpt4o-mini) and Gemini (model=gemini-1.5-flash)
        4. All responses were cleaned for symbols, markdown, and other stylistic indicators that may be too telling on whether it's Gemini or OpenAI
        5. Output was set to 400 randomly selected responses from openai and the other 400 were gemini
        6. OpenAI responses were mapped to label 0, Gemini responses were mapped to label 1
        Final dataset in csv format (https://drive.google.com/file/d/1MYuEV_dFLlXw-pZu7Rrtbvwj26fvgC82/view?usp=sharing)
        7. LastMile AI's AutoEval platform (https://lastmileai.dev/models) was used to fine-tune the alBERTa model on this dataset
        8. Model scores were callibrated where the threshold was set to 0.552
    ''')

# Input fields for question and answer
question = st.text_input("Question (your input):", placeholder="Type your question here...")
answer = st.text_area("Answer (LLM output):", placeholder="Type your answer here...")

# Function to assign a score (0 to 1)
def classify_question_answer(question, answer):
    # Request payload and headers
    payload = json.dumps({
        "metric": {
            "id": MODEL_ID
        },
        "input": [
            question
        ],
        "output": [
            answer
        ]
    })
    score = 0
    try:
        response = requests.post(API_URL, headers=HEADERS, data=payload, timeout=TIMEOUT)
        response_data = json.loads(response.text)
        print(response_data)
        score = response_data["scores"][0]
    except Exception as e:
        print(e)

    return score

# Button to classify
if st.button("Classify"):
    if question and answer:
        score = classify_question_answer(question, answer)
        if score is not None :
            if score <= THRESHOLD:
                st.subheader(":green-background[OpenAI]")
                create_bar(score, "OpenAI", "#0ca37f")
            else:
                st.subheader(":blue-background[Gemini]")
                create_bar(score, "Gemini", "#248bf4")
        else:
            st.error("Please provide both a question and an answer.")
    else:
        st.error("Both question and answer are required for classification.")
