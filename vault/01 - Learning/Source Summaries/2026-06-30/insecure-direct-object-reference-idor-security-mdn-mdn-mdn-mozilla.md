---
type: learning-source-summary
compiled_at: 2026-06-30T07:45:38.492014+00:00
source_quality: 9
classification: severity rule
vulnerability_class: IDOR / BOLA / Access Control
---

# Insecure Direct Object Reference (IDOR) - Security | MDN MDN MDN Mozilla

- URL: `https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/IDOR`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `9342`
- Classification: **severity rule**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- Skip to main content Skip to search HTML: Markup language Elements Global attributes Attributes See all… Responsive images HTML cheatsheet Date & time formats See all… SVG MathML XML CSS: Styling language Properties Selectors At-rules Values See all… Box model Animations Flexbox Colors See all… Column layouts Centering an element Card component See all… JavaScript: Scripting language Standard built-in objects Expressions & operators Statements & declarations Functions See all… Control flow & error handing Loops and iteration Working with objects Using classes See all… Web APIs: Programming interfaces File system API Fetch API Geolocation API HTML DOM API Push API Service worker API See all… Using the Web animation API Using the Fetch API Working with the History API Using the Web speech API Using web workers All web technology Accessibility HTTP URI Web extensions WebAssembly WebDriver See all… Media Performance Privacy Security Progressive web apps Learn web development Getting started modules Core modules MDN Curriculum Check out the video course from Scrimba, our partner Structuring content with HTML module CSS styling basics module CSS layout module Dynamic scripting with JavaScript module Discover our tools Playground HTTP Observatory Border-image generator Border-radius generator Box-shadow generator Color format converter Color mixer Shape generator Get to know MDN better About MDN Advertise with us Community MDN on GitHub Web Security Attacks Insecure Direct Object Reference (IDOR) OS default Light Dark Deutsch English (US) Insecure Direct Object Reference (IDOR) Insecure Direct Object Reference (IDOR) is a vulnerability that allows an attacker to exploit insufficient access control and insecure exposure of object identifiers, such as database keys or file paths.
- For example, maybe your application doesn't provide the user's ID in the URL but instead passes the user ID in a hidden form element: html <form action="updateUser" method="POST"> <input type="hidden" name="user_id" value="1234" /> <button type="submit">Update profile</button> </form> If no server-side access control is performed, the attacker can manipulate the user_id value in the hidden <input> element to a different user ID and might be able to modify the profile without authorization.
- In this article Example scenarios Defenses against IDOR Defense summary checklist See also Example scenarios The classic IDOR attack happens when the server only checks that the user is authenticated, but not whether they are authorized to access an object reference.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
