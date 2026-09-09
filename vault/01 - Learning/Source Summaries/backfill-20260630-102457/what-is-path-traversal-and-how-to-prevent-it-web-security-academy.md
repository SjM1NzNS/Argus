---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.013448+00:00
source_quality: 8
classification: technique
vulnerability_class: File Upload / Media Processing
---

# What is path traversal, and how to prevent it? | Web Security Academy

- URL: `https://portswigger.net/web-security/file-path-traversal`
- Source group: `backfill_deep_content`
- Content chars: `6604`
- Classification: **technique**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- As a result, an attacker can request the following URL to retrieve the /etc/passwd file from the server's filesystem: https://insecure-website.com/loadImage?filename=../../../etc/passwd This causes the application to read from the following file path: /var/www/images/../../../etc/passwd The sequence ../ is valid within a file path, and means to step up one level in the directory structure.
- The three consecutive ../ sequences step up from /var/www/images/ to the filesystem root, and so the file that is actually read is: /etc/passwd On Unix-based operating systems, this is a standard file containing details of the users that are registered on the server, but an attacker could retrieve other arbitrary files using the same technique.
- The following is an example of an equivalent attack against a Windows-based server: https://insecure-website.com/loadImage?filename=..\..\..\windows\win.ini Common obstacles to exploiting path traversal vulnerabilities Many applications that place user input into file paths implement defenses against path traversal attacks.

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
