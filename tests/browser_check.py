"""Real-browser checks. Start a local HTTP server, then run this script."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = os.environ.get('PORTFOLIO_URL', 'http://127.0.0.1:8765').rstrip('/')
CHROME = os.environ.get('CHROME_PATH', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
SHOTS = Path(__file__).parent / 'screenshots'
SHOTS.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True)
    cases = [('pl-PL','light',1440),('en-US','dark',1440),('pl-PL','dark',390),('en-US','light',320),('de-DE','light',768)]
    for locale, theme, width in cases:
        context = browser.new_context(locale=locale, color_scheme=theme, viewport={'width':width,'height':950}, reduced_motion='reduce')
        page = context.new_page()
        errors = []
        failed = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.on('response', lambda response: failed.append(f'{response.status} {response.url}') if response.status >= 400 else None)
        page.goto(BASE, wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        language = 'pl' if locale.startswith('pl') else 'en'
        expect(page.locator('html')).to_have_attribute('lang', language)
        expect(page.locator('html')).to_have_attribute('data-theme', theme)
        expect(page.locator('h1')).to_contain_text('Adam Bielas')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow: {locale} {width}'
        assert page.evaluate('document.fonts.check("600 16px Manrope")'), 'Font not loaded'
        assert page.locator('[data-i18n]').evaluate_all('(els) => els.every(el => el.textContent.trim())')
        assert page.locator('#cv-download').get_attribute('href').endswith(f'{language.upper()}.pdf')
        page.screenshot(path=str(SHOTS / f'{locale}-{theme}-{width}.png'), full_page=True)
        for href in ['assets/CV_Adam_Bielas_PL.pdf','assets/CV_Adam_Bielas_EN.pdf','assets/favicon.svg','assets/fonts/manrope.ttf','app.js','style.css']:
            response = context.request.get(f'{BASE}/{href}')
            assert response.ok, href
            if href.endswith('.pdf'): assert response.body().startswith(b'%PDF')
        page.keyboard.press('Tab')
        expect(page.locator('.skip')).to_be_focused()
        page.locator('#language').click()
        other = 'en' if language == 'pl' else 'pl'
        expect(page.locator('html')).to_have_attribute('lang', other)
        page.locator('#theme').click()
        new_theme = 'dark' if theme == 'light' else 'light'
        page.reload(wait_until='networkidle')
        expect(page.locator('html')).to_have_attribute('lang', other)
        expect(page.locator('html')).to_have_attribute('data-theme', new_theme)
        page.locator('#cv-preview').click()
        expect(page.locator('#cv-dialog')).to_be_visible()
        assert page.locator('#cv-frame').get_attribute('src').endswith(f'{other.upper()}.pdf')
        page.keyboard.press('Escape')
        expect(page.locator('#cv-dialog')).not_to_be_visible()
        expect(page.locator('#cv-preview')).to_be_focused()
        assert page.locator('.email').get_attribute('href') == 'mailto:adam.bielas.praca@gmail.com'
        assert page.locator('a[href="https://www.linkedin.com/in/adambielas/"]').count() == 1
        assert page.locator('a[href="https://github.com/Rabuuwu"]').count() == 1
        assert not errors, errors
        assert not failed, failed
        print(f'PASS {locale} {theme} {width}px: layout, language, theme, persistence, CV, keyboard, resources')
        context.close()
    context = browser.new_context(locale='pl-PL', color_scheme='light')
    page = context.new_page()
    page.add_init_script('Object.defineProperty(window, "localStorage", {get(){throw new Error("storage unavailable")}})')
    page.goto(BASE, wait_until='networkidle')
    page.locator('#language').click()
    expect(page.locator('html')).to_have_attribute('lang','en')
    page.locator('#theme').click()
    expect(page.locator('html')).to_have_attribute('data-theme','dark')
    print('PASS restricted storage: language and theme still work')
    context.close()
    context = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
    page = context.new_page()
    page.goto(BASE, wait_until='networkidle')
    expect(page.locator('h1')).to_contain_text('Adam Bielas')
    expect(page.locator('noscript')).to_be_visible()
    print('PASS JavaScript disabled: content and CV links available')
    context.close()
    browser.close()
