# Streamlit App for Classifying Gemini or OpenAI responses using LastMile AI's alBERTa model
Fine-tuned [alBERTa model](https://docs.lastmileai.dev/autoeval/models/) on Gemini and OpenAI responses using the [LastMile AI AutoEval platform](https://docs.lastmileai.dev/autoeval/). 

How was it fine-tuned?
1. The training dataset is composed of 800 natural language question and answers. All questions were sampled from https://ai.google.com/research/NaturalQuestions.
2. Data cleaning of the natural questions and standardizing on the format
3. Ran all 800 natural language questions in OpenAI (model=gpt4o-mini) and Gemini (model=gemini-1.5-flash)
4. All responses were cleaned for symbols, markdown, and other stylistic indicators that may be too telling on whether it's Gemini or OpenAI
5. Output was set to 400 randomly selected responses from openai and the other 400 were gemini
6. OpenAI responses were mapped to label 0, Gemini responses were mapped to label 1
Final dataset in csv format (https://drive.google.com/file/d/1MYuEV_dFLlXw-pZu7Rrtbvwj26fvgC82/view?usp=sharing)
7. LastMile AI's AutoEval platform (https://lastmileai.dev/models) was used to fine-tune the alBERTa model on this dataset
8. Model scores were callibrated where the threshold was set to 0.552
