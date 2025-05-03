import requests
from bs4 import BeautifulSoup
import json

def scrape_ai_competition():
    companies = ["OpenAI", "xAI", "Gemini", "Anthropic"]
    results = {}

    for company in companies:
        url = f"https://www.google.com/search?q={company}+latest+LLM+version"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the latest LLM version from the search results
        latest_version = soup.find("div", class_="BNeawe").text if soup.find("div", class_="BNeawe") else "Not found"
        results[company] = latest_version

    return results

if __name__ == "__main__":
    data = scrape_ai_competition()
    with open("report.md", "w", encoding="utf-8") as f:
        f.write("# AI Competition Report\n\n")
        for company, version in data.items():
            f.write(f"## {company}\n")
            f.write(f"Latest LLM Version: {version}\n\n")
