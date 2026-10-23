#!/usr/bin/env python3
"""Check that existing artifact tests reject faults, using disposable copies only."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(root, target=None):
    command = [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_generated_site.py', '-v']
    if target:
        command.extend(['-k', target])
    return subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=30)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='portfolio-regression-') as directory:
        root = Path(directory)
        for name in ('assets', 'content', 'templates', 'scripts', 'tests', 'projects'):
            shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('index.html', 'app.js', 'style.css'):
            shutil.copy2(ROOT / name, root / name)
        baseline = run(root)
        if baseline.returncode:
            sys.stderr.write(baseline.stdout + baseline.stderr)
            return 1
        page = root / 'index.html'
        original = page.read_text()
        mutations = [
            ('engineering section removed', 'test_engineering_and_ai_sections_present', original.replace('id="engineering"', 'id="removed-engineering"')),
            ('duplicate document id', 'test_unique_ids', original.replace('</main>', '<div id="main"></div></main>')),
            ('broken local navigation', 'test_internal_navigation_and_assets_resolve', original.replace('</main>', '<a href="missing-page.html">Missing</a></main>')),
            ('unverified numeric claim', 'test_unmeasured_business_metrics_not_presented', original.replace('</main>', '<p>90%</p></main>')),
            ('ambiguous experience', 'test_experience_distinguishes_it_from_developer_role', original.replace('Software Developer role since 2025', 'Software Developer for three years')),
        ]
        for label, target, content in mutations:
            if content == original:
                raise RuntimeError(f'Mutation did not apply: {label}')
            page.write_text(content)
            result = run(root, target)
            detected = result.returncode == 1 and f'FAIL: {target}' in result.stderr
            outcomes.append({'mutation': label, 'test': target, 'detected': detected, 'exit_code': result.returncode})
            page.write_text(original)
        content = root / 'content/portfolio.json'
        data = json.loads(content.read_text())
        data['home']['intro']['en'] += ' Deliberate source drift.'
        content.write_text(json.dumps(data))
        target = 'test_generator_reproduces_committed_artifacts'
        result = run(root, target)
        outcomes.append({'mutation': 'source changed without regeneration', 'test': target,
                         'detected': result.returncode == 1 and f'FAIL: {target}' in result.stderr,
                         'exit_code': result.returncode})
    report = {'control_tests_passed': True, 'mutations': outcomes,
              'all_detected': all(row['detected'] for row in outcomes)}
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['all_detected'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
