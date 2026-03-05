# apurvabamezai.com

Academic personal website + data-driven CV system for Apurva Bamezai.

**Single source of truth:** edit `data/cv.yaml`, push to GitHub, and both the website and PDF CV update automatically.

> **REMINDER: Cancel Owlstown Ace Pro subscription before May 9, 2026.**

---

## Folder Structure

```
apurvabamezai.com/
├── data/
│   └── cv.yaml              ← THE file you edit (drives everything)
├── content/                  ← Markdown pages & blog posts
│   ├── _index.md             ← Homepage
│   ├── research/_index.md
│   ├── cv/_index.md
│   ├── teaching/_index.md
│   └── news/                 ← Blog/announcement posts
│       └── 2025-welcome.md
├── layouts/                  ← Hugo templates (don't need to touch)
├── static/
│   ├── css/main.css          ← Site styles
│   ├── js/main.js            ← Nav toggle, abstract expand
│   ├── img/                  ← Profile photo goes here
│   └── files/                ← Generated PDFs land here
├── cv-generator/             ← Python + LaTeX PDF generation
│   ├── generate.py
│   ├── requirements.txt
│   └── templates/
│       ├── full_cv.tex.j2    ← Full academic CV template
│       └── resume.tex.j2    ← Short 1-2 page resume template
├── .github/workflows/
│   └── deploy.yml            ← Auto-build + deploy on push
├── hugo.yaml                 ← Hugo configuration
├── netlify.toml              ← Netlify settings
└── README.md                 ← This file
```

---

## Quick Start

### Prerequisites

Install these once:

```bash
# Hugo (static site generator)
brew install hugo

# Python 3 (for PDF generation)
brew install python3

# LaTeX (for PDF compilation)
brew install --cask mactex-no-gui
# OR for a smaller install:
brew install basictex
sudo tlmgr install enumitem titlesec fancyhdr lastpage

# Python packages
pip3 install -r cv-generator/requirements.txt
```

### Run Locally

```bash
# Preview the website (live-reloads on changes)
hugo server

# Visit http://localhost:1313
```

### Generate PDFs Locally

```bash
python3 cv-generator/generate.py
# Outputs:
#   static/files/Bamezai_CV.pdf
#   static/files/Bamezai_Resume.pdf
```

---

## How to Update Content

### Update CV data (publications, positions, awards, etc.)

1. Open `data/cv.yaml` in any text editor
2. Find the section you want to change
3. Edit the YAML (each section has comments explaining the format)
4. Save, commit, and push:

```bash
git add data/cv.yaml
git commit -m "Update publications"
git push
```

The website and PDFs rebuild automatically.

### Add a new publication

Copy an existing entry in the relevant section of `data/cv.yaml`:

```yaml
publications:
  peer_reviewed:
    - authors: "Your Author, Names Here"
      title: "Your Paper Title"
      journal: Journal Name
      year: 2025
      status: "published"
      url: "https://link-to-paper.com"
      abstract: "Optional abstract text for the website."
      note: ""
```

### Add a news post

Create a new markdown file in `content/news/`:

```bash
# Example: content/news/2026-new-paper.md
```

```markdown
---
title: "New paper accepted at JDE"
date: 2026-01-15
summary: "Our paper on peer learning has been accepted."
---

Full post content goes here. You can use **markdown** formatting.
```

### Update your photo

Replace `static/img/profile-placeholder.jpg` with your actual photo (keep the same filename, or update the reference in `layouts/index.html`).

### Update social links

Edit the `personal` section in `data/cv.yaml`:

```yaml
personal:
  google_scholar: "https://scholar.google.com/citations?user=YOURID"
  orcid: "0000-0000-0000-0000"
  linkedin: "https://linkedin.com/in/yourprofile"
```

---

## Deployment

### How it works

1. You push changes to the `main` branch on GitHub
2. GitHub Actions automatically:
   - Generates new PDFs from `data/cv.yaml`
   - Builds the Hugo site
   - Deploys to Netlify
3. Site is live within ~2 minutes

### GitHub Secrets Required

In your GitHub repo settings (Settings > Secrets and variables > Actions), add:

- `NETLIFY_AUTH_TOKEN` — Get from Netlify: User Settings > Applications > Personal access tokens
- `NETLIFY_SITE_ID` — Get from Netlify: Site configuration > General > Site ID

### Manual Deploy (without GitHub Actions)

```bash
# Build everything locally
python3 cv-generator/generate.py
hugo --minify

# The site is in the public/ folder — upload to any static host
```

---

## Domain & DNS Setup

### Phase 1: DNS Redirect (Do Now)

Keep your domain registered at Squarespace. Just update DNS to point to Netlify.

**In Squarespace DNS settings** (Domains > your domain > DNS Settings):

| Type  | Host | Value               | TTL  |
|-------|------|---------------------|------|
| A     | @    | 75.2.60.5           | 3600 |
| CNAME | www  | [yoursite].netlify.app | 3600 |

Replace `[yoursite]` with your actual Netlify site subdomain (shown in Netlify dashboard).

**In Netlify** (Domain management > Add custom domain):

1. Add `apurvabamezai.com` and `www.apurvabamezai.com`
2. Netlify will automatically provision an SSL certificate (Let's Encrypt)
3. HTTPS should be active within a few minutes

**Verify:** Visit `https://www.apurvabamezai.com` — it should show your new site.

Once confirmed working, cancel your Owlstown subscription (before May 9, 2026).

### Phase 2: Domain Transfer (After Mid-March 2026)

Your domain is in a 60-day post-renewal transfer lock until approximately mid-March 2026. After that, transfer to a cheaper registrar.

**Recommended: Cloudflare Registrar**
- At-cost pricing (~$10/year for .com)
- Free DNS, free CDN, free SSL
- No markup or hidden fees

**Transfer Steps:**

1. **Unlock domain at Squarespace:**
   - Squarespace Domains > your domain > Transfer Away
   - Disable transfer lock
   - Get the authorization/EPP code

2. **Initiate transfer at Cloudflare:**
   - Cloudflare dashboard > Registrar > Transfer
   - Enter your domain name
   - Paste the authorization code
   - Pay for one year renewal (~$10)

3. **Confirm transfer:**
   - You'll receive an email at the domain's admin contact
   - Approve the transfer
   - Transfer takes 1-5 days

4. **Update DNS at Cloudflare:**
   - Same records as above (A record + CNAME)
   - Or use Cloudflare's proxy for extra performance

5. **Verify site stays live throughout:**
   - DNS propagation may cause brief interruptions
   - Keep Squarespace DNS active until transfer completes

**Alternatives to Cloudflare:**
- **Porkbun:** ~$10/year, friendly interface, good support
- **Namecheap:** ~$13/year, well-known, slightly more expensive

**Transfer window:** Anytime between mid-March 2026 and December 2026.

---

## Three CV Outputs

The `data/cv.yaml` supports three output formats:

1. **Full Academic CV** (`Bamezai_CV.pdf`) — All sections, matches your existing LaTeX CV style
2. **Short Resume** (`Bamezai_Resume.pdf`) — 1-2 pages, selected sections, includes detailed professional experience bullets
3. **Website CV page** — Auto-rendered at `/cv/`, always in sync

The `details` field on professional positions is included in the resume but omitted from the short academic CV. The `technical_extended` skills (SPSS, Microsoft Office) are included in the resume but not the academic CV.

---

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Site generator | [Hugo](https://gohugo.io) | Static site from YAML + templates |
| PDF generator | Python + Jinja2 + LaTeX | YAML → LaTeX → PDF |
| Hosting | [Netlify](https://netlify.com) | Free static hosting + HTTPS |
| CI/CD | GitHub Actions | Auto-rebuild on push |
| Domain | Squarespace (→ Cloudflare) | DNS + registration |
| Fonts | Playfair Display + Source Sans 3 | Google Fonts |

---

## Troubleshooting

**Hugo server won't start:**
```bash
hugo version  # Should show v0.120+
brew upgrade hugo
```

**PDF generation fails:**
```bash
# Check LaTeX is installed
pdflatex --version

# If missing packages:
sudo tlmgr install enumitem titlesec fancyhdr lastpage
```

**Site looks broken after deploy:**
- Check GitHub Actions log for errors (Actions tab in your repo)
- Verify `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` secrets are set

---

> **REMINDER: Cancel Owlstown Ace Pro subscription before May 9, 2026.**
