# Neostats
# 📊 Excel-Based Chatbot using Local LLM

This project is a simple chatbot that allows users to upload an Excel file and ask questions about the data in plain English. It works completely offline using a local Mistral-7B model (GGUF format) and does not require any API key.

## ✅ Features

- Upload `.xlsx` Excel files
- Ask natural language questions (e.g., "What is the average quantity ordered?")
- Get text-based answers or automatic charts
- Offline and private (no internet required)
- Built with Streamlit for an easy-to-use web interface

## 🛠 Technologies Used

- **Streamlit** – Web interface
- **Pandas** – Excel file processing
- **Plotly** – For generating charts
- **llama-cpp-python** – Running local Mistral model
- **Mistral-7B-Instruct** – The language model used for answering queries

## 🔧 Setup Instructions
After activation of virtual environment:
1. Clone this repo and install dependencies
   pip install -r requirements.txt
   
2.From HuggingFace
Place the .gguf file in the models/ folder

3.Run the app:
streamlit run main.py
