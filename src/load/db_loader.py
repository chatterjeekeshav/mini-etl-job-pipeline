import psycopg2
from psycopg2.extras import execute_batch


def load_to_db(df):
    conn = None

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="job_pipeline",
            user="postgres",
            password="1234"
        )

        cursor = conn.cursor()

        insert_query = """
            INSERT INTO jobs (
                job_id, title, company, location,
                category, salary_min, salary_max, posted_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_id) DO NOTHING;
        """

        data_tuples = [
            (
                row["job_id"],
                row["title"],
                row["company"],
                row["location"],
                row["category"],
                row["salary_min"],
                row["salary_max"],
                row["posted_date"]
            )
            for _, row in df.iterrows()
        ]

        execute_batch(cursor, insert_query, data_tuples)

        conn.commit()
        print(f"✅ {len(df)} records inserted successfully.")

    except Exception as e:
        print(f"❌ Error loading data: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()