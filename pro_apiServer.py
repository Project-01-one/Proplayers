from fastapi import FastAPI, Query
from get_linkedin_job_data import get_linkedin_job_ids

app = FastAPI()

@app.get("/get_jobs")
def get_jobs(
    keyword: str = Query(..., description="Job title or keyword"),
    time_filter: int = Query(30, description="Filter jobs posted within the last X minutes")
):
    """
    API to fetch LinkedIn job postings based on keyword and time filter.
    Example: /get_jobs?keyword=Data%20Engineer&time_filter=30
    """
    jobs = get_linkedin_job_ids(keyword, time_filter)
    return jobs
