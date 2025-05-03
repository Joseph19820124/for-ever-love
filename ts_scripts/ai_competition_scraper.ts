import axios from 'axios';
import * as cheerio from 'cheerio';
import * as fs from 'fs';

async function scrapeAICompetition(): Promise<{ [key: string]: string }> {
    const companies = ["OpenAI", "xAI", "Gemini", "Anthropic"];
    const results: { [key: string]: string } = {};

    for (const company of companies) {
        const url = `https://www.google.com/search?q=${company}+latest+LLM+version`;
        try {
            const response = await axios.get(url);
            const $ = cheerio.load(response.data);
            
            // Extract the latest LLM version from the search results
            const latestVersion = $('.BNeawe').first().text() || 'Not found';
            results[company] = latestVersion;
        } catch (error) {
            console.error(`Error fetching data for ${company}:`, error);
            results[company] = 'Error';
        }
    }

    return results;
}

async function main() {
    const data = await scrapeAICompetition();
    const report = `# AI Competition Report\n\n` +
        Object.entries(data).map(([company, version]) => 
            `## ${company}\nLatest LLM Version: ${version}\n\n`
        ).join('');

    fs.writeFileSync('report.md', report, 'utf-8');
}

main().catch(console.error);
