"""Dependency-free checks of published artifacts and reproducible static generation."""
import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('portfolio_builder', ROOT / 'scripts/build_portfolio.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.i18n = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('a', 'link', 'img', 'script'):
            self.links.extend(attrs[k] for k in ('href', 'src') if attrs.get(k))
        if attrs.get('data-i18n'):
            self.i18n.append(attrs['data-i18n'])


class GeneratedSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = [ROOT / 'index.html', *sorted((ROOT / 'projects').glob('*/index.html'))]

    def test_all_cases_are_published(self):
        self.assertEqual(len(self.pages), 1 + len(builder.DATA['cases']))
        for case in builder.DATA['cases']:
            self.assertTrue((ROOT / 'projects' / case['slug'] / 'index.html').is_file())

    def test_unique_ids(self):
        for page in self.pages:
            ids = Document(page.read_text()).ids
            self.assertEqual(len(ids), len(set(ids)), str(page))

    def test_internal_navigation_and_assets_resolve(self):
        for page in self.pages:
            for link in Document(page.read_text()).links:
                if ':' in link or link.startswith('//'):
                    continue
                path, _, fragment = link.partition('#')
                target = page.parent / path if path else page
                if target.is_dir():
                    target /= 'index.html'
                self.assertTrue(target.exists(), (page, link))
                if fragment and target.suffix == '.html':
                    self.assertIn(fragment, Document(target.read_text()).ids, (page, link))

    def test_bilingual_payload_is_valid_and_complete(self):
        for page in self.pages:
            text = page.read_text()
            payload = text.split('<script type="application/json" id="page-translations">')[1].split('</script>')[0]
            data = json.loads(payload)
            for key, pair in data['strings'].items():
                self.assertEqual(set(pair), {'en', 'pl'}, (page, key))
                self.assertTrue(all(pair.values()), (page, key))
            for lang in ('pl', 'en'):
                self.assertTrue(data['meta'][lang]['description'])

    def test_engineering_and_ai_sections_present(self):
        doc = Document((ROOT / 'index.html').read_text())
        for section in ('engineering', 'aiAutomation', 'experience', 'contact'):
            self.assertIn(section, doc.ids)

    def test_unmeasured_business_metrics_not_presented(self):
        for page in self.pages:
            text = page.read_text()
            for claim in ('90%', '~15 s', '~3 min'):
                self.assertNotIn(claim, text, str(page))

    def test_experience_distinguishes_it_from_developer_role(self):
        text = (ROOT / 'index.html').read_text()
        self.assertIn('Software Developer role since 2025', text)
        self.assertIn('Telecommunications installer', text)

    def test_generator_reproduces_committed_artifacts(self):
        original = builder.ROOT
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'templates').mkdir()
            (root / 'templates/home.html').write_text((ROOT / 'templates/home.html').read_text())
            try:
                builder.ROOT = root
                builder.build_home()
                for case in builder.DATA['cases']:
                    builder.build_case(case)
                for page in self.pages:
                    self.assertEqual(page.read_bytes(), (root / page.relative_to(ROOT)).read_bytes(), str(page))
            finally:
                builder.ROOT = original


if __name__ == '__main__':
    unittest.main()
