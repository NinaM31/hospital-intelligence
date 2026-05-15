from gpt_utils import ask_gpt

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

def generate_sql(uesr_question):
    prompt = build_sql_prompt(uesr_question)
    return clean_sql_output(ask_gpt(prompt))