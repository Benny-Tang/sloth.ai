import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from agents.compliance_agent import MODEL, analyze_updates
from scraper.regulatory_scraper import scrape_regulatory_updates

app = FastAPI(title="Sloth AI", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@app.get("/health")
async def health():
    return {
        "status": "online",
        "system": "Sloth AI",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "model": MODEL,
    }


@app.get("/api/scan")
async def scan():
    """Scrape regulatory sources and return raw results, no AI analysis."""
    try:
        return {"success": True, "data": scrape_regulatory_updates()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/alerts")
async def alerts():
    """Scrape + analyze: returns structured, actionable compliance alerts."""
    try:
        scraped = scrape_regulatory_updates()
        analyzed = await analyze_updates(scraped)
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "scan_status": scraped.get("status"),
            "alerts": analyzed,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(BASE_DIR, "frontend.html")) as f:
        return f.read()
