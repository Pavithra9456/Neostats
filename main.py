import streamlit as st
from excel_processor import load_excel, preprocess
from chatbot import generate_response

st.set_page_config(page_title="Excel Insight Assistant")
st.title("📊 Excel-Based Chat Assistant")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = load_excel(uploaded_file)
    processed_df = preprocess(df)
    st.success("Excel file successfully processed!")

    st.dataframe(processed_df.head())

    query = st.text_input("Ask your question:")
    if st.button("Submit") and query:
        with st.spinner("Thinking..."):
            response = generate_response(query, processed_df)
            if isinstance(response, str):
                st.write(response)
            else:
                st.plotly_chart(response)
