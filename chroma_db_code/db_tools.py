import psycopg2


def get_customer(customer_id):

    conn = psycopg2.connect(
        host="localhost",
        database="loandb",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            customer_name,
            cibil_score,
            income,
            loan_type
        FROM customers
        WHERE customer_id=%s
        """,
        (customer_id,)
    )

    result = cur.fetchone()

    conn.close()

    return result
