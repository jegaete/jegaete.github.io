"""
Sincroniza la colección _projects/ con los "Funding" de ORCID.

ORCID manda en los datos básicos de cada proyecto:
  title, title_en (título traducido), years, date, funder (institución + programa),
  grant_number, type (award) y website (solo si la ficha no tiene uno propio).
  También se actualiza la línea "**Período:** ..." del texto de la ficha.

Se conservan tal como estén en la página:
  role, project_number, el texto de la ficha (debajo del front matter) y cualquier
  otro campo que no sea de los anteriores. Para que un campo no se toque, agregar
  su nombre a la lista `keep:` de la ficha, p. ej.  keep: [funder, years]

- Cada ficha queda vinculada a ORCID con `orcid_put_code`.
- Proyectos nuevos en ORCID -> se crea una ficha con "Descripción pendiente".
- Proyectos que ya no están en ORCID -> se borra la ficha solo si es un borrador
  ("Descripción pendiente"); si tiene texto propio, se avisa y se deja.

Uso:  python .github/scripts/sync_orcid_projects.py
"""
import datetime
import difflib
import os
import re
import sys
import unicodedata

import requests
import yaml

ORCID_ID = "0000-0002-6650-6018"
PROJECTS_DIR = "_projects"
STUB_MARKER = "*Descripción pendiente."
HEADERS = {"Accept": "application/json",
           "User-Agent": "jegaete.github.io projects sync (mailto:jgaete@uandes.cl)"}

# Nombres cortos de instituciones frecuentes
ORG_SHORT = {
    "Agencia Nacional de Investigación y Desarrollo": "ANID",
    "Ministerio de Educación, Gobierno de Chile": "Ministerio de Educación de Chile",
}
# "Tipos" de ORCID que no aportan información al lector
GENERIC_TYPES = {"donación", "donacion", "licitación", "licitacion", "grant", "contract", "award"}

# Orden de los campos en el front matter
KEY_ORDER = ["title", "title_en", "collection", "type", "permalink", "excerpt", "date",
             "years", "funder", "grant_number", "role", "website", "orcid_put_code",
             "project_number", "keep"]
DROP_FIELDS = {"status"}   # "En curso" se calcula en la página a partir de years


def slugify(text, max_length=50):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_length].rstrip("-")


def norm_title(t):
    return re.sub(r"\s+", " ", slugify(t or "", 1000).replace("-", " ")).strip()


def get_json(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def fetch_orcid():
    data = get_json(f"https://pub.orcid.org/v3.0/{ORCID_ID}/fundings")
    put_codes = [s["put-code"] for g in data.get("group", []) for s in g.get("funding-summary", [])]
    out = []
    for pc in put_codes:
        f = get_json(f"https://pub.orcid.org/v3.0/{ORCID_ID}/funding/{pc}")
        title = ((f.get("title") or {}).get("title") or {}).get("value", "").strip()
        if not title:
            continue
        ids = ((f.get("external-ids") or {}).get("external-id")) or []
        out.append({
            "put_code": pc,
            "type": f.get("type") or "",
            "title": re.sub(r"\s+", " ", title).strip(),
            "title_en": (((f.get("title") or {}).get("translated-title") or {}).get("value") or "").strip(),
            "org_type": ((f.get("organization-defined-type") or {}).get("value") or "").strip(),
            "org": ((f.get("organization") or {}).get("name") or "").strip(),
            "start": (((f.get("start-date") or {}).get("year") or {}).get("value") or ""),
            "end": (((f.get("end-date") or {}).get("year") or {}).get("value") or ""),
            "grant_number": "; ".join(i.get("external-id-value", "") for i in ids
                                      if i.get("external-id-type") == "grant_number"),
            "url": ((f.get("url") or {}).get("value") or "").strip(),
        })
    return out


def funder_label(p):
    org = ORG_SHORT.get(p["org"], p["org"])
    t = p["org_type"]
    if t and t.lower() not in GENERIC_TYPES:
        return f"{org} — {t}"
    return org


def years_label(p):
    s, e = p["start"], p["end"]
    if s and e and s != e:
        return f"{s}–{e}"
    return s or e


def read_project(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)


def write_project(path, fm, body):
    ordered = {k: fm[k] for k in KEY_ORDER if k in fm and fm[k] not in (None, "", [])}
    for k, v in fm.items():
        if k not in ordered and k not in DROP_FIELDS and v not in (None, "", []):
            ordered[k] = v
    front = yaml.safe_dump(ordered, allow_unicode=True, sort_keys=False, width=10000).strip()
    body = body if body.startswith("\n") else "\n" + body
    content = f"---\n{front}\n---\n{body}"
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if content != old:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def refresh_body(body, fm):
    """Actualiza la línea '**Período:** ...' del texto de la ficha con los años de ORCID."""
    if "years" in set(fm.get("keep") or []) or not fm.get("years"):
        return body
    return re.sub(r"(\*\*Período:\*\*\s*)[0-9]{4}(?:\s*[-–]\s*[0-9]{4})?",
                  lambda m: m.group(1) + str(fm["years"]), body)


def apply_orcid(fm, p):
    keep = set(fm.get("keep") or [])
    new = {
        "title": p["title"],
        "title_en": p["title_en"],
        "type": "award" if p["type"] == "award" else "",
        "date": datetime.date(int(p["start"] or 2000), 1, 1),
        "years": years_label(p),
        "funder": funder_label(p),
        "grant_number": p["grant_number"],
    }
    for k, v in new.items():
        if k in keep:
            continue
        if v:
            fm[k] = v
        else:
            fm.pop(k, None)
    if p["url"] and not fm.get("website") and "website" not in keep:
        fm["website"] = p["url"]
    fm["orcid_put_code"] = p["put_code"]
    fm["collection"] = "projects"
    if "excerpt" not in keep:
        role = fm.get("role")
        fm["excerpt"] = f"{fm.get('funder', '')}{' — ' + str(role) if role else ''} ({fm.get('years', '')})"
    return fm


def match(p, files, used):
    """Busca la ficha existente que corresponde a un proyecto de ORCID."""
    for name, (fm, _) in files.items():
        if name not in used and fm.get("orcid_put_code") == p["put_code"]:
            return name
    expected = f"{p['start'] or '2000'}-{slugify(p['title'])}.md"
    if expected in files and expected not in used and not files[expected][0].get("orcid_put_code"):
        return expected
    best, best_score = None, 0.0
    for name, (fm, _) in files.items():
        if name in used or fm.get("orcid_put_code"):
            continue
        same_year = str(fm.get("date", ""))[:4] == str(p["start"])
        score = difflib.SequenceMatcher(None, norm_title(fm.get("title")), norm_title(p["title"])).ratio()
        if same_year and score > best_score:
            best, best_score = name, score
    return best if best_score >= 0.8 else None


def main():
    projects = fetch_orcid()
    if not projects:
        sys.exit("ORCID no devolvió proyectos; no se modifica nada.")
    os.makedirs(PROJECTS_DIR, exist_ok=True)

    files = {}
    for name in sorted(os.listdir(PROJECTS_DIR)):
        if name.endswith(".md"):
            fm, body = read_project(os.path.join(PROJECTS_DIR, name))
            if fm is not None:
                files[name] = (fm, body)

    used, created, updated = set(), [], []
    for p in projects:
        name = match(p, files, used)
        if name:
            used.add(name)
            fm, body = files[name]
            fm = apply_orcid(dict(fm), p)
            body = refresh_body(body, fm)
            if write_project(os.path.join(PROJECTS_DIR, name), fm, body):
                updated.append(name)
        else:
            year = p["start"] or "2000"
            slug = slugify(p["title"])
            name = f"{year}-{slug}.md"
            i = 2
            while name in files or os.path.exists(os.path.join(PROJECTS_DIR, name)):
                name = f"{year}-{slug}-{i}.md"
                i += 1
            fm = apply_orcid({"permalink": f"/projects/{name[:-3]}/"}, p)
            body = f"\n{STUB_MARKER} Editar este archivo para agregar información del proyecto.*\n"
            write_project(os.path.join(PROJECTS_DIR, name), fm, body)
            files[name] = (fm, body)
            used.add(name)
            created.append(name)

    deleted, orphans = [], []
    for name, (fm, body) in files.items():
        if name in used:
            continue
        if STUB_MARKER in body:
            os.remove(os.path.join(PROJECTS_DIR, name))
            deleted.append(name)
        else:
            orphans.append(name)

    print(f"ORCID: {len(projects)} proyectos")
    for label, items in (("Actualizadas", updated), ("Creadas", created), ("Borradas (borradores)", deleted)):
        print(f"{label}: {len(items)}")
        for n in items:
            print(f"  - {n}")
    if orphans:
        print("AVISO — fichas con texto propio que ya no están en ORCID (no se borran):")
        for n in orphans:
            print(f"  - {n}")


if __name__ == "__main__":
    main()
