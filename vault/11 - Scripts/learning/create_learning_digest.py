#!/usr/bin/env python3
from __future__ import annotations

import json, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

RUN_DIR = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else max(
    [p for p in (Path.home()/"SecurityResearch/01 - Learning/Inbox").iterdir() if (p/"learning-candidates.jsonl").exists()],
    key=lambda p: p.stat().st_mtime,
)
ROOT = Path.home()/"SecurityResearch"
RUN_LABEL = RUN_DIR.name
JSONL = RUN_DIR/"learning-candidates.jsonl"
PROPOSAL = ROOT/"01 - Learning/Skill Patch Proposals"/f"{RUN_LABEL}-compiler-proposals.md"
OUT = ROOT/"01 - Learning/Daily Digests"/f"{RUN_LABEL}-daily-learning-digest.md"
OUT.parent.mkdir(parents=True, exist_ok=True)

HIGH_SIGNAL_HOSTS = {
    "hackerone.com", "rekt.news", "solodit.cyfrin.io", "code4rena.com", "audits.sherlock.xyz", "cantina.xyz",
    "simonwillison.net", "embracethered.com", "www.chainsecurity.com", "chainsecurity.com", "immunefi.com",
    "portswigger.net", "apisecurity.io", "labs.detectify.com", "www.paradigm.xyz", "paradigm.xyz",
}
NOISE_TERMS = re.compile(r"customers|compliance|fellowship|predictions|vasp|buy[- ]vs[- ]build|regulatory|career|contact|pricing|leaderboard|opportunities \| cantina|contests - all|writing$", re.I)
STRONG_TERMS = re.compile(r"idor|bola|access control|prompt injection|role confusion|race|toctou|ssrf|graphql|bridge|rekt|proof|oracle|rounding|invariant|exploit|cve|ghsa|report #|finding|audit|postmortem|root cause|xss|file upload|deserialization|jwt|oauth", re.I)

records=[]
if JSONL.exists():
    records=[json.loads(l) for l in JSONL.read_text(encoding='utf-8').splitlines() if l.strip()]
actual=[r for r in records if r.get('content_quality')=='actual_content' and r.get('local_processing_status') in {'fetched_content','browser_fetched_content'}]

def candidate_score(r: dict) -> int:
    url=r.get('effective_url') or r.get('url') or ''
    title=r.get('title') or ''
    blob=' '.join([url,title,r.get('source_name') or '', r.get('content_excerpt') or ''])[:12000]
    host=urlparse(url).netloc.lower()
    score=0
    if host in HIGH_SIGNAL_HOSTS or any(host.endswith('.'+h) for h in HIGH_SIGNAL_HOSTS): score+=20
    if STRONG_TERMS.search(blob): score+=35
    if NOISE_TERMS.search(blob): score-=50
    if r.get('source_group') in {'appsec_fyi_linked_resources','daily_deep_content','browser_dom_linked_resources'}: score+=10
    if r.get('linked_resource_score'): score += min(int(r.get('linked_resource_score') or 0)//10, 15)
    chars=int(r.get('content_char_count') or 0)
    if chars > 3000: score+=5
    if chars > 20000: score-=5  # often index/listing-ish despite extraction
    return score

ranked=sorted([(candidate_score(r), r) for r in actual], key=lambda x:(-x[0], x[1].get('title') or ''))
high=[(s,r) for s,r in ranked if s>=35]
watch=[(s,r) for s,r in ranked if 15<=s<35]
noise=[(s,r) for s,r in ranked if s<15]

proposal_sections=[]
if PROPOSAL.exists():
    current=None
    for line in PROPOSAL.read_text(encoding='utf-8').splitlines():
        if line.startswith('### '):
            current=line[4:].strip(); proposal_sections.append((current,0))
        elif current and line.startswith('- `'):
            name,count=proposal_sections[-1]; proposal_sections[-1]=(name,count+1)

def md_item(score, r):
    url=r.get('effective_url') or r.get('url') or ''
    title=(r.get('title') or 'untitled').replace('\n',' ')[:180]
    src=r.get('source_name') or ''
    return f"- **{score}** — [{title}]({url}) — `{src}`"

lines=[]
lines.append(f"# Daily learning digest — {RUN_LABEL}\n")
lines.append(f"- Generated: {datetime.now(timezone.utc).isoformat()}")
lines.append(f"- Inbox: `{RUN_DIR}`")
lines.append(f"- Records: `{len(records)}`")
lines.append(f"- Actual content compiled candidates: `{len(actual)}`")
lines.append(f"- Heuristic review-priority candidates: `{len(high)}`")
lines.append(f"- Watchlist candidates: `{len(watch)}`")
lines.append(f"- Likely noise/defer: `{len(noise)}`\n")
lines.append("## Content status counts\n")
for k,v in sorted(Counter(r.get('content_quality') or 'unknown' for r in records).items()): lines.append(f"- {k}: {v}")
lines.append("\n## Source groups\n")
for k,v in sorted(Counter(r.get('source_group') or 'unknown' for r in records).items()): lines.append(f"- {k}: {v}")
if proposal_sections:
    lines.append("\n## Compiler proposal sections\n")
    for name,count in proposal_sections: lines.append(f"- {name}: {count}")
lines.append("\n## Heuristic review-priority candidates\n")
lines.append("This score ranks likely topical relevance for review; it is not a trust, evidence, corroboration, or promotion score.\n")
for s,r in high[:25]: lines.append(md_item(s,r))
lines.append("\n## Watchlist\n")
for s,r in watch[:25]: lines.append(md_item(s,r))
lines.append("\n## Likely noise / defer\n")
for s,r in noise[:25]: lines.append(md_item(s,r))
lines.append("\n## Recommended action\n")
if high:
    lines.append("Review heuristic-priority candidates first. Promotion still requires source-specific novelty, categorical source policy, provenance, corroboration where configured, eval linkage where applicable, and a recorded review decision.")
else:
    lines.append("No heuristic review-priority candidates; keep proposals as discovery/watchlist only.")
OUT.write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps({'digest':str(OUT),'records':len(records),'actual':len(actual),'high_signal':len(high),'watchlist':len(watch),'noise':len(noise)}, indent=2))
