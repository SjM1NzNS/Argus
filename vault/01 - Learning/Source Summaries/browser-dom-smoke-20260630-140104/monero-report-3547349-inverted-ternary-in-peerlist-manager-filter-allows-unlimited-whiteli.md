---
type: learning-source-summary
compiled_at: 2026-06-30T12:02:12.841350+00:00
source_quality: 6
classification: severity rule
vulnerability_class: File Upload / Media Processing
---

# Monero | Report #3547349 - Inverted ternary in peerlist_manager::filter() allows unlimited whitelist entries per host via different ports | HackerOne

- URL: `https://hackerone.com/reports/3547349`
- Source group: `browser_dom_linked_resources`
- Content chars: `12735`
- Classification: **severity rule**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- Compare it with another function, which is correct: Code • 509 Bytes 1 //-------------------------------------------------------------------------------------------------- 2 template<typename F> inline 3 bool peerlist_manager::foreach(bool white, const F &f) 4 { 5 CRITICAL_REGION_LOCAL(m_peerlist_lock); 6 peers_indexed::index<by_time>::type& by_time_index = white ? m_peers_white.get<by_time>() : m_peers_gray.get<by_time>(); 7 for(const peers_indexed::value_type& vl: boost::adaptors::reverse(by_time_index)) 8 if (!f(vl)) 9 return false; 10 return true; 11 } 12 Releases Affected: latest master branch Code • 63 Bytes 1$ git rev-parse master 2f99ee72d4b5065ddcaba2b74fcc6c8dc9be385dc Steps To Reproduce: add test to tests/unit_tests/test_peerlist.cpp Code • 3.12 KiB 1// XXXKE peerlist_manager::filter() has inverted ternary 2TEST(peer_list, filter_inverted_ternary_bug) 3{ 4 nodetool::peerlist_manager plm; 5 plm.init(nodetool::peerlist_types{}, false); 6 7 { 8 nodetool::peerlist_entry ple{}; 9 ple.adr = MAKE_IPV4_ADDRESS(93,184,216,34, 18080); 10 ple.id = 9999; 11 ple.last_seen = 1000; 12 plm.append_with_peer_gray(ple); 13 } 14 ASSERT_EQ(plm.get_gray_peers_count(), 1u); 15 16 { 17 nodetool::peerlist_entry ple{}; 18 ple.adr = MAKE_IPV4_ADDRESS(45,33,32,1, 28080); 19 ple.id = 8888; 20 ple.last_seen = 1000; 21 plm.append_with_peer_gray(ple); 22 } 23 ASSERT_EQ(plm.get_gray_peers_count(), 2u); 24 25 { 26 nodetool::peerlist_entry ple{}; 27 ple.adr = MAKE_IPV4_ADDRESS(45,33,32,1, 18080); 28 ple.id = 1001; 29 ple.last_seen = 2000; 30 plm.append_with_peer_white(ple); 31 } 32 std::cout << "[Step 1] After adding 45.33.32.1:18080 to white:" << std::endl; 33 std::cout << " white_count = " << plm.get_white_peers_count() 34 << " (expect 1)" << std::endl; 35 std::cout << " gray_count = " << plm.get_gray_peers_count() 36 << std::endl; 37 38 EXPECT_EQ(plm.get_white_peers_count(), 1u); 39 EXPECT_EQ(plm.get_gray_peers_count(), 2u) 40 << "filter(true,...) evicted from gray list instead of white list. " 41 "Gray entry 45.33.32.1:28080 was wrongly removed."; 42 43 { 44 nodetool::peerlist_entry ple{}; 45 ple.adr = MAKE_IPV4_ADDRESS(45,33,32,1, 18081); 46 ple.id = 1002; 47 ple.last_seen = 3000; 48 plm.append_with_peer_white(ple); 49 } 50 std::cout << "[Step 2] After adding 45.33.32.1:18081 to white:" << std::endl; 51 std::cout << " white_count = " << plm.get_white_peers_count() 52 << " (expect 1 if fixed, 2 if buggy)" << std::endl; 53 std::cout << " gray_count = " << plm.get_gray_peers_count() << std::endl; 54 55 EXPECT_EQ(plm.get_white_peers_count(), 1u) 56 << "Same host (45.33.32.1) has multiple white list entries " 57 "on different ports. evict_host_from_peerlist did not clean white list. "; 58 59 nodetool::peerlist_manager plm2; 60 plm2.init(nodetool::peerlist_types{}, false); 61 62 for (int i = 1; i <= 3; i++) 63 { 64 nodetool::peerlist_entry ple{}; 65 ple.adr = MAKE_IPV4_ADDRESS(104,16,0,i, 18080); 66 ple.id = 2000 + i; 67 ple.last_seen = 1000 + i; 68 plm2.append_with_peer_white(ple); 69 } 70 ASSERT_EQ(plm2.get_white_peers_count(), 3u); 71 72 for (int port = 0; port < 20; port++) 73 { 74 nodetool::peerlist_entry ple{}; 75 ple.adr = MAKE_IPV4_ADDRESS(45,33,32,1, 18080 + port); 76 ple.id = 5000 + port; 77 ple.last_seen = 5000 + port; 78 plm2.append_with_peer_white(ple); 79 } 80 81 std::cout << "After 3 honest peers + 20 attacker ports on 45.33.32.1:" << std::endl; 82 std::cout << " white_count = " << plm2.get_white_peers_count() 83 << "" << std::endl; 84 85 std::set<std::string> unique_hosts; 86 size_t attacker_entries = 0; 87 plm2.foreach(true, [&](const nodetool::peerlist_entry &pe) { 88 unique_hosts.insert(pe.adr.host_str()); 89 if (pe.adr.host_str() == "45.33.32.1") 90 attacker_entries++; 91 return true; 92 }); 93 94 std::cout << " unique_hosts = " << unique_hosts.size() << std::endl; 95 std::cout << " attacker_entries = " << attacker_entries 96 << "" << std::endl; 97 98} 99 save this file as Dockerfile.test-peerlist Code • 990 Bytes 1FROM ubuntu:22.04 AS builder 2 3RUN set -ex && \ 4 apt-get update && \ 5 DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends --yes install \ 6 build-essential \ 7 ca-certificates \ 8

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
