import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH")

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_table_stats():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'gpt_%';
        """)

        tables = cursor.fetchall()
        table_stats = []
        for table in tables:
            table_name = table[0]

            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            record_count = cursor.fetchone()[0]
            table_stats.append({
                "table_name": table_name,
                "record_count": record_count
            })
        return table_stats

def run_query(sql):
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn)

def init_insights_table():
    create_table_sql="""
        CREATE TABLE IF NOT EXISTS gpt_olap_insights(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_title TEXT NOT NULL,
            input_prompt TEXT NOT NULL,
            gpt_output TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    with get_connection() as conn:
        conn.execute(create_table_sql)
        conn.commit()

def save_insight(analysis_title, input_prompt, gpt_output):
    init_insights_table()

    insert_sql="""
        INSERT INTO gpt_olap_insights (analysis_title, input_prompt, gpt_output) VALUES (?,?,?)
    """

    with get_connection() as conn:
        conn.execute(insert_sql, (analysis_title, input_prompt, gpt_output))
        conn.commit()

def get_insights():
    init_insights_table()

    get_insights="""
        SELECT analysis_title, gpt_output, created_at 
        FROM gpt_olap_insights 
        ORDER BY created_at DESC;
    """
    return run_query(get_insights)