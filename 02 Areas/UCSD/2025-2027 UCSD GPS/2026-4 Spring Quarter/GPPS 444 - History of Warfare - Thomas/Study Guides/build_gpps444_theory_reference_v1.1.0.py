from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image as RLImage,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = "GPPS444_theory_reference_v1.1.0.pdf"
DOC_TITLE = "GPPS 444 Theory Reference v1.1.0"
ASSET_DIR = Path("assets/gpps444_theory_reference_v1.1.0")
ASSET_DIR.mkdir(parents=True, exist_ok=True)

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
WARM_AMBER = colors.HexColor("#FFF5E6")
ACCENT_GOLD = colors.HexColor("#C69C3F")
DEEP_GREEN = colors.HexColor("#276749")
INK = colors.HexColor("#222222")


class BookmarkAnchor(Flowable):
    def __init__(self, name, title=""):
        super().__init__()
        self.width = 0
        self.height = 0
        self._name = name
        self._title = title

    def draw(self):
        self.canv.bookmarkPage(self._name, fit="XYZ", left=0, top=self.canv._pagesize[1])
        if self._title:
            self.canv.addOutlineEntry(self._title, self._name, level=0)


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=23, alignment=TA_CENTER, textColor=DARK_NAVY, spaceAfter=6))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=9, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=5))
styles.add(ParagraphStyle(name="TOC", parent=styles["Normal"], fontSize=7.8, leading=9.2, spaceBefore=0, spaceAfter=0.5, textColor=MED_BLUE))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontSize=9.2, leading=10.5, textColor=DARK_NAVY, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], fontSize=7.05, leading=8.2, spaceAfter=2))
styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontSize=6.35, leading=7.25, spaceAfter=1.2))
styles.add(ParagraphStyle(name="Dense", parent=styles["Normal"], fontSize=6.05, leading=6.9, spaceAfter=0.7))
styles.add(ParagraphStyle(name="Tiny", parent=styles["Normal"], fontSize=5.85, leading=6.6, textColor=colors.HexColor("#555555")))
styles.add(ParagraphStyle(name="RefBullet", parent=styles["Body"], leftIndent=7, firstLineIndent=0))
styles.add(ParagraphStyle(name="DenseBullet", parent=styles["Dense"], leftIndent=6, firstLineIndent=0))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def para(text, style="Body"):
    return Paragraph(esc(text), styles[style])


def bullet_list(items, style="RefBullet"):
    return ListFlowable(
        [ListItem(Paragraph(esc(item), styles[style]), bulletColor=DARK_NAVY) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=8,
        bulletFontSize=4.7,
    )


def text_block(title, items, style="Dense"):
    return [
        Paragraph(f"<b>{esc(title)}</b>", styles["Small"]),
        bullet_list(items, "DenseBullet" if style == "Dense" else "Small"),
    ]


THEORIES = [
    {
        "anchor": "battle_outcome_framework",
        "session": "Course-wide",
        "title": "Thomas Battle-Outcome Framework",
        "reading": "Thomas syllabus themes; slides and terminology handout",
        "visual": ["Mass", "Mobility", "Logistics", "Leadership"],
        "caption": "Mechanism: battle outcomes emerge when mass, mobility, adaptability, logistics, leadership, terrain, technology, weather, and chance interact. Assumption: no single variable explains every case. Strength/limit cue: excellent for quiz diagnosis, weak if used as a checklist without a causal claim.",
        "situation": "Use this framework whenever Thomas asks why one side won a battle or campaign, from Salamis to Midway.",
        "intuition": "Thomas wants causal military judgment, not memorized chronology. The analyst identifies the decisive variable in a specific case, then explains how supporting variables either amplified or neutralized it. Technology is never automatic; it works through organization, terrain, weather, logistics, and leadership.",
        "concepts": ["Mass: force available at the decisive point, only useful if organized and supplied.", "Mobility: the ability to maneuver across land, sea, air, or operational theaters.", "Adaptability: institutional capacity to learn after failure and change methods.", "Supply chains: food, fodder, credit, ammunition, transport, and administration.", "Operational leadership: command judgment under uncertainty and friction.", "Offense-defense balance: whether attack can force decision or defense can absorb and exhaust."],
        "assumptions": ["Battle and campaign outcomes can be explained through interacting variables.", "The decisive factor changes by case and period.", "Good answers rank causes rather than listing them."],
        "strengths": ["Works across the full course.", "Prevents technology-only or hero-only explanations.", "Maps directly to Thomas's recurring quiz language."],
        "weaknesses": ["Can become a generic checklist.", "Needs period-specific meaning for each variable.", "Can underplay politics if kept only at battlefield level."],
        "refs": "Thomas (2026); Parker (2020).",
    },
    {
        "anchor": "western_way_of_war",
        "session": "Sessions 1-2 and Epilogue",
        "title": "Western Way of War",
        "reading": "Parker, TCHW Introduction and Epilogue",
        "visual": ["Discipline", "Capital", "Adaptation", "Decisive Battle"],
        "caption": "Mechanism: political competition, finance, drill, and technology make violence repeatable and exportable. Assumption: institutions can learn and fund war over time. Strength/limit cue: powerful as a course arc, dangerous if treated as a simple superiority story.",
        "situation": "This explains why the course tracks disciplined infantry, state finance, gunpowder, and industrial mobilization as a cumulative military tradition.",
        "intuition": "Parker's western way of war is a tradition built from disciplined formations, aggressive battle-seeking, technological adaptation, and capital-intensive state capacity. It is useful because each session asks how a military system extends, limits, or complicates that pattern. The important caveat is that Asia, the Ottoman Empire, and nonstate actors also innovate and often expose Western blind spots.",
        "concepts": ["Decisive battle: a preference for resolving conflict by destroying the enemy main force.", "Discipline: training and order that keep formations coherent under fear.", "Capital intensity: substituting money, equipment, and technology for sheer manpower.", "Institutional learning: preserving lessons in drill, doctrine, and administration.", "Eclecticism: borrowing any useful weapon, tactic, or organization.", "Credit networks: financing long wars without paying every cost immediately."],
        "assumptions": ["States preserve and transmit battlefield learning.", "Political competition rewards military adaptation.", "Finance and administration can support expensive military systems."],
        "strengths": ["Gives GPPS 444 its long arc.", "Links battle tactics to states and economies.", "Explains repeated Western adaptation after military shocks."],
        "weaknesses": ["Risks Eurocentrism.", "Can flatten non-Western military systems.", "Overfocuses on battle unless logistics and politics are included."],
        "refs": "Parker (2020); Thomas (2026).",
    },
    {
        "anchor": "hoplite_phalanx",
        "session": "Session 2",
        "title": "Hoplite-Phalanx Citizen Soldier Model",
        "reading": "Hanson, TCHW Chs. 1-2; Greek warfare slides",
        "visual": ["Narrow Ground", "Shield Wall", "Citizen Cohesion", "Mass Compressed"],
        "caption": "Mechanism: disciplined heavy infantry on restricted terrain compresses enemy mass and magnifies cohesion. Assumption: the phalanx holds formation. Strength/limit cue: strong in chosen terrain, brittle against flexible maneuver or cavalry in open ground.",
        "situation": "Thermopylae and Salamis show smaller Greek forces using terrain, cohesion, and civic commitment to offset Persian mass.",
        "intuition": "Greek warfare links military organization to political identity. The hoplite phalanx turned citizen infantry into a dense weapon system: shields, spears, frontage, and morale mattered together. The model introduces one of the course's core lessons: numbers are not decisive when terrain and organization prevent them from being used.",
        "concepts": ["Hoplite: heavily armed infantryman with spear and shield.", "Phalanx: dense formation whose power depends on shared frontage and cohesion.", "Citizen soldier: political identity tied to military service.", "Restricted terrain: geography that denies envelopment and limits enemy mass.", "Force multiplier: a condition that lets a smaller force fight larger."],
        "assumptions": ["The unit can maintain cohesion.", "Terrain denies enemy maneuver.", "Morale and leadership sustain close combat."],
        "strengths": ["Explains Greek resistance to Persian numerical superiority.", "Shows how terrain can reverse the mass advantage.", "Connects warfare to civic order."],
        "weaknesses": ["Rigid in rough or open maneuver warfare.", "Vulnerable if flanked or disrupted.", "Can romanticize civic morale over logistics and alliance politics."],
        "refs": "Hanson (2005a, 2005b); Thomas (2026).",
    },
    {
        "anchor": "roman_adaptation",
        "session": "Sessions 3-4",
        "title": "Roman Adaptability and Engineering",
        "reading": "Hanson, TCHW Chs. 2-3; Roman warfare slides",
        "visual": ["Defeat", "Learning", "Legion", "Engineering"],
        "caption": "Mechanism: Rome absorbs defeat, adapts organization, and turns engineering into operational power. Assumption: the state survives long enough to learn. Strength/limit cue: explains Alesia and expansion, but professionalization can redirect loyalty from state to commander.",
        "situation": "Rome survived Cannae, adapted against Carthage and Hellenistic phalanxes, and used roads, camps, and siege works to expand.",
        "intuition": "Roman warfare is the course's early model of institutional resilience. Rome did not win because it never failed; it won because it learned from failure, copied useful practices, reorganized formations, and used engineering to convert labor into combat power. That same expansion created political strains as soldiers became tied to generals.",
        "concepts": ["Maniple and legion: flexible tactical organization compared with rigid phalanx.", "Castrametation: disciplined camp building and field organization.", "Lines of communication: roads and routes that link armies to supply and control.", "Siege engineering: walls, ramps, circumvallation, and countervallation.", "Professionalization: soldiers increasingly dependent on commanders and rewards."],
        "assumptions": ["Institutions can absorb catastrophic defeat.", "Engineering labor can be mobilized and protected.", "Political institutions can sustain long wars."],
        "strengths": ["Explains Alesia as engineering plus leadership.", "Makes adaptability a concrete institutional trait.", "Links battlefield success to empire-building."],
        "weaknesses": ["Professional armies can threaten republican control.", "Engineering systems are vulnerable to ambush and local knowledge.", "Expansion stretches governance and logistics."],
        "refs": "Hanson (2005b, 2005c); Thomas (2026).",
    },
    {
        "anchor": "fortress_siege",
        "session": "Session 5",
        "title": "Castle, Fortress, and Siege Dominance",
        "reading": "Bachrach, TCHW Ch. 4; Intro to Irregular Warfare handout",
        "visual": ["Fortress", "Route Control", "Time Cost", "Food Cost"],
        "caption": "Mechanism: fortifications convert territory into defended strongpoints and make attackers pay in time, labor, food, and engineering. Assumption: the strongpoint can hold long enough to matter. Strength/limit cue: explains defense dominance, but raids can bypass walls.",
        "situation": "Medieval castles controlled routes and populations even when no decisive field battle occurred.",
        "intuition": "Stone fortifications shift war from finding and destroying an enemy army to controlling places. The attacker must assault, starve, negotiate, mine, bombard, or bypass the fortress. Because each option is slow and expensive, medieval strategy often revolves around supply, patience, and political control rather than dramatic battle.",
        "concepts": ["Fortification: fixed defense protecting people, stores, and authority.", "Siege: compelling surrender by assault, blockade, starvation, or negotiation.", "Defense dominance: attack is slower, costlier, and less certain than defense.", "Terrain control: strongpoints shape movement without continuous front lines.", "Logistical drag: sieges consume transport, food, fodder, and time."],
        "assumptions": ["The fortification can be supplied or endure.", "Attackers lack quick wall-breaking technology.", "Political control depends on places as well as armies."],
        "strengths": ["Explains why medieval war centers on sieges.", "Connects defense, logistics, and political control.", "Sets up the gunpowder and trace italienne transition."],
        "weaknesses": ["Static defense can be bypassed.", "Castles cannot protect all economic assets.", "Improved artillery eventually defeats old walls."],
        "refs": "Bachrach (2005); Thomas (2026).",
    },
    {
        "anchor": "chevauchee",
        "session": "Sessions 5-6",
        "title": "Chevauchee and Economic Warfare",
        "reading": "Allmand, TCHW Ch. 5; Ares chevauchee explainer",
        "visual": ["Fast Raid", "Tax Base", "Political Pain", "Bad Battle"],
        "caption": "Mechanism: mobile devastation bypasses fortresses and attacks the ruler's tax base and legitimacy. Assumption: the defender must visibly protect subjects. Strength/limit cue: good coercion by punishment, weak for holding territory.",
        "situation": "Edward III and the Black Prince used mounted devastation to force French rulers into bad political and battlefield choices.",
        "intuition": "The chevauchee is a mobility solution in a defense-dominant world. Instead of reducing every castle, a raiding column destroys villages, crops, and confidence in royal protection. Battle is often a secondary effect: the defender is provoked into fighting on unfavorable terms or suffers public humiliation.",
        "concepts": ["Operational raid: fast destruction designed to induce response, not govern territory.", "Tax base: productive economy that funds war-making.", "Provocation: forcing the ruler to fight badly or look weak.", "Living off the land: supply through seizure and foraging.", "Fabian response: refusing battle while sheltering population and shadowing the raid."],
        "assumptions": ["The defender's legitimacy depends on protection.", "Raiders move faster than interception forces.", "Economic destruction creates bargaining pressure."],
        "strengths": ["Explains Crecy, Poitiers, and political devastation.", "Connects medieval war to coercion theory.", "Shows mobility countering fortification."],
        "weaknesses": ["Cannot govern what it ruins.", "Can be blunted by refusal of battle.", "May destroy resources needed later."],
        "refs": "Allmand (2005); Ares (2026a); Thomas (2026).",
    },
    {
        "anchor": "infantry_missile_revolution",
        "session": "Session 6",
        "title": "Infantry, Missile, and Polearm Revolution",
        "reading": "Allmand, TCHW Ch. 5; Session 6 one-pager",
        "visual": ["Longbow", "Stakes", "Mud", "Cavalry Shock Fails"],
        "caption": "Mechanism: disciplined infantry, missiles, polearms, and prepared ground neutralize mounted aristocratic shock. Assumption: infantry has cohesion and terrain protection. Strength/limit cue: tactics make weapons decisive; weapons alone do not.",
        "situation": "At Agincourt, longbows, stakes, mud, and dismounted men-at-arms made French mounted shock fail.",
        "intuition": "The late medieval transition is not simply new weapons replacing knights. It is a tactical shift in which cheaper infantry weapons became decisive only when paired with discipline, ground choice, preparation, and command. This points toward more permanent, paid, inspectable forces.",
        "concepts": ["Longbow: high-rate missile weapon effective when massed.", "Crossbow: slower but accessible to less trained troops.", "Pike and halberd: polearms that disrupt cavalry shock.", "Dismounted men-at-arms: elites used as infantry when mounted attack is unsafe.", "Indenture contract: paid service with accountability and inspection.", "Compagnies d'Ordonnance: French permanent companies pointing toward standing armies."],
        "assumptions": ["Infantry has discipline and chosen ground.", "Cavalry cannot bypass the position.", "Weapons are integrated into a tactical system."],
        "strengths": ["Explains the declining battlefield dominance of armored cavalry.", "Links weapons, cost, social order, and tactics.", "Prepares the transition to gunpowder."],
        "weaknesses": ["Cavalry remains useful in changed roles.", "Missile infantry can be vulnerable without protection.", "Early gunpowder is not yet consistently decisive in the field."],
        "refs": "Allmand (2005); Ares (2026b); Thomas (2026).",
    },
    {
        "anchor": "gunpowder_trace_italienne",
        "session": "Session 7",
        "title": "Gunpowder Revolution and Trace Italienne",
        "reading": "Parker, TCHW Ch. 6; Week 4 reference",
        "visual": ["Cannon", "Old Wall Breaks", "Bastion", "Fiscal State"],
        "caption": "Mechanism: artillery defeats vertical walls, bastioned fortresses restore defense, and war becomes more expensive. Assumption: states can fund engineers, guns, and garrisons. Strength/limit cue: excellent for state-capacity logic, incomplete if battlefield tactics are ignored.",
        "situation": "Cannon made medieval walls fall faster, but the trace italienne forced bigger armies, longer sieges, and heavier fiscal systems.",
        "intuition": "Parker's military revolution is a system, not a single invention. Improved gunpowder, trunnions, metallurgy, and artillery weakened old fortifications; low, thick, angled bastions then restored defensive strength. The long-run result was larger armies, more engineers, more garrisons, and states organized around paying for war.",
        "concepts": ["Corned gunpowder: granulated powder that improved power and reliability.", "Trunnion carriage: mounting that improved aiming and reload efficiency.", "Trace italienne: low bastioned fortress built to absorb and flank cannon fire.", "Military Revolution: linked changes in technology, tactics, fortification, army size, and finance.", "Fiscal-military state: state organized to tax, borrow, and administer sustained war."],
        "assumptions": ["Engineering knowledge diffuses.", "States can fund new fortifications and siege trains.", "Fortress networks shape strategy as much as field battle."],
        "strengths": ["Explains why war becomes larger and costlier.", "Connects technology to state capacity.", "Frames the Roberts-Parker debate."],
        "weaknesses": ["Can overstate Europe if Ottoman and Asian gunpowder are ignored.", "Battlefield innovation still matters.", "Timing varies by region."],
        "refs": "Parker (2005a); Thomas (2026).",
    },
    {
        "anchor": "ottoman_standing_army",
        "session": "Session 8",
        "title": "Ottoman Expansion and Standing Military Institutions",
        "reading": "Session 8 one-pager; lecture supplement noted in syllabus extract",
        "visual": ["Janissaries", "Siege Artillery", "Frontier", "Imperial Logistics"],
        "caption": "Mechanism: standing infantry, artillery, and imperial logistics extend Ottoman power across fortified frontiers. Assumption: central institutions can recruit, supply, and discipline forces. Strength/limit cue: corrects a Eurocentric arc, but local notes are needed because TCHW under-treats Ottoman land institutions.",
        "situation": "Mohacs and Vienna show Ottoman standing forces, siege artillery, and logistics creating a durable early modern threat.",
        "intuition": "The Ottoman case complicates any simple Western-way narrative. Janissaries, siege artillery, and frontier administration show sophisticated non-Western military institutions. For Thomas, the key move is comparison: what did Ottoman standing forces and logistics do well, where did adaptation slow, and how did European fiscal-military systems eventually catch up?",
        "concepts": ["Janissaries: elite standing infantry tied to central authority.", "Devshirme: recruitment and service system connected to Ottoman state formation.", "Siege artillery: large guns used to break fortified places.", "Habsburg-Ottoman frontier: long fortified border where logistics and dynastic strategy interacted.", "Galley warfare: Mediterranean naval system relevant to Lepanto and Ottoman maritime power."],
        "assumptions": ["Lecture supplements the reading for Ottoman land institutions.", "Standing forces can be supplied across imperial distances.", "Land, sea, and frontier contexts must be separated."],
        "strengths": ["Corrects Eurocentric overreach.", "Highlights standing army and artillery outside Western Europe.", "Connects Mohacs, Vienna, and Lepanto to course themes."],
        "weaknesses": ["Assigned chapter coverage is thin.", "Risks flattening a long empire into rise-and-decline.", "Needs careful periodization."],
        "refs": "Parker (2005b); Thomas (2026).",
    },
    {
        "anchor": "dynastic_firepower",
        "session": "Session 8 / Breitenfeld bridge",
        "title": "Dynastic War, Volley Fire, and Combined Arms",
        "reading": "Parker, TCHW Ch. 9; Breitenfeld materials",
        "visual": ["Volley Fire", "Light Artillery", "Cavalry", "Flexible Formation"],
        "caption": "Mechanism: drill, volley fire, regimental artillery, and cavalry coordination turn gunpowder into battlefield effect. Assumption: troops can execute discipline under fire. Strength/limit cue: explains Breitenfeld, but the advantage was copyable and strategy remained siege-heavy.",
        "situation": "At Breitenfeld in 1631, the Swedish system beat deeper Imperial formations through firepower, discipline, and combined arms.",
        "intuition": "Gunpowder only changes battle when it is embedded in organization. Maurice of Nassau's countermarch and Gustavus Adolphus's Swedish system show how training, standardized guns, flexible formations, and disciplined cavalry created practical battlefield power. Breitenfeld mattered because it made the system visible, not because it ended adaptation.",
        "concepts": ["Volley fire: coordinated musket discharge for concentrated effect.", "Countermarch: ranks rotate to sustain fire.", "Tercio: deep pike-and-shot infantry formation.", "Regimental artillery: lighter guns integrated with infantry.", "Combined arms: infantry, cavalry, artillery, and command systems supporting one another."],
        "assumptions": ["Troops can drill enough to sustain fire discipline.", "Artillery is standardized and mobile enough.", "Commanders coordinate arms under stress."],
        "strengths": ["Explains Breitenfeld beyond raw numbers.", "Shows adaptation from pike shock to fire systems.", "Connects tactics to the military revolution debate."],
        "weaknesses": ["Copyable systems lose novelty.", "Sieges and logistics still dominate strategy.", "Mercenary and fiscal limits constrain innovation."],
        "refs": "Parker (2005c); Ares (2026c); Thomas (2026).",
    },
    {
        "anchor": "nation_in_arms",
        "session": "Session 9",
        "title": "Nation in Arms and Napoleonic Operational System",
        "reading": "Lynn, TCHW Ch. 11; Session 9 one-pager",
        "visual": ["Conscription", "Corps Columns", "Concentration", "Austerlitz"],
        "caption": "Mechanism: revolutionary citizenship supplies mass, while corps organization turns mass into mobile concentration. Assumption: terrain can feed dispersed corps and enemies can be isolated. Strength/limit cue: explains Austerlitz, but not Britain's naval-financial counter.",
        "situation": "Austerlitz shows Napoleon using national manpower, corps mobility, deception, and concentration to destroy a coalition army.",
        "intuition": "The French Revolution politicized war by making citizens fight as members of a nation. Napoleon converted that manpower into operational power through corps organization, artillery, meritocratic command, foraging logistics, and deception. Politics supplied mass; organization made that mass fast and decisive.",
        "concepts": ["Nation in arms: citizens mobilized for national war.", "Conscription: state extraction of manpower.", "Corps system: semi-independent combined-arms formations.", "Manoeuvre sur les derrieres: move against flank or rear to cut retreat.", "Nelson Touch: British naval initiative and seamanship at Trafalgar."],
        "assumptions": ["National motivation and administration sustain mass armies.", "Foraging terrain can feed dispersed corps.", "Enemies can be defeated separately before coalitions unite."],
        "strengths": ["Explains Austerlitz as mobility and leadership.", "Connects politics to military capacity.", "Shows why Britain countered through sea control and finance."],
        "weaknesses": ["Depends on supply-rich terrain.", "Creates enemies who learn and copy.", "Cannot defeat Britain through land victory alone."],
        "refs": "Lynn (2005b); Ares (2026d); Thomas (2026).",
    },
    {
        "anchor": "napoleonic_limits",
        "session": "Session 10",
        "title": "Limits of Mass, Mobility, and Coalition War",
        "reading": "Lynn, TCHW Ch. 11; Session 10 one-pager",
        "visual": ["Distance", "Scorched Earth", "Weather", "Coalition Learning"],
        "caption": "Mechanism: operational mobility outruns logistics, while defensive depth and coalition learning absorb Napoleon's shocks. Assumption: defenders can trade space for time without political collapse. Strength/limit cue: explains Russia and Waterloo, but can become hindsight if inevitability is assumed.",
        "situation": "Russia 1812 and Waterloo show Napoleon's system breaking against distance, climate, scorched earth, coalition learning, and British finance.",
        "intuition": "Napoleon's strengths became liabilities at continental scale. Corps mobility and foraging worked in rich terrain against isolated opponents; they failed when Russia used depth, climate, and political refusal. By 1815, coalitions had learned the method and could bring numbers, finance, and coordination against him.",
        "concepts": ["Scorched earth: denying supplies to make mobility self-destructive.", "Strategic depth: trading space for time.", "Coalition learning: enemies adopting the methods that beat them.", "Sea control plus finance: Britain's ability to fund and reconstitute coalitions.", "Culminating point: when attack outruns its logistical and political base."],
        "assumptions": ["Defenders can absorb invasion without surrender.", "Coalition partners can coordinate.", "Logistics and weather can overpower battlefield genius."],
        "strengths": ["Explains Russia without winter myth alone.", "Frames Waterloo as a coalition-system victory.", "Connects all five Thomas themes."],
        "weaknesses": ["Can understate Napoleon's tactical skill.", "Requires careful chronology.", "Risks treating coalition resilience as inevitable."],
        "refs": "Lynn (2005b); Ares (2026e); Thomas (2026).",
    },
    {
        "anchor": "industrialized_war",
        "session": "Session 11",
        "title": "Industrialization of War, 1815-1871",
        "reading": "Murray, TCHW Ch. 12; Session 11 syllabus block",
        "visual": ["Rail", "Rifles", "Telegraph", "Mass Firepower"],
        "caption": "Mechanism: industrial tools increase range, movement, command speed, and firepower faster than tactics adapt. Assumption: states can mobilize transport, industry, and manpower. Strength/limit cue: explains Crimea and the U.S. Civil War as transition cases, but does not yet produce mature combined arms.",
        "situation": "Crimea and the American Civil War show rifles, railroads, telegraphy, and mass production changing war before commanders fully understood the consequences.",
        "intuition": "Industrialization multiplies both reach and lethality. Railways move armies and supplies; telegraphs move orders; rifled weapons extend killing zones; mass production sustains huge armies. The mismatch is that old habits of attack and command often survive into a new technological environment, creating bloody lessons before doctrine catches up.",
        "concepts": ["Rifled musket: greater range and accuracy than smoothbore weapons.", "Rail mobilization: moving troops and supplies at operational scale.", "Telegraph command: faster communication between capitals and fronts.", "Trench precursor: field fortifications responding to modern firepower.", "Industrial base: factories, arsenals, and transport networks sustaining war."],
        "assumptions": ["Industrial infrastructure can be militarized.", "Commanders can integrate new tools into operations.", "Political systems can sustain mass casualties and mobilization."],
        "strengths": ["Explains why battlefield defense strengthened.", "Links war to industrial society.", "Connects Crimea, Civil War, and Franco-Prussian War transitions."],
        "weaknesses": ["Tactics lag technology.", "Railways can create predictable lines.", "Communication speed does not guarantee good strategy."],
        "refs": "Murray (2005a); Thomas (2026).",
    },
    {
        "anchor": "towards_world_war",
        "session": "Session 12",
        "title": "Towards World War I: Firepower and Stalemate",
        "reading": "Murray, TCHW Ch. 13; Session 12 syllabus block",
        "visual": ["Machine Gun", "Artillery", "Barbed Wire", "Trench"],
        "caption": "Mechanism: rapid-fire weapons, artillery, and barbed wire strengthen prepared defense faster than armies solve offensive movement. Assumption: attackers still seek decisive maneuver under old expectations. Strength/limit cue: explains early WWI stalemate, but not the later adaptation cycle.",
        "situation": "The Somme and early trench warfare reveal how industrial firepower made massed attack catastrophic without synchronized combined arms.",
        "intuition": "By 1914, armies had enormous manpower and modern weapons but incomplete doctrine for breaking defended fronts. Firepower was easy to concentrate; movement was hard to protect. The result was trench systems, artillery dependency, attrition, and a gap between political expectations of decisive victory and operational reality.",
        "concepts": ["Machine gun: defensive automatic fire multiplying small-unit lethality.", "Mass artillery: primary killer and suppressive tool of WWI.", "Barbed wire: cheap obstacle that fixes attackers under fire.", "Trench system: defense in depth built around survival and attrition.", "Mobilization timetable: prewar planning that pressures states toward rapid escalation."],
        "assumptions": ["Defenders can dig and supply deep positions.", "Attackers lack reliable mobility across the killing zone.", "Political leaders remain committed despite casualty shock."],
        "strengths": ["Explains the offense-defense reversal of 1914-1916.", "Connects technology, doctrine, and state mobilization.", "Clarifies why mass alone became a casualty generator."],
        "weaknesses": ["Can make stalemate seem static rather than adaptive.", "Understates Eastern, Balkan, and Ottoman variation.", "Needs Session 13 to explain 1918 breakthroughs."],
        "refs": "Murray (2005b); Thomas (2026).",
    },
    {
        "anchor": "wwi_combined_arms",
        "session": "Session 13",
        "title": "WWI Adaptation, Air Power, and Combined Arms",
        "reading": "Murray, TCHW Ch. 14; Session 13 one-pager",
        "visual": ["Artillery", "Infantry", "Tanks", "Aircraft"],
        "caption": "Mechanism: offensive power returns when fire, movement, armor, aircraft, logistics, and reserves synchronize. Assumption: armies learn and coordinate under industrial strain. Strength/limit cue: explains Amiens and Megiddo, but air power is not yet independently decisive.",
        "situation": "Amiens, Riga, Megiddo, and Saint-Mihiel show armies slowly learning to break trench deadlock through coordinated systems.",
        "intuition": "The answer to WWI stalemate was not a single wonder weapon. It was synchronization: artillery suppression, infantry tactics, tanks, aircraft reconnaissance, logistics, deception, reserves, and command. Air power began as eyes for artillery, then expanded into air superiority, interdiction, close support, and strategic bombing experiments.",
        "concepts": ["Creeping barrage: artillery screen advancing ahead of infantry.", "Storm-troop tactics: infiltration against weak points and rear areas.", "Tank: armored mobility to cross wire and fire zones.", "Reconnaissance aviation: aircraft observing movement and correcting artillery.", "Tactical vs strategic air power: support to battlefield forces versus attacks on enemy economy or will."],
        "assumptions": ["Institutions can learn from costly failure.", "Communications and logistics can sustain combined action.", "Enemy morale and reserves can be exhausted."],
        "strengths": ["Explains why 1918 differs from 1914.", "Shows adaptation under pressure.", "Connects air power to ground war rather than treating it as magic."],
        "weaknesses": ["Learning was slow and expensive.", "Breakthrough did not always become exploitation.", "Air power remained immature."],
        "refs": "Murray (2005c); Ares (2026f); Thomas (2026).",
    },
    {
        "anchor": "wwii_blitzkrieg",
        "session": "Session 14",
        "title": "WWII Air-Land Battle and Blitzkrieg",
        "reading": "Murray, TCHW Ch. 15; Session 14 one-pager",
        "visual": ["Armor", "Air Support", "Radio", "Operational Tempo"],
        "caption": "Mechanism: armor, airpower, radios, and initiative move faster than enemy decision cycles. Assumption: logistics and reserves can keep up. Strength/limit cue: explains France 1940, but Barbarossa exposes strategic and supply limits.",
        "situation": "France 1940 shows German combined-arms tempo shattering rigid defenses, while Barbarossa shows that operational brilliance can outrun strategy and logistics.",
        "intuition": "Blitzkrieg is best understood as a combined-arms and command system. Tanks, aircraft, radios, initiative, and mission-type orders created shock when aimed at an enemy with rigid doctrine and slow decisions. The method became brittle against depth, industrial scale, harsh weather, ideological brutality, and supply limits.",
        "concepts": ["Blitzkrieg: rapid combined-arms penetration and exploitation.", "Operational tempo: acting faster than the opponent can decide.", "Mission command: subordinate initiative within commander's intent.", "Air superiority: control of air needed to support maneuver.", "Strategic overreach: tactical success failing to produce attainable political ends."],
        "assumptions": ["Enemy defense is brittle or slow.", "Fuel, infantry, and reserves can follow armor.", "Political objectives match operational reach."],
        "strengths": ["Explains Poland, France, and early Barbarossa.", "Shows doctrine and command matter as much as tanks.", "Links mobility to decision cycles."],
        "weaknesses": ["Fails against depth and logistical exhaustion.", "Can confuse operational victory with strategic success.", "Depends heavily on enemy errors."],
        "refs": "Murray (2005d); Ares (2026g); Thomas (2026).",
    },
    {
        "anchor": "air_sea_undersea",
        "session": "Session 15",
        "title": "Undersea and Air-Sea Battle",
        "reading": "Murray, TCHW Ch. 16; Session 15 one-pager",
        "visual": ["Convoys", "Codebreaking", "Carriers", "Submarines"],
        "caption": "Mechanism: sea control becomes a system of intelligence, production, escorts, air cover, carriers, and submarines. Assumption: industrial replacement and communications hold. Strength/limit cue: explains Atlantic and Midway, but no single platform wins alone.",
        "situation": "The Battle of the Atlantic and Midway show maritime war becoming a contest of systems rather than isolated surface fleet battle.",
        "intuition": "World War II sea power was about sustaining global movement. U-boats threatened sea lines, but convoy tactics, escorts, aircraft, codebreaking, and shipbuilding adapted. Carriers replaced battleships as mobile airfields, while submarines strangled Japanese logistics. Sea control was the precondition for projecting land and air power.",
        "concepts": ["Sea lines of communication: maritime routes that sustain war.", "Convoy system: protected group movement against submarines.", "Carrier aviation: mobile air power projected from ships.", "Codebreaking: intelligence advantage that shapes timing and risk.", "Commerce raiding: attacking logistics rather than main fleets."],
        "assumptions": ["Sea control is necessary for theater sustainment.", "Industrial powers can replace losses.", "Intelligence can be converted into operational timing."],
        "strengths": ["Explains Allied adaptation in the Atlantic.", "Explains Midway as intelligence plus carrier vulnerability.", "Connects naval operations to logistics."],
        "weaknesses": ["Can overstate platforms over systems.", "Luck and timing still mattered.", "Sea control must be turned into land results."],
        "refs": "Murray (2005e); Ares (2026h); Thomas (2026).",
    },
    {
        "anchor": "amphibious_airborne",
        "session": "Session 16",
        "title": "Amphibious and Airborne Operational Learning",
        "reading": "Murray, TCHW Ch. 16; Session 16 one-pager",
        "visual": ["Beach", "Naval Fire", "Logistics", "Bypass"],
        "caption": "Mechanism: sea and air mobility create entry points, but success depends on rapid sustainment and adaptation. Assumption: air and sea support can protect follow-on forces. Strength/limit cue: explains Tarawa to Kwajalein learning, but prepared defenders can impose extreme costs.",
        "situation": "Guadalcanal, Tarawa, Kwajalein, Iwo Jima, and Crete show entry operations succeeding only when mobility is joined to logistics and learning.",
        "intuition": "Landing is not victory. Amphibious and airborne operations must move combat power onto defended ground, hold it, supply it, reinforce it, and exploit it. The Pacific war shows a learning cycle: Tarawa revealed bad assumptions; Kwajalein and island-hopping showed adaptation; Iwo Jima showed how expensive victory could remain.",
        "concepts": ["Amphibious warfare: synchronized sea-air-land assault and sustainment.", "Island-hopping: bypassing strongpoints to make them irrelevant.", "Naval gunfire: sea-based fire support for landing forces.", "Airborne operation: vertical insertion to seize key nodes.", "Operational learning: changing tactics and sequencing after failure."],
        "assumptions": ["Attackers can sustain forces after entry.", "Air and naval superiority suppress enemy response.", "Commanders learn from prior failures."],
        "strengths": ["Explains Tarawa-to-Kwajalein adaptation.", "Connects mobility to logistics.", "Shows why prepared terrain restores defensive advantage."],
        "weaknesses": ["Landing forces are exposed until reinforced.", "Bad intelligence or tides can wreck plans.", "Even successful assaults can be strategically costly."],
        "refs": "Murray (2005e); Ares (2026i); Thomas (2026).",
    },
    {
        "anchor": "nuclear_deterrence",
        "session": "Session 17",
        "title": "Nuclear Weapons and Modern Strategy",
        "reading": "Parker, TCHW Epilogue; Sessions 17-20 guide",
        "visual": ["Second Strike", "Stalemate", "Escalation", "Security Dilemma"],
        "caption": "Mechanism: nuclear weapons make decisive conventional victory politically catastrophic by threatening unacceptable retaliation. Assumption: actors believe retaliation is survivable and credible. Strength/limit cue: explains great-power caution, but proliferation creates volatile regional dilemmas.",
        "situation": "Cold War nuclear stalemate shows military power becoming less about winning battle than deterring escalation.",
        "intuition": "Nuclear weapons transform the offense-defense problem. The point is no longer simply to destroy the enemy first; it is to prevent war by making victory too costly. Deterrence depends on credibility, survivability, command control, and political signaling. After the Cold War, proliferation shifts the problem from bipolar stability to regional insecurity.",
        "concepts": ["Deterrence: preventing action by threatening unacceptable costs.", "Second strike: surviving an attack and retaliating.", "Mutual vulnerability: both sides can suffer catastrophic damage.", "Security dilemma: one state's security measures threaten others.", "Escalation control: managing steps from crisis to wider war."],
        "assumptions": ["Leaders are sensitive to catastrophic retaliation.", "Command and control can survive crisis.", "Signals are understood enough to affect behavior."],
        "strengths": ["Explains great-power caution after 1945.", "Connects technology to strategy rather than tactics.", "Links GPPS 444 to security theory."],
        "weaknesses": ["Accidents and misperception can defeat rational logic.", "Weak command systems raise risk.", "Deterrence does not solve conventional or irregular conflict."],
        "refs": "Parker (2020); Thomas (2026).",
    },
    {
        "anchor": "precision_rma",
        "session": "Session 18",
        "title": "Revolution in Military Affairs and Precision Warfare",
        "reading": "Parker, TCHW Epilogue; Sessions 17-20 guide",
        "visual": ["ISR", "C4I", "PGMs", "System Loop"],
        "caption": "Mechanism: sensors, command networks, and precision weapons compress find-fix-strike time. Assumption: enemy assets are visible, networked, and targetable. Strength/limit cue: devastating against conventional militaries, weak against decentralized insurgency and supply-chain disruption.",
        "situation": "The Gulf Wars show high-tech forces destroying conventional Iraqi formations rapidly with low friendly casualties.",
        "intuition": "The RMA is not a single weapon. It is a system of systems joining intelligence, surveillance, communications, computing, and precision munitions. It substitutes information and accuracy for massed fires. Its weakness is that tactical destruction of visible targets does not automatically build political order or defeat enemies who hide among civilians.",
        "concepts": ["ISR: intelligence, surveillance, and reconnaissance.", "C4I: command, control, communications, computers, and intelligence.", "Precision-guided munition: weapon designed to hit specific targets accurately.", "System of systems: integrated sensors, processors, weapons, and operators.", "Singleton technique: isolated innovation without a sustaining scientific-industrial base."],
        "assumptions": ["Global supply chains and microelectronics remain available.", "Networks function under cyber and electromagnetic stress.", "The target set is identifiable and conventional."],
        "strengths": ["Dominates conventional state militaries.", "Reduces friendly exposure.", "Makes battlefield visibility and timing central."],
        "weaknesses": ["Fragile against cyber, jamming, and satellite attacks.", "Very expensive and supply-chain dependent.", "Can mistake tactical victory for strategic success."],
        "refs": "Parker (2020); Ares (2026j); Thomas (2026).",
    },
    {
        "anchor": "asymmetric_demodernization",
        "session": "Sessions 18-20",
        "title": "Asymmetric Warfare and Demodernization",
        "reading": "Parker, TCHW Epilogue; Ares epilogue notes",
        "visual": ["Low Cost", "Urban Terrain", "Political Will", "State Collapse"],
        "caption": "Mechanism: weak actors avoid Western battlefield strengths and attack political will through cheap, decentralized violence. Assumption: superior powers are casualty- and cost-sensitive. Strength/limit cue: effective at frustrating intervention, but devastating for local governance and civilians.",
        "situation": "Iraq, Afghanistan, Somalia, Bosnia, Rwanda, and urban battles show low-tech actors frustrating high-tech militaries by fighting politically and irregularly.",
        "intuition": "Asymmetry is adaptation by the weaker side. If the West dominates open conventional battle, opponents shift to cities, jungles, caves, IEDs, media, suicide attacks, and civilian populations. Parker's demodernization thesis adds that state collapse can regress war into brutal low-tech violence by militias, criminal bands, and extremists.",
        "concepts": ["Asymmetric warfare: weaker actors target vulnerabilities rather than strengths.", "Demodernization: regression into low-tech, brutal, fragmented violence.", "Force protection paradox: casualty avoidance can distort strategic purpose.", "Sinews of war: public willingness to pay human and financial costs.", "Complex terrain: cities, jungles, mountains, and civilian spaces that hide forces."],
        "assumptions": ["Irregular actors can hide and recruit.", "Democratic publics are sensitive to casualties and costs.", "High-tech forces need political outcomes, not just target destruction."],
        "strengths": ["Explains why superior armies can be strategically frustrated.", "Connects tactics to political will.", "Fits Thomas's current-conflict demodernization theme."],
        "weaknesses": ["Does not guarantee stable governance for weak actors.", "Can provoke overwhelming retaliation.", "Often imposes catastrophic costs on civilians."],
        "refs": "Parker (2020); Cohen (2002); Ares (2026k); Thomas (2026).",
    },
    {
        "anchor": "future_network_warfare",
        "session": "Sessions 19-20",
        "title": "Future Warfare: Space, AI, and Network Fragility",
        "reading": "Parker, TCHW Epilogue; Session 19-20 syllabus block",
        "visual": ["Satellites", "AI", "Networks", "Supply Fragility"],
        "caption": "Mechanism: future combat depends on networks linking sensors, decision systems, supply chains, and weapons, making connectivity both strength and target. Assumption: states can protect space, cyber, and industrial dependencies. Strength/limit cue: powerful for speed and precision, fragile if networks or civilian supply chains fail.",
        "situation": "Future warfare themes point from satellites and AI to the vulnerability of the very networks that make precision warfare possible.",
        "intuition": "The course ends by asking whether the Western way of war can keep adapting. Space systems, AI, cyber operations, and networked weapons promise speed and precision, but also create new dependencies. The future battlefield may punish forces that are too centralized, too visible, or too dependent on fragile global supply chains.",
        "concepts": ["Network warfare: operations built around connected sensors, shooters, and command systems.", "Counter-space: disabling or degrading satellites and orbital services.", "AI-enabled decision support: machine assistance for sensing, targeting, and logistics.", "Electromagnetic warfare: contest over signals, jamming, and spectrum access.", "Supply-chain fragility: dependence on specialized civilian components and partners."],
        "assumptions": ["Networked systems remain connected and trusted.", "Human leaders can control machine-speed operations.", "Industrial and allied supply chains remain resilient."],
        "strengths": ["Captures the frontier of military adaptation.", "Links precision warfare to vulnerability.", "Connects historical themes to Ukraine and contemporary security."],
        "weaknesses": ["Forecasts are uncertain.", "AI and space claims can become hype.", "Low-tech opponents may sidestep the networked fight."],
        "refs": "Parker (2020); Thomas (2026).",
    },
]


REFERENCES = [
    "Allmand, C. (2005). New weapons, new tactics, 1300-1500. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 84-101). Cambridge University Press.",
    "Ares. (2026a). The chevauchee: A field guide [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026b). TCHW Part Two, Ch. 5: New weapons, new tactics, 1300-1500 [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026c). Breitenfeld presentation materials and midterm framework reference [Course notes]. GPPS 444 History of Warfare.",
    "Ares. (2026d). Session 9: Napoleonic Wars I [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026e). Session 10: Napoleonic Wars II [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026f). Session 13: Mechanized Warfare II (WWI) [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026g). Murray, The world in conflict [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026h). Session 15: Undersea and air-sea battle (WWII) [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026i). Session 16: Sea-land battle (WWII) [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026j). Sessions 17-20 study guide: Nuclear weapons, precision, and the future of warfare [Study guide]. GPPS 444 History of Warfare.",
    "Ares. (2026k). TCHW Epilogue and course synthesis [Battle and reading notes]. GPPS 444 History of Warfare.",
    "Bachrach, B. S. (2005). Roman ramparts, 300-1300. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 61-83). Cambridge University Press.",
    "Cohen, E. A. (2002). Supreme command: Soldiers, statesmen, and leadership in wartime. Free Press.",
    "Hanson, V. D. (2005a). Genesis of the infantry, 600-350 BC. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 3-19). Cambridge University Press.",
    "Hanson, V. D. (2005b). From phalanx to legion, 350-250 BC. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 20-33). Cambridge University Press.",
    "Hanson, V. D. (2005c). The Roman way of war, 250 BC-AD 300. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 34-60). Cambridge University Press.",
    "Lynn, J. A. (2005a). States in conflict, 1661-1763. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 167-197). Cambridge University Press.",
    "Lynn, J. A. (2005b). Nations in arms, 1763-1815. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 198-216). Cambridge University Press.",
    "Murray, W. A. (2005a). The industrialization of war, 1815-1871. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 219-244). Cambridge University Press.",
    "Murray, W. A. (2005b). Towards World War I, 1871-1914. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 245-277). Cambridge University Press.",
    "Murray, W. A. (2005c). The West at war, 1914-1918. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 278-313). Cambridge University Press.",
    "Murray, W. A. (2005d). The world in conflict, 1919-1941. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 314-332). Cambridge University Press.",
    "Murray, W. A. (2005e). The world at war, 1941-1945. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 333-365). Cambridge University Press.",
    "Parker, G. (2005a). The gunpowder revolution, 1300-1500. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 101-114). Cambridge University Press.",
    "Parker, G. (2005b). Ships of the line, 1500-1650. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 117-130). Cambridge University Press.",
    "Parker, G. (2005c). Dynastic war, 1494-1660. In G. Parker (Ed.), The Cambridge history of warfare (rev. ed., pp. 148-166). Cambridge University Press.",
    "Parker, G. (2020). Epilogue: The future of Western warfare. In G. Parker (Ed.), The Cambridge history of warfare (2nd ed., pp. 413-432). Cambridge University Press.",
    "Thomas, R. (2026). GPPS 444: A history of warfare, Spring 2026 [Syllabus]. University of California San Diego.",
]


DEEP_SNAPSHOTS = {
    "battle_outcome_framework": [
        ("Mechanism", "Rank the causal variables: mass, mobility, adaptability, logistics, leadership, terrain, technology, weather, and chance."),
        ("Operational logic", "Ask how each variable helped one side concentrate, sustain, move, or survive at the decisive point."),
        ("Preconditions", "Requires source detail on terrain, supply, command choices, force mix, and political purpose."),
        ("Failure mode", "Assumptions fail when the answer becomes a checklist or treats technology as automatic causation."),
        ("Exam use", "Use as the opening diagnostic paragraph before making a sharper single-cause argument."),
        ("Cases", "Salamis, Alesia, Agincourt, Breitenfeld, Russia 1812, Midway, Ukraine."),
    ],
    "western_way_of_war": [
        ("Mechanism", "Disciplined formations, capital, drill, and state competition make organized violence repeatable."),
        ("Operational logic", "Battle-seeking works when institutions can replace losses, preserve lessons, and fund force packages."),
        ("Preconditions", "Needs taxation, credit, command discipline, social acceptance of military service, and adaptive institutions."),
        ("Failure mode", "Fails as a simple superiority story when non-Western innovation or political limits are ignored."),
        ("Exam use", "Frame as a course arc, then immediately qualify with Ottoman, Asian, irregular, and nuclear exceptions."),
        ("Cases", "Greek infantry, Roman adaptation, trace italienne states, British sea finance, RMA, demodernization."),
    ],
    "hoplite_phalanx": [
        ("Mechanism", "Close-order shield and spear cohesion turns citizen infantry into a frontage-limited shock system."),
        ("Operational logic", "Choose narrow ground, compress enemy numbers, keep shields locked, and deny cavalry or missile maneuver."),
        ("Preconditions", "Requires training, morale, equipment, civic obligation, and terrain that protects the flanks."),
        ("Failure mode", "Breaks when formation opens, flanks are turned, or enemy mobility avoids the frontal contest."),
        ("Exam use", "Use to show how terrain and social organization can defeat raw mass."),
        ("Cases", "Marathon, Thermopylae, Plataea, Salamis as paired land-sea Greek adaptation."),
    ],
    "roman_adaptation": [
        ("Mechanism", "Rome converts defeat into organizational learning, then uses engineering to impose operational control."),
        ("Operational logic", "Legions, roads, camps, and siege works reduce uncertainty and let armies fight repeatedly far from Rome."),
        ("Preconditions", "Requires manpower reserves, civic resilience, administrative discipline, and political willingness to endure losses."),
        ("Failure mode", "Fails when expansion strains institutions or professional loyalty shifts from republic to commander."),
        ("Exam use", "Use as Thomas's clearest early example of adaptability after failure."),
        ("Cases", "Cannae recovery, Scipio in Spain/Africa, Cynoscephalae, Alesia."),
    ],
    "fortress_siege": [
        ("Mechanism", "Fixed defenses convert space into time costs, forcing attackers to spend labor, food, money, and engineers."),
        ("Operational logic", "Control routes and populations through strongpoints; decide whether to assault, starve, negotiate, or bypass."),
        ("Preconditions", "Requires stores, garrison discipline, defensible terrain, and attackers without fast wall-breaking tools."),
        ("Failure mode", "Fails when fortresses are bypassed, isolated politically, or made obsolete by artillery."),
        ("Exam use", "Use to explain defense dominance and why medieval war is siege-centric."),
        ("Cases", "Medieval castle networks, Crusader fortresses, Constantinople as transition case."),
    ],
    "chevauchee": [
        ("Mechanism", "Mounted devastation bypasses castles and attacks tax base, legitimacy, morale, and bargaining leverage."),
        ("Operational logic", "Move fast, live off the land, destroy selectively, and provoke the defender into bad battle."),
        ("Preconditions", "Requires mobility edge, weak interception, political value of civilian protection, and forage access."),
        ("Failure mode", "Fails when defenders refuse battle, shelter population, shadow raiders, or deny forage."),
        ("Exam use", "Use as a medieval bridge to coercion, economic warfare, and modern punishment strategies."),
        ("Cases", "Edward III 1346, Black Prince 1355-1356, Crecy, Poitiers, Du Guesclin's Fabian response."),
    ],
    "infantry_missile_revolution": [
        ("Mechanism", "Disciplined infantry plus missiles, stakes, polearms, and ground choice neutralize aristocratic mounted shock."),
        ("Operational logic", "Make cavalry attack into prepared terrain under dense missile fire and countershock."),
        ("Preconditions", "Requires cohesion, preparation time, protected flanks, and weapons integrated into tactics."),
        ("Failure mode", "Fails if cavalry maneuvers around the position or missile troops lack protection."),
        ("Exam use", "Use to argue that tactics make weapons decisive, not the reverse."),
        ("Cases", "Bannockburn, Morgarten, Crecy, Poitiers, Agincourt, Swiss pike warfare."),
    ],
    "gunpowder_trace_italienne": [
        ("Mechanism", "Artillery defeats vertical walls; bastioned design restores defense and raises the fiscal cost of war."),
        ("Operational logic", "Siege trains and engineers become operational centers; states must fund guns, garrisons, and fortification networks."),
        ("Preconditions", "Requires metallurgy, powder quality, trained engineers, credit, taxation, and administrative reach."),
        ("Failure mode", "Fails when reduced to cannon alone or when Ottoman/Asian gunpowder systems are ignored."),
        ("Exam use", "Use for the Roberts-Parker military revolution debate and state-capacity arguments."),
        ("Cases", "Constantinople 1453, Italian Wars, Netherlands fortress warfare, Breitenfeld as later tactical bridge."),
    ],
    "ottoman_standing_army": [
        ("Mechanism", "Standing infantry, siege artillery, frontier administration, and imperial logistics create durable expansion capacity."),
        ("Operational logic", "Use central institutions to mobilize specialized troops and move heavy siege power across frontier zones."),
        ("Preconditions", "Requires recruitment systems, road/supply organization, political legitimacy, and fiscal extraction."),
        ("Failure mode", "Fails when adaptation slows, frontier costs rise, or European fiscal-military competitors catch up."),
        ("Exam use", "Use to puncture a purely Western narrative while still comparing institutions."),
        ("Cases", "Constantinople 1453, Mohacs 1526, Vienna 1529/1683, Lepanto 1571."),
    ],
    "dynastic_firepower": [
        ("Mechanism", "Drill, volley fire, linear formations, and combined arms make gunpowder battle controllable."),
        ("Operational logic", "Coordinate infantry, cavalry, artillery, and reserves so firepower opens decision points for maneuver."),
        ("Preconditions", "Requires training, command discipline, supply of powder/shot, and officers who can control formations."),
        ("Failure mode", "Fails when rigid drill cannot adapt or when logistics cannot feed larger armies."),
        ("Exam use", "Use Breitenfeld to show adaptation from pike shock toward flexible fire systems."),
        ("Cases", "Dutch reforms, Swedish brigades, Breitenfeld 1631, Rocroi 1643, Louis XIV wars."),
    ],
    "nation_in_arms": [
        ("Mechanism", "Revolutionary politics produces mass manpower; Napoleon turns it into operational tempo through corps and leadership."),
        ("Operational logic", "Independent corps march dispersed, concentrate rapidly, forage, deceive, and seek decisive battle."),
        ("Preconditions", "Requires nationalism, administrative conscription, meritocratic command, roads, and enough local resources to forage."),
        ("Failure mode", "Fails when terrain, weather, distance, sea power, or coalition resilience deny decisive concentration."),
        ("Exam use", "Use to connect politics, mass, mobility, leadership, and logistics in one argument."),
        ("Cases", "Valmy, Ulm, Austerlitz, Jena-Auerstedt, Spain, Trafalgar."),
    ],
    "napoleonic_limits": [
        ("Mechanism", "Operational brilliance loses strategic value when logistics, coalitions, and defensive depth absorb the shock."),
        ("Operational logic", "Defenders trade space for time, avoid decisive defeat, attack supply, and learn across campaigns."),
        ("Preconditions", "Requires coalition finance, political endurance, sea control, and terrain large enough to dilute Napoleon's tempo."),
        ("Failure mode", "Fails if treated as inevitable decline rather than contingent strategic overreach."),
        ("Exam use", "Pair with nation-in-arms to show the limit of every military system."),
        ("Cases", "Trafalgar, Peninsular War, Russia 1812, Leipzig 1813, Waterloo 1815."),
    ],
    "industrialized_war": [
        ("Mechanism", "Railroads, telegraphs, rifles, and mass production expand the scale and speed of mobilization and firepower."),
        ("Operational logic", "States move and supply armies faster, but commanders still struggle to attack through modern fire."),
        ("Preconditions", "Requires industry, bureaucracy, rail networks, communications, and national mobilization capacity."),
        ("Failure mode", "Fails when old tactics meet new firepower or when rail plans become strategically rigid."),
        ("Exam use", "Use as the bridge from Napoleonic maneuver to WWI stalemate."),
        ("Cases", "Crimean War, U.S. Civil War, Prussian wars, Sedan 1870."),
    ],
    "towards_world_war": [
        ("Mechanism", "Modern firepower and mobilization schedules harden into plans that outpace political control and maneuver doctrine."),
        ("Operational logic", "Armies can mobilize and kill at scale, but cannot yet restore movement against entrenched defenders."),
        ("Preconditions", "Requires conscription, rail timetables, heavy artillery, machine guns, and alliance politics."),
        ("Failure mode", "Fails if planners assume offense without solving protection, communications, and logistics under fire."),
        ("Exam use", "Use to explain why Europe expected decision but got attrition."),
        ("Cases", "Franco-Prussian lessons, Schlieffen Plan, Marne, early trench systems, Russo-Japanese War as warning."),
    ],
    "wwi_combined_arms": [
        ("Mechanism", "Combined arms slowly reconnect fire and movement through artillery, infantry, tanks, aircraft, and communications."),
        ("Operational logic", "Suppress, infiltrate, communicate, exploit, and sustain across depth instead of merely taking first trenches."),
        ("Preconditions", "Requires staff learning, ammunition, rehearsals, air observation, rolling barrages, and transport resilience."),
        ("Failure mode", "Fails when breakthrough outruns communications, reserves, roads, or artillery range."),
        ("Exam use", "Use as Thomas's adaptation-after-failure template."),
        ("Cases", "Somme, Verdun, Riga, Cambrai, Hundred Days, Gallipoli as amphibious failure."),
    ],
    "wwii_blitzkrieg": [
        ("Mechanism", "Armor, radios, aircraft, and mission command create tempo that dislocates brittle defenses."),
        ("Operational logic", "Penetrate, bypass strongpoints, paralyze command, and convert tactical success into operational collapse."),
        ("Preconditions", "Requires fuel, maintenance, air-ground coordination, initiative, infantry follow-up, and reachable political objectives."),
        ("Failure mode", "Fails against depth, weather, industrial attrition, and logistics that cannot match operational reach."),
        ("Exam use", "Use France 1940 and Barbarossa as paired success/limit examples."),
        ("Cases", "Poland, France 1940, North Africa, Barbarossa, Stalingrad, Kursk."),
    ],
    "air_sea_undersea": [
        ("Mechanism", "Sea control emerges from convoys, escorts, carriers, submarines, aircraft, codebreaking, and production."),
        ("Operational logic", "Protect logistics across oceans while denying the enemy the ability to move, supply, or choose battle."),
        ("Preconditions", "Requires shipbuilding, trained crews, intelligence fusion, bases, fuel, and air cover."),
        ("Failure mode", "Fails when attrition exceeds replacement or when commanders treat platforms separately from systems."),
        ("Exam use", "Use to show logistics as the hidden center of WWII operational art."),
        ("Cases", "Battle of the Atlantic, Midway, Guadalcanal, submarine campaign against Japan."),
    ],
    "amphibious_airborne": [
        ("Mechanism", "Joint operations put force across defended barriers, then adapt procedures after costly first attempts."),
        ("Operational logic", "Integrate fire support, landing craft, logistics over beaches, airborne seizure, and rapid follow-on sustainment."),
        ("Preconditions", "Requires intelligence, rehearsals, specialized craft, naval/air superiority, and command integration."),
        ("Failure mode", "Fails when surprise, weather, beaches, reefs, or resupply assumptions prove false."),
        ("Exam use", "Use Tarawa-to-Kwajalein or Crete-to-no-more-major-airborne as adaptation examples."),
        ("Cases", "Gallipoli, Crete, Tarawa, Kwajalein, Normandy, Market Garden."),
    ],
    "nuclear_deterrence": [
        ("Mechanism", "Nuclear weapons shift success from battlefield victory to preventing escalation through credible retaliation."),
        ("Operational logic", "Survivable forces, second strike, command control, and signaling stabilize or destabilize crises."),
        ("Preconditions", "Requires rational-enough leadership, secure arsenals, communication, and belief in retaliatory capability."),
        ("Failure mode", "Fails through accident, misperception, first-strike fears, rogue command, or uncontrolled escalation."),
        ("Exam use", "Use to mark the sharpest break in the course's decisive-battle tradition."),
        ("Cases", "Hiroshima/Nagasaki, Cuban Missile Crisis, MAD, NATO flexible response, India-Pakistan crises."),
    ],
    "precision_rma": [
        ("Mechanism", "Sensors, networks, stealth, command systems, and precision munitions substitute information for massed fire."),
        ("Operational logic", "Find, fix, target, strike, assess, and repeat faster than the opponent can adapt."),
        ("Preconditions", "Requires ISR, secure networks, GPS/space support, trained operators, munitions stocks, and visible targets."),
        ("Failure mode", "Fails against concealment, civilian masking, political disorder, depleted stocks, or network disruption."),
        ("Exam use", "Use to separate tactical destruction from strategic success."),
        ("Cases", "1991 Gulf War, Kosovo, Iraq 2003, drone campaigns, Ukraine precision/artillery mix."),
    ],
    "asymmetric_demodernization": [
        ("Mechanism", "Weak actors avoid open battle and attack political will through terrain, civilians, media, time, and cheap weapons."),
        ("Operational logic", "Disperse, hide, impose costs, survive retaliation, and make the stronger power's victory politically unusable."),
        ("Preconditions", "Requires sanctuary, recruitment, local knowledge, external support, and a stronger opponent with political constraints."),
        ("Failure mode", "Fails when irregulars cannot govern, alienate civilians, or face opponents willing to absorb costs."),
        ("Exam use", "Use for Thomas's Ukraine/Sudan/Middle East demodernization link."),
        ("Cases", "Vietnam, Afghanistan, Iraq, Somalia, Bosnia, Rwanda, urban Ukraine, nonstate militias."),
    ],
    "future_network_warfare": [
        ("Mechanism", "Space, AI, cyber, spectrum, and supply chains make speed possible while creating new attack surfaces."),
        ("Operational logic", "Protect networks, degrade enemy connectivity, shorten decision cycles, and keep logistics resilient under disruption."),
        ("Preconditions", "Requires trusted data, hardened satellites, cyber defense, human control, and industrial redundancy."),
        ("Failure mode", "Fails through spoofing, jamming, brittle automation, supply interruption, or adversary low-tech evasion."),
        ("Exam use", "Use as the final adaptation question: can the Western way keep learning?"),
        ("Cases", "Ukraine drones and EW, anti-satellite threats, AI targeting debates, PGM supply-chain stress."),
    ],
}


def get_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrapped(draw, text, font, width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_arrow(draw, start, end, fill, width=5):
    draw.line([start, end], fill=fill, width=width)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        sign = 1 if ex > sx else -1
        pts = [(ex, ey), (ex - sign * 18, ey - 10), (ex - sign * 18, ey + 10)]
    else:
        sign = 1 if ey > sy else -1
        pts = [(ex, ey), (ex - 10, ey - sign * 18), (ex + 10, ey - sign * 18)]
    draw.polygon(pts, fill=fill)


def make_visual(theory):
    path = ASSET_DIR / f"{theory['anchor']}.png"
    if path.exists():
        return path
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#F8FAFC")
    d = ImageDraw.Draw(img)
    title_font = get_font(42, True)
    node_font = get_font(34, True)
    small_font = get_font(27, False)
    blue = "#1B2A4A"
    med = "#2C5282"
    gold = "#C69C3F"
    green = "#276749"
    d.rectangle([0, 0, w, 92], fill=blue)
    d.text((48, 24), theory["title"], fill="white", font=title_font)
    labels = theory["visual"]
    positions = [(90, 270), (455, 270), (820, 270), (1185, 270)]
    box_w, box_h = 300, 150
    for idx, label in enumerate(labels):
        x, y = positions[idx]
        fill = ["#EBF4FF", "#EFFAF3", "#FFF5E6", "#EEF2FF"][idx % 4]
        d.rounded_rectangle([x, y, x + box_w, y + box_h], radius=22, fill=fill, outline=med, width=4)
        lines = wrapped(d, label, node_font, box_w - 40)
        yy = y + (box_h - len(lines) * 40) / 2
        for line in lines:
            tw = d.textbbox((0, 0), line, font=node_font)[2]
            d.text((x + (box_w - tw) / 2, yy), line, fill=blue, font=node_font)
            yy += 42
        if idx < len(labels) - 1:
            draw_arrow(d, (x + box_w + 18, y + box_h / 2), (positions[idx + 1][0] - 22, y + box_h / 2), gold, 7)
    d.rounded_rectangle([190, 560, 1410, 760], radius=24, fill="white", outline=green, width=4)
    mechanism = theory["caption"].split(".")[0].replace("Mechanism: ", "")
    lines = wrapped(d, mechanism, small_font, 1100)
    yy = 590
    d.text((230, yy), "Mechanism", fill=green, font=node_font)
    yy += 52
    for line in lines[:3]:
        d.text((230, yy), line, fill="#222222", font=small_font)
        yy += 36
    d.text((48, 826), "GPPS 444 History of Warfare | explanatory mechanism diagram", fill="#475569", font=small_font)
    img.save(path)
    return path


def header_table(theory, continuation=False):
    label = f"{theory['session']} | {theory['title']}"
    sub = f"{theory['reading']}" + (" | details and exam use" if continuation else "")
    data = [[Paragraph(f"<b>{esc(label)}</b><br/><font size='6.2'><i>{esc(sub)}</i></font>", styles["Body"])]]
    table = Table(data, colWidths=[7.2 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_NAVY if not continuation else MED_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0, DARK_NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def two_col(left_title, left_items, right_title, right_items, width):
    col_w = (width - 8) / 2
    left = [Paragraph(f"<b>{esc(left_title)}</b>", styles["Small"]), bullet_list(left_items, "Small")]
    right = [Paragraph(f"<b>{esc(right_title)}</b>", styles["Small"]), bullet_list(right_items, "Small")]
    table = Table([[left, right]], colWidths=[col_w, col_w])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
        ("BACKGROUND", (1, 0), (1, 0), WARM_AMBER),
        ("BOX", (0, 0), (-1, -1), 0.4, BORDER_GREY),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def snapshot_table(theory, width):
    rows = []
    snapshot = DEEP_SNAPSHOTS[theory["anchor"]]
    for left, right in zip(snapshot[0::2], snapshot[1::2]):
        rows.append([
            Paragraph(f"<b>{esc(left[0])}:</b> {esc(left[1])}", styles["Tiny"]),
            Paragraph(f"<b>{esc(right[0])}:</b> {esc(right[1])}", styles["Tiny"]),
        ])
    table = Table(rows, colWidths=[(width - 8) / 2, (width - 8) / 2])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FAFAFA")),
        ("BOX", (0, 0), (-1, -1), 0.35, BORDER_GREY),
        ("INNERGRID", (0, 0), (-1, -1), 0.2, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return table


def snapshot_value(theory, label):
    for key, value in DEEP_SNAPSHOTS[theory["anchor"]]:
        if key == label:
            return value
    return ""


def application_drill(theory, width):
    rows = [
        [
            Paragraph("<b>Campaign / battle examples</b>", styles["Tiny"]),
            Paragraph(esc(snapshot_value(theory, "Cases")), styles["Tiny"]),
        ],
        [
            Paragraph("<b>Military mechanism to name</b>", styles["Tiny"]),
            Paragraph(esc(snapshot_value(theory, "Mechanism")), styles["Tiny"]),
        ],
        [
            Paragraph("<b>Tactical / operational logic</b>", styles["Tiny"]),
            Paragraph(esc(snapshot_value(theory, "Operational logic")), styles["Tiny"]),
        ],
        [
            Paragraph("<b>Assumption stress test</b>", styles["Tiny"]),
            Paragraph(esc(snapshot_value(theory, "Failure mode")), styles["Tiny"]),
        ],
        [
            Paragraph("<b>Exam sentence</b>", styles["Tiny"]),
            Paragraph(esc(snapshot_value(theory, "Exam use")), styles["Tiny"]),
        ],
    ]
    table = Table(rows, colWidths=[1.65 * inch, width - 1.65 * inch])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF6FF")),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.35, BORDER_GREY),
        ("INNERGRID", (0, 0), (-1, -1), 0.2, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return table


def cover_page(story):
    story.append(Paragraph("GPPS 444 Theory Reference", styles["CoverTitle"]))
    story.append(Paragraph("History of Warfare | Professor Thomas | Spring 2026 | UC San Diego", styles["CoverSub"]))
    desc = (
        "Full-course reference manual synthesizing Thomas's recurring analytical themes, the Parker/TCHW reading sequence, "
        "existing GPPS 444 midterm framework materials, session one-pagers, and Ares battle notes. Each theory unit gets two "
        "pages: a mechanism image and intuition page, followed by concepts, assumptions, strengths, weaknesses, and references."
    )
    box = Table([[Paragraph(esc(desc), styles["Small"])]], colWidths=[7.1 * inch])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(box)
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Clickable Table of Contents</b>", styles["Section"]))
    for i, t in enumerate(THEORIES, 1):
        story.append(Paragraph(f"<a href='#{t['anchor']}'>{i:02d}. {esc(t['session'])} - {esc(t['title'])}</a>", styles["TOC"]))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="35%", thickness=0.4, color=BORDER_GREY, hAlign="LEFT"))
    story.append(Paragraph(
        "Generated with GPT-5 Codex via the Claudia agent system for GPPS 444, Professor Thomas, UC San Diego. "
        "Always verify against official course materials and assigned readings. This is a study aid, not a substitute for reading the texts.",
        styles["Tiny"],
    ))
    story.append(PageBreak())


def build_theory(story, theory, idx, width):
    img_path = make_visual(theory)
    story.append(BookmarkAnchor(theory["anchor"], f"{idx:02d}. {theory['title']}"))
    story.append(header_table(theory))
    story.append(Spacer(1, 5))
    story.append(RLImage(str(img_path), width=6.7 * inch, height=3.75 * inch))
    story.append(Paragraph(f"<b>Image caption/footnote.</b> {esc(theory['caption'])}", styles["Small"]))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>SITUATION</b>", styles["Section"]))
    story.append(para(theory["situation"]))
    story.append(Paragraph("<b>CORE INTUITION</b>", styles["Section"]))
    story.append(para(theory["intuition"]))
    story.append(Paragraph("<b>COMBAT SNAPSHOT: MECHANISM, LIMITS, EXAM USE</b>", styles["Section"]))
    story.append(snapshot_table(theory, width))
    story.append(PageBreak())

    story.append(header_table(theory, continuation=True))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>KEY CONCEPTS, KEYWORDS & TERMINOLOGY</b>", styles["Section"]))
    story.append(bullet_list(theory["concepts"]))
    story.append(Spacer(1, 3))
    story.append(two_col("ASSUMPTIONS", theory["assumptions"], "STRENGTHS", theory["strengths"], width))
    story.append(Spacer(1, 4))
    story.append(two_col("WEAKNESSES", theory["weaknesses"], "APA REFERENCES / UNIT DISCLOSURE", [
        f"APA references used in this unit: {theory['refs']}",
        "Generated for Edgar Agunias on 2026-06-01 by Ares using GPT-5 Codex and course-local sources.",
        f"Image asset: {ASSET_DIR / (theory['anchor'] + '.png')}",
    ], width))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>CAMPAIGN / BATTLE APPLICATION DRILL</b>", styles["Section"]))
    story.append(application_drill(theory, width))
    story.append(PageBreak())


def references_and_disclosure(story):
    story.append(BookmarkAnchor("references", "References and Disclosure"))
    story.append(Paragraph("References", styles["CoverTitle"]))
    for ref in REFERENCES:
        story.append(Paragraph(esc(ref), styles["Small"]))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    disclosure = (
        "Generated for: Edgar Agunias<br/>"
        "Date: 2026-06-01<br/>"
        "Model: GPT-5 Codex<br/>"
        "Sources: GPPS 444 syllabus extraction, Parker-edited TCHW PDF/table of contents, existing midterm framework reference v1.1.1, GPPS 444 session one-pagers, Breitenfeld materials, and Ares memory files<br/>"
        "Agent: Ares"
    )
    story.append(Paragraph(disclosure, styles["Small"]))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(doc.leftMargin, 0.35 * inch, DOC_TITLE)
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


def main():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.48 * inch,
    )
    story = []
    cover_page(story)
    usable_width = letter[0] - doc.leftMargin - doc.rightMargin
    for idx, theory in enumerate(THEORIES, 1):
        build_theory(story, theory, idx, usable_width)
    references_and_disclosure(story)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    main()
