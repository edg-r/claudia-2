# GPCO 410 One-Pager: Myanmar 2010 Polity Report

**Use for:** Regime Type / Polity IV data memo  
**Source anchor:** *Polity IV Country Report 2010: Myanmar (Burma)*  
**Main takeaway:** Polity does not code Myanmar in 2010 as democratizing in a meaningful electoral sense. It codes an authoritarian military regime managing an executive-guided transition while preserving decisive military control.

## What the 2010 Report Says

Myanmar's 2010 country score is unchanged from 2009: `POLITY = -6`, with `DEMOC = 0` and `AUTOC = 6`. That places the regime on the autocratic side of the Polity scale, not in the democratic range. The report marks the case as **tentative** and fragmented in northern and eastern peripheral regions, which matters because the political order was not only authoritarian but also territorially contested.

The report's narrative is blunt about the transition. The 2008 Constitution and 2010 election were part of a military-designed "roadmap to democracy," but the military preserved a leading role. The constitution reserved 25 percent of seats in both houses for military appointees, gave the military a veto over constitutional change because amendments required more than 75 percent approval, protected military control over key security ministries, and gave the commander-in-chief broad emergency authority. The 2010 election produced an expected USDP landslide, the NLD was effectively excluded after refusing to register, and international observers treated the election as a sham (Marshall & Jaggers, 2011).

## How to Read the Codes

| Code | Myanmar 2010 | Meaning for regime type |
|---|---:|---|
| `POLITY` | `-6` | Combined score: `DEMOC - AUTOC`. Myanmar is coded as autocratic, not democratic. |
| `DEMOC` | `0` | No institutionalized democracy points. |
| `AUTOC` | `6` | Strong autocratic authority traits. |
| `XRREG / XRCOMP / XROPEN` | `2 / 0 / 0` | Executive recruitment is an **executive-guided transition**: the ruling military is redesigning the formal system from above, not allowing open competitive executive selection. |
| `XCONST` | `2` | Very weak constraint on executive authority. The country report labels this "slight limitations," but the manual treats `2` as an intermediate category near unlimited authority. |
| `PARREG / PARCOMP` | `4 / 1` | Participation is restricted and competition is repressed. Organized activity exists, but outside opposition is tightly controlled. |
| `DURABLE` | `47` | Polity treats the same basic authority pattern as dating back to the 1962 military takeover. |

Two distinctions are important for Edgar's memo. First, `POLITY` is an aggregate score, not a full constitutional diagnosis. Second, component codes are not mechanical facts; they are expert-coded judgments converted into a reproducible scale (Marshall & Gurr, 2020). That means the memo can praise Polity's transparency while still critiquing what its aggregate score leaves out.

## How Edgar Should Use This in the Data Memo

Use the report as evidence that Polity **saw** the Tatmadaw's reserved role. The best critique is not "Polity missed the military." The better critique is: Polity's own country narrative records military veto power, military-appointed legislators, control over coercive ministries, and emergency authority, but the aggregate `POLITY` score has no separate civilian-control-of-coercion component.

This helps explain the later coding problem. In the time-series data, Myanmar rises after the 2015 election and is coded `polity2 = +8` for 2016-2018. That increase is understandable under Polity's rules because executive recruitment, participation, and formal constraints changed. But the 2010 report shows the institutional trap that remained built into the system: elected civilian rule could expand without fully subordinating the military. For the memo, frame Myanmar as a case where Polity captures **formal authority characteristics** better than it captures **reserved military veto power**.

The clean thesis move:

> Myanmar shows both the strength and limit of Polity IV. The score is reproducible because coders apply published rules to executive recruitment, executive constraints, and participation. But the Myanmar report itself shows that regime type also depended on whether elected civilians controlled the coercive core of the state. Since Polity does not separately measure that, the later high score risks overstating democratic consolidation.

## Memo Sentence Bank

- "The 2010 country report coded Myanmar as `POLITY = -6`, with no democracy points and six autocracy points, despite the formal 2008 constitutional roadmap."
- "The report's narrative makes clear that the transition was executive-guided by the military rather than competitively democratic."
- "Polity recognized the Tatmadaw's reserved constitutional position, but the combined score did not include an independent measure of civilian control over coercive institutions."
- "Myanmar is therefore a good measurement case because the aggregate score is defensible under the codebook but incomplete for assessing coup vulnerability."

## References

Marshall, M. G., & Gurr, T. R. (2020). *Polity5: Political regime characteristics and transitions, 1800-2018: Dataset users' manual*. Center for Systemic Peace. https://www.systemicpeace.org/inscr/p5manualv2018.pdf

Marshall, M. G., & Jaggers, K. (2011). *Polity IV country report 2010: Myanmar (Burma)*. Center for Systemic Peace. https://www.systemicpeace.org/polity/Myanmar2010.pdf

---
Generated for: Edgar Agunias
Date: 2026-05-17
Model: GPT-5 (Codex)
Sources: `inbox/Myanmar2010.pdf`; Polity5 v2018 users' manual; Athena course memory for the Regime Type / Polity IV data memo
Agent: Athena
---
