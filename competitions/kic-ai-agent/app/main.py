from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

from .agent import ResearchAgent  # noqa: E402

app = FastAPI(title="KIC Research Agent")


class ResearchRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(req: ResearchRequest):
    return ResearchAgent().run(req.query)
