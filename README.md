# Sloth AI — Regulatory & Tax Compliance Monitoring
**At scale, in real time.**

Sloth AI monitors regulatory bulletins, tax authority notices, and
financial news across multiple jurisdictions, and turns raw headlines into
structured, actionable compliance alerts — each with a severity rating,
plain-language explanation, and a recommended next step.

Originally built for a fintech/regtech hackathon.

## Architecture

```
[Regulatory bulletins / tax notices / financial news]
                    |
           [Regulatory Scraper]
                    |
           [Compliance Agent]  <- Groq LLM: classify severity,
                    |             explain, recommend action
           [FastAPI + Dashboard]
```

## Tech stack

| Layer | Technology |
|---|---|
| LLM | Groq (`openai/gpt-oss-120b`) |
| Scraping | requests + BeautifulSoup |
| Backend | FastAPI |
| Frontend | Single-page dashboard (vanilla JS) |

## Project structure

```
sloth-ai/
├── scraper/
│   └── regulatory_scraper.py   # Pulls headlines from regulatory/news sources
├── agents/
│   └── compliance_agent.py     # Classifies + explains each update via Groq
├── api/
│   └── server.py               # FastAPI: /health, /api/scan, /api/alerts
├── frontend.html
├── requirements.txt
└── README.md
```

## Running locally

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000` and click **Run Compliance Scan**.

## API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | System status |
| `/api/scan` | GET | Raw scraped regulatory headlines, no AI analysis |
| `/api/alerts` | GET | Scraped + analyzed: structured compliance alerts |

## Extending

`scraper/regulatory_scraper.py`'s `SOURCES` list currently points at general
financial/regulatory news. For production use, extend it with
jurisdiction-specific regulator sites (e.g. SEC, MAS, BNM, FCA, HMRC) for
more precise, authoritative signal.

## License

MIT
