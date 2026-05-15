import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def dataframe_to_text(df, max_rows=15):
    return df.head(max_rows).to_markdown(index=False)

def build_insight_prompt(analysis_title, analysis_description, df):
    table_text = dataframe_to_text(df)

    prompt = f"""
        You are an expert data warehouse analyst.

        The following OLAP result comes from a hospital data warehouse.

        Analysis title:
        {analysis_title}

        Analysis description:
        {analysis_description}

        OLAP result:
        {table_text}

        Generate:
        1. Summary: a concise natural language description of the result.
        2. Insight: the main pattern or observation.
        3. Recommendation: one practical recommendation.

        Rules:
        - Base your answer only on the provided table.
        - Do not invent causes that are not supported by the data.
        - Keep the answer concise and useful.
        - Use clear academic/business language.
    """
    return prompt.strip()


def ask_gpt(prompt):
    if not OPENAI_API_KEY: return "OPENAI_API_KEY is missing. Add it to your .env file."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a careful data warehouse analyst. Only use the provided data."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    return response.choices[0].message.content