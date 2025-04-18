from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import os
from app.crawler import crawl_docs

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Doc2MD Crawler Web App"}

@app.get("/crawl")
def crawl_framework(framework: str = Query(..., description="e.g., langchain")):
    if framework not in ["langchain", "langgraph", "pydantic"]:
        return {"error": "Unsupported framework"}
    crawl_docs(framework)
    return {"status": "completed", "framework": framework}

@app.get("/download")
def download_markdown_zip():
    zip_path = "/tmp/docs.zip"
    os.system(f"cd {os.getcwd()}/docs && zip -r {zip_path} .")
    return FileResponse(zip_path, media_type='application/zip', filename="docs.zip")