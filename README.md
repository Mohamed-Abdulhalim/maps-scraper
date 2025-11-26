Lead Finder – Automated Google Maps Scraper & Lead Pipeline

A production-grade pipeline that turns Google Maps into clean, structured business leads.
Scrape → Clean → Enrich → Upsert → View in a live dashboard.

Built for real-world use: scalable scraping, automated cleaning, deduplication, and a live Supabase-powered UI deployed on Vercel.

✨ Highlights (Why This Project Feels Enterprise-Level)
Full Google Maps Extraction

Scrapes names, phones, websites, addresses, ratings, reviews, photos, categories, and deep profile details.

Uses Selenium + undetected-chromedriver, rotating UA/languages, randomized delays, and periodic browser restarts to avoid bans.

Industrial-grade Cleaning & Normalization

Fixes and standardizes phone numbers, addresses, URLs, and social links.

Extracts price info where available.

Removes duplicate businesses and duplicate photos.

Produces clean, analysis-ready datasets.

Phone Enrichment Layer

Revisits profiles missing phone numbers and pulls them directly from the business’s detailed section.

Supabase Cloud Database (Upsert Logic)

Final data is upserted into PostgreSQL (via Supabase).

Idempotent inserts keyed by profile URL ensure no duplicates ever.

Batch upserts for performance.

CI/CD Automation

GitHub Actions runs the full pipeline (scrape → clean → enrich → upload) on a schedule.

Rotates target cities each run for wide geographic coverage.

Zero manual intervention required.

Live Dashboard UI

Flask backend + Vercel deployment.

Search by category / location.

Fast pagination, mobile-friendly UI, instant data access.

Security Built-In

No credentials in code.

.env.example provided for local dev.

Production secrets stored in GitHub Secrets.

🛠️ Tech Stack

Python 3.11

Selenium, undetected-chromedriver

Supabase (PostgreSQL)

GitHub Actions (CI)

Flask (dashboard + API)

HTML/JS frontend (Vercel)

📂 Project Structure
maps-scraper/
├── maps.py             # Main scraper → results.csv
├── csv_cleaner.py      # Cleans & normalizes → Cleaned.csv
├── phone_enricher.py   # Fills missing phones → Enriched.csv
├── supabase_push.py    # Upsert into Supabase
├── app.py              # Flask API + dashboard
├── templates/index.html
├── categories.txt
├── requirements.txt
└── .github/workflows/scrape.yml

⚙️ Local Setup

Install packages

pip install -r requirements.txt


Create .env

SUPABASE_URL=...
SUPABASE_SERVICE_ROLE=...


Run pipeline

py maps.py --categories-file categories.txt --location "Cairo, Egypt" --max-places 20 --output results.csv --headless
py csv_cleaner.py --in results.csv --out Cleaned.csv
py phone_enricher.py --in Cleaned.csv --out Enriched.csv
py supabase_push.py Enriched.csv


Run dashboard

export SUPABASE_URL=...
export SUPABASE_ANON_KEY=...
py app.py


Visit: http://localhost:5000

🕒 Automation (GitHub Actions)

The pipeline runs automatically on schedule:

Headless scrape

Cleaning

Phone enrichment

Upsert to Supabase

Rotate to next city

Trigger manually via Actions → Run workflow.

💡 Use Cases

Lead generation for sales teams

Local business intelligence

Market research

Building directories or location-based apps

Automated client data collection for agencies/consultants

🔮 Roadmap

Excel / Notion export

Email enrichment

Rating / “open now” filters in UI

Multi-region parallel scraping

Advanced analytics dashboard

📜 License

MIT License.

🙋‍♂️ Author

Mohamed Abdulhalim
Data scraping, automation, Supabase & Python development.
LinkedIn: https://www.linkedin.com/in/halim99/
