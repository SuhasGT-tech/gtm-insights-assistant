import pandas as pd
import requests

df = pd.read_csv("sales_pipeline.csv")

HF_TOKEN = "your_openrouter_key_here"

def ask_question(question):
    product_summary = df.groupby("Product")["Deal_Value_USD"].sum().to_string()
    region_summary = df.groupby("Region")["Deal_Value_USD"].sum().to_string()
    rep_summary = df.groupby("Sales_Rep")["Deal_Value_USD"].sum().to_string()

    full_prompt = f"""You are a GTM data analyst. Answer clearly with numbers.

Sales by Product:
{product_summary}

Sales by Region:
{region_summary}

Sales by Rep:
{rep_summary}

Question: {question}
Answer:"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": "Bearer your_openrouter_key_here"},
        json={
            "model": "openrouter/auto:free",
            "messages": [{"role": "user", "content": full_prompt}]
        }
    )
    result = response.json()
    return result["choices"][0]["message"]["content"]

print("GTM Insights Assistant 🚀")
print("Type your question or 'exit' to quit\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    answer = ask_question(question)
    print(f"AI: {answer}\n")