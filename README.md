# Adam Bielas — portfolio

Personal portfolio for Adam Bielas, Full Stack Developer from Tychy, Poland.

**Site:** https://rabuuwu.github.io/ (available after GitHub Pages is enabled and the deployment succeeds).

## What is included

- Polish and English content. The first browser language determines the initial locale: Polish for `pl-*`, English otherwise. A manual language choice takes precedence and persists locally.
- Light and dark themes. The initial theme follows the operating system; a manual choice persists locally. Changes to the system theme are followed until a manual preference is stored.
- Commercial CRM inventory and local-AI case studies, plus D&D Companion and TradingHelper project links.
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
- `app.js`: Polish translations, automatic locale selection, preference persistence and CV dialog behavior. English strings are read from the HTML; use the same `data-i18n` key to supply the Polish equivalent.
- `style.css`: design tokens, both palettes, typography, system illustration and responsive layouts.
- `assets/CV_Adam_Bielas_PL.pdf` and `assets/CV_Adam_Bielas_EN.pdf`: original CV files. Replace these exact filenames to update them.
- `assets/social.png`: social sharing image. Replace it if the identity or visual direction changes.
- `tests/browser_check.py`: functional and responsive checks in a real Chromium browser.

The case studies reflect the CV. Inventory improvements are approximate, and the mobile CRM app is explicitly described as a test version. Personal repositories are linked as source code, not as verified public demos. The system and case study graphics are illustrations, not screenshots of a client's CRM.

## Browser verification

Requires Python 3.10+ and Google Chrome, or a Chromium installation with its executable passed through `CHROME_PATH`.

```sh
python3 -m pip install -r tests/requirements.txt
# Start the local server first, then:
python3 tests/browser_check.py
```

The default Chrome executable is the macOS application path. For Linux:

```sh
CHROME_PATH=/usr/bin/google-chrome python3 tests/browser_check.py
```

To verify a deployed version:

```sh
PORTFOLIO_URL=https://rabuuwu.github.io python3 tests/browser_check.py
```

Checks cover Polish and English, an unsupported-language fallback, system theme selection, manual preference persistence, restricted local storage, CV selection/preview, Escape and focus restoration, keyboard navigation, required resources and no horizontal overflow at 320, 390, 768 and 1440 px. Screenshots go to ignored `tests/screenshots/`. The JavaScript-disabled case checks content and CV fallback links.

## GitHub Pages

The workflow `.github/workflows/pages.yml` runs browser checks, packages only `index.html`, `style.css`, `app.js`, `.nojekyll` and `assets/`, and deploys on pushes to `main`. Tests, repository metadata and local Vibe runtime files are excluded from the published artifact.

1. In repository **Settings → Pages**, select **GitHub Actions** as the source.
2. Push to `main`, or run **Deploy portfolio** manually from the Actions tab.
3. Wait for the deploy job to succeed. The deployment environment links to the live site.

GitHub Free supports Pages for public repositories. Keeping this repository private requires a GitHub plan that supports private-repository Pages. The site itself is intended to be public. See [GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## Preferences and privacy

The browser stores only `portfolio-language` and `portfolio-theme` in local storage. If storage is unavailable, switches still work for the current page. No contact form, cookies or application tracking are implemented. GitHub Pages hosting is subject to GitHub's own infrastructure policies.
