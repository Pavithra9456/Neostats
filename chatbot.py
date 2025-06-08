from llama_cpp import Llama
import pandas as pd
import re

MODEL_PATH = r"C:\Users\Pavithra Reddy\Desktop\Neostats\models\mistral-7b-instruct-v0.1.Q3_K_M.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4
)

# List of your exact columns normalized (lowercase, no spaces)
VALID_COLUMNS = [
    "ordernumber", "quantityordered", "priceeach", "orderlinenumber", "sales",
    "orderdate", "status", "qtr_id", "month_id", "year_id", "productline",
    "msrp", "productcode", "customername", "phone", "addressline1",
    "addressline2", "city", "state", "postalcode", "country", "territory",
    "contactlastname", "contactfirstname", "dealsize"
]

def generate_prompt(query: str, df: pd.DataFrame) -> str:
    table_md = df.head(20).to_markdown(index=False)
    prompt = f"""
You are an intelligent data assistant. Based on the following table (in markdown format), answer the query below.
If the query asks for a chart, return Python code to create it using plotly.

Data:
{table_md}

Query:
{query}

Answer:
"""
    return prompt

def parse_and_execute(query: str, df: pd.DataFrame):
    query_lower = query.lower()

    # Extract math operation and column name, expecting normalized column names
    math_ops = ["average", "sum", "min", "max", "count"]

    # Normalize column names in df as keys for easy matching
    df_cols = [col.lower().replace(' ', '') for col in df.columns]

    for op in math_ops:
        # regex to match e.g. 'average of quantityordered' or 'sum quantityordered'
        pattern = rf'{op} (of )?([a-z0-9_]+)'
        match = re.search(pattern, query_lower)
        if match:
            operation = op
            col_candidate = match.group(2)

            # Match user column to dataframe columns (handle case and spaces)
            if col_candidate in df_cols:
                col_index = df_cols.index(col_candidate)
                actual_col = df.columns[col_index]
            else:
                # Column not found
                return f"Column '{col_candidate}' not found in the data."

            # Now, check if the operation is valid on this column
            if operation in ["average", "sum", "min", "max"]:
                if pd.api.types.is_numeric_dtype(df[actual_col]):
                    if operation == "average":
                        return f"The average of '{actual_col}' is {df[actual_col].mean():.2f}."
                    elif operation == "sum":
                        return f"The sum of '{actual_col}' is {df[actual_col].sum():.2f}."
                    elif operation == "min":
                        return f"The minimum value of '{actual_col}' is {df[actual_col].min()}."
                    elif operation == "max":
                        return f"The maximum value of '{actual_col}' is {df[actual_col].max()}."
                else:
                    return f"Column '{actual_col}' is not numeric and cannot perform '{operation}'."
            elif operation == "count":
                return f"The count of non-null entries in '{actual_col}' is {df[actual_col].count()}."

    # If no math operation found, fallback to LLM prompt
    summary_md = df.describe(include='all').to_markdown()
    prompt = f"""
You are a helpful data assistant.

Here is a summary of the data:

{summary_md}

Query:
{query}

Answer:
"""
    response = llm(prompt)
    return response["choices"][0]["text"].strip()

def generate_response(query: str, df: pd.DataFrame):
    try:
        answer = parse_and_execute(query, df)
        return answer
    except Exception as e:
        return f"Error processing your query: {e}"
