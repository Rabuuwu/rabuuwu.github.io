"""Real-browser mobile and accessibility smoke checks; not a WCAG certification."""
import os
from pathlib import Path
import re
from playwright.sync_api import sync_playwright, expect

BASE = os.environ.get('PORTFOLIO_URL', 'http://127.0.0.1:8765').rstrip('/')
CHROME = os.environ.get('CHROME_PATH')
ROOT = Path(__file__).resolve().parents[1]
ROUTES = ['/', *[f'/projects/{p.parent.name}/' for p in sorted((ROOT / 'projects').glob('*/index.html'))]]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME or None, headless=True)
    try:
        for locale in ('pl-PL', 'en-US'):
            for theme in ('light', 'dark'):
                for width in (320, 1440):
                    context = browser.new_context(locale=locale, color_scheme=theme,
                                                  viewport={'width': width, 'height': 900},
                                                  reduced_motion='reduce')
                    try:
                        page = context.new_page()
                        errors = []
                        page.on('pageerror', lambda error: errors.append(str(error)))
                        for route in ROUTES:
                            response = page.goto(BASE + route, wait_until='networkidle')
                            assert response and response.ok, (route, 'HTTP response')
                            expect(page.locator('html')).to_have_attribute('lang', locale[:2])
                            expect(page.locator('html')).to_have_attribute('data-theme', theme)
                            expect(page.locator('main')).to_have_count(1)
                            expect(page.locator('h1')).to_have_count(1)
                            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), (route, width)
                            for button in page.locator('button:visible').all():
                                expect(button).to_have_accessible_name(re.compile(r'\S'))
                            assert page.locator('img').evaluate_all('(images) => images.every(img => img.hasAttribute("alt"))')
                            assert page.locator('iframe').evaluate_all('(frames) => frames.every(frame => !!frame.title.trim())')
                            missing = page.locator('[aria-labelledby], [aria-controls]').evaluate_all('''elements => elements.flatMap(el =>
                                [el.getAttribute('aria-labelledby'), el.getAttribute('aria-controls')]
                                .filter(Boolean).flatMap(value => value.split(/\\s+/))
                                .filter(id => !document.getElementById(id)))''')
                            assert not missing, (route, missing)
                            page.keyboard.press('Tab')
                            expect(page.locator('.skip')).to_be_focused()
                            page.keyboard.press('Enter')
                            assert page.url.endswith('#main'), route
                            if route == '/':
                                for anchor in ('engineering', 'aiAutomation'):
                                    expect(page.locator(f'#{anchor} h2')).to_be_visible()
                                    assert page.locator(f'#{anchor} .engineering-item').count() >= 2
                            assert not errors, errors
                            print(f'PASS accessibility smoke {route} {locale} {theme} {width}px')
                    finally:
                        context.close()
    finally:
        browser.close()
