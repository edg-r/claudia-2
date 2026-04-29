# Advanced AI Workflows Among Graduate and Professional Students in the Human Sciences

A research paper on what non-trivial student practice actually looks like in April 2026, built for a reader who is already past the upload-and-summarize stage.

## 1. Executive Summary

Five findings worth leading with.

**First, the orchestration frontier has moved from single-prompt chat to multi-agent, file-backed systems run out of a terminal.** The leading public exemplars are no longer ChatGPT or Claude.ai in the browser. They are Claude Code and Codex CLI installations with dozens of named subagents, persistent Markdown memory, and hook automation. Academic variants of this pattern are in active circulation on GitHub (letitbk/claude-academic-setup, Imbad0202/academic-research-skills, wanshuiyin/ARIS) and are being adopted by a small but visible cohort of social-science researchers. Edgar's Claudia system is an unusually mature instance of this same class, not an outlier kind.

**Second, the centre of gravity for advanced qualitative work is LLM-assisted thematic analysis with explicit protocols.** The GATOS workflow (Shen, Wu, Patt, Mendoza-Denton 2025, Sage IJQM) and the LATA pilot (Wang et al. CSCW 2025) are the two most-cited protocols. Both move past "ask ChatGPT to code my transcripts" into formally specified pipelines with inter-rater checks, inductive-deductive mixing, and documented failure modes around sarcasm, marginalised-group speech, and humour. The pattern is diffusing fastest in education research, maternal health, and equity-focused evaluation work.

**Third, the RAG-over-personal-corpus pattern has standardised around three stacks**: Obsidian plus Smart Connections or Copilot plus Ollama for local-first users; Zotero with the 54yyyu/zotero-mcp or cookjohn/zotero-mcp plugins for citation-heavy researchers; and NotebookLM for students who want source-grounded Q&A without owning the pipeline. The interesting practitioners run two or three of these side by side and route queries by what each is good at.

**Fourth, voice preservation is becoming a named craft problem, not a style preference.** The most useful writing on it in 2025 and 2026 comes from working academics (Kim Klassen, the Transmitter's "from bench to bot" column, Thesify, Indisputably) rather than vendors. The consensus protocol has stabilised: draft first in your own voice, use the model as analyzer not writer, feed samples of your own strong prose when rewriting is needed, and document what the model touched. Edgar's own voice_profile plus aggressive-when-AI-source rule is one of the sharper articulations of the same idea.

**Fifth, the governance layer is being built by students and instructors in parallel, not by universities.** Harvard FAS's 2024 policy, Stanford GSB's allow-but-disclose stance, and LSE's Eden Centre framework are all thin scaffolds that defer to instructors. The actual norms are forming in syllabus language, in per-course disclosure blocks, and in student-side protocols like Claudia's ai-disclosure SOP. There is no dominant template. Students running sophisticated workflows are often ahead of their institutions on attribution practice.

## 2. Framing the Gap

The dominant public narrative about students and AI is wrong in two directions at once. The panic version assumes students are mostly using LLMs to replace thought. The evangelist version assumes the frontier is "ChatGPT for summaries." Both miss the actual frontier, which lives in three-layer toolchains that do not appear in mainstream coverage because mainstream coverage is written by people who do not run terminals.

A rough partition of what students are actually doing:

- **Tier 0, assistive chat.** Upload, ask, paste back. This is the vast majority of documented practice and the ceiling of every vendor-marketed use case. Nothing in this paper covers it.
- **Tier 1, tool-integrated chat.** Custom GPTs, Claude Projects, NotebookLM notebooks, Zotero plus AI plugins. Source grounding is real, but the workflow is still a chat with better retrieval. Aaron Tay at Singapore Management University writes the best practitioner-facing coverage of this tier on his Substack.
- **Tier 2, agentic and orchestrated.** Claude Code, Codex, Aider, Cursor with subagents. Persistent Markdown memory. MCP connectors. Hook automation. Multi-agent handoff. This is where Claudia lives and where the research question below concentrates.
- **Tier 3, fully autonomous research loops.** Projects like ARIS (Auto-Research-In-Sleep) that run overnight, score their own work, and rewrite. Mostly in ML research and coding domains, not yet in the human sciences at student scale, but the pattern is leaking in.

The human-sciences frontier sits inside Tier 2, with a small number of Tier-3-curious students experimenting. The rest of this paper assumes Tier 2 as the baseline of interest.

## 3. Taxonomy of Advanced Workflows

Ten patterns, each with concrete exemplars.

### 3.1 Orchestration and multi-agent

The most public academic-flavored orchestrators on GitHub as of April 2026:

- **letitbk/claude-academic-setup** — a Claude Code plus Cursor configuration for social-science researchers. Ships 22 skills, 13 plugins, 5 commands, 14 IDE extensions, covering R, Stata, Python. Emphasises "Plan Mode before non-trivial tasks, because planning is cheap while re-doing analysis is expensive." This is the single closest public analog to Claudia in the social-science space.
- **Imbad0202/academic-research-skills** — Claude Code skills pack structured around a research → write → review → revise → finalize pipeline. Built for paper drafting.
- **wanshuiyin/ARIS** — lightweight Markdown-only skills for autonomous ML research (cross-model review loops, idea discovery, experiment automation). Framework-free and agent-agnostic (Claude Code, Codex, OpenClaw). ARIS has a "let it work while you sleep" ethos that is uncommon in student-facing tools.
- **wshobson/agents** — a widely-cloned multi-agent orchestration pack for Claude Code. Not academic-specific but used as a template.

Patterns that show up in all four: named subagents rather than generic tool calls, Markdown-only memory (no vector DBs in the orchestration layer itself), explicit Plan-Mode gates, and review agents that score the primary agent's output before it ships. Claudia's Atlas-Hermes-course-agent structure is idiomatic within this cohort.

### 3.2 Persistent memory and RAG over personal corpus

The standard stack for human-sciences students:

- **Obsidian plus Smart Connections or Copilot plus Ollama.** The Karpathy LLM Wiki pattern (kytmanov/obsidian-llm-wiki-local) is the most-referenced open implementation: drop Markdown notes, AI extracts concepts, wiki auto-links and grows. Reduces to three operations: ingest, query, lint. nomic-embed-text is the practitioner-favorite embedding model on CPU; mxbai-embed-large is the quality favorite. Edgar's Ollama plus nomic-embed-text setup is exactly this idiom.
- **Zotero plus MCP.** 54yyyu/zotero-mcp and cookjohn/zotero-mcp are the two active implementations. They expose semantic search, annotation extraction, PDF content read, BibTeX export to Claude or ChatGPT directly. The Zotero forums have an official discussion thread that treats this as a near-endorsed direction.
- **NotebookLM.** The one non-local option in common use. Practitioners describe it as strong on source-grounded Q&A and one-click structured artefacts (study guides, briefing docs, timelines), weak on reasoning and anything agentic. The most common practitioner recommendation is to run NotebookLM alongside Claude Projects and route by query type.

### 3.3 Deep use by discipline

What actually shows up as documented practice, not projection:

- **Law.** Obsidian-plus-RAG for case outlines is discussed on the Obsidian forum (forum.obsidian.md/t/obsidian-rag-personal-ai-bot). UC Davis Mabie Law Library maintains the most practical student-facing genAI guide. Stanford's HAI hallucination study (Magesh et al., "Hallucination-Free?", dho.stanford.edu) is cited everywhere as the reason law students no longer trust Lexis+ Protégé or Westlaw AI-Assisted Research unsupervised. The named limitation is 17 to 33 percent hallucination across vendor tools.
- **IR and security studies.** Thin on public documentation. Edgar's Claudia system, with theory-reference PDFs built from Fearon, Powell, Walter, Bueno de Mesquita, is one of the more developed student stacks I could find. The Political-LLM project (political-llm.org) and Le Mens et al., "Positioning Political Texts with Large Language Models by Asking and Averaging" (Political Analysis 2024) anchor the methods side.
- **History.** The OCR-plus-LLM pipeline for archival material is the most documented human-sciences use of advanced AI anywhere. Transcription Pearl is the GUI tool. Character-level accuracy on handwritten historical documents now sits at 93 to 94 percent with LLM post-correction (Humphries et al., "Unlocking the Archives," arXiv 2411.03340). A 45,000-page historical-records pipeline is documented in Boros et al., "Multimodal LLMs for OCR, OCR Post-Correction, and NER in Historical Documents" (arXiv 2504.00414). Edgar's ocrmypdf plus tesseract pipeline on GPPS 444 and GPPS 463 scans is the same pattern at smaller scale.
- **Policy (MPP, MPA, MIA).** Almost no public documentation of advanced workflows at named programs. The gap is striking. HKS, SAIS, SIPA, Harris, Hertie, LKY all publish about AI in the abstract but not about student practice. This is a research gap rather than an absence.
- **Qualitative social science.** GATOS (Shen et al., Sage IJQM 2025) is the reference protocol for LLM-assisted thematic coding. LATA (Wang et al., CSCW 2025) is the second. Jiang, Ko-Wong, Valdovinos Gutierrez (Educational Researcher 2025, "Feasibility and Comparability of Using AI for Qualitative Data Analysis in Equity-Focused Research") is the equity-specific study. All three are protocol papers, not hype.
- **Applied quantitative methods.** The tooling here is real. hanlulong/stata-mcp and tmonk/stata-workbench expose Stata to Cursor, Claude Code, Codex over MCP. Andrew Heiss's stata-quarto gist is widely circulated. The Bernhard Bieri literate-programming-in-Stata post is the clearest walkthrough of the Quarto plus Stata plus AI pipeline.

### 3.4 Qualitative methods at scale

Beyond thematic analysis, the patterns documented in 2025 and 2026:

- **Coding closed-ended survey open-responses.** GATOS handles this explicitly.
- **NLP on political speeches.** Le Mens et al. (Political Analysis 2024) "ask and average" protocol. Specific use case: position UK party manifestos and US Senators on ideological dimensions by averaging LLM responses to positional questions. Cited in the Codebook LLMs paper (Halterman and Keith, Political Analysis 2025) as a measurement tool.
- **Archival-scale document triage.** See history section above.
- **Legal case clustering.** Agentic.ai's "best research and analysis agents" roundup documents several law-adjacent stacks, but none are student-specific.
- **Ethnographic field-note processing.** Mostly absent from the documented literature. The equity concerns in Jiang et al. 2025 suggest principled caution is warranted here.

### 3.5 Writing beyond drafting

The mature practice is not "use AI to write faster." It is a set of named passes:

- **Reverse outlining.** Submit a finished draft, ask for an outline of what it says, compare to what you meant to say.
- **Counter-argument generation.** Ask a devil's-advocate agent to attack your thesis. Imbad0202/academic-research-skills ships this as a review stage.
- **Citation verification.** Feed draft plus source PDFs, ask which claims lack direct support. Stanford's Legal RAG paper is the reason this is taken seriously.
- **Response-to-reviewer drafting.** Load reviewer comments and prior draft, generate a traceability matrix (claim → change → location). Appears explicitly in the 7-agent academic paper reviewer pattern documented in the Popularaitools Claude Code 2026 guide.
- **House-style enforcement.** Claudia's Calliope agent with style-edit skill and voice_profile.md is one of the few public instances of this as a named, persistent system. The Enago Academy and Kim Klassen posts describe the principle; Claudia operationalises it.

### 3.6 Study and exam prep as active learning

Three patterns actually in use:

- **AI-generated spaced-repetition cards tied to primary sources.** AnkiDecks, StudyCards AI, CogniGuide are the vendor end. The sophisticated student version is to generate cards from reading PDFs with explicit source-page anchors and accept or reject manually. FSRS has displaced SM-2 as the default algorithm. Retain.cards and FlashRecall are the FSRS-native alternatives to Anki.
- **Socratic-dialogue exam prep.** Not a vendor feature. Emerges as a user pattern: "act as a hostile examiner on this topic, press until I contradict myself." Joe Sabado's knowledge-system Substack documents a variant for leadership work.
- **Theory-reference cards from readings.** Edgar's theory-reference-pdf skill (retired BLUF, per your own 2026-04-22 feedback) is the sharpest articulation of the difference between slide-summary cards (shallow) and reading-anchored theory cards (deep). This pattern is rare in the documented literature. It is worth publishing.

### 3.7 Tool-layer integrations

What is actually wired up in sophisticated stacks:

- **MCP servers.** Google Workspace (taylorwilsdon/google_workspace_mcp, a-bonus/google-docs-mcp), Notion (official plus ContexaAI), Zotero (two implementations above), Stata (hanlulong). Claudia's Gmail connector sits in this bucket, including the read-and-draft-only limitation.
- **Local LLM stacks.** Ollama plus Open WebUI plus Obsidian plugins for privacy-sensitive work. nomic-embed-text and mxbai-embed-large are the default embeddings. Llama 3.2 and Qwen 2.5 are the default generators for local-first users.
- **LaTeX and Quarto.** Quarto plus Stata plus Claude Code is the mature applied-stats pipeline. LaTeX MCP is thin; most practitioners use Overleaf plus clipboard flow.
- **Reference manager automation.** Zotero MCP is the central example. The lifelong-research Substack series ("Zotero Meets Claude") is the most detailed walkthrough.

### 3.8 Governance, disclosure, voice

The institutional layer is weak and the practitioner layer is doing most of the work.

- **Institutional.** Harvard FAS 2024 AI policy treats undisclosed AI-assisted writing as plagiarism but defers citation form to instructors. Stanford GSB allows AI on take-home work with disclosure and bans it on in-class assessments. LSE's Eden Centre publishes a school position but defers to courses. Oxford's policy (Bodleian LibGuide) requires declaration when AI is explicitly permitted. No top program has a mandatory disclosure template.
- **Practitioner.** Claudia's ai-disclosure SOP with the Edgar-to-grader template, anchored to Anthropic usage policy and UCSD or GPS academic-integrity pages, is one of the cleaner instances of filling this gap. Thesify's PhD-AI-policies 2025 guide and the Thesify voice-preservation post are the clearest practitioner references.
- **Voice.** The stabilised protocol: draft in your own voice first, use the model as analyzer not writer, feed samples of your strong prose when rewriting is necessary, document what the model touched, invert the protocol when the source is already AI-generated (Edgar's feedback_voice_pass_ai_source rule, which has no published equivalent I could find and may be original).

### 3.9 Community and diffusion

Where advanced practice is actually shared:

- **Substack.** Aaron Tay (aarontay.substack.com, Singapore Management University librarian) is the single best source on academic agentic workflows. Joe Sabado (joesabado.substack.com) documents a personal Claude-plus-MCP research system. Simon Willison (simonw.substack.com) is the reference for engineer-flavored patterns. "Intelligence and Power" (intelligenceandpower.substack.com) covers no-code research pipelines.
- **GitHub.** The four orchestrator repos named above plus the Stata MCP pair. These are the concrete artefacts.
- **Discord.** AI Study Hub, Learn AI Together (Louis-Francois Bouchard's server), Jeremy Howard's Solve It community. None are human-sciences specific. The human-sciences graduate student Discord frontier is thin.
- **School newspapers and faculty blogs.** Almost nothing at the level of sophistication relevant here. The Chronicle of Higher Ed and Inside Higher Ed cover policy and panic, not practice.
- **Course syllabi that teach these workflows.** Vanishingly rare. Andrew Heiss's Quarto-Stata material and the Political-LLM course materials are the two instances I could find that treat Tier-2 workflows as a teachable skill.

### 3.10 Emerging patterns (12 to 18 months)

Speculative but grounded:

- **1M-context literature review.** Claude Opus 4.6 1M-context tier, Gemini 3.1 Pro, GPT-5.5 Pro all ship 1M-capable configurations as of spring 2026. Cross-paper synthesis over 50 to 100 papers in a single context without RAG is now possible. The pricing cliff at 200k input tokens (Edgar's reference_anthropic_pricing_cliff note is correct and widely experienced) keeps this from being the default, but practitioners are routing the hard synthesis calls to 1M and the iterative work to 200k.
- **Agent-based literature review.** Undermind, Elicit Deep Search, Consensus Deep Search, AI2 Paperfinder are all marketed as agents. Aaron Tay's "Deep Research, Shallow Agency" post is the sharpest critique: their agency is bounded by pre-programmed workflows and they fail on off-track queries. The sophisticated pattern is to use them as first-pass discovery and hand off synthesis to a general-purpose agent.
- **Multimodal archival work.** The history-OCR pattern is expanding to maps, photographs, annotated manuscripts. Still research-paper-only, not yet standard practice.
- **Local models for privacy-sensitive coursework.** IRB-covered qualitative data, legal clinic work, anything with confidentiality constraints. Ollama plus Llama 3.2 or Qwen 2.5 is the default stack. Edgar's nomic-embed-text setup is directly adjacent.
- **Overnight autonomous research loops.** ARIS is the proof of concept. Human-sciences students are not yet doing this at scale, but the pattern is cheap to copy and I expect visible instances within 12 months.

## 4. Discipline-by-Discipline Snapshots

Short vignettes, what advanced use looks like on the ground.

**Law.** JD students at Stanford, Yale, and UC Davis use Obsidian-plus-RAG for case outlines and issue spotting. Westlaw AI-Assisted Research and Lexis+ Protégé are present but distrusted after Stanford's Legal RAG hallucination study. Clinic work increasingly uses local models for client-data isolation. The mature practice: outline in Obsidian, query with a local or Claude-Projects-based agent, always verify primary authority against the cite.

**IR and security studies.** Underdocumented. What exists is theory-reference pipelines (Claudia's model), actor-position coding via LLM (Political-LLM methods), and informal Socratic exam prep. SAIS, Fletcher, GPS are silent publicly. This is a research gap as much as a practice gap.

**History.** Most developed discipline for advanced AI work in the humanities. OCR plus LLM post-correction is mature. Handwriting recognition on historical manuscripts is approaching human-expert accuracy. PhD students document pipelines for 10,000 to 45,000 page corpora. Named-entity extraction with JSON output is standard. The bottleneck is validation, not capability.

**Policy (MPP, MPA, MIA).** Surprisingly thin. HKS, Harris, SIPA, LKY publish on AI-in-policy as subject matter but not AI-as-workflow. Memo pipelines, policy-brief house-style enforcement, stakeholder simulation exercises are all plausible use cases and Edgar's Claudia stack is a leading instance. Publish something.

**Qualitative social science.** GATOS and LATA protocols are the reference. Inter-rater reliability between human and LLM coder is the metric. Equity critiques (Jiang et al. 2025) are now part of the canon.

**Anthropology and ethnography.** Nearly absent from the documented literature. The equity concerns around sarcasm, humour, and marginalised-group speech cut hardest here.

**Applied quantitative methods.** Stata plus Quarto plus Cursor plus Claude Code is the mature pipeline. R plus Claude Code plus Quarto is the R-side equivalent. stargazer-to-OOXML pipelines for Word-delivered homework (Edgar's 2026-04-20 workflow) are common but rarely documented.

**Journalism and MBA programs.** Out of scope for this paper but adjacent. Journalism schools are beta-testing FOIA-document-triage pipelines. MBA programs at top-ten schools are integrating AI into case-analysis workflows with varying levels of sophistication.

## 5. Tooling Layer

What is actually in use, stripped of vendor marketing.

**The orchestration layer.** Claude Code (dominant), Codex CLI (growing), Cursor (for IDE-bound work), Aider (for coding-heavy workflows). ChatGPT and Claude.ai browser remain the default for Tier 0 and 1. Plan-Mode-before-action is the stabilised best practice.

**The memory layer.** Markdown files under version control is the dominant pattern. Vector databases (Qdrant, Chroma, Weaviate) are used in RAG pipelines but not as the primary memory substrate. SQLite for structured metadata (Claudia's claudia.db is idiomatic here). Obsidian as the human-facing view.

**The embedding layer.** nomic-embed-text and mxbai-embed-large locally via Ollama. OpenAI text-embedding-3-large for cloud work. Embedding 10k notes runs in about 5 minutes on an 8-core CPU. Chunking is almost always naive 500-to-1000-token windows with 100-token overlap. Semantic search plus keyword fallback is the common retrieval pattern.

**The generator layer.** Claude Opus 4.6 for reasoning and long synthesis. Claude Sonnet 4.6 for bulk operations. GPT-5 and GPT-5.5 Thinking for second-opinion cross-model review. Qwen 2.5 and Llama 3.2 for local-first work. Gemini 3.1 Pro for 1M-context synthesis when Claude is blocked.

**The connector layer.** MCP servers for Google Workspace, Zotero, Notion, Stata, GitHub. Read-and-draft-only scopes are common (Edgar has documented this for Gmail). Write permissions are requested sparingly and often rejected.

**The output layer.** Markdown as primary. Word with track changes for document deliverables (Edgar's 2026-04-20 voice-pass workflow is idiomatic). PDF via pandoc where possible, via Chrome headless --print-to-pdf where pandoc's pipeline is broken (Edgar's reference_pdf_generation_fallback note is a known workaround). LaTeX for formal academic writing remains outside most AI pipelines.

## 6. Governance and Voice

The craft problem.

**Disclosure.** Harvard requires it (FAS 2024). Stanford requires it when AI is allowed (GSB explicit). LSE expects it (Eden Centre framework). Oxford requires it when AI is explicitly permitted (Bodleian LibGuide). No top program ships a template. Students are writing their own. Claudia's ai-disclosure SOP with Edgar-to-grader template is a clean instance.

**Attribution.** APA and MLA now have AI-source citation formats as of 2024 updates. They are underused. The practitioner move is to disclose in a footer block plus cite specific AI generations as AI-generated where they appear verbatim.

**Voice preservation.** Five-move protocol that has stabilised across Kim Klassen, Enago, Thesify, the Transmitter, and Indisputably:

1. Draft first in your own voice.
2. Use the model as analyzer (reverse outline, devil's advocate, citation check) not writer.
3. If rewriting, feed samples of your own strong prose as style anchor.
4. Document what the model touched.
5. Disclose appropriately.

Edgar's rule inversion for AI-source prose (feedback_voice_pass_ai_source) is a refinement on this protocol that I did not find elsewhere. It is publishable.

**What separates careful from reckless.** Careful practice keeps the human in the critical loop for every claim that will ship under the student's name. Reckless practice delegates claims. The distinction is not about tool choice; it is about where the student places verification.

## 7. Where to Watch Next

Twelve to eighteen month horizon.

- **Standardised per-course disclosure templates** will emerge. Claudia's ai-disclosure SOP is a plausible template.
- **Local-model coursework in IRB-covered programs** will become mandatory in some disciplines (clinical psych, social work, public health).
- **Agent-based literature review will split into two camps**: vendor deep-research tools for discovery, general agents for synthesis. The Undermind-plus-Claude pattern will harden.
- **1M-context single-shot literature reviews** will become common for policy memos and comprehensive exams.
- **Overnight research loops** (ARIS-pattern) will leak from ML into human sciences. Expect first visible graduate-student instances within 12 months.
- **House-style voice profiles as shared institutional artefacts.** Journals, firms, and policy schools will start publishing voice specifications machine-readable by LLMs.
- **MCP for institutional LMS.** Canvas, Blackboard, Moodle integrations via MCP are obvious and not yet shipped. When they do, the student workflow collapses into a single orchestrated surface.

## 8. Open Questions and Research Gaps

What is not being documented yet and should be.

- **Policy-school practice.** HKS, SAIS, SIPA, Harris, LKY, GPS are nearly silent publicly. The case studies do not exist.
- **Ethnographic and anthropological practice.** The equity concerns make this hard, but the absence of documentation is itself a finding.
- **Longitudinal studies of voice drift.** Does sustained AI-editing erode author voice measurably over a two-year program? No study I could find addresses this.
- **Failure-mode taxonomies for agentic research.** What breaks when a five-agent orchestration fails? Aaron Tay's "shallow agency" piece is the closest to this, but the taxonomy is incomplete.
- **Cost-accounting for graduate-student AI usage.** The 200k-pricing-cliff reality (Edgar has documented this) is not in any published practitioner guide. Students are learning it the hard way.
- **Disclosure template library.** No shared resource exists. Someone should build one.

## 9. Annotated Source List

Ordered roughly by usefulness for a sophisticated reader.

- **Aaron Tay, "Deep Research, Shallow Agency" and "The agentic researcher," aarontay.substack.com.** Sharpest critical view of vendor deep-research tools. Singapore Management University librarian writing for practicing academics.
- **Humphries et al., "Unlocking the Archives," arXiv:2411.03340.** Benchmark paper on LLM transcription of handwritten historical documents. Reference for history OCR pipelines.
- **Boros et al., "Multimodal LLMs for OCR, OCR Post-Correction, and NER in Historical Documents," arXiv:2504.00414.** Companion to Humphries. End-to-end pipeline description.
- **Shen, Wu, Patt, Mendoza-Denton, "Understanding Graduate School Through AI: A Scalable Approach to Thematic Coding," Sage IJQM 2025.** The GATOS protocol paper. Reference for LLM-assisted thematic analysis.
- **Wang et al., "LATA: A Pilot Study on LLM-Assisted Thematic Analysis," CSCW 2025.** Second key thematic-analysis protocol. Design-oriented, more practitioner-facing than GATOS.
- **Jiang, Ko-Wong, Valdovinos Gutierrez, "Feasibility and Comparability of Using AI for Qualitative Data Analysis in Equity-Focused Research," Educational Researcher 2025.** The equity critique. Required reading before deploying GATOS or LATA on marginalised-group data.
- **Magesh et al., "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools," Stanford HAI (dho.stanford.edu).** 17 to 33 percent hallucination benchmark. Single most-cited paper in student-facing legal AI discussion.
- **Le Mens et al., "Positioning Political Texts with Large Language Models by Asking and Averaging," Political Analysis 2024.** Reference method paper for LLM-based positional coding of political text.
- **Halterman and Keith, "Codebook LLMs," Political Analysis 2025.** Evaluation of LLMs as measurement tools for political-science concepts.
- **letitbk/claude-academic-setup (GitHub).** Closest public analog to Claudia for social-science researchers. Worth forking and reading the skill definitions.
- **Imbad0202/academic-research-skills (GitHub).** Paper-drafting pipeline in Claude Code skills.
- **wanshuiyin/ARIS (GitHub).** Overnight autonomous research. Framework-free, Markdown-only.
- **hanlulong/stata-mcp and tmonk/stata-workbench (GitHub).** The two working Stata-MCP implementations. Essential for applied-stats students.
- **54yyyu/zotero-mcp and cookjohn/zotero-mcp (GitHub).** The two Zotero-MCP implementations. cookjohn is plugin-native, 54yyyu is external server.
- **kytmanov/obsidian-llm-wiki-local (GitHub).** Karpathy LLM Wiki pattern in executable form.
- **Kim Klassen, "How Can I Keep My Authentic Voice When Writing with AI?" kimklassen.com.** Clearest practitioner-facing voice-preservation protocol.
- **The Transmitter, "Keeping it personal: How to preserve your voice when using AI," thetransmitter.org.** Academic-voice-specific version of the same protocol. Neuroscience-flavored but generalises.
- **Thesify, "How to Preserve Your Academic Voice While Using AI Writing Tools," thesify.ai.** Graduate-writing-specific. Paired with their PhD AI policies guide.
- **Harvard FAS AI policy (fall 2024), via HGSE registrar (registrar.gse.harvard.edu/learning/policies-forms/ai-policy).** The policy reference for disclosure-as-plagiarism-shield.
- **Stanford GSB AI policy, via gradpilot.com/ai-policies/stanford-university.** The disclosure-on-take-home-allowed stance.
- **LSE Eden Centre, info.lse.ac.uk/staff/divisions/Eden-Centre/Artificial-Intelligence-Education-and-Assessment.** European flagship institutional framework.
- **Oxford Bodleian LibGuide on AI in academic work, libguides.bodleian.ox.ac.uk.** Permission-plus-declaration model.
- **Simon Willison's newsletter (simonw.substack.com) and simonwillison.net/tags/ai-assisted-programming.** The canonical source on agent-shaped LLM workflows for non-PhD researchers.
- **Joe Sabado, "The AI Knowledge System I Built for My Research and Leadership Work," joesabado.substack.com.** Personal Claude-plus-MCP academic-adjacent system. Good companion read to Claudia.
- **Andy Matuschak, notes.andymatuschak.org.** Reference for the spaced-repetition and note-taking research layer underneath all this.
- **Anthropic Claude 1M context announcement and documentation, code.claude.com/docs.** Technical reference for the 1M-context workflow frontier.

---

Generated for: Edgar Agunias
Date: 2026-04-24
Model: Claude Opus 4.7 (1M context)
Sources: Web search across GitHub, arXiv, Sage IJQM, Political Analysis, Educational Researcher, Stanford HAI, Substack (aarontay, simonw, joesabado, intelligenceandpower), university policy pages (Harvard FAS, Stanford GSB, LSE Eden Centre, Oxford Bodleian, UC Davis Mabie), Zotero forums, Obsidian forum. Cross-referenced against Claudia workspace memory (CLAUDE.md, feedback files, SOPs). No PDFs were read directly for this task; all citations are from web-retrievable sources.
Agent: Atlas
---
