"""Build three theory-reference PDFs for the GPCO 410 rationalist war bundle.

Follows _claudia/skills/theory-reference-pdf.md — one PDF per reading, with a
cover/TOC page plus one page per theory component. Each theory page has the
six-component structure: Situation, Core Intuition, Key Concepts, Assumptions,
Strengths/Weaknesses.
"""
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Colors and styles
# ---------------------------------------------------------------------------

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
ACCENT_GOLD = colors.HexColor("#C69C3F")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
WARM_AMBER = colors.HexColor("#FFF5E6")
TEXT = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#4B5563")

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=20, leading=24, textColor=DARK_NAVY, spaceAfter=4,
)
SUBTITLE_STYLE = ParagraphStyle(
    "SubtitleStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=13, textColor=MUTED, spaceAfter=6,
)
DESC_STYLE = ParagraphStyle(
    "DescStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.5, leading=12, textColor=TEXT, spaceAfter=4,
)
TOC_HEADER_STYLE = ParagraphStyle(
    "TOCHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=11, leading=14, textColor=DARK_NAVY, spaceBefore=10, spaceAfter=4,
)
TOC_ENTRY_STYLE = ParagraphStyle(
    "TOCEntry", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9, leading=12, textColor=MED_BLUE, spaceBefore=1, spaceAfter=1,
    leftIndent=12,
)
SECTION_LABEL = ParagraphStyle(
    "SectionLabel", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9, leading=11, textColor=DARK_NAVY, spaceBefore=6, spaceAfter=2,
)
BODY_STYLE = ParagraphStyle(
    "BodyStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9, leading=12, textColor=TEXT, spaceAfter=3,
)
BODY_SMALL = ParagraphStyle(
    "BodySmall", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.5, leading=11, textColor=TEXT, spaceAfter=2,
)
BULLET_STYLE = ParagraphStyle(
    "Bullet", parent=BODY_SMALL, leftIndent=10, bulletIndent=0, spaceAfter=2,
)
ATTRIBUTION_STYLE = ParagraphStyle(
    "Attribution", parent=styles["Normal"], fontName="Helvetica",
    fontSize=7, leading=9, textColor=MUTED, spaceBefore=2, spaceAfter=1,
)

# ---------------------------------------------------------------------------
# BookmarkAnchor flowable
# ---------------------------------------------------------------------------

class BookmarkAnchor(Flowable):
    def __init__(self, name, title=""):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0
        self._name = name
        self._title = title

    def draw(self):
        self.canv.bookmarkPage(
            self._name, fit="XYZ", left=0, top=self.canv._pagesize[1]
        )
        if self._title:
            self.canv.addOutlineEntry(self._title, self._name, level=0)


class HeaderBar(Flowable):
    """Colored header bar with class number, theory title, and citation."""
    def __init__(self, width, label, title, citation, color=DARK_NAVY, tag=None):
        Flowable.__init__(self)
        self.width = width
        self.height = 0.58 * inch
        self.label = label
        self.title = title
        self.citation = citation
        self.color = color
        self.tag = tag

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(10, self.height - 14, self.label.upper())
        c.setFont("Helvetica-Bold", 14)
        c.drawString(10, self.height - 32, self.title)
        c.setFillColor(colors.HexColor("#D5DEEC"))
        c.setFont("Helvetica-Oblique", 8.5)
        c.drawString(10, self.height - 48, self.citation)
        if self.tag:
            tag_w = c.stringWidth(self.tag, "Helvetica-Bold", 8) + 10
            c.setFillColor(ACCENT_GOLD)
            c.rect(self.width - tag_w - 8, self.height - 20, tag_w, 14,
                   fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(self.width - tag_w - 3, self.height - 16, self.tag)


# ---------------------------------------------------------------------------
# Theory data
# ---------------------------------------------------------------------------

COURSE_META = {
    "course": "GPCO 410 — International Politics & Security",
    "instructor": "Prof. Christina Praether",
    "institution": "UC San Diego — School of Global Policy and Strategy",
    "term": "Spring 2026",
}

# Each reading becomes its own PDF. Each reading has 1+ theory pages.
READINGS = [
    {
        "slug": "fearon_rationalist_explanations",
        "file_title": "Fearon — Rationalist Explanations for War",
        "doc_title": "Rationalist Explanations for War",
        "author_full": "James D. Fearon",
        "citation": "Fearon, J. D. (1995). Rationalist Explanations for War. International Organization, 49(3), 379–414.",
        "week": "Week 3 — Information & Commitment Problems",
        "description": (
            "Theory reference for Fearon's foundational 1995 article. Fearon asks why "
            "rational, unitary states ever fight when war is ex post inefficient — and "
            "identifies three mechanisms that can defeat bargaining: private information "
            "with incentives to misrepresent, commitment problems, and issue indivisibility. "
            "Use this PDF as exam-prep reference for the rationalist framework."
        ),
        "theories": [
            {
                "anchor": "fearon_puzzle",
                "label": "Fearon §1",
                "title": "The Bargaining Puzzle of War",
                "citation": "Fearon 1995, pp. 379–390",
                "color": DARK_NAVY,
                "tag": "CORE",
                "situation": (
                    "If the United States and Iraq in 2003 could have forecast the costs of invasion and occupation, both "
                    "would have preferred a negotiated settlement over the $2+ trillion war; the question is why that bargain "
                    "was unreachable."
                ),
                "intuition": (
                    "War is <b>costly and risky</b>, so for any distribution of power there must exist a set of ex ante bargains "
                    "both sides prefer to fighting. Fearon's central move is to treat war as a <b>bargaining failure</b>: the "
                    "puzzle is not why states want things, but why they cannot find the mutually-preferred deal that the "
                    "existence of war costs guarantees must exist. This reframes standard causes (anarchy, greed, misperception) "
                    "as incomplete — they explain conflict of interest, not the failure to settle it peacefully."
                ),
                "concepts": [
                    ("Bargaining range", "The set of settlements both states prefer to war given their expected costs and probability of victory; war costs guarantee this set is non-empty."),
                    ("Ex post inefficiency of war", "Whatever war settles could in principle have been settled without paying the fighting costs, leaving both sides better off."),
                    ("Ex ante bargain", "An agreement reached before fighting that divides the stakes in the shadow of war."),
                    ("Rationalist explanation", "An account of war consistent with states being unitary, rational, and cost-sensitive — not requiring irrationality or pathology."),
                    ("p − c framework", "A state's reservation value is roughly (probability of victory) × (stakes) − (costs); the bargaining range lies between the two sides' reservation values."),
                ],
                "assumptions": [
                    "States are unitary rational actors with coherent preferences over outcomes.",
                    "War is costly to both sides in expectation (not merely risky).",
                    "Issues are at least partly divisible into continuous bargains (money, territory, policy).",
                    "Leaders can credibly make and accept proposals (baseline bargaining capacity).",
                ],
                "strengths": [
                    "Reframes the question of war from 'causes of conflict' to 'causes of bargaining failure,' which is analytically sharper.",
                    "Provides a unified lens that evaluates other theories (misperception, anarchy, domestic politics) against a rational baseline.",
                    "Generates testable mechanisms — information, commitment, indivisibility — rather than unfalsifiable motives.",
                    "Survives as the field's default framework 30 years later; most subsequent IR security theory builds on or reacts to it.",
                ],
                "weaknesses": [
                    "Assumes unitary rational states, which masks bureaucratic politics, leader psychology, and principal-agent problems.",
                    "Treats war costs as common knowledge; if leaders systematically underestimate costs, the bargaining range may be illusory.",
                    "Has difficulty with identity-driven or existential conflicts where 'splitting the stakes' is morally inconceivable.",
                    "Mostly silent on civil war, terrorism, and mobilization dynamics that are not clean two-actor bargains.",
                ],
            },
            {
                "anchor": "fearon_information",
                "label": "Fearon §2",
                "title": "Private Information & Incentives to Misrepresent",
                "citation": "Fearon 1995, pp. 390–401",
                "color": MED_BLUE,
                "tag": "MECHANISM 1",
                "situation": (
                    "Saddam Hussein in 1990–91 appeared to genuinely believe the U.S. would not fight for Kuwait; the U.S. "
                    "had incentives to bluff resolve and Iraq had incentives to hide its true willingness to absorb costs — "
                    "a classic information-plus-misrepresentation breakdown."
                ),
                "intuition": (
                    "Even rational states may not reach a settlement because they hold <b>private information</b> about their "
                    "own capabilities, resolve, or costs, and they have <b>incentives to misrepresent</b> that information to "
                    "extract better terms. Cheap-talk signals are not credible; only <b>costly signals</b> (mobilization, "
                    "alliance commitments, audience costs) can transmit private information. When bluffing is tempting and "
                    "signals are expensive, negotiations can fail and the states discover their true relative strength only "
                    "by fighting."
                ),
                "concepts": [
                    ("Private information", "Information about capabilities or resolve known to one side but not credibly communicable to the other."),
                    ("Incentives to misrepresent", "The strategic gain from appearing stronger or more resolved than one actually is, to shift the bargain."),
                    ("Costly signaling", "Actions (mobilization, public threats, tying hands) whose cost is prohibitive for bluffers and therefore credible when taken."),
                    ("Audience costs", "Domestic political penalties leaders pay for backing down from public threats — a mechanism for generating credibility."),
                    ("Risk-return tradeoff", "Demanding more risks rejection and war; demanding less concedes surplus. Under uncertainty, some probability of war is optimal for the proposer."),
                    ("Screening / risky demand", "A proposer may optimally make a demand high enough that weak types reject — fighting becomes a consequence of rational screening."),
                ],
                "assumptions": [
                    "States have asymmetric information about capabilities or resolve.",
                    "Communicating that information truthfully is costly or infeasible.",
                    "Proposers cannot perfectly infer the target's type before making a demand.",
                    "Leaders weigh marginal bargaining gains against the marginal risk of war.",
                ],
                "strengths": [
                    "Explains why even fully rational, cost-minded states sometimes fight: screening and bluffing are equilibrium behavior.",
                    "Generates empirical predictions — costly signals should reduce war risk; cheap talk should not.",
                    "Ties crisis bargaining behavior (mobilization, audience costs, alliance treaties) to a clean theoretical logic.",
                    "Accommodates both deterrence successes (credible signal transmits info) and deterrence failures (signal was too cheap)."
                ],
                "weaknesses": [
                    "Requires leaders to understand the costly-signaling logic; many historical crises show leaders missing obvious signals.",
                    "Empirical measurement of 'private information' is hard; the theory can rationalize almost any war ex post.",
                    "Audience costs research (Snyder, Downes, Trachtenberg) has challenged whether democratic leaders really face them.",
                    "Does not explain wars that continue after private information has been revealed by initial combat.",
                ],
            },
            {
                "anchor": "fearon_commitment",
                "label": "Fearon §3",
                "title": "Commitment Problems",
                "citation": "Fearon 1995, pp. 401–409",
                "color": MED_BLUE,
                "tag": "MECHANISM 2",
                "situation": (
                    "A rising China and a declining United States may both prefer peace today, but the U.S. cannot trust that "
                    "a future China will honor current concessions once the power shift is complete — creating an incentive "
                    "for preventive action now."
                ),
                "intuition": (
                    "Some situations have bargains both sides prefer to war today, but at least one side <b>cannot credibly "
                    "commit</b> to honor that bargain tomorrow. If power is shifting, if a concession would make the conceding "
                    "side militarily vulnerable, or if an indivisible asset (a choke point, a nuclear program) would alter "
                    "future bargaining positions, the rising or favored side cannot promise to forgo the future gains, and "
                    "the declining side prefers to fight now rather than face worse terms later. Unlike information problems, "
                    "commitment problems persist even under <b>complete information</b>."
                ),
                "concepts": [
                    ("Credible commitment", "The ability to bind one's future self to honor a present promise; typically requires external enforcement or structural constraint."),
                    ("Preventive war", "War initiated now by a declining power to block an adversary's future rise to greater strength."),
                    ("Power shift", "An exogenous or endogenous change in the relative military or economic capability of two states over time."),
                    ("First-strike advantage", "A structural feature where striking first yields a decisive gain, making defensive mobilization itself a trigger for war."),
                    ("Bargaining in the shadow of power change", "Settlements today must account for how future distributions of power will tempt deviation from those settlements."),
                ],
                "assumptions": [
                    "States cannot sign and enforce contracts across time (no world government).",
                    "Relative power changes meaningfully over relevant time horizons.",
                    "Concessions today alter the military balance tomorrow (concessions are not purely fungible).",
                    "Leaders have long time horizons and value future payoffs.",
                ],
                "strengths": [
                    "Explains preventive wars and power-transition conflicts without needing irrationality or misperception.",
                    "Operates even under complete information — closes the gap the information mechanism leaves open.",
                    "Powell (2006) extends this into a general theory that reframes most 'inefficient' war as commitment failure.",
                    "Generates testable predictions: wars should cluster around rapid power shifts and first-strike-advantaged technologies.",
                ],
                "weaknesses": [
                    "Power shifts are often gradual and observable; why fight now rather than renegotiate at each step?",
                    "Predicts more preventive war than the historical record shows; democracies especially rarely attack preventively.",
                    "Assumes away institutional or reputational mechanisms that could sustain commitment (alliances, IOs, nuclear deterrence).",
                    "Difficult to distinguish ex ante from information problems; many cases involve both.",
                ],
            },
            {
                "anchor": "fearon_indivisibility",
                "label": "Fearon §4",
                "title": "Issue Indivisibility",
                "citation": "Fearon 1995, pp. 381–382, 389–390",
                "color": DARK_NAVY,
                "tag": "MECHANISM 3",
                "situation": (
                    "Jerusalem's Temple Mount or Kosovo's sovereignty present as indivisible in the eyes of the contestants — "
                    "there is no fractional bargain both sides will accept because the stake cannot be physically or symbolically split."
                ),
                "intuition": (
                    "If the object of dispute is <b>genuinely indivisible</b>, the bargaining range may be empty: no proposal "
                    "strictly between the two reservation values exists. Fearon treats this mechanism cautiously — most "
                    "supposedly indivisible issues (territory, sovereignty) can in practice be divided via side-payments, "
                    "power-sharing, lotteries, or rotational arrangements. He argues true indivisibility is <b>rare as an "
                    "empirical cause of war</b>, and that when indivisibility does drive conflict it usually traces back to "
                    "domestic-political or identity mechanisms that make division politically impossible, not physically impossible."
                ),
                "concepts": [
                    ("Indivisible good", "An asset that cannot be partitioned or shared without destroying its value (symbolic, sacred, or structurally unitary)."),
                    ("Side-payments", "Transfers in money, policy, or territory that can substitute for direct division of the disputed good."),
                    ("Lottery / randomization", "Probabilistic assignment of the whole good, which in expectation divides its value between claimants."),
                    ("Constructed indivisibility", "Indivisibility that is politically or symbolically manufactured (by domestic audiences, religious claims, identity politics) rather than inherent."),
                ],
                "assumptions": [
                    "The disputed good truly admits no fractional division or acceptable substitute.",
                    "Side-payments and lotteries are unavailable or unacceptable to the parties.",
                    "Domestic actors cannot be compensated for accepting a partial outcome.",
                ],
                "strengths": [
                    "Provides a theoretically clean third mechanism that closes the taxonomy of bargaining failure.",
                    "Useful lens for ethno-religious and sovereignty conflicts where symbolic stakes dominate.",
                    "Forces analysts to ask why division is unavailable, often revealing the real (domestic-political) mechanism.",
                ],
                "weaknesses": [
                    "Fearon himself treats this as the weakest of the three mechanisms — most indivisibilities dissolve under side-payments.",
                    "When it does explain cases, it typically reduces to a domestic-politics or identity theory in disguise.",
                    "Hard to operationalize empirically; 'indivisible' is often what losers call a concession they did not want to make.",
                    "Offers little predictive traction: cannot forecast which issues will become indivisible ex ante.",
                ],
            },
        ],
    },
    {
        "slug": "powell_commitment",
        "file_title": "Powell — War as a Commitment Problem",
        "doc_title": "War as a Commitment Problem",
        "author_full": "Robert Powell",
        "citation": "Powell, R. (2006). War as a Commitment Problem. International Organization, 60(1), 169–203.",
        "week": "Week 3 — Information & Commitment Problems",
        "description": (
            "Theory reference for Powell's 2006 article, which argues that most cases previously coded as bargaining failures "
            "due to information or indivisibility are better understood as commitment problems driven by large, rapid shifts "
            "in the distribution of power. Powell unifies preventive war, bargaining over power itself, and first-strike "
            "advantage under a single mechanism: the inability to commit across a shifting balance."
        ),
        "theories": [
            {
                "anchor": "powell_unification",
                "label": "Powell §1",
                "title": "Commitment Problems as the Master Mechanism",
                "citation": "Powell 2006, pp. 169–178",
                "color": DARK_NAVY,
                "tag": "CORE",
                "situation": (
                    "The U.S. decision to invade Iraq in 2003 is frequently explained as intelligence failure (information); "
                    "Powell would reframe it as a commitment problem: even if WMD claims were known false, Washington could "
                    "not trust Saddam's future commitments once sanctions eroded and regional power shifted."
                ),
                "intuition": (
                    "Powell argues that <b>information asymmetries and indivisibilities are not sufficient</b> to produce war "
                    "on their own — rational actors can usually resolve these through signaling or side-payments. What "
                    "actually prevents bargaining is the <b>inability to commit</b> to future behavior when the distribution "
                    "of power will change. In a dynamic bargaining model with <b>large, rapid shifts in power</b>, the rising "
                    "state cannot credibly promise to accept today's division once it has grown stronger, and the declining "
                    "state prefers to fight now rather than accept worse terms later. This single mechanism subsumes "
                    "preventive war, bargaining over strategic resources, and first-strike advantages."
                ),
                "concepts": [
                    ("Commitment problem", "A dynamic inefficiency: a bargain both sides prefer today cannot be reached because one side will want to renege once circumstances change."),
                    ("Dynamic inconsistency", "Preferences that are consistent at any single moment but inconsistent across time as the power balance shifts."),
                    ("Large, rapid shift in power", "The crucial scope condition — commitment failure produces war only when the shift is too fast or too steep for gradual renegotiation to absorb."),
                    ("Bargaining over the distribution of power itself", "When the stake of the dispute (territory, weapons, sanctions relief) directly alters future bargaining power, not just current payoffs."),
                    ("Inefficiency puzzle", "Powell's framing: why rational actors burn surplus by fighting when a mutually-preferred bargain exists in the static game."),
                    ("Subgame perfection", "Equilibrium concept requiring credible play at every decision node; commitment problems violate this by making future compliance non-credible."),
                ],
                "assumptions": [
                    "Actors are rational, forward-looking, and weigh future payoffs meaningfully.",
                    "No third party can enforce intertemporal contracts between states.",
                    "The distribution of power can shift significantly and at least partly endogenously with bargaining outcomes.",
                    "Concessions today (territory, weapons capability, strategic terrain) feed back into tomorrow's bargaining leverage.",
                ],
                "strengths": [
                    "Provides a unified theoretical core that generates preventive war, power-transition war, and first-strike dynamics from one mechanism.",
                    "Sharpens Fearon's taxonomy by showing indivisibility and some information cases are really commitment problems in disguise.",
                    "Matches key stylized facts: wars cluster around rapid power shifts (rising Germany, rising China concerns, nuclear proliferation decisions).",
                    "Formally rigorous — derives results from an infinite-horizon bargaining model with clean comparative statics.",
                ],
                "weaknesses": [
                    "Requires 'large and rapid' shifts — most real-world shifts are gradual, suggesting the mechanism explains fewer wars than advertised.",
                    "Empirical identification is hard: most observed wars involve information and commitment together.",
                    "Understates how institutions, alliances, and nuclear deterrence can sustain commitment in practice.",
                    "Less applicable to asymmetric or non-state conflicts where the bargaining-over-power frame is strained.",
                ],
            },
            {
                "anchor": "powell_preventive",
                "label": "Powell §2",
                "title": "Preventive War and Bargaining Over Power",
                "citation": "Powell 2006, pp. 178–195",
                "color": MED_BLUE,
                "tag": "APPLICATION",
                "situation": (
                    "Israel's 1981 Osirak strike against Iraq's reactor illustrates bargaining over the distribution of power "
                    "itself: a nuclear-armed Iraq would shift the regional balance so decisively that Israel preferred to pay "
                    "the cost of a preventive strike rather than negotiate with a future nuclear Iraq."
                ),
                "intuition": (
                    "When a state can acquire a <b>capability that itself changes the bargaining balance</b> — nuclear weapons, "
                    "strategic territory, military technology — current bargaining cannot address the problem by simple "
                    "transfers. The declining side cannot 'buy off' the rising side, because any concession either accelerates "
                    "the shift or leaves the declining side worse off later. Preventive war becomes rational: <b>the cost of "
                    "fighting now</b> is lower than the <b>expected cost of a worsened bargain later</b>. This logic holds "
                    "under complete information and even with perfectly divisible stakes."
                ),
                "concepts": [
                    ("Preventive logic", "Fight now to avoid facing a stronger adversary later, even when current war is costly."),
                    ("Power-shifting asset", "A stake (nukes, territory, chokepoint) whose acquisition changes the future bargaining range, not just current payoffs."),
                    ("Non-fungibility of concessions", "Some concessions cannot be cleanly compensated because they endogenously change future power."),
                    ("Shadow of the future", "How today's bargain is shaped by anticipation of tomorrow's balance; in Powell, this shadow is what drives the inefficiency."),
                    ("Window of opportunity", "A temporary relative-power advantage that closes as the rising state grows; fighting occurs during the window's narrow span."),
                ],
                "assumptions": [
                    "The rising state's capability gain is genuinely threatening to the declining state's core interests.",
                    "No side-payment package can substitute for blocking the capability (or the rising state rejects all such packages).",
                    "The declining state still has a military advantage window wide enough to fight effectively.",
                    "Third-party enforcement (treaties, sanctions) cannot lock in the current balance.",
                ],
                "strengths": [
                    "Explains preventive attacks against nuclear programs (Osirak, Israeli strikes in Syria, U.S. debates on Iran/North Korea).",
                    "Clarifies why sanctions and arms-control regimes often precede military action — states are searching for a commitment technology.",
                    "Links nicely to rising-China literature and debates about a U.S.–China Thucydides trap.",
                    "Formalizes intuitions that had been loose in the power-transition literature (Organski, Gilpin) with clean equilibrium logic.",
                ],
                "weaknesses": [
                    "Preventive war is historically rare — the mechanism predicts more of it than we observe, especially among democracies.",
                    "Cannot explain why some rising-power dynamics produce war (Germany 1914) and others do not (U.S. rise over Britain).",
                    "Assumes the declining state can identify the shift early and act decisively, which is empirically uneven.",
                    "Underweights reputational and domestic-political constraints on striking first.",
                ],
            },
            {
                "anchor": "powell_firststrike",
                "label": "Powell §3",
                "title": "First-Strike Advantage as Commitment Failure",
                "citation": "Powell 2006, pp. 195–201",
                "color": MED_BLUE,
                "tag": "APPLICATION",
                "situation": (
                    "European mobilization schedules in July 1914 gave a decisive advantage to whichever side mobilized first; "
                    "every major power feared that declining to mobilize would concede the military balance, so all mobilized "
                    "simultaneously and war became unavoidable — a textbook first-strike / commitment spiral."
                ),
                "intuition": (
                    "When military technology or doctrine gives <b>the side that strikes first</b> a decisive advantage, "
                    "neither state can credibly commit to refrain from attacking during a crisis. Even if both strictly prefer "
                    "peace, each knows the other has an incentive to preempt, which itself becomes a reason to preempt. The "
                    "peaceful bargain is not self-enforcing because a tiny deviation toward attack is rewarded. Powell shows "
                    "this is formally equivalent to a commitment problem over the distribution of power — the 'power' in "
                    "question is simply who moves first."
                ),
                "concepts": [
                    ("First-strike advantage", "Technology or doctrine that rewards attacking first relative to defending or waiting."),
                    ("Security dilemma (strategic interaction version)", "Defensive measures appear offensive to the other side, creating a spiral of mutual preemption incentives."),
                    ("Preemption", "Striking first in anticipation of an imminent attack, rational when the adversary's attack is believed to be coming."),
                    ("Crisis instability", "A state of affairs where bargaining equilibria are not robust to small moves toward military action."),
                    ("Offense-defense balance", "The relative ease of offensive vs. defensive operations given technology, geography, and doctrine; offense-dominance breeds first-strike problems."),
                ],
                "assumptions": [
                    "Moving first confers a decisive and non-compensable battlefield advantage.",
                    "Peaceful settlement requires both sides to refrain from attack indefinitely.",
                    "Neither side has a costless way to verify the other's restraint.",
                    "Small moves toward mobilization cannot be de-escalated without loss of advantage.",
                ],
                "strengths": [
                    "Unifies 1914-style mobilization spirals and Cold War nuclear first-strike concerns under one formal logic.",
                    "Explains why arms-control regimes focus so much on reducing offense-dominance (SALT, INF, de-MIRVing).",
                    "Shows security-dilemma dynamics are a special case of commitment failure, not a separate theory.",
                    "Generates policy-relevant predictions: secure second-strike capability should stabilize bargaining.",
                ],
                "weaknesses": [
                    "Depends on measuring offense-defense balance, which empirical work (Lieber, Glaser) shows is slippery.",
                    "Modern conventional and nuclear forces often favor defense and second-strike, limiting the mechanism's scope.",
                    "Does not explain restraint in many offense-dominant situations (post-1945 crises).",
                    "Assumes crisis dynamics are decoupled from domestic-political constraints on preemption.",
                ],
            },
        ],
    },
    {
        "slug": "morrow_strategic_setting",
        "file_title": "Morrow — The Strategic Setting of Choices",
        "doc_title": "The Strategic Setting of Choices",
        "author_full": "James D. Morrow",
        "citation": "Morrow, J. D. (1999). The Strategic Setting of Choices: Signaling, Commitment, and Negotiation in International Politics. In D. A. Lake & R. Powell (Eds.), Strategic Choice and International Relations (pp. 77–114). Princeton University Press.",
        "week": "Week 3 — Information & Commitment Problems (foundational reading)",
        "description": (
            "Theory reference for Morrow's chapter, which supplies the formal-theory toolkit underlying Fearon and Powell. "
            "Morrow lays out how signaling, commitment, and negotiation work as strategic settings — not just as substantive "
            "problems of war. Treat this PDF as the grammar behind the rationalist bundle: it defines the concepts Fearon "
            "and Powell apply."
        ),
        "theories": [
            {
                "anchor": "morrow_strategic_choice",
                "label": "Morrow §1",
                "title": "The Strategic Choice Framework",
                "citation": "Morrow 1999, pp. 77–85",
                "color": DARK_NAVY,
                "tag": "FOUNDATION",
                "situation": (
                    "When analysts ask whether U.S.–China competition is driven by 'structural' pressures or 'leader' choices, "
                    "Morrow's framework insists the answer is always both — actors choose within a structure, and the structure "
                    "is itself the aggregated product of past choices."
                ),
                "intuition": (
                    "Morrow argues international politics should be analyzed as a sequence of <b>strategic choices made by "
                    "purposive actors within strategic settings</b>. The framework separates three layers: <b>actors</b> "
                    "(with preferences and beliefs), <b>actions</b> (what choices are available), and <b>settings</b> (the "
                    "structure of interaction — who moves when, what is known to whom, what payoffs follow). Most IR "
                    "theoretical disagreements, he argues, are actually disagreements about the setting: what looks like a "
                    "debate about 'human nature' is usually a debate about information, sequencing, or enforcement."
                ),
                "concepts": [
                    ("Strategic setting", "The structure of an interaction: the players, their available actions, information conditions, and payoff consequences of action combinations."),
                    ("Strategic choice", "A decision made with awareness that other actors are also choosing, and that their choices depend on one's own."),
                    ("Actors, actions, settings", "Morrow's three analytic layers; clean IR theory specifies each explicitly rather than conflating them."),
                    ("Common knowledge", "Information known to all players and known to be known by all players — a strong condition that underlies many equilibrium claims."),
                    ("Equilibrium", "A profile of strategies in which no player can improve their payoff by unilaterally deviating, given others' strategies."),
                    ("Reduced-form modeling", "Simplifying complex political reality to the strategic core that matters for the predicted outcome."),
                ],
                "assumptions": [
                    "Actors are purposive — they choose to pursue preferences, even if preferences are shaped by structure.",
                    "The relevant strategic structure can be specified with enough precision to permit equilibrium analysis.",
                    "Players understand they are in a strategic interaction (not just parametric decision-making).",
                    "Analysts can ex ante identify the correct level of abstraction for a given question.",
                ],
                "strengths": [
                    "Gives IR a common analytical language that bridges realism, liberalism, and constructivism at the level of mechanism.",
                    "Clarifies that 'structure vs. agency' debates are usually about where to locate the strategic setting.",
                    "Underwrites both Fearon and Powell: their models are applications of Morrow's framework to war.",
                    "Forces theoretical precision about what is being assumed (preferences, information, sequencing).",
                ],
                "weaknesses": [
                    "Rests on a rational-choice foundation many IR scholars reject (constructivists, some liberals).",
                    "Equilibrium-based prediction requires strong informational assumptions that rarely hold empirically.",
                    "Can obscure preference formation by taking preferences as given exogenously.",
                    "Pushes some substantive questions (identity, ideology) into 'preferences' where the theory has little to say.",
                ],
            },
            {
                "anchor": "morrow_signaling",
                "label": "Morrow §2",
                "title": "Signaling and Private Information",
                "citation": "Morrow 1999, pp. 85–95",
                "color": MED_BLUE,
                "tag": "TOOLKIT",
                "situation": (
                    "When NATO publicly moves troops to Poland's eastern flank, it is not just defending territory — it is "
                    "paying a cost that a non-resolved state would not pay, thereby signaling to Russia that the alliance "
                    "would absorb further costs to defend Article 5."
                ),
                "intuition": (
                    "A <b>signal</b> is an observable action that transmits information about an actor's unobservable type "
                    "(capability, resolve, preferences). For a signal to be informative, it must be <b>costly in a way that "
                    "distinguishes types</b> — specifically, the signal must be cheaper for one type than for another. "
                    "<b>Cheap talk</b> (unsubstantiated verbal claims) is uninformative in equilibrium because bluffers would "
                    "imitate it costlessly. <b>Separating equilibria</b> occur when different types take different actions, "
                    "so observers can infer the type; <b>pooling equilibria</b> occur when all types take the same action "
                    "and no information is revealed."
                ),
                "concepts": [
                    ("Type", "A hidden characteristic of an actor that others cannot directly observe (capability, resolve, preferences)."),
                    ("Signal", "An observable action that may reveal information about the sender's type."),
                    ("Costly signaling", "A signal whose cost differs across types, such that only certain types find it worth sending."),
                    ("Cheap talk", "Costless communication; uninformative in equilibrium when incentives to misrepresent exist."),
                    ("Separating equilibrium", "Outcome where different types choose different signals and observers can infer type from signal."),
                    ("Pooling equilibrium", "Outcome where all types choose the same signal, so observers learn nothing from the signal itself."),
                    ("Audience costs", "Domestic political penalties that raise the cost of backing down from public commitments, making public threats more credible."),
                ],
                "assumptions": [
                    "There is genuine private information — asymmetry of what the sender knows vs. the receiver.",
                    "Signal costs are structured so they bite asymmetrically across types.",
                    "Receivers update beliefs using Bayes' rule (or a close cognitive approximation).",
                    "Senders anticipate how their signals will be interpreted and choose strategically.",
                ],
                "strengths": [
                    "Provides microfoundations for why crisis bargaining, alliances, and arms races look the way they do.",
                    "Explains puzzles like why states publicly commit rather than negotiate privately (audience-cost logic).",
                    "Integrates cleanly with Fearon's 'incentives to misrepresent' mechanism for war.",
                    "Supports strong empirical work on reputation, commitment devices, and crisis escalation.",
                ],
                "weaknesses": [
                    "Relies on Bayesian updating, which empirical decision-makers often violate.",
                    "Many 'audience cost' predictions have not held up in survey and historical research (Snyder, Downes, Trachtenberg).",
                    "Pooling equilibria are theoretically common but leave the theory with little predictive bite in those cases.",
                    "Signal costs are hard to measure, leaving room for ad hoc interpretation.",
                ],
            },
            {
                "anchor": "morrow_commitment",
                "label": "Morrow §3",
                "title": "Commitment and Credible Promises",
                "citation": "Morrow 1999, pp. 95–104",
                "color": MED_BLUE,
                "tag": "TOOLKIT",
                "situation": (
                    "A peace deal between a sitting government and rebel forces routinely unravels because neither side can "
                    "credibly promise to refrain from exploiting the other's disarmament — the classic Walter (1997) "
                    "civil-war commitment problem, built on Morrow's framework."
                ),
                "intuition": (
                    "A <b>commitment</b> is a binding on one's own future behavior. Credible commitment is hard because "
                    "rational actors will re-optimize as circumstances change, breaking promises that were sincere when "
                    "made. Morrow catalogs <b>commitment technologies</b> that make promises credible: tying one's hands "
                    "(audience costs, sunk investments), delegation to third parties (international institutions), "
                    "reputation building (repeated interaction), and structural changes (alliances, treaties, constitutional "
                    "design). Where no such technology is available, bargains break down even with complete information and "
                    "divisible stakes."
                ),
                "concepts": [
                    ("Commitment", "A binding constraint on one's own future action that survives the temptation to deviate."),
                    ("Tying hands", "Actions taken now that raise the cost of future deviation (audience costs, sunk costs, public declarations)."),
                    ("Delegation", "Handing a decision to a third party whose incentives differ from one's own, creating an external enforcer."),
                    ("Reputation", "A record of past behavior used by others to predict future behavior, valuable when repeated interaction is expected."),
                    ("Time inconsistency", "A situation where an actor's optimal plan changes between the time of promising and the time of action, even without new information."),
                    ("Self-enforcing agreement", "A bargain that neither side has incentive to break once it is in place, requiring no external enforcement."),
                ],
                "assumptions": [
                    "Actors have stable preferences that allow comparison across time.",
                    "Third parties exist who can enforce agreements or to whom decisions can be delegated.",
                    "Repeated interaction or observable behavior is possible (for reputation to bite).",
                    "Commitment technologies have differential availability — not every actor can access every device.",
                ],
                "strengths": [
                    "Explains why institutions, alliances, and constitutions exist — they are commitment technologies.",
                    "Provides the formal backbone for Powell's later unification of war under commitment problems.",
                    "Generates cross-issue predictions (trade, arms control, civil-war settlements, monetary policy).",
                    "Clarifies when a promise is and is not credible, cutting through rhetoric about 'intentions.'",
                ],
                "weaknesses": [
                    "Many commitment devices are endogenous — you cannot assume them into existence where power asymmetry blocks them.",
                    "Overstates the availability of credible third parties; 'international institutions' often lack enforcement teeth.",
                    "Reputation effects are empirically weaker than the theory predicts (Mercer, Press).",
                    "Some actors genuinely change preferences, which the theory handles awkwardly as 'new information about type.'",
                ],
            },
            {
                "anchor": "morrow_negotiation",
                "label": "Morrow §4",
                "title": "Negotiation and Bargaining Structure",
                "citation": "Morrow 1999, pp. 104–114",
                "color": DARK_NAVY,
                "tag": "TOOLKIT",
                "situation": (
                    "In WTO trade negotiations, the sequence of offers, who holds outside options, and the deadline structure "
                    "determine which member gets the surplus — two members with identical preferences can reach very different "
                    "outcomes depending purely on bargaining structure."
                ),
                "intuition": (
                    "Negotiation outcomes are determined not just by preferences and power but by the <b>structure of "
                    "bargaining itself</b>: who makes offers, in what order, under what deadlines, with what outside options, "
                    "and under what information conditions. Morrow walks through the <b>Rubinstein alternating-offers model</b> "
                    "and its variants to show how small changes in structure produce large changes in predicted division. "
                    "This matters for war because crisis bargaining is a structured negotiation — the structure of signaling "
                    "and commitment discussed earlier is the <b>setting</b> within which proposals and counterproposals unfold."
                ),
                "concepts": [
                    ("Bargaining structure", "The rules of interaction: offer order, deadlines, information flows, outside options."),
                    ("Rubinstein bargaining", "A canonical model of alternating offers with discounting, yielding a unique subgame-perfect division dependent on patience and who moves first."),
                    ("Outside option / BATNA", "The payoff a party secures by walking away from the negotiation (Best Alternative to a Negotiated Agreement)."),
                    ("Discount factor", "How much future payoffs are weighted relative to present ones; more patient actors extract more in bargaining."),
                    ("Deadline effects", "Time constraints shift bargaining power toward the less time-sensitive side; last-minute deals reflect deadline-driven concessions."),
                    ("Nash bargaining solution", "A cooperative-game prediction that parties split surplus proportional to their bargaining power and outside options."),
                ],
                "assumptions": [
                    "Both parties recognize they are in a structured bargaining setting with definable rules.",
                    "Preferences, discount factors, and outside options are sufficiently stable over the negotiation horizon.",
                    "Offers and responses are observable and mutually understood.",
                    "The bargaining structure itself is not costlessly renegotiable mid-negotiation.",
                ],
                "strengths": [
                    "Generates clean, formally derived predictions about division and timing in crisis bargaining.",
                    "Integrates cleanly with Fearon's war model: war is the failure of the bargaining process, not an alternative to it.",
                    "Explains why bargaining structure is often itself contested (who hosts talks, who moves first, what the deadline is).",
                    "Applies to any negotiation domain — crisis bargaining, trade talks, alliance formation, civil-war settlements.",
                ],
                "weaknesses": [
                    "Equilibrium predictions depend sensitively on assumed structure — changing offer protocols changes outcomes.",
                    "Ignores emotional, reputational, and symbolic dynamics that empirically drive many negotiations.",
                    "Rubinstein-style models assume exogenous structure, while real negotiators contest the structure itself.",
                    "Cannot straightforwardly handle multilateral bargaining beyond very small numbers of players.",
                ],
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Page construction
# ---------------------------------------------------------------------------

PAGE_W, PAGE_H = letter
MARGIN = 0.55 * inch
FRAME_W = PAGE_W - 2 * MARGIN
FRAME_H = PAGE_H - 2 * MARGIN


def make_footer(title):
    def footer(canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 7)
        canv.setFillColor(MUTED)
        canv.setStrokeColor(BORDER_GREY)
        canv.setLineWidth(0.3)
        canv.line(MARGIN, 0.45 * inch, PAGE_W - MARGIN, 0.45 * inch)
        canv.drawString(MARGIN, 0.3 * inch, title)
        canv.drawRightString(PAGE_W - MARGIN, 0.3 * inch, f"p. {doc.page}")
        canv.restoreState()
    return footer


def build_cover_story(reading):
    story = []
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(reading["doc_title"], TITLE_STYLE))
    story.append(Paragraph(
        f"{reading['author_full']} &nbsp;·&nbsp; {reading['week']}",
        SUBTITLE_STYLE,
    ))
    story.append(Paragraph(
        f"{COURSE_META['course']} &nbsp;·&nbsp; {COURSE_META['instructor']}<br/>"
        f"{COURSE_META['institution']} &nbsp;·&nbsp; {COURSE_META['term']}",
        SUBTITLE_STYLE,
    ))

    # Description box
    desc_tbl = Table(
        [[Paragraph(reading["description"], DESC_STYLE)]],
        colWidths=[FRAME_W],
    )
    desc_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(desc_tbl)
    story.append(Spacer(1, 0.08 * inch))

    # Citation
    cite_style = ParagraphStyle(
        "Cite", parent=DESC_STYLE, fontName="Helvetica-Oblique",
        fontSize=8, textColor=MUTED,
    )
    story.append(Paragraph(f"<b>Source:</b> {reading['citation']}", cite_style))

    # TOC
    story.append(Paragraph("Contents", TOC_HEADER_STYLE))
    for t in reading["theories"]:
        toc_text = (
            f'<a href="#{t["anchor"]}" color="#2C5282">'
            f'<b>{t["label"]}</b> — {t["title"]} '
            f'<font color="#4B5563">({t["citation"]})</font></a>'
        )
        story.append(Paragraph(toc_text, TOC_ENTRY_STYLE))

    # Attribution footnote
    story.append(Spacer(1, 0.15 * inch))
    story.append(HRFlowable(
        width="35%", thickness=0.4, color=BORDER_GREY, hAlign="LEFT",
        spaceBefore=2, spaceAfter=4,
    ))
    today = date.today().isoformat()
    attribution = (
        f"Generated by Atlas (Claude Opus 4.6) on {today} for Edgar Agunias. "
        f"{COURSE_META['course']} · {COURSE_META['instructor']} · {COURSE_META['institution']}. "
        f"Primary source: {reading['citation']}. "
        f"Always verify against official course materials and the assigned text. "
        f"This document is a study aid and does not substitute for careful reading of the original."
    )
    story.append(Paragraph(attribution, ATTRIBUTION_STYLE))
    return story


def build_theory_page(theory):
    story = []
    story.append(BookmarkAnchor(theory["anchor"], f"{theory['label']} — {theory['title']}"))
    story.append(HeaderBar(
        FRAME_W, theory["label"], theory["title"],
        theory["citation"], color=theory.get("color", DARK_NAVY),
        tag=theory.get("tag"),
    ))
    story.append(Spacer(1, 0.12 * inch))

    story.append(Paragraph("SITUATION", SECTION_LABEL))
    story.append(Paragraph(theory["situation"], BODY_STYLE))

    story.append(Paragraph("CORE INTUITION", SECTION_LABEL))
    story.append(Paragraph(theory["intuition"], BODY_STYLE))

    story.append(Paragraph("KEY CONCEPTS, KEYWORDS &amp; TERMINOLOGY", SECTION_LABEL))
    for term, defn in theory["concepts"]:
        story.append(Paragraph(
            f"<b>{term}</b> — {defn}", BULLET_STYLE, bulletText="•",
        ))

    story.append(Paragraph("ASSUMPTIONS", SECTION_LABEL))
    for a in theory["assumptions"]:
        story.append(Paragraph(a, BULLET_STYLE, bulletText="•"))

    # Strengths / Weaknesses two-column
    story.append(Paragraph("STRENGTHS &amp; WEAKNESSES", SECTION_LABEL))
    s_items = [Paragraph(f"• {s}", BODY_SMALL) for s in theory["strengths"]]
    w_items = [Paragraph(f"• {w}", BODY_SMALL) for w in theory["weaknesses"]]
    n = max(len(s_items), len(w_items))
    while len(s_items) < n:
        s_items.append(Paragraph("", BODY_SMALL))
    while len(w_items) < n:
        w_items.append(Paragraph("", BODY_SMALL))

    header_row = [
        Paragraph("<b>Strengths</b>", BODY_SMALL),
        Paragraph("<b>Weaknesses</b>", BODY_SMALL),
    ]
    body_rows = [[s_items[i], w_items[i]] for i in range(n)]
    tbl_data = [header_row] + body_rows
    col_w = (FRAME_W - 6) / 2
    tbl = Table(tbl_data, colWidths=[col_w, col_w])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
        ("BACKGROUND", (1, 0), (1, 0), WARM_AMBER),
        ("LINEAFTER", (0, 0), (0, -1), 0.4, BORDER_GREY),
        ("BOX", (0, 0), (-1, -1), 0.3, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tbl)
    return story


def build_pdf(reading, out_path):
    doc = BaseDocTemplate(
        str(out_path),
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title=reading["doc_title"],
        author="Atlas (Claude Opus 4.6) for Edgar Agunias",
    )
    frame = Frame(MARGIN, MARGIN, FRAME_W, FRAME_H,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    footer = make_footer(f"{reading['doc_title']} — Theory Reference")
    template = PageTemplate(id="main", frames=[frame], onPage=footer)
    doc.addPageTemplates([template])

    story = []
    story.extend(build_cover_story(reading))
    for theory in reading["theories"]:
        story.append(PageBreak())
        story.extend(build_theory_page(theory))
    doc.build(story)


def main():
    out_dir = Path(__file__).parent
    paths = []
    for reading in READINGS:
        out_path = out_dir / f"{reading['file_title']}.pdf"
        build_pdf(reading, out_path)
        paths.append(out_path)
        print(f"Built: {out_path}")
    return paths


if __name__ == "__main__":
    main()
