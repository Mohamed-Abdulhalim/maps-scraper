#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import math
from flask import Flask, jsonify, request, render_template
from supabase import create_client, Client

APP_PORT = int(os.environ.get("PORT", "5000"))
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE", "places")

app = Flask(__name__, static_folder=None, template_folder="templates")

# --------- Supabase client ----------
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("Set SUPABASE_URL and SUPABASE_ANON_KEY env vars for read-only UI.")

sb = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Columns your UI expects (keep these in sync with your table)
COLUMNS = [
    "name",
    "category",
    "query_location",
    "category_line",
    "address_line",
    "phone",
    "phone_e164",
    "website",
    "website_fallback",
    "profile_url",
    "rating",
    "reviews_count",
    "opening_hours",
    "is_open_now",
    "today_time_hint",
    "hours_note",
    "gmaps_primary_category",
    "main_photo_url",
    "photo_urls",
]

# ---------- Helpers ----------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def to_str(x):
    return "" if x is None else str(x)

def list_categories() -> list[str]:
    # fetch, then dedupe client-side
    res = sb.table(SUPABASE_TABLE).select("category").execute()
    cats = sorted({(r.get("category") or "").strip() for r in res.data if r.get("category")})
    # sensible default if table is empty
    return cats or ["restaurants", "clinics", "gyms"]

def list_locations() -> list[str]:
    res = sb.table(SUPABASE_TABLE).select("query_location").execute()
    locs = sorted({(r.get("query_location") or "").strip() for r in res.data if r.get("query_location")})
    return locs or ["Cairo, Egypt"]

def parse_photos(row):
    raw = to_str(row.get("photo_urls"))
    photos = []
    if raw:
        for part in raw.split(","):
            u = part.strip()
            if u.startswith("http"):
                photos.append(u)
    if not row.get("main_photo_url") and photos:
        row["main_photo_url"] = photos[0]
    row["photos"] = photos
    return row

# ---------- Routes ----------
@app.get("/")
def index():
    return render_template(
        "index.html",
        categories=list_categories(),
        locations=list_locations(),
    )

@app.get("/search")
def search():
    category = request.args.get("category", "", type=str)
    location = request.args.get("location", "", type=str)
    page     = max(1, request.args.get("page", default=1, type=int))
    per_page = max(1, min(100, request.args.get("per_page", default=20, type=int)))

    start = (page - 1) * per_page
    end   = start + per_page - 1  # Supabase range is inclusive

    q = sb.table(SUPABASE_TABLE).select("*", count="exact")
    if category:
        q = q.eq("category", category)
    if location:
        q = q.eq("query_location", location)

    # best-effort ordering; won't break if rating column is missing
    try:
        q = q.order("rating", desc=True)
    except Exception:
        pass

    res = q.range(start, end).execute()
    rows = res.data or []
    total = res.count or len(rows)
    pages = max(1, math.ceil(total / per_page))

    items = []
    for row in rows:
        # normalize Nones -> ""
        row = {k: ("" if v is None else v) for k, v in row.items()}

        # photo handling: support both comma list in photo_urls and optional main_photo_url
        raw = (row.get("photo_urls") or "").strip()
        photos = [u.strip() for u in raw.split(",") if u.strip().startswith("http")]
        main_photo = row.get("main_photo_url") or (photos[0] if photos else "")
        row["photos"] = photos
        row["main_photo_url"] = main_photo  # front-end already falls back

        items.append(row)

    return jsonify(
        {
            "items": items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT, debug=False)
