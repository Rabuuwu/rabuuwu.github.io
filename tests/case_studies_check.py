"""Browser regressions for the expanded portfolio and its case study journeys."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = os.environ.get('PORTFOLIO_URL', 'http://127.0.0.1:8765').rstrip('/')
CHROME = os.environ.get('CHROME_PATH', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
SLUGS = ['crm-inventory', 'ai-call-summaries', 'ksef', 'customer-app', 'dnd-companion', 'trading-helper']
SHOTS = Path(__file__).parent / 'screenshots'
SHOTS.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True)
    for locale, theme, width in [('en-US', 'light', 1440), ('pl-PL', 'dark', 390)]:
        context = browser.new_context(locale=locale, color_scheme=theme, viewport={'width': width, 'height': 900}, reduced_motion='reduce')
        page = context.new_page()
        errors, missing = [], []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.on('response', lambda r: missing.append(f'{r.status} {r.url}') if r.status >= 400 else None)
        page.goto(BASE, wait_until='networkidle')
        expect(page.locator('a[data-case-link]')).to_have_count(6)
        for anchor in ['experience', 'competencies', 'approach']:
            assert page.locator(f'#{anchor}').count() == 1
        assert page.locator('.competence-item').count() == 8
        assert page.locator('.work-step').count() == 7
        if width < 720:
            page.locator('#menu-toggle').click()
            expect(page.locator('#site-nav')).to_be_visible()
            page.keyboard.press('Escape')
            expect(page.locator('#site-nav')).not_to_be_visible()
            expect(page.locator('#menu-toggle')).to_be_focused()
        for slug in SLUGS:
            page.set_viewport_size({'width': width, 'height': 900})
            response = page.goto(f'{BASE}/projects/{slug}/', wait_until='networkidle')
            assert response.status == 200
            expect(page.locator('html')).to_have_attribute('lang', 'pl' if locale.startswith('pl') else 'en')
            expect(page.locator('html')).to_have_attribute('data-theme', theme)
            assert page.locator('h1').count() == 1
            assert page.locator('.case-section').count() >= 5
            assert page.locator('link[rel=canonical]').get_attribute('href') == f'https://rabuuwu.github.io/projects/{slug}/'
            assert page.locator('meta[property="og:url"]').get_attribute('content').endswith(f'/projects/{slug}/')
            assert page.locator('meta[property="og:title"]').get_attribute('content')
            assert page.locator('meta[property="og:description"]').get_attribute('content')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (slug, width)
            assert page.locator('[data-i18n]').evaluate_all('(els) => els.every(el => el.textContent.trim())')
            assert page.locator('[data-i18n]').evaluate_all('(els) => els.every(el => !!el.dataset.i18n)')
            page.screenshot(path=str(SHOTS / f'{slug}-{locale}-{theme}-{width}.png'), full_page=True)
            page.set_viewport_size({'width': 320, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (slug, '320px initial language')
            initial_title = page.locator('h1').inner_text()
            initial_meta = page.locator('meta[name="description"]').get_attribute('content')
            page.locator('#language').click()
            assert page.locator('h1').inner_text() != initial_title
            assert page.locator('meta[name="description"]').get_attribute('content') != initial_meta
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (slug, '320px switched language')
            page.set_viewport_size({'width': width, 'height': 900})
            other = 'en' if locale.startswith('pl') else 'pl'
            page.locator('#cv-preview').click()
            expect(page.locator('#cv-dialog')).to_be_visible()
            assert page.locator('#cv-frame').get_attribute('src').endswith(f'{other.upper()}.pdf')
            page.keyboard.press('Escape')
            expect(page.locator('#cv-dialog')).not_to_be_visible()
            page.locator('#language').click()
            for href in page.locator('.case-toc a').evaluate_all('(els) => els.map(el => el.getAttribute("href"))'):
                assert page.locator(href).count() == 1
            page.locator('.back-link').click()
            expect(page.locator('h1')).to_contain_text('Adam Bielas')
            print(f'PASS {slug} {locale} {theme} {width}px: route, content, translations, metadata, CV, navigation')
        # Language and theme choices survive journeys between pages.
        page.locator('#language').click()
        page.locator('#theme').click()
        page.locator('a[data-case-link]').first.click()
        expect(page.locator('html')).to_have_attribute('lang', 'en' if locale.startswith('pl') else 'pl')
        expect(page.locator('html')).to_have_attribute('data-theme', 'light' if theme == 'dark' else 'dark')
        assert not errors, errors
        assert not missing, missing
        context.close()
    context = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
    page = context.new_page()
    for slug in SLUGS:
        page.goto(f'{BASE}/projects/{slug}/', wait_until='networkidle')
        assert page.locator('.case-section').count() >= 5
        expect(page.locator('a[download]')).to_be_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    print('PASS all case studies without JavaScript: static content and CV download')
    context.close()
    browser.close()
