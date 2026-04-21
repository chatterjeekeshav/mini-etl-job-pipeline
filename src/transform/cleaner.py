def transform_jobs(data):
    cleaned = []

    for job in data:
        cleaned.append({
            "job_id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "category": job.get("category", {}).get("label"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "posted_date": job.get("created")
        })

    return cleaned