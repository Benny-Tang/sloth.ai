"""
Sloth AI - Regulatory & Compliance Monitoring
Scrapes public regulatory/government bulletin sources and financial news
for jurisdiction-level regulatory changes (tax rate changes, new rules,
compliance deadlines). Falls back to representative simulated data if a
source fails, so the pipeline never breaks on a missing external dependency.
"""
import datetime

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Public regulatory/financial news sources to monitor. Extend this list with
# jurisdiction-specific regulator sites (e.g. SEC, MAS, BNM, FCA) as needed.
SOURCES = [
    {"name": "Reuters Regulatory", "url": "https://www.reuters.com/legal/government/"},
    {"name": "Reuters Tax", "url": "https://www.reuters.com/business/finance/"},
]


def scrape_regulatory_updates():
    items = []
    sources_ok = []

    for source in SOURCES:
        try:
            r = requests.get(source["url"], headers=HEADERS, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                count = 0
                for h in soup.find_all(["h2", "h3"], limit=6):
                    text = h.get_text(strip=True)
                    if 20 < len(text) < 300:
                        items.append({
                            "source": source["name"],
                            "headline": text[:250],
                            "url": source["url"],
                        })
                        count += 1
                if count:
                    sources_ok.append(source["name"])
        except requests.RequestException:
            continue

    if items:
        return {
            "status": "live",
            "sources_ok": sources_ok,
            "items": items[:10],
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

    return {
        "status": "simulated",
        "note": "Live scraping unavailable â€” showing representative regulatory signals",
        "sources_ok": [],
        "items": [
            {"source": "Regulatory Bulletin", "headline": "New cross-border data residency rule takes effect Q1", "jurisdiction": "EU", "url": "#"},
            {"source": "Tax Authority Notice", "headline": "Corporate tax rate revised for financial services sector", "jurisdiction": "Singapore", "url": "#"},
            {"source": "Central Bank Circular", "headline": "Updated KYC/AML reporting thresholds effective immediately", "jurisdiction": "Malaysia", "url": "#"},
            {"source": "Regulatory Bulletin", "headline": "New licensing requirement for digital payment providers", "jurisdiction": "UK", "url": "#"},
        ],
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }
