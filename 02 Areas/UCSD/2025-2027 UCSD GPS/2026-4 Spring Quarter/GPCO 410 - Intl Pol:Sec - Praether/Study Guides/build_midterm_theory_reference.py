from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
OUT = BASE_DIR / "GPCO410_Midterm_Theory_Reference_v1.3.1.pdf"
TITLE = "GPCO 410 Midterm Theory Reference"
COURSE = "GPCO 410 International Politics & Security"
DATE = "2026-04-30"
MODEL = "GPT-5 (Codex, medium reasoning)"
ASSET_DIR = BASE_DIR / "assets" / "GPCO410_Midterm_Theory_Reference_v1.3.0"
ASSET_DISPLAY_DIR = "Study Guides/assets/GPCO410_Midterm_Theory_Reference_v1.3.0"

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
ACCENT_GOLD = colors.HexColor("#C69C3F")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
WARM_AMBER = colors.HexColor("#FFF5E6")


class BookmarkAnchor(Flowable):
    def __init__(self, name, title=""):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0
        self._name = name
        self._title = title

    def draw(self):
        self.canv.bookmarkPage(self._name, fit="XYZ", left=0, top=self.canv._pagesize[1])
        if self._title:
            self.canv.addOutlineEntry(self._title, self._name, level=0)


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=22, leading=26, textColor=DARK_NAVY, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], fontSize=9.5, leading=12,
    alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=8))
styles.add(ParagraphStyle(
    name="Box", parent=styles["Normal"], fontSize=8.2, leading=10.5,
    textColor=colors.HexColor("#222222")))
styles.add(ParagraphStyle(
    name="TOC", parent=styles["Normal"], fontSize=8.6, leading=10.5,
    leftIndent=8, firstLineIndent=-8, spaceAfter=1))
styles.add(ParagraphStyle(
    name="Header", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=11, leading=13, textColor=colors.white))
styles.add(ParagraphStyle(
    name="HeaderSub", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=7.6, leading=9, textColor=colors.HexColor("#EAF2FF")))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading3"], fontName="Helvetica-Bold",
    fontSize=9.4, leading=11, textColor=DARK_NAVY, spaceBefore=6, spaceAfter=2))
styles.add(ParagraphStyle(
    name="Body", parent=styles["Normal"], fontSize=12, leading=14.1, spaceAfter=4))
styles.add(ParagraphStyle(
    name="VisualLabel", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8.2, leading=10, textColor=MED_BLUE, spaceAfter=1))
styles.add(ParagraphStyle(
    name="VisualBody", parent=styles["Normal"], fontSize=8.1, leading=9.6,
    textColor=colors.HexColor("#222222"), spaceAfter=2))
styles.add(ParagraphStyle(
    name="TheoryBullet", parent=styles["Normal"], fontSize=9.4, leading=11.2,
    leftIndent=10, firstLineIndent=-6, spaceAfter=2))
styles.add(ParagraphStyle(
    name="Small", parent=styles["Normal"], fontSize=7, leading=8.5,
    textColor=colors.HexColor("#555555")))


theories = [
    {
        "id": "w1_strategic_choice",
        "session": "W1",
        "title": "Strategic Choice and Game Theory",
        "author": "International Relations: A Strategic-Choice Approach - David A. Lake & Robert Powell; A Non-Technical Introduction to Bargaining Theory - Abhinay Muthoo; course W1 lecture",
        "situation": "A crisis bargain over territory works like chess under pressure: each state chooses not only from what it wants, but from what it expects the other side will do in response.",
        "intuition": "Strategic choice treats international politics as interdependent decision-making. Lake and Powell's point is that political outcomes should be explained by how actors choose within a strategic environment, not by simply listing background conditions or desires. A state, leader, rebel organization, or voter ranks outcomes, chooses among available strategies, forms beliefs about what others will do, and receives payoffs that depend on everyone else's choices. Muthoo's bargaining logic adds the same idea in negotiation form: the final deal depends on outside options, patience, information, and credible threats. The exam move is to make the choice set visible before making a causal claim: who are the actors, what are their alternatives, what do they believe, and why does the equilibrium beat the rejected options?",
        "concepts": [
            ("Actors", "States, leaders, rebel groups, voters, or institutions whose choices affect one another."),
            ("Preferences", "Ranked outcomes; what each actor wants before strategic interaction begins. Preferences are not the same thing as strategies, because an actor can want one outcome while choosing a second-best action under constraint."),
            ("Strategies", "Available actions, including alternatives not chosen. A good application names the full feasible set and explains why some options are dominated, risky, or non-credible."),
            ("Beliefs", "Expectations about other actors' types, resolve, likely moves, or information. Beliefs connect information problems to strategic choice."),
            ("Payoffs", "The expected value of outcomes once preferences, costs, risks, and beliefs are combined."),
            ("Equilibrium", "A stable outcome in which no actor wants to change strategy given the others' choices."),
            ("Outside option", "What an actor can get if bargaining fails; stronger outside options shift bargaining leverage."),
            ("Credibility", "Whether a threat, promise, or offer is believable given the actor's incentives after the other side responds."),
        ],
        "assumptions": [
            "Actors can rank outcomes and compare expected payoffs.",
            "Choices are interdependent; one actor's best move depends on another's likely move.",
            "Information, sequencing, and credibility shape what strategies are available.",
            "The analyst can specify the relevant actors and strategic setting without collapsing internal divisions that matter to the outcome.",
        ],
        "strengths": [
            "Forces explicit actor-preference-strategy-belief-payoff analysis.",
            "Works across deterrence, bargaining, civil war, and democratic peace.",
            "Prevents purely descriptive case narratives.",
            "Makes counterfactuals disciplined by asking what alternatives were actually available.",
        ],
        "weaknesses": [
            "Can over-clean real-world preferences and factional politics.",
            "Equilibrium predictions are sensitive to assumptions.",
            "May understate emotion, ideology, identity, and organizational dysfunction.",
            "Can become empty if the analyst says 'strategic' without specifying incentives, information, and sequencing.",
        ],
    },
    {
        "id": "w2_preferences_signaling",
        "session": "W2",
        "title": "Preferences, Signaling, and Credibility",
        "author": "Actors and Preferences in International Relations - Jeffry A. Frieden; The Diplomacy of Violence - Thomas C. Schelling; Interests, Institutions, and Information - Helen V. Milner; Notes on Signaling Theory",
        "situation": "A leader who moves troops to a border may be bluffing for concessions or signaling real resolve; the opponent must infer which type she is from costly behavior.",
        "intuition": "Week 2 adds two building blocks to strategic choice. Frieden asks analysts to specify where preferences come from instead of treating the state as a black box: leaders, sectors, coalitions, bureaucracies, and institutions can rank outcomes differently. Schelling then shows why coercive diplomacy depends on communication under danger: threats and promises must be made credible when the target cannot directly observe resolve. Signaling theory supplies the mechanism. Cheap talk is easy to mimic; credible signals work because they impose costs, tie hands, sink resources, or expose the sender to future punishment. Milner's cooperation frame keeps the distinction clear: cooperation is policy adjustment for mutual gain, but it often requires information and institutions to make preferences, promises, and compliance believable.",
        "concepts": [
            ("Preference ordering", "A rank order over possible outcomes, not a vague statement of interest."),
            ("Private information", "Information an actor has about its own capability, costs, or resolve that others lack."),
            ("Cheap talk", "A statement that is costless to make and therefore easy to mimic."),
            ("Costly signal", "An action that reveals information because only high-resolve actors are willing to pay the cost."),
            ("Tying hands", "Creating future punishment for backing down, as in public threats."),
            ("Sinking costs", "Paying upfront costs, such as mobilization, to show seriousness."),
            ("Commitment", "A threat or promise that changes the sender's future incentives enough to shape the target's expectations."),
            ("Policy adjustment", "Milner's cooperation baseline: actors alter behavior so both sides can be better off than under unilateral action."),
        ],
        "assumptions": [
            "Actors know or can form preferences over outcomes.",
            "Observers can see at least some signals and update from them.",
            "Low-resolve actors cannot mimic high-resolve signals without real cost.",
            "Domestic and international audiences can understand at least part of the signal's cost or constraint.",
        ],
        "strengths": [
            "Separates disagreement over preferences from disagreement over beliefs.",
            "Explains red lines, mobilization, public threats, and coercive diplomacy.",
            "Connects directly to Fearon's audience-cost and bargaining models.",
            "Keeps domestic sources of preferences visible instead of assuming a unitary national interest.",
        ],
        "weaknesses": [
            "Preferences are often unstable, hidden, or endogenous.",
            "Signals can be misread by different audiences.",
            "Domestic and international audiences can produce conflicting incentives.",
            "Costliness does not guarantee clarity; actors may disagree about what a signal means.",
        ],
    },
    {
        "id": "w3_fearon",
        "session": "W3.1",
        "title": "Fearon's Rationalist Bargaining Model of War",
        "author": "Rationalist Explanations for War - James D. Fearon",
        "situation": "In July 1914, European powers could have preferred a settlement to continental war, but private information and incentives to bluff made the bargaining range hard to locate before mobilization escalated.",
        "intuition": "Fearon begins from the inefficiency puzzle: because war destroys resources, there should usually be a settlement both sides prefer to fighting. A rationalist explanation cannot simply say leaders wanted incompatible things; it must explain why they could not find or enforce a mutually preferable bargain. Fearon's three mechanisms are private information with incentives to misrepresent, commitment problems, and issue indivisibilities. The first is especially important in short crises: states privately know more about their capabilities, costs, and resolve than opponents do, yet they also have incentives to exaggerate those traits to win a better deal. War can then occur as a costly screening device, revealing information that bargaining could not credibly communicate.",
        "concepts": [
            ("Inefficiency puzzle", "War is costly, so ex post there should have been a bargain both sides preferred."),
            ("Bargaining range", "The set of settlements both sides prefer to war."),
            ("Private information", "Hidden capability, resolve, or costs."),
            ("Incentive to misrepresent", "A reason to exaggerate resolve to get a better deal."),
            ("Commitment problem", "Inability to credibly promise to honor a deal later."),
            ("Issue indivisibility", "A disputed good cannot be divided or compensated; Fearon treats this as rare."),
            ("Risk-return tradeoff", "Actors may gamble on war when beliefs make the expected payoff of fighting exceed available offers."),
            ("Costly revelation", "War reveals information, but only by destroying resources that bargaining was supposed to preserve."),
        ],
        "assumptions": [
            "War is costly to both sides.",
            "Actors are rational and compare war to negotiated bargains.",
            "Offers can be made, but private information cannot be costlessly revealed.",
            "The disputed good or policy can usually be divided, compensated, or settled unless another mechanism blocks agreement.",
        ],
        "strengths": [
            "Gives a disciplined mechanism for war despite costs.",
            "Unifies crisis bargaining, bluffing, and bargaining failure.",
            "Sets up later Powell and Walter commitment-problem arguments.",
            "Useful diagnostic test: identify the bargaining range, then explain why actors failed to reach it.",
        ],
        "weaknesses": [
            "Cannot easily explain long wars after information is revealed.",
            "Unitary-actor assumptions fit authoritarian pathologies poorly.",
            "Underplays preference formation and domestic politics.",
            "Issue indivisibility can become a catch-all if not tied to compensation or credible commitment limits.",
        ],
    },
    {
        "id": "w3_powell",
        "session": "W3.2",
        "title": "Powell's War as a Commitment Problem",
        "author": "War as a Commitment Problem - Robert Powell",
        "situation": "A declining state may attack a rising rival now, not because it lacks information, but because any deal today lets the rival become too powerful to restrain tomorrow.",
        "intuition": "Powell argues that commitment problems are the master mechanism behind rationalist war. The key is a shifting distribution of power: actors may know the facts and prefer peace in the abstract, but no agreement is self-enforcing if today's bargain gives one side the ability or incentive to demand more tomorrow. This is why Powell matters after Fearon. He shows that war can occur under complete information, with divisible stakes, and between fully rational actors. Preventive war, bargains over power-shifting assets, and first-strike incentives are illustrations of one commitment logic, not three separate named theories: actors fight because future promises cannot bind a changed balance of coercive power.",
        "concepts": [
            ("Dynamic inconsistency", "A deal that is attractive today is not credible tomorrow after power shifts."),
            ("Power-shifting asset", "A concession or object that changes future bargaining power."),
            ("Preventive war", "War by a declining actor to avoid a worse future position."),
            ("First-strike advantage", "A crisis condition where striking first improves survival odds."),
            ("Non-fungibility", "Side payments cannot fully compensate for lost future power."),
            ("Complete information", "Powell's mechanism can produce war even when actors know the facts."),
            ("Self-enforcing agreement", "A bargain that actors want to honor later without outside enforcement; Powell's cases fail because later incentives change."),
            ("Window of opportunity", "A temporary advantage that creates pressure to fight before the bargaining position deteriorates."),
        ],
        "assumptions": [
            "No central enforcer can bind future behavior.",
            "Power shifts are large enough to alter future bargaining.",
            "Actors are forward-looking and calculate future vulnerability.",
            "The relevant asset or institutional change affects future coercive leverage, not only current payoffs.",
        ],
        "strengths": [
            "Explains war under complete information.",
            "Clarifies why some bargains cannot be made credible.",
            "Travels well to civil-war demobilization and regime transitions.",
            "Sharpens exam answers by separating information failure from enforcement failure.",
        ],
        "weaknesses": [
            "Can overstate commitment logic where information failure is primary.",
            "Abstracts from identity, ideology, and domestic constraints.",
            "Requires careful proof that the relevant power shift is real.",
            "The mechanism is easy to over-apply unless the future distribution of power is explicitly shown.",
        ],
    },
    {
        "id": "w3_cases",
        "session": "W3.3",
        "title": "Strategic Misperception and Case Diagnostics",
        "author": "The Strategic Setting of Choices - James D. Morrow; The Persian Gulf Crisis - Steve A. Yetiv; Saddam's Delusions: The View from the Inside - Kevin M. Woods, James Lacey & Williamson Murray; The Talks That Could Have Ended the War in Ukraine - Samuel Charap & Sergey Radchenko",
        "situation": "Saddam in 1990 and Saddam in 2002-03 made different errors: the first hinged on U.S. resolve signals, while the second included beliefs about sanctions, WMD ambiguity, and great-power veto protection.",
        "intuition": "Week 3 case readings teach diagnosis, not a new master theory. Morrow supplies the strategic-setting vocabulary: choices only make sense once the analyst specifies actors, preferences, information, institutions, and constraints. Yetiv's Gulf War account shows how Saddam misread U.S. resolve in 1990-91 through Vietnam, regional, and diplomatic signals. Woods, Lacey, and Murray show a different 2002-03 pathway: authoritarian filters, WMD ambiguity, sanctions politics, Iran deterrence, and beliefs about France/Russia at the UN shaped Saddam's expectations. Charap and Radchenko then give a live bargaining case where assurances, guarantees, territorial control, and outside commitments mattered. The exam task is to diagnose the mechanism precisely, not to say a leader 'miscalculated in game theory.'",
        "concepts": [
            ("Strategic setting", "The configuration of actors, choices, information, and institutions around a decision."),
            ("Rational miscalculation", "Wrong beliefs about another actor's type, resolve, or likely response."),
            ("Authoritarian information pathology", "Bad news and dissent are filtered before reaching the leader."),
            ("Assurance", "A promise or statement meant to reduce fear but without strong enforcement."),
            ("Guarantee", "A stronger commitment backed by credible enforcement or protection."),
            ("Case mechanism", "The specific causal route from beliefs and incentives to bargaining failure."),
            ("Chronology discipline", "Assign beliefs to the right conflict and time period before applying theory."),
            ("Organizational filter", "Information is selected, distorted, or suppressed before leaders see it."),
        ],
        "assumptions": [
            "Cases can be decomposed into actors, preferences, strategies, beliefs, and payoffs.",
            "Different wars can involve different mechanisms even when the same leader appears.",
            "Source-specific chronology matters for assigning beliefs correctly.",
            "Leaders act on perceived incentives, so the analyst must reconstruct beliefs from source evidence rather than hindsight.",
        ],
        "strengths": [
            "Keeps theory tied to concrete historical evidence.",
            "Prevents conflating the 1990-91 Gulf War with the 2003 Iraq War.",
            "Good exam bridge between formal theory and world events.",
            "Makes room for misperception without abandoning rationalist mechanism-testing.",
        ],
        "weaknesses": [
            "Case evidence can be messy or post hoc.",
            "Multiple mechanisms may operate at once.",
            "Risk of importing local shorthand instead of source terminology.",
            "Retrospective evidence can tempt analysts to overstate what actors knew at the time.",
        ],
    },
    {
        "id": "w4_audience_costs",
        "session": "W4.1",
        "title": "Audience Costs and Crisis Signaling",
        "author": "Domestic Political Audiences and the Escalation of International Disputes - James D. Fearon",
        "situation": "Kennedy's public quarantine speech during the Cuban Missile Crisis made retreat politically costly, helping Khrushchev infer that U.S. resolve was not cheap talk.",
        "intuition": "Audience-cost theory explains how domestic politics can make international signals credible. Fearon models crises as a war of attrition: each public escalation raises the cost of retreat, and the side with lower resolve should prefer to back down before paying too much. Leaders who make public threats create domestic political penalties if they later retreat, so escalation becomes a tying-hands signal. Democracies often generate larger and more visible audience costs through elections, opposition, and media scrutiny. The result is not that democracies are always peaceful; it is that when they enter public crises, they can reveal resolve faster, win concessions earlier, or exit before escalation becomes uncontrolled.",
        "concepts": [
            ("Audience costs", "Domestic penalties for publicly committing and then backing down."),
            ("War of attrition", "Sequential escalation where each side waits for the other to quit."),
            ("Tying hands", "Creating a cost paid if the leader retreats."),
            ("Resolve", "Willingness to bear costs to obtain an outcome."),
            ("Regime type", "Institutional context that affects the size and visibility of audience costs."),
            ("Crisis duration", "High-audience-cost crises should resolve faster."),
            ("Public commitment", "A threat or demand made where domestic audiences can observe retreat."),
            ("Signaling advantage", "The ability to communicate resolve credibly because backing down would be politically costly."),
        ],
        "assumptions": [
            "Domestic audiences observe commitments and punish retreat.",
            "Leaders value political survival.",
            "Opponents understand the domestic institution well enough to update beliefs.",
            "Public escalation is sufficiently visible that backing down can be identified and punished.",
        ],
        "strengths": [
            "Links domestic accountability to international credibility.",
            "Explains public threats and democratic signaling advantages.",
            "Complements democratic-peace institutional explanations.",
            "Explains why public red lines can change the informational structure of a crisis.",
        ],
        "weaknesses": [
            "Empirical measurement is difficult.",
            "Voters may reward restraint rather than punish backing down.",
            "Autocracies can also create nationalist or elite audience costs.",
            "Leaders may avoid public commitments precisely when they want bargaining flexibility, creating selection problems.",
        ],
    },
    {
        "id": "w4_selectorate",
        "session": "W4.2",
        "title": "Institutional Democratic Peace / Selectorate Logic",
        "author": "An Institutional Explanation of the Democratic Peace - Bruce Bueno de Mesquita, James D. Morrow, Randolph M. Siverson & Alastair Smith",
        "situation": "Two democracies facing a dispute know that both leaders must satisfy large winning coalitions, so both expect the other to try hard in war and become more selective about fighting.",
        "intuition": "The institutional democratic peace does not require democratic norms. It derives from political survival incentives. Leaders need a winning coalition to stay in office, and the size of that coalition changes how they allocate resources and how risky war is for them politically. Large-coalition leaders cannot cheaply buy loyalty with private goods, so they must provide public goods and avoid disastrous policy failure. If they fight, they try harder because defeat threatens office. When two large-W states bargain, each expects the other to mobilize high effort and punish failure, making peaceful settlement more attractive. The theory therefore predicts dyadic democratic peace and democratic war selectivity, not simple democratic pacifism.",
        "concepts": [
            ("Selectorate", "Those with a formal role in choosing leaders."),
            ("Winning coalition", "The subset whose support keeps the leader in office."),
            ("W/S ratio", "A loyalty norm shaping how replaceable supporters are."),
            ("Public goods", "Broad benefits such as security, victory, or growth."),
            ("Private goods", "Targeted patronage or rents for coalition members."),
            ("Trying harder", "Large-W leaders devote more resources to wars they enter."),
            ("War selectivity", "Large-W leaders avoid risky fights but invest heavily when they do fight."),
            ("Dyadic peace", "Peace is expected between two large-W regimes, not necessarily between any democracy and any regime."),
        ],
        "assumptions": [
            "Leaders primarily seek political survival.",
            "Institutional coalition size shapes the cost of failure.",
            "Opponents can infer institutional incentives.",
            "War effort translates into outcome probability closely enough that leaders care about expected military performance.",
        ],
        "strengths": [
            "Microfounds dyadic democratic peace without relying on norms.",
            "Explains democratic war selectivity and war-winning patterns.",
            "Travels beyond binary democracy/autocracy labels.",
            "Explains both initiation and conduct of war through one political-survival logic.",
        ],
        "weaknesses": [
            "Measurement of W and S is contested in hybrid regimes.",
            "Downplays identity, ideology, and normative affinity.",
            "Covert action against democracies complicates the dyadic claim.",
            "Institutional incentives may be overridden by ideology, threat perception, or incomplete information.",
        ],
    },
    {
        "id": "w4_public_opinion",
        "session": "W4.3",
        "title": "Cognitive-Interactionist Public Support for War",
        "author": "Mass Public Decisions to Go to War: A Cognitive-Interactionist Framework - Richard K. Herrmann, Philip E. Tetlock & Penny S. Visser",
        "situation": "Americans could support the 1991 Gulf War but divide over Kosovo because stable foreign-policy dispositions interact with case-specific cues about interests, power, motives, and cultural status.",
        "intuition": "Mass publics are neither pure ideologues nor passive reactors to each new case. Herrmann, Tetlock, and Visser argue that citizens combine relatively stable foreign-policy dispositions with case-specific images of the adversary and conflict. A person high in internationalism may support action when intervention appears legitimate and multilateral, while a highly assertive person may respond more to threat and coercive leverage. Situational cues include relative power, stakes, adversary motives, cultural status, and whether the target is seen as enemy, ally, barbarian, dependent, or imperial. The interaction matters: the same case cue can move different dispositional types by different amounts, or even in opposite directions.",
        "concepts": [
            ("Cognitive-interactionist framework", "Public opinion comes from interaction between dispositions and situations."),
            ("Internationalism", "Disposition favoring active U.S. engagement abroad."),
            ("Assertiveness", "Disposition favoring coercive rather than accommodative tools."),
            ("Image theory", "Judgments based on relative power, motives, interests, and cultural status."),
            ("Ordinal interaction", "Groups move in the same direction but by different amounts."),
            ("Disordinal interaction", "Groups move in opposite directions, producing polarization."),
            ("Enemy / ally / barbarian images", "Image-theory categories that combine motive, power, and cultural judgments."),
            ("Knowledge effects", "More informed citizens may use situational cues differently from less informed citizens."),
        ],
        "assumptions": [
            "Citizens hold measurable foreign-policy dispositions.",
            "Survey vignettes capture meaningful situational cues.",
            "Knowledge moderates how citizens combine cues.",
            "Dispositions are stable enough to interact with case cues rather than being recreated from scratch each crisis.",
        ],
        "strengths": [
            "Adds mass public microfoundations to democratic accountability.",
            "Explains variation across intervention cases.",
            "Shows foreign-policy ideology is not reducible to left-right ideology.",
            "Useful bridge between democratic accountability and the domestic politics of intervention.",
        ],
        "weaknesses": [
            "Survey experiments may not map perfectly to real crises.",
            "Elite framing and media environments are under-modeled.",
            "Not a complete theory of war onset by itself.",
            "Public support can be shaped by elite framing before citizens evaluate case cues.",
        ],
    },
    {
        "id": "w4_civil_war",
        "session": "W4.4",
        "title": "Civil War Bargaining Failures and Correlates",
        "author": "Bargaining Failures and Civil War - Barbara F. Walter; Civil War - Christopher Blattman & Edward Miguel",
        "situation": "A weak state with low income and organized challengers may have a bargaining range, but rebels and governments still fight because enforcement is weak and future power cannot be guaranteed.",
        "intuition": "The civil-war readings extend Fearon and Powell inside the state. Walter emphasizes bargaining failures: information problems, commitment problems, and security dilemmas are sharper because domestic groups lack a neutral enforcer and because disarmament or decentralization can permanently change the balance of power. Blattman and Miguel survey the empirical literature and warn that low income, slow growth, weak state capacity, and rough terrain are robust correlates, but causal mechanisms are hard to identify. The combined exam lesson is to separate correlates from mechanisms: poverty may predict risk, but the causal story still has to specify how actors mobilize, bargain, mistrust enforcement, and choose violence.",
        "concepts": [
            ("Civil war onset", "Entry into organized intrastate violence above a battle-death threshold."),
            ("State capacity", "Ability of the state to tax, monitor, police, and enforce bargains."),
            ("Commitment problem", "Groups cannot trust future guarantees once they disarm or lose leverage."),
            ("Collective action", "The problem of mobilizing individuals into sustained rebellion."),
            ("Low income", "The most robust cross-national correlate of civil war risk."),
            ("Identification problem", "Difficulty separating causes of war from consequences of war."),
            ("Security dilemma", "Groups arm for protection, but those arms make rivals less secure and can trigger escalation."),
            ("Opportunity cost", "Low income can reduce the cost of joining rebellion, though the evidence should be handled carefully."),
        ],
        "assumptions": [
            "Organized groups can compare war to settlement.",
            "State weakness affects enforcement and rebel opportunities.",
            "Observed correlations require caution before causal claims.",
            "Domestic bargaining occurs under weak or contested sovereignty rather than under a neutral enforcer.",
        ],
        "strengths": [
            "Connects intrastate war to the same bargaining toolkit as interstate war.",
            "Adds empirical discipline through civil-war correlates.",
            "Useful for Myanmar, Syria, Colombia, and sectarian-war prompts.",
            "Disciplines data-heavy answers by distinguishing prediction from explanation.",
        ],
        "weaknesses": [
            "Mechanisms are often weakly identified in cross-national data.",
            "Unitary rebel/government assumptions can hide spoilers.",
            "Material correlates do not fully explain identity or ideology.",
            "The civil-war category covers very different conflicts, so one mechanism rarely fits all cases cleanly.",
        ],
    },
    {
        "id": "w5_walter",
        "session": "W5.1",
        "title": "Walter's Civil-War Settlement Commitment Problem",
        "author": "Committing to Peace: The Successful Settlement of Civil Wars, Chapter 2, Theory and Hypotheses - Barbara F. Walter",
        "situation": "The Cambodia settlement held under UNTAC while Rwanda's Arusha accords collapsed because combatants need credible protection during the dangerous demobilization window.",
        "intuition": "Civil-war settlements fail during implementation. To make peace, fighters must disarm, surrender territory, and accept a new political order; that creates a window of vulnerability in which the other side can cheat, seize the state, or eliminate a rival. Walter's key move is backward induction. Combatants look ahead to the last stage of demobilization, see the sucker payoff if they disarm while the rival cheats, and refuse to begin the process unless the implementation environment changes. Written terms are therefore insufficient. Negotiated settlements need credible third-party security guarantees plus real power sharing in the first postwar government so that demobilization is protected and the loser is not permanently excluded.",
        "concepts": [
            ("Implementation phase", "The dangerous post-agreement period when forces demobilize."),
            ("Window of vulnerability", "The period when disarming groups are exposed to exploitation."),
            ("Third-party security guarantee", "Outside verification or enforcement that protects demobilization."),
            ("Power-sharing pact", "Guaranteed political, military, or territorial inclusion after war."),
            ("Backward induction", "Combatants anticipate last-move cheating and refuse to start demobilization."),
            ("Sucker payoff", "The catastrophic outcome of disarming while the rival cheats."),
            ("Hegemony payoff", "The tempting outcome in which one side gains full control after the other becomes vulnerable."),
            ("Verification versus enforcement", "Monitoring may suffice under rough balance; coercive enforcement is needed when one side is exposed."),
        ],
        "assumptions": [
            "Combatants prefer hegemony to power sharing, but peace to continued war under the right guarantees.",
            "Demobilization has a known last move.",
            "Third-party commitment can be observed and believed by combatants.",
            "The first postwar government can credibly allocate power if the pact is externally protected.",
        ],
        "strengths": [
            "Explains why signed peace deals often fail at implementation.",
            "Produces policy levers: enforcement, verification, and power sharing.",
            "Clear bridge from Powell's power-shift logic to civil wars.",
            "Gives concrete policy diagnostics: mandate, troop commitment, verification, enforcement, and power-sharing design.",
        ],
        "weaknesses": [
            "Treats third parties as more credible and less strategic than they may be.",
            "Assumes coherent factions, straining in multi-party wars.",
            "Selection bias complicates evidence on third-party guarantees.",
            "Does not fully explain settlements that partially implement, stall, and persist below the war threshold.",
        ],
    },
    {
        "id": "w5_democratization",
        "session": "W5.2",
        "title": "Democratization and Civil War Risk",
        "author": "Democratization and Civil War: Empirical Evidence - Lars-Erik Cederman, Simon Hug & Lutz F. Krebs",
        "situation": "Myanmar's 2010 opening and 2021 coup show why regime transitions can increase conflict risk: elites compete over control of government while coercive institutions and credible commitments remain unsettled.",
        "intuition": "Cederman, Hug, and Krebs examine how democratization relates to civil war onset. The key course takeaway is not that democracy simply causes peace or war. It is that transitions can be dangerous because regime change reopens competition over governmental power while institutions may still be too weak to bind winners, protect losers, or control coercive actors. Their core distinction is source-faithful and should stay on the page: democratization is especially tied to governmental conflict, meaning conflict over control of the central government, while territorial conflict follows a different logic of autonomy, secession, or territory. For Myanmar-style applications, the transition itself matters because electoral opening changes elite incentives and fears before a stable democratic bargain exists.",
        "concepts": [
            ("Democratization", "Movement toward more competitive political institutions."),
            ("Governmental conflict", "Conflict over control of central government."),
            ("Territorial conflict", "Conflict over autonomy, secession, or control of territory."),
            ("Transition risk", "Heightened conflict danger during incomplete or reversed democratization."),
            ("Elite incentives", "Strategic reasons incumbent or opposition actors may use violence."),
            ("Institutional weakness", "Low capacity to bind losers, protect rights, or enforce bargains."),
            ("Conflict over government", "A fight about who controls the central state, cabinet, coercive apparatus, and national policy."),
            ("Incomplete transition", "A regime opening that creates competition without fully credible democratic constraints."),
        ],
        "assumptions": [
            "Regime change alters access to governmental power.",
            "Actors fear exclusion or punishment under new institutions.",
            "Civil war risk differs by governmental versus territorial conflict logic.",
            "Transitions change expectations about future exclusion, punishment, or loss of coercive privilege.",
        ],
        "strengths": [
            "Links regime transition to civil-war bargaining and commitment problems.",
            "Fits Myanmar and other incomplete democratization cases.",
            "Gives precise terminology for Orange-memo and midterm answers.",
            "Connects regime-type change to bargaining and commitment problems without inventing new labels.",
        ],
        "weaknesses": [
            "Quantitative associations need careful causal interpretation.",
            "Country-specific institutions can matter more than aggregate transition labels.",
            "Territorial and governmental conflicts can overlap in real cases.",
            "Country-level transition labels can hide which actors actually control coercion.",
        ],
    },
]


AUTHOR_CONTEXT = {
    "w1_strategic_choice": "Lake and Powell write from the rationalist turn in international-relations theory, when scholars were pushing beyond descriptive realism toward actor-centered explanations that could travel across security, political economy, and domestic politics. Muthoo's bargaining theory comes from formal economics, where negotiation outcomes are explained by outside options, patience, information, and credible commitment rather than by moral claims about who deserves what.",
    "w2_preferences_signaling": "Frieden's preference work belongs to the political-economy and comparative-politics effort to open the state and identify which domestic actors want which policies. Schelling wrote during the Cold War nuclear age, when coercion, deterrence, and communication under the shadow of catastrophic violence were central policy problems. Milner and signaling theory add the post-Cold War institutionalist concern with how actors communicate, cooperate, and make promises believable under anarchy.",
    "w3_fearon": "Fearon's 1995 article is a landmark of the rationalist war literature of the 1990s. It responds to explanations that treated war as the obvious result of greed, aggression, or incompatible interests by asking a sharper puzzle: if fighting is costly, why do rational states fail to bargain around it before the costs are paid?",
    "w3_powell": "Powell's 2006 article comes after Fearon and deliberately narrows the rationalist agenda. Rather than treating private information, commitment problems, and indivisibility as equal suspects in every case, Powell argues that commitment problems do the deepest work because anarchy makes future bargains hard to enforce when power shifts.",
    "w3_cases": "The Week 3 case readings sit in the applied-security tradition: they use historical evidence to test whether a formal mechanism actually fits a crisis. Morrow supplies the strategic vocabulary, Yetiv reconstructs the 1990-91 Gulf crisis, Woods, Lacey, and Murray use captured Iraqi records to reinterpret Saddam's 2002-03 beliefs, and Charap and Radchenko analyze the 2022 Ukraine negotiation window.",
    "w4_audience_costs": "Fearon's audience-cost article appears in the early democratic-peace and crisis-bargaining debate of the 1990s. Scholars were trying to explain why democracies seemed to behave differently in international crises without assuming that democratic publics were simply more peaceful or morally superior.",
    "w4_selectorate": "Bueno de Mesquita, Morrow, Siverson, and Smith write in the selectorate tradition, which recasts regime type as a leader-survival problem. Their institutional democratic-peace account emerged as an alternative to norms-based explanations: democracies are not peaceful because citizens are nicer, but because large winning coalitions change the political cost of bad wars.",
    "w4_public_opinion": "Herrmann, Tetlock, and Visser write from political psychology and public-opinion research at a moment when scholars were moving beyond the Almond-Lippmann view of the public as incoherent or unstable. Their framework treats citizens as bounded but structured thinkers whose foreign-policy judgments depend on both dispositions and case images.",
    "w4_civil_war": "Walter's 2009 review and Blattman and Miguel's 2010 survey come from the post-Cold War explosion of civil-war research. The environment is empirical and policy-facing: scholars were trying to explain why internal wars began, why they persisted, and why poverty, weak states, rough terrain, and enforceability problems appeared so consistently in the data.",
    "w5_walter": "Walter's book was written after the 1990s wave of negotiated settlements, peacekeeping missions, and failed accords in places like Rwanda, Bosnia, Cambodia, and Angola. The policy environment matters: the question is not whether combatants can sign an agreement, but why signing does not solve the last-mile security problem of disarmament and implementation.",
    "w5_democratization": "Cederman, Hug, and Krebs write in the quantitative democratization-and-conflict literature. Their article responds to the broad democratic-peace intuition by focusing on transitions: moving toward democracy can destabilize politics before institutions can credibly regulate competition for governmental power.",
}


MECHANISM_DETAIL = {
    "w1_strategic_choice": "Mechanism: start with the strategic setting, not the outcome. Each actor ranks outcomes, compares strategies, forms beliefs about the other side, and anticipates how payoffs change after the other side responds. The causal claim is strongest when it shows why the chosen strategy was better than plausible alternatives given those beliefs, not merely why the actor wanted the final outcome.",
    "w2_preferences_signaling": "Mechanism: preferences tell us what actors want; signals help others infer hidden resolve, capability, or type. A signal becomes informative when it is harder for low-resolve actors to mimic than high-resolve actors, either because it burns resources, risks public punishment, or changes future incentives. A good answer separates preference conflict from belief conflict before deciding which mechanism is doing the work.",
    "w3_fearon": "Mechanism: war occurs when bargaining fails despite a possible peaceful bargain. Private information and incentives to misrepresent hide the bargaining range; commitment problems make future compliance non-credible; indivisibility blocks division or compensation only in special cases. The theory's power is diagnostic: identify the bargain both sides should prefer, then show the precise obstacle that kept it unavailable.",
    "w3_powell": "Mechanism: today's bargain changes tomorrow's power, so promises that look acceptable now become incredible later. The declining side anticipates future vulnerability; the rising side cannot credibly promise restraint once stronger; and no outside enforcer can bind the future distribution of coercive power. Preventive war, power-shifting bargains, and first-strike incentives are examples of that same intertemporal enforcement failure.",
    "w3_cases": "Mechanism: cases are used to discipline theory choice. Reconstruct what actors believed at the time, identify the institutional and informational filters around them, then match the evidence to a mechanism: private information, misread resolve, commitment failure, assurance failure, or authoritarian distortion. The same leader can belong to different mechanisms in different crises, so chronology is not cosmetic.",
    "w4_audience_costs": "Mechanism: public escalation changes the informational game by making retreat domestically costly. If backing down threatens office, reputation, or political support, then only leaders with sufficient resolve should be willing to escalate publicly. Opponents update from that willingness, which can shorten crises or induce concessions before fighting.",
    "w4_selectorate": "Mechanism: leaders choose foreign policy under survival constraints. Small-coalition leaders can survive bad public outcomes by rewarding loyal insiders with private goods; large-coalition leaders need broader public-goods performance and are punished more harshly for losing. Because other democracies anticipate high effort and high punishment for failure, two large-W states bargain differently than mixed or autocratic dyads.",
    "w4_public_opinion": "Mechanism: citizens combine standing dispositions with images of the specific case. Internationalism, assertiveness, knowledge, perceived motives, relative power, and cultural status interact, so the same intervention cue can persuade one group and polarize another. Public support is therefore neither fixed ideology nor pure elite manipulation; it is structured interpretation.",
    "w4_civil_war": "Mechanism: civil-war risk emerges when mobilization opportunities and bargaining failures meet weak enforcement. Poverty or rough terrain may predict risk, but the exam answer still needs the actor-level path: who can organize, what bargain would avoid war, why promises are not credible, and how state capacity or security dilemmas make violence preferable to settlement.",
    "w5_walter": "Mechanism: implementation reverses the incentives of settlement. Once a group disarms, the rival may gain a hegemony payoff by cheating; knowing this, combatants use backward induction and refuse to demobilize unless guarantees change the endgame. Third-party security guarantees and power sharing matter because they protect the vulnerable transition from war to politics.",
    "w5_democratization": "Mechanism: democratization reopens competition over control of government before institutions necessarily become credible. Incumbents may fear exclusion or punishment; challengers may see a new path to central power; coercive actors may resist losing privilege. Cederman, Hug, and Krebs's key source-faithful distinction is that this transition risk is especially about governmental conflict, not automatically about territorial conflict.",
}


EXAM_DEPLOYMENT = {
    "w1_strategic_choice": "Exam deployment: use this page as the skeleton for almost any GPCO 410 essay. Write one sentence naming the actors, one sentence ranking preferences, one sentence listing strategies including rejected alternatives, one sentence on beliefs, and one sentence comparing expected payoffs. Then state the equilibrium or bargaining failure. This is especially useful when the prompt gives a case but does not name the theory.",
    "w2_preferences_signaling": "Exam deployment: ask whether the dispute is really about different preferences, hidden information, or credibility. If the issue is hidden resolve, use costly signaling, tying hands, or sinking costs. If the issue is where preferences come from, open the state and identify domestic coalitions or leaders. Do not call every message a signal; show why the signal was costly or why it failed.",
    "w3_fearon": "Exam deployment: begin with the inefficiency puzzle. Say what settlement should have existed, then choose among private information, commitment problem, and indivisibility. Use Fearon when uncertainty, bluffing, or incentives to misrepresent are central; switch to Powell or Walter when the core problem is future enforcement even after information is clear.",
    "w3_powell": "Exam deployment: use Powell when the prompt turns on future power, preventive incentives, first-move advantages, disarmament, regime change, or concessions that alter coercive leverage. Do not present Powell as three named types. Say instead that commitment problems are the master mechanism and that preventive war, power-shifting assets, or first-strike dynamics illustrate it.",
    "w3_cases": "Exam deployment: use this as the case-discipline page. Stamp the year, name the conflict, and avoid transferring beliefs across cases. For Saddam, keep 1990-91 U.S. resolve misreading separate from 2002-03 sanctions, WMD ambiguity, Iran deterrence, and France/Russia veto beliefs. For Ukraine, distinguish assurances from enforceable guarantees.",
    "w4_audience_costs": "Exam deployment: use audience costs when public threats, democratic accountability, reputation for backing down, or red lines appear in the prompt. The move is not 'democracy causes peace'; it is 'public commitment changes the cost of retreat and therefore the credibility of resolve.' Always check whether domestic audiences actually observe and punish retreat.",
    "w4_selectorate": "Exam deployment: use selectorate logic when comparing democracies, autocracies, and hybrid regimes in war initiation or war effort. Identify the winning coalition and ask how the leader survives after success or failure. The strongest exam contrast is dyadic: two large-W states have mutual reasons to expect high effort and high punishment for losing.",
    "w4_public_opinion": "Exam deployment: use this theory when the prompt asks why citizens support one intervention but not another, or why democratic leaders face different domestic constraints across cases. Name the relevant disposition and case image, then explain the interaction. It pairs well with audience costs but answers a different question: how publics evaluate war, not just how leaders signal resolve.",
    "w4_civil_war": "Exam deployment: use this page to avoid confusing correlates with causes. It is fine to mention low income or weak state capacity, but the mechanism must still specify bargaining failure, mobilization, enforcement, or security dilemma. This is the bridge page for prompts that mix data patterns with theory application.",
    "w5_walter": "Exam deployment: use Walter when the question asks why negotiated settlements are rare, why peace agreements collapse, or why third parties matter. Work backward from demobilization: what is the last-move temptation, who is vulnerable, what guarantee would change payoffs, and whether power sharing gives the loser enough protection to enter postwar politics.",
    "w5_democratization": "Exam deployment: use Cederman, Hug, and Krebs for transition-risk cases such as Myanmar. Keep the terms governmental conflict, conflict over government, and territorial conflict visible. The best answer says democratization can raise conflict risk during transition because competition over central state power intensifies before institutions can credibly bind winners and protect losers.",
}


PITFALLS_AND_CONTRASTS = {
    "w1_strategic_choice": (
        "Common pitfall: writing a case narrative and sprinkling the word strategic over it. The framework only works if the alternatives and rejected strategies are visible.",
        "Compare with: Fearon and Powell are narrower theories of bargaining failure. Strategic choice is the broader grammar that lets Edgar state actors, preferences, strategies, beliefs, and payoffs before choosing a mechanism.",
    ),
    "w2_preferences_signaling": (
        "Common pitfall: treating preferences, interests, and strategies as interchangeable. Preferences rank outcomes; strategies are actions chosen under constraint; signals are actions or statements that shape beliefs.",
        "Compare with: Fearon uses private information and incentives to misrepresent to explain war. Week 2 gives the upstream vocabulary for what is hidden, how actors communicate it, and why some communication is credible.",
    ),
    "w3_fearon": (
        "Common pitfall: saying war happened because the sides disagreed. Fearon requires a bargaining-range failure: if war is costly, disagreement alone is not enough unless it blocks a mutually preferable settlement.",
        "Compare with: Powell accepts the bargaining setup but argues that future commitment problems, not just hidden information, can make war rational even when actors know the facts.",
    ),
    "w3_powell": (
        "Common pitfall: calling preventive war, power-shifting assets, and first-strike advantage three separate Powell theories. They are illustrations of one commitment-problem mechanism.",
        "Compare with: Fearon is strongest when actors cannot credibly reveal private information. Powell is strongest when the facts are sufficiently clear but future enforcement remains impossible.",
    ),
    "w3_cases": (
        "Common pitfall: turning every bad decision into irrationality. These cases often show rational action under wrong beliefs, distorted information, bad institutions, or credible-commitment traps.",
        "Compare with: the case page is not a rival to Fearon, Powell, or Walter. It is the evidence discipline that tells Edgar which abstract mechanism actually fits a concrete historical sequence.",
    ),
    "w4_audience_costs": (
        "Common pitfall: assuming any public statement creates audience costs. The audience must observe the commitment, interpret retreat as failure, and have some way to punish the leader.",
        "Compare with: selectorate theory explains why leaders fight or avoid wars based on survival coalitions. Audience-cost theory explains how public commitments reveal resolve during crises.",
    ),
    "w4_selectorate": (
        "Common pitfall: reducing the theory to democracies are peaceful. The claim is dyadic and institutional: large winning coalitions change leader incentives, war selectivity, effort, and expected punishment for failure.",
        "Compare with: audience costs focus on crisis signals; selectorate logic focuses on leader survival and war effort across regime types. They can reinforce each other but are not the same theory.",
    ),
    "w4_public_opinion": (
        "Common pitfall: treating public opinion as either fully rational policy analysis or pure manipulation. Herrmann, Tetlock, and Visser occupy the middle: structured dispositions interact with case images.",
        "Compare with: audience costs ask how leaders use public commitments. Cognitive-interactionism asks what citizens think they are supporting and why similar wars produce different domestic reactions.",
    ),
    "w4_civil_war": (
        "Common pitfall: listing correlates such as poverty, terrain, or weak state capacity as if they are mechanisms by themselves. The exam answer must still explain how those conditions alter bargaining, enforcement, or mobilization.",
        "Compare with: Walter 2002 narrows the civil-war problem to settlement implementation. Blattman and Miguel are broader, warning that prediction and causal explanation are not the same thing.",
    ),
    "w5_walter": (
        "Common pitfall: saying third parties help because they are neutral. Walter's logic is more precise: third parties change the implementation payoff structure by protecting combatants during demobilization.",
        "Compare with: Powell's commitment problem operates under anarchy between states. Walter adapts the same enforcement logic to civil wars, where disarmament and postwar government formation create acute last-move vulnerability.",
    ),
    "w5_democratization": (
        "Common pitfall: saying democracy causes civil war. Cederman, Hug, and Krebs are about democratization and transition risk, especially governmental conflict over central power, not a blanket anti-democracy claim.",
        "Compare with: selectorate logic asks how consolidated institutions change leaders' war incentives. Cederman, Hug, and Krebs ask why incomplete or shifting institutions can make conflict over government more likely.",
    ),
}


VISUAL_SLOTS = {
    "w1_strategic_choice": {
        "asset": ASSET_DIR / "w1_strategic_choice_decision_board.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w1_strategic_choice_decision_board.png",
        "graph": "Actors -> preferences -> strategies -> beliefs -> expected payoffs -> equilibrium, with rejected strategies shown as dimmed paths.",
        "prompt": "Create a clean conceptual study-guide graphic showing two states facing a strategic-choice decision board. Use simple labeled lanes for actors, preferences, strategies, beliefs, payoffs, and equilibrium. Include dimmed rejected options and one highlighted stable outcome. Style: flat editorial infographic, academic, high-contrast navy/gold accents, no decorative clutter, 16:9, readable labels.",
    },
    "w2_preferences_signaling": {
        "asset": ASSET_DIR / "w2_preferences_signaling_filter.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w2_preferences_signaling_filter.png",
        "graph": "Hidden type/resolve -> cheap talk or costly signal -> receiver updates beliefs -> target chooses concession, resistance, or escalation.",
        "prompt": "Create a conceptual infographic of crisis signaling. Show a sender with hidden resolve choosing between cheap talk, tying hands, and sinking costs, then a receiver updating beliefs. Use arrows, small cost icons, and labels for preferences, private information, costly signal, and credibility. Style: clean political-science study graphic, slate navy with amber signal highlights, 16:9, readable labels.",
    },
    "w3_fearon": {
        "asset": ASSET_DIR / "w3_fearon_bargaining_range.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w3_fearon_bargaining_range.png",
        "graph": "War costs create a bargaining range; private information, incentives to misrepresent, commitment problems, or indivisibility can block agreement.",
        "prompt": "Create a bargaining-range diagram for Fearon's rationalist explanations for war. Show a horizontal issue line, each side's war value after costs, the bargaining range between them, and three overlays labeled private information, commitment problem, and issue indivisibility. Style: crisp textbook infographic, minimal icons, blue and gold, 16:9, large readable labels.",
    },
    "w3_powell": {
        "asset": ASSET_DIR / "w3_powell_power_shift_timeline.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w3_powell_power_shift_timeline.png",
        "graph": "Today's bargain -> power shift tomorrow -> future renegotiation threat -> preventive or first-strike incentive now.",
        "prompt": "Create a power-shift timeline for Powell's war as a commitment problem. Show a declining state and rising state across time, with today's bargain becoming non-credible after tomorrow's distribution of power changes. Include labels for commitment problem, preventive war, first-strike advantage, and no central enforcer. Style: restrained academic infographic, navy/red risk accent, 16:9, readable labels.",
    },
    "w3_cases": {
        "asset": ASSET_DIR / "w3_cases_diagnostic_flowchart.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w3_cases_diagnostic_flowchart.png",
        "graph": "Case evidence -> beliefs at the time -> information filters -> mechanism match, with separate branches for 1990-91 Iraq and 2002-03 Iraq.",
        "prompt": "Create a case-diagnostic flowchart for strategic misperception. Show evidence feeding into beliefs-at-the-time, information filters, and mechanism choice. Include two separate Iraq branches labeled 1990-91 U.S. resolve misreading and 2002-03 sanctions/WMD/veto beliefs. Style: clean classroom flowchart, no photos, blue/gray with warning accents, 16:9, readable labels.",
    },
    "w4_audience_costs": {
        "asset": ASSET_DIR / "w4_audience_costs_public_threat.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w4_audience_costs_public_threat.png",
        "graph": "Public threat -> domestic audience observes -> retreat becomes costly -> opponent updates resolve -> crisis ends or escalates.",
        "prompt": "Create an audience-cost crisis-signaling graphic. Show a leader making a public threat, domestic audience watching, retreat cost rising, and an opponent updating beliefs about resolve. Include labels for tying hands, audience costs, public commitment, and backing down. Style: flat editorial infographic, navy/gold, 16:9, readable labels.",
    },
    "w4_selectorate": {
        "asset": ASSET_DIR / "w4_selectorate_winning_coalition.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w4_selectorate_winning_coalition.png",
        "graph": "Selectorate -> winning coalition size -> public/private goods strategy -> war selectivity and effort -> dyadic democratic peace.",
        "prompt": "Create a selectorate-theory infographic comparing small winning coalition and large winning coalition leaders. Show private goods versus public goods, political survival, war selectivity, and trying harder when fighting. Style: clean comparative chart, academic, teal/navy/gold, 16:9, readable labels.",
    },
    "w4_public_opinion": {
        "asset": ASSET_DIR / "w4_public_opinion_interaction_matrix.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w4_public_opinion_interaction_matrix.png",
        "graph": "Foreign-policy disposition + case image cues -> support, opposition, or polarization, with ordinal and disordinal interaction examples.",
        "prompt": "Create a cognitive-interactionist public-opinion graphic. Show stable dispositions such as internationalism and assertiveness crossing with case images such as enemy, ally, and barbarian. Include output cells for support, opposition, and polarization, plus labels ordinal interaction and disordinal interaction. Style: clean matrix infographic, restrained colors, 16:9, readable labels.",
    },
    "w4_civil_war": {
        "asset": ASSET_DIR / "w4_civil_war_correlates_to_mechanisms.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w4_civil_war_correlates_to_mechanisms.png",
        "graph": "Correlates such as low income, weak capacity, and rough terrain feed into mobilization and enforcement mechanisms, not directly into war.",
        "prompt": "Create a civil-war study graphic showing the difference between correlates and mechanisms. On the left list low income, weak state capacity, rough terrain, and slow growth; arrows pass through mobilization, enforcement failure, and security dilemma before reaching civil war onset. Style: clear academic process diagram, earth-neutral with blue accents, 16:9, readable labels.",
    },
    "w5_walter": {
        "asset": ASSET_DIR / "w5_walter_demobilization_endgame.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w5_walter_demobilization_endgame.png",
        "graph": "Peace agreement -> demobilization -> window of vulnerability -> cheat/hegemony temptation unless guarantees and power sharing change payoffs.",
        "prompt": "Create a Walter civil-war settlement implementation diagram. Show combatants signing a peace agreement, then entering demobilization and a window of vulnerability. Add third-party security guarantees and power sharing as safeguards that change the endgame. Style: clean policy infographic, navy/green security accents, 16:9, readable labels.",
    },
    "w5_democratization": {
        "asset": ASSET_DIR / "w5_democratization_governmental_conflict.png",
        "display_asset": f"{ASSET_DISPLAY_DIR}/w5_democratization_governmental_conflict.png",
        "graph": "Democratization opens competition over central government; weak institutions and coercive veto players raise governmental conflict risk, distinct from territorial conflict.",
        "prompt": "Create a democratization-and-civil-war infographic. Show regime opening leading to competition over central government, elite fears, weak institutions, and coercive actors, ending in governmental conflict risk. Include a side branch labeled territorial conflict as a separate logic. Style: crisp academic infographic, navy/gold/red risk accents, 16:9, readable labels.",
    },
}


ELI5_CONCLUSIONS = {
    "w1_strategic_choice": "ELI5 conclusion: Do not just ask what a country wanted. Ask who was choosing, what choices they saw, what they thought the other side would do, and why one choice looked better than the rest.",
    "w2_preferences_signaling": "ELI5 conclusion: A signal only teaches the other side something if it would hurt to fake it. If anyone could say the same words for free, the message is probably cheap talk.",
    "w3_fearon": "ELI5 conclusion: War is like both sides burning money to settle an argument. Fearon asks why they could not make a deal before burning it.",
    "w3_powell": "ELI5 conclusion: Sometimes the problem is not what each side knows today. It is that tomorrow's stronger side cannot promise it will stay nice once it has more power.",
    "w3_cases": "ELI5 conclusion: Bad decisions are not all the same kind of bad. First figure out what the actor believed at that moment, then choose the theory that actually fits.",
    "w4_audience_costs": "ELI5 conclusion: When a leader makes a threat in public, backing down can become embarrassing or dangerous at home. That cost can make the threat more believable abroad.",
    "w4_selectorate": "ELI5 conclusion: Leaders fight differently depending on who can fire them. A leader who needs lots of public support cannot survive failure the same way a patronage ruler can.",
    "w4_public_opinion": "ELI5 conclusion: People do not support wars from facts alone or ideology alone. They mix their usual worldview with how this particular enemy, ally, or crisis looks.",
    "w4_civil_war": "ELI5 conclusion: Poverty or weak government can tell us where civil war is more likely, but the answer still has to explain how people organize, distrust deals, and choose fighting.",
    "w5_walter": "ELI5 conclusion: A peace deal is scariest right when soldiers put down their weapons. Walter says peace needs protection during that moment, not just signatures on paper.",
    "w5_democratization": "ELI5 conclusion: Opening elections can be dangerous when everyone suddenly competes for the central state but nobody yet trusts the rules or the people with guns.",
}


for theory in theories:
    theory["context"] = AUTHOR_CONTEXT[theory["id"]]
    theory["mechanism"] = MECHANISM_DETAIL[theory["id"]]
    theory["deployment"] = EXAM_DEPLOYMENT[theory["id"]]
    theory["pitfall"], theory["contrast"] = PITFALLS_AND_CONTRASTS[theory["id"]]
    theory["visual"] = VISUAL_SLOTS[theory["id"]]
    theory["eli5"] = ELI5_CONCLUSIONS[theory["id"]]


def bullet_list(items):
    return [Paragraph(f"- <b>{term}</b> - {body}", styles["TheoryBullet"]) for term, body in items]


def plain_bullets(items):
    return [Paragraph(f"- {item}", styles["TheoryBullet"]) for item in items]


def header_table(t):
    data = [[Paragraph(f"{t['session']} - {t['title']}", styles["Header"])],
            [Paragraph(t["author"], styles["HeaderSub"])]]
    tbl = Table(data, colWidths=[7.05 * inch], style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MED_BLUE if t["session"].startswith("W5") else DARK_NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tbl


def section(title, flowables):
    return [Paragraph(title, styles["Section"])] + flowables


def visual_slot(t):
    visual = t["visual"]
    asset = visual["asset"]
    if not asset.exists():
        raise FileNotFoundError(f"Missing visual asset for {t['id']}: {asset}")
    image = Image(str(asset), width=7.05 * inch, height=3.97 * inch)
    data = [[
        [
            image,
            Spacer(1, 3),
            Paragraph("Concept graph", styles["VisualLabel"]),
            Paragraph(visual["graph"], styles["VisualBody"]),
            Paragraph(f"Embedded asset: {visual['display_asset']}", styles["Small"]),
        ]
    ]]
    tbl = Table(data, colWidths=[7.05 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F8FA")),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tbl


def theory_page(t):
    story = [BookmarkAnchor(t["id"], f"{t['session']} - {t['title']}"), header_table(t), Spacer(1, 5)]
    story += section("AUTHOR / READING CONTEXT", [Paragraph(t["context"], styles["Body"])])
    story += section("SITUATION", [Paragraph(t["situation"], styles["Body"])])
    story += section("CORE INTUITION", [Paragraph(t["intuition"], styles["Body"])])
    story += section("MECHANISM", [Paragraph(t["mechanism"], styles["Body"])])
    story += section("VISUAL SLOT / CONCEPT GRAPH", [visual_slot(t)])
    story += section("KEY CONCEPTS, KEYWORDS & TERMINOLOGY", bullet_list(t["concepts"]))
    story += section("ASSUMPTIONS", plain_bullets(t["assumptions"]))

    col_w = (7.05 * inch - 10) / 2
    left = [Paragraph("<b>Strengths</b>", styles["Body"])] + plain_bullets(t["strengths"])
    right = [Paragraph("<b>Weaknesses</b>", styles["Body"])] + plain_bullets(t["weaknesses"])
    table = Table([[left, right]], colWidths=[col_w, col_w])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
        ("BACKGROUND", (1, 0), (1, 0), WARM_AMBER),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ("LINEAFTER", (0, 0), (0, -1), 0.5, BORDER_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += section("EXAM DEPLOYMENT LOGIC", [Paragraph(t["deployment"], styles["Body"])])
    story += [Paragraph("STRENGTHS / WEAKNESSES", styles["Section"]), table]
    story += section("COMMON PITFALL", [Paragraph(t["pitfall"], styles["Body"])])
    story += section("COMPARE WITH", [Paragraph(t["contrast"], styles["Body"])])
    story += section("ELI5 CONCLUSION", [Paragraph(t["eli5"], styles["Body"])])
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(doc.leftMargin, 0.38 * inch, TITLE)
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.55 * inch,
    )
    story = [
        Paragraph(TITLE, styles["CoverTitle"]),
        Paragraph("GPCO 410 International Politics & Security | Prof. Lauren Prather | UC San Diego GPS | Spring 2026", styles["CoverSub"]),
    ]
    desc = Paragraph(
        "Exam-ready midterm reference for W1-W5 theory. This v1.3.1 revision preserves the v1.2.0 source-faithful theory architecture and the v1.3.0 ELI5 additions, then embeds the completed conceptual PNG assets for all 11 major theory/topic entries. Use it to identify the right mechanism for a case, name the assigned-reading vocabulary, sketch a concept graph, and compare strengths and limits during exam prep.",
        styles["Box"],
    )
    box = Table([[desc]], colWidths=[7.05 * inch])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [box, Spacer(1, 7), Paragraph("Table of Contents", styles["Section"])]
    for t in theories:
        story.append(Paragraph(f'<a href="#{t["id"]}">{t["session"]} - {t["title"]}</a>', styles["TOC"]))
    story += [
        Spacer(1, 8),
        HRFlowable(width="35%", thickness=0.5, color=BORDER_GREY, hAlign="LEFT"),
        Paragraph(
            f"Generated with {MODEL} via the Claudia agent system. Prepared for Edgar Agunias, GPCO 410 International Politics & Security, Prof. Lauren Prather, UC San Diego GPS. Always verify against official course materials and readings; this is a study aid, not a substitute for assigned texts.",
            styles["Small"],
        ),
        PageBreak(),
    ]
    for i, t in enumerate(theories):
        if i:
            story.append(PageBreak())
        story.extend(theory_page(t))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
