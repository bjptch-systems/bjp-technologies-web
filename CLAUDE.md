# CLAUDE.md — BJP Technologies (T) Limited
# Master Project Instructions for Claude Code

> Read this file completely before doing anything in this project.
> Every decision, every file, every command must align with what is written here.
> When in doubt — check this file first, then ask.

---

## 1. Project Identity

**Company:** BJP Technologies (T) Limited
**Tagline:** Secure Technology. Scalable Growth.
**Location:** Ubungo – Dar es Salaam, Tanzania
**Primary Domain:** bjptechnologies.co.tz
**Alias Domain:** technologies.bejundas.co.tz (301 redirects to primary — not the Django host)
**Parent Platform:** bejundas.co.tz (multi-vertical business platform)
**Contact:** info@bjptechnologies.co.tz | +255 678 290 994
**Postal:** P.O Box 7276, Msakuzi – Mbezi

**What this project is:**
A professional corporate website and service platform for BJP Technologies — a premium IT solutions company in Tanzania. The primary domain is `bjptechnologies.co.tz`. The subdomain `technologies.bejundas.co.tz` is a 301 redirect alias configured on a separate cPanel — it points to the primary domain and is never listed in Django's `ALLOWED_HOSTS`. The site showcases IT services, enables client enquiries, and is the Technologies vertical of the wider Bejundas ecosystem. Built in Django, deployed on cPanel via Passenger (WSGI), uses MySQL, and version-controlled through GitHub with automated CI/CD via GitHub Actions.

**Bejundas Platform Context:**
This repo is one of 6 independent repos under the Bejundas brand. Each subdomain is its own Django project with its own CLAUDE.md and repo. Do not mix concerns across subdomains.

| Subdomain | Service | Repo |
|---|---|---|
| financial.bejundas.co.tz | Financial Services | bejundas-financial |
| construction.bejundas.co.tz | Construction & Engineering | bejundas-construction |
| energies.bejundas.co.tz | Energies & Gas | bejundas-energies |
| farming.bejundas.co.tz | Farming | bejundas-farming |
| investments.bejundas.co.tz | Investments & Hospitality | bejundas-investments |
| **technologies.bejundas.co.tz** | **BJP Technologies ← THIS REPO** | **bjp-technologies-web** |

---

## 2. Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| Language | Python 3.11 | Minimum version |
| Framework | Django 6.x | Latest stable |
| Database | MySQL / MariaDB | cPanel managed, `utf8mb4` charset |
| ORM | Django ORM | No raw SQL unless absolutely necessary |
| Templates | Django Templates | Jinja2 not used |
| Static files | WhiteNoise + collectstatic | Served via Django in production |
| CSS | Bootstrap 5 + custom CSS | BJP brand variables |
| JS | Vanilla JS | No framework; jQuery only if Bootstrap requires it |
| Server | cPanel + Phusion Passenger (WSGI) | `passenger_wsgi.py` entry point |
| CI/CD | GitHub Actions | Deploy on merge to `main` |
| Env vars | python-dotenv | `.env` file, never committed |
| Testing | pytest + pytest-django | All tests in `tests/` per app |
| Linting | ruff + black | Enforced in CI |

---

## 3. Project Structure

```
bjp-technologies-web/
│
├── CLAUDE.md                    ← You are here
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── passenger_wsgi.py            ← cPanel Passenger entry point
├── .env                         ← NEVER commit. Local + server only
├── .env.example                 ← Commit this. Template for .env
├── .gitignore
├── pytest.ini
├── pyproject.toml               ← ruff + black config
│
├── .github/
│   └── workflows/
│       └── deploy.yml           ← CI/CD pipeline
│
├── config/                      ← Django project settings package
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py              ← Shared settings
│   │   ├── development.py       ← Local dev overrides
│   │   └── production.py        ← Production settings
│   ├── urls.py                  ← Root URL config
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/                    ← Shared: base templates, context processors, utils
│   │   ├── templates/core/
│   │   │   ├── base.html
│   │   │   ├── navbar.html
│   │   │   └── footer.html
│   │   ├── templatetags/
│   │   ├── context_processors.py
│   │   └── utils.py
│   │
│   ├── main/                    ← Homepage, about, services overview
│   │   ├── templates/main/
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   └── services.html
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   │
│   ├── services/                ← Individual service detail pages
│   │   ├── templates/services/
│   │   ├── models.py            ← Service model (editable from admin)
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   │
│   ├── industries/              ← Industry pages
│   │   ├── templates/industries/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   │
│   └── contact/                 ← Contact form, enquiry model
│       ├── templates/contact/
│       ├── models.py            ← ContactEnquiry model
│       ├── forms.py
│       ├── views.py
│       ├── urls.py
│       └── tests/
│
├── static/
│   ├── css/
│   │   ├── style.css            ← Main stylesheet (BJP brand)
│   │   └── variables.css        ← CSS custom properties
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── logo/
│
├── templates/                   ← Global template overrides (e.g. 404, 500)
│   ├── 404.html
│   └── 500.html
│
├── public/
│   ├── static/                  ← collectstatic output (gitignored)
│   └── media/                   ← User uploads (gitignored)
│
├── docs/                        ← Project documentation
│   ├── deployment.md
│   ├── database.md
│   └── branching.md
│
└── tmp/
    └── restart.txt              ← Touch this to restart Passenger
```

---

## 4. Brand & Design System

### Colors
```css
--navy:        #0D1B4B;   /* Primary brand color */
--navy-dark:   #080F2E;   /* Darkest navy */
--navy-mid:    #132260;   /* Mid navy */
--blue:        #1565C0;   /* Action blue */
--blue-light:  #1E88E5;   /* Hover state */
--accent:      #00C6FF;   /* Cyan accent */
--white:       #FFFFFF;
--off-white:   #F4F6FC;
--grey-light:  #E8ECF4;
--grey:        #8A94B0;
--text-body:   #3A4468;
```

### Typography
- Display / headings: `DM Serif Display` (Google Fonts)
- Body: `Outfit` (Google Fonts)
- Monospace / labels: `Space Mono` (Google Fonts)

### Logo
The BJP logo is a geometric network of three connected circles (triangle formation) in navy blue and cyan. Always use the SVG version — never rasterize it.

### Design Principles
- Clean, professional, enterprise feel
- Navy dark hero sections with cyan accents
- Light off-white content sections
- Cards with subtle border and hover lift effect
- Animated counters, scroll-reveal, floating particles in hero

---

## 5. Django Conventions

### Models
- Every model **must** have `created_at` and `updated_at` fields using `auto_now_add` and `auto_now`
- Use `UUIDField` as primary key for all models exposed in URLs
- Always define `__str__`, `Meta.verbose_name`, and `Meta.verbose_name_plural`
- Never use `null=True` on string fields — use `blank=True, default=''` instead
- Use `choices` for any field with a fixed set of values

```python
import uuid
from django.db import models

class BaseModel(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

All models must inherit from `BaseModel` (defined in `apps/core/models.py`).

### Views
- Prefer **Class-Based Views** for standard CRUD and list/detail pages
- Use **Function-Based Views** only for simple one-off views (e.g. home page with no model)
- Every view must have a corresponding URL name
- Use `get_object_or_404` — never raw `Model.objects.get()`

### URLs
- URL names follow pattern: `appname:action` e.g. `main:home`, `services:detail`, `contact:submit`
- Always use `{% url 'appname:action' %}` in templates — never hardcode paths

### Templates
- All templates extend `{% extends 'core/base.html' %}`
- Define blocks: `{% block title %}`, `{% block meta_description %}`, `{% block content %}`
- Use `{% load static %}` at the top of every template
- Never put business logic in templates — only display logic

### Forms
- All forms live in `forms.py` inside their app
- Use `ModelForm` where possible
- Always include CSRF token: `{% csrf_token %}`
- Validate in the form's `clean()` method, not in the view

### Admin
- Register every model in `admin.py`
- Use `list_display`, `search_fields`, and `list_filter` on every `ModelAdmin`
- Group related fields with `fieldsets`

### SiteSettings Singleton (Site-wide Content)
All editable website content lives in `apps/core/models.SiteSettings` — a singleton model (always pk=1). Access it via `SiteSettings.get()`. It is passed to every template as `{{ company }}` by the `company_info` context processor in `apps/core/context_processors.py`.

**Sections covered:**
- Company identity (name, tagline, email, phone, address, postal, domain)
- Social media URLs
- Home page: hero headline/subtext/CTAs, stats counters (4), about strip
- About page: banner headline, counters (4), intro/what-we-do/approach body texts
- Services page: banner headline + subtext
- Industries page: banner headline + subtext
- Contact page: Google Maps embed URL
- Footer: CTA headline, body, button text

**Proxy model admin pattern:** Each section has its own proxy model (e.g. `HeroSectionSettings`, `AboutPageSettings`) registered as a separate `ModelAdmin` with `changelist_view` redirecting to the singleton change form. All 11 sections appear as collapsible sub-links under "Site Settings" in the Unfold sidebar. To add a new editable section: add fields to `SiteSettings`, create a proxy model, register a proxy admin, add a sidebar link in `config/settings/base.py`, wire `{{ company.field }}` in the template, and run `makemigrations`.

---

## 6. Database Rules

- Database name: `bjptechn_bjp_db` (cPanel prefixes with account username)
- Database user: `bjptechn_bjp_user` (cPanel prefixes with account username)
- Host: `localhost`
- Port: `3306`
- Charset: `utf8mb4` always (supports emoji and full Unicode)
- **Never** run `migrate --fake` without documenting why in a comment
- **Never** delete a migration file
- **Never** edit a migration that has already been applied to production
- When renaming a field, create a new field, copy data, then deprecate old field — never rename directly

---

## 7. Git Branching Workflow

This is non-negotiable. Claude Code must follow this workflow on every task.

### Branch Structure
```
main           ← Production only. Protected. No direct commits.
develop        ← Integration branch. Features merge here first.
feature/*      ← New features e.g. feature/contact-form
fix/*          ← Bug fixes e.g. fix/navbar-mobile
hotfix/*       ← Emergency production fixes e.g. hotfix/broken-deploy
chore/*        ← Non-code changes e.g. chore/update-requirements
docs/*         ← Documentation e.g. docs/deployment-guide
```

### Rules
1. **Never commit directly to `main` or `develop`**
2. Every piece of work starts with a new branch from `develop`
3. Branch names are lowercase, hyphen-separated, prefixed with type
4. Commit messages follow Conventional Commits format (see below)
5. Before merging to `develop`, the branch must pass all CI checks
6. Before merging `develop` to `main`, a PR review is required
7. After merging, delete the feature branch

### Commit Message Format (Conventional Commits)
```
type(scope): short description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

Examples:
```
feat(contact): add contact enquiry form with email notification
fix(navbar): correct mobile menu z-index overlap
chore(deps): update Django to 5.1.2
test(services): add unit tests for ServiceDetailView
docs(deploy): add cPanel restart procedure
```

### Claude Code Branch Workflow
When asked to implement any feature, Claude Code must:
1. Confirm which branch to start from (default: `develop`)
2. Create the branch: `git checkout -b feature/description develop`
3. Make all changes on that branch
4. Run tests before finishing: `pytest`
5. Run linting: `ruff check . && black --check .`
6. Stage and commit with proper message
7. Report what was done and what the PR should include
8. **Never merge** — leave merging to the developer

---

## 8. CI/CD Pipeline

### GitHub Actions Workflow (`.github/workflows/deploy.yml`)
```yaml
name: Test and Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: bjp_test_db
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check .
      - run: black --check .
      - run: pytest --tb=short
        env:
          DJANGO_SETTINGS_MODULE: config.settings.ci
          DB_NAME: bjp_test_db
          DB_USER: root
          DB_PASS: root
          DB_HOST: 127.0.0.1
          SECRET_KEY: ci-test-secret-key-not-real

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to cPanel via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host:     ${{ secrets.CPANEL_HOST }}
          username: ${{ secrets.CPANEL_USER }}
          password: ${{ secrets.CPANEL_PASS }}
          script: |
            cd ~/bjp-technologies-web
            git pull origin main
            source ~/virtualenv/bjp-technologies-web/3.11/bin/activate
            pip install -r requirements.txt --quiet
            python manage.py migrate --no-input
            python manage.py collectstatic --no-input
            touch tmp/restart.txt
            echo "Deploy complete: $(date)"
```

### Required GitHub Secrets
- `CPANEL_HOST` — server IP or hostname
- `CPANEL_USER` — SSH username
- `CPANEL_PASS` — SSH password (or use `CPANEL_KEY` for SSH key)

---

## 9. Environment Variables

### `.env.example` (commit this)
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=bjptechnologies.co.tz,www.bjptechnologies.co.tz

# Database
DB_NAME=bjp_db
DB_USER=bjp_user
DB_PASS=your-database-password
DB_HOST=localhost
DB_PORT=3306

# Email (for contact form)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@bjptechnologies.co.tz
EMAIL_HOST_PASSWORD=your-email-app-password
DEFAULT_FROM_EMAIL=BJP Technologies <info@bjptechnologies.co.tz>
CONTACT_EMAIL=info@bjptechnologies.co.tz
```

### Rules
- `.env` is **gitignored** — never commit it
- Load with `python-dotenv` in `passenger_wsgi.py` and `manage.py`
- Access with `os.environ['KEY']` — use `os.environ.get('KEY', default)` only for optional values
- In production, `DEBUG` must be `False` — CI checks for this

---

## 10. Testing Standards

- Every model needs a test for `__str__`, `save()`, and all custom methods
- Every view needs a test for: correct status code, correct template used, authenticated/unauthenticated access
- Every form needs a test for: valid data, invalid data, each required field
- Use `pytest-django` fixtures — not `unittest.TestCase` where avoidable
- Use `factory_boy` for model factories — never create test data inline
- Test database uses SQLite in CI for speed, MySQL locally to match production
- Minimum coverage target: 80%

### Test file naming
```
apps/contact/tests/
├── __init__.py
├── test_models.py
├── test_views.py
└── test_forms.py
```

---

## 11. Security Rules

These are hard rules. Claude Code must never violate them.

- `DEBUG = False` in production — always
- `SECRET_KEY` from environment — never hardcoded
- `ALLOWED_HOSTS` must list only real domains in production:
  ```python
  ALLOWED_HOSTS = ['bjptechnologies.co.tz', 'www.bjptechnologies.co.tz']
  # technologies.bejundas.co.tz is a 301 redirect — not listed here
  ```
- No credentials, API keys, passwords, or tokens in any committed file
- All forms must have `{% csrf_token %}`
- Use `HTTPS` in production — `SECURE_SSL_REDIRECT = True`
- Set `SECURE_HSTS_SECONDS`, `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`
- Input validation on all form fields
- Use Django's built-in password hashing — never implement custom hashing
- File uploads must be validated for type and size

---

## 12. Pages & URL Map

| Page | URL | App | View |
|---|---|---|---|
| Home | `/` | main | `HomeView` |
| About | `/about/` | main | `AboutView` |
| Services | `/services/` | services | `ServicesListView` |
| Service Detail | `/services/<slug>/` | services | `ServiceDetailView` |
| Industries | `/industries/` | industries | `IndustriesView` |
| Industry Detail | `/industries/<slug>/` | industries | `IndustryDetailView` |
| Contact | `/contact/` | contact | `ContactView` |
| Contact Success | `/contact/success/` | contact | `ContactSuccessView` |
| Admin | `/admin/` | django.contrib.admin | — |

---

## 13. Services Data (from Company Profile)

These 7 services must be represented as database records in the `Service` model:

1. **Software Development** — Custom web apps, ERP, HR, Payroll, SACCOS loan management, POS, API integrations (PHP, Laravel)
2. **Website & Digital Solutions** — Corporate websites, e-commerce, CMS, maintenance
3. **Cloud & Infrastructure** — AWS, Oracle Cloud, DigitalOcean, Linux admin, cPanel/WHM, backup & recovery
4. **Cybersecurity** — WAF (ModSecurity), VAPT, malware removal, secure auth, server hardening
5. **Managed IT Services** — 24/7 monitoring, patching, helpdesk, data backup
6. **Payment & System Integrations** — M-Pesa, Tigo Pesa, Airtel Money, Mastercard/Visa, bank gateways
7. **IT Consulting & Advisory** — Infrastructure design, cloud migration, compliance, digital transformation

### Industries Served
1. Startups & SMEs
2. Financial Institutions (SACCOS, Microfinance)
3. NGOs & Development Organizations
4. Education Institutions
5. Healthcare Providers
6. Retail & Wholesale Businesses

---

## 14. Contact Form Requirements

The `ContactEnquiry` model must capture:
- First name, last name
- Email address
- Phone number (optional)
- Company/organisation (optional)
- Service of interest (dropdown from Service model)
- Message
- IP address (auto-captured)
- Status: `new` / `read` / `replied`
- `created_at`, `updated_at`

On submission:
1. Save to database
2. Send email notification to `info@bjptechnologies.co.tz`
3. Send confirmation email to the submitter
4. Redirect to `/contact/success/`

---

## 15. cPanel Deployment Reference

### Passenger Configuration
- Python version: 3.11
- Application root: `~/bjp-technologies-web`
- Startup file: `passenger_wsgi.py`
- Entry point: `application`
- Virtualenv: auto-created by cPanel at `~/virtualenv/bjp-technologies-web/3.11/`

### Manual Deploy Steps (for reference — CI/CD handles this automatically)
```bash
cd ~/bjp-technologies-web
git pull origin main
source ~/virtualenv/bjp-technologies-web/3.11/bin/activate
pip install -r requirements.txt
python manage.py migrate --no-input
python manage.py collectstatic --no-input
touch tmp/restart.txt
```

### Restarting the App
```bash
touch ~/bjp-technologies-web/tmp/restart.txt
```
Passenger detects this file change and gracefully restarts the Django process.

---

## 16. Skills Available to Claude Code

Read the relevant skill file before starting any task of that type:

| Task | Skill File |
|---|---|
| Writing or modifying Django models | `.claude/skills/django-models.md` |
| Writing views and URL patterns | `.claude/skills/django-views.md` |
| Building or editing HTML templates | `.claude/skills/frontend-templates.md` |
| Writing or modifying database migrations | `.claude/skills/mysql-migrations.md` |
| Deploying to cPanel | `.claude/skills/cpanel-deploy.md` |
| Writing tests | `.claude/skills/testing.md` |
| Git branch operations | `.claude/skills/git-branch-workflow.md` |
| Security checks | `.claude/skills/security.md` |

---

## 17. Agents Available to Claude Code

Use these agents for repeated multi-step operations:

| Agent | Trigger phrase | What it does |
|---|---|---|
| `branch-agent` | "start feature X" | Creates branch from develop, sets up file stubs, opens context |
| `migration-agent` | "update model X" | Writes migration safely, checks for conflicts, applies in dev |
| `test-agent` | "write tests for X" | Generates full test suite for a view, model, or form |
| `deploy-agent` | "deploy to production" | Runs full deploy checklist, reports status |
| `review-agent` | "review branch X" | Checks for secrets, missing tests, DEBUG=True, unapplied migrations |
| `page-builder-agent` | "build page X" | Scaffolds view + URL + template + test in one operation |

---

## 18. Definition of Done

A task is **done** only when all of the following are true:

- [ ] Code is on a feature branch (not `main` or `develop`)
- [ ] All new code has corresponding tests
- [ ] `pytest` passes with no failures
- [ ] `ruff check .` passes with no errors
- [ ] `black --check .` passes
- [ ] No hardcoded secrets or credentials
- [ ] Migrations are created and tested locally
- [ ] Template renders correctly in browser
- [ ] `collectstatic` runs without errors
- [ ] Branch is committed with a conventional commit message
- [ ] PR description summarises what changed and why

---

## 19. What Claude Code Must Never Do

- Never commit to `main` directly
- Never commit `.env` or any file containing secrets
- Never use `DEBUG = True` in production settings
- Never delete or edit an existing migration
- Never use `Model.objects.get()` without wrapping in try/except or using `get_object_or_404`
- Never write HTML, CSS, or JS that references the BJP brand colors using hardcoded hex — always use CSS variables
- Never add a Python package without adding it to `requirements.txt`
- Never skip writing tests for new functionality
- Never run `python manage.py migrate` on production manually — let CI/CD handle it
- Never store uploaded files inside the project directory — use `MEDIA_ROOT` which is gitignored

---

## 20. Quick Reference

```bash
# Start development
source venv/bin/activate
python manage.py runserver

# Run tests
pytest
pytest apps/contact/  # specific app
pytest -v --tb=short  # verbose

# Lint and format
ruff check .
black .

# New migration after model change
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# New feature branch
git checkout develop
git pull origin develop
git checkout -b feature/my-feature-name

# Finish feature
git add .
git commit -m "feat(scope): description"
git push origin feature/my-feature-name
# Then open PR on GitHub targeting develop
```

---

## 21. Session Tracker — Rules for Claude Code

Claude Code **must** update `SESSION_LOG.md` at the end of every working session without exception. This is not optional. If a session ends without updating the log, the session is considered incomplete.

### When to Update
- At the natural end of a session (task complete, developer signs off)
- Before switching to a different branch or feature mid-session
- After any deployment action
- After any migration is created or applied

### How to Update

Append a new entry to `SESSION_LOG.md` in the project root using this exact format:

```markdown
---

## Session [NUMBER] — [DATE] [TIME EAT]

**Goal:** One sentence — what this session set out to do.
**Branch:** feature/branch-name
**Status:** ✅ Complete | 🔄 In Progress | ❌ Blocked

### What Was Done
- Bullet point list of every meaningful action taken
- Be specific: "Created ContactEnquiry model with 9 fields" not "worked on models"
- Include file paths for every file created or modified

### Files Changed
| File | Action | Notes |
|---|---|---|
| apps/contact/models.py | Created | ContactEnquiry model |
| apps/contact/admin.py | Modified | Registered ContactEnquiry |

### Migrations
- Migration name: `0001_initial_contact_enquiry`
- Applied: ✅ Yes / ❌ No

### Tests
- Tests written: X
- Tests passing: X / X
- Coverage areas: models, views, forms

### Decisions Made
- Decision: [what was decided]
  Reason: [why — this is the most important part]

### Blockers / Issues
- None / describe any issue encountered

### Next Session Should
- [ ] First priority task
- [ ] Second priority task
- [ ] Any pending item

---
```

### Session Log Location
`SESSION_LOG.md` lives in the project root and is committed to git at the end of every session:

```bash
git add SESSION_LOG.md
git commit -m "docs(session): session [NUMBER] — [brief description]"
git push origin [current-branch]
```

---

## 22. Project Phases

The BJP Technologies website is being built in structured phases. Claude Code must always know which phase is active and only work within that phase's scope unless explicitly told to move to the next.

### Phase Overview

| Phase | Name | Scope | Status |
|---|---|---|---|
| **Phase 1** | Infrastructure & Hosting | Django scaffold → GitHub → cPanel → SSH deploy | ✅ Complete |
| **Phase 2** | Core Foundation | Base templates, brand CSS, navbar, footer, static files | ✅ Complete |
| **Phase 3** | Content Pages | Home, About, Services, Industries pages | ✅ Complete |
| **Phase 4** | Contact System | Contact form, model, email notifications, admin | ✅ Complete |
| **Phase 5** | Admin & CMS | Django admin configuration, content management | ✅ Complete |
| **Phase 6** | Polish & Launch | SEO, performance, security audit, go-live | 🔄 Current |
| **Phase 6.5** | Products Module | New `apps/products/` app, navbar tab, home strip, PMS + BMS product detail pages | 🔄 Current |

---

### Phase 1 — Infrastructure & Hosting
**Goal:** A working, empty Django project that is version-controlled on GitHub, connected to cPanel via SSH, and auto-deploys on push to `main`. No frontend work. No content. Just infrastructure.

**Deliverables:**
- [ ] GitHub repo created: `bjp-technologies-web` (private)
- [ ] Branch protection rules set on `main` and `develop`
- [ ] Django project scaffolded with `config/settings/` (base, dev, production)
- [ ] `passenger_wsgi.py` created and tested
- [ ] `requirements.txt` and `requirements-dev.txt` complete
- [ ] `.env.example` committed, `.env` on server only
- [ ] `.gitignore` complete
- [ ] `pytest.ini` and `pyproject.toml` configured
- [ ] MySQL database created in cPanel (`bjp_db`, `bjp_user`)
- [ ] cPanel Python App configured (Python 3.11, Passenger)
- [ ] SSH key added to GitHub repo deploy keys
- [ ] GitHub Actions `deploy.yml` workflow created
- [ ] First successful auto-deploy confirmed (site returns 200 OK)
- [ ] `SESSION_LOG.md` initialized with Session 1 entry
- [ ] ALLOWED_HOSTS confirmed with both `bjptechnologies.co.tz` and `www.bjptechnologies.co.tz`

**Definition of Done for Phase 1:**
Pushing to `main` on GitHub automatically deploys to `technologies.bejundas.co.tz` and the Django default page (or a basic placeholder) loads in the browser with no errors.

---

### Phase 2 — Core Foundation
**Goal:** The shared visual foundation that all pages inherit from. No content yet — just the shell.

**Deliverables:**
- [ ] `apps/core/` app created and registered
- [ ] `core/base.html` with all blocks defined
- [ ] `core/navbar.html` with BJP brand and responsive mobile menu
- [ ] `core/footer.html` with contact details and links
- [ ] `static/css/style.css` with all BJP brand CSS variables
- [ ] `static/css/variables.css` with design tokens
- [ ] `static/js/main.js` with navbar scroll, mobile menu, scroll-top
- [ ] BJP logo SVG in `static/images/logo/`
- [ ] Google Fonts loaded (Outfit, DM Serif Display, Space Mono)
- [ ] `collectstatic` runs cleanly
- [ ] Context processor for company info registered
- [ ] Placeholder 404 and 500 pages

---

### Phase 3 — Content Pages
**Goal:** All public-facing pages built, connected to models where needed, and rendering correctly.

**Deliverables:**
- [ ] `apps/main/` — Home and About pages
- [ ] `apps/services/` — Services list + Service detail pages + Service model
- [ ] `apps/industries/` — Industries list + Industry detail pages + Industry model
- [ ] All 7 services seeded into database via fixture or management command
- [ ] All 6 industries seeded into database
- [ ] Animated hero section, counters, scroll-reveal working
- [ ] All pages mobile responsive
- [ ] All pages pass HTML validation

---

### Phase 4 — Contact System
**Goal:** Full contact form that saves to database and sends email notifications.

**Deliverables:**
- [ ] `apps/contact/` — ContactEnquiry model, form, view, template
- [ ] Form validates all fields correctly
- [ ] On submit: saves to DB, sends email to `info@bjptechnologies.co.tz`
- [ ] Confirmation email sent to submitter
- [ ] Admin panel shows enquiries with status management
- [ ] Contact success page
- [ ] Rate limiting on form submission (prevent spam)

---

### Phase 5 — Admin & CMS
**Goal:** Client can manage content through Django admin without developer involvement.

**Deliverables:**
- [x] All models registered with rich admin configuration
- [x] Services editable from admin (name, description, icon, order)
- [x] Contact enquiries manageable (mark as read, replied)
- [x] Admin branding customized (BJP logo and colors)
- [x] Superuser credentials documented securely (not in repo)
- [x] SiteSettings singleton — all website content editable from admin (see Section 5)
- [x] Admin panel split into per-section proxy model links (11 sections under Site Settings)

---

### Phase 6 — Polish & Launch
**Goal:** Production-ready. Secure. Fast. SEO-ready.

**Deliverables:**
- [x] All security settings verified (HSTS, CSRF, XSS, SSL redirect)
- [x] `DEBUG=False` confirmed in production
- [x] Meta tags and Open Graph tags on all pages
- [x] Sitemap generated (`django.contrib.sitemaps`)
- [x] robots.txt configured
- [ ] Page load speed tested (target under 3s)
- [ ] All images optimized
- [ ] Final security audit (no secrets, no debug, no SQL exposure)
- [ ] DNS confirmed pointing to cPanel
- [ ] SSL certificate active and auto-renewing
- [ ] Go-live sign-off from developer

---

### Phase 6.5 — Products Module
**Goal:** Surface BJP's productized software (PMS, BMS, etc.) as a first-class section of the website. Scope expansion off Phase 6, triggered by the launch of PMS as a sellable product.

**Deliverables:**
- [x] `apps/products/` app — `Product` model (BaseModel) with identity, descriptions, features (JSON), CTAs, optional contact block, SEO, assets, status (`live`/`coming-soon`)
- [x] Public views `/products/` + `/products/<slug>/` — live-only; coming-soon products 404 on detail
- [x] "Products" nav item added as first entry after About, before Services
- [x] "Our Products" strip on the home page, between hero and Services
- [x] Unfold admin with rich fieldsets, status badge, contact-state indicator, bulk Live/Coming-Soon actions; sidebar entry under Website Content
- [x] Sitemap entry (`ProductSitemap`) + `products:list` in static sitemap
- [x] PMS seeded via data migration with content from team brief; assets in `static/images/products/pms/`
- [ ] BMS seeded via follow-up branch (`feature/products-module-bms`) once assets land
- [ ] PMS contact block populated via admin once BJP provides values

**Definition of Done for Phase 6.5:**
Both PMS and BMS pages live on the main domain, listed on the home page strip, reachable from the Products nav tab. Admin can add a third product without code changes.

---

### Phase Rules for Claude Code
1. **Always know the current phase** — check this section at the start of every session
2. **Do not work ahead** — if Phase 1 is active, do not write frontend templates
3. **Update phase status** when a phase is complete — change ⏳ to ✅
4. **Update SESSION_LOG.md** with which phase deliverables were completed
5. **If a deliverable is blocked**, mark it ❌ and document the blocker in SESSION_LOG.md

---

*Last updated: June 2026*
*Project: BJP Technologies (T) Limited — bjptechnologies.co.tz (primary)*
*Stack: Django 6 + MySQL + cPanel + GitHub Actions*
*Current Phase: Phase 6 — Polish & Launch (Phase 6.5 — Products Module in flight)*
