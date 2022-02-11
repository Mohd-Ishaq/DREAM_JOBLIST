from app.models import Jobs
from .router import jobs_applied
from fastapi import FastAPI
from .router import recruiters
from .router import jobs
from .router import seekers
from .router import auth


app = FastAPI()

app.include_router(recruiters.router)
app.include_router(jobs.router)
app.include_router(seekers.router)
app.include_router(auth.router)
app.include_router(jobs_applied.router)


@app.get("/")
def hello():
    return "hello world!"
