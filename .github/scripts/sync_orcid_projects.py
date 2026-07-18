import requests
import os
import re
import unicodedata
from datetime import datetime

ORCID_ID = "0000-0002-6650-6018"
PROJECTS_DIR = "_projects"
STUB_MARKER = "*Descripción pendiente."

def slugify(text, max_length=50):
    # Normalize to ASCII (removes accents: á→a, ñ→n, etc.)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text[:max_length].rstrip('-')

def get_grant_number(external_ids):
    for eid in external_ids.get('external-id', []):
        if eid.get('external-id-type') == 'grant_number':
            return eid.get('external-id-value', '')
    return ''

def main():
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/fundings"
    resp = requests.get(url, headers={'Accept': 'application/json'}, timeout=15)
    data = resp.json()

    os.makedirs(PROJECTS_DIR, exist_ok=True)
    current_year = datetime.now().year

    # Build the canonical set of filenames from ORCID
    orcid_projects = []
    correct_filenames = set()

    for group in data.get('group', []):
        grant_number = get_grant_number(group.get('external-ids', {}))
        for summary in group.get('funding-summary', []):
            title = summary.get('title', {}).get('title', {}).get('value', '')
            if not title:
                continue

            start = summary.get('start-date') or {}
            end   = summary.get('end-date') or {}
            start_year = (start.get('year') or {}).get('value', '')
            end_year   = (end.get('year')   or {}).get('value', '')
            funder = (summary.get('organization') or {}).get('name', '')

            year = start_year or '2000'
            slug = slugify(title)
            filename = f"{year}-{slug}.md"
            correct_filenames.add(filename)
            orcid_projects.append((filename, title, year, start_year, end_year, funder, grant_number))

    # --- Cleanup: delete auto-generated stubs that no longer match any ORCID slug ---
    existing_files = set(os.listdir(PROJECTS_DIR))
    deleted_count = 0
    for fname in list(existing_files):
        if fname in correct_filenames:
            continue
        filepath = os.path.join(PROJECTS_DIR, fname)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if STUB_MARKER in content:
                os.remove(filepath)
                print(f"Deleted stale stub: {fname}")
                deleted_count += 1
        except Exception as e:
            print(f"Error reading {fname}: {e}")

    # --- Create stubs for new projects not yet in the repo ---
    existing_files = set(os.listdir(PROJECTS_DIR))
    new_count = 0

    for filename, title, year, start_year, end_year, funder, grant_number in orcid_projects:
        if filename in existing_files:
            print(f"Skipped (exists): {filename}")
            continue

        years_str = f"{start_year}–{end_year}" if end_year else start_year
        is_active = end_year and int(end_year) >= current_year
        status = "active" if is_active else "completed"
        excerpt = f"{funder} ({years_str})" if funder else years_str
        title_safe = title.replace('"', '\\"')
        funder_safe = funder.replace('"', '\\"')
        slug = slugify(title)

        content = f"""---
title: "{title_safe}"
collection: projects
permalink: /projects/{year}-{slug}/
excerpt: "{excerpt}"
date: {year}-01-01
years: "{years_str}"
status: {status}
funder: "{funder_safe}"
grant_number: "{grant_number}"
---

{STUB_MARKER} Editar este archivo para agregar información del proyecto.*
"""
        filepath = os.path.join(PROJECTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filename}")
        new_count += 1

    print(f"\nDone. Deleted {deleted_count} stale stub(s), created {new_count} new project(s).")

if __name__ == '__main__':
    main()
