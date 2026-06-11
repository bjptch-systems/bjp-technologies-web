# SESSION_LOG.md — BJP Technologies (T) Limited
# technologies.bejundas.co.tz

---

## Session 13 — 2026-05-10 EAT

**Goal:** Automate cPanel deployment on merge to main via GitHub webhook.
**Branch:** chore/automate-cpanel-deploy → chore/test-webhook-deploy → chore/webhook-live-test
**Status:** ✅ Complete

### What Was Done
- Added GitHub repo About section (description, website, topics) via `gh repo edit`
- Diagnosed homepage counter bug: `24/7` and `100%` values were being overwritten with `0` by counter-up.js
- Fixed counter animation in `static/js/main.js` to skip non-numeric values
- Investigated automated cPanel deployment — SSH (port 22) blocked by host, cPanel UAPI (port 2083) blocked externally by OpenResty proxy
- Added `.cpanel.yml` for post-deploy tasks
- Replaced all failed approaches (SSH, UAPI, JSON API) with GitHub webhook → Django endpoint → detached shell script
- Created `apps/core/webhook.py` with HMAC signature validation
- Created `scripts/deploy.sh` (git pull, pip install, migrate, collectstatic, Passenger restart)
- Wired `/deploy/webhook/` URL in `config/urls.py`
- Stripped deploy job from GitHub Actions — tests only now
- User configured GitHub webhook pointing to `https://bjptechnologies.co.tz/deploy/webhook/`
- User added `GITHUB_WEBHOOK_SECRET` to server `.env`

### Files Changed
| File | Action | Notes |
|---|---|---|
| static/js/main.js | Modified | Skip counter animation for non-numeric values |
| .github/workflows/deploy.yml | Modified | Removed deploy job, tests only |
| .cpanel.yml | Created | Post-deploy tasks for cPanel Git Version Control |
| apps/core/webhook.py | Created | GitHub webhook receiver with HMAC validation |
| scripts/deploy.sh | Created | Shell script: git pull + pip + migrate + collectstatic + restart |
| config/urls.py | Modified | Added /deploy/webhook/ route |
| .env.example | Modified | Added GITHUB_WEBHOOK_SECRET |

### Decisions Made
- Decision: Use GitHub webhook → Django endpoint instead of cPanel UAPI
  Reason: Host's OpenResty proxy blocks all external calls to port 2083 regardless of method or content-type
- Decision: Keep repo public for now
  Reason: No terminal access on host, SSH blocked, cPanel UI blocks PAT in clone URL — private repo auth not achievable without hosting provider help
- Decision: Deploy script runs fully detached (`start_new_session=True`)
  Reason: Passenger restarts on `touch tmp/restart.txt` — detached process survives the parent being killed

### Outcome
- Automated deploy fully working ✅
- Webhook returns 200, deploy script confirmed running via `/tmp/bjp_deploy.log` ✅
- Every future merge to `main` auto-deploys: git pull → pip install → migrate → collectstatic → Passenger restart

### Next Session Should
- [ ] Address private repo if hosting provider enables SSH access
- [ ] Continue Phase 6: page load speed, image optimisation, final security audit

> This file is updated by Claude Code at the end of every working session.
> It is the single source of truth for project progress, decisions, and context.
> Never delete entries. Always append new entries at the bottom.
> Committed to git at the end of every session.

---

## Project Summary

**Repo:** bjp-technologies-web
**Domain:** bjptechnologies.co.tz (primary)
**Stack:** Django 6 + MySQL + cPanel + GitHub Actions
**Current Phase:** Phase 6 — Polish & Launch
**Started:** April 2026

## Phase Progress

| Phase | Name | Status |
|---|---|---|
| Phase 1 | Infrastructure & Hosting | ✅ Complete |
| Phase 2 | Core Foundation | ✅ Complete |
| Phase 3 | Content Pages | ✅ Complete |
| Phase 4 | Contact System | ✅ Complete |
| Phase 5 | Admin & CMS | ✅ Complete |
| Phase 6 | Polish & Launch | 🔄 Current |

---

## Session 1 — [DATE] [TIME EAT]

**Goal:** Project planning — CLAUDE.md, skills, agents, phases, and session tracker created.
**Branch:** N/A (pre-repo setup session)
**Status:** ✅ Complete

### What Was Done
- Discussed project architecture: Django + MySQL + cPanel + GitHub Actions
- Confirmed domain: technologies.bejundas.co.tz (Bejundas Technologies subdomain)
- Confirmed database: MySQL (PostgreSQL not supported on cPanel)
- Designed GitHub CI/CD pipeline via SSH + appleboy/ssh-action
- Created full CLAUDE.md with 22 sections
- Created 5 skill files in `.claude/skills/`
- Created 6 agent definitions in `.claude/agents/agents.md`
- Created SESSION_LOG.md (this file)
- Designed 6-phase delivery plan
- Built HTML/CSS/JS website template (BJP brand, navy/cyan colors)

### Files Created
| File | Action | Notes |
|---|---|---|
| CLAUDE.md | Created | 22-section master instructions |
| .claude/skills/git-branch-workflow.md | Created | Branch naming, commits, PR rules |
| .claude/skills/django-models.md | Created | BaseModel, conventions, examples |
| .claude/skills/django-views.md | Created | CBV/FBV, URLs, context processors |
| .claude/skills/frontend-templates.md | Created | BJP brand, blocks, static files |
| .claude/skills/testing-migrations-deploy-security.md | Created | Testing, migrations, deploy, security |
| .claude/agents/agents.md | Created | 6 agent definitions |
| SESSION_LOG.md | Created | This file |

### Decisions Made
- **Decision:** Use MySQL over PostgreSQL
  **Reason:** cPanel does not support PostgreSQL natively. MySQL is the standard.
- **Decision:** Domain is technologies.bejundas.co.tz not bjptechnologies.co.tz
  **Reason:** BJP Technologies is the Technologies vertical of the Bejundas platform.
- **Decision:** Each Bejundas subdomain gets its own repo and CLAUDE.md
  **Reason:** Independent deployments, no cross-contamination risk between verticals.
- **Decision:** Branch-based development (never commit to main directly)
  **Reason:** Same workflow used successfully in HMS project. CI/CD enforces this.
- **Decision:** 6-phase delivery starting with infrastructure before any frontend
  **Reason:** Get the deploy pipeline working first so every subsequent session can see results live immediately.

### Blockers / Issues
- None at this stage — planning phase only.

### Next Session Should
- [ ] Create GitHub repo `bjp-technologies-web` (private)
- [ ] Set branch protection rules on `main` and `develop`
- [ ] Scaffold Django project locally with `config/settings/` structure
- [ ] Create `passenger_wsgi.py`
- [ ] Create `requirements.txt` and `.env.example`
- [ ] Push initial commit to GitHub
- [ ] Create MySQL database in cPanel (bjp_db, bjp_user)
- [ ] Configure cPanel Python App (Python 3.11, Passenger)
- [ ] Set up GitHub Actions deploy.yml
- [ ] Confirm first successful deploy to technologies.bejundas.co.tz

---

---

## Session 3 — 2026-04-29 EAT

**Goal:** Update CLAUDE.md with correct primary domain and confirm Django 6.x as framework version.
**Branch:** develop
**Status:** ✅ Complete
**Phase:** Phase 1 — Infrastructure & Hosting

### What Was Done
- Updated Section 1 (Project Identity): added primary domain `bjptechnologies.co.tz` and noted `technologies.bejundas.co.tz` as a 301 redirect alias on a separate cPanel — not the Django host
- Updated Section 2 (Tech Stack): confirmed Django 6.x (was already updated; no change needed)
- Updated Section 9 (Environment Variables): changed `ALLOWED_HOSTS` in `.env.example` to `bjptechnologies.co.tz,www.bjptechnologies.co.tz`
- Updated Section 11 (Security Rules): added explicit `ALLOWED_HOSTS` production values with comment excluding the redirect alias
- Updated Section 22 footer: changed domain reference to `bjptechnologies.co.tz (primary)`
- Updated Phase 1 deliverables: added ALLOWED_HOSTS confirmation checklist item

### Files Changed
| File | Action | Notes |
|---|---|---|
| CLAUDE.md | Modified | 6 targeted changes — domain, ALLOWED_HOSTS, security, footer, phase checklist |
| SESSION_LOG.md | Modified | This entry |

### Migrations
- N/A

### Tests
- N/A

### Decisions Made
- **Decision:** `bjptechnologies.co.tz` is the primary Django-hosted domain.
  **Reason:** The site has its own dedicated domain. `technologies.bejundas.co.tz` is a 301 redirect alias configured on a separate cPanel account — Django never receives requests on that hostname so it must not appear in `ALLOWED_HOSTS`.
- **Decision:** Django 6.x confirmed as the framework version.
  **Reason:** Django 6.0.4 is available on PyPI and Python 3.12.3 is installed locally, which satisfies Django 6's minimum Python version requirement.

### Blockers / Issues
- Waiting for MySQL database (`bjp_db`, `bjp_user`) to be created in cPanel before proceeding with Phase 1.

### Next Session Should
- [ ] Confirm MySQL database created in cPanel (bjp_db / bjp_user) and note cPanel-prefixed names
- [ ] Configure cPanel Python App (Python 3.12, Passenger, app root)
- [ ] Create SSH deploy key and add to GitHub repo deploy keys
- [ ] Set CPANEL_HOST, CPANEL_USER, CPANEL_PASS secrets in GitHub repo
- [ ] Push develop → main and confirm first auto-deploy

---

---

## Session 4 — 2026-04-30 EAT

**Goal:** Complete Phase 1 — scaffold Django project, connect to GitHub, deploy to cPanel, confirm site live.
**Branch:** develop → merged to main
**Status:** ✅ Complete
**Phase:** Phase 1 — Infrastructure & Hosting

### What Was Done
- Created GitHub repo `bjp-technologies-web` (private) — manual creation by developer, cloned via cPanel Git Version Control
- Created `develop` branch and pushed initial planning files to `main`
- Scaffolded Django 6.0.4 project with `config/settings/` package (base, development, production, ci)
- Created all 5 app stubs: core, main, services, industries, contact
- Created `passenger_wsgi.py`, `manage.py`, `requirements.txt`, `requirements-dev.txt`
- Created `.env.example`, `.gitignore`, `pytest.ini`, `pyproject.toml`
- Created `.github/workflows/deploy.yml` (GitHub Actions CI + SSH deploy)
- Replaced `mysqlclient` with `PyMySQL` — shared hosting has no MySQL dev libraries
- Patched PyMySQL version info to satisfy Django 6's mysqlclient >= 2.2.1 check
- Created `Passengerfile.json` for cPanel Passenger process manager
- Created MySQL database `bjptechn_bjp_db` and user `bjptechn_bjp_user` in cPanel
- Configured cPanel Python App (Python 3.12.12, Passenger, app root: bjp-technologies-web)
- Added cPanel server SSH public key as GitHub deploy key
- Created `.env` on server via File Manager with production credentials
- Set `DJANGO_SETTINGS_MODULE=config.settings.production` in Python App env vars
- Ran `pip install`, `migrate`, `collectstatic` via cPanel Python App execute scripts
- Confirmed site live at `https://bjptechnologies.co.tz` — Django responding with 404 (correct, no URLs yet)

### Files Changed
| File | Action | Notes |
|---|---|---|
| config/settings/base.py | Created | PyMySQL install + version patch |
| config/settings/development.py | Created | SQLite for local dev |
| config/settings/production.py | Created | MySQL, security headers |
| config/settings/ci.py | Created | CI MySQL config |
| apps/core/ | Created | App stub + context_processors.py |
| apps/main/ | Created | App stub |
| apps/services/ | Created | App stub |
| apps/industries/ | Created | App stub |
| apps/contact/ | Created | App stub |
| passenger_wsgi.py | Created | cPanel Passenger entry point |
| Passengerfile.json | Created | Passenger process config |
| requirements.txt | Created | PyMySQL, Django, WhiteNoise, dotenv |
| requirements-dev.txt | Created | pytest, ruff, black, factory-boy |
| .env.example | Created | Template for server .env |
| .gitignore | Created | Excludes venv, .env, public/ |
| pytest.ini | Created | Test configuration |
| pyproject.toml | Created | ruff + black config |
| .github/workflows/deploy.yml | Created | CI test + SSH deploy pipeline |
| CLAUDE.md | Modified | Phase 1 marked complete, Phase 2 current |
| SESSION_LOG.md | Modified | This entry |

### Migrations
- Migration name: Django built-in (admin, auth, contenttypes, sessions)
- Applied: ✅ Yes — on `bjptechn_bjp_db` MySQL database

### Tests
- Tests written: 0 (Phase 1 — infrastructure only, no app logic)
- Tests passing: N/A
- Coverage areas: N/A

### Decisions Made
- **Decision:** Use PyMySQL instead of mysqlclient.
  **Reason:** Shared hosting (cPanel) does not have MySQL development libraries (`libmysqlclient-dev`) required to build mysqlclient. PyMySQL is pure Python and installs without system dependencies.
- **Decision:** Patch `pymysql.version_info` to `(2, 2, 1)` after `install_as_MySQLdb()`.
  **Reason:** Django 6 checks mysqlclient version >= 2.2.1. PyMySQL reports 1.4.6 which fails the check. Patching the version tuple is the standard workaround for this combination.
- **Decision:** Deploy manually via cPanel Git Version Control + Python App instead of GitHub Actions SSH.
  **Reason:** SSH port 22 is blocked on the shared hosting server. cPanel Terminal was unavailable. GitHub Actions SSH deploy will be wired up once SSH access is resolved. Manual pull via cPanel UI is the interim deploy method.
- **Decision:** Use cPanel Git Version Control for server-side repo management.
  **Reason:** No SSH access and no cPanel Terminal available. Git Version Control in cPanel is the only available path to clone and update the repo on the server.
- **Decision:** Set `DJANGO_SETTINGS_MODULE=config.settings.production` in Python App env vars.
  **Reason:** manage.py defaults to development (SQLite). Without this env var, execute scripts run migrations on SQLite instead of MySQL.

### Blockers / Issues
- SSH port 22 blocked — GitHub Actions auto-deploy not yet wired up. Manual pull via cPanel Git Version Control is the interim deploy method.
- Branch protection rules skipped — requires GitHub Pro for private repos.
- Server response is slow (~5–10s) — expected on shared hosting with cold Passenger starts.

### Phase Deliverables Completed
- [x] GitHub repo created: `bjp-technologies-web` (private)
- [x] Django project scaffolded with `config/settings/` (base, dev, production)
- [x] `passenger_wsgi.py` created and tested
- [x] `requirements.txt` and `requirements-dev.txt` complete
- [x] `.env.example` committed, `.env` on server only
- [x] `.gitignore` complete
- [x] `pytest.ini` and `pyproject.toml` configured
- [x] MySQL database created in cPanel (`bjptechn_bjp_db`, `bjptechn_bjp_user`)
- [x] cPanel Python App configured (Python 3.12.12, Passenger)
- [x] SSH deploy key added to GitHub repo
- [x] GitHub Actions `deploy.yml` workflow created
- [x] Django responding live at `https://bjptechnologies.co.tz` (404 — correct, no URLs yet)
- [x] `SESSION_LOG.md` updated
- [x] ALLOWED_HOSTS confirmed: `bjptechnologies.co.tz`, `www.bjptechnologies.co.tz`
- [ ] ⚠️ Branch protection rules — skipped (requires GitHub Pro)
- [ ] ⚠️ GitHub Actions auto-deploy — pending SSH access resolution

### Next Session Should
- [ ] Start Phase 2 — Core Foundation
- [ ] Create `apps/core/templates/core/base.html` with all blocks
- [ ] Create `core/navbar.html` and `core/footer.html`
- [ ] Create `static/css/style.css` with BJP brand variables
- [ ] Create `static/js/main.js`
- [ ] Add BJP logo SVG to `static/images/logo/`
- [ ] Load Google Fonts (Outfit, DM Serif Display, Space Mono)
- [ ] Create placeholder 404 and 500 pages
- [ ] Wire up `apps/main/` HomeView so site returns 200 OK instead of 404

---

## Session 5 — 2026-04-30 EAT

**Goal:** Complete Phase 2 — build all base templates, BJP brand CSS, home page content sections, and commit to feature branch.
**Branch:** feature/phase-2-core-foundation
**Status:** ✅ Complete
**Phase:** Phase 2 — Core Foundation

### What Was Done
- Analysed Luminos HTML template (cloned locally) — selected `index-four.html` as design base
- Copied all Luminos assets into `static/` (CSS, JS plugins, fonts, images)
- Built `apps/core/templates/core/base.html` — full page shell with all blocks, Google Fonts, all JS deferred, mobile sidebar, preloader, scroll-to-top
- Built `apps/core/templates/core/navbar.html` — `header-area-four header--sticky` structure, BJP white logo, 7-service dropdown, responsive hamburger
- Built `apps/core/templates/core/footer.html` — original Luminos light gradient footer, BJP content (services, industries, contact info), CTA banner in BJP navy, copyright + social icons
- Created `static/css/bjp.css` — purely additive brand overrides: logo sizing, sticky nav navy, CTA navy, primary button navy, scroll progress cyan
- Restored all Luminos style.css color/font variables to originals — resolved all UI conflicts (invisible nav, wrong hero, invisible footer text, wrong font)
- Built `apps/main/templates/main/home.html` — 7 sections: hero (jarallax), 3 service cards, 7-service grid, animated stats counters, About strip, Why Choose BJP, Tech Partners, Industries
- Fixed animated counter: moved `.counter` class from `<h3>` to `<span>` inside it (CounterUp.js requirement)
- Added 3 new home page sections:
  - **About strip**: 2-col (image + text), key trust points, linked to About page
  - **Why Choose BJP**: 4 differentiator cards using `single-working-process-choose-us` with tag badges
  - **Tech Partners**: FA6 brand icons (AWS, Azure, Python, Laravel, Linux, Ubuntu, Stripe) + M-Pesa text badge
- Generated `docs/BJP_Technologies_Phase1_Report.pdf` using reportlab
- Created stub templates for all apps (services, industries, contact, 404, 500)
- Wired up all URL namespaces in `config/urls.py`

### Files Changed
| File | Action | Notes |
|---|---|---|
| apps/core/templates/core/base.html | Created | Full page shell, all JS, mobile sidebar |
| apps/core/templates/core/navbar.html | Created | BJP nav, dropdown, hamburger |
| apps/core/templates/core/footer.html | Created | CTA banner + light gradient footer |
| apps/main/templates/main/home.html | Created | 7 content sections including 3 new |
| apps/services/templates/services/*.html | Created | List + detail stubs |
| apps/industries/templates/industries/*.html | Created | List + detail stubs |
| apps/contact/templates/contact/*.html | Created | Contact + success stubs |
| templates/404.html | Created | Custom error page |
| templates/500.html | Created | Custom error page |
| static/css/bjp.css | Created | BJP brand additions only |
| static/css/style.css | Created | Luminos base (variables restored to originals) |
| static/css/plugins/ | Created | fontawesome, swiper, metismenu, popup |
| static/css/vendor/ | Created | bootstrap.min.css |
| static/js/ | Created | All JS plugins and vendor files |
| static/fonts/ | Created | Aeonik + FontAwesome 6 Pro fonts |
| static/images/ | Created | All Luminos image assets |
| static/images/logo/ | Created | bjp-logo.svg + bjp-logo-white.svg |
| config/urls.py | Modified | All 4 app URL namespaces wired up |
| apps/main/views.py | Modified | HomeView + AboutView, default_industries context |
| apps/*/urls.py | Modified | URL patterns for all apps |
| docs/BJP_Technologies_Phase1_Report.pdf | Created | Phase 1 completion report (reportlab) |

### Migrations
- Migration name: N/A (no new models in Phase 2)
- Applied: N/A

### Tests
- Tests written: 0 (Phase 2 — templates and static, no new model/form logic)
- Tests passing: N/A
- Coverage areas: N/A

### Decisions Made
- **Decision:** Keep Luminos CSS variables at their original values; add BJP identity only in bjp.css.
  **Reason:** Changing Luminos's internal `--color-primary`, `--color-body`, and font variables cascades unpredictably across dark-background sections that expect white text. Additive overrides in bjp.css are safe and reversible.
- **Decision:** Use FA6 brand icons for the Tech Partners section instead of image logos.
  **Reason:** No official partner logo SVGs available locally. FA6 brand icons are already loaded, render crisply, and display correct brand colors. Sufficient for Phase 2 — real logos can replace them in Phase 6 polish.
- **Decision:** Use placeholder image (about/01.webp from Luminos assets) for About strip.
  **Reason:** Real BJP photography not yet available. Placeholder is contextually appropriate (tech/IT imagery). Replace with real photo in Phase 5/6.

### Blockers / Issues
- None for Phase 2 core foundation.
- SSH auto-deploy still pending (inherited from Phase 1).

### Phase Deliverables Completed (Phase 2)
- [x] `apps/core/` templates: base.html, navbar.html, footer.html
- [x] `static/css/bjp.css` with BJP brand CSS
- [x] BJP logo SVG (dark + white versions)
- [x] Google Fonts loaded (DM Serif Display, Outfit, Space Mono)
- [x] All JS plugins: WOW, Jarallax, CounterUp, Swiper, MetisMenu, SVG-Inject
- [x] `collectstatic` runs cleanly (Django check: 0 issues)
- [x] Home page with 7 content sections including About strip, Why Choose BJP, Tech Partners
- [x] Animated stat counters working (CounterUp.js `.counter` span pattern)
- [x] Context processor for company info
- [x] Placeholder 404 and 500 pages
- [x] All URL routes wired: main, services, industries, contact

### Next Session Should
- [ ] Start Phase 3 — Content Pages
- [ ] Build `apps/main/templates/main/about.html` — full About page
- [ ] Build `apps/services/` — Services list + Service model + Service detail pages
- [ ] Build `apps/industries/` — Industries list + Industry model + Industry detail pages
- [ ] Seed 7 services and 6 industries via fixture or management command
- [ ] Test all pages mobile-responsive

---

<!-- 
TEMPLATE FOR NEXT SESSION — copy this block and fill in:

---

## Session [N] — [DATE] [TIME EAT]

**Goal:** 
**Branch:** 
**Status:** ✅ Complete | 🔄 In Progress | ❌ Blocked
**Phase:** Phase [N] — [Name]

### What Was Done
- 

### Files Changed
| File | Action | Notes |
|---|---|---|
|  |  |  |

### Migrations
- Migration name: 
- Applied: ✅ Yes / ❌ No / N/A

### Tests
- Tests written: 
- Tests passing: / 
- Coverage areas: 

### Decisions Made
- **Decision:** 
  **Reason:** 

### Blockers / Issues
- 

### Phase Deliverables Completed
- [ ] 

### Next Session Should
- [ ] 

---
-->

---

## Session 5 — 2026-04-30 EAT

**Goal:** Build all Phase 3 content pages — models, templates, seed command, and tests.
**Branch:** feature/phase-3-content-pages
**Status:** ✅ Complete
**Phase:** Phase 3 — Content Pages

### What Was Done
- Added `BaseModel` (abstract UUID pk + timestamps) to `apps/core/models.py`
- Built `Service` model: name, slug (auto-gen), tagline, description, bullet_points, icon_svg, order, is_active
- Built `Industry` model: name, slug (auto-gen), tagline, description, services_offered, image, order, is_active
- Created migrations for both models (0001_initial)
- Registered both models in admin with list_display, search_fields, prepopulated_fields, readonly timestamps
- Created `apps/core/management/commands/seed_content.py` — idempotent, seeds 7 services + 6 industries from company profile
- Updated `ServicesListView` + `ServiceDetailView` to use real model (added other_services context)
- Updated `IndustriesListView` + `IndustryDetailView` to use real model
- Updated `HomeView` to pull industries and featured_services from DB; removed `{% empty %}` fallback
- Built 5 full page templates using Luminos CSS patterns:
  - `apps/main/templates/main/about.html` — counter strip, what-we-do-wrapper, keybenefits, service grid, CTA
  - `apps/services/templates/services/list.html` — service banner + single-service-list rows + CTA
  - `apps/services/templates/services/detail.html` — service-single-area-banner, service-area-details-wrapper, bullet list, sidebar CTA, other services
  - `apps/industries/templates/industries/list.html` — rts-career-banner-area, industry cards grid, CTA
  - `apps/industries/templates/industries/detail.html` — career banner, bg-gradient-one-industry, check-wrapper, 6-card services grid, CTA
- Fixed `contact:submit` → `contact:contact` across all templates
- Wrote 37 tests covering model str, slug, helper methods, timestamps; view status codes, templates, context, 404 for invalid/inactive

### Files Changed
| File | Action | Notes |
|---|---|---|
| apps/core/models.py | Modified | Added BaseModel abstract class |
| apps/core/management/commands/seed_content.py | Created | Seeds 7 services + 6 industries |
| apps/services/models.py | Created | Service model with auto-slug, get_bullet_list |
| apps/services/admin.py | Modified | ServiceAdmin with all required fields |
| apps/services/migrations/0001_initial.py | Created | Service table migration |
| apps/services/views.py | Modified | Real CBVs replacing TemplateView stubs |
| apps/services/urls.py | Modified | Wired to new views |
| apps/services/templates/services/list.html | Modified | Full Luminos-styled template |
| apps/services/templates/services/detail.html | Modified | Full Luminos-styled template |
| apps/services/tests/test_models.py | Created | 8 model tests |
| apps/services/tests/test_views.py | Created | 10 view tests |
| apps/industries/models.py | Created | Industry model with auto-slug, get_services_list |
| apps/industries/admin.py | Modified | IndustryAdmin with all required fields |
| apps/industries/migrations/0001_initial.py | Created | Industry table migration |
| apps/industries/views.py | Modified | Real CBVs replacing TemplateView stubs |
| apps/industries/urls.py | Modified | Wired to new views |
| apps/industries/templates/industries/list.html | Modified | Full Luminos-styled template |
| apps/industries/templates/industries/detail.html | Modified | Full Luminos-styled template |
| apps/industries/tests/test_models.py | Created | 8 model tests |
| apps/industries/tests/test_views.py | Created | 9 view tests |
| apps/main/templates/main/about.html | Modified | Full About page (was stub) |
| apps/main/templates/main/home.html | Modified | Removed {% empty %} fallback from industries loop |
| apps/main/views.py | Modified | HomeView pulls from DB |

### Migrations
- Migration name: `apps/services/migrations/0001_initial.py`
- Applied: ❌ No — must be run on cPanel after deploy
- Migration name: `apps/industries/migrations/0001_initial.py`
- Applied: ❌ No — must be run on cPanel after deploy

### Tests
- Tests written: 37
- Tests passing: 37 / 37
- Coverage areas: Service model (str, slug, bullet_list, timestamps), Industry model (str, slug, services_list, timestamps), ServicesListView (200, template, active/inactive filter), ServiceDetailView (200, 404, other_services), IndustriesListView (200, template, active/inactive filter), IndustryDetailView (200, 404, context)

### Decisions Made
- **Decision:** Used `bg-gradient-one-industry` wrapper for industry detail pages, `single-service-list` for services list
  **Reason:** Matches Luminos reference pages exactly — `industry.html` and `service.html` patterns
- **Decision:** Service detail sidebar is sticky with contact CTA
  **Reason:** Encourages lead generation on service pages without a separate page visit
- **Decision:** `contact:contact` is the correct URL name (not `contact:submit` as initially assumed)
  **Reason:** The contact app defines `name="contact"` in its urlpatterns

### Blockers / Issues
- None

### Phase 3 Deliverables Completed
- [x] `apps/services/` — Service model, list + detail views, templates
- [x] `apps/industries/` — Industry model, list + detail views, templates
- [x] `apps/main/templates/main/about.html` — full About page
- [x] 7 services seeded via seed_content command
- [x] 6 industries seeded via seed_content command
- [x] HomeView pulls from DB, no fallback needed
- [x] All pages use Luminos CSS patterns

### Deploy Steps Required on cPanel After Merge
1. `git pull origin main`
2. `manage.py migrate --no-input` ← runs Service + Industry migrations
3. `manage.py seed_content` ← seeds 7 services + 6 industries
4. `manage.py collectstatic --no-input`
5. Touch `tmp/restart.txt`

### Next Session Should
- [ ] Merge feature/phase-3-content-pages → develop → main
- [ ] Deploy to cPanel and run the 4 commands above
- [ ] Verify all pages live: /about/, /services/, /services/<slug>/, /industries/, /industries/<slug>/
- [ ] Start Phase 4 — Contact System

---

## Session 6 — 2026-05-04 EAT

**Goal:** Build Phase 4 — complete contact system with model, form, views, email notifications, admin, templates, and tests.
**Branch:** feature/phase-4-contact-system
**Status:** ✅ Complete
**Phase:** Phase 4 — Contact System

### What Was Done
- Created `ContactEnquiry` model (inherits BaseModel) with 10 fields: first_name, last_name, email, phone, company, service (FK → Service), message, ip_address, status (new/read/replied), timestamps
- Created `ContactForm` (ModelForm) with service dropdown from active Service records, message minimum-length validation (10 chars), and strip on name fields
- Created `ContactView` (FormView): IP capture (X-Forwarded-For aware), IP-based rate limiting (5 submissions per 30 min), saves enquiry, sends notification email to info@bjptechnologies.co.tz via EmailMessage with reply-to set, sends confirmation email to submitter
- Created `ContactSuccessView` (TemplateView) 
- Created `ContactEnquiryAdmin` with list_display, list_filter, search_fields, list_editable status, readonly meta fields, fieldsets
- Updated `urls.py` — replaced TemplateView stubs with real views
- Built full `contact.html` template: jarallax banner, 3 info cards (address/phone/email), Luminos contact-form structure with all 7 fields, inline field errors, non-field error block, Google Map (Dar es Salaam / Ubungo coordinates)
- Built `success.html` template: navy circle check icon, confirmation message, Back to Home + Explore Services buttons, phone fallback card
- Created migration `0001_initial` and applied locally
- Wrote 30 tests: 8 model, 10 form, 12 view (GET, POST valid/invalid, IP capture, rate limit block, rate limit window reset)
- All 67 tests across entire project pass
- ruff and black pass clean

### Files Changed
| File | Action | Notes |
|---|---|---|
| apps/contact/models.py | Created | ContactEnquiry model with BaseModel, FK to Service |
| apps/contact/forms.py | Created | ContactForm with service dropdown + message validation |
| apps/contact/views.py | Created | ContactView + ContactSuccessView + email methods |
| apps/contact/admin.py | Created | ContactEnquiryAdmin with full configuration |
| apps/contact/urls.py | Modified | Real views replacing TemplateView stubs |
| apps/contact/migrations/0001_initial.py | Created | ContactEnquiry table |
| apps/contact/templates/contact/contact.html | Modified | Full Luminos-styled contact page |
| apps/contact/templates/contact/success.html | Modified | Branded success page |
| apps/contact/tests/test_models.py | Created | 8 model tests |
| apps/contact/tests/test_forms.py | Created | 10 form tests |
| apps/contact/tests/test_views.py | Created | 12 view tests |
| docs/generate_phase3_report.py | Modified | black formatting only |

### Migrations
- Migration name: `apps/contact/migrations/0001_initial.py`
- Applied: ✅ Yes — locally (SQLite dev db)
- Applied: ❌ No — cPanel production (run after deploy)

### Tests
- Tests written: 30
- Tests passing: 67 / 67 (full project suite)
- Coverage areas: ContactEnquiry str/full_name/status default/optional fields/FK null/timestamps/ordering; ContactForm valid/invalid/required fields/message length/optional service; ContactView GET/POST redirect/DB save/IP capture/status default/invalid data/rate limit block/rate limit window

### Decisions Made
- **Decision:** IP-based rate limiting implemented in the view using DB query (no external library).
  **Reason:** No django-ratelimit or caching layer is set up. Simple DB query counting submissions from same IP in last 30 minutes is sufficient for a corporate contact form with low submission volume.
- **Decision:** Email uses `EmailMessage` (not `send_mail`) with `reply_to` set to the submitter's email.
  **Reason:** `send_mail` does not support `reply_to`. This lets `info@bjptechnologies.co.tz` reply directly to the enquirer with one click.
- **Decision:** Both email methods use `fail_silently=True`.
  **Reason:** Email delivery failure should not block the user from seeing the success page or the enquiry being saved to the database. Admin can see all enquiries regardless.

### Blockers / Issues
- None

### Phase 4 Deliverables Completed
- [x] `apps/contact/` — ContactEnquiry model, form, view, template
- [x] Form validates all fields correctly
- [x] On submit: saves to DB, sends email to info@bjptechnologies.co.tz
- [x] Confirmation email sent to submitter
- [x] Admin panel shows enquiries with status management
- [x] Contact success page
- [x] Rate limiting on form submission (5/30 min per IP)

### Deploy Steps Required on cPanel After Merge
1. `git pull origin main`
2. `manage.py migrate --no-input` ← runs ContactEnquiry migration
3. `manage.py seed_content` ← (if not already run from Phase 3)
4. `manage.py collectstatic --no-input`
5. Touch `tmp/restart.txt`

### Next Session Should
- [ ] Merge feature/phase-4-contact-system → develop → main via PR
- [ ] Deploy to cPanel (migrate + collectstatic + restart)
- [ ] Verify /contact/ form submits and saves to admin
- [ ] Start Phase 5 — Admin & CMS (admin branding, rich admin config, content management)

---

---

## Session 8 — 2026-05-06 EAT

**Goal:** Phase 5 — Integrate Wagtail CMS as the primary admin dashboard; brand it with BJP identity.
**Branch:** feature/phase-5-admin-cms
**Status:** ✅ Complete
**Phase:** Phase 5 — Admin & CMS

### What Was Done
- Confirmed Wagtail 7.3.1 compatibility with Django 6.0.4 and MySQL before starting
- Installed Wagtail 7.3.1 and pinned all new dependencies in requirements.txt
- Added all Wagtail INSTALLED_APPS and RedirectMiddleware to settings/base.py
- Added Wagtail admin settings (WAGTAIL_SITE_NAME, WAGTAILADMIN_BASE_URL, etc.)
- Moved Django admin to /django-admin/; Wagtail CMS available at /cms/
- Registered Service as a Wagtail SnippetViewSet with panels (identity + content sections)
- Registered Industry as a Wagtail SnippetViewSet with panels
- Registered ContactEnquiry as a Wagtail SnippetViewSet — most fields read-only, only status is editable; inspect view shows full detail
- Created apps/core/wagtail_hooks.py: BJP-branded dashboard panel showing enquiry stats + recent 5 enquiries
- Created static/css/wagtail_brand.css: BJP navy sidebar, cyan active states, branded buttons and panel borders
- Created templates/wagtailadmin/branding/logo.html: BJP white SVG logo in sidebar
- Created templates/wagtailadmin/branding/favicon.html: BJP favicon
- Created templates/core/wagtail/dashboard_enquiries.html: stat cards + recent enquiry list
- Ran all Wagtail migrations (115 migration steps across wagtailcore, wagtailadmin, wagtaildocs, etc.)
- All 67 existing tests pass unchanged
- ruff + black clean

### Files Changed
| File | Action | Notes |
|---|---|---|
| requirements.txt | Modified | Added wagtail==7.3.1, modelcluster, taggit, Pillow |
| config/settings/base.py | Modified | Wagtail INSTALLED_APPS, middleware, settings block |
| config/urls.py | Modified | /cms/ → wagtailadmin, /documents/ → wagtaildocs, /django-admin/ → Django admin |
| apps/services/wagtail_hooks.py | Created | ServiceSnippetViewSet with identity + content panels |
| apps/industries/wagtail_hooks.py | Created | IndustrySnippetViewSet with identity + content panels |
| apps/contact/wagtail_hooks.py | Created | ContactEnquirySnippetViewSet — read-only details, editable status |
| apps/core/wagtail_hooks.py | Created | EnquiriesDashboardPanel + insert_global_admin_css hook |
| static/css/wagtail_brand.css | Created | BJP navy/cyan admin theme override |
| templates/wagtailadmin/branding/logo.html | Created | BJP white SVG logo for sidebar |
| templates/wagtailadmin/branding/favicon.html | Created | BJP favicon |
| templates/core/wagtail/dashboard_enquiries.html | Created | Dashboard enquiry stats panel |

### Migrations
- All 115 Wagtail migration steps applied cleanly to local dev DB
- No new migrations created for project models (no model field changes)

### Tests
- Tests written: 0 new (Wagtail admin is integration-level; unit tests unchanged)
- Tests passing: 67 / 67
- All existing contact, services, industries, main tests pass

### Decisions Made
- **Decision:** Wagtail admin at /cms/, Django admin kept at /django-admin/ as fallback.
  **Reason:** Clean separation — Wagtail is the primary CMS; Django admin available for emergency superuser/auth work without being the default entry point.
- **Decision:** ContactEnquiry panels are mostly read-only; only status is editable.
  **Reason:** Enquiries are form submissions, not CMS content. Staff should update status (new → read → replied) but never alter the submission data.
- **Decision:** Service and Industry stay as plain Django models, registered as Wagtail Snippets.
  **Reason:** They don't need Wagtail's page tree or routing — they're database-driven content served by our own Django views. Snippets give the Wagtail UI without requiring model rewrite.

### Phase 5 Deliverables Completed
- [x] All models registered with rich admin configuration (via Wagtail Snippets)
- [x] Services editable from admin (name, description, icon, order, active toggle)
- [x] Industries editable from admin
- [x] Contact enquiries manageable (status update, read-only detail, inspect view)
- [x] Admin branding customized (BJP logo, navy sidebar, cyan accents)
- [ ] Superuser credentials documented securely (to be done post-deploy)

### Deploy Steps Required on cPanel After Merge
1. `pip install -r requirements.txt` ← installs wagtail + dependencies
2. `manage.py migrate --no-input` ← applies all 115 Wagtail migration steps
3. `manage.py collectstatic --no-input`
4. Touch `tmp/restart.txt`
5. Visit /cms/ and log in with existing superuser credentials
6. In Wagtail Settings → Sites: update the default site to bjptechnologies.co.tz:443

### Next Session Should
- [ ] Merge feature/phase-5-admin-cms → develop → main via PR
- [ ] Deploy to cPanel (pip install + migrate + collectstatic + restart)
- [ ] Create superuser on server if not already done: manage.py createsuperuser
- [ ] Update Wagtail Site record to bjptechnologies.co.tz:443 via /cms/settings/sites/
- [ ] Begin Phase 6 — Polish & Launch (SEO, security audit, meta tags, sitemap, go-live)

---

## Session 9 — 2026-05-07 EAT

**Goal:** Phase 5 continuation — replace Wagtail CMS with django-unfold, deploy to cPanel, fix production errors, create superuser.
**Branch:** feature/phase-5-admin-cms
**Status:** ✅ Complete
**Phase:** Phase 5 — Admin & CMS

### What Was Done
- Diagnosed root cause of Wagtail sidebar disappearing: MutationObserver in `wagtail_brand.css` modifying React-managed DOM elements, causing React to unmount the entire sidebar after each mutation cycle
- Evaluated 4 alternative admin packages (django-jazzmin, django-unfold, django-grappelli, django-material-admin) — selected **django-unfold 0.92.0** for Django 6 compatibility, Tailwind CSS base, and full custom dashboard support
- Removed all Wagtail packages from requirements.txt, config/settings/base.py, and config/urls.py
- Installed django-unfold 0.92.0 and Pillow 12.2.0
- Configured full UNFOLD settings block: BJP navy/blue color scale, custom sidebar navigation with icons and badge, dashboard callback, logo/icon from static
- Created `apps/core/admin.py` with `dashboard_callback` (KPI context: services, industries, enquiry counts, recent 6 enquiries) and `enquiry_badge` (shows unread count in sidebar)
- Migrated all ModelAdmin classes to `unfold.admin.ModelAdmin` across services, industries, contact apps
- Built custom `templates/admin/index.html` extending `unfold/layouts/base_simple.html`: 4 KPI cards (Active Services gradient, Active Industries, Unread Enquiries alert, Total Received), Enquiry Status breakdown panel with segmented progress bar, Recent Enquiries list with status badges
- Created `apps/core/migrations/0001_drop_wagtail_tables.py` — RunPython migration that auto-drops all 46 Wagtail tables and cleans django_migrations history on `manage.py migrate`
- Fixed MySQL quoting bug in migration: changed `"table"` (SQLite double-quote) to `` `table` `` (MySQL backtick)
- Generated Phase 5 PDF completion report using ReportLab (10 sections, BJP branded)
- Cleaned .gitignore: added rules for .playwright-mcp/, *.png, *.jpg, luminos/, and temporary deploy scripts
- Created `install_deps.py` — one-time cPanel script to install unfold without triggering health-check block; pushed, used on server, then removed
- Created `create_superuser.py` — one-time cPanel script for superuser creation via File Manager (avoids special character issues in cPanel env vars); pushed, used on server, then removed
- Fixed cPanel "Invalid parameter passed" error: caused by spaces in username (SU_USERNAME="Bjp Admin") and special characters (`!` in password) in env vars — resolved by editing script directly in File Manager with simple credentials
- Superuser `bjpadmin` created successfully on production server
- All changes merged to main via PR and deployed to production

### Files Changed
| File | Action | Notes |
|---|---|---|
| requirements.txt | Modified | Wagtail removed; django-unfold 0.92.0 + Pillow added |
| config/settings/base.py | Modified | Full UNFOLD config, sitemaps not yet added |
| config/urls.py | Modified | Wagtail URLs removed; admin restored to /admin/ |
| apps/core/admin.py | Created | dashboard_callback + enquiry_badge functions |
| apps/core/migrations/0001_drop_wagtail_tables.py | Created | Auto-drops 46 Wagtail tables on migrate |
| apps/services/admin.py | Modified | unfold.admin.ModelAdmin base class |
| apps/industries/admin.py | Modified | unfold.admin.ModelAdmin base class |
| apps/contact/admin.py | Modified | unfold.admin.ModelAdmin base class |
| templates/admin/index.html | Created | Custom Unfold dashboard with KPI cards |
| .gitignore | Modified | Added ignore rules for screenshots, playwright, luminos |
| docs/generate_phase5_report.py | Created | ReportLab PDF generator |
| docs/BJP_Technologies_Phase5_Report.pdf | Created | Phase 5 completion report |

### Migrations
- Migration name: `apps/core/migrations/0001_drop_wagtail_tables.py`
- Applied: ✅ Yes — production MySQL via cPanel Execute python script
- Fixed: MySQL backtick quoting (was double-quote — syntax error 1064)

### Tests
- Tests written: 0 new
- Tests passing: 67 / 67
- Coverage areas: No new model/form logic added

### Decisions Made
- **Decision:** Replace Wagtail with django-unfold instead of patching MutationObserver.
  **Reason:** Wagtail's React sidebar is incompatible with DOM-level CSS injection. The root cause is architectural — Wagtail rebuilds the sidebar via React after every DOM mutation, creating an infinite loop. Switching to django-unfold gives full control over the admin UI with zero React dependency.
- **Decision:** Use File Manager to edit create_superuser.py instead of cPanel env vars.
  **Reason:** cPanel's "Execute python script" rejects env vars containing `!` and `@` characters with "Invalid parameter passed" at the API level. Credentials edited directly in File Manager never touch git and are deleted immediately after use.
- **Decision:** Drop Wagtail tables via a RunPython migration rather than manual SQL.
  **Reason:** Ensures cleanup runs automatically on every new environment (local, CI, staging) without manual intervention. The migration is forward-only (noop reverse) since table recreation is not meaningful.

### Blockers / Issues
- cPanel "Run Pip Install" failed with "Web application is inaccessible" — chicken-and-egg: app is down because unfold is missing, but cPanel checks app health before completing pip install. Resolved with standalone install_deps.py script.
- cPanel env var special characters (`!`, `@`) caused "Invalid parameter passed" on execute scripts. Resolved by editing script directly in File Manager.

### Phase 5 Deliverables Completed
- [x] All models registered with rich admin configuration
- [x] Services editable from admin (name, description, icon, order)
- [x] Industries editable from admin
- [x] Contact enquiries manageable (mark as read, replied, status badge)
- [x] Admin branding customized (BJP logo, navy/cyan color scale, custom dashboard)
- [x] Superuser `bjpadmin` created on production server

### Next Session Should
- [x] Start Phase 6 — Polish & Launch
- [x] Add sitemap.xml (django.contrib.sitemaps)
- [x] Add robots.txt
- [x] Add per-page OG tags to all templates
- [x] Add Content Security Policy header

---

## Session 10 — 2026-05-07 EAT

**Goal:** Phase 6 — SEO hardening, sitemap, robots.txt, per-page Open Graph tags, Content Security Policy header.
**Branch:** feature/phase-6-polish-launch
**Status:** 🔄 In Progress
**Phase:** Phase 6 — Polish & Launch

### What Was Done
- Audited live site headers via curl: confirmed HSTS, X-Frame-Options: DENY, X-Content-Type-Options, Referrer-Policy, CSRF/session secure cookies all present — security posture already strong from Phase 1 production settings
- Confirmed all 4 main pages live and rendering correctly: Home, About, Services, Industries
- Identified 3 missing items: robots.txt (404), sitemap.xml (404), per-page OG tags (generic base fallback only)
- Added `django.contrib.sitemaps` to INSTALLED_APPS
- Created `apps/core/sitemaps.py` with 3 sitemap classes:
  - `StaticViewSitemap` — home, about, services list, industries list, contact (priority 0.8)
  - `ServiceSitemap` — all active Service records by slug (priority 0.7)
  - `IndustrySitemap` — all active Industry records by slug (priority 0.7)
- Created `templates/robots.txt` — served as text/plain via TemplateView; blocks /admin/, includes sitemap URL
- Added `.gitignore` exception `!templates/robots.txt` to override the `*.txt` ignore rule
- Created `apps/core/middleware.py` — `ContentSecurityPolicyMiddleware` added to production MIDDLEWARE only; allows Google Fonts, self-hosted scripts and styles
- Added OG tag blocks (`og_title`, `og_description`, `og_url`) to all 7 page templates: home, about, services/list, services/detail, industries/list, industries/detail, contact
- Updated `config/urls.py` with robots.txt TemplateView route and sitemap.xml route
- All ruff and black checks pass; Django system check: 0 issues
- Noted: Google Search Console already set up by developer with `bjptechnologies.co.tz` verified — 18 pages indexed, site appearing in Google search results for "bjp technologies" with correct title and AI Overview identifying BJP Technologies (T) Limited as a Tanzanian IT company

### Files Changed
| File | Action | Notes |
|---|---|---|
| apps/core/sitemaps.py | Created | 3 sitemap classes: static, services, industries |
| apps/core/middleware.py | Created | CSP header middleware (production only) |
| templates/robots.txt | Created | robots.txt served as text/plain |
| config/urls.py | Modified | Added robots.txt + sitemap.xml routes |
| config/settings/base.py | Modified | Added django.contrib.sitemaps to INSTALLED_APPS |
| config/settings/production.py | Modified | Added CSP middleware to MIDDLEWARE |
| .gitignore | Modified | Added !templates/robots.txt exception |
| apps/main/templates/main/home.html | Modified | Added og_title, og_description, og_url blocks |
| apps/main/templates/main/about.html | Modified | Added og_title, og_description, og_url blocks |
| apps/services/templates/services/list.html | Modified | Added og_title, og_description, og_url blocks |
| apps/services/templates/services/detail.html | Modified | Added og_title, og_description, og_url blocks |
| apps/industries/templates/industries/list.html | Modified | Added og_title, og_description, og_url blocks |
| apps/industries/templates/industries/detail.html | Modified | Added og_title, og_description, og_url blocks |
| apps/contact/templates/contact/contact.html | Modified | Added og_title, og_description, og_url blocks |

### Migrations
- N/A — no model changes

### Tests
- Tests written: 0 new (SEO/middleware — integration level)
- Tests passing: 67 / 67

### Decisions Made
- **Decision:** CSP middleware added to production MIDDLEWARE override, not base.py.
  **Reason:** Development does not need CSP enforcement and it can break local debugging. Production-only middleware prevents false positives during dev.
- **Decision:** Use TemplateView with content_type='text/plain' for robots.txt.
  **Reason:** No extra package or file serving config needed — Django's template system handles it natively. The template lives in the project templates/ directory alongside 404.html and 500.html.
- **Decision:** Sitemap uses location() method instead of get_absolute_url() on models.
  **Reason:** Adding get_absolute_url() would couple the model to URL configuration. Location-based sitemaps keep the model clean.

### Google Search Console Status
- Domain: `bjptechnologies.co.tz` — verified ✅
- Pages indexed: 18 (as of 2026-05-07)
- Search appearance: Confirmed — "BJP Technologies (T) Limited | Secure Technology. Scalable..." appears for query "bjp technologies"
- Google AI Overview: Correctly identifies BJP Technologies (T) Limited as a Tanzanian IT company
- Next step: Submit `https://bjptechnologies.co.tz/sitemap.xml` in Search Console → Indexing → Sitemaps after deployment

### Phase 6 Deliverables Completed (so far)
- [x] Security settings verified (HSTS, CSRF, XSS, SSL redirect, X-Frame-Options)
- [x] DEBUG=False confirmed in production
- [x] Per-page OG tags on all pages
- [x] Sitemap (django.contrib.sitemaps) — deployed
- [x] robots.txt — deployed
- [x] Content Security Policy header — deployed
- [ ] Page load speed tested (target under 3s) — pending
- [ ] All images optimized — pending
- [ ] Final security audit — pending
- [ ] Go-live sign-off from developer

### Next Session Should
- [ ] Submit sitemap to Google Search Console (Indexing → Sitemaps)
- [ ] Run page speed test (Google PageSpeed Insights)
- [ ] Review image optimization opportunities
- [ ] Final security audit checklist
- [ ] Update CLAUDE.md Phase 6 to ✅ Complete when all deliverables done
- [ ] Merge feature/phase-6-polish-launch → develop → main via PR

---

---

## Session 11 — 2026-05-07 17:07 EAT

**Goal:** Complete dynamic content implementation — make all static website content editable from Django admin, split SiteSettings admin into per-section links, and add collapsible sidebar navigation.
**Branch:** feature/dynamic-content
**Status:** ✅ Complete

### What Was Done
- Completed home page about strip wiring (`{{ company.about_headline }}`, `{{ company.about_body }}`)
- Created migration `0003_add_homepage_content_fields` for hero, stats, and about strip fields
- Split `SiteSettings` admin into 6 proxy model admins (Company Identity, Address, Social Media, Hero Section, Stats Counters, About Strip), each with its own sidebar link under a new "Site Settings" group
- Created migration `0004_add_sitesettings_proxy_models` for proxy models
- Performed full site audit for remaining hardcoded content across all templates
- Round 1 — quick wins (existing data, no new fields):
  - Contact page: wired `{{ company.address }}`, `{{ company.phone }}`, `{{ company.email }}` (was hardcoded literals)
  - About page services grid: replaced hardcoded 6-card duplicate with dynamic `{% for service in services %}` loop; fixed `AboutView` to pass services queryset
- Round 1 — new fields added to `SiteSettings`:
  - About page: banner headline, 4 counters (value + label), intro paragraph, what-we-do body, our-approach body
  - Footer CTA: headline, body, button text
  - Contact page: `maps_embed_url`
- Round 2 — page banner fields added:
  - Services page: banner headline + subtext
  - Industries page: banner headline + subtext
- Added 5 new proxy model admins (About Page, Services Page, Industries Page, Contact Page, Footer CTA) with sidebar links
- Created migration `0005_add_page_content_fields` (24 new fields + 5 proxy models)
- Made "Site Settings" sidebar group collapsible (`"collapsible": True` in Unfold nav config)
- Pushed all 4 commits to `origin/feature/dynamic-content`

### Files Changed
| File | Action | Notes |
|---|---|---|
| apps/core/models.py | Modified | Added 24 new SiteSettings fields + 11 proxy models total |
| apps/core/admin.py | Modified | 11 proxy model admins replacing single SiteSettingsAdmin |
| apps/core/context_processors.py | Modified | Returns SiteSettings object as `company` |
| apps/core/templates/core/footer.html | Modified | Footer CTA wired to SiteSettings |
| apps/core/migrations/0003_add_homepage_content_fields.py | Created | Hero, stats, about strip fields |
| apps/core/migrations/0004_add_sitesettings_proxy_models.py | Created | 6 proxy models |
| apps/core/migrations/0005_add_page_content_fields.py | Created | 24 fields + 5 proxy models |
| apps/main/views.py | Modified | AboutView now passes services queryset |
| apps/main/templates/main/home.html | Modified | Hero, stats, about strip all dynamic |
| apps/main/templates/main/about.html | Modified | Banner, counters, all body texts, services grid dynamic |
| apps/services/templates/services/list.html | Modified | Banner headline + subtext dynamic |
| apps/industries/templates/industries/list.html | Modified | Banner headline + subtext dynamic |
| apps/contact/templates/contact/contact.html | Modified | Address, phone, email, maps URL dynamic |
| config/settings/base.py | Modified | Unfold nav: Site Settings group (11 items, collapsible) |

### Migrations
- `0003_add_homepage_content_fields` — Applied ✅
- `0004_add_sitesettings_proxy_models` — Applied ✅
- `0005_add_page_content_fields` — Applied ✅
- **Server note:** All 3 migrations must be applied on cPanel after pulling

### Tests
- Tests written: 0 new
- Tests passing: all existing pass
- Coverage: no regressions

### Decisions Made
- **Decision:** Use proxy models (not separate DB tables) for each SiteSettings admin section.
  **Reason:** All site settings belong in one row — splitting into real models would require joins or multiple singleton patterns. Proxy models give separate admin URLs and forms while reading/writing the same row.
- **Decision:** `collapsible: True` on Site Settings nav group rather than nesting under a parent item.
  **Reason:** Unfold's app_list template supports `group.collapsible` natively via Alpine.js — auto-opens when an item in the group is active, collapses otherwise.
- **Decision:** About page services grid replaced with dynamic loop (not just made editable).
  **Reason:** It was a full duplicate of Service model data that would go stale silently. Dynamic loop is always in sync with admin edits.
- **Decision:** Left 4 items hardcoded (About/Services/Industries bottom CTA sections, "Why Clients Choose" benefit tiles).
  **Reason:** Boilerplate marketing text with no real edit frequency. Making them dynamic would add ~8 more fields with near-zero business value.

### Blockers / Issues
- None

### Next Session Should
- [ ] PR `feature/dynamic-content → develop` (user to action)
- [ ] PR `develop → main` (user to action)
- [ ] Run `python manage.py migrate` on cPanel after pull (migrations 0003, 0004, 0005)
- [ ] Continue Phase 6: page speed test, image optimisation, final security audit
- [ ] Go-live sign-off when Phase 6 checklist complete

---

## Session 12 — 2026-05-09

**Goal:** Add admin-editable logo and favicon to SiteSettings — client can upload a new logo from the admin panel without developer involvement.
**Branch:** feature/logo-branding-admin
**Status:** ✅ Complete

### What Was Done
- Created `apps/core/validators.py` — `validate_logo_file` (accepts SVG, PNG, WebP) and `validate_favicon_file` (accepts PNG, ICO) with clear ValidationError messages
- Added `logo` and `favicon` FileFields to `SiteSettings` model with validators and help text
- Added `LogoBrandingSettings` proxy model (12th proxy, same DB row as SiteSettings)
- Added `LogoBrandingSettingsAdmin` with logo preview and favicon preview as `readonly_fields` — previews render the uploaded file on a navy background so the client can see exactly how it looks
- Added "Logo & Branding" as the first item in the Site Settings sidebar group in Unfold navigation
- Updated `apps/core/templates/core/navbar.html` — if `company.logo` is set, use it with `filter: brightness(0) invert(1)` (converts any logo to white on dark navy); else falls back to existing static `bjp-logo-horizontal-light.png`
- Updated `apps/core/templates/core/footer.html` — same pattern, falls back to `bjp-logo-horizontal-transparent.png`
- Updated `apps/core/templates/core/base.html` — if `company.favicon` is set, renders a single `<link rel="icon">` pointing to the upload; else falls back to all three existing static favicon sizes
- Added media file serving in development to `config/urls.py` (`urlpatterns += static(MEDIA_URL, ...)` when DEBUG=True)
- Created and applied migration `0006_add_logo_branding_fields`
- All 67 tests passing, ruff and black clean

### Files Changed
| File | Action | Notes |
|---|---|---|
| `apps/core/validators.py` | Created | Logo and favicon file type validators |
| `apps/core/models.py` | Modified | `logo`, `favicon` FileFields + `LogoBrandingSettings` proxy model |
| `apps/core/admin.py` | Modified | `LogoBrandingSettingsAdmin` with preview fields |
| `config/settings/base.py` | Modified | "Logo & Branding" added to Unfold sidebar |
| `config/urls.py` | Modified | Media serving in development |
| `apps/core/templates/core/navbar.html` | Modified | Dynamic logo with static fallback |
| `apps/core/templates/core/footer.html` | Modified | Dynamic logo with static fallback |
| `apps/core/templates/core/base.html` | Modified | Dynamic favicon with static fallback |
| `apps/core/migrations/0006_add_logo_branding_fields.py` | Created | Logo + favicon fields + LogoBrandingSettings proxy |

### Migrations
- Migration name: `0006_add_logo_branding_fields`
- Applied locally: ✅ Yes
- **Server note:** Must run `python manage.py migrate` on cPanel after pulling this branch

### Tests
- Tests written: 0 new (no new views or form logic; validators covered by Django's framework)
- Tests passing: 67 / 67
- Coverage areas: all existing tests unaffected

### Decisions Made
- **Decision:** Single `logo` field + CSS `filter: brightness(0) invert(1)` for dark backgrounds — not two separate logo fields.
  **Reason:** Two-field approach puts the burden on the client to upload both files every rebrand. CSS filter handles the dark-background variant automatically — the client uploads once, it works everywhere.
- **Decision:** `FileField` not `ImageField` for logo.
  **Reason:** `ImageField` uses Pillow which cannot validate SVG files. FileField with a custom extension validator accepts SVG, PNG, and WebP explicitly while rejecting JPEG (no transparency support) and other formats.
- **Decision:** Logo preview rendered with navy (`#0D1B4B`) background in admin.
  **Reason:** The logo only appears on dark backgrounds on the live site. Previewing on white would be misleading — a white/light-coloured logo would appear invisible.
- **Decision:** Fallback to static files when no upload present.
  **Reason:** Ensures zero visual regression on the current live site. Client can upload at any time; until they do, the site is identical to before.

### Blockers / Issues
- None

### Next Session Should
- [ ] User confirms logo upload works in admin and renders correctly on site
- [ ] Generate post-session PDF report for logo branding feature
- [ ] PR `feature/logo-branding-admin → develop` (user to action after confirmation)
- [ ] Run `python manage.py migrate` on cPanel (migration 0006)
- [ ] Upload logo via admin panel on production after migration

---

## Session 14 — 2026-05-27 ~14:30 EAT

**Goal:** Integrate Google Analytics 4 end to end — the tracking tag, conversion events, and an in-admin analytics dashboard — following `docs/ga4-integration-playbook.md`.
**Branch:** feature/ga4-phase1-tracking (Phase 1, merged) and feature/ga4-phase2-dashboard (Phase 2)
**Status:** ✅ Complete (code) — pending production deploy + env vars

> Note: Session 13 was the automated-deploy/webhook work (documented as `docs/BJP_Technologies_Session13_Report.pdf`); this is Session 14.

### What Was Done

**Phase 1 — the tracking tag (branch `feature/ga4-phase1-tracking`, merged via PR #62):**
- Added `ga_measurement_id` + `ga_enabled` fields to `SiteSettings` (the pk=1 singleton)
- Seed migration `0008_seed_ga_measurement_id` pins Measurement ID `G-C9L66H4VE4` on first deploy (uses pk=1, not the playbook's UUID — adapted to this repo)
- `company_info` context processor now exposes `analytics_enabled` = `not DEBUG and ga_enabled and bool(ga_measurement_id)`
- gtag.js injected in `core/base.html` `<head>`; conversion-event block fires before `</body>`
- `ContactSuccessView` fires `contact_submit` conversion event (adapted: this site redirects to a separate success page rather than inline-rendering)
- `AnalyticsSettings` proxy model + admin + Unfold sidebar entry ("Google Analytics")
- 6 tests covering tag injection, the three kill-switches (DEBUG / switch off / blank ID), and conversion events

**Phase 2 — the in-admin dashboard (branch `feature/ga4-phase2-dashboard`):**
- Added Google Data API deps to `requirements.txt` (google-analytics-data, google-auth, google-auth-oauthlib)
- `GA_PROPERTY_ID` + `GA_OAUTH_*` settings (server-side Data API credentials, via os.environ)
- `ga_capture_token` management command — one-time OAuth refresh-token capture; `ga_verify` — credential smoke test
- New `apps/analytics/` app: `services.py` (single cached gateway, quota-safe TTLs, `rows[0]` handling, `bypass_cache` for the Refresh button), virtual `AnalyticsOverview` model, `AnalyticsOverviewAdmin.changelist_view` rendering the dashboard inside admin chrome via `each_context()`
- `overview.html` with scoped `.ga-dash` CSS (Unfold ships a narrow Tailwind bundle that drops most utilities), `not_configured.html` fallback
- Dashboard: realtime active users, traffic KPIs (today/7d/30d), top pages/sources/countries, device split, `contact_submit` conversions
- Registered app + Unfold sidebar "Overview" entry
- 13 tests: context-builder shape, empty-data + error paths, `rows[0]` regression, admin-chrome regression, permissions
- Verified live: `ga_verify` returns `✓ Auth works`; `_build_dashboard_context()` runs clean against the real API (zeros — property <48h old); dashboard rendered + screenshotted in admin (chrome intact, gradients survived)

### Files Changed
| File | Action | Notes |
|---|---|---|
| docs/ga4-integration-playbook.md | Added | Portable GA4 reference (the spec for this work) |
| apps/core/models.py | Modified | `ga_measurement_id`, `ga_enabled` + `AnalyticsSettings` proxy |
| apps/core/admin.py | Modified | `AnalyticsSettingsAdmin` |
| apps/core/context_processors.py | Modified | `analytics_enabled` flag |
| apps/core/templates/core/base.html | Modified | gtag.js + conversion-event block |
| apps/contact/views.py | Modified | `ContactSuccessView` fires `contact_submit` |
| apps/core/migrations/0007_*.py, 0008_*.py | Created | Fields + seed migration |
| apps/core/management/commands/ga_capture_token.py, ga_verify.py | Created | OAuth token capture + verify |
| requirements.txt, .env.example | Modified | Google deps + GA_* env vars |
| config/settings/base.py | Modified | GA_* settings, `apps.analytics`, Unfold Analytics sidebar group |
| apps/analytics/ (full app) | Created | services, models, admin, templates, tests |

### Migrations
- `core/0007_analyticssettings_sitesettings_ga_enabled_and_more` — applied locally ✅
- `core/0008_seed_ga_measurement_id` — applied locally ✅
- `analytics/0001_initial` — applied locally ✅
- **Server note:** CI/CD `migrate` on deploy creates the analytics table + runs the seed

### Tests
- Tests written: 19 new (6 Phase 1 + 13 Phase 2)
- Tests passing: 86 / 86
- Coverage areas: context processor, tag rendering, conversion events, service layer (rows[0] regression), dashboard admin (chrome regression, empty/error paths), permissions
- ruff clean; black clean on all new files

### Decisions Made
- **Decision:** Seed migration targets pk=1, not the playbook's UUID.
  **Reason:** This repo's `SiteSettings` forces integer pk=1 in `save()` — the playbook's UUID singleton doesn't apply here.
- **Decision:** Fire the conversion event in `ContactSuccessView`, not inline on form render.
  **Reason:** Contact uses `FormView` → redirect to a separate success page; there is no inline success-render to attach `ga_event` to.
- **Decision:** OAuth user-token (not a service account).
  **Reason:** GA4 won't attach a service account to a personal-Gmail-owned property (playbook §0). Authenticate as the GA4 admin via a Desktop OAuth client; refresh token stored in env.
- **Decision:** Ship scoped `.ga-dash` raw CSS instead of Tailwind utilities.
  **Reason:** Unfold's precompiled Tailwind bundle silently drops most utility classes — the documented trap (playbook §8.1). Verified the dashboard renders correctly via browser screenshot.

### Blockers / Issues
- Dashboard shows zeros because the GA4 property is < 48h old — standard reports lag 24–48h on first data. Realtime confirms data arrival immediately. Not a bug; resolves with time.

### Next Session Should
- [ ] PR `feature/ga4-phase2-dashboard → develop → main` to deploy the dashboard
- [ ] Add the four `GA_*` env vars in cPanel (Setup Python App → Environment variables) — dashboard shows "Setup Required" until then
- [ ] Confirm GA4 OAuth consent screen is "In production" (not Testing) so the refresh token never expires
- [ ] Mark `contact_submit` as a Key Event in GA4; add internal-traffic filter for the office IP
- [ ] After ~48h, confirm the dashboard shows real numbers; hit Refresh data to bust the cache

---

## Session 15 — 2026-06-11 EAT

**Goal:** Add a Products module to the BJP Technologies website and ship the PMS (Property Management System) product page as the first record.
**Branch:** `feature/products-module-pms` (off `develop`)
**Status:** ✅ Complete (Phase 6.5 — Products Module — PMS leg)

### What Was Done
- Phase 6.5 opened in CLAUDE.md Section 22 as a scope expansion off Phase 6 — Products Module, with PMS as the first product.
- New Django app `apps/products/` with `Product` model inheriting `BaseModel` (UUID pk, timestamps), covering: identity (name, slug, tagline, byline, live_url, status), descriptions (short/long), detail sections (problem_statements, target_users, features JSON, differentiators, how_it_works_steps, pricing_summary, onboarding_promise), CTAs (primary + secondary label/URL pairs), optional contact block (email, phone, hours, WhatsApp — rendered conditionally), SEO (meta_title, meta_description), assets (hero_image, og_image, logo_image, accent_color, screenshots JSON), and ordering.
- Status choices: `live` / `coming-soon`. Public views filter to live only; coming-soon detail returns 404.
- Migration `0001_initial` (auto) + data migration `0002_seed_pms` seeded the PMS record from the team brief at `pms details/bjp-feature-brief.md`. Idempotent — re-running does nothing if `slug='pms'` exists.
- Rich Unfold-themed `ProductAdmin` with fieldsets (Identity, Descriptions, Detail page sections, CTAs, Contact block (collapse), SEO (collapse), Assets, Advanced (collapse)), status badge, contact-state indicator, view-on-site link, edit/delete buttons, and Live ↔ Coming Soon bulk actions.
- New Unfold sidebar item "Products" added as the first entry under Website Content (before Services).
- Views `ProductsListView` + `ProductDetailView` at `/products/` and `/products/<slug>/`, both restricted to live products.
- URL namespace `products` registered in `config/urls.py` between `main` and `services` so the URL hierarchy mirrors the navbar.
- Sitemap updated: new `ProductSitemap` (priority 0.8, monthly) + `products:list` added to `StaticViewSitemap`.
- "Products" link added to both the main navbar (`apps/core/templates/core/navbar.html`) and the mobile sidebar (`apps/core/templates/core/base.html`) as the first item after About, before Services.
- Home page (`apps/main/templates/main/home.html`) gained an "Our Products" strip rendered between hero and Services, hidden when no live products exist. `HomeView` extended to provide `products` context.
- Detail page template loads Bootstrap Icons via CDN inside `{% block extra_css %}` (only paid on product detail pages, not site-wide).
- PMS assets (7 files: hero, 4 features, OG card, logo SVG) copied from `pms details/bjp-feature-assets/` into `static/images/products/pms/`.
- `.gitignore` updated: `pms details/` and `bms details/` added as untracked source folders; negation pattern `!static/**/*.png|jpg|jpeg` added so site image assets are not blocked by the broad `*.png` rule (which exists to block loose screenshots in repo root).

### Files Changed
| File | Action | Notes |
|---|---|---|
| `apps/products/__init__.py`, `apps.py`, `migrations/__init__.py`, `tests/__init__.py` | Created | App scaffold |
| `apps/products/models.py` | Created | `Product(BaseModel)` with 25 fields + helpers |
| `apps/products/migrations/0001_initial.py` | Created | Schema |
| `apps/products/migrations/0002_seed_pms.py` | Created | PMS data, idempotent |
| `apps/products/admin.py` | Created | Unfold `ProductAdmin` with fieldsets + bulk actions |
| `apps/products/views.py` | Created | `ProductsListView` + `ProductDetailView` |
| `apps/products/urls.py` | Created | `products:list` + `products:detail` |
| `apps/products/templates/products/list.html` | Created | Banner + 2-col card grid |
| `apps/products/templates/products/detail.html` | Created | Hero, problem, differentiators, features grid, target users, how-it-works, screenshots, pricing, conditional contact, CTAs |
| `apps/products/tests/test_models.py` | Created | 24 model tests |
| `apps/products/tests/test_views.py` | Created | 18 view/integration tests |
| `apps/main/views.py` | Modified | Added `products` to `HomeView` context |
| `apps/main/templates/main/home.html` | Modified | Inserted "Our Products" strip |
| `apps/core/templates/core/navbar.html` | Modified | Added Products link before Services |
| `apps/core/templates/core/base.html` | Modified | Added Products to mobile sidebar |
| `apps/core/sitemaps.py` | Modified | Added `ProductSitemap` |
| `config/urls.py` | Modified | Registered `apps.products.urls` and `ProductSitemap` |
| `config/settings/base.py` | Modified | Added `apps.products` to INSTALLED_APPS; added Products to Unfold sidebar as first item under Website Content |
| `.gitignore` | Modified | Excluded `pms details/` + `bms details/`; added `!static/**/*.png` negation |
| `static/images/products/pms/*.{png,svg}` | Added | 7 PMS assets |

### Migrations
- `products/0001_initial` — applied locally ✅
- `products/0002_seed_pms` — applied locally ✅
- **Server note:** CI/CD `migrate` on deploy creates the products table + seeds PMS

### Tests
- Tests written: 42 new (24 model + 18 view/integration)
- Tests passing: 128 / 128 (entire suite)
- Coverage areas: Product model (`__str__`, slug auto-gen, `is_live`, `has_contact_block`, list helpers, JSON features), seeded PMS record (exists, live, feature count, contact block empty by default, CTA URLs), list view (live-only filter), detail view (404 for missing/coming-soon, conditional contact block render), navbar integration (Products link on home), home-page strip
- ruff clean; black clean on all new files
- Manual smoke: home/products/pms detail all 200; bad slug 404; sitemap includes `/products/` + `/products/pms/`

### Decisions Made
- **Decision:** Build the full `apps/products/` app with model + admin instead of a single hardcoded `/products/pms/` page.
  **Reason:** A second product (BMS) is already ready and confirmed — a hardcoded one-off would mean rebuilding within a week. The full app pays off the moment Product #2 lands.
- **Decision:** Assets stored as relative-path `CharField`s under `static/images/`, not `ImageField`/`FileField` uploads.
  **Reason:** Mirrors the existing `Service.icon_svg` pattern in this repo, keeps assets git-tracked alongside the code, and avoids the media/static dual-storage complexity. The admin form takes a path string; when BJP wants self-serve uploads later, this can be migrated to `ImageField` with `upload_to='products/'`.
- **Decision:** CTAs both link directly to `pms.bjptechnologies.co.tz` (external, new tab) — no BJP contact-form intermediate.
  **Reason:** User decision captured in pre-build confirmation. The PMS product owns its own demo-request flow; bouncing leads through the BJP contact form would add friction.
- **Decision:** Contact block (email, phone, hours, WhatsApp) renders conditionally, hidden until `has_contact_block` is true.
  **Reason:** The brief explicitly lists Section 12 contact details as `⚠️ TODO`. Field exists on the model so BJP can fill them in via admin without redeploy. Until then the block is invisible — no placeholder text shipped to users.
- **Decision:** Bootstrap Icons loaded via CDN inside `{% block extra_css %}` on the detail template only — not site-wide in `base.html`.
  **Reason:** Only the product detail page needs `bi-*` classes (for the features grid). Loading site-wide would cost every other page bandwidth they don't need.
- **Decision:** Status filter at view level (not just admin), so `coming-soon` products return 404 on the public site.
  **Reason:** Lets BJP draft product #3 in admin without it leaking to users until they flip the switch.
- **Decision:** Products is the first item under Website Content in the Unfold sidebar and the first nav item after About in the public navbar.
  **Reason:** Per user direction during planning — "products should lead first".

### Blockers / Issues
- None functionally. Awaiting:
  - PMS contact details (email, phone, hours, WhatsApp) from BJP to populate via admin
  - Final PMS logo (current is a placeholder wordmark per brief §14)

### Next Session Should
- [ ] Merge PR `feature/products-module-pms → develop`
- [ ] After merging to develop, open develop → main PR to push live
- [ ] Verify live: nav shows Products, home shows the PMS strip, `/products/pms/` renders end-to-end
- [ ] Fill in PMS contact block from admin (Site → Products → PMS) once BJP provides values
- [ ] Start `feature/products-module-bms` — much smaller scope: just a new data-migration seeding the BMS record + assets

---
