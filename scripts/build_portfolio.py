#!/usr/bin/env python3
"""Build committed static HTML from reviewed bilingual content. No dependencies."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/portfolio.json').read_text())
SITE_URL = 'https://rabuuwu.github.io'
COMMON = {
 'skip': {'en':'Skip to content','pl':'Przejdź do treści'},
 'work': {'en':'Projects','pl':'Projekty'},
 'experienceNav': {'en':'Experience','pl':'Doświadczenie'},
 'competenciesNav': {'en':'Skills','pl':'Kompetencje'},
 'contact': {'en':'Contact','pl':'Kontakt'},
 'menu': {'en':'Menu','pl':'Menu'},
 'readCase': {'en':'Read case study','pl':'Zobacz case study'},
 'preview': {'en':'Preview CV','pl':'Podgląd CV'},
 'download': {'en':'Download CV ↓','pl':'Pobierz CV ↓'},
 'close': {'en':'Close','pl':'Zamknij'},
 'openPdf': {'en':'Open PDF in a new tab','pl':'Otwórz PDF w nowej karcie'},
 'cvTitle': {'en':'Experience and education in my CV.','pl':'Doświadczenie i wykształcenie w CV.'},
 'back': {'en':'Back to portfolio','pl':'Wróć do portfolio'},
 'contents': {'en':'In this case study','pl':'W tym case study'},
 'source': {'en':'Source repository','pl':'Repozytorium projektu'},
 'pwa': {'en':'Open the PWA','pl':'Otwórz PWA'},
 'next': {'en':'Explore my other projects','pl':'Zobacz pozostałe projekty'},
 'caseCv': {'en':'My professional background','pl':'Moje doświadczenie zawodowe'},
 'caseContact': {'en':'Discuss a project or integration','pl':'Porozmawiajmy o projekcie lub integracji'},
}

class Page:
 def __init__(self, language='en'):
  self.strings = dict(COMMON)
  self.language = language
 def add(self, pair, key):
  assert set(pair) == {'en','pl'}, key
  self.strings[key] = pair
  return pair[self.language]
 def tag(self, tag, pair, key, attrs=''):
  self.add(pair,key)
  return f'<{tag} data-i18n="{key}"{attrs}>{pair[self.language]}</{tag}>'
 def payload(self, meta):
  payload = {'strings':self.strings,'meta':meta}
  raw = json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')
  return f'<script type="application/json" id="page-translations">{raw}</script>'

THEME_SCRIPT = "document.documentElement.classList.add('js');try{const t=localStorage.getItem('portfolio-theme');document.documentElement.dataset.theme=t==='light'||t==='dark'?t:matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}catch{document.documentElement.dataset.theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}"

def header(prefix='', language='en', language_url='pl/'):
 labels = {key: value[language] for key, value in COMMON.items()}
 target_language = 'PL' if language == 'en' else 'EN'
 target_locale = 'pl' if language == 'en' else 'en'
 return f'''<header class="header wrap">
 <a class="wordmark" href="{prefix}#main" aria-label="Adam Bielas">ab<span>.</span></a>
 <button id="menu-toggle" aria-expanded="false" aria-controls="site-nav" type="button" data-i18n="menu">{labels['menu']}</button>
 <nav id="site-nav" aria-label="{'Main navigation' if language == 'en' else 'Nawigacja główna'}" data-i18n-aria="navigation">
 <a href="{prefix}#work" data-i18n="work">{labels['work']}</a><a href="{prefix}#experience" data-i18n="experienceNav">{labels['experienceNav']}</a><a href="{prefix}#competencies" data-i18n="competenciesNav">{labels['competenciesNav']}</a><a href="{prefix}#contact" data-i18n="contact">{labels['contact']}</a>
 </nav><div class="preferences"><a id="language" href="{language_url}" lang="{target_locale}" hreflang="{target_locale}" aria-label="{'Zmień język na polski' if language == 'en' else 'Change language to English'}">{target_language}</a><button id="theme" type="button" aria-label="{'Switch to dark mode' if language == 'en' else 'Włącz ciemny motyw'}"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.4 14A8.6 8.6 0 0 1 10 3.6 8.6 8.6 0 1 0 20.4 14Z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg></button></div>
 </header>'''

def cv_dialog(prefix='', language='en'):
 return f'''<dialog id="cv-dialog" aria-labelledby="dialog-title"><div class="dialog-head"><h2 id="dialog-title" data-i18n="cvTitle">{COMMON['cvTitle'][language]}</h2><button id="cv-close" type="button" data-i18n="close">{COMMON['close'][language]}</button></div><iframe id="cv-frame" title="{'Adam Bielas CV' if language == 'en' else 'CV Adama Bielasa'}"></iframe><p><a id="cv-open" href="{prefix}CV_Adam_Bielas_{language.upper()}.pdf" target="_blank" rel="noopener noreferrer" data-i18n="openPdf">{COMMON['openPdf'][language]}</a></p></dialog>'''

def alternate_links(en_url, pl_url):
 return (f'<link rel="alternate" hreflang="en" href="{en_url}">'
         f'<link rel="alternate" hreflang="pl" href="{pl_url}">'
         f'<link rel="alternate" hreflang="x-default" href="{en_url}">')

def json_ld(data):
 raw = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')
 return f'<script type="application/ld+json">{raw}</script>'

def build_seo_files():
 urls = [SITE_URL + '/', SITE_URL + '/pl/']
 for case in DATA['cases']:
  urls.extend([SITE_URL + '/projects/' + case['slug'] + '/', SITE_URL + '/pl/projects/' + case['slug'] + '/'])
 entries = ''.join(f'<url><loc>{html.escape(url)}</loc></url>' for url in urls)
 (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + entries + '</urlset>\n')

def build_home(language='en'):
 p = Page(language);p.strings.update(DATA['home'])
 doc = (ROOT/'templates/home.html').read_text()
 for key, pair in p.strings.items():
  # These values are authored HTML, not external inputs. All default content remains static.
  pattern = rf'(<[a-z0-9]+\b[^>]*\bdata-i18n="{re.escape(key)}"[^>]*>)(.*?)(</[a-z0-9]+>)'
  doc = re.sub(pattern,lambda m: m[1]+pair[language]+m[3],doc,flags=re.S)
 home_url = SITE_URL + ('/pl/' if language == 'pl' else '/')
 lang_url = '../' if language == 'pl' else 'pl/'
 doc = re.sub(r'<header\b.*?</header>',header('',language,lang_url),doc,flags=re.S)
 # Six direct case-study links, retaining the existing two commercial visuals.
 for classname, slug in [('inventory','crm-inventory'),('ai-case','ai-call-summaries')]:
  pattern=rf'(<article class="case {classname}">.*?)(</article>)'
  link=f'<a class="case-read text-link" data-case-link href="projects/{slug}/" data-i18n="readCase">{COMMON["readCase"][language]}</a>'
  doc=re.sub(pattern,lambda m:m[1]+link+m[2],doc,flags=re.S)
 small=[]
 for slug,key in [('ksef','ksef'),('customer-app','mobile')]:
  item=next(c for c in DATA['cases'] if c['slug']==slug)
  title=p.tag('h3',DATA['home'][key+'ShortTitle'],key+'ShortTitle')
  body=p.tag('p',DATA['home'][key+'ShortBody'],key+'ShortBody')
  status=p.tag('p',item['status'],key+'ShortStatus',' class="case-type"')
  small.append(f'<article class="compact-case">{status}{title}{body}<a class="text-link" data-case-link href="projects/{slug}/" data-i18n="readCase">{COMMON["readCase"][language]}</a></article>')
 doc=doc.replace('<div class="personal-projects">','<div class="compact-cases">'+''.join(small)+'</div><div class="personal-projects">')
 for name,slug in [('DnDCompanion','dnd-companion'),('TradingHelper','trading-helper')]:
  old=rf'<a href="https://github.com/Rabuuwu/{name}"[^>]*class="project-link"[^>]*>.*?</a>'
  replacement=f'<a href="projects/{slug}/" class="project-link" data-case-link data-i18n="readCase">{COMMON["readCase"][language]}</a>'
  doc=re.sub(old,replacement,doc,flags=re.S)
 experiment=p.tag('h3',DATA['home']['fsTitle'],'fsTitle')+p.tag('p',DATA['home']['fsBody'],'fsBody')
 fs=f'<aside class="experiment">{experiment}<a class="text-link" href="https://github.com/Rabuuwu/FSE-IT" target="_blank" rel="noopener noreferrer">GitHub</a></aside>'
 doc=doc.replace('</div></section>\n<section class="about-section',fs+'</div></section>\n<section class="about-section',1)
 # Replace the old technology-only lists and one-line timeline with a full dedicated section.
 doc=re.sub(r'<div class="skills">.*?</div></div></section>', '</div></section>',doc,flags=re.S,count=1)
 timeline=''
 for i,row in enumerate(DATA['timeline']):
  timeline += '<article class="career-entry">'+p.tag('p',row['date'],f'careerDate{i}',' class="career-date"')+'<div>'+p.tag('h3',row['title'],f'careerTitle{i}')+p.tag('p',row['body'],f'careerBody{i}')+'</div></article>'
 experience='<section class="experience-section wrap" id="experience" aria-labelledby="experience-title">'+p.tag('h2',DATA['home']['experienceTitle'],'experienceTitle',' id="experience-title"')+p.tag('p',DATA['home']['experienceIntro'],'experienceIntro',' class="section-intro"')+'<div class="career-list">'+timeline+'</div></section>'
 skills=''
 for i,(title,body) in enumerate(DATA['competencies']):
  skills+='<article class="competence-item">'+p.tag('h3',title,f'skillTitle{i}')+p.tag('p',body,f'skillBody{i}')+'</article>'
 competencies='<section class="competencies-section" id="competencies" aria-labelledby="competencies-title"><div class="wrap">'+p.tag('h2',DATA['home']['competenciesTitle'],'competenciesTitle',' id="competencies-title"')+p.tag('p',DATA['home']['competenciesIntro'],'competenciesIntro',' class="section-intro"')+'<div class="competence-grid">'+skills+'</div></div></section>'
 steps=''
 for i,(title,body) in enumerate(DATA['steps']):
  steps+='<li class="work-step">'+p.tag('h3',title,f'stepTitle{i}')+p.tag('p',body,f'stepBody{i}')+'</li>'
 approach='<section class="approach-section wrap" id="approach" aria-labelledby="approach-title">'+p.tag('h2',DATA['home']['approachTitle'],'approachTitle',' id="approach-title"')+p.tag('p',DATA['home']['approachIntro'],'approachIntro',' class="section-intro"')+'<ol class="work-steps">'+steps+'</ol></section>'
 personal='<section class="personal-section wrap">'+p.tag('h2',DATA['home']['personalTitle'],'personalTitle')+p.tag('p',DATA['home']['personalBody'],'personalBody')+'</section>'
 doc=doc.replace('<section class="cv-section',experience+competencies+approach+personal+'<section class="cv-section',1)
 # Reuse the existing typography and grid; these sections distinguish evidence from claims.
 for field, heading in [('engineering', {'en':'Engineering practice','pl':'Praktyka inżynierska'}), ('aiAutomation', {'en':'AI and automation','pl':'AI i automatyzacja'})]:
  cards=''.join('<article class="engineering-item">'+p.tag('h3',title,f'{field}Title{i}')+p.tag('p',body,f'{field}Body{i}')+'</article>' for i,(title,body) in enumerate(DATA[field]))
  section=f'<section class="competencies-section" id="{field}" aria-labelledby="{field}-title"><div class="wrap">'+p.tag('h2',heading,f'{field}Heading',f' id="{field}-title"')+'<div class="competence-grid">'+cards+'</div></div></section>'
  doc=doc.replace('<section class="cv-section',section+'<section class="cv-section',1)
 offer='<div class="offer">'+p.tag('h3',DATA['home']['offerTitle'],'offerTitle')+p.tag('p',DATA['home']['offerBody'],'offerBody')+'</div>'
 doc=doc.replace('<a class="email"',offer+'<a class="email"',1)
 doc=re.sub(r'<dialog\b.*?</dialog>',cv_dialog('../assets/' if language == 'pl' else 'assets/',language),doc,flags=re.S)
 meta={'en':{'title':'Adam Bielas — Full Stack Developer','description':'Adam Bielas: CRM development, API integrations, web and mobile applications, local AI and telecommunications. Experience and detailed case studies.'},'pl':{'title':'Adam Bielas — Programista Full Stack','description':'Adam Bielas: rozwój CRM, integracje API, aplikacje webowe i mobilne, lokalne AI oraz telekomunikacja. Doświadczenie i szczegółowe case studies.'}}
 doc=re.sub(r'(<meta name="description" content=")[^"]*(">)',lambda m:m[1]+html.escape(meta[language]['description'],quote=True)+m[2],doc)
 doc=re.sub(r'(<meta property="og:description" content=")[^"]*(">)',lambda m:m[1]+html.escape(meta[language]['description'],quote=True)+m[2],doc)
 doc=re.sub(r'(<meta property="og:title" content=")[^"]*(">)',lambda m:m[1]+html.escape(meta[language]['title'],quote=True)+m[2],doc)
 doc=re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)',lambda m:m[1]+html.escape(meta[language]['title'],quote=True)+m[2],doc)
 doc=re.sub(r'(<meta name="twitter:description" content=")[^"]*(">)',lambda m:m[1]+html.escape(meta[language]['description'],quote=True)+m[2],doc)
 doc=re.sub(r'(<title>)[^<]*(</title>)',lambda m:m[1]+html.escape(meta[language]['title'])+m[2],doc)
 doc=re.sub(r'(<link rel="canonical" href=")[^"]*(">)',lambda m:m[1]+home_url+m[2],doc)
 doc=re.sub(r'(<meta property="og:url" content=")[^"]*(">)',lambda m:m[1]+home_url+m[2],doc)
 doc=doc.replace('<head>','<head>'+alternate_links(SITE_URL+'/',SITE_URL+'/pl/'),1)
 doc=doc.replace('<html lang="en">',f'<html lang="{language}">',1)
 locale='pl_PL' if language == 'pl' else 'en_US'
 alternate_locale='en_US' if language == 'pl' else 'pl_PL'
 og_meta=(f'<meta property="og:image" content="{SITE_URL}/assets/social.png">'
          '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
          f'<meta property="og:image:alt" content="Adam Bielas — Full Stack Developer"><meta property="og:locale" content="{locale}"><meta property="og:locale:alternate" content="{alternate_locale}">')
 doc=doc.replace('<meta property="og:image" content="https://rabuuwu.github.io/assets/social.png">',og_meta,1)
 doc=doc.replace('<body>',f'<body data-assets="{"../" if language == "pl" else ""}assets/">')
 if language == 'pl':
  doc=doc.replace('href="style.css"','href="../style.css"').replace('src="app.js"','src="../app.js"')
  doc=doc.replace('href="assets/','href="../assets/').replace('src="assets/','src="../assets/')
 website_id=SITE_URL+'/#website'
 person={'@type':'Person','@id':SITE_URL+'/#adam-bielas','name':'Adam Bielas','url':SITE_URL+'/','jobTitle':'Full Stack Developer','address':{'@type':'PostalAddress','addressLocality':'Tychy','addressCountry':'PL'},'sameAs':['https://github.com/Rabuuwu','https://www.linkedin.com/in/adambielas/']}
 structured={'@context':'https://schema.org','@graph':[person,{'@type':'WebSite','@id':website_id,'url':SITE_URL+'/','name':'Adam Bielas — Full Stack Developer','inLanguage':language}, {'@type':'WebPage','@id':home_url+'#webpage','url':home_url,'name':meta[language]['title'],'description':meta[language]['description'],'inLanguage':language,'isPartOf':{'@id':website_id},'about':{'@id':SITE_URL+'/#adam-bielas'}}]}
 doc=doc.replace('</head>',json_ld(structured)+'</head>',1)
 doc=doc.replace('</body>',p.payload(meta)+'\n</body>')
 dest=ROOT/('pl/index.html' if language == 'pl' else 'index.html')
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(doc)

def build_case(c, language='en'):
 p=Page(language)
 prefix='../../../' if language == 'pl' else '../../'
 home_prefix=prefix+('pl/' if language == 'pl' else '')
 route='/pl/projects/' if language == 'pl' else '/projects/'
 url=SITE_URL+route+c['slug']+'/'
 en_url=SITE_URL+'/projects/'+c['slug']+'/'
 pl_url=SITE_URL+'/pl/projects/'+c['slug']+'/'
 meta={lang:{'title':c['title'][lang]+' | Adam Bielas','description':c['summary'][lang]} for lang in ['en','pl']}
 sections='';toc=''
 for i,s in enumerate(c['sections']):
  title=p.add(s['title'],f'sectionTitle{i}')
  toc+=f'<li><a href="#{s["id"]}" data-i18n="sectionTitle{i}">{title}</a></li>'
  paragraphs=''.join(p.tag('p',pair,f'paragraph{i}-{j}') for j,pair in enumerate(s['paragraphs']))
  bullets=''.join(p.tag('li',pair,f'bullet{i}-{j}') for j,pair in enumerate(s['bullets']))
  sections+=f'<section class="case-section" id="{s["id"]}"><h2 data-i18n="sectionTitle{i}">{title}</h2>{paragraphs}'+(f'<ul>{bullets}</ul>' if bullets else '')+'</section>'
 diagram=''
 if c['diagram']:
  diagram='<ol class="architecture-flow" aria-label="System flow" data-i18n-aria="flow">'+''.join(p.tag('li',pair,f'flow{i}') for i,pair in enumerate(c['diagram']))+'</ol>'
 figure=''
 if c['screenshot']:
  shot=c['screenshot'];p.add(shot['alt'],'screenshotAlt');caption=p.tag('figcaption',shot['caption'],'screenshotCaption')
  figure=f'<figure class="case-screenshot {"phone-shot" if c["slug"]=="dnd-companion" else ""}"><img src="{prefix}assets/projects/{shot["file"]}" alt="{html.escape(shot["alt"][language],quote=True)}" data-i18n-alt="screenshotAlt" loading="lazy" width="{390 if c["slug"]=="dnd-companion" else 1440}" height="{844 if c["slug"]=="dnd-companion" else 1000}">{caption}</figure>'
 links=''
 if c['repo']:links+=f'<a class="button secondary" href="{c["repo"]}" target="_blank" rel="noopener noreferrer" data-i18n="source">{COMMON["source"][language]}</a>'
 if c['slug']=='dnd-companion':links+='<a class="text-link" href="https://rabuuwu.github.io/DnDCompanion/" target="_blank" rel="noopener noreferrer" data-i18n="pwa">'+COMMON['pwa'][language]+'</a>'
 title=p.tag('h1',c['title'],'caseTitle');summary=p.tag('p',c['summary'],'caseSummary',' class="case-lead"')
 kind=p.tag('p',c['kind'],'caseKind',' class="case-kind"');status=p.tag('p',c['status'],'caseStatus',' class="status-label"')
 tags='<ul class="tags">'+''.join('<li>'+html.escape(tech)+'</li>' for tech in c['tech'])+'</ul>'
 doc=f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="theme-color" content="#F5F7FC">
<title>{html.escape(meta[language]['title'])}</title><meta name="description" content="{html.escape(meta[language]['description'],quote=True)}"><meta property="og:title" content="{html.escape(meta[language]['title'],quote=True)}"><meta property="og:description" content="{html.escape(meta[language]['description'],quote=True)}"><meta property="og:type" content="article"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}/assets/social.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Adam Bielas — Full Stack Developer"><meta property="og:locale" content="{'pl_PL' if language == 'pl' else 'en_US'}"><meta property="og:locale:alternate" content="{'en_US' if language == 'pl' else 'pl_PL'}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(meta[language]['title'],quote=True)}"><meta name="twitter:description" content="{html.escape(meta[language]['description'],quote=True)}"><meta name="twitter:image" content="{SITE_URL}/assets/social.png"><link rel="canonical" href="{url}">{alternate_links(en_url,pl_url)}<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}style.css"><script>{THEME_SCRIPT}</script><script src="{prefix}app.js" defer></script></head>
<body class="case-page" data-assets="{prefix}assets/"><a class="skip" href="#main" data-i18n="skip">{'Przejdź do treści' if language == 'pl' else 'Skip to content'}</a>{header(home_prefix,language,('../../../projects/'+c['slug']+'/' if language == 'pl' else '../../pl/projects/'+c['slug']+'/'))}
<main id="main"><div class="case-hero wrap"><a class="back-link text-link" href="{home_prefix}#work" data-i18n="back">{COMMON['back'][language]}</a><div class="case-status-row">{kind}{status}</div>{title}{summary}{tags}<div class="actions">{links}</div>{diagram}</div>
<div class="case-layout wrap"><aside class="case-toc"><h2 data-i18n="contents">{COMMON['contents'][language]}</h2><ol>{toc}</ol></aside><article class="case-article">{figure}{sections}</article></div>
<section class="case-next wrap"><h2 data-i18n="next">{COMMON['next'][language]}</h2><div class="actions"><a class="button secondary" href="{home_prefix}#work" data-i18n="back">{COMMON['back'][language]}</a><a class="text-link" href="mailto:adam.bielas.praca@gmail.com" data-i18n="caseContact">{COMMON['caseContact'][language]}</a></div></section>
<section class="case-cv wrap"><h2 data-i18n="caseCv">{COMMON['caseCv'][language]}</h2><div class="actions"><button class="button secondary" id="cv-preview" type="button" data-i18n="preview">{COMMON['preview'][language]}</button><a class="button primary" id="cv-download" href="{prefix}assets/CV_Adam_Bielas_{language.upper()}.pdf" download data-i18n="download">{COMMON['download'][language]}</a></div></section></main>
<footer class="wrap"><p>© <span id="year">2026</span> Adam Bielas</p><a href="{home_prefix}#main" data-i18n="back">{COMMON['back'][language]}</a></footer>{cv_dialog(prefix+'assets/',language)}
<noscript><div class="noscript">{'Treść strony jest dostępna bez JavaScriptu.' if language == 'pl' else 'This page is available without JavaScript.'}</div></noscript>{p.payload(meta)}
</body></html>'''
 person={'@type':'Person','@id':SITE_URL+'/#adam-bielas','name':'Adam Bielas','url':SITE_URL+'/' ,'jobTitle':'Full Stack Developer','sameAs':['https://github.com/Rabuuwu','https://www.linkedin.com/in/adambielas/']}
 article={'@context':'https://schema.org','@type':'Article','headline':meta[language]['title'],'description':meta[language]['description'],'inLanguage':language,'mainEntityOfPage':url,'author':person,'image':SITE_URL+'/assets/social.png'}
 doc=doc.replace('</head>',json_ld(article)+'</head>',1)
 dest=ROOT/('pl/projects/' if language == 'pl' else 'projects/')/c['slug'];dest.mkdir(parents=True,exist_ok=True);(dest/'index.html').write_text(doc)

if __name__=='__main__':
 for language in ('en','pl'):
  build_home(language)
  for c in DATA['cases']:build_case(c,language)
 build_seo_files()
 print('Built bilingual homepage and',len(DATA['cases'])*2,'static case-study pages plus sitemap')
