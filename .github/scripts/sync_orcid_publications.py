"""
Genera _data/publications.yml a partir de ORCID (y Crossref para completar
autores, volumen, número y páginas). Las citas se formatean en APA 7.

- Fuente principal: https://pub.orcid.org/v3.0/<ORCID>/works
- Enriquecimiento: https://api.crossref.org/works/<DOI>
- Si un trabajo no tiene DOI (o Crossref falla), se usan los autores y la cita
  BibTeX guardados en ORCID.
- Exclusiones y publicaciones agregadas a mano: _data/publications_config.yml

Uso:  python .github/scripts/sync_orcid_publications.py
"""
import html
import os
import re
import sys
import time

import requests
import yaml

ORCID_ID = "0000-0002-6650-6018"
CONFIG_PATH = "_data/publications_config.yml"
OUTPUT_PATH = "_data/publications.yml"
HIGHLIGHT_FAMILY = "Gaete"          # apellido que se destaca en negrita
UA = "jegaete.github.io publications sync (mailto:jgaete@uandes.cl)"
ORCID_HEADERS = {"Accept": "application/json", "User-Agent": UA}

SESSION = requests.Session()
AUTHOR_OVERRIDES = {}   # DOI -> lista de autores ("Apellido, N."), desde la configuración


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def get_json(url, headers=None, retries=3):
    for attempt in range(retries):
        try:
            r = SESSION.get(url, headers=headers or {"User-Agent": UA}, timeout=30)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            if attempt == retries - 1:
                print(f"  ! Error consultando {url}: {e}")
                return None
            time.sleep(2 * (attempt + 1))


def clean_text(s):
    """Quita etiquetas HTML/MathML, decodifica entidades y normaliza espacios."""
    if not s:
        return ""
    s = html.unescape(str(s))
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_doi(doi):
    if not doi:
        return ""
    doi = doi.strip().lower()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", doi)
    return doi


def initials(given):
    """'Marcelo A.' -> 'M. A.' ; 'Jean-Paul' -> 'J.-P.' ; 'J.' -> 'J.'"""
    given = clean_text(given).replace(".", ". ")
    parts = []
    for word in given.split():
        sub = [p for p in word.split("-") if p]
        if not sub:
            continue
        parts.append("-".join(f"{p[0].upper()}." for p in sub))
    return " ".join(parts)


def apa_name(family, given):
    family = clean_text(family)
    ini = initials(given)
    name = f"{family}, {ini}" if ini else family
    esc = html.escape(name)
    if HIGHLIGHT_FAMILY.lower() in family.lower():
        esc = f"<strong>{esc}</strong>"
    return esc


def apa_author_list(names):
    """names: lista de strings ya formateados (HTML). Regla APA 7 (hasta 20)."""
    n = len(names)
    if n == 0:
        return ""
    if n == 1:
        return names[0]
    if n == 2:
        return f"{names[0]}, &amp; {names[1]}"
    if n <= 20:
        return ", ".join(names[:-1]) + f", &amp; {names[-1]}"
    return ", ".join(names[:19]) + f", &hellip; {names[-1]}"


def split_name(raw):
    """'Gaete, Jorge' -> ('Gaete','Jorge'); 'Jorge Gaete' -> ('Gaete','Jorge')."""
    raw = clean_text(raw)
    if "," in raw:
        fam, giv = raw.split(",", 1)
        return fam.strip(), giv.strip()
    bits = raw.split()
    if len(bits) == 1:
        return raw, ""
    return bits[-1], " ".join(bits[:-1])


def format_pages(pages):
    pages = clean_text(pages)
    return re.sub(r"\s*[-‐‑–—]+\s*", "–", pages)


def format_apa(authors_html, year, title, journal, volume="", issue="",
               pages="", article_number="", doi="", url=""):
    out = []
    if authors_html:
        out.append(f"{authors_html} ({year or 's.f.'}).")
    else:
        out.append(f"({year or 's.f.'}).")
    t = clean_text(title).rstrip(".")
    if t:
        end = "" if t[-1] in "?!" else "."
        out.append(f"{html.escape(t)}{end}")
    src = ""
    if journal:
        src = f"<em>{html.escape(clean_text(journal))}</em>"
        if volume:
            src += f", <em>{html.escape(clean_text(volume))}</em>"
            if issue:
                src += f"({html.escape(clean_text(issue))})"
        if pages and pages != article_number:
            src += f", {html.escape(format_pages(pages))}"
        elif article_number:
            src += f", Article {html.escape(clean_text(article_number))}"
        src += "."
        out.append(src)
    if doi:
        out.append(f'<a href="https://doi.org/{html.escape(doi)}" target="_blank" rel="noopener">https://doi.org/{html.escape(doi)}</a>')
    elif url:
        out.append(f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(url)}</a>')
    return " ".join(out)


def parse_bibtex(bib):
    """Extrae campos simples de una cita BibTeX guardada en ORCID."""
    fields = {}
    if not bib:
        return fields
    for m in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", bib + "\n", re.S):
        fields[m.group(1).lower()] = clean_text(m.group(2))
    return fields


# ---------------------------------------------------------------------------
# Fuentes
# ---------------------------------------------------------------------------
def fetch_orcid_works():
    data = get_json(f"https://pub.orcid.org/v3.0/{ORCID_ID}/works", ORCID_HEADERS)
    if not data or "group" not in data:
        sys.exit("No se pudo leer ORCID; no se modifica nada.")
    works = []
    for g in data["group"]:
        summaries = g.get("work-summary") or []
        if not summaries:
            continue
        # la versión preferida en ORCID es la de mayor display-index
        s = max(summaries, key=lambda x: int(x.get("display-index") or 0))
        ids = ((g.get("external-ids") or {}).get("external-id")) or []
        doi = ""
        for i in ids:
            if i.get("external-id-type") == "doi":
                doi = normalize_doi(i.get("external-id-value"))
                break
        pd = s.get("publication-date") or {}
        works.append({
            "put_code": s.get("put-code"),
            "type": s.get("type") or "",
            "title": clean_text(((s.get("title") or {}).get("title") or {}).get("value")),
            "journal": clean_text((s.get("journal-title") or {}).get("value")),
            "year": ((pd.get("year") or {}).get("value")) or "",
            "month": ((pd.get("month") or {}).get("value")) or "",
            "doi": doi,
            "url": ((s.get("url") or {}).get("value")) or "",
        })
    return works


def fetch_orcid_details(put_codes):
    """Detalle completo (autores, cita BibTeX) en lotes de 100."""
    details = {}
    put_codes = [str(p) for p in put_codes]
    for i in range(0, len(put_codes), 100):
        chunk = ",".join(put_codes[i:i + 100])
        data = get_json(f"https://pub.orcid.org/v3.0/{ORCID_ID}/works/{chunk}", ORCID_HEADERS)
        for b in (data or {}).get("bulk", []):
            w = b.get("work")
            if w:
                details[w.get("put-code")] = w
    return details


def fetch_crossref(doi):
    data = get_json(f"https://api.crossref.org/works/{requests.utils.quote(doi, safe='/')}")
    return (data or {}).get("message")


def date_parts(msg):
    for key in ("issued", "published-online", "published-print", "published"):
        parts = ((msg.get(key) or {}).get("date-parts") or [[None]])[0]
        if parts and parts[0]:
            return parts
    return [None]


# ---------------------------------------------------------------------------
# Construcción de cada entrada
# ---------------------------------------------------------------------------
def entry_from_crossref(work, msg):
    names = []
    if work["doi"] in AUTHOR_OVERRIDES:
        names = [apa_name(*split_name(a)) for a in AUTHOR_OVERRIDES[work["doi"]]]
    for a in ([] if names else (msg.get("author") or [])):
        if a.get("family"):
            names.append(apa_name(a["family"], a.get("given", "")))
        elif a.get("name"):
            names.append(html.escape(clean_text(a["name"])))
    parts = date_parts(msg)
    year = str(parts[0]) if parts[0] else work["year"]
    month = f"{parts[1]:02d}" if len(parts) > 1 and parts[1] else ""
    title = clean_text((msg.get("title") or [work["title"]])[0]) or work["title"]
    journal = clean_text((msg.get("container-title") or [work["journal"]])[0]) or work["journal"]
    return {
        "year": year, "month": month, "title": title, "journal": journal,
        "apa": format_apa(apa_author_list(names), year, title, journal,
                          msg.get("volume", ""), msg.get("issue", ""),
                          msg.get("page", ""), msg.get("article-number", ""),
                          work["doi"]),
    }


def entry_from_orcid(work, detail):
    names, bib = [], {}
    if detail:
        for c in ((detail.get("contributors") or {}).get("contributor")) or []:
            cn = ((c.get("credit-name") or {}).get("value")) or ""
            if cn:
                names.append(apa_name(*split_name(cn)))
        cit = detail.get("citation") or {}
        if (cit.get("citation-type") or "").lower() == "bibtex":
            bib = parse_bibtex(cit.get("citation-value"))
    if not names and bib.get("author"):
        names = [apa_name(*split_name(a)) for a in re.split(r"\s+and\s+", bib["author"]) if a.strip()]
    journal = work["journal"] or bib.get("journal", "")
    return {
        "year": work["year"], "month": work["month"],
        "title": work["title"], "journal": journal,
        "apa": format_apa(apa_author_list(names), work["year"], work["title"], journal,
                          bib.get("volume", ""), bib.get("number", ""), bib.get("pages", ""),
                          "", work["doi"], work["url"]),
    }


def entry_from_manual(m):
    names = [apa_name(*split_name(a)) for a in m.get("authors", [])]
    doi = normalize_doi(m.get("doi", ""))
    year = str(m.get("year", ""))
    return {
        "id": m.get("id") or f"manual-{year}-{re.sub(r'[^a-z0-9]+', '-', m.get('title', '').lower())[:40]}",
        "year": year, "month": f"{int(m['month']):02d}" if m.get("month") else "",
        "title": clean_text(m.get("title")), "journal": clean_text(m.get("journal")),
        "doi": doi, "source": "manual",
        "apa": format_apa(apa_author_list(names), year, m.get("title", ""), m.get("journal", ""),
                          str(m.get("volume", "")), str(m.get("issue", "")), str(m.get("pages", "")),
                          str(m.get("article_number", "")), doi, m.get("url", "")),
    }


ERRATUM = re.compile(r"^(erratum|correction|corrigendum|retraction)\b", re.I)


def main():
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    exclude_codes = {int(x) for x in (cfg.get("exclude_put_codes") or [])}
    exclude_dois = {normalize_doi(x) for x in (cfg.get("exclude_dois") or [])}
    exclude_types = set(cfg.get("exclude_types") or ["preprint"])
    for doi, authors in (cfg.get("author_overrides") or {}).items():
        AUTHOR_OVERRIDES[normalize_doi(doi)] = list(authors or [])

    works = fetch_orcid_works()
    print(f"ORCID: {len(works)} trabajos")

    kept = [w for w in works
            if w["put_code"] not in exclude_codes
            and w["doi"] not in exclude_dois
            and w["type"] not in exclude_types]
    print(f"Tras exclusiones: {len(kept)}")

    need_detail = [w["put_code"] for w in kept if not w["doi"]]
    details = fetch_orcid_details(need_detail) if need_detail else {}

    entries, seen_dois, crossref_fail = [], set(), []
    for w in kept:
        if w["doi"] and w["doi"] in seen_dois:
            continue
        e = None
        if w["doi"]:
            msg = fetch_crossref(w["doi"])
            time.sleep(0.1)
            if msg:
                e = entry_from_crossref(w, msg)
            else:
                crossref_fail.append(w["doi"])
                details.update(fetch_orcid_details([w["put_code"]]))
        if e is None:
            e = entry_from_orcid(w, details.get(w["put_code"]))
        if ERRATUM.match(e["title"]):
            print(f"  - Omitida (fe de erratas): {e['title'][:70]}")
            continue
        e.update({"id": w["put_code"], "doi": w["doi"], "source": "orcid"})
        if w["doi"]:
            seen_dois.add(w["doi"])
        entries.append(e)

    for m in cfg.get("manual") or []:
        e = entry_from_manual(m)
        if e["doi"] and e["doi"] in seen_dois:
            print(f"  - Manual ya presente en ORCID, se omite: {e['title'][:60]}")
            continue
        entries.append(e)

    entries.sort(key=lambda e: (str(e["year"]), str(e["month"] or "00"), e["title"].lower()),
                 reverse=True)

    ordered = [{k: e.get(k, "") for k in
                ("id", "year", "month", "title", "journal", "doi", "source", "apa")}
               for e in entries]
    header = ("# ARCHIVO GENERADO AUTOMÁTICAMENTE desde ORCID + Crossref.\n"
              "# No editar a mano: los cambios se sobrescriben. Para excluir o agregar\n"
              "# publicaciones, editar _data/publications_config.yml.\n")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(ordered, f, allow_unicode=True, sort_keys=False, width=10000)

    print(f"Escritas {len(ordered)} publicaciones en {OUTPUT_PATH}")
    if crossref_fail:
        print("Crossref no encontró estos DOI (se usaron datos de ORCID):")
        for d in crossref_fail:
            print(f"  - {d}")


if __name__ == "__main__":
    main()
