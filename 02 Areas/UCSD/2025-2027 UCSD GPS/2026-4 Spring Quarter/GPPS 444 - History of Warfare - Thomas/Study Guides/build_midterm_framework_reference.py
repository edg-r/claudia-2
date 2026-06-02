from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
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


OUT = "GPPS_444_Midterm_Framework_Reference.pdf"
DOC_TITLE = "GPPS 444 Midterm Framework Reference"

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
WARM_AMBER = colors.HexColor("#FFF5E6")


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
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=23,
        alignment=TA_CENTER,
        textColor=DARK_NAVY,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        parent=styles["Normal"],
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#333333"),
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["Normal"],
        fontSize=7.2,
        leading=8.6,
    )
)
styles.add(
    ParagraphStyle(
        name="TinyGrey",
        parent=styles["Normal"],
        fontSize=6.8,
        leading=8,
        textColor=colors.HexColor("#666666"),
    )
)
styles.add(
    ParagraphStyle(
        name="TOC",
        parent=styles["Normal"],
        fontSize=8.6,
        leading=10.4,
        spaceBefore=0,
        spaceAfter=1,
        textColor=MED_BLUE,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontSize=9.5,
        leading=11,
        textColor=DARK_NAVY,
        spaceBefore=5,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontSize=7.7,
        leading=9.3,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="RefBullet",
        parent=styles["Body"],
        leftIndent=7,
        firstLineIndent=0,
    )
)


frameworks = [
    {
        "anchor": "thomas_battle_analysis",
        "session": "Course-wide",
        "title": "Thomas Battle-Outcome Framework",
        "reading": "Slides 1 and Terminology handout; course memory",
        "situation": "Use this framework when a quiz asks why one side won: explain how mass, mobility, adaptability, logistics, leadership, terrain, weather, technology, organization, and chance interacted.",
        "intuition": "Thomas treats battle outcomes as multi-variable judgments, not single-cause stories. Technology matters, but only through organization, terrain, weather, training, culture, logistics, and leadership. Good answers identify the decisive variable and show why rival variables mattered less in that case.",
        "concepts": [
            ("Mass", "The amount of force available at the decisive point; numbers matter only if they can be organized, supplied, and brought to bear."),
            ("Mobility", "Maneuver and speed across terrain, roads, sea lanes, or operational theaters."),
            ("Adaptability", "Transition resilience: the ability to change formations, doctrine, or methods when the old system stops working."),
            ("Supply chains", "The food, fodder, credit, transport, ammunition, and administration that let armies keep fighting."),
            ("Operational leadership", "Battlefield vision and command judgment that converts resources into advantage under fog and friction."),
            ("Offense-defense balance", "The recurring question of whether the attacker can force decision or the defender can absorb, delay, and exhaust."),
        ],
        "assumptions": [
            "A battle or campaign can be analyzed through interacting variables.",
            "The decisive factor changes by period and case.",
            "Quiz answers should connect evidence to a causal mechanism, not list facts.",
        ],
        "strengths": [
            "Works across the whole course, from hoplites to Waterloo.",
            "Prevents technology-only explanations.",
            "Maps directly to Thomas's quiz language.",
        ],
        "weaknesses": [
            "Can become a checklist if not tied to one decisive causal story.",
            "Needs period awareness; mobility in Salamis is not mobility in Napoleon's corps system.",
            "May understate politics if treated only at the tactical level.",
        ],
    },
    {
        "anchor": "western_way_war",
        "session": "Sessions 1-2",
        "title": "Western Way of War",
        "reading": "TCHW introduction and Part One; syllabus-extracted course arc",
        "situation": "This framework explains why the course follows the rise of disciplined infantry, drill, finance, and technology as a dominant military tradition that later becomes globally influential.",
        "intuition": "The western way of war in Parker's framing is not simply European superiority. It is a tradition built around discipline, decisive battle, technological adaptation, finance, and institutional learning. The reference point is useful because each session asks how a specific military system advances, limits, or complicates that tradition.",
        "concepts": [
            ("Decisive battle", "Preference for resolving conflicts through organized combat against the enemy's main force."),
            ("Discipline", "Training and order that let units hold formation and execute under pressure."),
            ("Institutional adaptation", "States and armies copy, refine, and standardize effective methods."),
            ("Finance and credit", "War depends on the ability to mobilize money over time, not just manpower in the moment."),
            ("Imitation", "Nonwestern powers often resist western arms by adopting selected western techniques, while western armies borrow from Asia too."),
        ],
        "assumptions": [
            "A broad military tradition can be traced across different periods.",
            "Institutions can preserve battlefield lessons and reproduce them.",
            "The framework must be qualified for non-European cases and borrowed innovations.",
        ],
        "strengths": [
            "Gives the course a unifying arc.",
            "Connects tactics to states, finance, and political order.",
            "Helps compare ancient, early modern, and Napoleonic warfare.",
        ],
        "weaknesses": [
            "Risks Eurocentrism if treated as a universal rule.",
            "Can hide Asian and Ottoman contributions to weapons, tactics, and organization.",
            "Overemphasizes battle if logistics and politics are ignored.",
        ],
    },
    {
        "anchor": "hoplite_phalanx",
        "session": "Session 2",
        "title": "Hoplite-Phalanx Citizen Soldier Model",
        "reading": "Slides 2; TCHW Part One, Greek warfare",
        "situation": "At Thermopylae and Salamis, smaller Greek forces used organization, terrain, and civic commitment to offset Persian mass.",
        "intuition": "Greek warfare links military form to social form. Hoplites fought as heavy citizen infantry in close phalanx formation, where cohesion, shields, spears, and terrain could make a smaller force tactically dangerous. The model shows how organization and morale can turn mass against itself.",
        "concepts": [
            ("Hoplite", "Heavily armed infantryman carrying shield and spear."),
            ("Phalanx", "Dense armored formation whose strength depends on cohesion and frontage."),
            ("Citizen soldier", "A fighter whose political identity and military service reinforce each other."),
            ("Restricted terrain", "Narrow ground or sea space that limits enemy maneuver and neutralizes superior numbers."),
            ("Force multiplier", "A condition that makes a smaller force fight as if it were larger."),
        ],
        "assumptions": [
            "The formation can maintain cohesion.",
            "Terrain denies the enemy room to envelop or exploit mass.",
            "Citizen morale and leadership sustain close combat.",
        ],
        "strengths": [
            "Explains Thermopylae's delay and Salamis's ambush logic.",
            "Shows terrain and organization beating raw numbers.",
            "Introduces the course's citizenship-vs-levies theme.",
        ],
        "weaknesses": [
            "Poor in open terrain against flexible or cavalry-heavy opponents.",
            "Formation rigidity limits maneuver.",
            "Can romanticize civic morale while underplaying logistics and alliance politics.",
        ],
    },
    {
        "anchor": "roman_adaptation",
        "session": "Sessions 3-4",
        "title": "Roman Adaptability and Engineering",
        "reading": "Slides 3-4; TCHW Roman chapters",
        "situation": "Rome survived Cannae, adapted against Carthage and Hellenistic phalanxes, and used roads, siege works, and political-military integration to expand.",
        "intuition": "Roman warfare is the course's early model of institutional adaptation. Rome absorbed defeats, copied useful enemy practices, organized flexible formations, and turned engineering into a force multiplier. Military victory also fed political power, especially as professional soldiers became tied to commanders.",
        "concepts": [
            ("Maniple/legion flexibility", "More adaptable organization than a rigid phalanx, especially on broken ground."),
            ("Castrametation", "Camp-building and field organization; a sign of Roman discipline and engineering."),
            ("Lines of communication", "Roads and routes that connect armies to supply, reinforcement, and political control."),
            ("Siege engineering", "Fortifications, circumvallation, and construction used to turn time and labor into combat power."),
            ("Professionalization", "The Marian reform logic: soldiers increasingly depend on the state or commander for livelihood and rewards."),
        ],
        "assumptions": [
            "The state can learn from defeat rather than collapse.",
            "Engineering labor can be mobilized and protected.",
            "Political institutions can sustain long wars.",
        ],
        "strengths": [
            "Explains Alesia as engineering plus leadership, not just courage.",
            "Highlights adaptability as a Roman comparative advantage.",
            "Links battlefield success to empire-building.",
        ],
        "weaknesses": [
            "Professional armies can shift loyalty from state to general.",
            "Engineering systems are vulnerable to ambush and local knowledge, as at Teutoburg Forest.",
            "Expansion stretches governance and logistics.",
        ],
    },
    {
        "anchor": "fortress_siege",
        "session": "Session 5",
        "title": "Castle, Fortress, and Siege Dominance",
        "reading": "TCHW medieval warfare; course arc",
        "situation": "In medieval warfare, stone fortifications often made defense dominant because castles controlled territory even when no decisive field battle occurred.",
        "intuition": "Fortification shifts the logic of war from annihilating an army to controlling strongpoints, routes, and populations. Castles, walls, and siege engines make time, labor, food, and engineering central. The attacker must either reduce the fortress, bypass it, or devastate the surrounding economy.",
        "concepts": [
            ("Fortification", "A fixed defensive system that protects people, supplies, and political control."),
            ("Siege", "An operation to compel surrender through assault, starvation, bombardment, mining, or negotiation."),
            ("Defense dominance", "A condition where fortifications make attack slow, expensive, and uncertain."),
            ("Terrain control", "Strongpoints shape movement even without continuous front lines."),
            ("Logistical drag", "Sieges consume manpower, food, transport, and time."),
        ],
        "assumptions": [
            "The fortress can be supplied or hold out long enough to matter.",
            "The attacker lacks fast, reliable wall-breaking technology.",
            "Political control depends on places, not just field armies.",
        ],
        "strengths": [
            "Explains why medieval war often centered on sieges.",
            "Connects defense, logistics, and political control.",
            "Sets up the importance of gunpowder and trace italienne later.",
        ],
        "weaknesses": [
            "Static defense can be bypassed by raids.",
            "Fortresses cannot protect all economic assets outside the walls.",
            "Once artillery improves, old vertical walls become liabilities.",
        ],
    },
    {
        "anchor": "chevauchee",
        "session": "Sessions 5-6",
        "title": "Chevauchee and Economic Warfare",
        "reading": "Chevauchee explainer; TCHW Ch. 5",
        "situation": "Edward III and the Black Prince used fast mounted devastation to make the French king choose between political humiliation and bad battle.",
        "intuition": "The chevauchee is a mobility-led workaround in a defense-dominant world. Instead of reducing every castle, a mounted column destroys the countryside, tax base, and legitimacy of the ruler who cannot protect subjects. Battle is often the desired secondary effect; economic and political pain are the primary instruments.",
        "concepts": [
            ("Operational raid", "A fast campaign designed to destroy resources and induce response, not hold ground."),
            ("Tax base", "The productive economy that funds royal war-making."),
            ("Provocation", "Devastation forces a ruler to fight on unfavorable terms or look weak."),
            ("Living off the land", "Supply by seizure and foraging, which increases speed but damages political control."),
            ("Fabian response", "Refusing battle, shadowing the enemy, sheltering population, and letting the raid exhaust itself."),
        ],
        "assumptions": [
            "The target ruler depends on visible protection of subjects.",
            "The raiding force can move faster than the defender can intercept.",
            "Economic destruction produces bargaining pressure.",
        ],
        "strengths": [
            "Explains Crecy, Poitiers, and the political logic of devastation.",
            "Connects medieval war to later coercion by punishment.",
            "Shows mobility countering fortification.",
        ],
        "weaknesses": [
            "Cannot hold territory or govern what it ruins.",
            "Can be blunted by refusal of battle and protected towns.",
            "May destroy the resources needed for later occupation.",
        ],
    },
    {
        "anchor": "infantry_revolution",
        "session": "Session 6",
        "title": "Infantry, Missile, and Polearm Revolution",
        "reading": "Allmand, TCHW Ch. 5; Session 6 one-pager",
        "situation": "At Agincourt, prepared ground, longbows, stakes, mud, and disciplined infantry made mounted aristocratic shock fail.",
        "intuition": "The late medieval shift is less 'new weapon wins' than 'new tactics make cheaper weapons decisive.' Longbows, pikes, halberds, crossbows, and early handguns empowered disciplined common infantry against armored cavalry. Training, chosen terrain, and formation discipline mattered as much as the weapon itself.",
        "concepts": [
            ("Longbow", "High-rate English missile weapon effective when massed on prepared ground."),
            ("Pike/halberd", "Polearms that let infantry resist or break cavalry charges."),
            ("Dismounted men-at-arms", "Elite fighters used as infantry when mounted shock is tactically unsafe."),
            ("Indenture contract", "Paid military service that supports accountability and semi-professional forces."),
            ("Compagnies d'Ordonnance", "French standing companies that point toward permanent armies."),
        ],
        "assumptions": [
            "Infantry has discipline and favorable ground.",
            "Cavalry cannot maneuver around the prepared position.",
            "Weapons are integrated into a tactical system.",
        ],
        "strengths": [
            "Explains the decline of the armored knight as decisive arm.",
            "Links social order, cost, and battlefield practice.",
            "Prepares the transition to gunpowder and standing armies.",
        ],
        "weaknesses": [
            "Does not eliminate cavalry; it changes cavalry's role.",
            "Missile infantry can be vulnerable without terrain or protection.",
            "Early gunpowder is not yet consistently decisive in the field.",
        ],
    },
    {
        "anchor": "gunpowder_trace",
        "session": "Session 7",
        "title": "Gunpowder Revolution and Trace Italienne",
        "reading": "Week 4 reference; Parker, TCHW Ch. 6",
        "situation": "Cannon made medieval walls fall faster, but the trace italienne restored defensive strength and forced bigger armies, longer sieges, and fiscal strain.",
        "intuition": "Parker's military revolution is systemic. Better powder, shot, guns, and carriages made artillery effective against old walls; low, thick, angled bastions then made sieges slower and more expensive. The result was not simply more offense, but a new offense-defense cycle that favored states able to pay for engineers, garrisons, and large armies.",
        "concepts": [
            ("Corned gunpowder", "Granulated powder that made guns more powerful and reliable."),
            ("Trunnion carriage", "Gun mounting that improved aiming and reload efficiency."),
            ("Trace italienne", "Low, thick, bastioned artillery fortress designed to absorb and flank cannon fire."),
            ("Military Revolution", "The cluster of tactical, fortification, army-size, and fiscal changes in early modern war."),
            ("Fiscal-military state", "A state organized to tax, borrow, and administer sustained warfare."),
        ],
        "assumptions": [
            "States can fund new fortifications and siege systems.",
            "Artillery and engineering knowledge diffuse across Europe.",
            "Fortress networks shape strategy as much as field battles do.",
        ],
        "strengths": [
            "Explains why war becomes larger, slower, and more expensive.",
            "Connects technology to state capacity.",
            "Frames Breitenfeld against the broader Roberts/Parker debate.",
        ],
        "weaknesses": [
            "Can overstate Europe if Ottoman and Asian gunpowder systems are ignored.",
            "Battlefield innovation still matters; fortresses are not the whole story.",
            "The timing varies by region.",
        ],
    },
    {
        "anchor": "ottoman_standing",
        "session": "Session 8",
        "title": "Ottoman Expansion and Standing Military Institutions",
        "reading": "Session 8 one-pager; Week 4 reference; lecture supplement noted",
        "situation": "Ottoman expansion toward Mohacs and Vienna shows how standing infantry, siege artillery, dynastic ambition, and logistics created a durable early modern threat.",
        "intuition": "The Ottoman case matters because it complicates a simple western-way story. Janissaries, siege artillery, and imperial logistics show nonwestern institutional sophistication. For Thomas, the key is to compare Ottoman adaptability and standing forces with European gunpowder and fiscal-military developments while noting the reading's Eurocentric gaps.",
        "concepts": [
            ("Janissaries", "Elite standing infantry associated with Ottoman military power and central authority."),
            ("Devshirme", "Recruitment system tied to Ottoman state formation and military service."),
            ("Siege artillery", "Large guns used against fortifications, including the Constantinople model."),
            ("Habsburg-Ottoman frontier", "A long military border where fortress, logistics, and dynastic strategy interacted."),
            ("Galley warfare", "Mediterranean naval system relevant to Lepanto and Ottoman maritime power."),
        ],
        "assumptions": [
            "Lecture supplements the TCHW reading for Ottoman land institutions.",
            "Standing forces and artillery can be supplied across imperial distances.",
            "Comparison must separate land, sea, and frontier contexts.",
        ],
        "strengths": [
            "Corrects a Eurocentric reading gap.",
            "Highlights standing army and artillery before many European analogues.",
            "Connects Mohacs, Vienna, and Lepanto to course themes.",
        ],
        "weaknesses": [
            "The assigned chapter under-treats Ottoman institutions.",
            "Risks flattening a long imperial arc into 'rise and decline.'",
            "Needs lecture notes for fuller Janissary and devshirme detail.",
        ],
    },
    {
        "anchor": "dynastic_firepower",
        "session": "Session 8 / Breitenfeld bridge",
        "title": "Dynastic War, Volley Fire, and Combined Arms",
        "reading": "Parker, TCHW Ch. 9; Session 8 one-pager; Breitenfeld materials",
        "situation": "At Breitenfeld in 1631, Swedish volley fire, light artillery, disciplined cavalry, and flexible formations defeated deeper Imperial squares.",
        "intuition": "Early modern warfare combined mass, drill, firearms, and organization. Maurice of Nassau's countermarch and Gustavus Adolphus's Swedish system show how continuous fire, standardized guns, and flexible formations could turn gunpowder into battlefield effect. But the advantage was copyable and existed inside a siege-dominated strategic world.",
        "concepts": [
            ("Volley fire", "Coordinated musket discharge designed to concentrate fire and maintain pressure."),
            ("Countermarch", "Drill system allowing ranks to rotate and sustain fire."),
            ("Tercio", "Deep Spanish infantry formation combining pike and shot."),
            ("Regimental artillery", "Light guns integrated with infantry for mobile fire support."),
            ("Combined arms", "Mutual support among infantry, cavalry, artillery, and command systems."),
        ],
        "assumptions": [
            "Troops can drill enough to execute fire discipline.",
            "Artillery is standardized and mobile enough for field use.",
            "Commanders can coordinate arms under battlefield stress.",
        ],
        "strengths": [
            "Explains Breitenfeld through discipline and firepower, not just numbers.",
            "Shows adaptability from pike shock to linear fire.",
            "Connects battle tactics to the military revolution debate.",
        ],
        "weaknesses": [
            "Copyable systems lose surprise quickly.",
            "Sieges and logistics still dominate strategy.",
            "Mercenary and fiscal limits constrain battlefield innovation.",
        ],
    },
    {
        "anchor": "nation_in_arms",
        "session": "Session 9",
        "title": "Nation in Arms and Napoleonic Operational System",
        "reading": "Lynn, TCHW Ch. 11; Session 9 one-pager",
        "situation": "Austerlitz shows Napoleon using national manpower, corps mobility, deception, and concentration to destroy a coalition army.",
        "intuition": "The French Revolution politicized war by making citizens fight as members of a nation, not merely subjects of a ruler. Napoleon inherited that manpower and motivation, then refined it through corps organization, meritocratic command, artillery, flexible logistics, and operational maneuver.",
        "concepts": [
            ("Nation in arms", "Mobilized citizens who understand war as their own national struggle."),
            ("Conscription", "State manpower extraction, regularized in revolutionary France and expanded under Napoleon."),
            ("Corps system", "Semi-independent combined-arms formations that march separately and concentrate for battle."),
            ("Manoeuvre sur les derrieres", "Operational move against the enemy flank or rear to cut retreat and create annihilation."),
            ("The Nelson Touch", "British naval initiative and seamanship at Trafalgar, preserving command of the sea."),
        ],
        "assumptions": [
            "National motivation and state administration can sustain mass armies.",
            "Foraging terrain can feed dispersed corps on the move.",
            "Enemies can be isolated and defeated before coalitions unite.",
        ],
        "strengths": [
            "Explains Austerlitz as leadership, mobility, and local superiority.",
            "Connects politics directly to military capacity.",
            "Shows why Britain used sea control and finance as strategic counters.",
        ],
        "weaknesses": [
            "Depends heavily on movement through supply-rich terrain.",
            "Produces enemies who learn and copy the system.",
            "Cannot solve Britain's naval and financial position by land victory alone.",
        ],
    },
    {
        "anchor": "napoleonic_limits",
        "session": "Session 10",
        "title": "Limits of Mass, Mobility, and Coalition War",
        "reading": "Lynn, TCHW Ch. 11; Session 10 one-pager",
        "situation": "Russia 1812 and Waterloo show Napoleon's system breaking against distance, climate, scorched earth, coalition learning, and British finance.",
        "intuition": "Napoleon's strengths became brittle at scale. Corps, foraging, and speed worked when terrain was rich and enemies accepted decisive battle. Russia turned defense into space, weather, delay, and political refusal; by Waterloo, the coalitions had learned Napoleonic methods and could absorb battlefield shocks.",
        "concepts": [
            ("Scorched earth", "Denying supplies and shelter to make enemy mobility self-destructive."),
            ("Strategic depth", "Using space to stretch the attacker and delay decision."),
            ("Coalition learning", "Enemies adopting the operational principles that once defeated them."),
            ("Sea control plus finance", "Britain's ability to protect trade, fund allies, and reconstitute coalitions."),
            ("Culminating point", "The stage where offensive power outruns its logistical and political base."),
        ],
        "assumptions": [
            "Defenders can trade space for time without political collapse.",
            "Coalition partners can coordinate rather than be defeated separately.",
            "Logistics, weather, and hostile population can overpower battlefield genius.",
        ],
        "strengths": [
            "Explains Russia as logistical failure, not just winter myth.",
            "Frames Waterloo as coalition-system victory, not only one battle.",
            "Ties together mass, mobility, supply chains, leadership, and offense-defense.",
        ],
        "weaknesses": [
            "Can understate Napoleon's remaining tactical skill.",
            "Needs careful chronology: Russia, Leipzig, and Waterloo are different failures.",
            "Risk of hindsight if coalition resilience is treated as inevitable.",
        ],
    },
]


def para(text, style="Body"):
    return Paragraph(text, styles[style])


def bullets(items):
    return ListFlowable(
        [ListItem(para(x, "RefBullet"), bulletColor=DARK_NAVY) for x in items],
        bulletType="bullet",
        start="circle",
        leftIndent=9,
        bulletFontSize=5,
    )


def kv_bullets(items):
    return bullets([f"<b>{term}</b> - {desc}" for term, desc in items])


def header_table(fw, width):
    title = f"{fw['session']} | {fw['title']}"
    data = [[Paragraph(f"<b>{title}</b><br/><font size='7'><i>{fw['reading']}</i></font>", styles["Small"])]]
    t = Table(data, colWidths=[width])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), DARK_NAVY),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def strengths_table(fw, width):
    col_w = (width - 8) / 2
    left = [Paragraph("<b>Strengths</b>", styles["Body"])] + [Paragraph(f"- {x}", styles["Small"]) for x in fw["strengths"]]
    right = [Paragraph("<b>Weaknesses</b>", styles["Body"])] + [Paragraph(f"- {x}", styles["Small"]) for x in fw["weaknesses"]]
    rows = max(len(left), len(right))
    data = []
    for i in range(rows):
        data.append([left[i] if i < len(left) else "", right[i] if i < len(right) else ""])
    t = Table(data, colWidths=[col_w, col_w])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                ("BACKGROUND", (1, 0), (1, -1), WARM_AMBER),
                ("BOX", (0, 0), (-1, -1), 0.35, BORDER_GREY),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER_GREY),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def add_framework(story, fw, width):
    story.append(BookmarkAnchor(fw["anchor"], fw["title"]))
    story.append(header_table(fw, width))
    story.append(Spacer(1, 4))
    story.append(para("<b>SITUATION</b>", "Section"))
    story.append(para(fw["situation"]))
    story.append(para("<b>CORE INTUITION</b>", "Section"))
    story.append(para(fw["intuition"]))
    story.append(para("<b>KEY CONCEPTS, KEYWORDS, AND TERMINOLOGY</b>", "Section"))
    story.append(kv_bullets(fw["concepts"]))
    story.append(para("<b>ASSUMPTIONS</b>", "Section"))
    story.append(bullets(fw["assumptions"]))
    story.append(para("<b>STRENGTHS / WEAKNESSES</b>", "Section"))
    story.append(strengths_table(fw, width))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER_GREY)
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, 0.43 * inch, letter[0] - doc.rightMargin, 0.43 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(doc.leftMargin, 0.28 * inch, DOC_TITLE)
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.28 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=letter,
        leftMargin=0.52 * inch,
        rightMargin=0.52 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.58 * inch,
        title=DOC_TITLE,
        author="Ares via Claudia",
    )
    width = letter[0] - doc.leftMargin - doc.rightMargin
    story = []
    story.append(para(DOC_TITLE, "CoverTitle"))
    story.append(
        para(
            "GPPS 444 - History of Warfare | Spring 2026 | Vice Admiral Robert Thomas, USN (ret.) | UC San Diego GPS",
            "CoverSub",
        )
    )
    desc = Table(
        [[
            para(
                "Exam-ready midterm reference built from existing Ares study guides, Thomas's course framework, the extracted syllabus, machine-readable slides, and the Parker-edited TCHW text. Warfare concepts are treated as the course's practical theories: each page gives a situation, intuition, vocabulary, assumptions, and strengths/weaknesses for quiz or essay deployment.",
                "Small",
            )
        ]],
        colWidths=[width],
    )
    desc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(desc)
    story.append(Spacer(1, 6))
    story.append(para("<b>Hyperlinked Table of Contents</b>", "Section"))
    for i, fw in enumerate(frameworks, 1):
        story.append(para(f"{i}. <a href='#{fw['anchor']}' color='#2C5282'>{fw['title']}</a>", "TOC"))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="35%", color=BORDER_GREY, thickness=0.5, hAlign="LEFT"))
    story.append(
        para(
            "Generated with GPT-5 Codex via the Claudia agent system. Course: GPPS 444, History of Warfare, Thomas, UC San Diego. Always verify against official course materials and readings. This is a study aid and does not substitute for careful reading of the assigned texts.",
            "TinyGrey",
        )
    )
    story.append(PageBreak())

    for idx, fw in enumerate(frameworks):
        add_framework(story, fw, width)
        if idx != len(frameworks) - 1:
            story.append(PageBreak())

    story.append(PageBreak())
    story.append(para("References", "CoverTitle"))
    refs = [
        "Allmand, C. (2005). New weapons, new tactics, 1300-1500. In G. Parker (Ed.), <i>The Cambridge history of warfare</i> (rev. ed.). Cambridge University Press.",
        "Lynn, J. A. (2005). Nations in arms, 1763-1815. In G. Parker (Ed.), <i>The Cambridge history of warfare</i> (rev. ed.). Cambridge University Press.",
        "Parker, G. (Ed.). (2020). <i>The Cambridge history of warfare</i> (2nd ed.). Cambridge University Press.",
        "Thomas, R. (2026). <i>GPPS 444: A history of warfare, Spring 2026</i> [Syllabus and lecture slides]. University of California San Diego.",
    ]
    for ref in refs:
        story.append(para(ref, "Body"))
    story.append(Spacer(1, 6))
    story.append(
        para(
            "Generated for: Edgar Agunias<br/>Date: 2026-04-29<br/>Model: GPT-5 Codex<br/>Sources: GPPS 444 extracted syllabus, Ares memory, machine-readable course slides and handouts, existing Study Guides, and machine-readable TCHW PDF text<br/>Agent: Ares",
            "TinyGrey",
        )
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
