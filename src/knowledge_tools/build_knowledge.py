from pathlib import Path
from bs4 import BeautifulSoup
import json, re, sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('knowledge.py')
RESUME = Path(sys.argv[3]) if len(sys.argv) > 3 else Path('resume_facts.json')
PAGES = [('about','index.html'),('experience','experience.html'),('projects','projects.html'),('project-dow','projects/dow/index.html'),('project-zeiss','projects/zeiss/index.html'),('project-bosch','projects/bosch/index.html'),('project-amazon','projects/amazon/index.html'),('project-ask-venkat','projects/ask-venkat/index.html')]

def clean(s):
    s=re.sub(r'\s+',' ',s).strip().replace('← Back to projects','').replace('Explore the project in detail →','')
    return re.sub(r'\s+',' ',s).strip()

def split_text(text,max_chars=1500):
    sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])',text); out=[]; cur=''
    for sent in sentences:
        if cur and len(cur)+1+len(sent)>max_chars: out.append(cur.strip()); cur=sent
        else: cur=(cur+' '+sent).strip()
    if cur: out.append(cur.strip())
    return out

chunks=json.loads(RESUME.read_text(encoding='utf-8'))
for slug, rel in PAGES:
    soup=BeautifulSoup((ROOT/rel).read_text(encoding='utf-8',errors='ignore'),'html.parser')
    main=soup.find('main') or soup.body
    for bad in main.find_all(['script','style','nav','footer']): bad.decompose()
    for si, sec in enumerate(main.find_all('section',recursive=True),1):
        if set(sec.get('class') or []) & {'next','cta','project-cta'}: continue
        text=clean(sec.get_text(' ',strip=True))
        if len(text)<80: continue
        for pi, part in enumerate(split_text(text),1):
            chunks.append({'id':f'{slug}-{si:02d}-{pi:02d}','section':slug,'text':f"Portfolio context — {slug.replace('-', ' ')}. {part}"})

with OUT.open('w',encoding='utf-8') as f:
    f.write('KNOWLEDGE_CHUNKS = [\n')
    for c in chunks:
        f.write('    '+repr(c)+',\n')
    f.write(']\n')
print(f'Wrote {len(chunks)} chunks to {OUT}')
