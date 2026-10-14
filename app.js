'use strict';
(() => {
  document.documentElement.classList.add('js');
  const pageContent = JSON.parse(document.getElementById('page-translations')?.textContent || '{}');
  const en = Object.fromEntries([...document.querySelectorAll('[data-i18n]')].map(el => [el.dataset.i18n, el.innerHTML]));
  const translations = {
    en,
    pl: {
      skip: 'Przejdź do treści', work: 'Projekty', about: 'O mnie', contact: 'Kontakt', location: 'Tychy, Polska',
      headline: 'Od realnego problemu<br>do działającego systemu.',
      intro: 'Tworzę aplikacje webowe i mobilne, łączę systemy i wykorzystuję AI w praktyce. Od pierwszej rozmowy po wdrożenie i utrzymanie.',
      viewWork: 'Zobacz moje projekty', letsTalk: 'Porozmawiajmy ↗', interface: 'Interfejs', localLlm: 'Lokalny LLM',
      systemCaption: 'Różne elementy. Jeden działający system.', experienceShort: 'Rozwijam i utrzymuję oprogramowanie w NDI od 2023 roku.', scroll: 'Zobacz więcej ↓',
      workTitle: 'Oprogramowanie,<br>które robi różnicę.', workIntro: 'Wybrane realizacje komercyjne i projekty własne. Odpowiedzi na konkretne potrzeby.', commercial: 'Praca komercyjna / NDI',
      inventoryMetric: 'krótszy czas inwentaryzacji', inventoryTitle: 'Z papieru do połączonego magazynu.',
      inventoryBody: 'Moduł CRM z historią urządzeń, powiązaniami z adresami klientów i automatyczną dokumentacją. Zaprojektowałem model SQL, zbudowałem i wdrożyłem moduł. Nadal go utrzymuję.',
      callDocumentation: 'Dokumentowanie rozmowy', callSeconds: '~15 s', localModel: 'Lokalny model. Integracja z CRM.', aiTitle: 'Rozmowy zamienione w przydatne podsumowania.',
      aiBody: 'Połączyłem rozmowy, transkrypcje i podsumowania AI z CRM przez uwierzytelniane API i dostroiłem lokalny model LLM. Czas dokumentowania spadł z około 3 minut do 15 sekund.',
      personal: 'Projekt własny', dndBody: 'Postacie, kampanie, ekwipunek i notatki w jednym miejscu. Pomocnik do sesji RPG, aktywnie rozwijany.',
      tradingBody: 'Skaner rynku i panel PWA z symulacją transakcji PAPER. Narzędzie analityczne do badania pomysłów, bez składania zleceń u brokera.',
      aboutTitle: 'Łączę elementy.<br>I sprawiam, że działają.', aboutLead: 'Jestem programistą Full Stack z Tychów. Pracuję nad całym cyklem: wymaganiami, bazą danych, interfejsem, integracjami, wdrożeniem i utrzymaniem.',
      aboutBody: 'W NDI rozwijam produkcyjny CRM operatora internetowego. Doświadczenie w telekomunikacji pomaga mi rozumieć ludzi, urządzenia i procesy stojące za oprogramowaniem.',
      aboutMore: 'Poza modułami CRM wdrożyłem i utrzymuję integrację z KSeF. Zbudowałem też aplikację do zgłoszeń klientów w React Native / Expo, obecnie w wersji testowej.',
      build: 'Tworzę', connect: 'Łączę', present: 'obecnie', career: 'Rozwój oprogramowania od 2023; stanowisko programisty od 2025.',
      cvTitle: 'Więcej szczegółów w CV.', cvBody: 'Doświadczenie, technologie i wykształcenie. W wersji polskiej i angielskiej.', preview: 'Podgląd CV', download: 'Pobierz CV ↓',
      contactIntro: 'Masz projekt lub propozycję współpracy?', contactTitle: 'Stwórzmy razem<br>coś przydatnego.', contactLocation: 'Tychy, Polska. Angielski: C1.', backTop: 'Na początek ↑', close: 'Zamknij', openPdf: 'Otwórz PDF w nowej karcie'
    }
  };
  Object.entries(pageContent.strings || {}).forEach(([key, value]) => { translations.en[key] = value.en; translations.pl[key] = value.pl; });
  const aria = { en: { navigation: 'Main navigation', flow: 'System flow', systemAlt: 'Connected interface, API, CRM database and local AI modules' }, pl: { navigation: 'Nawigacja główna', flow: 'Przepływ systemu', systemAlt: 'Połączone moduły interfejsu, API, bazy CRM i lokalnego AI' } };
  function read(key) { try { return localStorage.getItem(key); } catch { return null; } }
  function save(key, value) { try { localStorage.setItem(key, value); } catch { /* Preferences still work without storage. */ } }
  let language = read('portfolio-language');
  if (!['pl', 'en'].includes(language)) language = (navigator.languages?.[0] || navigator.language || 'en').toLowerCase().startsWith('pl') ? 'pl' : 'en';
  const langButton = document.getElementById('language');
  const themeButton = document.getElementById('theme');
  const frame = document.getElementById('cv-frame');
  const dialog = document.getElementById('cv-dialog');
  const pdf = () => `${document.body.dataset.assets || 'assets/'}CV_Adam_Bielas_${language.toUpperCase()}.pdf`;
  function updateThemeButton() {
    const dark = document.documentElement.dataset.theme === 'dark';
    themeButton.setAttribute('aria-label', language === 'pl' ? `Włącz ${dark ? 'jasny' : 'ciemny'} motyw` : `Switch to ${dark ? 'light' : 'dark'} mode`);
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.innerHTML = dark ? '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5" stroke="currentColor" stroke-width="1.7"/></svg>' : '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.4 14A8.6 8.6 0 0 1 10 3.6 8.6 8.6 0 1 0 20.4 14Z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>';
    document.querySelector('meta[name="theme-color"]').content = dark ? '#101a30' : '#F5F7FC';
  }
  function renderLanguage() {
    document.documentElement.lang = language;
    document.querySelectorAll('[data-i18n]').forEach(el => { el.innerHTML = translations[language][el.dataset.i18n] ?? en[el.dataset.i18n]; });
    document.querySelectorAll('[data-i18n-alt]').forEach(el => el.alt = translations[language][el.dataset.i18nAlt] || translations.en[el.dataset.i18nAlt]);
    document.querySelectorAll('[data-i18n-aria]').forEach(el => el.setAttribute('aria-label', aria[language][el.dataset.i18nAria]));
    langButton.textContent = language === 'pl' ? 'EN' : 'PL';
    langButton.setAttribute('aria-label', language === 'pl' ? 'Zmień język na angielski' : 'Change language to Polish');
    document.getElementById('cv-download').href = pdf();
    document.getElementById('cv-open').href = pdf();
    frame.title = language === 'pl' ? 'CV Adama Bielasa' : 'Adam Bielas CV';
    if (dialog.open) frame.src = pdf();
    const meta = pageContent.meta?.[language];
    if (meta) {
      document.title = meta.title;
      document.querySelector('meta[name="description"]').content = meta.description;
      document.querySelector('meta[property="og:title"]').content = meta.title;
      document.querySelector('meta[property="og:description"]').content = meta.description;
    }
    updateThemeButton();
  }
  langButton.addEventListener('click', () => { language = language === 'pl' ? 'en' : 'pl'; save('portfolio-language', language); renderLanguage(); });
  themeButton.addEventListener('click', () => { const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = theme; save('portfolio-theme', theme); updateThemeButton(); });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => { if (!['light', 'dark'].includes(read('portfolio-theme'))) { document.documentElement.dataset.theme = event.matches ? 'dark' : 'light'; updateThemeButton(); } });
  document.getElementById('cv-preview').addEventListener('click', () => { frame.src = pdf(); dialog.showModal(); });
  document.getElementById('cv-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { const box = dialog.getBoundingClientRect(); if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close(); });
  const menuButton = document.getElementById('menu-toggle');
  const siteNav = document.getElementById('site-nav');
  function setMenu(open) {
    menuButton.setAttribute('aria-expanded', String(open));
    document.querySelector('.header').dataset.menuOpen = String(open);
  }
  menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
  siteNav.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenu(false); menuButton.focus();
    }
  });
  document.getElementById('year').textContent = new Date().getFullYear();
  renderLanguage();
})();
