---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.396607+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: File Upload / Media Processing
---

# 10 Types of Web Vulnerabilities that are Often Missed - Labs Detectify

- URL: `https://labs.detectify.com/2021/09/30/10-types-web-vulnerabilities-often-missed/`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `24403`
- Classification: **Web2 skill update**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- XXE via Office Open XML Parsers Office Open XML (OOXML) (pronounced oooksamaliabaddabingbaddaboom ) is a file format that is able to represent word, spreadsheet and presentation documents.
- These file types are actually ZIP files filled with a bunch of XML files.
- Unzip one! test$ file test.docx test.docx: Microsoft Word 2007+ test$ unzip test.docx Archive: test.docx inflating: word/numbering.xml inflating: word/settings.xml inflating: word/fontTable.xml inflating: word/styles.xml inflating: word/document.xml inflating: word/_rels/document.xml.rels inflating: _rels/.rels inflating: word/theme/theme1.xml inflating: [Content_Types].xml If you are hacker-minded, you might have already guessed where this is headed.

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
