# Adam Bielas — portfolio

Personal portfolio for Adam Bielas, Full Stack Developer from Tychy, Poland.

**Site:** https://rabuuwu.github.io/.

## What is included

- Polish and English content. The first browser language determines the initial locale: Polish for `pl-*`, English otherwise. A manual language choice takes precedence and persists locally.
- Light and dark themes. The initial theme follows the operating system; a manual choice persists locally. Changes to the system theme are followed until a manual preference is stored.
- A concise homepage with biography, a professional timeline, eight competence groups, a seven-step work approach, personal context and collaboration scope.
- Six detailed bilingual case studies: CRM inventory, AI call summaries, KSeF, the test customer-request app, D&D Companion and TradingHelper.
- An additional FSE-IT experiment, explicitly separated from completed commercial work.
- Genuine application screenshots: the public D&D Companion login and a locally running TradingHelper dashboard in offline sample mode.
- Email, LinkedIn and GitHub contact links.
- CV preview in a keyboard-accessible modal and download in the selected language. Both original PDF versions are included with the owner's authorization; they contain the contact information from the CV.
- Responsive layout, visible keyboard focus, skip link, reduced-motion support and readable static content when JavaScript is disabled.
- Locally hosted Manrope variable font, distributed under the SIL Open Font License in `assets/fonts/OFL.txt`. No third-party font requests or analytics.

The site uses plain HTML, CSS and JavaScript. No build tool, framework, backend, API keys or external translation service is required. English is the fallback for unsupported languages. Email links open the visitor's email application; the site does not send messages itself. PDF rendering depends on the browser's PDF viewer; a direct PDF link is provided as a fallback.

## Local preview

From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/. Use HTTP rather than opening `index.html` directly so that fonts, preferences and PDF resources behave consistently.

## Content and design

- `index.html`: English fallback content, section structure, contact links and SEO metadata.
- `content/portfolio.json`: reviewed English/Polish copy, timeline, competence examples, work steps and six case studies.
- `templates/home.html`: retained homepage layout; the generator replaces copy and adds the expanded sections.
- `scripts/build_portfolio.py`: dependency-free static generator. Run `python3 scripts/build_portfolio.py` after changing content or layout, then commit the generated HTML.
- `projects/<slug>/index.html`: generated static case study pages, each with canonical and Open Graph metadata and a working return link.
- `app.js`: shared language/theme preferences, translated metadata, mobile navigation and CV dialog. Default English content is always in HTML; reviewed page translations are embedded as non-executable JSON.
- `style.css`: design tokens, both palettes, typography, system illustration and responsive layouts.
- `assets/CV_Adam_Bielas_PL.pdf` and `assets/CV_Adam_Bielas_EN.pdf`: original CV files. Replace these exact filenames to update them.
- `assets/social.png`: social sharing image. Replace it if the identity or visual direction changes.
- `tests/browser_check.py`: homepage functional and responsive checks in a real Chromium browser.
- `tests/case_studies_check.py`: all-case-study navigation, translation, metadata, 320px layout, shared preferences, keyboard, CV and no-JavaScript checks.

The commercial case studies combine the CV with explicit owner confirmations. Both time improvements are **estimates from comparing average task times**, not controlled benchmarks. AI responsibility is split between recording access, using faster-whisper, custom API work, local-model fine-tuning, local-LLM summary generation and CRM presentation. The customer-request application remains a **test version**.

Personal-project features were checked in the current source, not inferred from technology dependencies alone. D&D Companion messaging is between users who are friends; a separate item-use operation was not found and is not advertised. TradingHelper does not submit broker orders; its broker profiles model costs. FSE-IT is an experiment: proposed ML and automated testing are not presented as implemented.

No company code, customer data, recordings or internal addresses are published. The commercial diagrams are explanatory illustrations. The D&D screenshot is an anonymous public login screen. The TradingHelper screenshot is the actual UI with isolated, generated **sample data**, not real market quotations or investment results. Private DealFlow details and unconfirmed personal plans are omitted.

## Browser verification

Requires Python 3.10+ and Google Chrome, or a Chromium installation with its executable passed through `CHROME_PATH`.

```sh
python3 -m pip install -r tests/requirements.txt
# Start the local server first, then:
python3 tests/browser_check.py
python3 tests/case_studies_check.py
```

The default Chrome executable is the macOS application path. For Linux:

```sh
CHROME_PATH=/usr/bin/google-chrome python3 tests/browser_check.py
CHROME_PATH=/usr/bin/google-chrome python3 tests/case_studies_check.py
```

To verify a deployed version:

```sh
PORTFOLIO_URL=https://rabuuwu.github.io python3 tests/browser_check.py
PORTFOLIO_URL=https://rabuuwu.github.io python3 tests/case_studies_check.py
```

Checks cover Polish and English, an unsupported-language fallback, system theme selection, manual preference persistence, restricted local storage, CV selection/preview, Escape and focus restoration, keyboard navigation, required resources and no horizontal overflow at 320, 390, 768 and 1440 px. Screenshots go to ignored `tests/screenshots/`. The JavaScript-disabled case checks content and CV fallback links.

## GitHub Pages

The workflow `.github/workflows/pages.yml` runs browser checks, packages only `index.html`, `style.css`, `app.js`, `.nojekyll`, `assets/` and `projects/`, and deploys on pushes to `main`. Content source, generators, templates, tests, repository metadata and local Vibe runtime files are excluded from the published artifact.

1. In repository **Settings → Pages**, select **GitHub Actions** as the source.
2. Push to `main`, or run **Deploy portfolio** manually from the Actions tab.
3. Wait for the deploy job to succeed. The deployment environment links to the live site.

GitHub Free supports Pages for public repositories. Keeping this repository private requires a GitHub plan that supports private-repository Pages. The site itself is intended to be public. See [GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## Preferences and privacy

The browser stores only `portfolio-language` and `portfolio-theme` in local storage. If storage is unavailable, switches still work for the current page. No contact form, cookies or application tracking are implemented. GitHub Pages hosting is subject to GitHub's own infrastructure policies.

## Reviewed sources and unresolved details

- Commercial work: original CV PL/EN and the owner’s explicit confirmations during this portfolio update. Original CV files remain unchanged.
- [D&D Companion](https://github.com/Rabuuwu/DnDCompanion/tree/1ba0778a7165dac4a4b4ff52e0781fdf039ca831): client/server packages, character ownership, campaign permissions, migrations and deployment workflow. The old local-hosting README description conflicts with the current Pages/Render setup; the case study follows current implementation and states the verification boundary.
- [TradingHelper](https://github.com/Rabuuwu/TradingHelper/tree/793b5bf8c41891638a56470a00b0a9977428aab9): provider, scanner, ntfy queue, PAPER, API, PWA and architecture. The screenshot was produced from that code with `MARKET_DATA_PROVIDER=sample`, alerts disabled and a separate temporary database.
- [FSE-IT](https://github.com/Rabuuwu/FSE-IT/tree/d1c4b1a581ab9ed49cc09536328a0d1dc37df5b0): implemented content/API functionality, separated from README intentions.

Possible future additions need owner confirmation: current availability and collaboration terms; the latest English-level declaration and LinkedIn status; individual technical decision rationales; current project usage, lessons learned and next steps. The LinkedIn URL was previously supplied directly by the owner; public LinkedIn access was restricted during this audit. No new C1 claim was added to the site text; the original CV retains its existing declaration.
