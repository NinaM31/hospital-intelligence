from gpt_utils import ask_gpt, dataframe_to_text

SCHEMA_CONTEXT = """
Hospital Data Warehouse Schema:

1. visit_fact
- visit_id
- patient_id
- doctor_id
- date_id
- total_cost
- insurance_covered

2. treatment_fact
- treatment_id
- visit_id
- treatment_name
- treatment_cost
- treatment_type

3. doctor_dim
- doctor_id
- department
- specialization
- location
- first_name
- last_name

4. patient_dim
- patient_id
- first_name
- last_name
- dob
- gender
- address
- city

5. date_dim
- date_id
- yyyy_mm_dd
- year
- month
- day
- quarter

Relationships:
- visit_fact.doctor_id = doctor_dim.doctor_id
- visit_fact.patient_id = patient_dim.patient_id
- visit_fact.date_id = date_dim.date_id
- treatment_fact.visit_id = visit_fact.visit_id
"""

import re
def clean_sql_output(sql: str) -> str:
    sql = sql.strip()

    # Remove ```sql  ```
    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```\s*", "", sql)
    sql = re.sub(r"\s*```$", "", sql)
    return sql.strip()

def build_sql_prompt(user_question):
    return f"""
        You are an expert at converting natural language questions into SQLite queries
        USE ONLY THIS SCHEMA:
        {SCHEMA_CONTEXT}

        Rules:
        - Return only the SQL query
        - Use SQLite syntax
        - Do not explain
        - Do not use tables or columns outside the schema
        - Use joins when needed

        User question:
        {user_question}
    """

def build_nl2sql_insight_prompt(df):
    table_text = dataframe_to_text(df)

    prompt = f"""
        You are an expert data warehouse analyst.

        The following OLAP result comes from a hospital data warehouse.

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

def generate_sql(uesr_question):
    prompt = build_sql_prompt(uesr_question)
    return clean_sql_output(ask_gpt(prompt))