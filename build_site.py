#!/usr/bin/env python3
"""
build_site.py — bilingual (DE/EN) static marketing site for a commercial
Vedic-astrology (Jyotiṣa) consulting practice, with Stripe payment links.

Run:    python3 build_site.py
Output: ./website/index.html ...            (German, default)
        ./website/en/index.html ...         (English)

Host the ./website folder on GitHub Pages / Cloudflare Pages / Netlify (free).
Edit BASE + I18N below. Each package has its own Stripe Payment Link.
"""

from pathlib import Path
from html import escape

# ─────────────────────────────────────────────────────────────────────────────
# BASE — shared, language-independent settings
# ─────────────────────────────────────────────────────────────────────────────
BASE = {
    "brand":      "Jyotiṣa Beratung",
    "consultant": "Peter Zanella",
    "city":       "Wädenswil",
    "email":      "kontakt@deine-domain.ch",
    "phone":      "+41 00 000 00 00",
    "domain":     "https://www.deine-domain.ch",   # no trailing slash
    "tool_url":   "https://bed-chart-calc-2nrjb8bmicny8hme55rdrp.streamlit.app",
    "calendly":   "https://calendly.com/dein-name/erstgespraech",
    "languages":  ["de", "en"],   # first = default (served at root)
    # Packages: price + Stripe Payment Link are shared across languages.
    # Create one Payment Link per package in Stripe → paste the URL here.
    "packages": [
        {"id": "birth",   "price": "CHF 180",
         "stripe": "https://buy.stripe.com/test_BIRTH_LINK"},
        {"id": "year",    "price": "CHF 150",
         "stripe": "https://buy.stripe.com/test_YEAR_LINK"},
        {"id": "match",   "price": "CHF 200",
         "stripe": "https://buy.stripe.com/test_MATCH_LINK"},
        {"id": "muhurta", "price": "CHF 120",
         "stripe": "https://buy.stripe.com/test_MUHURTA_LINK"},
    ],
    "show_testimonials": False,
}

# ─────────────────────────────────────────────────────────────────────────────
# I18N — per-language text. Add/adjust freely.
# ─────────────────────────────────────────────────────────────────────────────
I18N = {
    "de": {
        "name": "Deutsch", "code": "de",
        "tagline": "Vedische Astrologie – klar, fundiert, persönlich",
        "intro": ("Dein Geburtshoroskop nach klassischer indischer Astrologie – mit "
                  "Lahiri-Ayanamsha, Vargas, Daśās, Shad Bala und Panchang. Ich übersetze "
                  "die Rechnung in eine verständliche, alltagstaugliche Deutung."),
        "about": ("Ich arbeite seit Jahren mit der vedischen Astrologie (Jyotiṣa) und habe "
                  "das hier verlinkte Berechnungs-Tool selbst entwickelt. In der Beratung "
                  "geht es nicht um starre Vorhersagen, sondern um Orientierung: Stärken, "
                  "Timing (Daśā/Transit) und konkrete Entscheidungen – ruhig und ehrlich."),
        "nav": {"angebot": "Angebot", "ablauf": "Ablauf", "ueber": "Über mich",
                "tool": "Tool", "faq": "FAQ", "book": "Termin buchen"},
        "ui": {"eyebrow_hero": "Jyotiṣa · " + BASE["city"],
               "h_angebot": "Beratungen & Preise",
               "sub_angebot": "Jede Beratung verbindet die exakte Rechnung aus meinem Tool "
                              "mit einer klaren, persönlichen Deutung.",
               "h_ablauf": "In vier Schritten",
               "h_ueber": "Über mich", "h_tool": "Rechne dein Horoskop selbst",
               "tool_p": ("Probiere das Tool aus, mit dem ich arbeite: vollständige vedische "
                          "Berechnung mit Vargas, Daśās, Shad Bala, Panchang und PDF-Export. "
                          "Ideal als Vorbereitung auf die Beratung."),
               "h_faq": "Häufige Fragen", "h_book": "Termin vereinbaren",
               "book_p": ("Wähle ein Paket, bezahle sicher über Stripe und buche danach dein "
                          "Zeitfenster. Du bekommst eine kurze Bestätigung per E-Mail."),
               "btn_pay": "Buchen & bezahlen", "btn_book": "Zeit auswählen",
               "btn_tool": "Kostenloses Horoskop-Tool", "btn_tool2": "Zum Tool →",
               "free": "Kostenlos", "voices": "Stimmen",
               "cookie": ('Diese Seite nutzt für Buchung/Zahlung externe Dienste '
                          '(Calendly, Stripe), die Cookies setzen können.'),
               "cookie_more": "Mehr erfahren", "cookie_ok": "Verstanden",
               "disclaimer": ("Vedische Astrologie dient der persönlichen Reflexion und "
                              "Orientierung. Sie ersetzt keine medizinische, psychologische, "
                              "rechtliche oder finanzielle Beratung. Es werden keine "
                              "bestimmten Ergebnisse garantiert.")},
        "packages": {
            "birth": {"dur": "75 Min", "title": "Geburtshoroskop",
                      "desc": "Tiefenanalyse von Rāśi/Navamsa, Yogas, Shad Bala und der "
                              "aktuellen Daśā-Periode.",
                      "incl": ["Live-Gespräch (Video/vor Ort)", "Persönliches PDF-Horoskop",
                               "Audioaufzeichnung", "2 Wochen Nachfragen per E-Mail"]},
            "year": {"dur": "60 Min", "title": "Jahresprognose",
                     "desc": "Varshaphala plus Daśā/Transit für die nächsten 12 Monate – "
                             "Timing für wichtige Themen.",
                     "incl": ["Live-Gespräch", "Monats-Übersicht als PDF",
                              "Audioaufzeichnung"]},
            "match": {"dur": "75 Min", "title": "Partnerschaft",
                      "desc": "Kompatibilität (Ashtakoota/Guna Milan), Mangal-Dosha und die "
                              "Dynamik beider Horoskope.",
                      "incl": ["Gespräch zu zweit oder allein", "Kompatibilitäts-PDF",
                               "Audioaufzeichnung"]},
            "muhurta": {"dur": "45 Min", "title": "Muhurta – Zeitwahl",
                        "desc": "Günstige Zeitfenster für Hochzeit, Geschäft, Umzug oder Reise.",
                        "incl": ["Konkrete Datums-/Zeitvorschläge", "Begründung je Fenster",
                                 "PDF-Übersicht"]},
        },
        "steps": [("Paket & Zahlung", "Beratung wählen und sicher über Stripe bezahlen."),
                  ("Geburtsdaten", "Datum, Uhrzeit und Ort schicken; ich rechne das Horoskop."),
                  ("Gespräch", "Wir gehen deine Fragen in Ruhe durch – Video oder vor Ort."),
                  ("Unterlagen", "Du erhältst PDF und Aufzeichnung zum Nachhören.")],
        "faq": [("Brauche ich meine genaue Geburtszeit?",
                 "Je genauer, desto besser – Aszendent und Häuser hängen daran. Bei "
                 "unbekannter Zeit ist eine Eingrenzung möglich."),
                ("Ist das eine Vorhersage der Zukunft?",
                 "Nein. Jyotiṣa zeigt Tendenzen, Stärken und Timing. Es ersetzt keine "
                 "medizinische, rechtliche oder finanzielle Beratung."),
                ("Online oder vor Ort?",
                 "Beides – online per Video oder vor Ort nach Absprache."),
                ("Womit rechnest du?",
                 "Mit meinem eigenen Tool: Lahiri-Ayanamsha, Whole-Sign-Häuser, Vargas, "
                 "Vimśottarī-Daśā, Ashtakavarga, Shad Bala u. v. m.")],
        "testimonials": [("„Sehr klare, bodenständige Deutung.“", "M. K., Zürich"),
                         ("„Das Timing-Gespräch hat mir geholfen.“", "S. R., Bern")],
        "legal_titles": {"impressum": "Impressum", "datenschutz": "Datenschutz", "agb": "AGB"},
    },
    "en": {
        "name": "English", "code": "en",
        "tagline": "Vedic astrology — clear, grounded, personal",
        "intro": ("Your birth chart in classical Indian astrology — Lahiri ayanamsha, vargas, "
                  "daśās, Shad Bala and panchang. I turn the calculation into a clear, "
                  "down-to-earth reading you can use."),
        "about": ("I have worked with Vedic astrology (Jyotiṣa) for years and built the chart "
                  "tool linked here myself. A reading is not rigid prediction but orientation: "
                  "strengths, timing (daśā/transit) and real decisions — calm and honest."),
        "nav": {"angebot": "Services", "ablauf": "Process", "ueber": "About",
                "tool": "Tool", "faq": "FAQ", "book": "Book a session"},
        "ui": {"eyebrow_hero": "Jyotiṣa · " + BASE["city"],
               "h_angebot": "Sessions & pricing",
               "sub_angebot": "Every session pairs the exact calculation from my tool with a "
                              "clear, personal interpretation.",
               "h_ablauf": "In four steps",
               "h_ueber": "About me", "h_tool": "Calculate your own chart",
               "tool_p": ("Try the tool I work with: a full Vedic calculation with vargas, "
                          "daśās, Shad Bala, panchang and PDF export. A great way to prepare "
                          "for your session."),
               "h_faq": "FAQ", "h_book": "Book a session",
               "book_p": ("Choose a package, pay securely via Stripe, then pick your time "
                          "slot. You'll get a short confirmation by email."),
               "btn_pay": "Book & pay", "btn_book": "Pick a time",
               "btn_tool": "Free chart tool", "btn_tool2": "Open the tool →",
               "free": "Free", "voices": "Testimonials",
               "cookie": ('This site uses external services for booking/payment '
                          '(Calendly, Stripe) that may set cookies.'),
               "cookie_more": "Learn more", "cookie_ok": "Got it",
               "disclaimer": ("Vedic astrology is for personal reflection and orientation. It "
                              "is not medical, psychological, legal or financial advice, and no "
                              "specific outcomes are guaranteed.")},
        "packages": {
            "birth": {"dur": "75 min", "title": "Birth chart",
                      "desc": "In-depth analysis of Rāśi/Navamsa, yogas, Shad Bala and your "
                              "current daśā period.",
                      "incl": ["Live session (video/in person)", "Personal PDF chart",
                               "Audio recording", "2 weeks of email follow-up"]},
            "year": {"dur": "60 min", "title": "Year ahead",
                     "desc": "Varshaphala plus daśā/transit for the next 12 months — timing "
                             "for the things that matter.",
                     "incl": ["Live session", "Month-by-month PDF", "Audio recording"]},
            "match": {"dur": "75 min", "title": "Relationship",
                      "desc": "Compatibility (Ashtakoota/Guna Milan), Mangal dosha and the "
                              "dynamic between both charts.",
                      "incl": ["Together or on your own", "Compatibility PDF",
                               "Audio recording"]},
            "muhurta": {"dur": "45 min", "title": "Muhurta — timing",
                        "desc": "Favourable windows for marriage, business, a move or travel.",
                        "incl": ["Concrete date/time options", "Reasoning per window",
                                 "PDF summary"]},
        },
        "steps": [("Package & payment", "Choose a session and pay securely via Stripe."),
                  ("Birth details", "Send date, time and place; I cast the chart."),
                  ("The session", "We work through your questions — video or in person."),
                  ("Your files", "You receive the PDF and a recording to revisit.")],
        "faq": [("Do I need my exact birth time?",
                 "The more exact the better — the ascendant and houses depend on it. If it's "
                 "unknown, a rectification can narrow it down."),
                ("Is this fortune-telling?",
                 "No. Jyotiṣa shows tendencies, strengths and timing. It is not a substitute "
                 "for medical, legal or financial advice."),
                ("Online or in person?",
                 "Both — online by video or in person by arrangement."),
                ("What do you calculate with?",
                 "My own tool: Lahiri ayanamsha, whole-sign houses, vargas, Vimśottarī daśā, "
                 "Ashtakavarga, Shad Bala and more.")],
        "testimonials": [("“Clear, grounded reading.”", "M. K., Zurich"),
                         ("“The timing session really helped.”", "S. R., Bern")],
        "legal_titles": {"impressum": "Imprint", "datenschutz": "Privacy", "agb": "Terms"},
    },
}

PAL = {"ink": "#2b2118", "paper": "#fdf6e9", "paper2": "#f6ecd6", "gold": "#b8902f",
       "gold2": "#c9a84a", "accent": "#9a342c", "line": "#e3d6b8", "muted": "#8a7a5c"}

CSS = f"""
:root{{--ink:{PAL['ink']};--paper:{PAL['paper']};--paper2:{PAL['paper2']};
--gold:{PAL['gold']};--gold2:{PAL['gold2']};--accent:{PAL['accent']};
--line:{PAL['line']};--muted:{PAL['muted']};}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);
font-family:'Inter',system-ui,sans-serif;line-height:1.6;font-size:17px}}
h1,h2,h3{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;
line-height:1.1;margin:0 0 .4em}}
h1{{font-size:clamp(2.6rem,6vw,4.4rem);letter-spacing:.5px}}
h2{{font-size:clamp(1.9rem,4vw,2.8rem)}} h3{{font-size:1.35rem}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 24px}}
.eyebrow{{font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;
color:var(--gold);font-weight:600;margin-bottom:.7em}}
.diamond-rule{{display:flex;align-items:center;gap:14px;color:var(--gold);margin:56px 0 40px}}
.diamond-rule::before,.diamond-rule::after{{content:'';flex:1;height:1px;background:var(--line)}}
.btn{{display:inline-block;padding:13px 26px;border-radius:2px;font-weight:600;
font-size:.95rem;transition:.15s;cursor:pointer;border:none}}
.btn-primary{{background:var(--ink);color:var(--paper)}}
.btn-primary:hover{{background:#3c2f20;text-decoration:none}}
.btn-ghost{{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--gold)}}
.btn-ghost:hover{{background:var(--paper2);text-decoration:none}}
header.nav{{position:sticky;top:0;z-index:50;background:rgba(253,246,233,.92);
backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}}
.nav-in{{display:flex;align-items:center;justify-content:space-between;height:64px}}
.brand{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:600;
display:flex;align-items:center;gap:9px;color:var(--ink)}}
.brand .dot{{color:var(--gold)}}
.nav-links{{display:flex;gap:24px;align-items:center}}
.nav-links a{{color:var(--ink);font-size:.92rem}}
.nav-links a:hover{{color:var(--accent);text-decoration:none}}
.lang{{font-size:.82rem;color:var(--muted);border-left:1px solid var(--line);padding-left:18px}}
.lang a{{color:var(--muted)}} .lang a.on{{color:var(--ink);font-weight:600}}
.menu-btn{{display:none;background:none;border:0;font-size:1.5rem;color:var(--ink)}}
.hero{{padding:72px 0 40px}}
.hero-grid{{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}}
.hero p.lead{{font-size:1.18rem;color:#4a3c2a;max-width:46ch;margin:.6em 0 1.6em}}
.hero .cta-row{{display:flex;gap:14px;flex-wrap:wrap}}
.chakra{{width:100%;max-width:380px;margin:0 auto;
filter:drop-shadow(0 8px 24px rgba(120,90,20,.18))}}
.cards{{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin-top:28px}}
.card{{background:var(--paper2);border:1px solid var(--line);border-radius:4px;
padding:26px;display:flex;flex-direction:column}}
.card h3{{margin-bottom:.15em}}
.price{{font-family:'Cormorant Garamond',serif;font-size:2rem;color:var(--accent);
font-weight:600;margin:.1em 0}}
.dur{{font-size:.82rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1em}}
.card ul{{list-style:none;padding:0;margin:14px 0 20px;font-size:.93rem}}
.card li{{padding-left:20px;position:relative;margin:.35em 0}}
.card li::before{{content:'◆';position:absolute;left:0;color:var(--gold);font-size:.7em;top:.35em}}
.card .btns{{margin-top:auto;display:flex;gap:10px;flex-wrap:wrap}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:28px}}
.step .num{{font-family:'Cormorant Garamond',serif;font-size:2.4rem;color:var(--gold);line-height:1}}
.step h3{{font-size:1.1rem;margin:.3em 0 .2em}} .step p{{font-size:.92rem;color:#4a3c2a;margin:0}}
.about-grid{{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}}
.tool-box{{background:var(--ink);color:var(--paper);border-radius:6px;padding:40px;text-align:center}}
.tool-box h2{{color:var(--paper)}} .tool-box p{{color:#e8dcc2;max-width:52ch;margin:.4em auto 1.4em}}
.tool-box .btn-ghost{{color:var(--paper);box-shadow:inset 0 0 0 1.5px var(--gold2)}}
.tool-box .btn-ghost:hover{{background:#3c2f20}}
details{{border-bottom:1px solid var(--line);padding:16px 0}}
summary{{cursor:pointer;font-weight:600;font-size:1.05rem;list-style:none;
display:flex;justify-content:space-between;align-items:center}}
summary::-webkit-details-marker{{display:none}}
summary::after{{content:'+';color:var(--gold);font-size:1.4rem}}
details[open] summary::after{{content:'–'}} details p{{margin:.7em 0 0;color:#4a3c2a}}
.quote{{background:var(--paper2);border-left:3px solid var(--gold);padding:20px 24px;border-radius:0 4px 4px 0}}
.quote cite{{display:block;margin-top:8px;color:var(--muted);font-style:normal;font-size:.88rem}}
.book{{text-align:center;background:var(--paper2);border:1px solid var(--line);
border-radius:6px;padding:48px 24px}}
.contact{{display:flex;gap:28px;justify-content:center;flex-wrap:wrap;margin-top:18px;font-size:.95rem}}
footer{{margin-top:64px;border-top:1px solid var(--line);background:var(--paper2)}}
.foot-in{{padding:36px 0;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}}
.foot-links a{{color:var(--ink);font-size:.9rem;margin-right:18px}}
.disclaimer{{font-size:.8rem;color:var(--muted);max-width:60ch;margin-top:14px}}
.cookie{{position:fixed;bottom:0;left:0;right:0;background:var(--ink);color:var(--paper);
padding:14px 24px;display:flex;gap:16px;align-items:center;justify-content:center;
flex-wrap:wrap;z-index:100;font-size:.88rem}}
.cookie a{{color:var(--gold2)}} .cookie button{{background:var(--gold);color:var(--ink);
border:0;padding:8px 18px;border-radius:2px;font-weight:600;cursor:pointer}}
.legal{{max-width:760px;margin:0 auto;padding:48px 24px}} .legal h1{{font-size:2.4rem}}
.legal h2{{font-size:1.5rem;margin-top:1.4em}} .legal p,.legal li{{font-size:.96rem;color:#3c2f20}}
.note{{background:#fff8e8;border:1px dashed var(--gold);padding:14px 18px;border-radius:4px;
font-size:.85rem;color:#6b5a35}}
@media(max-width:820px){{.nav-links{{display:none}}.menu-btn{{display:block}}
.nav-links.open{{display:flex;position:absolute;top:64px;left:0;right:0;flex-direction:column;
background:var(--paper);padding:18px 24px;gap:16px;border-bottom:1px solid var(--line)}}
.hero-grid,.about-grid{{grid-template-columns:1fr}}.cards{{grid-template-columns:1fr}}
.steps{{grid-template-columns:1fr 1fr}}.chakra{{max-width:300px;order:-1}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
"""


def chakra_svg():
    signs = ["Mī", "Me", "Vṛ", "Mi", "Ka", "Si", "Ka", "Tu", "Vṛ", "Dh", "Ma", "Ku"]
    cells = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3),
             (2, 3), (1, 3), (0, 3), (0, 2), (0, 1)]
    sq = 92
    p = [f'<svg class="chakra" viewBox="0 0 {sq*4} {sq*4}" xmlns="http://www.w3.org/2000/svg">']
    p.append(f'<rect x="2" y="2" width="{sq*4-4}" height="{sq*4-4}" fill="none" '
             f'stroke="{PAL["gold"]}" stroke-width="2"/>')
    for i in range(1, 4):
        p.append(f'<line x1="{sq*i}" y1="0" x2="{sq*i}" y2="{sq*4}" stroke="{PAL["line"]}"/>')
        p.append(f'<line x1="0" y1="{sq*i}" x2="{sq*4}" y2="{sq*i}" stroke="{PAL["line"]}"/>')
    p.append(f'<rect x="{sq}" y="{sq}" width="{sq*2}" height="{sq*2}" fill="{PAL["paper2"]}" '
             f'stroke="{PAL["gold"]}" stroke-width="1.5"/>')
    p.append(f'<text x="{sq*2}" y="{sq*2-6}" text-anchor="middle" '
             f'font-family="Cormorant Garamond,serif" font-size="26" fill="{PAL["accent"]}">Rāśi</text>')
    p.append(f'<text x="{sq*2}" y="{sq*2+22}" text-anchor="middle" '
             f'font-family="Cormorant Garamond,serif" font-size="18" fill="{PAL["muted"]}">Chakra</text>')
    for (cx, cy), name in zip(cells, signs):
        p.append(f'<text x="{cx*sq+sq/2}" y="{cy*sq+sq/2+6}" text-anchor="middle" '
                 f'font-family="Inter,sans-serif" font-size="20" fill="{PAL["ink"]}">{name}</text>')
    p.append(f'<text x="{sq/2}" y="22" text-anchor="middle" font-size="16" fill="{PAL["gold"]}">◆</text>')
    p.append('</svg>')
    return "".join(p)


def chrome(lang, title, desc, body, alt_href, hreflang, is_legal=False):
    L = I18N[lang]
    other = [x for x in BASE["languages"] if x != lang][0]
    nav = L["nav"]
    altlinks = "".join(
        f'<link rel="alternate" hreflang="{lg}" href="{escape(u)}">' for lg, u in hreflang)
    jsonld = ('{"@context":"https://schema.org","@type":"ProfessionalService","name":"'
              + BASE["brand"] + '","areaServed":"' + BASE["city"] + '","email":"'
              + BASE["email"] + '","url":"' + BASE["domain"] + '","priceRange":"CHF 120–200"}')
    head = f"""<!doctype html><html lang="{L['code']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}"><meta property="og:type" content="website">
{altlinks}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style><script type="application/ld+json">{jsonld}</script></head><body>"""
    nav_links = "" if is_legal else (
        f'<a href="#angebot">{escape(nav["angebot"])}</a>'
        f'<a href="#ablauf">{escape(nav["ablauf"])}</a>'
        f'<a href="#ueber">{escape(nav["ueber"])}</a>'
        f'<a href="#tool">{escape(nav["tool"])}</a>'
        f'<a href="#faq">{escape(nav["faq"])}</a>'
        f'<a class="btn btn-primary" href="#buchen">{escape(nav["book"])}</a>')
    lang_sw = (f'<span class="lang"><a class="{"on" if lang=="de" else ""}" '
               f'href="{escape("index.html" if lang=="de" else alt_href)}">DE</a> · '
               f'<a class="{"on" if lang=="en" else ""}" '
               f'href="{escape("index.html" if lang=="en" else alt_href)}">EN</a></span>')
    header = f"""<header class="nav"><div class="wrap nav-in">
<a class="brand" href="index.html"><span class="dot">◆</span>{escape(BASE['brand'])}</a>
<nav class="nav-links" id="nav">{nav_links}{lang_sw}</nav>
<button class="menu-btn" onclick="document.getElementById('nav').classList.toggle('open')">☰</button>
</div></header>"""
    lt = L["legal_titles"]
    footer = f"""<footer><div class="wrap foot-in">
<div><div class="brand"><span class="dot">◆</span>{escape(BASE['brand'])}</div>
<p class="disclaimer">{escape(L['ui']['disclaimer'])}</p></div>
<div class="foot-links"><a href="impressum.html">{escape(lt['impressum'])}</a>
<a href="datenschutz.html">{escape(lt['datenschutz'])}</a>
<a href="agb.html">{escape(lt['agb'])}</a><br><br>
<span class="disclaimer">© {escape(BASE['consultant'])}, {escape(BASE['city'])}</span></div>
</div></footer>
<div class="cookie" id="cookie">{escape(L['ui']['cookie'])}
<a href="datenschutz.html">{escape(L['ui']['cookie_more'])}</a>
<button onclick="ck()">{escape(L['ui']['cookie_ok'])}</button></div>
<script>function ck(){{try{{localStorage.setItem('cc','1')}}catch(e){{}}
document.getElementById('cookie').style.display='none';}}
try{{if(localStorage.getItem('cc'))document.getElementById('cookie').style.display='none';}}catch(e){{}}</script>
</body></html>"""
    return head + header + body + footer


def index_body(lang):
    L = I18N[lang]
    ui, nav = L["ui"], L["nav"]
    cards = ""
    for pk in BASE["packages"]:
        t = L["packages"][pk["id"]]
        lis = "".join(f"<li>{escape(x)}</li>" for x in t["incl"])
        pay = pk.get("stripe") or BASE["calendly"]
        cards += f"""<div class="card"><div class="dur">{escape(t['dur'])}</div>
<h3>{escape(t['title'])}</h3><div class="price">{escape(pk['price'])}</div>
<p>{escape(t['desc'])}</p><ul>{lis}</ul><div class="btns">
<a class="btn btn-primary" href="{escape(pay)}" target="_blank" rel="noopener">{escape(ui['btn_pay'])}</a>
</div></div>"""
    steps = "".join(
        f'<div class="step"><div class="num">{i:02d}</div><h3>{escape(t)}</h3>'
        f'<p>{escape(d)}</p></div>' for i, (t, d) in enumerate(L["steps"], 1))
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>"
                  for q, a in L["faq"])
    testi = ""
    if BASE["show_testimonials"]:
        items = "".join(f'<div class="quote">{escape(q)}<cite>{escape(w)}</cite></div>'
                        for q, w in L["testimonials"])
        testi = (f'<div class="wrap"><div class="diamond-rule">◆</div></div>'
                 f'<section><div class="wrap"><div class="eyebrow">{escape(ui["voices"])}</div>'
                 f'<div class="cards">{items}</div></div></section>')
    return f"""<main>
<section class="hero"><div class="wrap hero-grid">
<div><div class="eyebrow">{escape(ui['eyebrow_hero'])}</div>
<h1>{escape(L['tagline'])}</h1><p class="lead">{escape(L['intro'])}</p>
<div class="cta-row"><a class="btn btn-primary" href="#buchen">{escape(nav['book'])}</a>
<a class="btn btn-ghost" href="{escape(BASE['tool_url'])}" target="_blank" rel="noopener">{escape(ui['btn_tool'])}</a>
</div></div>{chakra_svg()}</div></section>
<div class="wrap"><div class="diamond-rule">◆</div></div>
<section id="angebot"><div class="wrap"><div class="eyebrow">{escape(nav['angebot'])}</div>
<h2>{escape(ui['h_angebot'])}</h2><p style="max-width:54ch;color:#4a3c2a">{escape(ui['sub_angebot'])}</p>
<div class="cards">{cards}</div></div></section>
<div class="wrap"><div class="diamond-rule">◆</div></div>
<section id="ablauf"><div class="wrap"><div class="eyebrow">{escape(nav['ablauf'])}</div>
<h2>{escape(ui['h_ablauf'])}</h2><div class="steps">{steps}</div></div></section>
<div class="wrap"><div class="diamond-rule">◆</div></div>
<section id="ueber"><div class="wrap about-grid">
<div><div class="eyebrow">{escape(nav['ueber'])}</div><h2>{escape(ui['h_ueber'])}</h2>
<p style="color:#4a3c2a">{escape(L['about'])}</p></div>
<div class="quote">{escape(L['intro'])}<cite>— {escape(BASE['consultant'])}</cite></div>
</div></section>
<div class="wrap"><div class="diamond-rule">◆</div></div>
<section id="tool"><div class="wrap"><div class="tool-box">
<div class="eyebrow" style="color:var(--gold2)">{escape(ui['free'])}</div>
<h2>{escape(ui['h_tool'])}</h2><p>{escape(ui['tool_p'])}</p>
<a class="btn btn-ghost" href="{escape(BASE['tool_url'])}" target="_blank" rel="noopener">{escape(ui['btn_tool2'])}</a>
</div></div></section>{testi}
<div class="wrap"><div class="diamond-rule">◆</div></div>
<section id="faq"><div class="wrap" style="max-width:760px"><div class="eyebrow">{escape(nav['faq'])}</div>
<h2>{escape(ui['h_faq'])}</h2><div style="margin-top:20px">{faq}</div></div></section>
<div class="wrap"><div class="diamond-rule">◆</div></div>
<section id="buchen"><div class="wrap"><div class="book">
<div class="eyebrow">{escape(nav['book'])}</div><h2>{escape(ui['h_book'])}</h2>
<p style="color:#4a3c2a;max-width:52ch;margin:.4em auto 1.4em">{escape(ui['book_p'])}</p>
<a class="btn btn-primary" href="{escape(BASE['calendly'])}" target="_blank" rel="noopener">{escape(ui['btn_book'])}</a>
<div class="contact"><span>✉ <a href="mailto:{escape(BASE['email'])}">{escape(BASE['email'])}</a></span>
<span>☎ {escape(BASE['phone'])}</span><span>📍 {escape(BASE['city'])}</span></div>
</div></div></section></main>"""


def legal_body(lang, key):
    b = BASE
    if key == "impressum":
        if lang == "de":
            return ('<div class="note">Vorlage – vor Veröffentlichung anpassen und juristisch '
                    'prüfen lassen.</div><h2>Verantwortlich</h2><p>{n}<br>[Strasse Nr.]<br>'
                    '[PLZ] {c}<br>Schweiz</p><h2>Kontakt</h2><p>E-Mail: {e}<br>Telefon: {p}</p>'
                    '<h2>Unternehmen</h2><p>[Einzelfirma / GmbH] · [UID/MWST falls vorhanden]</p>'
                    ).format(n=escape(b["consultant"]), c=escape(b["city"]),
                             e=escape(b["email"]), p=escape(b["phone"]))
        return ('<div class="note">Template – review before publishing.</div>'
                '<h2>Responsible</h2><p>{n}<br>[Street No.]<br>[ZIP] {c}<br>Switzerland</p>'
                '<h2>Contact</h2><p>Email: {e}<br>Phone: {p}</p>'
                '<h2>Business</h2><p>[Sole proprietorship / Ltd] · [VAT no. if any]</p>'
                ).format(n=escape(b["consultant"]), c=escape(b["city"]),
                         e=escape(b["email"]), p=escape(b["phone"]))
    if key == "datenschutz":
        if lang == "de":
            return ('<div class="note">Vorlage nach revDSG/DSGVO – an deine Dienste anpassen '
                    'und prüfen lassen.</div><h2>Verantwortliche Stelle</h2><p>{n}, {c} · {e}</p>'
                    '<h2>Welche Daten</h2><p>Bei Buchung/Kontakt: Name, E-Mail, Telefon sowie '
                    'die für die Beratung nötigen Geburtsdaten. Vertraulich, nur zur Beratung.</p>'
                    '<h2>Externe Dienste</h2><ul><li><b>Hosting:</b> [GitHub Pages/Netlify].</li>'
                    '<li><b>Buchung:</b> Calendly (Name/E-Mail, Cookies).</li>'
                    '<li><b>Zahlung:</b> Stripe (Zahlungsdaten).</li></ul>'
                    '<h2>Cookies</h2><p>Eigene Cookies werden nicht gesetzt; eingebundene '
                    'Dienste können Cookies setzen.</p><h2>Deine Rechte</h2><p>Auskunft, '
                    'Berichtigung, Löschung – per E-Mail an {e}.</p>'
                    ).format(n=escape(b["consultant"]), c=escape(b["city"]), e=escape(b["email"]))
        return ('<div class="note">Template (Swiss revDSG / EU GDPR) – adapt &amp; review.</div>'
                '<h2>Controller</h2><p>{n}, {c} · {e}</p><h2>What data</h2><p>On booking/contact: '
                'name, email, phone and the birth details needed for the reading. Confidential, '
                'used only to deliver the session.</p><h2>Third parties</h2><ul>'
                '<li><b>Hosting:</b> [GitHub Pages/Netlify].</li>'
                '<li><b>Booking:</b> Calendly (name/email, cookies).</li>'
                '<li><b>Payment:</b> Stripe (payment data).</li></ul>'
                '<h2>Cookies</h2><p>No own cookies; embedded services may set cookies.</p>'
                '<h2>Your rights</h2><p>Access, correction, deletion — email {e}.</p>'
                ).format(n=escape(b["consultant"]), c=escape(b["city"]), e=escape(b["email"]))
    # agb
    if lang == "de":
        return ('<div class="note">Vorlage – juristisch prüfen lassen.</div>'
                '<h2>1. Leistungen</h2><p>Astrologische Beratung zur persönlichen Orientierung. '
                'Keine garantierten Ergebnisse; kein Ersatz für medizinische/rechtliche/'
                'finanzielle Beratung.</p><h2>2. Termine &amp; Absagen</h2><p>Kostenlose '
                'Verschiebung bis 24 h vorher; danach kann das Honorar verrechnet werden.</p>'
                '<h2>3. Preise &amp; Zahlung</h2><p>Preise in CHF (inkl. allf. MWST), Zahlung '
                'über Stripe.</p><h2>4. Vertraulichkeit</h2><p>Alle Daten werden vertraulich '
                'behandelt.</p><h2>5. Haftung</h2><p>Entscheidungen liegen bei der Klientin/dem '
                'Klienten; Haftung ausgeschlossen, soweit zulässig.</p><h2>6. Recht</h2>'
                '<p>Schweizer Recht; Gerichtsstand {c}.</p>').format(c=escape(b["city"]))
    return ('<div class="note">Template – have it reviewed.</div>'
            '<h2>1. Services</h2><p>Astrological consulting for personal orientation. No '
            'guaranteed outcomes; not a substitute for medical/legal/financial advice.</p>'
            '<h2>2. Bookings &amp; cancellations</h2><p>Free rescheduling up to 24 h before; '
            'later cancellations may be charged.</p><h2>3. Prices &amp; payment</h2><p>Prices in '
            'CHF (incl. VAT where applicable), paid via Stripe.</p><h2>4. Confidentiality</h2>'
            '<p>All data is kept confidential.</p><h2>5. Liability</h2><p>Decisions rest with the '
            'client; liability excluded where permitted.</p><h2>6. Law</h2><p>Swiss law; venue '
            '{c}.</p>').format(c=escape(b["city"]))


def main():
    try:
        here = Path(__file__).parent
    except NameError:        # running inside a notebook / REPL where __file__ is undefined
        here = Path.cwd()
    root = here / "website"
    default = BASE["languages"][0]
    dom = BASE["domain"]

    def url_for(lang, page):
        sub = "" if lang == default else f"{lang}/"
        return f"{dom}/{sub}{page}"

    for lang in BASE["languages"]:
        outdir = root if lang == default else root / lang
        outdir.mkdir(parents=True, exist_ok=True)
        L = I18N[lang]
        # cross-language link (other lang, same page)
        for page, builder, title, desc in [
            ("index.html", lambda lg: index_body(lg),
             f"{BASE['brand']} — {L['tagline']}", L["intro"]),
            ("impressum.html", lambda lg: f'<main class="legal"><h1>{escape(L["legal_titles"]["impressum"])}</h1>{legal_body(lg,"impressum")}</main>',
             L["legal_titles"]["impressum"], L["legal_titles"]["impressum"]),
            ("datenschutz.html", lambda lg: f'<main class="legal"><h1>{escape(L["legal_titles"]["datenschutz"])}</h1>{legal_body(lg,"datenschutz")}</main>',
             L["legal_titles"]["datenschutz"], L["legal_titles"]["datenschutz"]),
            ("agb.html", lambda lg: f'<main class="legal"><h1>{escape(L["legal_titles"]["agb"])}</h1>{legal_body(lg,"agb")}</main>',
             L["legal_titles"]["agb"], L["legal_titles"]["agb"]),
        ]:
            other = [x for x in BASE["languages"] if x != lang][0]
            # relative path to the same page in the other language
            if lang == default:
                alt = f"{other}/{page}"
            else:
                alt = f"../{page}" if other == default else f"../{other}/{page}"
            hreflang = [(lg, url_for(lg, page)) for lg in BASE["languages"]]
            is_legal = page != "index.html"
            html = chrome(lang, title, desc, builder(lang), alt, hreflang, is_legal)
            (outdir / page).write_text(html, encoding="utf-8")

    print("Generated in:", root.resolve())
    for f in sorted(root.rglob("*.html")):
        print("  ·", f.relative_to(root))


if __name__ == "__main__":
    main()
