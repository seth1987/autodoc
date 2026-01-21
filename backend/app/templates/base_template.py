"""Base HTML template with CSS from reference design."""

# CSS extracted from audit-deux-decembre-complet.html
BASE_CSS = """
:root {
    --ink: #2c2c2c;
    --ink-light: #555;
    --ink-faded: #888;
    --paper: #fdfcfa;
    --paper-warm: #f8f5f0;
    --accent: #b8860b;
    --accent-soft: #d4a853;
    --sage: #7d8c6e;
    --sage-light: #e8ebe4;
    --terracotta: #c67d5e;
    --terracotta-light: #f5ebe6;
    --navy: #3d4f5f;
    --navy-light: #e8eef2;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Source Sans Pro', Georgia, serif;
    font-size: 15px;
    line-height: 1.7;
    color: var(--ink);
    background: var(--paper);
}

.cover {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px;
    background: var(--paper-warm);
    position: relative;
    page-break-after: always;
}

.cover::before {
    content: '';
    position: absolute;
    top: 40px;
    left: 40px;
    right: 40px;
    bottom: 40px;
    border: 1px solid var(--accent-soft);
    pointer-events: none;
}

.cover-phase {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 11px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 60px;
}

.cover h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 400;
    color: var(--ink);
    line-height: 1.1;
    margin-bottom: 20px;
}

.cover-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    font-weight: 400;
    font-style: italic;
    color: var(--ink-light);
    margin-bottom: 80px;
}

.cover-brand {
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    font-weight: 500;
    color: var(--ink);
    margin-bottom: 8px;
}

.cover-tagline {
    font-size: 14px;
    color: var(--ink-faded);
    letter-spacing: 1px;
}

.cover-date {
    position: absolute;
    bottom: 60px;
    right: 80px;
    font-size: 13px;
    color: var(--ink-faded);
}

.content {
    max-width: 820px;
    margin: 0 auto;
    padding: 50px 45px;
}

.toc {
    padding: 50px 0;
    margin-bottom: 30px;
    page-break-after: always;
}

.toc h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 26px;
    font-weight: 400;
    color: var(--ink);
    margin-bottom: 35px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--ink);
}

.toc ol {
    list-style: none;
    counter-reset: toc;
}

.toc li {
    counter-increment: toc;
    padding: 12px 0;
    border-bottom: 1px solid #e5e2dd;
    display: flex;
    align-items: baseline;
}

.toc li::before {
    content: counter(toc) ".";
    font-family: 'Cormorant Garamond', serif;
    font-size: 17px;
    color: var(--accent);
    width: 28px;
    flex-shrink: 0;
}

.toc li span {
    font-size: 14px;
    color: var(--ink-light);
}

.section {
    margin-bottom: 55px;
    page-break-inside: avoid;
}

.section-header {
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--ink);
}

.section-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 13px;
    color: var(--accent);
    letter-spacing: 2px;
    margin-bottom: 6px;
}

.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    font-weight: 500;
    color: var(--ink);
    line-height: 1.2;
}

.subsection {
    margin-bottom: 40px;
}

.subsection-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
    font-weight: 500;
    color: var(--ink);
    margin-bottom: 18px;
}

h4 {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: var(--ink);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 30px 0 15px;
}

p {
    margin-bottom: 14px;
    color: var(--ink-light);
}

strong {
    color: var(--ink);
    font-weight: 600;
}

em {
    font-style: italic;
    color: var(--ink-faded);
}

ul, ol {
    margin: 16px 0;
    padding-left: 0;
    list-style: none;
}

ul li, ol li {
    padding: 8px 0 8px 24px;
    position: relative;
    color: var(--ink-light);
}

ul li::before {
    content: '—';
    position: absolute;
    left: 0;
    color: var(--accent);
}

.note {
    margin: 25px 0;
    padding: 22px 26px;
    background: var(--paper-warm);
    border-left: 3px solid var(--accent);
}

.note-title {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
    margin-bottom: 10px;
}

.note p:last-child, .note ul:last-child {
    margin-bottom: 0;
}

.note.success {
    background: var(--sage-light);
    border-left-color: var(--sage);
}

.note.success .note-title {
    color: var(--sage);
}

.note.warning {
    background: #fef9e7;
    border-left-color: var(--accent);
}

.note.alert {
    background: var(--terracotta-light);
    border-left-color: var(--terracotta);
}

.note.alert .note-title {
    color: var(--terracotta);
}

.note.info {
    background: var(--navy-light);
    border-left-color: var(--navy);
}

.note.info .note-title {
    color: var(--navy);
}

.quote {
    font-family: 'Cormorant Garamond', serif;
    font-size: 24px;
    font-style: italic;
    text-align: center;
    color: var(--ink);
    padding: 35px 45px;
    margin: 30px 0;
    position: relative;
}

.quote::before {
    content: '"';
    font-size: 50px;
    position: absolute;
    top: 8px;
    left: 15px;
    color: var(--accent-soft);
    opacity: 0.5;
}

.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin: 25px 0;
}

.col {
    padding: 22px;
    background: var(--paper-warm);
}

.col-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 17px;
    font-weight: 500;
    margin-bottom: 12px;
    color: var(--ink);
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 13px;
}

thead {
    border-bottom: 2px solid var(--ink);
}

th {
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: 600;
    text-align: left;
    padding: 10px 12px;
    color: var(--ink);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

td {
    padding: 12px;
    border-bottom: 1px solid #e5e2dd;
    color: var(--ink-light);
    vertical-align: top;
}

tbody tr:last-child td {
    border-bottom: none;
}

.timeline {
    margin: 30px 0;
    padding-left: 25px;
    border-left: 1px solid var(--accent-soft);
}

.timeline-item {
    padding: 0 0 28px 22px;
    position: relative;
}

.timeline-item:last-child {
    padding-bottom: 0;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -5px;
    top: 4px;
    width: 9px;
    height: 9px;
    background: var(--paper);
    border: 2px solid var(--accent);
    border-radius: 50%;
}

.timeline-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 17px;
    font-weight: 500;
    color: var(--ink);
    margin-bottom: 8px;
}

.timeline-item p {
    font-size: 13px;
    margin-bottom: 6px;
}

.cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 25px 0;
}

.card {
    padding: 22px;
    border: 1px solid #e5e2dd;
}

.card-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 16px;
    font-weight: 500;
    color: var(--ink);
    margin-bottom: 10px;
}

.card p {
    font-size: 13px;
    margin-bottom: 0;
}

.checklist li {
    padding-left: 28px;
}

.checklist li::before {
    content: '✓';
    color: var(--sage);
    font-weight: bold;
}

.checklist li.cross::before {
    content: '✗';
    color: var(--terracotta);
}

.tag {
    display: inline-block;
    font-size: 9px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 3px 8px;
    margin-left: 6px;
}

.tag-urgent {
    background: var(--terracotta-light);
    color: var(--terracotta);
}

.tag-rec {
    background: var(--sage-light);
    color: var(--sage);
}

.tag-ok {
    background: #e8f5e9;
    color: #4a7c4e;
}

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin: 30px 0;
    text-align: center;
}

.stat {
    padding: 18px;
    background: var(--paper-warm);
}

.stat-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 32px;
    font-weight: 500;
    color: var(--ink);
}

.stat-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--ink-faded);
    margin-top: 4px;
}

.conclusion {
    margin-top: 50px;
    padding: 45px;
    background: var(--ink);
    color: var(--paper);
}

.conclusion h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    font-weight: 400;
    margin-bottom: 25px;
    color: var(--paper);
}

.conclusion h3 {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent-soft);
    margin: 25px 0 12px;
}

.conclusion p {
    color: rgba(255,255,255,0.8);
    font-size: 14px;
}

.conclusion ul {
    margin: 12px 0;
}

.conclusion li {
    color: rgba(255,255,255,0.8);
    padding: 6px 0 6px 22px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    font-size: 14px;
}

.conclusion li::before {
    color: var(--accent-soft);
}

.sources {
    margin-top: 50px;
    padding-top: 40px;
    border-top: 1px solid #e5e2dd;
}

.sources h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 24px;
    font-weight: 400;
    margin-bottom: 25px;
}

.sources h3 {
    font-size: 14px;
    font-weight: 600;
    color: var(--ink);
    margin: 30px 0 15px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--accent-soft);
}

.source {
    padding: 12px 0;
    border-bottom: 1px solid #eee;
    font-size: 12px;
}

.source:last-child {
    border-bottom: none;
}

.source strong {
    display: block;
    margin-bottom: 4px;
    color: var(--ink);
}

.source-url {
    color: var(--navy);
    font-size: 11px;
    word-break: break-all;
}

.source-meta {
    color: var(--ink-faded);
    font-size: 11px;
    margin-top: 4px;
}

.footer {
    text-align: center;
    padding: 45px;
    font-size: 12px;
    color: var(--ink-faded);
}

.footer-brand {
    font-family: 'Cormorant Garamond', serif;
    font-size: 18px;
    color: var(--ink);
    margin-bottom: 6px;
}

.divider {
    text-align: center;
    margin: 45px 0;
    color: var(--accent-soft);
    font-size: 18px;
    letter-spacing: 8px;
}

.page-break {
    page-break-after: always;
}

@media print {
    body {
        background: white;
        font-size: 11pt;
    }

    .cover {
        height: 100vh;
    }

    .content {
        padding: 0;
    }

    .section {
        page-break-inside: avoid;
    }

    .note, .col, .card, .stat, .conclusion {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    @page {
        margin: 1.5cm;
        size: A4;
    }
}

@media (max-width: 700px) {
    .cover {
        padding: 40px;
    }

    .cover h1 {
        font-size: 32px;
    }

    .content {
        padding: 25px 20px;
    }

    .two-col, .cards, .stats {
        grid-template-columns: 1fr;
    }
}
"""

# HTML template structure
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Source+Sans+Pro:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
{css}
    </style>
</head>
<body>
{content}
</body>
</html>
"""


def get_html_template(title: str, content: str) -> str:
    """
    Generate complete HTML document.

    Args:
        title: Document title.
        content: HTML body content.

    Returns:
        Complete HTML document string.
    """
    return HTML_TEMPLATE.format(
        title=title,
        css=BASE_CSS,
        content=content
    )
