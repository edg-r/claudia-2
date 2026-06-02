from pathlib import Path
import shutil
import textwrap

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
COURSE_DIR = BASE_DIR.parent
ASSET_DIR = BASE_DIR / "assets" / "gpps463_theory_reference_v1.1.0"
PDF_PATH = BASE_DIR / "GPPS463_theory_reference_v1.1.0.pdf"
NOTES_PATH = BASE_DIR / "GPPS463_theory_reference_v1.1.0_notes.md"
VERSION = "v1.1.0"
MODEL_PROVENANCE = "GPT-5 Codex (reasoning effort not exposed)"

DARK = colors.HexColor("#17324D")
BLUE = colors.HexColor("#256D85")
GREEN = colors.HexColor("#2F6F5E")
GOLD = colors.HexColor("#B8872D")
TEXT = colors.HexColor("#202A34")
MUTED = colors.HexColor("#5F6B76")
LIGHT_BLUE = colors.HexColor("#EAF4F7")
LIGHT_GREEN = colors.HexColor("#EDF7F2")
LIGHT_GOLD = colors.HexColor("#FFF7E8")
LIGHT_GREY = colors.HexColor("#F5F6F8")
LINE = colors.HexColor("#C9D1D8")
WARM = colors.HexColor("#FFF4E3")


def rel(path):
    return COURSE_DIR / path


THEORIES = [
    {
        "anchor": "constructed_region",
        "session": "LD1",
        "title": "Southeast Asia as a Constructed Political Region",
        "source": "Ravanilla lecture frame; syllabus extraction",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/constructed_region_shared_experience_map.png"),
        "situation": "Southeast Asia became a useful political category despite lacking one religion, language, colonial ruler, regime type, or development path.",
        "intuition": "The region is best treated as historically constructed rather than naturally unified. Maritime interaction, colonial disruption, Cold War strategy, and ASEAN institution-building made Southeast Asia analytically real. Ravanilla's frame is useful because it keeps diversity at the center: the shared experience is not sameness, but repeated exposure to common pressures that produced divergent state and development outcomes.",
        "concepts": [
            ("Constructed region", "a category made durable by strategic, academic, and institutional use."),
            ("Shared experience in diversity", "the region's unity comes from common pressures across very different societies."),
            ("Area studies frame", "a comparative lens that asks why cases within a region diverge."),
            ("ASEAN institutionalization", "postwar organization that helped stabilize the regional category."),
            ("Political economy puzzle", "variation in institutions, coalitions, state capacity, and development."),
        ],
        "assumptions": [
            "Regional labels shape what scholars and policymakers compare.",
            "Shared pressures can matter even when responses diverge.",
            "Culture alone cannot explain the region's political variation.",
        ],
        "strengths": ["Prevents essentialist claims about a single Southeast Asian culture.", "Frames the whole course as comparative political economy.", "Explains why maritime geography and external pressure recur."],
        "weaknesses": ["Broad frame rather than a precise causal theory.", "Can understate within-country variation.", "Needs case-specific mechanisms to explain outcomes."],
        "caption": "Mechanism: repeated external and institutional pressures turn a diverse zone into a durable political category. Assumption: categories shape comparison. Strength/limit: excellent map for the course, but too broad to predict specific outcomes alone.",
        "refs": ["Ravanilla, N. (2026). GPPS 463 course lectures and syllabus materials. University of California San Diego."],
    },
    {
        "anchor": "mandala",
        "session": "LD2",
        "title": "Mandala Authority and Maritime Trading Networks",
        "source": "Hayton (2014), Ch. 1; Ravanilla lecture frame",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/mandala_fading_authority_rings.png"),
        "situation": "Srivijaya and other precolonial polities projected influence through ports, ritual authority, tribute, and trade without fixed modern borders.",
        "intuition": "Precolonial Southeast Asian authority often worked through mandalas: centers of sacred and commercial power whose authority faded with distance. Maritime networks such as the Nusantao world made coastal movement, monsoon timing, and entrepots central to state formation. The point is not that Southeast Asia lacked politics; it had a different institutional technology from modern territorial bureaucracy.",
        "concepts": [
            ("Mandala", "center-out authority with overlapping allegiance rather than fixed borders."),
            ("Nusantao", "Solheim's term for maritime trading and communication networks."),
            ("Entrepot", "port intermediary linking China, South Asia, and island Southeast Asia."),
            ("Monsoon cycle", "seasonal wind system that structured sailing and commercial dwell time."),
            ("Indic adoption", "selective elite use of Sanskrit, Hindu-Buddhist forms, and kingship models."),
        ],
        "assumptions": ["Authority can be personal and relational without modern borders.", "Trade routes can generate political power.", "Local elites selectively adapt outside cultural forms."],
        "strengths": ["Restores precolonial Southeast Asian agency.", "Explains why maritime nodes mattered more than interior borders.", "Useful contrast with Sinic village bureaucracy."],
        "weaknesses": ["Can romanticize flexible authority.", "Less precise for modern state capacity.", "Mandala logic varied sharply across mainland and island cases."],
        "caption": "Mechanism: trade and ritual centrality produce authority that fades outward. Assumption: allegiance is negotiated, not territorially fixed. Strength/limit: captures precolonial order, but needs later institutional analysis for modern development.",
        "refs": ["Hayton, B. (2014). Wrecks and wrongs: Prehistory to 1500. In *The South China Sea: The struggle for power in Asia* (Ch. 1). Yale University Press."],
    },
    {
        "anchor": "sinic_village",
        "session": "LD3",
        "title": "Sinic Village Governance and Civic Capital",
        "source": "Dell, Lane, and Querubin (2018)",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/sinic_village_civic_capital_flow.png"),
        "situation": "Vietnamese villages just inside the old Dai Viet frontier show better long-run public goods and consumption than nearby villages incorporated later.",
        "intuition": "Dell, Lane, and Querubin argue that historical state institutions can leave durable local capacity. Dai Viet delegated tax, conscription, and public-works responsibilities to village councils, which created repeated practice in collective action. That institutional habit persisted, producing civic capital that later improved public goods and economic outcomes.",
        "concepts": [
            ("Historical state", "precolonial administrative reach that shaped later development."),
            ("Regression discontinuity", "comparison around a historical boundary treated as plausibly exogenous."),
            ("Village councils", "local institutions responsible for quotas, records, and public works."),
            ("Civic capital", "local capacity for cooperation and public-goods provision."),
            ("Sinic vs. Indic institutions", "administrative villages versus looser patron-client mandalas."),
        ],
        "assumptions": ["Boundary assignment was not driven by modern development potential.", "Village institutions changed behavior, not just labels.", "Local collective-action capacity can persist across regimes."],
        "strengths": ["Strong causal identification for institutional persistence.", "Links ancient institutions to modern public goods.", "Clarifies Sinic-Indic contrast without cultural essentialism."],
        "weaknesses": ["Vietnam frontier case may not travel everywhere.", "Modern outcomes still reflect later colonial and socialist policies.", "Civic capital is hard to observe directly."],
        "caption": "Mechanism: delegated village obligations create repeated cooperation that persists as civic capital. Assumption: the boundary isolates institutional exposure. Strength/limit: credible local evidence, but portability beyond Vietnam is limited.",
        "refs": ["Dell, M., Lane, N., & Querubin, P. (2018). The historical state, local collective action, and economic development in Vietnam. *Econometrica, 86*(6), 2083-2121."],
    },
    {
        "anchor": "diamond_geography",
        "session": "LD4",
        "title": "Geography as Deep Constraint",
        "source": "Diamond (1997), Prologue",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/diamond_geography_scale_ladder.png"),
        "situation": "Diamond answers Yali's question by tracing unequal power to continental differences in domesticable species, diffusion, and disease exposure.",
        "intuition": "Diamond pushes explanation back to deep geography. Some regions accumulated productive crops, animals, pathogens, and technologies earlier because their environments made domestication and diffusion easier. The course use is as a baseline: geography explains broad world-historical inequality, but it is too coarse to explain why neighboring Southeast Asian states diverged politically and economically.",
        "concepts": [
            ("Ultimate causes", "deep geographic conditions behind later power differences."),
            ("Proximate causes", "guns, germs, steel, ships, and states."),
            ("East-west axis", "diffusion is easier across similar climates and latitudes."),
            ("Domesticable species", "plants and animals that enabled surplus and hierarchy."),
            ("Scale problem", "a theory can explain continents but miss regional variation."),
        ],
        "assumptions": ["Environmental starting conditions strongly shape long-run possibilities.", "Diffusion and domestication advantages compound over time.", "Broad material capacity precedes conquest."],
        "strengths": ["Useful antidote to racial or civilizational explanations.", "Explains large-scale timing differences.", "Provides a baseline before institutions enter."],
        "weaknesses": ["Too deterministic at small scales.", "Weak for within-Southeast Asia variation.", "Underplays agency, institutions, and colonial choices."],
        "caption": "Mechanism: geography shapes domestication, diffusion, and conquest toolkits. Assumption: early material advantages compound. Strength/limit: powerful at continental scale, weak for within-region institutional divergence.",
        "refs": ["Diamond, J. (1997). Prologue: Yali's question. In *Guns, germs, and steel: The fates of human societies*. W. W. Norton."],
    },
    {
        "anchor": "european_diversion",
        "session": "LD4",
        "title": "European Diversion and Colonial Capacity",
        "source": "Ravanilla lecture frame; Diamond contrast",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/european_diversion_timeline.png"),
        "situation": "Europe's fragmented post-Roman order produced fiscal-military states and merchant coalitions that later projected naval power into Southeast Asia.",
        "intuition": "The European diversion frame explains why Europe took a distinctive path toward coercive, commercial, and naval capacity. Feudal insecurity, free towns, merchant capital, and interstate competition forced rulers to bargain, tax, borrow, and fight. Those capacities later mattered in Southeast Asia, where flexible mandalas faced centralized European firms and states.",
        "concepts": [
            ("Fiscal-military state", "state capacity built through taxation, debt, and war-making."),
            ("Free towns", "commercial autonomy that strengthened merchants and capital markets."),
            ("Interstate competition", "rivalry that forced innovation in finance and coercion."),
            ("Naval projection", "capacity to move force and commerce overseas."),
            ("Institutional mismatch", "European territorial/state forms confronting mandala politics."),
        ],
        "assumptions": ["European fragmentation generated productive competition.", "War-making can build state capacity.", "Commercial institutions and coercion reinforced each other."],
        "strengths": ["Connects European history to colonial conquest.", "Explains capacity differences without civilizational superiority.", "Pairs well with colonial institution readings."],
        "weaknesses": ["Lecture synthesis more than one assigned article.", "Can overstate Europe and understate Southeast Asian adaptation.", "Needs case detail for Dutch, British, French, Spanish variation."],
        "caption": "Mechanism: fragmented security competition builds fiscal, merchant, and naval capacity. Assumption: war and commerce reinforce institutional development. Strength/limit: explains European projection, but not colonial effects by itself.",
        "refs": ["Ravanilla, N. (2026). GPPS 463 lecture materials on European colonial capacity. University of California San Diego."],
    },
    {
        "anchor": "ajr_reversal",
        "session": "LD5",
        "title": "Extractive Institutions and Reversal of Development",
        "source": "Acemoglu and Robinson (2012), Ch. 9",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/ajr_reversal_extractive_spillover.png"),
        "situation": "The VOC's violent spice monopoly in eastern Indonesia damaged trade networks and pushed neighboring societies toward defensive autarky.",
        "intuition": "Acemoglu and Robinson's reversal argument is that colonialism often damaged places that had previously been commercially developed. Extractive institutions restricted production, coerced labor, and destroyed local markets to benefit colonizers. In Indonesia, monopoly violence did not simply extract wealth; it changed incentives for surrounding polities, making commerce dangerous and undercutting long-run development.",
        "concepts": [
            ("Extractive institutions", "rules that transfer wealth upward rather than broaden opportunity."),
            ("Inclusive institutions", "rules that protect property, entry, and broad participation."),
            ("Reversal of development", "formerly richer areas become poorer after extractive colonialism."),
            ("VOC monopoly", "Dutch company rule organized around coercive control of spices."),
            ("Defensive autarky", "retreat from markets to avoid colonial predation."),
        ],
        "assumptions": ["Colonial institutions changed incentives durably.", "Local commerce was damaged by monopoly coercion.", "Extractive rules can spill beyond directly ruled territory."],
        "strengths": ["Sharp mechanism linking colonialism to long-run underdevelopment.", "Explains why precolonial prosperity could reverse.", "Useful contrast with Dell and Olken's positive persistence."],
        "weaknesses": ["Can flatten differences across colonial powers.", "Less attentive to mixed or unintended colonial legacies.", "Broad institutional categories can be blunt."],
        "caption": "Mechanism: monopoly violence destroys commerce and induces market retreat. Assumption: extractive rules persist through incentives. Strength/limit: clarifies reversal, but struggles with mixed colonial effects.",
        "refs": ["Acemoglu, D., & Robinson, J. A. (2012). *Why nations fail: The origins of power, prosperity, and poverty* (Ch. 9). Crown Business."],
    },
    {
        "anchor": "dell_olken",
        "session": "LD5",
        "title": "Positive Persistence of Extractive Colonial Economies",
        "source": "Dell and Olken (2018)",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/dell_olken_java_factory_catchment.png"),
        "situation": "Java villages near Dutch sugar factories were coerced under the Cultivation System, yet later had more infrastructure, schooling, and manufacturing.",
        "intuition": "Dell and Olken complicate the simple colonial-extraction-bad story. The Cultivation System was coercive, but sugar production required roads, rail, irrigation, factory skills, and administrative organization. Those localized investments persisted, creating industrial agglomeration and higher modern outcomes near former factory catchments.",
        "concepts": [
            ("Cultivation System", "Dutch forced cultivation regime in nineteenth-century Java."),
            ("Factory catchment", "area around sugar factories supplying cane and labor."),
            ("Agglomeration", "clustering of infrastructure, skills, and firms."),
            ("Persistence", "historical investments continuing to shape modern outcomes."),
            ("Coercive development", "growth-enhancing infrastructure created through exploitative rule."),
        ],
        "assumptions": ["Factory placement can be separated from preexisting advantages.", "Infrastructure and skills persist over time.", "Extraction can leave useful capital even when morally coercive."],
        "strengths": ["Avoids one-note colonial legacy claims.", "Provides credible micro evidence.", "Explains why some extractive systems left developmental residues."],
        "weaknesses": ["Positive local effects do not justify coercion.", "Java sugar may be unusually infrastructure-intensive.", "Distributional harms can be hidden by average effects."],
        "caption": "Mechanism: coercive sugar production builds durable infrastructure and skills. Assumption: local factory exposure created persistent advantages. Strength/limit: captures mixed legacies, but not the human costs of extraction.",
        "refs": ["Dell, M., & Olken, B. A. (2020). The development effects of the extractive colonial economy: The Dutch Cultivation System in Java. *Review of Economic Studies, 87*(1), 164-203. https://doi.org/10.1093/restud/rdz017"],
    },
    {
        "anchor": "stubbs_war",
        "session": "LD6",
        "title": "War, Strong States, and Export-Oriented Industrialization",
        "source": "Stubbs (1999)",
        "image_source": rel("Study Guides/assets/midterm_theory_reference_v1.3.0/stubbs_war_eoi_conditional_path.png"),
        "situation": "Cold War security pressures helped some Asian states build capacity and shift into export-oriented industrialization, while the Philippines remained weak.",
        "intuition": "Stubbs argues that war and Cold War geopolitics were central to the Asian miracle. Security threats disrupted old elites, justified stronger states, brought U.S. and Japanese aid, and opened external markets. The mechanism is conditional: war helps development when it strengthens state capacity and export discipline, not when it merely destroys territory or leaves old elites intact.",
        "concepts": [
            ("Export-oriented industrialization", "growth strategy based on producing for foreign markets."),
            ("Security pressure", "insurgency and external threat that motivate state-building."),
            ("Aid and market access", "geostrategic resources from allies and core economies."),
            ("Elite disruption", "weakening of landed or patronage elites blocking reform."),
            ("Philippine exception", "case where war did not create a strong developmental state."),
        ],
        "assumptions": ["Threats can discipline elites and rulers.", "Aid and market access are developmentally useful if institutions can use them.", "War's developmental effects depend on political context."],
        "strengths": ["Adds geopolitics to institutions and markets.", "Explains timing of EOI transitions.", "Highlights why similar colonial legacies can diverge after WWII."],
        "weaknesses": ["War often destroys rather than builds capacity.", "Philippine exception limits the claim.", "Can underplay domestic coalition politics."],
        "caption": "Mechanism: security pressure plus aid and elite disruption builds strong export states. Assumption: war strengthens rather than merely destroys institutions. Strength/limit: powerful for miracle cases, conditional for laggards.",
        "refs": ["Stubbs, R. (1999). War and economic development: Export-oriented industrialization in East and Southeast Asia. *Comparative Politics, 31*(3), 337-355."],
    },
    {
        "anchor": "krugman_growth",
        "session": "LD8-LD9",
        "title": "Growth Accounting and the Myth of the Asian Miracle",
        "source": "Krugman (1994)",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/krugman_growth_accounting_inputs_tfp.png"),
        "situation": "Singapore and other high-growth Asian economies looked miraculous, but much of their growth came from mobilizing more labor, capital, and education.",
        "intuition": "Krugman separates output growth into input accumulation and total factor productivity. Fast growth is less mysterious if countries save more, educate more, work more, and invest more. The warning is sustainability: input mobilization can be spectacular for a while, but eventually faces diminishing returns unless productivity rises.",
        "concepts": [
            ("Growth accounting", "decomposes output into input growth and productivity growth."),
            ("Total factor productivity", "efficiency in using labor and capital."),
            ("Input mobilization", "growth from more labor, capital, education, and savings."),
            ("Diminishing returns", "additional inputs eventually add less output."),
            ("Perspiration vs. inspiration", "effort and savings versus technological leap."),
        ],
        "assumptions": ["Inputs can be measured well enough to separate productivity.", "Input-driven growth faces ceilings.", "High growth rates should not be extrapolated mechanically."],
        "strengths": ["Punctures vague miracle rhetoric.", "Gives a common framework for Thailand and Singapore.", "Clarifies sustainability questions."],
        "weaknesses": ["Accounting is not a political explanation.", "Can understate institutional sophistication.", "Less useful for distribution or crisis response."],
        "caption": "Mechanism: output growth splits into inputs and productivity. Assumption: measured inputs can be separated from efficiency. Strength/limit: great anti-hype tool, but thin on politics.",
        "refs": ["Krugman, P. (1994). The myth of Asia's miracle. *Foreign Affairs, 73*(6), 62-78. http://www.jstor.org/stable/20046929"],
    },
    {
        "anchor": "thailand_miracle",
        "session": "LD8",
        "title": "Thailand's Entrepreneur-Led Non-Developmental State",
        "source": "Jansen (2001); LD8 lecture",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/thailand_entrepreneur_led_growth_networks.png"),
        "situation": "Thailand grew rapidly without Korea- or Singapore-style industrial planning, relying more on openness, macro stability, and Chinese-Thai business networks.",
        "intuition": "Thailand complicates the idea that miracles require a classic developmental state. The state preserved macro stability and openness, while private entrepreneurs, land, labor, savings, and FDI drove accumulation. This was not pure laissez-faire; it was a permissive, market-facing growth model with serious distributional and financial fragilities.",
        "concepts": [
            ("Non-developmental state", "growth-supporting state without heavy industrial planning."),
            ("Chinese-Thai entrepreneurs", "business networks in trade, finance, and production."),
            ("Macroeconomic orthodoxy", "stable prices, deficits, exchange rates, and external balance."),
            ("Open economy", "trade and FDI as growth channels."),
            ("Financial fragility", "weakness exposed by capital inflows and the 1997 crisis."),
        ],
        "assumptions": ["Private networks can coordinate investment under stable conditions.", "Openness can support growth without strong planning.", "Rural and labor exclusion can be politically managed for a time."],
        "strengths": ["Strong contrast to Singapore.", "Explains growth without overclaiming state planning.", "Links pre-1997 success to later vulnerability."],
        "weaknesses": ["Underexplains inequality and regional resentment.", "Weak political institutions limited redistribution.", "Financial liberalization exposed serious fragility."],
        "caption": "Mechanism: openness, stability, and business networks substitute partly for developmental planning. Assumption: private coordination works under macro stability. Strength/limit: explains growth, but also crisis vulnerability.",
        "refs": ["Jansen, K. (2001). Thailand: The making of a miracle? *Development and Change, 32*(2), 343-370."],
    },
    {
        "anchor": "singapore_model",
        "session": "LD9",
        "title": "Singapore's State-Created Comparative Advantage",
        "source": "Huff (1995); LD9 lecture",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/singapore_state_created_comparative_advantage.png"),
        "situation": "Singapore entered independence as a vulnerable, resource-poor city-state and built export competitiveness through state coordination.",
        "intuition": "Singapore used markets inside state-shaped conditions. The PAP state disciplined labor, forced savings through the CPF, built housing and infrastructure, attracted MNEs, and shifted the economy across phases. Comparative advantage was not discovered passively; it was created through capable, adaptive policy.",
        "concepts": [
            ("State-created comparative advantage", "policy changes capabilities and cost structures."),
            ("Export-oriented industrialization", "production for external markets."),
            ("CPF", "forced savings used for housing, infrastructure, and stability."),
            ("EDB", "state agency for attracting foreign investment."),
            ("MNE-led development", "foreign firms substitute for missing domestic industrial capital."),
        ],
        "assumptions": ["A capable state can shape markets without destroying signals.", "Foreign capital can serve national development when embedded locally.", "Labor discipline can generate stability and predictability."],
        "strengths": ["Best Southeast Asian case for active industrial policy.", "Shows openness and intervention can coexist.", "Links growth strategy to nation-building."],
        "weaknesses": ["Hard to replicate beyond a city-state.", "Political control and labor discipline carry democratic costs.", "Dependent on global demand and MNE strategies."],
        "caption": "Mechanism: the PAP state coordinates labor, savings, infrastructure, and MNE attraction. Assumption: capable bureaucracy can steer markets. Strength/limit: powerful model, but unusually hard to replicate.",
        "refs": ["Huff, W. G. (1995). The developmental state, government, and Singapore's economic development since 1960. *World Development, 23*(8), 1421-1438."],
    },
    {
        "anchor": "wade_afc",
        "session": "LD10",
        "title": "Wade's Global-Finance Account of the Asian Financial Crisis",
        "source": "Wade (2000)",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/wade_afc_global_finance_wheels.png"),
        "situation": "The 1997 crisis hit previously successful Asian economies, raising the question of whether the Asian model failed or global finance turned unstable.",
        "intuition": "Wade argues that domestic cronyism and weak regulation are only inner wheels. The outer wheels were volatile global capital markets, post-Bretton Woods liquidity, Japanese and European conditions, capital inflows, asset bubbles, and sudden reversals. The crisis was produced by the interaction between domestic vulnerabilities and international financial architecture.",
        "concepts": [
            ("Wheels within wheels", "nested domestic, regional, and global crisis mechanisms."),
            ("Hot money", "short-term mobile capital that can reverse rapidly."),
            ("Capital account openness", "exposure to cross-border financial volatility."),
            ("Washington Consensus", "liberalization package promoted after crisis."),
            ("Capital controls", "policy tool for limiting destabilizing flows."),
        ],
        "assumptions": ["Global financial architecture shapes crisis risk.", "Emerging markets are vulnerable to sudden stops.", "Post-crisis narratives are politically loaded."],
        "strengths": ["Corrects purely domestic-blame stories.", "Explains regional contagion and sudden reversal.", "Connects Southeast Asia to global political economy."],
        "weaknesses": ["Less precise on cross-national variation.", "Can underplay genuine local financial weakness.", "Policy remedy may be hard to implement."],
        "caption": "Mechanism: domestic vulnerabilities sit inside global capital-flow cycles. Assumption: external finance can destabilize good performers. Strength/limit: strong on system risk, weaker on country variation.",
        "refs": ["Wade, R. (2000). Wheels within wheels: Rethinking the Asian crisis and the Asian model. *Annual Review of Political Science, 3*, 85-115."],
    },
    {
        "anchor": "macintyre_veto",
        "session": "LD10",
        "title": "MacIntyre's Veto-Player Model",
        "source": "MacIntyre (2001)",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/macintyre_veto_players_policy_risk.png"),
        "situation": "During the Asian Financial Crisis, investors judged governments by whether institutions could respond credibly and decisively.",
        "intuition": "MacIntyre argues that veto authority shapes policy risk. Too few veto players create volatility because leaders can reverse policy abruptly. Too many create rigidity because policy change is blocked. The sweet spot is intermediate: enough vetoes for credible commitment, not so many that crisis response freezes.",
        "concepts": [
            ("Veto player", "actor whose agreement is needed to change policy."),
            ("Veto point", "institutional location where policy can be blocked."),
            ("Credible commitment", "belief that government will stick to policy."),
            ("Policy rigidity", "too many vetoes block adjustment."),
            ("Policy volatility", "too few vetoes allow abrupt swings."),
        ],
        "assumptions": ["Investors care about institutional policy posture.", "Veto authority can be compared across regimes.", "Crisis makes credibility and decisiveness especially valuable."],
        "strengths": ["Clean framework for AFC variation.", "Explains why both extremes can be bad.", "Bridges institutions and investor behavior."],
        "weaknesses": ["Informal veto actors complicate counts.", "The sweet spot is hard to identify.", "Better for investment response than democracy or equity."],
        "caption": "Mechanism: veto concentration creates risk through volatility at one extreme and rigidity at the other. Assumption: investors value both commitment and action. Strength/limit: elegant, but informal politics muddy the count.",
        "refs": ["MacIntyre, A. (2001). Institutions and investors: The politics of the economic crisis in Southeast Asia. *International Organization, 55*(1), 81-122. http://www.jstor.org/stable/3078598"],
    },
    {
        "anchor": "hicken2008",
        "session": "LD10",
        "title": "Crisis Severity and Reform Momentum",
        "source": "Hicken (2008)",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/hicken2008_crisis_severity_reform_momentum.png"),
        "situation": "Thailand was hit harder by the AFC but reformed more; the Philippines was hit less hard but let weak institutions survive.",
        "intuition": "Hicken's paradox is that severe crisis can generate political reform pressure, while a mild crisis can preserve the status quo. Thailand's collapse discredited old arrangements and helped produce constitutional reform and stronger party government. The Philippines' milder shock validated existing reforms and reduced urgency, leaving fiscal and governance problems unresolved.",
        "concepts": [
            ("Crisis as catalyst", "shock makes blocked reform politically possible."),
            ("Mild-shock trap", "less damage reduces pressure to repair weak institutions."),
            ("Reform momentum", "political energy generated by visible failure."),
            ("Thai Rak Thai", "post-1997 party benefiting from institutional change."),
            ("Philippine malaise", "continuing debt, revenue, and governance problems."),
        ],
        "assumptions": ["Reform requires urgency to overcome blockers.", "Visible failure can discredit incumbent institutions.", "Less severe crisis can preserve weak coalitions."],
        "strengths": ["Sharp Thailand-Philippines comparison.", "Explains why worse short-term damage can aid reform.", "Matches Edgar's confirmed Hicken angle."],
        "weaknesses": ["Severe crisis can also produce backlash.", "Reform quality is not guaranteed.", "Less useful outside crisis moments."],
        "caption": "Mechanism: severe crisis creates urgency; mild crisis preserves institutional stickiness. Assumption: reform needs political pressure. Strength/limit: powerful paradox, but severe shocks can also destabilize.",
        "refs": ["Hicken, A. (2008). Politics of economic recovery in Thailand and the Philippines. In A. MacIntyre, T. J. Pempel, & J. Ravenhill (Eds.), *East Asia ten years after the crisis*. Cornell University Press."],
    },
    {
        "anchor": "hicken2006",
        "session": "LD10",
        "title": "Party Fabrication and Thai Rak Thai",
        "source": "Hicken (2006)",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/hicken2006_party_fabrication_thai_rak_thai.png"),
        "situation": "Thailand's 1997 constitution altered electoral incentives and helped Thai Rak Thai build a more centralized, programmatic party machine.",
        "intuition": "Hicken argues that Thaksin and Thai Rak Thai were not only products of wealth or charisma. Constitutional reform changed party incentives by reducing fragmentation, discouraging party switching, strengthening executives, and creating institutions that rewarded larger parties. Stronger parties improved decisiveness, but also concentrated power and strained checks.",
        "concepts": [
            ("Party fabrication", "institutional construction of stronger party organizations."),
            ("1997 Constitution", "rules reshaping electoral and executive incentives."),
            ("Party fragmentation", "many weak parties and factional coalitions."),
            ("Programmatic appeal", "national policy platform beyond personal vote buying."),
            ("Prime-ministerial power", "stronger executive control over coalition politics."),
        ],
        "assumptions": ["Politicians adapt to electoral incentives.", "Party leaders can enforce discipline under new rules.", "Institutional design shapes party systems."],
        "strengths": ["Explains TRT beyond personality.", "Links crisis reform to party-system change.", "Shows why decisiveness can increase after fragmentation."],
        "weaknesses": ["Stronger parties can weaken accountability.", "Informal money and monarchy-military politics remain important.", "Does not by itself explain later coups."],
        "caption": "Mechanism: new electoral rules reduce fragmentation and empower stronger parties. Assumption: politicians adapt to incentives. Strength/limit: explains decisiveness, but not all informal vetoes.",
        "refs": ["Hicken, A. (2006). Party fabrication: Constitutional reform and the rise of Thai Rak Thai. *Journal of East Asian Studies, 6*, 381-407."],
    },
    {
        "anchor": "malesky_single_party",
        "session": "LD11",
        "title": "Inequality Inside Single-Party Regimes",
        "source": "Malesky, Abrami, and Zheng (2011)",
        "image_source": rel("Study Guides/assets/midterm2_theory_images/malesky_abrami_zheng_single_party_inequality.png"),
        "situation": "Vietnam and China are both fast-growing single-party regimes, but Vietnam has lower inequality because its internal party institutions are broader.",
        "intuition": "Malesky, Abrami, and Zheng shift the comparison from democracy versus dictatorship to variation inside authoritarian parties. Vietnam's broader Central Committee and more competitive internal structures force leaders to answer to a wider coalition, producing more equalizing transfers and public services than China's narrower top leadership bodies.",
        "concepts": [
            ("Authoritarian institutional variation", "differences inside nondemocratic regimes."),
            ("Winning coalition", "selectorate logic about whose support leaders need."),
            ("Central Committee", "broader party body in Vietnam's internal accountability."),
            ("Equalizing transfers", "fiscal redistribution across provinces."),
            ("Vertical checks", "constraints inside party hierarchy."),
        ],
        "assumptions": ["Authoritarian leaders face internal accountability.", "Coalition breadth shapes redistribution.", "Public spending decisions mediate inequality."],
        "strengths": ["Avoids crude democracy/dictatorship binaries.", "Explains Vietnam-China inequality contrast.", "Connects institutions to distribution."],
        "weaknesses": ["Internal party accountability is not democracy.", "Hard to measure informal elite bargaining.", "Growth and inequality also reflect markets and demography."],
        "caption": "Mechanism: broader party coalitions push leaders toward redistribution. Assumption: authoritarian elites still answer to internal constituencies. Strength/limit: strong within-regime comparison, not a democratic endorsement.",
        "refs": ["Malesky, E., Abrami, R., & Zheng, Y. (2011). Institutions and inequality in single-party regimes: A comparative analysis of Vietnam and China. *Comparative Politics, 43*(4), 401-419. http://www.jstor.org/stable/23040636"],
    },
    {
        "anchor": "ravanilla_deadly_populism",
        "session": "LD14",
        "title": "Deadly Populism and Local Outsider Incentives",
        "source": "Ravanilla, Sexton, and Haim (2022)",
        "diagram": ["Duterte mandate", "Outsider mayor", "Police effort", "Drug-war violence"],
        "situation": "Municipalities led by outsider mayors saw more antidrug incidents and police killings during Duterte's drug war.",
        "intuition": "Ravanilla, Sexton, and Haim show that national populist violence depends on local implementation incentives. Outsider mayors, lacking entrenched machines, could use aggressive drug-war cooperation to signal loyalty, build reputations, and improve reelection prospects. Accountability therefore runs through local electoral competition as well as Duterte's national rhetoric.",
        "concepts": [
            ("Deadly populism", "punitive mass appeal translated into lethal local action."),
            ("Local political outsider", "mayor without entrenched dynastic or machine roots."),
            ("Implementation incentives", "local reasons to carry out national policy aggressively."),
            ("Signaling loyalty", "using enforcement to align with the president."),
            ("Electoral accountability", "violence can be politically rewarded, not only imposed."),
        ],
        "assumptions": ["Local officials have discretion in national campaigns.", "Outsiders need visible signals to build support.", "Voters and police respond to presidential and local incentives."],
        "snapshot": [
            ("Political-economy mechanism", "National punitive populism becomes local violence when ambitious outsider mayors treat implementation as a way to win police support, presidential favor, and electoral credibility."),
            ("Author-specific argument", "The paper's distinctive claim is subnational: Duterte's rhetoric mattered, but variation in killings follows mayoral incentives and outsider status."),
            ("Course examples", "Philippine municipalities with outsider mayors show higher antidrug incidents and police killings; use this as the local-implementation case."),
            ("When assumptions fail", "If police, voters, or entrenched machines ignore mayoral signals, outsider status should not translate into extra violence."),
            ("Exam use / nearby contrast", "Contrast with Slater: both center coalitions, but Slater explains state capacity from elite protection pacts while Ravanilla et al. explain violent implementation through electoral incentives."),
        ],
        "strengths": ["Connects populism to subnational political economy.", "Shows why violence varied locally.", "Avoids treating Duterte as the only causal actor."],
        "weaknesses": ["Local incentives may interact with policing capacity and fear.", "Causal pathways can vary by municipality.", "Normative accountability remains difficult."],
        "caption": "Mechanism: national mandate is filtered through outsider mayor incentives and local police effort. Assumption: local officials have discretionary implementation power. Strength/limit: explains local variation, but national coercion still matters.",
        "refs": ["Ravanilla, N., Sexton, R., & Haim, D. (2022). Deadly populism: How local political outsiders drive Duterte's war on drugs in the Philippines. *The Journal of Politics, 84*(2), 1035-1056. https://doi.org/10.1086/715257"],
    },
    {
        "anchor": "ostwald_malapportionment",
        "session": "LD15",
        "title": "Malapportionment and UMNO/BN Dominance",
        "source": "Ostwald (2013)",
        "diagram": ["Votes", "Unequal districts", "Seat bonus", "BN survival"],
        "situation": "In Malaysia's 2013 election, BN lost the popular vote but retained a large seat advantage because its voters were concentrated in smaller districts.",
        "intuition": "Ostwald shows how electoral institutions convert votes into power unevenly. Single-member districts and malapportionment gave BN voters more parliamentary weight, especially in rural and Bumiputera-leaning constituencies. UMNO/BN dominance therefore relied not only on popularity or repression, but on an electoral geography that turned coalition support into a seat bonus.",
        "concepts": [
            ("Malapportionment", "unequal district size that gives some votes more weight."),
            ("Gerrymandering", "boundary design to advantage a party."),
            ("Single-member plurality", "winner-take-all district elections."),
            ("Seat-vote distortion", "gap between popular vote and legislative seats."),
            ("Rural weighting", "overrepresentation of lower-density districts."),
        ],
        "assumptions": ["District size and boundaries systematically advantage BN.", "Seat share matters more than national vote share for governing.", "Opposition support is inefficiently concentrated."],
        "snapshot": [
            ("Political-economy mechanism", "Electoral geography turns unequal district sizes into a parliamentary seat bonus, letting UMNO/BN preserve rule even when national vote share weakens."),
            ("Author-specific argument", "Ostwald's key move is to show that Malaysia's 2013 outcome was not simply fraud or popularity; institutional translation of votes into seats did causal work."),
            ("Course examples", "Use BN's 2013 popular-vote loss but parliamentary survival, especially rural/Bumiputera-weighted constituencies, as the anchor."),
            ("When assumptions fail", "If opposition support spreads efficiently across districts or the governing coalition fractures, malapportionment can delay but not guarantee dominance."),
            ("Exam use / nearby contrast", "Pair with Slater: Ostwald explains electoral survival rules; Slater explains the deeper elite coalition and state-capacity bargain behind durable rule."),
        ],
        "strengths": ["Concrete mechanism for authoritarian electoral durability.", "Explains popular-vote/seat-share mismatch.", "Pairs well with Slater's coalition story."],
        "weaknesses": ["Does not fully explain voter preferences.", "Predates the 2018 turnover.", "Malapportionment delays change but cannot prevent it forever."],
        "caption": "Mechanism: unequal districts convert votes into a governing seat bonus. Assumption: electoral geography is politically structured. Strength/limit: strong for 2013 dominance, less direct after 2018 turnover.",
        "refs": ["Ostwald, K. (2013). How to win a lost election: Malapportionment and Malaysia's 2013 general election. *The Round Table, 102*(6), 521-532. https://doi.org/10.1080/00358533.2013.857146"],
    },
    {
        "anchor": "slater_protection",
        "session": "LD16",
        "title": "Protection Pacts and Authoritarian Leviathans",
        "source": "Slater (2010), Ch. 1",
        "diagram": ["Contentious threat", "Elite pact", "Extract", "Organize"],
        "situation": "Malaysia and Singapore built stronger states than the Philippines or Thailand because elites had stronger reasons to coordinate around protection.",
        "intuition": "Slater's answer is coalitional. High state capacity emerges when elites face threatening contentious politics and decide that a stronger central state protects them better than fragmented private bargaining. Protection pacts allow rulers to extract resources and organize power, producing durable state, party, military, and authoritarian institutions.",
        "concepts": [
            ("Contentious politics", "strikes, riots, rebellions, protests, and insurgencies."),
            ("Elite collective action", "powerful groups coordinating around a shared institutional project."),
            ("Protection pact", "elite coalition backing strong state power against mass threat."),
            ("Provision pact", "weaker bargain based on benefits rather than shared protection."),
            ("Infrastructural power", "state capacity to implement policy across society."),
        ],
        "assumptions": ["Elites support capacity when disorder threatens them collectively.", "State strength requires elite collective action.", "Contention type shapes domination, fragmentation, or militarization."],
        "snapshot": [
            ("Political-economy mechanism", "Threatened elites accept taxation, coercion, and centralized organization when a stronger state protects property and order better than private bargaining."),
            ("Author-specific argument", "Slater argues authoritarian strength is not automatic; it depends on protection pacts forged under contentious threat."),
            ("Course examples", "Malaysia and Singapore illustrate stronger domination; Thailand and the Philippines are useful contrasts for fragmentation or weaker elite coordination."),
            ("When assumptions fail", "If contention is not collectively threatening, elites defect, rely on private protection, or support militarized rather than party-state solutions."),
            ("Exam use / nearby contrast", "Contrast with Stubbs: Stubbs makes war/security pressure the state-building shock; Slater makes domestic elite collective action the institutional hinge."),
        ],
        "strengths": ["Explains state capacity, party strength, and authoritarian durability together.", "Strong Southeast Asian case logic.", "Avoids assuming authoritarianism automatically builds capacity."],
        "weaknesses": ["Can make repression look institutionally productive.", "Less direct for democratic transitions.", "Elite threat perceptions are hard to measure."],
        "caption": "Mechanism: threatening contention creates elite protection pacts, enabling extraction and organization. Assumption: elites prefer strong states when protection is shared. Strength/limit: strong coalitional theory, but threat perception is difficult to observe.",
        "refs": ["Slater, D. (2010). To extract and to organize. In *Ordering power: Contentious politics and authoritarian Leviathans in Southeast Asia* (pp. 3-44). Cambridge University Press. https://doi.org/10.1017/CBO9780511760891.003"],
    },
    {
        "anchor": "tajima_segregation",
        "session": "LD18",
        "title": "Ethnic Segregation and Public Goods",
        "source": "Tajima, Samphantharak, and Ostwald (2018)",
        "diagram": ["Diverse district", "Segregated villages", "Advocacy", "Public goods"],
        "situation": "Indonesian districts can be ethnically diverse overall yet provide more discretionary public goods when ethnic groups are spatially segregated into homogeneous villages.",
        "intuition": "The article complicates the simple diversity-penalty argument. Ethnic fractionalization can hurt consensus and advocacy, but spatial segregation may let homogeneous villages coordinate more effectively and lobby district officials. Public goods in one village can then create spatial interdependence, giving other villages leverage to demand matching investments.",
        "concepts": [
            ("Ethnic fractionalization", "probability two people belong to different groups."),
            ("Spatial segregation", "groups separated into different local communities."),
            ("Decision level", "district level where allocation decisions are made."),
            ("User level", "village level where goods are consumed."),
            ("Spatial interdependence", "provision in one locality affects demands elsewhere."),
        ],
        "assumptions": ["Village advocacy affects district allocation.", "Homogeneous villages coordinate more easily.", "Discretionary public goods differ from formula-based goods."],
        "snapshot": [
            ("Political-economy mechanism", "Spatially homogeneous villages can solve local coordination problems and lobby district officials, so segregation can raise discretionary public-goods access despite district diversity."),
            ("Author-specific argument", "The authors separate ethnic fractionalization from spatial segregation, showing that diversity's effect depends on where political demand is organized."),
            ("Course examples", "Use Indonesian district-village allocation: diverse districts can still produce goods when village-level ethnic clustering supports advocacy."),
            ("When assumptions fail", "If goods are formula-based, officials ignore lobbying, or segregation increases conflict, the public-goods advantage should weaken or reverse."),
            ("Exam use / nearby contrast", "Contrast with simple diversity-penalty theories: this reading says diversity is not enough; political geography and allocation level matter."),
        ],
        "strengths": ["Separates diversity from spatial organization.", "Uses detailed Indonesian data.", "Explains when segregation can improve access to goods."],
        "weaknesses": ["Segregation has normative and social costs.", "Findings depend on allocation discretion.", "Integration may be valuable for reasons beyond public goods."],
        "caption": "Mechanism: segregated villages coordinate advocacy and use neighboring provision as leverage. Assumption: district officials respond to local lobbying. Strength/limit: clarifies political geography, but does not celebrate segregation.",
        "refs": ["Tajima, Y., Samphantharak, K., & Ostwald, K. (2018). Ethnic segregation and public goods: Evidence from Indonesia. *American Political Science Review, 112*(3), 637-653. https://doi.org/10.1017/S0003055418000136"],
    },
    {
        "anchor": "hayton_coc",
        "session": "LD19",
        "title": "South China Sea Code-of-Conduct Gridlock",
        "source": "Hayton (2021)",
        "diagram": ["ASEAN unity", "China leverage", "Scope/legal disputes", "Weak COC"],
        "situation": "After 25 years, ASEAN and China still had no binding South China Sea Code of Conduct because the process managed tensions without constraining China.",
        "intuition": "Hayton frames the COC as diplomatic process more than binding solution. ASEAN states want rules that constrain Chinese behavior, while China prefers bilateral leverage and a code that limits external actors rather than itself. Divergent ASEAN threat perceptions, scope disputes, legal-binding questions, and China's veto over agreement keep the process alive but weak.",
        "concepts": [
            ("Code of Conduct", "proposed rules for South China Sea behavior."),
            ("ASEAN consensus", "collective bargaining limited by divergent member interests."),
            ("Bilateral leverage", "China's preference for one-on-one bargaining."),
            ("UNCLOS", "legal baseline favored by Vietnam and other littoral states."),
            ("Process diplomacy", "talks that manage relations even without solving the dispute."),
        ],
        "assumptions": ["China benefits from delay and weak constraints.", "ASEAN members have divergent stakes.", "Diplomatic process can reduce escalation without resolving claims."],
        "snapshot": [
            ("Political-economy mechanism", "ASEAN's consensus process and China's bilateral leverage produce negotiations that manage tension while avoiding binding constraints on Chinese behavior."),
            ("Author-specific argument", "Hayton is skeptical: the COC process survives because it is useful diplomacy, not because it is close to solving the sovereignty/security problem."),
            ("Course examples", "Use the 25-year COC delay, disputes over scope/legal force, and China's preference for limiting external actors rather than itself."),
            ("When assumptions fail", "If ASEAN members coordinate tightly or China accepts enforceable rules, the process could become more than symbolic management."),
            ("Exam use / nearby contrast", "Contrast with Quang: Hayton emphasizes gridlock and process diplomacy; Quang identifies concrete design fixes and Vietnamese agenda-setting agency."),
        ],
        "strengths": ["Explains why talks persist despite failure.", "Shows ASEAN unity limits.", "Connects maritime disputes to institutional bargaining."],
        "weaknesses": ["Journalistic synthesis rather than formal model.", "Less systematic on U.S.-China competition.", "Future bargaining may change with shocks."],
        "caption": "Mechanism: ASEAN collective bargaining meets Chinese leverage and unresolved legal scope. Assumption: process can manage tensions without binding rules. Strength/limit: explains gridlock, but not a full grand-strategy theory.",
        "refs": ["Hayton, B. (2021, July 21). After 25 years, there's still no South China Sea code of conduct. *Foreign Policy*. https://foreignpolicy.com/2021/07/21/south-china-sea-code-of-conduct-asean/"],
    },
    {
        "anchor": "rand_influence",
        "session": "LD19",
        "title": "U.S.-China Competition for Influence",
        "source": "RAND Research Report (2020), Chs. 1-4",
        "diagram": ["U.S. offers", "China offers", "Partner alignment", "Relative influence"],
        "situation": "Southeast Asian states assess U.S. and Chinese influence by comparing what each power can offer or threaten across economic, military, and diplomatic channels.",
        "intuition": "RAND defines influence as the ability to shape another actor's behavior. In U.S.-China competition, relative influence matters more than absolute influence: partners compare economic incentives, military cooperation, diplomatic support, coercive risks, and alignment costs. Southeast Asian countries are not passive objects; they hedge, bargain, and choose issue-specific alignment.",
        "concepts": [
            ("Influence", "ability to shape another actor's behavior."),
            ("Competition for influence", "rivalry over partner alignment."),
            ("Relative influence", "U.S. influence compared with Chinese influence."),
            ("Partner alignment", "continued support on issues important to a major power."),
            ("Hedging", "keeping options open between competing powers."),
        ],
        "assumptions": ["States compare U.S. and Chinese offers strategically.", "Influence has economic, military, diplomatic, and coercive dimensions.", "Alignment can be partial and issue-specific."],
        "snapshot": [
            ("Political-economy mechanism", "Influence competition works through relative packages of markets, security, diplomacy, credibility, and coercive risk that Southeast Asian states compare issue by issue."),
            ("Author-specific argument", "RAND's value is measurement: influence is behavioral and relative, not just a count of visits, aid dollars, or favorable opinion."),
            ("Course examples", "Use hedging behavior: states may welcome U.S. security support while depending on Chinese trade or infrastructure."),
            ("When assumptions fail", "If domestic politics or regime survival concerns dominate foreign-policy choice, external offers alone will mispredict alignment."),
            ("Exam use / nearby contrast", "Pair with ASPI: RAND supplies the influence framework; Cutler/ASPI supplies one economic-statecraft route for rebuilding U.S. influence."),
        ],
        "strengths": ["Provides explicit measurement framework.", "Treats Southeast Asian states as strategic actors.", "Connects course politics to IR competition."],
        "weaknesses": ["Policy-report frame may reflect U.S. strategic priorities.", "Influence is difficult to measure cleanly.", "Can underplay domestic politics inside partner states."],
        "caption": "Mechanism: partner behavior reflects relative U.S. and Chinese incentives, coercion, and credibility. Assumption: Southeast Asian states compare offers across domains. Strength/limit: useful framework, but measurement is tricky.",
        "refs": ["Lin, B., Chase, M. S., Blank, J., Cooper, C. A., III, Grossman, D., Harold, S. W., Moroney, J. D. P., Morris, L. J., Ma, L., Orner, P., Shih, A., & Kim, S. (2020). *Regional responses to U.S.-China competition in the Indo-Pacific: Study overview and conclusions*. RAND Corporation. https://www.rand.org/pubs/research_reports/RR4412z6.html"],
    },
    {
        "anchor": "quang_coc",
        "session": "LD19",
        "title": "Saving the China-ASEAN Code of Conduct",
        "source": "Nguyen Minh Quang (2019)",
        "diagram": ["Vietnam chair", "Agenda setting", "Legal clarity", "COC progress"],
        "situation": "Quang argues that Vietnam's ASEAN chairmanship offered a chance to move stalled COC negotiations toward more meaningful rules.",
        "intuition": "Quang's Diplomat article treats the Code of Conduct as salvageable but stuck. Negotiations suffer from undefined geographic scope, dispute-settlement disagreement, competing conflict-management approaches, and uncertain legal status. Vietnam matters because its direct South China Sea stakes and ASEAN role could push agenda-setting, legal clarity, and coalition-building.",
        "concepts": [
            ("Geographic scope", "which waters and features the COC covers."),
            ("Dispute settlement", "how parties resolve violations or interpret rules."),
            ("Conflict management", "self-restraint, trust-building, and incident prevention."),
            ("Legal status", "whether the COC is binding or merely declaratory."),
            ("ASEAN chairmanship", "agenda-setting opportunity for a member state."),
        ],
        "assumptions": ["ASEAN agenda-setting can shift negotiations at the margin.", "Vietnam has both incentive and capacity to push stronger rules.", "COC progress depends on clarifying specific design problems."],
        "snapshot": [
            ("Political-economy mechanism", "Vietnam can use ASEAN chair agenda-setting to push legal clarity, negotiation sequencing, and coalition discipline against a stalled China-ASEAN bargaining process."),
            ("Author-specific argument", "Quang is more constructive than Hayton: the COC is not doomed, but it needs fixes on scope, dispute settlement, conflict management, and legal status."),
            ("Course examples", "Use Vietnam's direct South China Sea stakes and 2020 ASEAN chairmanship as the course-local case of small-state institutional agency."),
            ("When assumptions fail", "If ASEAN consensus collapses or China refuses constraint, chairmanship agency becomes procedural rather than substantive."),
            ("Exam use / nearby contrast", "Contrast with Hayton's gridlock frame and RAND's broader influence frame; Quang is the negotiation-design checklist."),
        ],
        "strengths": ["Names concrete negotiation blockers.", "Adds agency for Vietnam within ASEAN.", "Pairs well with Hayton's pessimism."],
        "weaknesses": ["Optimism depends on China's willingness to accept constraints.", "ASEAN consensus remains fragile.", "Canvas extract is text-only from a PDF, not the original PDF file."],
        "caption": "Mechanism: Vietnam's chairmanship could target scope, settlement, management, and legal-status problems. Assumption: ASEAN agenda-setting has leverage. Strength/limit: precise negotiation checklist, but China can still stall.",
        "refs": ["Nguyen, M. Q. (2019, June 29). Saving the China-ASEAN South China Sea Code of Conduct. *The Diplomat*."],
    },
    {
        "anchor": "aspi_trade",
        "session": "LD19",
        "title": "Trade Reengagement and the TPP Roadmap",
        "source": "Cutler (2020), ASPI Report introduction",
        "diagram": ["U.S. exit", "CPTPP baseline", "Sectoral steps", "Reengagement"],
        "situation": "The ASPI report argues that after U.S. withdrawal from TPP, reengagement with CPTPP countries could rebuild U.S. economic leadership in Asia.",
        "intuition": "Cutler's introduction frames trade architecture as strategic presence. The United States cannot compete for regional influence only through security ties; it needs economic rule-making and credible market engagement. The TPP/CPTPP framework offers a baseline, while sectoral deals on digital trade, essential goods, or climate could rebuild trust before full reentry.",
        "concepts": [
            ("TPP", "high-standard trade agreement originally signed by the United States and 11 partners."),
            ("CPTPP", "successor agreement concluded without the United States."),
            ("Economic statecraft", "using trade rules and market access to shape regional order."),
            ("Sectoral deals", "narrow agreements that rebuild engagement incrementally."),
            ("Credibility problem", "regional doubt after U.S. withdrawal from TPP."),
        ],
        "assumptions": ["Trade architecture shapes strategic influence.", "Asia-Pacific partners value U.S. economic engagement if credible.", "Incremental sectoral agreements can restore trust."],
        "snapshot": [
            ("Political-economy mechanism", "Trade rules create strategic presence by shaping market access, standards, supply-chain expectations, and partner confidence in U.S. commitment."),
            ("Author-specific argument", "Cutler's roadmap treats CPTPP as both economic architecture and credibility repair after U.S. withdrawal from TPP."),
            ("Course examples", "Use TPP withdrawal, CPTPP continuity without the United States, and sectoral digital/essential-goods/climate steps as the policy sequence."),
            ("When assumptions fail", "If U.S. domestic politics blocks credible market access, sectoral deals may look symbolic and China retains economic gravity."),
            ("Exam use / nearby contrast", "Pair with RAND: ASPI gives the trade-policy instrument; RAND explains why instruments matter for relative influence."),
        ],
        "strengths": ["Adds economic dimension to U.S.-China rivalry.", "Connects domestic U.S. trade politics to Southeast Asian alignment.", "Gives concrete policy pathway."],
        "weaknesses": ["Intro excerpt, not full report analysis.", "Domestic U.S. politics may block reentry.", "Trade rules alone cannot offset China's geographic/economic pull."],
        "caption": "Mechanism: credible trade engagement rebuilds U.S. regional influence through rules, access, and partner confidence. Assumption: economic architecture affects alignment. Strength/limit: concrete roadmap, but domestic politics constrain it.",
        "refs": ["Cutler, W. (2020). *Reengaging the Asia-Pacific on trade: A TPP roadmap for the next U.S. administration*. Asia Society Policy Institute."],
    },
]


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
            self.canv.addOutlineEntry(self._title, self._name, level=0, closed=False)


def xml_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text):
    return xml_escape(text).replace("*", "")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=26, alignment=TA_CENTER, textColor=DARK, spaceAfter=6))
    styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=TEXT, spaceAfter=7))
    styles.add(ParagraphStyle("TOC", parent=styles["Normal"], fontSize=7.8, leading=9.2, textColor=TEXT, spaceAfter=0.6))
    styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=7.2, leading=8.4, textColor=TEXT))
    styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=8.8, leading=10.6, textColor=TEXT, spaceAfter=3))
    styles.add(ParagraphStyle("BodyTight", parent=styles["Normal"], fontSize=8.2, leading=9.4, textColor=TEXT, spaceAfter=2))
    styles.add(ParagraphStyle("Micro", parent=styles["Normal"], fontSize=7.15, leading=8.1, textColor=TEXT, spaceAfter=1))
    styles.add(ParagraphStyle("MicroHead", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.1, leading=8.0, textColor=DARK, spaceAfter=0))
    styles.add(ParagraphStyle("H2", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=9, leading=10, textColor=DARK, spaceBefore=4, spaceAfter=2))
    styles.add(ParagraphStyle("HeaderWhite", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=12, textColor=colors.white))
    styles.add(ParagraphStyle("HeaderSub", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=7.4, leading=8.6, textColor=colors.HexColor("#DDE7F3")))
    styles.add(ParagraphStyle("Caption", parent=styles["Normal"], fontSize=7.6, leading=8.8, textColor=MUTED, spaceAfter=4))
    return styles


STYLES = make_styles()


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.35)
    canvas.line(doc.leftMargin, 0.48 * inch, letter[0] - doc.rightMargin, 0.48 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.32 * inch, "GPPS 463 Theory Reference")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.32 * inch, f"Page {doc.page}")
    canvas.restoreState()


def para(text, style="Body"):
    return Paragraph(inline(text), STYLES[style])


def bullet_items(items, style="BodyTight"):
    return [Paragraph(f"<b>{inline(term)}</b> -- {inline(desc)}", STYLES[style]) for term, desc in items]


def simple_bullets(items, style="BodyTight"):
    return [Paragraph(f"- {inline(item)}", STYLES[style]) for item in items]


def section(title, flowables):
    out = [Paragraph(title, STYLES["H2"])]
    out.extend(flowables)
    return out


def default_snapshot(theory):
    mechanism = theory["caption"].split(".")[0].replace("Mechanism: ", "")
    first_assumption = theory["assumptions"][0] if theory["assumptions"] else "The theory's scope conditions hold."
    first_limit = theory["weaknesses"][0] if theory["weaknesses"] else "The theory needs case-specific checks."
    return [
        ("Political-economy mechanism", mechanism),
        ("Author-specific argument", theory["intuition"].split(".")[0] + "."),
        ("Course examples", theory["situation"]),
        ("When assumptions fail", f"If {first_assumption[0].lower() + first_assumption[1:]} is violated, {first_limit[0].lower() + first_limit[1:]}"),
        ("Exam use / nearby contrast", f"Use this unit to connect {theory['title']} to the course's institutions, colonial legacy, state-building, and development thread."),
    ]


def snapshot_table(theory):
    rows = []
    for label, value in theory.get("snapshot", default_snapshot(theory)):
        rows.append([
            Paragraph(inline(label), STYLES["MicroHead"]),
            Paragraph(inline(value), STYLES["Micro"]),
        ])
    t = Table(rows, colWidths=[1.45 * inch, 5.48 * inch], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GREEN),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def deployment_table(theory):
    compare = theory.get("snapshot", default_snapshot(theory))[-1][1]
    rows = [
        ("Use when", theory["strengths"][0]),
        ("Contrast with", compare),
        ("Limit case", theory["weaknesses"][0]),
        ("One-sentence exam move", f"{theory['title']} explains {theory['situation'][0].lower() + theory['situation'][1:]}"),
    ]
    t = Table(
        [[Paragraph(inline(label), STYLES["MicroHead"]), Paragraph(inline(value), STYLES["Micro"])] for label, value in rows],
        colWidths=[1.45 * inch, 5.48 * inch],
        hAlign="CENTER",
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GOLD),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def header(theory, page_label):
    title = f"{theory['session']} | {theory['title']}"
    sub = f"{page_label} | {theory['source']}"
    t = Table([[Paragraph(inline(title), STYLES["HeaderWhite"])], [Paragraph(inline(sub), STYLES["HeaderSub"])]], colWidths=[7.2 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("BOX", (0, 0), (-1, -1), 0, DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def prepare_assets():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
        font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    except OSError:
        font_title = ImageFont.load_default()
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    for theory in THEORIES:
        dest = ASSET_DIR / f"{theory['anchor']}.png"
        if theory.get("image_source") and Path(theory["image_source"]).exists():
            shutil.copyfile(theory["image_source"], dest)
            theory["image_path"] = dest
            continue

        labels = theory.get("diagram", ["Condition", "Institution", "Policy", "Outcome"])
        img = Image.new("RGB", (1400, 850), "#F7F9FB")
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([34, 34, 1366, 816], radius=24, fill="#FFFFFF", outline="#C9D1D8", width=3)
        draw.text((80, 75), theory["title"], fill="#17324D", font=font_title)
        draw.text((80, 122), theory["session"], fill="#5F6B76", font=font_small)
        y = 300
        xs = [95, 410, 725, 1040]
        colors_fill = ["#EAF4F7", "#EDF7F2", "#FFF7E8", "#F1F5F9"]
        for i, label in enumerate(labels[:4]):
            box = [xs[i], y, xs[i] + 250, y + 135]
            draw.rounded_rectangle(box, radius=16, fill=colors_fill[i], outline="#17324D", width=3)
            wrapped = textwrap.wrap(label, width=17)
            ty = y + 38 - (len(wrapped) - 1) * 13
            for line in wrapped:
                tw = draw.textlength(line, font=font)
                draw.text((box[0] + 125 - tw / 2, ty), line, fill="#17324D", font=font)
                ty += 30
            if i < 3:
                draw.line([box[2] + 15, y + 67, xs[i + 1] - 15, y + 67], fill="#B8872D", width=8)
                draw.polygon([(xs[i + 1] - 15, y + 67), (xs[i + 1] - 40, y + 53), (xs[i + 1] - 40, y + 81)], fill="#B8872D")
        mechanism = theory["caption"].split(".")[0].replace("Mechanism: ", "")
        lines = textwrap.wrap(mechanism, width=80)
        draw.rounded_rectangle([130, 590, 1270, 735], radius=18, fill="#17324D", outline="#17324D")
        draw.text((170, 615), "Mechanism", fill="#FFFFFF", font=font_small)
        yy = 650
        for line in lines[:3]:
            draw.text((170, yy), line, fill="#FFFFFF", font=font_small)
            yy += 26
        img.save(dest)
        theory["image_path"] = dest


def validate_units():
    required = ["anchor", "session", "title", "source", "situation", "intuition", "concepts", "assumptions", "strengths", "weaknesses", "caption", "refs"]
    problems = []
    for theory in THEORIES:
        missing = [key for key in required if not theory.get(key)]
        if missing:
            problems.append(f"{theory.get('anchor', 'unknown')}: missing {', '.join(missing)}")
        if not theory.get("image_source") and not theory.get("diagram"):
            problems.append(f"{theory['anchor']}: no image source or diagram fallback")
    if problems:
        raise ValueError("Theory unit validation failed:\n" + "\n".join(problems))


def cover_page():
    story = [
        Paragraph("GPPS 463 Theory Reference", STYLES["CoverTitle"]),
        Paragraph("Politics of Southeast Asia | Nico Ravanilla | Spring 2026", STYLES["CoverSub"]),
    ]
    desc = (
        "Comprehensive syllabus-order reference for GPPS 463. Each unit gets exactly two pages: "
        "one explanation page and one visual/evaluation page. Built from existing midterm references, "
        "course study guides, local readings, Canvas-verified LD19 extracts, and Poseidon's course memory. "
        "LD12 is omitted as Canvas-confirmed no-source/no-discussion."
    )
    box = Table([[Paragraph(inline(desc), STYLES["Small"])]], colWidths=[7.2 * inch])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([box, Spacer(1, 6), Paragraph("Table of Contents", STYLES["H2"])])
    for i, theory in enumerate(THEORIES, 1):
        story.append(Paragraph(f'<a href="#{theory["anchor"]}">{i:02d}. {inline(theory["session"])} | {inline(theory["title"])}</a>', STYLES["TOC"]))
    story.extend([
        Spacer(1, 5),
        HRFlowable(width="35%", thickness=0.5, color=LINE, hAlign="LEFT"),
        Paragraph("Generated with GPT-5 Codex via the Claudia agent system for GPPS 463, Politics of Southeast Asia, Nico Ravanilla, UCSD. Always verify against official course materials and readings. This document is a study aid and does not substitute for careful reading of the assigned texts.", STYLES["Small"]),
        PageBreak(),
    ])
    return story


def theory_pages(theory):
    story = [
        BookmarkAnchor(theory["anchor"], f"{theory['session']} | {theory['title']}"),
        header(theory, "Page 1 of 2"),
        Spacer(1, 5),
    ]
    story.extend(section("Situation", [para(theory["situation"])]))
    story.extend(section("Core Intuition", [para(theory["intuition"])]))
    story.extend(section("Key Concepts, Keywords, and Terminology", bullet_items(theory["concepts"])))
    story.extend(section("Assumptions", simple_bullets(theory["assumptions"])))
    story.extend(section("Dense Exam Snapshot", [snapshot_table(theory)]))
    story.extend(section("Exam Deployment", [deployment_table(theory)]))
    story.append(PageBreak())

    story.extend([header(theory, "Page 2 of 2"), Spacer(1, 5)])
    img = RLImage(str(theory["image_path"]))
    img._restrictSize(6.9 * inch, 3.7 * inch)
    img.hAlign = "CENTER"
    story.extend([img, Paragraph(f"<b>Visual caption.</b> {inline(theory['caption'])}", STYLES["Caption"])])
    left = [Paragraph("<b>Strengths</b>", STYLES["H2"])] + simple_bullets(theory["strengths"])
    right = [Paragraph("<b>Weaknesses / Limits</b>", STYLES["H2"])] + simple_bullets(theory["weaknesses"])
    rows = max(len(left), len(right))
    left += [Paragraph("", STYLES["BodyTight"])] * (rows - len(left))
    right += [Paragraph("", STYLES["BodyTight"])] * (rows - len(right))
    table = Table([[left[i], right[i]] for i in range(rows)], colWidths=[3.48 * inch, 3.48 * inch])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("BACKGROUND", (1, 0), (1, -1), WARM),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("LINEAFTER", (0, 0), (0, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.extend(section("APA Reference", [Paragraph(inline(ref), STYLES["BodyTight"]) for ref in theory["refs"]]))
    story.append(PageBreak())
    return story


def disclosure_page():
    source_summary = (
        "GPPS 463 syllabus extraction; existing Midterm 1 and Midterm 2 theory references and assets; "
        "local readings and study guides for LD14-LD18; W10 Hayton and RAND PDFs; Canvas-verified Quang and ASPI text extracts; "
        "Canvas missing-source verification for LD12."
    )
    story = [
        BookmarkAnchor("disclosure", "References and Disclosure"),
        Paragraph("References and Disclosure", STYLES["CoverTitle"]),
        Paragraph("This PDF lists APA references inside each two-page theory unit so exam use stays local to the concept being reviewed.", STYLES["Body"]),
        Spacer(1, 12),
        Paragraph("Output Disclosure", STYLES["H2"]),
        Paragraph(f"Generated for: Edgar Agunias<br/>Date: 2026-06-01<br/>Model: {MODEL_PROVENANCE}<br/>Sources: {inline(source_summary)}<br/>Agent: Poseidon", STYLES["Body"]),
    ]
    return story


def write_notes():
    lines = [
        "# GPPS 463 Theory Reference v1.1.0 Notes",
        "",
        "Density revision source notes generated from the same data structure as the PDF.",
        "",
        "LD12 is omitted as Canvas-confirmed no-source/no-discussion unless future course-local lecture-summary provenance appears.",
        "",
    ]
    for i, theory in enumerate(THEORIES, 1):
        lines.extend([
            f"## {i:02d}. {theory['session']} | {theory['title']}",
            f"**Source:** {theory['source']}",
            "",
            f"**Situation:** {theory['situation']}",
            "",
            f"**Core intuition:** {theory['intuition']}",
            "",
            "**Key concepts:**",
        ])
        for term, desc in theory["concepts"]:
            lines.append(f"- **{term}:** {desc}")
        lines.extend(["", "**Assumptions:**"])
        for item in theory["assumptions"]:
            lines.append(f"- {item}")
        lines.extend(["", "**Dense exam snapshot:**"])
        for label, value in theory.get("snapshot", default_snapshot(theory)):
            lines.append(f"- **{label}:** {value}")
        lines.extend(["", "**Exam deployment:**"])
        for label, value in [
            ("Use when", theory["strengths"][0]),
            ("Contrast with", theory.get("snapshot", default_snapshot(theory))[-1][1]),
            ("Limit case", theory["weaknesses"][0]),
            ("One-sentence exam move", f"{theory['title']} explains {theory['situation'][0].lower() + theory['situation'][1:]}"),
        ]:
            lines.append(f"- **{label}:** {value}")
        lines.extend(["", "**Strengths:**"])
        for item in theory["strengths"]:
            lines.append(f"- {item}")
        lines.extend(["", "**Weaknesses / limits:**"])
        for item in theory["weaknesses"]:
            lines.append(f"- {item}")
        lines.extend(["", f"**Visual caption:** {theory['caption']}", "", "**APA reference:**"])
        for ref in theory["refs"]:
            lines.append(f"- {ref}")
        lines.append("")
    lines.extend([
        "---",
        "Generated for: Edgar Agunias",
        "Date: 2026-06-01",
        f"Model: {MODEL_PROVENANCE}",
        "Sources: GPPS 463 v1.0.0 theory reference build data and assets; Midterm 1 and Midterm 2 theory references/assets; local GPPS 463 study guides and readings; Canvas-verified Quang and ASPI extracts; Canvas LD12 verification note.",
        "Agent: Poseidon",
        "---",
        "",
    ])
    NOTES_PATH.write_text("\n".join(lines), encoding="utf-8")


def build():
    validate_units()
    prepare_assets()
    write_notes()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.52 * inch,
        leftMargin=0.52 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.62 * inch,
        title="GPPS 463 Theory Reference",
        author="Poseidon / Claudia",
    )
    story = cover_page()
    for theory in THEORIES:
        story.extend(theory_pages(theory))
    story.extend(disclosure_page())
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(PDF_PATH)
    print(f"theory_units={len(THEORIES)}")
    print(f"asset_dir={ASSET_DIR}")
