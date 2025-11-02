#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, csv, math
from supabase import create_client, Client


SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "places")
INPUT = os.getenv("CLEAN_CSV", "NewResults_clean.csv")
BATCH = int(os.getenv("UPSERT_BATCH", "500"))


sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


rows = []
with open(INPUT, "r", encoding="utf-8-sig", newline="") as f:
r = csv.DictReader(f)
for row in r:
rows.append(row)


for i in range(0, len(rows), BATCH):
chunk = rows[i:i+BATCH]
sb.table(SUPABASE_TABLE).upsert(chunk, on_conflict="profile_url").execute()
