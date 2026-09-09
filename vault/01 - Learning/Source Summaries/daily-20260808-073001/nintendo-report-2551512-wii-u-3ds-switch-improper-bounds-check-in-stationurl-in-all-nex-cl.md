---
type: learning-source-summary
compiled_at: 2026-08-08T05:31:23.160310+00:00
source_quality: 5
classification: severity rule
vulnerability_class: Web2 General
---

# Nintendo | Report #2551512 - [Wii U/3DS/Switch] Improper bounds check in StationURL in all NEX clients leading to remote crash/RCE | HackerOne

- URL: `https://hackerone.com/reports/2551512`
- Source group: `browser_dom_linked_resources`
- Content chars: `1730`
- Classification: **severity rule**
- Vulnerability class: **Web2 General**

## Source summary

- Skip to main content > Learn more about HackerOne Log in 6 #2551512 [Wii U/3DS/Switch] Improper bounds check in StationURL in all NEX clients leading to remote crash/RCE Share: Report SUMMARY BY NINTENDO SUMMARY BY JONBARROW nn::nex::StationURL::Format performs unsafe string formatting which lacks bounds checks.
- The StationURL is formatted to a string using code such as this: Code • 524 Bytes 1nn::nex::StationURL::Format() { 2 wchar_t url[1024]; 3 uint offset = 0; 4 uint written = 0; 5 bool writeDelimiter = false; 6 7 /* normalParams is a std::map<nn::nex::String, nn::nex::String> */ 8 for (auto param = normalParams.begin(); param != normalParams.end(); param++) { 9 if (writeDelimiter) { 10 written = swprintf(url + offset, 1024, L";"); 11 offset += written; 12 } 13 14 written = swprintf(url + offset, 1024, L"%ls%ls%ls", param->first, L"=", param->second); 15 offset += written; 16 writeDelimiter = true; 17 } 18 19 SetURL(url) 20} The calls to swprintf do not take into account the number of bytes already written into the url buffer, which can lead to a stack overflow given either a large enough number of parameters or a parameter with a large enough key/value.
- Since StationURLs are shared between clients, often using the server as a middleman, a remote user could send a large enough value through to another client, trigger this overflow TIMELINE jonbarrow submitted a report to Nintendo.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
