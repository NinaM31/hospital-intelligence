from flask import Flask, render_template, request, jsonify
from olap_queries import OLAP_QUERIES
from nl2sql import generate_sql
from gpt_utils import build_insight_prompt, ask_gpt
from db import get_table_stats, run_query, save_insight, get_insights

app = Flask(__name__)

@app.route("/")
def about_page():
    table_stats = get_table_stats()
    return render_template("about.html", table_stats=table_stats)

@app.route("/insights")
def insights():
    saved_insights = get_insights()
    return render_template("insights.html", saved_insights=saved_insights.to_dict(orient="records"))

@app.route("/olap")
def olap_page(): return render_template("olap.html", queries=OLAP_QUERIES)

@app.route("/olap-run-and-insight", methods=["POST"])
def olap_run_and_insight():
    data = request.get_json()
    query_key = data.get("query_key")
    query_info = OLAP_QUERIES[query_key]
    
    # OLAP query
    df = run_query(query_info["sql"])

    # GPT prompt
    prompt = build_insight_prompt(
        analysis_title=query_info["title"],
        analysis_description=query_info["description"],
        df=df
    )
    gpt_output = ask_gpt(prompt)

    # Save output
    save_insight(
        analysis_title=query_info["title"],
        input_prompt=prompt,
        gpt_output=gpt_output
    )
    return jsonify({
        "query_key": query_key,
        "title": query_info["title"],
        "description": query_info["description"],
        "columns": df.columns.tolist(),
        "rows": df.to_dict(orient="records"),
        "prompt": prompt,
        "gpt_output": gpt_output
    })

@app.route("/nl-to-sql")
def nl2sql_page():
    return render_template("nl2sql.html")

@app.route("/nl-to-sql-run", methods=["POST"])
def nl2sql_generate_and_run():
    data = request.get_json()

    question = data.get("question", "").strip()
    print(question)
    if not question:
        return jsonify({"error": "Question is empty."}), 400

    # Generate SQL
    generated_sql = generate_sql(question)
    print(question)

    # Run SQL (NO DELETE or INSERT)
    if not generated_sql.startswith("SELECT"):
        return jsonify({"error": "Only SELECT queries are allowed"}), 400
    
    try:
        df = run_query(generated_sql)
        print(df)
        return jsonify({
            "question": question,
            "generated_sql": generated_sql,
            "columns": df.columns.tolist(),
            "rows": df.to_dict(orient="records")
        })
    except Exception as e:
        return jsonify({
            "question": question,
            "generated_sql": generated_sql,
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)