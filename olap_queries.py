OLAP_QUERIES = {
    "rollup_revenue_by_department": {
        "title": "Roll-up: Revenue by Department",
        "description": "Aggregates total hospital revenue at the department level",
        "sql": """
            SELECT 
                dd.department,
                ROUND(SUM(vf.total_cost), 2) AS total_revenue
            FROM visit_fact vf
            JOIN doctor_dim dd 
            ON vf.doctor_id = dd.doctor_id
            GROUP BY dd.department
            ORDER BY total_revenue DESC;
        """
    },
    "slice_emergency_department": {
        "title": "Slice: Emergency Department Revenue",
        "description": "Filters the analysis to Emergency Department",
        "sql": """
            SELECT 
                dd.department,
                ROUND(SUM(vf.total_cost), 2) AS total_revenue
            FROM visit_fact vf
            JOIN doctor_dim dd 
            ON vf.doctor_id = dd.doctor_id
            WHERE dd.department = 'Emergency Department'
            GROUP BY dd.department;
        """
    },
    "drilldown_emergency_doctors": {
        "title": "Drill-down: Emergency Department Doctors",
        "description": "Drills down from Emergency Department revenue to doctor-level revenue",
        "sql": """
            SELECT 
                dd.first_name,
                dd.last_name,
                dd.department,
                ROUND(SUM(vf.total_cost), 2) AS total_revenue,
                COUNT(*) AS visit_count
            FROM visit_fact vf
            JOIN doctor_dim dd
            ON vf.doctor_id = dd.doctor_id
            WHERE dd.department = 'Emergency Department'
            GROUP BY dd.doctor_id, dd.first_name, dd.last_name, dd.department
            ORDER BY total_revenue DESC
            LIMIT 10;
    """
    },
    "insurance_revenue": {
        "title": "Insurance Revenue Analysis",
        "description": "Compares revenue and visit count by insurance coverage",
        "sql": """
            SELECT 
                insurance_covered,
                ROUND(SUM(total_cost), 2) AS total_revenue,
                COUNT(*) AS visit_count
            FROM visit_fact
            GROUP BY insurance_covered
            ORDER BY total_revenue DESC;
        """
    },
}