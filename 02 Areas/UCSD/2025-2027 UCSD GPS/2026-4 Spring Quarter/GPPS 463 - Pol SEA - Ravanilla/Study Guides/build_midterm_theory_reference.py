from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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


OUT_DIR = Path(__file__).resolve().parent
VERSION = "v1.3.1"
MODEL_PROVENANCE = "GPT-5 via Codex (reasoning effort not exposed)"
PDF_PATH = OUT_DIR / f"GPPS_463_Midterm_Theory_Reference_{VERSION}.pdf"
USABLE_WIDTH = 7.85 * inch

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
DEEP_GREEN = colors.HexColor("#2F6F5E")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
LIGHT_GREEN = colors.HexColor("#EDF7F2")
ACCENT_GOLD = colors.HexColor("#C69C3F")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
WARM_AMBER = colors.HexColor("#FFF5E6")
TEXT = colors.HexColor("#1F2933")


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


def esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=25,
        alignment=TA_CENTER,
        textColor=DARK_NAVY,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=TEXT,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=9.5,
        textColor=TEXT,
    )
)
styles.add(
    ParagraphStyle(
        name="TOC",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=10.2,
        leftIndent=2,
        spaceAfter=1,
        textColor=TEXT,
    )
)
styles.add(
    ParagraphStyle(
        name="SectionHead",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=9.2,
        textColor=DARK_NAVY,
        spaceBefore=3,
        spaceAfter=1,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=12.4,
        textColor=TEXT,
        spaceAfter=1,
    )
)
styles.add(
    ParagraphStyle(
        name="TightBullet",
        parent=styles["Body"],
        leftIndent=8,
        firstLineIndent=-5,
        bulletIndent=0,
    )
)
styles.add(
    ParagraphStyle(
        name="HeaderWhite",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=11.2,
        textColor=colors.white,
    )
)
styles.add(
    ParagraphStyle(
        name="HeaderSub",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.2,
        leading=8.4,
        textColor=colors.HexColor("#DDE7F3"),
    )
)


VISUAL_SLOTS = {
    "constructed_region": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/constructed_region_shared_experience_map.png",
        "graph": "Concept map: diversity nodes feeding into shared regional category and ASEAN/Cold War institutionalization.",
        "prompt": "Create a clean editorial concept-map graphic for a graduate study guide. Show Southeast Asia as a constructed political region, not a natural cultural unit. Use labeled nodes for maritime trade, colonial disruption, Cold War strategy, ASEAN institutionalization, and shared experience in diversity, with arrows converging on a central label 'Southeast Asia as political category'. Minimal cream background, navy lines, muted teal and gold accents, no flags, no cartoons, no small unreadable text.",
    },
    "mandala": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/mandala_fading_authority_rings.png",
        "graph": "Radial diagram: sacred/commercial center, fading authority rings, conditional peripheral allegiance.",
        "prompt": "Create a polished conceptual diagram of a precolonial Southeast Asian mandala polity. Show a bright central court or port hub, concentric rings of fading authority, tribute and trade arrows, and peripheral chiefs with conditional allegiance. Academic reference-sheet style, flat vector-like illustration, navy/teal/gold palette, labels limited to center, tribute, trade, fading authority, no modern borders, no cartoon people.",
    },
    "sinic_village": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/sinic_village_civic_capital_flow.png",
        "graph": "Causal flow: Dai Viet state delegation -> village councils/quotas/public works -> civic capital -> modern public goods/consumption.",
        "prompt": "Create a horizontal causal-flow graphic for Dell, Lane, and Querubin's Vietnam village-governance argument. Show Dai Viet state delegation leading to village councils, tax and conscription quotas, public works, repeated cooperation, civic capital, and modern public goods and consumption. Clean graduate political-economy style, subtle map-boundary motif, navy text boxes, green arrows, no decorative characters, no tiny paragraphs.",
    },
    "diamond_geography": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/diamond_geography_scale_ladder.png",
        "graph": "Scale ladder: continental biogeography -> proximate conquest toolkit -> institutional mediation -> within-SEA variation.",
        "prompt": "Create a conceptual scale-ladder diagram for Jared Diamond's geography argument as used in Southeast Asia politics. Show bottom layer 'continental biogeography', then domesticable species and east-west diffusion, then guns/germs/steel as proximate toolkit, then institutional mediation, ending with a warning label 'too coarse for within-SEA variation'. Editorial academic style, restrained colors, simple icons for crops, animals, ships, and institutions, no deterministic world map.",
    },
    "european_diversion": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/european_diversion_timeline.png",
        "graph": "Timeline: Rome collapse -> feudalism -> free towns/merchant coalitions -> nation-states -> naval projection into SEA.",
        "prompt": "Create a compact timeline graphic titled European Diversion for a politics study guide. Show five stages: Fall of Rome, feudal security bargains, free towns and merchant coalitions, fiscal-military nation-states, overseas naval projection into Southeast Asia. Use small symbolic icons, arrows, and one contrast callout 'mandalas stayed flexible/personalistic'. Navy, slate, and gold palette, clean print-friendly layout, no crowded text.",
    },
    "ajr_reversal": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/ajr_reversal_extractive_spillover.png",
        "graph": "Mechanism map: VOC monopoly violence -> output restriction/autarky -> destroyed commerce -> reversal of development.",
        "prompt": "Create an academic mechanism map for Acemoglu and Robinson's reversal-of-development argument in the Moluccas. Show VOC monopoly violence leading to spice-tree destruction, output restriction, defensive autarky by neighboring polities, destroyed commerce, and long-run underdevelopment. Use an abstract island-and-trade-network motif, red only for coercion, navy/gray for institutions, concise labels, no gore, no stereotyped imagery.",
    },
    "dell_olken": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/dell_olken_java_factory_catchment.png",
        "graph": "Spatial diagram: sugar factory catchment radius, roads/rail/irrigation/schools, durable agglomeration.",
        "prompt": "Create a spatial political-economy diagram for Dell and Olken's Java Cultivation System findings. Show a sugar factory at center, a 4-7 km catchment ring, cane villages, roads, rail, irrigation, schools, and modern manufacturing clustering around the old factory site. Clean reference-sheet graphic, muted green and navy palette, precise labels, no romantic plantation imagery, no people in distress.",
    },
    "war_eoi": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/stubbs_war_eoi_conditional_path.png",
        "graph": "Conditional path: war/security pressure + aid/market access + elite weakening -> strong state -> EOI, with Philippines failure branch.",
        "prompt": "Create a conditional causal-path diagram for Richard Stubbs on war and export-oriented industrialization. Show war and Cold War security pressure, U.S./Japanese aid and market access, elite disruption, strong state formation, and EOI success. Include a clearly marked Philippines failure branch where landed elites and weak tax capacity survive. Academic flowchart style, navy boxes, teal success path, amber caution branch, no battlefield imagery.",
    },
    "thai_miracle": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/thailand_non_developmental_state_growth_mix.png",
        "graph": "Balance chart: open economy, Chinese-Thai entrepreneurs, macro stability, land frontier, demography -> growth; 1997 fragility limit.",
        "prompt": "Create a polished balance-chart graphic for Thailand's non-developmental-state miracle. Show growth inputs on one side: open economy, Chinese-Thai entrepreneurial class, macro stability, land frontier, demographic transition, and cautious pro-business state. Show 1997 crisis, financial fragility, and inequality as limit tests on the other side. Graduate study-guide style, Thai case without flags or tourist imagery, navy/green/gold palette.",
    },
    "singapore_model": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/singapore_state_capitalism_control_panel.png",
        "graph": "Control-panel diagram: PAP state coordinates labor, savings, land, infrastructure, MNE attraction, logistics.",
        "prompt": "Create a clean control-panel style conceptual graphic for the Singapore development model. Center a capable PAP state coordinating labor discipline, CPF forced savings, land assembly, public housing, infrastructure, MNE-led manufacturing, and port/logistics services. Show markets operating inside state-shaped conditions, not laissez-faire. Modern editorial style, navy and teal with gold highlights, no skyline photo, no flag, no propaganda feel.",
    },
    "afc_paradox": {
        "asset": "Study Guides/assets/midterm_theory_reference_v1.3.0/hicken_crisis_reform_pressure_paradox.png",
        "graph": "Two-line comparison: Thailand severe shock -> reform pressure; Philippines mild shock -> institutional stickiness.",
        "prompt": "Create a two-track comparison graphic for Allen Hicken's Asian Financial Crisis reform-pressure paradox. Top track: Thailand, severe 1997 shock, visible institutional failure, reform pressure. Bottom track: Philippines, milder shock, status quo coalition survives, weak institutions remain sticky. Use simple line graphs or pressure gauges, academic reference-sheet style, navy/amber/teal palette, no stock-market clutter, concise labels.",
    },
}


ELI5_CONCLUSIONS = {
    "constructed_region": "ELI5: Southeast Asia is like a study group made from very different classmates. They became one group because outsiders, wars, trade, and ASEAN kept treating them as connected.",
    "mandala": "ELI5: A mandala kingdom was strongest near the king and weaker farther away, like a lamp whose light fades at the edge of the room.",
    "sinic_village": "ELI5: Dai Viet villages got practice solving problems together, so even after rulers changed, the habit of cooperation stuck around.",
    "diamond_geography": "ELI5: Geography gave some places an early toolbox, but it does not explain everything people later built with that toolbox.",
    "european_diversion": "ELI5: Europe's messy medieval fights accidentally trained rulers, towns, and merchants to raise money, build states, and send ships far away.",
    "ajr_reversal": "ELI5: The VOC did not just take spices. It broke the trading system so badly that places became poorer than they might have been.",
    "dell_olken": "ELI5: Java's sugar system was coercive, but it left roads, factories, and skills that later communities could still use.",
    "war_eoi": "ELI5: War can push states to get stronger, but only if it actually weakens old elites and gives the state room to build new export industries.",
    "thai_miracle": "ELI5: Thailand grew fast without a bossy developmental state because business networks, openness, and stability did a lot of the work, until finance got shaky.",
    "singapore_model": "ELI5: Singapore used markets, but the state set the rules, built the pipes, trained the workers, and kept everyone moving in the same direction.",
    "afc_paradox": "ELI5: A big crisis can force repairs, while a smaller crisis can let a weak system limp along unchanged.",
}


theories = [
    {
        "anchor": "constructed_region",
        "session": "LD1",
        "title": "Southeast Asia as a Constructed Political Region",
        "source": "What Is Southeast Asia? -- Nico Ravanilla (lecture frame); syllabus and lecture-gap memo",
        "priority": False,
        "author_context": "Ravanilla is teaching this as a contemporary area-studies and political-economy frame, after the Cold War had already made 'Southeast Asia' a strategic category and after ASEAN had made it an institutional one. The point is to treat the region as historically produced rather than naturally given.",
        "situation": "This frame explains why a region with no single language, religion, colonial ruler, or regime type still became a durable object of Cold War strategy, ASEAN institution-building, and comparative political analysis.",
        "intuition": "Southeast Asia is not a natural civilizational unit in the way older area-study categories sometimes pretend. Ravanilla's frame treats it as a politically constructed region held together by <b>shared experience in diversity</b>: maritime interaction, colonial disruption, Cold War strategy, and postwar institutionalization. The region became analytically real because military planners, scholars, diplomats, and ASEAN governments kept using the category. The exam move is to avoid reducing the region to culture or geography; instead, ask how common pressures produced divergent institutional responses across countries that differ sharply in religion, language, colonial history, regime type, and development outcomes.",
        "concepts": [
            ("Constructed region", "A category that becomes real through strategic, academic, and institutional use rather than through a single primordial identity."),
            ("Shared experience in diversity", "Ravanilla's unifying phrase: the region is held together by repeated exposure to diversity, not by sameness."),
            ("Leftover category", "The region was partly defined by what it was not: not India, not China, and not the Pacific. That origin warns against treating it as culturally obvious."),
            ("Cold War strategic label", "The term gained force when the region became a military and diplomatic problem after World War II."),
            ("ASEAN institutionalization", "One reason the category endured after its Cold War strategic birth."),
            ("Political economy toolkit", "The course asks how institutions, actors, and constraints generate different outcomes across cases."),
            ("Comparative puzzle", "Divergent GDP, HDI, corruption, and regime outcomes inside one region are the course's central empirical problem."),
        ],
        "assumptions": [
            "Regional categories shape what scholars compare and what policymakers treat as connected.",
            "Shared historical pressures can matter even when countries respond differently.",
            "Diversity itself can be an analytical feature rather than a problem to explain away.",
            "Institutional variation inside the region is large enough to make comparison useful.",
        ],
        "strengths": [
            "Prevents culture-only explanations of Southeast Asian politics.",
            "Sets up cross-country comparison as the default exam method.",
            "Connects ancient maritime networks to modern strategic and institutional labels.",
            "Explains why the course can compare unlike cases without pretending they are identical.",
        ],
        "weaknesses": [
            "Can become too broad if not paired with specific institutional mechanisms.",
            "Does not by itself explain why one country outperforms another.",
            "Risks making the region look more coherent than it felt to historical actors.",
            "Depends heavily on later strategic and scholarly usage, so it can obscure premodern self-understandings.",
        ],
        "exam_application": "Use this page to open comparison essays: define the region as a constructed comparison set, then move quickly to the mechanism that explains variation inside it. The strongest answers use the frame to avoid cultural essentialism while still naming shared pressures such as maritime trade, colonial intrusion, Cold War security, and ASEAN institutionalization.",
        "case_cues": "Good comparison cues: ASEAN as institutional reinforcement, Cold War military strategy as naming environment, maritime trade as older connective tissue, and internal divergence in regime type, HDI, corruption, colonial experience, and development as the puzzle the rest of the course explains.",
    },
    {
        "anchor": "mandala",
        "session": "LD2",
        "title": "Mandala as Equilibrium Institution",
        "source": "Wrecks and Wrongs: Prehistory to 1500 -- Bill Hayton (2014); Ravanilla LD2 lecture scaffolding",
        "priority": False,
        "author_context": "Hayton writes in the 2010s as a journalist-historian synthesizing archaeology, maritime history, and South China Sea historiography. Ravanilla uses that material to recover precolonial Southeast Asian agency before European colonial and modern nationalist categories took over the story.",
        "situation": "This theory explains why Angkor, Srivijaya, and other precolonial polities could dominate trade and ritual life without becoming hard-bordered territorial states.",
        "intuition": "The mandala was an institutional solution to ruler constraints: ecology, population, security, legitimacy, and limited monitoring capacity. Rulers could not monitor fixed territory like a modern state, so they organized power around a sacred and commercial center whose influence faded with distance. Ritual authority, patron-client ties, hydraulic works, tribute networks, and control of chokepoints substituted for cadastral maps and impersonal bureaucracy. The same flexibility that made mandalas adaptive also made them vulnerable to defection, legitimacy shocks, ecological breakdown, and technological displacement, which is why Ravanilla treats them as <b>self-undermining institutions</b> rather than failed nation-states.",
        "concepts": [
            ("Mandala", "A center-oriented, borderless polity whose authority fades with distance and depends on personal allegiance."),
            ("Cakravartin", "The wheel-turning universal ruler whose legitimacy is ritual and cosmological."),
            ("Patron-client ties", "Personalized exchange of protection, resources, and loyalty; powerful but hard to bureaucratize."),
            ("Self-undermining institution", "A form whose strengths generate its future vulnerabilities."),
            ("Entrepot", "A relay port that profits from controlling trade chokepoints, as Srivijaya did in the Straits."),
            ("Hydraulic infrastructure", "Canals, barays, and water-control systems that turned ecological constraints into agricultural surplus and political legitimacy."),
            ("Technological displacement", "A change such as better Chinese junk ships that reduced dependence on Srivijaya's intermediary position."),
        ],
        "assumptions": [
            "Premodern rulers faced severe monitoring and enforcement limits.",
            "Local elites could credibly switch allegiance when the center weakened.",
            "Legitimacy and trade control could substitute for bureaucratic territorial control.",
            "Peripheral allegiance is conditional; it lasts while the center can provide ritual, commercial, or military value.",
        ],
        "strengths": [
            "Explains rise and decline with the same mechanism.",
            "Gives a precise alternative to modern nation-state assumptions.",
            "Links ecology, religion, trade, and security in one exam-ready framework.",
            "Supplies vocabulary for comparing Southeast Asian decentralization to European feudalism.",
        ],
        "weaknesses": [
            "Can understate variation among Funan, Srivijaya, Angkor, Champa, and Majapahit.",
            "Does not fully explain why some states later centralized while others did not.",
            "Needs lecture-specific cases to avoid becoming a generic definition.",
            "Can sound too cultural unless tied to concrete ruler constraints and incentives.",
        ],
        "exam_application": "For a 'why Europe won' or state-formation prompt, present mandala as a rational response to monitoring limits, not as backwardness. Then contrast it with European feudalism's later conversion into fiscal-military states: both were decentralized security solutions, but only one path later hardened into taxation, capital markets, and overseas projection.",
        "case_cues": "Use Srivijaya for trade-chokepoint power, Angkor for hydraulic and ritual capacity, Champa for rotating river-valley authority, and Majapahit/Malacca for the transition from Indic mandala logics toward Islamic and commercial networks. The recurring mechanism is conditional allegiance: peripheral elites stay loyal while the center supplies protection, ritual legitimacy, or commercial access.",
    },
    {
        "anchor": "sinic_village",
        "session": "LD3",
        "title": "Sinic Village Governance and Civic Capital",
        "source": "The Historical State, Local Collective Action, and Economic Development in Vietnam -- Melissa Dell, Nathan Lane, and Pablo Querubin (2018)",
        "priority": False,
        "author_context": "Dell, Lane, and Querubin write in the 2010s historical political-economy tradition, using causal inference to test claims that older institutional zones still shape development. The paper enters debates about whether strong states destroy civil society or can generate local cooperation.",
        "situation": "This theory explains why villages on one side of a 1698 boundary in southern Vietnam still show higher consumption and civic participation than similar neighboring villages.",
        "intuition": "Dai Viet's Sinic state delegated tax, conscription, public works, and registry tasks to the village, forcing repeated local cooperation under a central mandate. Over centuries, villagers had to elect councils, fill quotas, maintain registers, redistribute land, and finance public goods, so cooperation became a learned local capacity rather than a one-time policy. Those informal norms survived the destruction of formal institutions under French, South Vietnamese, and socialist rule. The key contrast is not culture as essence, but administrative technology: one state made villages cooperate horizontally under state pressure, while the Khmer/Indic model organized peasants vertically through personal patrons.",
        "concepts": [
            ("Sinic state", "Centralized, bureaucratic, territorially uniform administration with the village as a governing unit."),
            ("Indic polity", "Personalistic patron-client rule associated with mandala organization and weaker village administration."),
            ("Institutionalized village governance", "The Dai Viet arrangement in which villages were responsible for taxes, public works, records, and conscription even when the center set the quotas."),
            ("Civic capital", "Durable norms and networks that make local cooperation easier."),
            ("Crowding in", "A strong state can generate civil society when it delegates implementation rather than absorbing all functions."),
            ("Regression discontinuity", "Comparison of neighboring units around a boundary to estimate a causal effect."),
            ("1698 Gia Dinh boundary", "The historical treatment line that lets the authors compare villages exposed to Dai Viet institutions earlier versus later."),
            ("Public-goods channel", "The mechanism from collective action to roads, schools, local tax capacity, and higher household consumption."),
        ],
        "assumptions": [
            "The 1698 boundary was plausibly unrelated to modern economic potential after controls.",
            "Informal norms can persist after formal institutions disappear.",
            "Village-level public goods and tax cooperation reflect a local collective-action channel.",
            "The relevant institutional contrast is administrative structure, not immutable ethnic culture.",
        ],
        "strengths": [
            "Combines historical depth with credible causal identification.",
            "Gives Ravanilla a clean Dai Viet-to-development causal sentence.",
            "Pushes beyond vague culture by naming a concrete administrative mechanism.",
            "Connects precolonial state type to modern consumption through measurable intermediate outcomes.",
        ],
        "weaknesses": [
            "External validity beyond the Vietnam boundary is limited.",
            "Sinic institutions bundle bureaucracy, literacy, village governance, and Confucian norms.",
            "Mechanism evidence relies partly on later proxies for older norms.",
            "The design estimates a local treatment effect, not every consequence of Sinic or Indic state forms.",
        ],
        "exam_application": "Deploy this when asked whether institutions persist after formal rupture. The exam sentence is: Dai Viet's village administration built civic capital by making local cooperation routine, so later regimes could destroy the formal rules without erasing the learned capacity for collective action.",
        "case_cues": "Use the 1698 Gia Dinh boundary as the clean empirical hook, then name the mechanisms: elected village councils, tax and conscription quotas, local registers, redistribution, and public works. Compare to the Khmer/Indic side to show that the difference is administrative design, not a vague claim about Vietnamese culture.",
    },
    {
        "anchor": "diamond_geography",
        "session": "LD4",
        "title": "Geography as Deep Constraint, Not Complete Explanation",
        "source": "Yali's Question, Prologue to Guns, Germs, and Steel -- Jared Diamond (1997)",
        "priority": False,
        "author_context": "Diamond wrote in the 1990s against racial explanations for global inequality and against thin cultural accounts that treated European dominance as self-evident. In this course, his argument is useful background, but Ravanilla treats it as too coarse for within-Southeast-Asia variation.",
        "situation": "This framework explains why Eurasian societies accumulated guns, germs, and steel before New Guinea or the Americas, but not why Vietnam and Cambodia diverged next door to each other.",
        "intuition": "Diamond's argument is that continental biogeography shaped the initial distribution of domesticable plants, animals, disease exposure, and technology diffusion. Eurasia's east-west axis let crops, animals, writing, and state technologies travel across similar climates, while large domesticable mammals generated both transport power and epidemic disease exposure. For Ravanilla, this is useful only as a deep constraint or amplifier. It cannot replace institutional analysis because the course's hardest questions are within-region and within-Eurasia: why some Southeast Asian polities centralized, commercialized, or industrialized while others did not despite broadly similar exposure to Eurasian crops, trade, and technology.",
        "concepts": [
            ("Yali's question", "Why did some societies get more cargo than others?"),
            ("Proximate causes", "Immediate tools of conquest such as steel weapons, ships, writing, and epidemic disease."),
            ("Ultimate causes", "Deeper conditions such as domesticable species and continental axes."),
            ("East-west axis", "Eurasia's climate band made crop and technology diffusion easier than north-south diffusion."),
            ("Amplifier", "Use geography to strengthen an institutional argument, not to replace it."),
            ("Domesticable species", "Plants and animals capable of producing surplus, density, specialization, transport, and disease exposure."),
            ("Continental scale", "The level where Diamond is strongest; below that, institutional variation becomes more important."),
        ],
        "assumptions": [
            "Environmental endowments shape long-run possibilities before modern institutions form.",
            "Diffusion is easier across similar climate zones.",
            "Biogeographic differences precede racial or cultural explanations.",
            "Geographic advantages matter through social and institutional mediation, not by magic.",
        ],
        "strengths": [
            "Rules out racist explanations for intercontinental inequality.",
            "Explains why European conquest had technological and epidemiological force.",
            "Provides the background for why Europe could project power into Southeast Asia.",
            "Gives a clean proximate-versus-ultimate vocabulary for short essays.",
        ],
        "weaknesses": [
            "Too coarse for the course's within-Southeast-Asia variation.",
            "Can become deterministic if treated as a full causal account.",
            "The sample SAQ pattern treats Diamond-alone answers as incomplete.",
            "Does not explain why similar geographic zones generated different institutions and state capacities.",
        ],
        "exam_application": "Use Diamond as an opening constraint or amplifier, then pivot to institutions. A strong answer says geography helps explain Europe's starting toolkit, but European state capacity and Southeast Asian institutional form explain how that toolkit became conquest, monopoly, and colonial extraction.",
        "case_cues": "For Southeast Asia, use Diamond to explain why Eurasian agriculture, disease exposure, ships, and metallurgy mattered at contact, then immediately narrow the scale. Melaka 1511 and the VOC in 1600 show the toolkit arriving; AJR, Dell-Olken, and Stubbs explain what institutions and geopolitical incentives did with it.",
    },
    {
        "anchor": "european_diversion",
        "session": "LD4",
        "title": "European Diversion: Feudalism to Free Towns to Nation-States",
        "source": "Why Did Europe Win? The European Diversion Lecture Framework -- Nico Ravanilla; sample SAQ calibration",
        "priority": False,
        "author_context": "This is Ravanilla's lecture synthesis rather than a single assigned author. It translates a broad historical-sociology story into exam mechanics: after Rome, Europe did not simply progress, it stumbled through security fragmentation, commercial bargaining, and fiscal-military consolidation.",
        "situation": "This framework explains why Europe, after Rome's collapse, developed the fiscal, military, commercial, and naval capacity to reach Southeast Asia first.",
        "intuition": "Ravanilla's lecture arc turns Europe's apparent chaos into an institutional sequence. Rome's collapse produced local autarky and feudalism, a decentralized security solution built around lords, vassals, serfs, and protection-for-service exchange. Trade fairs, merchant coalitions, and free towns then created islands of commercial autonomy where merchants could bargain for predictable rules. Territorial monarchs later converted those commercial and military resources into nation-states with capital markets, taxation, navies, and overseas capacity. The exam comparison is with the mandala: both solved security and monitoring problems through decentralization, but Europe's path eventually hardened into fiscal-military states while many Southeast Asian mandalas remained more flexible and personalistic.",
        "concepts": [
            ("Feudalism", "A lord-vassal-serf order exchanging land and protection for labor and military service."),
            ("Free towns", "Commercially autonomous urban spaces that protected merchant activity and political bargaining."),
            ("Merchant coalitions", "Networks such as Maghribi traders, Champagne fairs, and Hanseatic merchants that reduced transaction costs."),
            ("Nation-state", "A more centralized fiscal-military institution capable of capital mobilization and overseas projection."),
            ("Treaty of Tordesillas", "The 1494 Iberian division of the non-Christian world; a chronology anchor for early colonialism."),
            ("Caravel and galleon", "Naval technologies that mattered because European states and merchants could finance and deploy them."),
            ("Mercantilism", "The zero-sum trade doctrine that made spice, bullion, and monopoly control central colonial motives."),
        ],
        "assumptions": [
            "Security crises can produce institutional innovation rather than simple collapse.",
            "Commercial bargaining can convert local autonomy into broader state capacity.",
            "Naval technology matters most when embedded in fiscal and political institutions.",
            "The relevant contrast is institutional sequence, not European cultural superiority.",
        ],
        "strengths": [
            "Best template for the likely 'Why did Europe win?' SAQ.",
            "Uses comparison instead of Europe-only narrative.",
            "Shows how technology, markets, and state capacity fit together.",
            "Explains why Diamond's guns, germs, and steel needed state capacity behind them.",
        ],
        "weaknesses": [
            "Lecture-derived rather than a single assigned reading argument.",
            "Can overstate Europe's coherence if the sequence is made too smooth.",
            "Needs Southeast Asian contrast cases to earn full analytical credit.",
            "Risks turning a contingent path into an inevitable rise if not written carefully.",
        ],
        "exam_application": "For the likely colonization SAQ, write the causal chain: feudal security fragmentation created local bargains, free towns protected commerce, monarchs later consolidated taxation and navies, and those institutions converted Diamond's technology into overseas power. Then contrast mandalas to show why the comparison matters.",
        "case_cues": "Course anchors include the fall of Rome, feudal lord-vassal bargains, free towns and merchant coalitions, nation-state consolidation, the caravel/galleon, mercantilism, and the Treaty of Tordesillas. The Southeast Asian contrast should be institutional, not civilizational: mandalas solved different constraints and therefore accumulated different capacities.",
    },
    {
        "anchor": "ajr_reversal",
        "session": "LD5",
        "title": "Extractive Institutions and Reversal of Development",
        "source": "Reversing Development, Chapter 9 of Why Nations Fail -- Daron Acemoglu and James A. Robinson (2012)",
        "priority": False,
        "author_context": "Acemoglu and Robinson write in the early-2010s institutions-first development debate, arguing against geography-only and culture-only explanations. Their Southeast Asia chapter emphasizes how European coercion redirected already commercializing societies rather than merely exploiting stagnant ones.",
        "situation": "This theory explains why the Moluccas, once central to the global spice trade, fell into poverty after the VOC seized monopoly control and destroyed indigenous commercial networks.",
        "intuition": "Acemoglu and Robinson argue that European colonialism did not merely slow Southeast Asian development; it reversed a trajectory of commercialization. The VOC imposed extractive institutions to monopolize cloves, mace, and nutmeg, massacred or coerced local populations, restricted output to raise prices, and pushed neighboring polities into defensive autarky. The core mechanism is institutional: extraction concentrated power and wealth, destroyed open commerce, and locked in incentives against broad development. Ravanilla's lecture adds that the Dutch selected different extractive tools depending on local political structure, so 'extractive' is a family of strategies rather than one fixed policy.",
        "concepts": [
            ("Extractive institutions", "Political and economic arrangements that transfer wealth from many to a narrow elite."),
            ("Inclusive institutions", "Pluralistic politics and open economic rules with secure property rights and broad opportunity."),
            ("Reversal of development", "Colonial intervention actively undid existing commercial and institutional development."),
            ("VOC", "Dutch East India Company, a chartered company with military and monopoly authority."),
            ("Autarky response", "Neighboring states destroyed or abandoned export production to avoid VOC violence."),
            ("Reversal of fortune", "The broader AJR pattern in which once-dense or wealthy places became poorer under extractive colonial institutions."),
            ("Dutch optimization menu", "Ambon used coerced local elites, Banda used genocide and plantation rule, and Ternate/Tidore/Bacan saw spice-tree destruction."),
        ],
        "assumptions": [
            "Institutions are the main driver of long-run development outcomes.",
            "Precolonial Southeast Asian commerce could have continued developing absent VOC coercion.",
            "Extractive elites can maintain institutions that benefit them even after broad harm is visible.",
            "Local political structure shapes which extractive strategy colonizers choose.",
        ],
        "strengths": [
            "Powerful Moluccas cases: Ambon treaty, Banda genocide, spice supply restriction.",
            "Explains indirect regional damage beyond directly colonized places.",
            "Connects colonial institutional design to present underdevelopment.",
            "Provides the clearest vocabulary for institutional destruction and monopoly rent extraction.",
        ],
        "weaknesses": [
            "Counterfactual commercial trajectory is hard to prove.",
            "Struggles with Dell-Olken's positive Java persistence case.",
            "Can flatten local variation in how extraction worked.",
            "The inclusive-versus-extractive binary can hide intermediate cases such as China or post-apartheid South Africa.",
        ],
        "exam_application": "Use this when the prompt asks how colonialism changed the region's development path. The clean move is to distinguish monopoly rent extraction from mere conquest: VOC policy made production and trade politically dangerous, so even non-colonized neighbors retreated into autarky.",
        "case_cues": "Use Ambon for treaty-based elite coercion, Banda for genocide and plantation replacement, Ternate/Tidore/Bacan for spice-tree destruction, Banten and Maguindanao for defensive autarky, and Burma's move from Pegu to Ava for retreat from maritime commerce. Those cases let you show regional spillover, not only direct colonial rule.",
    },
    {
        "anchor": "dell_olken",
        "session": "LD5",
        "title": "Positive Persistence of Extractive Colonial Economies",
        "source": "The Development Effects of the Extractive Colonial Economy: The Dutch Cultivation System in Java -- Melissa Dell and Benjamin A. Olken (2020)",
        "priority": False,
        "author_context": "Dell and Olken write in the late-2010s historical economics literature, directly complicating the Acemoglu-Robinson expectation that extractive colonial institutions should leave only negative development legacies. Their case turns on the production technology of sugar and the geography of Java.",
        "situation": "This theory explains why areas near Dutch sugar factories in Java are more industrialized and richer today, even though the original system was coercive and extractive.",
        "intuition": "Dell and Olken show that 'extractive' is not specific enough. The Dutch Cultivation System coerced villages, but sugar production required local processing, roads, rail, irrigation, village administration, and labor coordination because cane spoils quickly after cutting. Those industrial and human-capital structures persisted after the colonial system ended, producing denser manufacturing and higher incomes around former factory sites. The exam contrast is with the Moluccas: rent extraction by output restriction destroyed commerce, while output extraction through local manufacturing left usable infrastructure and agglomeration effects. The moral judgment and the causal effect are separate: coercion can be abusive and still leave durable development channels.",
        "concepts": [
            ("Cultuurstelsel", "The Dutch Cultivation System forcing Javanese villages to grow sugar for colonial factories."),
            ("Catchment area", "The 4-7 km zone around a factory where villages supplied cane and labor."),
            ("Input-output linkages", "Supplier, processing, and market ties that make industry cluster locally."),
            ("Infrastructure persistence", "Roads and rail built for extraction continue supporting economic activity."),
            ("Counterfactual factory analysis", "Comparison of actual factory sites to feasible simulated alternatives."),
            ("Agglomeration", "The clustering of firms and skills around factory sites because one activity makes nearby related activities cheaper."),
            ("Communal land channel", "Village land arrangements and schools connected to the cultivation system helped preserve local productive capacity."),
        ],
        "assumptions": [
            "Historical factory locations can be compared to plausible unchosen sites.",
            "Local processing and transport constraints created durable economic structures.",
            "Long-run gains do not morally justify coercion, but they affect institutional persistence.",
            "The relevant comparison is not extraction versus no extraction, but different forms of extraction.",
        ],
        "strengths": [
            "Best counterpoint to a simple 'colonial extraction always hurts' answer.",
            "Gives concrete mechanisms: agglomeration, infrastructure, schooling, communal land.",
            "Pairs neatly with AJR for a two-Dutch-colonialisms essay.",
            "Uses unusually strong spatial evidence for a historical institutional claim.",
        ],
        "weaknesses": [
            "One island and one crop limit generalization.",
            "Site selection can never be perfectly ruled out.",
            "Positive persistence may obscure the coercive human costs of the system.",
            "The framework explains local persistence better than national political development.",
        ],
        "exam_application": "This is the best page for an essay that asks whether extraction always produces underdevelopment. Pair it with AJR: both are Dutch colonialism, but the Moluccas destroyed commerce through monopoly restriction while Java created durable local industry because sugar required nearby processing, roads, rail, and labor coordination.",
        "case_cues": "The evidence language to remember is factory proximity, 4-7 km catchment areas, counterfactual factory sites, spatial regression discontinuity, input-output linkages, infrastructure persistence, and communal-land schooling channels. The answer should separate moral evaluation from causal persistence: coercive extraction can be abusive and still leave productive structures.",
    },
    {
        "anchor": "war_eoi",
        "session": "LD6",
        "title": "War, Strong States, and Export-Oriented Industrialization",
        "source": "War and Economic Development: Export-Oriented Industrialization in East and Southeast Asia -- Richard Stubbs (1999)",
        "priority": False,
        "author_context": "Stubbs wrote in the late-1990s Asian Miracle debate, when scholars were arguing over markets, developmental states, and culture. He adds war and Cold War geopolitics as the missing historical environment that made state-building, aid, procurement, and export access possible.",
        "situation": "This theory explains why Japan, Korea, Taiwan, Singapore, Malaysia, Thailand, and Hong Kong could industrialize rapidly in a Cold War order that gave them security threats, aid, procurement, and market access.",
        "intuition": "Stubbs inserts war into the Asian miracle debate. War destroyed or weakened old elites, justified centralized state-building, injected U.S. and Japanese capital, and opened export markets for anti-communist allies. The mechanism has destructive, formative, and redistributive effects: old social structures are disrupted, stronger states are built under security pressure, and external resources flow to strategically important allies. The key negative case is the Philippines: war and U.S. rule did not dislodge landed elites or build a strong central state, so import-substitution, patronage, weak parties, and regional oligarchy persisted. War is therefore enabling, not automatic.",
        "concepts": [
            ("EOI", "Export-oriented industrialization, manufacturing for overseas markets."),
            ("ISI", "Import-substitution industrialization, domestic production behind protection."),
            ("Formative effects of war", "State-building, bureaucratic expansion, and mobilization produced around war."),
            ("Redistributive effects of war", "Aid, procurement, trade access, and capital flows redirected by security politics."),
            ("Weak predatory state", "Philippine pattern of elite capture, pork-barrel politics, and poor tax capacity."),
            ("Strong state / weak society", "A developmental pattern in which the state can override landed elites, labor, or local patrons."),
            ("Cold War capital injection", "Korean War and Vietnam War procurement, U.S. aid, and market access that helped allied economies industrialize."),
        ],
        "assumptions": [
            "Security threats can overcome peacetime elite resistance to state-building.",
            "Cold War allies received unusually favorable aid and market access.",
            "Industrialization required both domestic state capacity and external demand.",
            "War reshapes inherited institutions only when it changes the balance between state and society.",
        ],
        "strengths": [
            "Explains the timing of postwar export booms.",
            "Links colonial legacies to postcolonial security pressures.",
            "Philippine negative case ties W3 institutions to W6 war effects.",
            "Adds geopolitics to neoclassical and statist explanations of the Asian miracle.",
        ],
        "weaknesses": [
            "Hard to isolate war from education, land reform, and industrial policy.",
            "Does not fully explain post-1990 divergence.",
            "Can underplay domestic political choices by treating war as the driver.",
            "Fits Northeast Asian cases more tightly than every Southeast Asian case.",
        ],
        "exam_application": "Use Stubbs to bridge colonial legacies and the Asian Miracle. The mechanism is conditional: war creates pressure and resources, but development follows only when old elites are weakened and the state can redirect society toward exports, which is why the Philippines remains the critical negative case.",
        "case_cues": "Use Japan/Korea/Taiwan for procurement, aid, land reform, and strong-state formation; Singapore and Malaysia for Cold War labor control and threat discipline; and the Philippines for the failure case where landed elites, patronage, and weak tax capacity survived the war sequence. The contrast keeps war from becoming automatic destiny.",
    },
    {
        "anchor": "thai_miracle",
        "session": "LD8",
        "title": "Thailand's Non-Developmental-State Miracle",
        "source": "Thailand: The Making of a Miracle? -- Karel Jansen (2001)",
        "priority": True,
        "author_context": "Jansen wrote just after the 1997 Asian Financial Crisis, looking back at Thailand's boom with the crash already visible. That timing matters: he is explaining real growth while also warning that the 'miracle' rested on fragile financial and distributional foundations.",
        "situation": "This theory explains how Thailand sustained rapid growth without becoming a Korea-style developmental state or a directly colonized economy.",
        "intuition": "Jansen argues Thailand's miracle came from capital and labor accumulation, meaningful TFP growth, open trade, macro stability, and a dynamic Chinese-Thai entrepreneurial class working with a cautious, pro-business state. Thailand complicates the course's colonial-institutions story because it was never formally colonized, yet unequal treaties, buffer-state geopolitics, land concessions, and global markets still shaped its small-state, open-economy path. It also complicates developmental-state theory because the Thai state enabled business more than it directed industry: it maintained macro conditions and infrastructure while private networks drove much of the investment response. The 1997 crisis then exposes the limits of a miracle built on temporary factor conditions and fragile finance.",
        "concepts": [
            ("Factor accumulation", "Growth from more capital, labor, land, and education rather than only productivity."),
            ("TFP", "Total factor productivity, output gains not explained by measured inputs."),
            ("Chinese-Thai entrepreneurial class", "Commercial networks that supplied business capacity without heavy state planning."),
            ("Non-interventionist state", "A pro-business state that preserved stability and openness rather than picking champions."),
            ("Vanishing smile", "The 1997 crisis as a warning that earlier growth conditions were becoming exhausted."),
            ("Colonization by proxy", "Thailand avoided formal rule but accepted unequal treaties and concessions that constrained sovereignty."),
            ("Open-economy small state", "A growth path dependent on trade, foreign capital, and macro credibility more than autarkic industrial planning."),
        ],
        "assumptions": [
            "Entrepreneurial networks can substitute for Korea-style state industrial policy.",
            "Open trade and macro stability can sustain growth when paired with private capacity.",
            "Thailand's uncolonized status makes it a useful but imperfect counterfactual.",
            "A miracle can be real in output terms while fragile in institutional and financial terms.",
        ],
        "strengths": [
            "Shows the Asian miracle had multiple institutional routes.",
            "Connects W3 colonial legacy questions to post-midterm growth cases.",
            "Provides a useful contrast with Singapore's disciplined state capitalism.",
            "Keeps Thailand from being forced into the Korea/Taiwan developmental-state template.",
        ],
        "weaknesses": [
            "Land frontier and demographic advantages were temporary.",
            "Rising inequality challenges the miracle narrative.",
            "Thailand's small-state path struggled after the 1997 crisis.",
            "The framework can understate political instability and military-bureaucratic influence.",
        ],
        "exam_application": "Use Thailand as the uncolonized control case and as the non-developmental-state miracle. The best essay move is to show that Thailand confirms the importance of institutions and entrepreneurs while rejecting the idea that every Asian Miracle case needed Korea-style industrial discipline.",
        "case_cues": "Use Thailand's Chinese-Thai entrepreneurs, open economy, macro stability, land frontier, and rapid demographic transition as the growth package. Then add the 1997 crisis as the limit test: financial fragility and inequality reveal that a miracle can be real in growth-accounting terms while institutionally vulnerable.",
    },
    {
        "anchor": "singapore_model",
        "session": "LD9",
        "title": "Singapore Model: Disciplined State Capitalism",
        "source": "What Is the Singapore Model of Economic Development? -- W. G. Huff (1995)",
        "priority": True,
        "author_context": "Huff wrote in the mid-1990s, after Singapore's success was obvious but before later debates about inequality, foreign-labor dependence, and democratic limits became as prominent. He is explaining how a tiny post-1965 city-state made markets work through unusually invasive state coordination.",
        "situation": "This theory explains why Singapore could become an advanced economy by welcoming global capital while using a powerful state to discipline labor, savings, land, housing, and infrastructure.",
        "intuition": "Huff's Singapore is neither laissez-faire nor socialist planning. The PAP state made export capitalism work by controlling wages, weakening disruptive labor bargaining, forcing household savings through the CPF, assembling land, building housing and infrastructure, and attracting multinational firms to substitute for missing domestic entrepreneurs. The state did not reject markets; it changed the conditions under which markets operated, crowding in investment with ports, airports, education, sanitation, industrial estates, and credible administration. The model is highly effective but hard to copy because it depends on city-state scale, location, foreign economic presence, disciplined labor politics, and unusually deep state control.",
        "concepts": [
            ("State capitalism", "Market-facing growth steered by an activist state rather than left to prices alone."),
            ("MNE-led manufacturing", "Foreign firms supplied technology, production networks, and export capacity."),
            ("Central Provident Fund", "Forced-saving institution that financed public capacity and reserves."),
            ("Wage restraint", "Labor control through laws and wage institutions that kept exports competitive."),
            ("Crowding in", "Public infrastructure and human capital made private investment more profitable."),
            ("Statutory boards", "Quasi-public agencies that let Singapore implement policy with speed and technocratic discipline."),
            ("Entrepot continuity", "Singapore modernized an older chokepoint-trade role rather than inventing its geography from scratch."),
        ],
        "assumptions": [
            "Small size and strategic location made deep coordination possible.",
            "Foreign capital could substitute for domestic entrepreneurial scarcity.",
            "The PAP could sustain social discipline and long-horizon investment.",
            "A capable state can improve market performance without owning every productive asset.",
        ],
        "strengths": [
            "Strongest case against a pure free-market miracle story.",
            "Explains why infrastructure and services mattered as much as manufacturing.",
            "Gives a precise comparison to Thailand's lighter-touch state.",
            "Shows how authoritarian control, technocracy, and global capitalism can reinforce each other.",
        ],
        "weaknesses": [
            "City-state conditions are not easily portable.",
            "Political control and labor discipline carry democratic and distributional costs.",
            "Heavy dependence on foreign firms limits the nationalist developmental-state analogy.",
            "The model's success can hide how exceptional Singapore's location, size, and post-1965 crisis were.",
        ],
        "exam_application": "Use Singapore to separate markets from laissez-faire. A strong answer says Singapore embraced global capitalism, but only after the PAP state reshaped labor, savings, land, infrastructure, and MNE incentives so markets operated inside a disciplined political environment.",
        "case_cues": "Anchor the case in 1965 separation, city-state scale, port geography, MNE-led manufacturing, CPF forced savings, wage restraint, land assembly, public housing, statutory boards, and logistics infrastructure. Compare Thailand to show light-touch enabling versus Singapore's deeper social and economic discipline.",
    },
    {
        "anchor": "afc_paradox",
        "session": "LD10",
        "title": "Asian Financial Crisis and the Reform-Pressure Paradox",
        "source": "The Political Economy of the Asian Financial Crisis -- Allen Hicken (2008); LD10 discussion memory",
        "priority": True,
        "author_context": "Hicken wrote in 2008, after the 1997 Asian Financial Crisis but before the global financial crisis fully unfolded. That timing makes his Thailand-Philippines comparison especially useful for asking whether mild crisis survival preserves weak institutions until a later shock exposes them.",
        "situation": "This theory explains why Thailand's deeper 1997 crisis produced more reform pressure, while the Philippines' milder crisis let weak institutions survive.",
        "intuition": "Hicken's paradox is that weathering the storm can be politically dangerous. Thailand was hit harder by the Asian Financial Crisis, but severity created pressure for institutional reform because the old financial, party, and bureaucratic arrangements became visibly costly. The Philippines was less damaged, so elites could postpone costly changes to parties, banks, and state capacity; weak institutions survived precisely because they did not trigger a sufficiently dramatic collapse. The exam-ready point is not simply 'crisis causes reform'; it is that crisis severity changes whether weak institutions become politically unsustainable. Because Hicken wrote before the 2008 global financial crisis, later shocks become useful tests of whether mild survival still delays reform.",
        "concepts": [
            ("Crisis severity", "The depth of economic shock that changes the political cost of maintaining the status quo."),
            ("Reform pressure", "Demand for institutional change created when old arrangements become visibly costly."),
            ("Weathering the storm", "Surviving a crisis well enough that weak institutions avoid scrutiny."),
            ("Institutional stickiness", "Elites resist reform when the current system still protects their rents."),
            ("Timing test", "Hicken wrote before the 2008 global financial crisis, making later shocks useful for reassessment."),
            ("Status quo coalition", "Actors who benefit from weak parties, financial opacity, or patronage and therefore prefer limited reform."),
            ("Comparative crisis politics", "The method of comparing Thailand and the Philippines by how shock severity changed incentives for institutional change."),
        ],
        "assumptions": [
            "Elites reform institutions only when crisis makes inaction politically costly.",
            "A milder shock can preserve weak but rent-producing arrangements.",
            "Financial crisis effects operate through domestic political institutions, not just markets.",
            "Public recognition of institutional failure matters for converting economic pain into reform.",
        ],
        "strengths": [
            "Sharp comparative mechanism for Thailand versus the Philippines.",
            "Extends the course's weak-state Philippine thread beyond Stubbs.",
            "Useful for seminar questions because the argument is counterintuitive.",
            "Makes crisis politics about incentives and institutions, not just macroeconomic damage.",
        ],
        "weaknesses": [
            "Reform quality can vary even after severe crises.",
            "Later shocks may alter the reading's implications.",
            "Needs careful separation from a simplistic 'more crisis is better' claim.",
            "A mild crisis may still trigger quiet technocratic change that the framework can miss.",
        ],
        "exam_application": "Use this for crisis-politics prompts: do not say crisis automatically improves institutions. Say crisis severity changes elite incentives and public recognition of failure; Thailand faced enough pain to make reform politically necessary, while the Philippines could keep postponing harder fixes.",
        "case_cues": "The compact comparison is Thailand as severe shock and reform pressure versus the Philippines as milder shock and institutional survival. Add the 2008 timing caveat when useful: Hicken wrote before the later global crisis, so subsequent shocks become tests of whether weathering 1997 preserved the same weak arrangements.",
    },
]


def bullet_items(items):
    return [Paragraph(f"<bullet>&bull;</bullet>{esc(item)}", styles["TightBullet"]) for item in items]


def concept_items(items):
    return [
        Paragraph(f"<bullet>&bull;</bullet><b>{esc(term)}</b> -- {esc(defn)}", styles["TightBullet"])
        for term, defn in items
    ]


def header_bar(theory):
    bg = DEEP_GREEN if theory["priority"] else DARK_NAVY
    title = f"{theory['session']} -- {theory['title']}"
    if theory["priority"]:
        title += " [POST-MIDTERM]"
    table = Table(
        [
            [Paragraph(esc(title), styles["HeaderWhite"])],
            [Paragraph(esc(theory["source"]), styles["HeaderSub"])],
        ],
        colWidths=[USABLE_WIDTH],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.25, bg),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def strengths_table(theory):
    left = [Paragraph("<b>Strengths</b>", styles["Body"])] + bullet_items(theory["strengths"])
    right = [Paragraph("<b>Weaknesses</b>", styles["Body"])] + bullet_items(theory["weaknesses"])
    rows = max(len(left), len(right))
    data = []
    for i in range(rows):
        data.append([left[i] if i < len(left) else "", right[i] if i < len(right) else ""])
    col_w = (USABLE_WIDTH - 0.08 * inch) / 2
    t = Table(data, colWidths=[col_w, col_w])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
                ("BACKGROUND", (1, 0), (1, 0), WARM_AMBER),
                ("BOX", (0, 0), (-1, -1), 0.4, BORDER_GREY),
                ("LINEAFTER", (0, 0), (0, -1), 0.35, BORDER_GREY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def paired_table(left_items, right_items, left_title, right_title):
    left = [Paragraph(f"<b>{esc(left_title)}</b>", styles["Body"])] + left_items
    right = [Paragraph(f"<b>{esc(right_title)}</b>", styles["Body"])] + right_items
    rows = max(len(left), len(right))
    data = []
    for i in range(rows):
        data.append([left[i] if i < len(left) else "", right[i] if i < len(right) else ""])
    col_w = (USABLE_WIDTH - 0.08 * inch) / 2
    t = Table(data, colWidths=[col_w, col_w])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT_GREEN),
                ("BACKGROUND", (1, 0), (1, 0), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.35, BORDER_GREY),
                ("LINEAFTER", (0, 0), (0, -1), 0.3, BORDER_GREY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return t


def asset_path(slot):
    asset = Path(slot["asset"])
    if asset.parts[:2] == ("Study Guides", "assets"):
        asset = Path(*asset.parts[1:])
    return OUT_DIR / asset


def visual_asset_block(theory):
    slot = VISUAL_SLOTS[theory["anchor"]]
    image_path = asset_path(slot)
    if not image_path.exists():
        raise FileNotFoundError(f"Missing visual asset for {theory['anchor']}: {image_path}")

    image = Image(str(image_path))
    max_w = 5.85 * inch
    max_h = 3.28 * inch
    scale = min(max_w / image.imageWidth, max_h / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale

    data = [
        [image],
        [Paragraph(f"<b>Visual logic:</b> {esc(slot['graph'])}", styles["Small"])],
        [Paragraph(f"<b>Asset:</b> {esc(slot['asset'])}", styles["Small"])],
    ]
    t = Table(data, colWidths=[USABLE_WIDTH])
    t.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.35, BORDER_GREY),
                ("LINEBELOW", (0, 0), (-1, -2), 0.25, BORDER_GREY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def theory_page(theory):
    story = [BookmarkAnchor(theory["anchor"], theory["title"]), header_bar(theory), Spacer(1, 2)]
    story.append(Paragraph("SITUATION", styles["SectionHead"]))
    story.append(Paragraph(esc(theory["situation"]), styles["Body"]))
    story.append(Paragraph("AUTHOR / TIME-PERIOD CONTEXT", styles["SectionHead"]))
    story.append(Paragraph(esc(theory["author_context"]), styles["Body"]))
    story.append(Paragraph("CORE INTUITION", styles["SectionHead"]))
    story.append(Paragraph(theory["intuition"], styles["Body"]))
    story.append(Paragraph("KEY CONCEPTS / ASSUMPTIONS", styles["SectionHead"]))
    story.append(
        paired_table(
            concept_items(theory["concepts"]),
            bullet_items(theory["assumptions"]),
            "Course vocabulary",
            "Assumptions",
        )
    )
    story.append(Paragraph("STRENGTHS / WEAKNESSES", styles["SectionHead"]))
    story.append(strengths_table(theory))
    story.append(Paragraph("EXAM APPLICATION", styles["SectionHead"]))
    story.append(Paragraph(esc(theory["exam_application"]), styles["Body"]))
    story.append(Paragraph("CASE / COMPARISON CUES", styles["SectionHead"]))
    story.append(Paragraph(esc(theory["case_cues"]), styles["Body"]))
    story.append(Paragraph("CONCEPTUAL VISUAL", styles["SectionHead"]))
    story.append(KeepTogether(visual_asset_block(theory)))
    story.append(Paragraph("ELI5 CONCLUSION", styles["SectionHead"]))
    story.append(Paragraph(esc(ELI5_CONCLUSIONS[theory["anchor"]]), styles["Body"]))
    story.append(PageBreak())
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(doc.leftMargin, 0.34 * inch, "GPPS 463 Midterm Theory Reference")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.34 * inch, f"p. {doc.page}")
    canvas.restoreState()


def cover_story():
    story = [
        Paragraph("GPPS 463 Midterm Theory Reference", styles["CoverTitle"]),
        Paragraph(
            "Politics of Southeast Asia · Prof. Nico Ravanilla · UC San Diego GPS · Spring 2026",
            styles["CoverSub"],
        ),
    ]
    desc = (
        "Exam-ready reference built from Poseidon's existing GPPS 463 study guides and machine-readable "
        "course PDFs. The first eight entries consolidate Midterm 1 theory and lecture scaffolding; the final "
        "three entries extend the same framework through the post-midterm Asian Miracle, Singapore, and Asian "
        "Financial Crisis materials. v1.3.1 embeds the 11 generated conceptual visuals and retains short "
        "ELI5 conclusions for each major theory/topic."
    )
    box = Table([[Paragraph(desc, styles["Small"])]], colWidths=[USABLE_WIDTH])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.extend([box, Spacer(1, 7), Paragraph("<b>Clickable Table of Contents</b>", styles["SectionHead"])])
    for i, theory in enumerate(theories, start=1):
        tag = " [post-midterm]" if theory["priority"] else ""
        story.append(
            Paragraph(
                f'{i}. <a href="#{theory["anchor"]}" color="#2C5282">{esc(theory["title"])}{tag}</a>',
                styles["TOC"],
            )
        )
    story.extend(
        [
            Spacer(1, 7),
            HRFlowable(width="36%", thickness=0.4, color=BORDER_GREY, hAlign="LEFT"),
            Paragraph(
                f"Generated with {MODEL_PROVENANCE} via the Claudia agent system. Course: GPPS 463, Prof. Nico "
                "Ravanilla, UC San Diego GPS, Spring 2026. Always verify against official course materials "
                "and readings. This document is a study aid and does not substitute for careful reading of "
                "the assigned texts.",
                styles["Small"],
            ),
            PageBreak(),
        ]
    )
    return story


def build():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=0.28 * inch,
        rightMargin=0.28 * inch,
        topMargin=0.28 * inch,
        bottomMargin=0.36 * inch,
    )
    story = cover_story()
    for theory in theories:
        story.extend(theory_page(theory))
    if isinstance(story[-1], PageBreak):
        story.pop()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(PDF_PATH)
