from copy import deepcopy
from html import escape
from pathlib import Path
import re
import textwrap
import unicodedata

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from build_midterm_theory_reference import THEORIES as MIDTERM_THEORIES


VERSION = "v1.0.0"
DATE = "2026-05-31"
MODEL = "GPT-5.5 (medium reasoning)"
COURSE = "GPCO 403 - International Economics"
INSTRUCTOR = "Professor Kyle Handley"
TITLE = "GPCO 403 Comprehensive Theory Reference"

ROOT = Path(__file__).resolve().parent
OUT = ROOT / f"GPCO403_theory_reference_{VERSION}.pdf"
NOTES_OUT = ROOT / f"GPCO403_theory_reference_{VERSION}_notes.md"
ASSET_DIR = ROOT / "assets" / f"gpco403_theory_reference_{VERSION}"

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
ACCENT_GOLD = colors.HexColor("#C69C3F")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
WARM_AMBER = colors.HexColor("#FFF5E6")
TEXT = colors.HexColor("#202020")
GREEN = colors.HexColor("#1F6F5B")


def ascii_text(text):
    text = str(text)
    replacements = {
        "\u2014": " - ",
        "\u2013": " - ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2212": "-",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2192": "->",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).strip()


def strip_tags(text):
    text = re.sub(r"<sub>(.*?)</sub>", r"\1", str(text))
    text = re.sub(r"<super>(.*?)</super>", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return ascii_text(text)


def para(text, style):
    return Paragraph(escape(ascii_text(text)).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>"), style)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "_", ascii_text(text).lower()).strip("_")


def short_items(items, n):
    return list(items[:n])


POST_MIDTERM_THEORIES = [
    {
        "session": "Week 6",
        "title": "Ricardian Comparative Advantage",
        "source": "International Economics, Ch. 2; The Economist, The Miracle of Trade; Ricardian practice problems",
        "author": "Robert C. Feenstra and Alan M. Taylor; The Economist; Kyle Handley",
        "situation": "A country should export the good it produces at the lower opportunity cost, even if another country has absolute advantage in every good.",
        "intuition": "The Ricardian model explains trade through technology and productivity differences. The key result is not that the most productive country exports everything, but that each country specializes where its opportunity cost is lowest. Trade changes relative prices so countries can consume beyond their autarky production possibility frontier. The practical exam move is to convert productivity into opportunity cost before making any export prediction.",
        "concepts": [
            ("Absolute advantage", "Higher productivity in producing a good. It is not sufficient for predicting trade patterns."),
            ("Comparative advantage", "Lower opportunity cost of producing a good. This determines specialization and exports."),
            ("Opportunity cost", "The amount of one good sacrificed to produce another. In Ricardian questions, calculate it before interpreting the table."),
            ("No-trade relative price", "The domestic opportunity cost before trade. A country exports the good whose world relative price rises above its autarky price."),
            ("PPF", "The production possibility frontier. Ricardian PPFs are linear when labor is the only factor and unit labor requirements are fixed."),
            ("Gains from trade", "Consumption possibilities expand because specialization plus exchange beats autarky production alone."),
        ],
        "assumptions": [
            "Labor is the only factor of production.",
            "Technology differs across countries and goods.",
            "Labor is mobile across sectors domestically but not internationally.",
            "Markets are competitive and trade is frictionless.",
        ],
        "strengths": [
            "Shows why trade can benefit both countries even with absolute-advantage asymmetry.",
            "Gives a clean calculation framework for opportunity-cost exam problems.",
            "Explains specialization from relative productivity, not raw productivity.",
        ],
        "weaknesses": [
            "Ignores distributional conflict inside countries.",
            "Assumes away transport costs, multiple factors, and firm heterogeneity.",
            "Predicts complete specialization more often than real economies display.",
        ],
        "references": [
            "Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers.",
            "The Economist. (1996). The miracle of trade. The Economist.",
        ],
        "visual": {
            "kind": "ppf",
            "labels": ["Home CA", "Foreign CA", "World price"],
            "caption": "Mechanism: opportunity costs determine which good each country exports. Key assumption: labor productivity is fixed and labor moves within the country. Strength/limit cue: the model nails relative-cost logic but hides factor conflict and trade costs.",
        },
    },
    {
        "session": "Week 7",
        "title": "Heckscher-Ohlin Factor Endowments",
        "source": "International Economics, Ch. 4 and Ch. 17.1; Heckscher-Ohlin one-pager",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "A capital-abundant country exports capital-intensive goods, while a labor-abundant country exports labor-intensive goods.",
        "intuition": "Heckscher-Ohlin shifts the cause of trade from technology differences to factor endowment differences. Countries are relatively cheap in the factors they have in abundance, so goods using those factors intensively have lower autarky prices. Opening to trade raises the relative price of the abundant-factor-intensive export good and lowers the relative price of the scarce-factor-intensive import good.",
        "concepts": [
            ("Factor abundance", "A country has relatively more capital, labor, land, or skill than another country."),
            ("Factor intensity", "A good uses one factor relatively more than another good."),
            ("HO theorem", "Countries export goods intensive in their abundant factors and import goods intensive in scarce factors."),
            ("Autarky price", "The no-trade relative price that reveals comparative advantage."),
            ("Trade triangle", "The difference between production and consumption under trade, showing exports and imports."),
            ("Leontief paradox", "The empirical puzzle that U.S. exports appeared less capital-intensive than expected."),
        ],
        "assumptions": [
            "Countries share the same technologies.",
            "Factors cannot move internationally but move across sectors domestically.",
            "Goods differ in factor intensity.",
            "Preferences are similar enough that supply-side endowments drive trade.",
        ],
        "strengths": [
            "Explains trade patterns with factor abundance rather than technology alone.",
            "Connects trade to domestic factor prices and political conflict.",
            "Works well as a bridge from trade theory to distributional politics.",
        ],
        "weaknesses": [
            "Empirical fit is mixed without human capital, technology, and trade costs.",
            "Factor-intensity reversals can break the prediction.",
            "Simplified two-good, two-factor structure can be too clean for real economies.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "table",
            "labels": ["Abundance", "Intensity", "Export"],
            "caption": "Mechanism: match a country's abundant factor to the good that uses that factor intensively. Key assumption: countries have similar technology. Strength/limit cue: strong for distributional logic, weaker when technology and human capital differ.",
        },
    },
    {
        "session": "Week 7",
        "title": "Stolper-Samuelson Distributional Effects",
        "source": "International Economics, Ch. 4; Concept Check 4 prep",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "When the price of a capital-intensive export rises, capital owners gain in real terms and workers can lose.",
        "intuition": "Stolper-Samuelson is the distributional punchline of Heckscher-Ohlin. A rise in a good's relative price raises the real return to the factor used intensively in that good and lowers the real return to the other factor. Trade therefore does not simply create country-level gains; it rearranges income within the country and gives the losing factor an incentive to oppose liberalization.",
        "concepts": [
            ("Real factor return", "The purchasing power of wages or rents, not just the nominal payment."),
            ("Export-sector factor", "The factor used intensively in the rising-price sector."),
            ("Scarce factor", "The domestic factor used intensively in import-competing production; it tends to lose from trade."),
            ("Magnification effect", "Factor returns can change more than goods prices in the model."),
            ("Factor conflict", "Political conflict organized around labor, capital, land, or skill rather than around firms alone."),
        ],
        "assumptions": [
            "Two goods and two factors are used in competitive production.",
            "Factors are mobile across sectors domestically.",
            "Goods prices change because trade opens or policy changes.",
            "Technology and factor intensity are stable enough to identify the intensive factor.",
        ],
        "strengths": [
            "Explains why free trade can face domestic opposition despite national gains.",
            "Gives a precise exam rule for winners and losers.",
            "Connects trade prices to political economy.",
        ],
        "weaknesses": [
            "Short-run sector-specific factors may matter more than fully mobile factors.",
            "Does not by itself predict compensation or political institutions.",
            "Real economies include more than two factors and many worker types.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "flow",
            "labels": ["Price up", "Intensive factor gains", "Other factor loses"],
            "caption": "Mechanism: a goods-price change is transmitted into real factor returns. Key assumption: factors move across sectors. Strength/limit cue: powerful for winner-loser logic, but too long-run for sector-specific adjustment pain.",
        },
    },
    {
        "session": "Week 7",
        "title": "Factor Price Equalization and Its Limits",
        "source": "International Economics, Ch. 4; Heckscher-Ohlin practice questions",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "Trade in goods can partly substitute for factor mobility by pushing wages and returns toward convergence across countries.",
        "intuition": "The factor price equalization theorem says that if countries share technology, trade freely, and produce the same goods, trade equalizes goods prices and thereby equalizes factor prices. A labor-abundant country exporting labor-intensive goods raises wages; a capital-abundant country exporting capital-intensive goods raises rents. In practice, the theorem is more useful as a benchmark than a literal prediction because technology, institutions, trade costs, and specialization prevent full equalization.",
        "concepts": [
            ("Goods-price equalization", "Free trade makes the same good sell at the same price across countries under strong assumptions."),
            ("Factor-price equalization", "Equal goods prices imply equal wages and rental rates when technologies and produced goods are the same."),
            ("Integrated world equilibrium", "A benchmark where trading goods reproduces the allocation that would occur if factors could move freely."),
            ("Cone of diversification", "The range of factor endowments in which countries produce the same set of goods."),
            ("Wage convergence", "The partial tendency for trade to raise wages in labor-abundant countries and pressure wages in labor-scarce countries."),
        ],
        "assumptions": [
            "Identical technologies across countries.",
            "Both countries produce both goods after trade.",
            "No trade costs, tariffs, or institutional wedges.",
            "Factors are homogeneous and perfectly mobile between domestic sectors.",
        ],
        "strengths": [
            "Shows why goods trade can affect wages even without migration.",
            "Clarifies the link between HO trade patterns and income distribution.",
            "Provides a sharp benchmark for globalization debates.",
        ],
        "weaknesses": [
            "Full equalization rarely appears empirically.",
            "Technology, human capital, and institutions differ substantially.",
            "Complete specialization and trade costs break the result.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "convergence",
            "labels": ["Goods prices", "Wages", "Rents"],
            "caption": "Mechanism: goods-price convergence transmits into factor-price convergence. Key assumption: countries use the same technologies and produce the same goods. Strength/limit cue: clarifies wage pressure, but real-world wedges block full equalization.",
        },
    },
    {
        "session": "Week 8",
        "title": "Increasing Returns and Monopolistic Competition",
        "source": "International Economics, Ch. 6; firms and increasing returns one-pager",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "Two similar rich countries can trade cars for cars because consumers value varieties and firms lower average cost by serving a larger market.",
        "intuition": "Increasing-returns trade theory explains trade that does not depend on countries being very different. With fixed costs and product differentiation, larger markets allow firms to spread fixed costs over more output, lower average cost, and offer more varieties. Monopolistic competition gives firms some pricing power over differentiated products while entry keeps profits disciplined.",
        "concepts": [
            ("Increasing returns to scale", "Output rises more than proportionally as inputs expand."),
            ("Economies of scale", "Average costs fall as production scale increases."),
            ("Monopolistic competition", "Many firms sell differentiated products and face downward-sloping demand."),
            ("Product variety", "Consumers gain because trade expands the menu of differentiated goods."),
            ("Intra-industry trade", "Countries simultaneously import and export varieties within the same industry."),
            ("Love of variety", "Consumer welfare rises when more differentiated products are available."),
        ],
        "assumptions": [
            "Firms face fixed costs and downward-sloping demand.",
            "Products are differentiated but substitutable.",
            "Entry and competition limit pure profits.",
            "Consumers value variety and lower prices.",
        ],
        "strengths": [
            "Explains trade among similar countries.",
            "Adds scale and variety gains missing from Ricardian and HO models.",
            "Fits modern manufacturing and consumer-goods trade.",
        ],
        "weaknesses": [
            "Can understate distributional losses from firm exit.",
            "Model outcomes depend on market structure assumptions.",
            "Variety gains are harder to see in simple tariff accounting.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "scale",
            "labels": ["Bigger market", "Lower AC", "More varieties"],
            "caption": "Mechanism: market integration lets firms spread fixed costs and consumers access more varieties. Key assumption: differentiated products and scale economies matter. Strength/limit cue: explains rich-country intra-industry trade but needs firm-level selection for exporter patterns.",
        },
    },
    {
        "session": "Week 8",
        "title": "Firm Heterogeneity and Export Selection",
        "source": "International Economics, Ch. 6; firms and increasing returns class prep",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "Only the most productive firms export because they can cover the fixed costs of foreign-market entry.",
        "intuition": "Firm-level trade theory adds productivity differences across firms. Exporting requires fixed costs for distribution, compliance, marketing, and adaptation, so low-productivity firms serve only the domestic market or exit, while high-productivity firms profitably export. Trade reallocates market share toward more productive firms and raises average industry productivity even if individual firms do not all become more efficient.",
        "concepts": [
            ("Firm heterogeneity", "Firms in the same industry differ in productivity and costs."),
            ("Fixed export cost", "Up-front cost of entering foreign markets."),
            ("Selection effect", "Only firms above a productivity cutoff export."),
            ("Reallocation effect", "Market share shifts toward more productive firms after trade opens."),
            ("Exporter premium", "Exporters tend to be larger, more productive, and more capital or skill intensive."),
        ],
        "assumptions": [
            "Firms differ in productivity before exporting.",
            "Foreign-market entry requires fixed costs.",
            "Consumers can switch across varieties when prices and availability change.",
            "Less productive firms cannot fully avoid competitive pressure.",
        ],
        "strengths": [
            "Explains why exporters are a special subset of firms.",
            "Captures productivity gains from reallocation.",
            "Matches modern evidence on firm-level trade participation.",
        ],
        "weaknesses": [
            "Firm exit can impose local labor-market costs.",
            "Fixed costs and productivity are hard to measure directly.",
            "The model can treat adjustment as cleaner than it is politically.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "cutoff",
            "labels": ["Exit", "Home only", "Export"],
            "caption": "Mechanism: productivity cutoffs sort firms into exit, domestic-only, and exporting groups. Key assumption: exporting has fixed costs. Strength/limit cue: strong for firm-level data, but local adjustment losses remain outside the clean cutoff.",
        },
    },
    {
        "session": "Week 9",
        "title": "Small-Country Tariff Welfare",
        "source": "International Economics, Ch. 8; Week 9 trade policy prep",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "A small importer that cannot affect the world price loses from a tariff because consumers lose more than producers and the government gain.",
        "intuition": "In the small-country model, the world price is fixed. A tariff raises the domestic price by the tariff amount, causing consumers to buy less, domestic producers to produce more, and imports to fall. Consumer surplus falls by areas a+b+c+d; producer surplus rises by a; government revenue rises by c; the net national loss is the production and consumption deadweight loss, b+d.",
        "concepts": [
            ("Small country", "An importer too small to affect the world price."),
            ("Specific tariff", "A per-unit tax on imports."),
            ("Consumer surplus loss", "Consumers pay more and consume less after the tariff."),
            ("Producer surplus gain", "Domestic producers gain from the higher protected price."),
            ("Government revenue", "Tariff rate times post-tariff import quantity."),
            ("Deadweight loss", "Production distortion plus consumption distortion."),
        ],
        "assumptions": [
            "The country takes the world price as given.",
            "Markets are perfectly competitive.",
            "Supply and demand curves capture marginal cost and willingness to pay.",
            "No retaliation or market-power effects occur.",
        ],
        "strengths": [
            "Cleanest welfare accounting diagram for import policy.",
            "Separates transfers from efficiency losses.",
            "High-yield calculation framework for concept checks and exams.",
        ],
        "weaknesses": [
            "Ignores terms-of-trade effects for large countries.",
            "Static partial equilibrium omits supply chains and retaliation.",
            "Distributional and political benefits may motivate tariffs despite welfare loss.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "tariff",
            "labels": ["CS loss", "PS gain", "Gov rev", "DWL"],
            "caption": "Mechanism: the tariff raises the domestic price while the world price stays fixed. Key assumption: the importer is too small to move the world price. Strength/limit cue: excellent welfare accounting, but too static for supply-chain shocks.",
        },
    },
    {
        "session": "Week 9",
        "title": "Large-Country Tariff and Optimal Tariff Logic",
        "source": "International Economics, Ch. 8; Week 9 trade policy prep",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "A large importer may force foreign exporters to lower pre-tariff prices, creating a terms-of-trade gain that can offset deadweight loss.",
        "intuition": "A large country faces an upward-sloping foreign export supply curve. When it imposes a tariff, import demand falls enough to push down the foreign export price, so foreigners absorb part of the tax. Home gains a terms-of-trade rectangle e, but still suffers production and consumption distortions b+d. National welfare rises only if e exceeds b+d. The optimal tariff is a unilateral market-power result, not a cooperative policy recommendation, because retaliation can make everyone worse off.",
        "concepts": [
            ("Large country", "An importer with enough market power to affect the world price."),
            ("Terms-of-trade gain", "Home pays a lower pre-tariff price to foreign exporters."),
            ("Pass-through", "How much of the tariff shows up in domestic prices."),
            ("Optimal tariff", "The tariff rate that maximizes national welfare absent retaliation."),
            ("Retaliation", "Trading partners impose counter-tariffs, erasing gains and adding losses."),
        ],
        "assumptions": [
            "Foreign export supply is less than perfectly elastic.",
            "Home can exploit market power without immediate retaliation.",
            "Partial-equilibrium supply and demand capture the relevant market.",
            "Government values national welfare rather than global welfare.",
        ],
        "strengths": [
            "Explains why big countries may be tempted by tariffs.",
            "Clarifies the source of possible tariff gains.",
            "Sets up the WTO cooperation problem.",
        ],
        "weaknesses": [
            "Retaliation can reverse the unilateral gain.",
            "Empirical pass-through may be complete, eliminating the terms-of-trade benefit.",
            "Global welfare falls even when national welfare rises.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "tariff",
            "labels": ["ToT gain", "DWL", "Retaliation"],
            "caption": "Mechanism: reduced import demand lowers the foreign export price, generating a terms-of-trade gain. Key assumption: foreign export supply is not perfectly elastic. Strength/limit cue: explains unilateral temptation, but retaliation and pass-through can erase the gain.",
        },
    },
    {
        "session": "Week 9",
        "title": "Import Quotas and Voluntary Export Restraints",
        "source": "International Economics, Ch. 8; Week 9 trade policy prep",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "A quota can produce the same domestic price as a tariff, but welfare depends on who captures the quota rent.",
        "intuition": "A quota restricts import quantity directly. Under perfect competition, a quota set at the tariff-equivalent import level raises the domestic price and creates the same consumption and production distortions as a tariff. The key difference is the rent. If the government auctions licenses, it captures the rent like tariff revenue. If domestic firms receive licenses, rent-seeking may waste it. If foreign exporters capture the rent through a voluntary export restraint, the importing country loses the rent to foreigners.",
        "concepts": [
            ("Quota", "A direct quantity limit on imports."),
            ("Quota rent", "The value created by the gap between domestic and world price under restricted imports."),
            ("License auction", "Government sells import rights and captures rents."),
            ("Rent-seeking", "Resources wasted lobbying or competing for quota licenses."),
            ("VER", "A voluntary export restraint where foreign exporters limit shipments and often capture rents."),
        ],
        "assumptions": [
            "Quota quantity is binding.",
            "Markets are competitive unless rent allocation changes incentives.",
            "The quota is enforceable.",
            "Domestic and foreign actors can capture rents depending on license design.",
        ],
        "strengths": [
            "Shows why equivalent prices do not imply equivalent welfare.",
            "Highlights rent allocation and political economy.",
            "Useful for comparing tariffs, quotas, and VERs.",
        ],
        "weaknesses": [
            "Administration and evasion can complicate the clean diagram.",
            "Quality upgrading under quotas can change outcomes.",
            "Rent-seeking losses are hard to measure precisely.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "flow",
            "labels": ["Quota cap", "Price rises", "Rent owner?"],
            "caption": "Mechanism: quantity restriction creates scarcity rents. Key assumption: the quota binds. Strength/limit cue: reveals rent allocation, but administrative details decide who actually gains.",
        },
    },
    {
        "session": "Week 9",
        "title": "GATT/WTO Cooperation, MFN, and National Treatment",
        "source": "International Economics, Ch. 11.1-11.2; Week 9 trade policy prep",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "Countries bind tariffs and promise non-discrimination to escape a tariff retaliation game.",
        "intuition": "The WTO/GATT system addresses the cooperation problem created by unilateral tariff incentives. Large countries may prefer tariffs individually, but if each retaliates, all lose through high barriers and deadweight loss. MFN prevents discrimination across trading partners, and national treatment prevents countries from replacing border barriers with discriminatory internal taxes or regulations after importation.",
        "concepts": [
            ("GATT/WTO", "The institutional framework for negotiated tariff reductions and trade rules."),
            ("MFN", "Most-favored-nation treatment: a concession to one member must generally be extended to all members."),
            ("National treatment", "Imported goods must be treated no less favorably than like domestic goods after entry."),
            ("Bound tariff", "A legal ceiling on tariffs under WTO commitments."),
            ("Dispute settlement", "Institutional process for challenging alleged rule violations."),
            ("Prisoner's dilemma", "Each country has unilateral tariff incentives, but mutual tariffs make all worse off."),
        ],
        "assumptions": [
            "Governments value credible commitments.",
            "Rules can reduce uncertainty and retaliation risk.",
            "Members can monitor and challenge violations.",
            "Non-discrimination is administratively meaningful for like products.",
        ],
        "strengths": [
            "Explains why trade agreements exist even when unilateral free trade could be efficient.",
            "Gives precise legal-economic vocabulary for policy scenarios.",
            "Connects tariff theory to institutions.",
        ],
        "weaknesses": [
            "Rules can be slow or politically constrained.",
            "Exceptions and PTAs complicate non-discrimination.",
            "National-security and industrial-policy disputes strain the framework.",
        ],
        "references": ["Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers."],
        "visual": {
            "kind": "game",
            "labels": ["Cooperate", "Defect", "Retaliate"],
            "caption": "Mechanism: agreements help states escape mutually damaging tariff retaliation. Key assumption: commitments and enforcement are credible enough to shape behavior. Strength/limit cue: strong institutional logic, but exceptions and geopolitics weaken compliance.",
        },
    },
    {
        "session": "Week 9",
        "title": "Preferential Trade Agreements, Trade Creation, and Trade Diversion",
        "source": "International Economics, Ch. 11.2; Week 9 trade policy prep; Viner's PTA framework",
        "author": "Robert C. Feenstra and Alan M. Taylor; Jacob Viner; Kyle Handley; Plutus",
        "situation": "A free trade agreement can improve welfare by replacing costly domestic production, or reduce welfare by diverting imports from the world's lowest-cost supplier.",
        "intuition": "Preferential trade agreements are exceptions to MFN because members give each other lower tariffs than outsiders receive. Viner's key distinction is trade creation versus trade diversion. Trade creation is efficiency-enhancing: a partner replaces high-cost domestic production. Trade diversion is ambiguous or harmful: a higher-cost partner replaces a lower-cost non-member because the partner gets tariff-free access while the efficient outsider still pays the tariff.",
        "concepts": [
            ("PTA", "A preferential trade agreement that lowers barriers among members."),
            ("FTA", "A free trade area with internal free trade and separate external tariffs."),
            ("Customs union", "Internal free trade plus a common external tariff."),
            ("Rules of origin", "Requirements proving goods qualify for FTA preferences."),
            ("Trade creation", "Partner imports replace high-cost domestic production."),
            ("Trade diversion", "Partner imports replace lower-cost non-member imports because of tariff preferences."),
        ],
        "assumptions": [
            "Partner and non-member costs can be compared clearly.",
            "Tariff preferences change sourcing decisions.",
            "Rules of origin can prevent trade deflection in FTAs.",
            "Lost tariff revenue matters for national welfare.",
        ],
        "strengths": [
            "Gives a clean welfare test for regional agreements.",
            "Explains why PTAs are not automatically liberalizing in welfare terms.",
            "Useful for Data Brief 2 trade-agreement analysis.",
        ],
        "weaknesses": [
            "Dynamic gains, supply chains, and politics may alter the static verdict.",
            "Rules of origin can become hidden protectionism.",
            "Trade diversion is empirically case-specific.",
        ],
        "references": [
            "Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers.",
            "Viner, J. (1950). The customs union issue. Carnegie Endowment for International Peace.",
        ],
        "visual": {
            "kind": "table",
            "labels": ["Home", "Partner", "Non-member"],
            "caption": "Mechanism: tariff preferences can shift sourcing toward or away from efficiency. Key assumption: tariff-inclusive prices determine sourcing. Strength/limit cue: excellent static welfare screen, but dynamic integration effects may complicate the answer.",
        },
    },
    {
        "session": "Week 9",
        "title": "2018 Tariffs, Pass-Through, and Welfare Evidence",
        "source": "Amiti, Redding, and Weinstein, The Impact of the 2018 Tariffs on Prices and Welfare; Week 9 prep",
        "author": "Mary Amiti, Stephen J. Redding, and David E. Weinstein; Plutus",
        "situation": "The 2018 U.S. tariffs largely passed through into U.S. prices, so U.S. consumers and firms bore the burden instead of foreign exporters.",
        "intuition": "Amiti, Redding, and Weinstein test the large-country tariff logic empirically. Standard theory allowed for foreign exporters to absorb part of the tariff through lower pre-tariff prices, but the paper finds near-complete pass-through into U.S. import prices. The result implies little terms-of-trade gain for the United States and substantial costs to U.S. buyers, including monthly tax costs, deadweight losses, trade redirection, and higher input costs for manufacturers.",
        "concepts": [
            ("Pass-through", "The share of a tariff reflected in domestic import prices."),
            ("Incidence", "Who actually bears the burden of the tariff."),
            ("Trade redirection", "Imports or exports shift away from tariffed partners toward untariffed partners."),
            ("Deadweight loss", "Efficiency loss not captured by government revenue or producer surplus."),
            ("Input-cost channel", "Tariffs on intermediate goods raise costs for downstream domestic firms."),
            ("Complete pass-through", "Foreign export prices do not fall enough to absorb the tariff."),
        ],
        "assumptions": [
            "Price and trade data identify tariff effects relative to unaffected categories.",
            "Short-run supply chains and product differentiation limit substitution.",
            "Domestic buyers cannot quickly force foreign exporters to cut prices.",
            "Measured price changes capture the relevant incidence channel.",
        ],
        "strengths": [
            "Calibrates theory with real 2018 U.S. tariff evidence.",
            "Shows why large-country market power may fail in practice.",
            "Links tariffs to supply chains, consumer costs, and welfare loss.",
        ],
        "weaknesses": [
            "Short-run estimates may differ from long-run adjustment.",
            "Distributional political benefits are outside the welfare accounting.",
            "Results are tied to the specific tariff episode and products studied.",
        ],
        "references": [
            "Amiti, M., Redding, S. J., & Weinstein, D. E. (2019). The impact of the 2018 tariffs on prices and welfare. Journal of Economic Perspectives, 33(4), 187-210.",
        ],
        "visual": {
            "kind": "flow",
            "labels": ["Tariff", "Pass-through", "U.S. buyers pay"],
            "caption": "Mechanism: tariffs raised domestic import prices rather than lowering foreign export prices. Key assumption: supply chains and product specificity limit substitution. Strength/limit cue: strong empirical correction to large-country theory, but short-run evidence may not equal all long-run effects.",
        },
    },
]


DEFAULT_REFS = [
    "Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers.",
    "Handley, K. (2026). GPCO 403 International Economics lecture slides and course materials. UC San Diego School of Global Policy and Strategy.",
]

SPECIAL_REFS = {
    "Big Mac Index as Applied PPP": [
        "The Economist. (n.d.). The Big Mac index. The Economist.",
        "Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers.",
    ],
    "Exchange-Rate Regimes and Crisis Balance Sheets": [
        "Restrepo-Echavarria, P., & Grittayaphong, P. (2021, August 3). Dollar-denominated public debt in Asia and Latin America. Federal Reserve Bank of St. Louis.",
        "Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers.",
    ],
}

MIDTERM_VISUALS = {
    "National Income Accounting and Open-Economy GDP": {
        "kind": "flow",
        "labels": ["Production", "Income", "Spending"],
        "caption": "Mechanism: open-economy accounts separate what is produced, what residents earn, and what residents spend. Key assumption: final goods and cross-border income flows are measured consistently. Strength/limit cue: excellent for stopping category errors, but accounting identities do not prove causation.",
    },
    "Current Account and Balance of Payments Identity": {
        "kind": "flow",
        "labels": ["CA deficit", "FA surplus", "Claims created"],
        "caption": "Mechanism: double-entry accounting means a current-account deficit is matched by financial claims or reserve changes. Key assumption: transactions are classified consistently. Strength/limit cue: powerful ledger logic, but sustainability depends on the composition of liabilities.",
    },
    "Savings-Investment Gap and Twin Deficits": {
        "kind": "table",
        "labels": ["Saving", "Investment", "Current acct"],
        "caption": "Mechanism: CA = S - I, so investment above national saving requires foreign financing. Key assumption: the identity is measured over the same period. Strength/limit cue: clarifies fiscal links, but private saving and investment responses decide causality.",
    },
    "External Wealth and Valuation Effects": {
        "kind": "flow",
        "labels": ["Asset stock", "CA flow", "Valuation"],
        "caption": "Mechanism: net foreign assets change through current-account flows and asset-price or exchange-rate valuation effects. Key assumption: external positions can be valued accurately. Strength/limit cue: explains balance-sheet surprises, but valuation gains can reverse.",
    },
    "Intertemporal Trade and Consumption Smoothing": {
        "kind": "flow",
        "labels": ["Shock today", "Borrow/lend", "Repay later"],
        "caption": "Mechanism: countries trade present resources for future resources to smooth consumption or fund investment. Key assumption: future income can service debt. Strength/limit cue: useful for temporary shocks, dangerous for permanent income losses.",
    },
    "Exchange-Rate Basics and Cross-Rate Arbitrage": {
        "kind": "flow",
        "labels": ["Quote units", "Cross rate", "Arbitrage"],
        "caption": "Mechanism: currency prices must be internally consistent after unit conversion. Key assumption: transaction costs and spreads do not absorb the gap. Strength/limit cue: excellent no-arbitrage discipline, but not a full theory of exchange-rate movements.",
    },
    "Interest Parity and Forward Exchange Rates": {
        "kind": "flow",
        "labels": ["Spot convert", "Earn interest", "Forward cover"],
        "caption": "Mechanism: parity compares home and foreign returns after currency conversion and expected or contracted future exchange rates. Key assumption: comparable assets and mobile capital. Strength/limit cue: CIP is a strong benchmark; UIP often fails because risk premia and expectations matter.",
    },
    "Exchange-Rate Regimes and Crisis Balance Sheets": {
        "kind": "table",
        "labels": ["Regime", "FX move", "Balance sheet"],
        "caption": "Mechanism: pegs, floats, and managed regimes determine where exchange-rate pressure appears, while currency mismatch transmits depreciation into solvency risk. Key assumption: liabilities and revenues differ by currency. Strength/limit cue: strong for crisis vulnerability, weaker for timing triggers.",
    },
    "Law of One Price": {
        "kind": "flow",
        "labels": ["Cheap market", "Arbitrage", "One price"],
        "caption": "Mechanism: identical tradable goods should have equal common-currency prices when arbitrage is frictionless. Key assumption: goods are identical and resale is possible. Strength/limit cue: clean benchmark, but trade costs and segmentation create persistent wedges.",
    },
    "Purchasing Power Parity and the Real Exchange Rate": {
        "kind": "convergence",
        "labels": ["Inflation", "Exchange rate", "Real price"],
        "caption": "Mechanism: PPP links inflation differentials to exchange-rate adjustment and the real exchange rate. Key assumption: comparable baskets and long-run goods-market adjustment. Strength/limit cue: useful anchor, poor short-run forecast.",
    },
    "Big Mac Index as Applied PPP": {
        "kind": "table",
        "labels": ["Local price", "Dollar price", "Mispricing"],
        "caption": "Mechanism: a single standardized product creates an implied PPP exchange rate. Key assumption: Big Macs are comparable across countries. Strength/limit cue: memorable applied PPP, but nontraded inputs and local pricing limit precision.",
    },
}


def normalize_theory(t):
    theory = deepcopy(t)
    theory.setdefault("references", SPECIAL_REFS.get(theory["title"], DEFAULT_REFS))
    theory.setdefault("visual", MIDTERM_VISUALS.get(theory["title"], {
        "kind": "flow",
        "labels": ["Shock", "Mechanism", "Outcome"],
        "caption": "Mechanism: the diagram reduces the theory to its main causal path. Key assumption: the model's simplifying conditions hold closely enough. Strength/limit cue: useful as a fast benchmark, but application requires checking violated assumptions.",
    }))
    theory["anchor"] = slugify(theory["title"])
    theory["asset"] = ASSET_DIR / f"{theory['anchor']}.png"
    return theory


THEORIES = [normalize_theory(t) for t in MIDTERM_THEORIES] + [normalize_theory(t) for t in POST_MIDTERM_THEORIES]


styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=DARK_NAVY, alignment=TA_CENTER))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=9, leading=11, alignment=TA_CENTER, textColor=TEXT))
styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=7.3, leading=8.5, textColor=TEXT))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=8.1, leading=9.4, textColor=TEXT))
styles.add(ParagraphStyle("BodySmall", parent=styles["Normal"], fontSize=7.2, leading=8.25, textColor=TEXT))
styles.add(ParagraphStyle("Section", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=9.1, leading=10, textColor=DARK_NAVY, spaceAfter=1.5))
styles.add(ParagraphStyle("TOC", parent=styles["Normal"], fontSize=7.8, leading=8.9, textColor=MED_BLUE))
styles.add(ParagraphStyle("HeaderWhite", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12, leading=13.5, textColor=colors.white))
styles.add(ParagraphStyle("HeaderSmall", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=7.5, leading=8.4, textColor=colors.HexColor("#E8EEF8")))
styles.add(ParagraphStyle("Caption", parent=styles["Normal"], fontSize=7.8, leading=8.8, textColor=colors.HexColor("#444444")))
styles.add(ParagraphStyle("Ref", parent=styles["Normal"], fontSize=6.8, leading=7.8, leftIndent=12, firstLineIndent=-12, textColor=TEXT))


def wrap(draw, text, width, font, max_lines=None):
    words = ascii_text(text).split()
    lines = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".") + "..."
    return lines


def load_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_arrow(draw, start, end, fill, width=4):
    draw.line([start, end], fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    if x2 >= x1:
        pts = [(x2, y2), (x2 - 15, y2 - 8), (x2 - 15, y2 + 8)]
    else:
        pts = [(x2, y2), (x2 + 15, y2 - 8), (x2 + 15, y2 + 8)]
    draw.polygon(pts, fill=fill)


def make_visual(theory):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = theory["asset"]
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), "#F7F7F7")
    draw = ImageDraw.Draw(img)
    title_font = load_font(42, True)
    label_font = load_font(31, True)
    body_font = load_font(26)
    small_font = load_font(22)
    navy = "#1B2A4A"
    blue = "#2C5282"
    gold = "#C69C3F"
    amber = "#FFF5E6"
    green = "#1F6F5B"
    draw.rectangle([0, 0, W, 90], fill=navy)
    draw.text((40, 22), ascii_text(theory["title"])[:70], fill="white", font=title_font)
    labels = theory["visual"].get("labels", ["Shock", "Mechanism", "Outcome"])[:3]
    kind = theory["visual"].get("kind", "flow")

    if kind == "ppf":
        x0, y0, x1, y1 = 170, 820, 720, 220
        draw.line([x0, y0, x1, y0], fill=navy, width=5)
        draw.line([x0, y0, x0, y1], fill=navy, width=5)
        draw.line([x0, y0, x1 - 40, y1 + 40], fill=blue, width=7)
        draw.line([x0, y0 - 70, x1 - 90, y1 + 20], fill=green, width=7)
        draw.line([260, 720, 610, 405], fill=gold, width=5)
        draw.text((130, 850), "Good X", fill=navy, font=body_font)
        draw.text((70, 190), "Good Y", fill=navy, font=body_font)
        draw.text((760, 305), labels[0], fill=blue, font=label_font)
        draw.text((760, 390), labels[1], fill=green, font=label_font)
        draw.text((760, 475), labels[2], fill=gold, font=label_font)
    elif kind == "tariff":
        x0, y0, x1, y1 = 150, 810, 870, 210
        draw.line([x0, y0, x1, y0], fill=navy, width=5)
        draw.line([x0, y0, x0, y1], fill=navy, width=5)
        draw.line([220, 760, 820, 260], fill=blue, width=6)
        draw.line([220, 260, 820, 760], fill=green, width=6)
        draw.line([180, 560, 850, 560], fill=gold, width=5)
        draw.line([180, 455, 850, 455], fill="#AA3333", width=5)
        draw.rectangle([440, 455, 635, 560], outline=navy, width=4, fill=amber)
        draw.text((900, 250), labels[0], fill=blue, font=label_font)
        draw.text((900, 345), labels[1], fill=green, font=label_font)
        draw.text((900, 440), labels[2], fill="#AA3333", font=label_font)
        draw.text((185, 830), "Quantity", fill=navy, font=body_font)
        draw.text((80, 190), "Price", fill=navy, font=body_font)
    elif kind == "table":
        left, top = 160, 210
        cell_w, cell_h = 410, 135
        for r in range(4):
            for c in range(3):
                fill = navy if r == 0 else ("#FFFFFF" if r % 2 else "#EBF4FF")
                draw.rectangle([left + c * cell_w, top + r * cell_h, left + (c + 1) * cell_w, top + (r + 1) * cell_h], fill=fill, outline=navy, width=3)
                txt = labels[c] if r == 0 else [["Capital-rich", "Capital-good", "Capital-good"], ["Labor-rich", "Labor-good", "Labor-good"], ["Partner?", "Efficient?", "Welfare?"]][r - 1][c]
                draw.text((left + c * cell_w + 18, top + r * cell_h + 45), txt, fill=("white" if r == 0 else navy), font=label_font if r == 0 else body_font)
    elif kind == "scale":
        x0, y0, x1, y1 = 170, 790, 760, 230
        draw.line([x0, y0, x1, y0], fill=navy, width=5)
        draw.line([x0, y0, x0, y1], fill=navy, width=5)
        pts = [(190, 300), (320, 410), (480, 540), (710, 665)]
        draw.line(pts, fill=blue, width=8)
        for p in pts:
            draw.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=blue)
        draw.text((90, 190), "Average cost", fill=navy, font=body_font)
        draw.text((185, 815), "Output / market size", fill=navy, font=body_font)
        for i, label in enumerate(labels):
            draw.rounded_rectangle([870, 250 + i * 150, 1370, 335 + i * 150], radius=18, fill="#FFFFFF", outline=navy, width=3)
            draw.text((895, 272 + i * 150), label, fill=navy, font=label_font)
    elif kind == "cutoff":
        y = 540
        draw.line([190, y, 1330, y], fill=navy, width=7)
        for x, label, col in [(430, labels[0], "#AA3333"), (760, labels[1], gold), (1090, labels[2], green)]:
            draw.line([x, y - 90, x, y + 90], fill=col, width=7)
            draw.text((x - 120, y + 125), label, fill=col, font=label_font)
        draw.text((170, y - 150), "Low productivity", fill=navy, font=body_font)
        draw.text((1090, y - 150), "High productivity", fill=navy, font=body_font)
    elif kind == "game":
        boxes = [(220, 250, "Low tariffs"), (920, 250, "Tariff temptation"), (570, 620, "WTO commitment")]
        for x, y, text in boxes:
            draw.rounded_rectangle([x, y, x + 360, y + 105], radius=18, fill="#FFFFFF", outline=navy, width=4)
            draw.text((x + 30, y + 34), text, fill=navy, font=label_font)
        draw_arrow(draw, (580, 305), (920, 305), gold, 5)
        draw_arrow(draw, (920, 365), (760, 620), "#AA3333", 5)
        draw_arrow(draw, (570, 675), (400, 355), green, 5)
    elif kind == "convergence":
        x0, y0, x1, y1 = 180, 800, 1320, 220
        draw.line([x0, y0, x1, y0], fill=navy, width=5)
        draw.line([x0, y0, x0, y1], fill=navy, width=5)
        draw.line([230, 300, 1220, 500], fill=blue, width=7)
        draw.line([230, 720, 1220, 520], fill=green, width=7)
        draw.rectangle([1125, 455, 1280, 565], outline=gold, width=5)
        draw.text((1010, 610), "Convergence zone", fill=gold, font=label_font)
    else:
        x_positions = [180, 620, 1060]
        colors_ = [blue, gold, green]
        for i, label in enumerate(labels):
            x = x_positions[i]
            draw.rounded_rectangle([x, 345, x + 320, 505], radius=22, fill="#FFFFFF", outline=colors_[i], width=5)
            for j, line in enumerate(wrap(draw, label, 260, label_font, 2)):
                draw.text((x + 35, 388 + j * 36), line, fill=colors_[i], font=label_font)
            if i < 2:
                draw_arrow(draw, (x + 335, 425), (x_positions[i + 1] - 25, 425), navy, 6)

    caption = theory["visual"].get("caption", "")
    y = 900
    draw.rectangle([55, 875, W - 55, 965], fill="#FFFFFF", outline="#CCCCCC", width=2)
    for idx, line in enumerate(wrap(draw, caption, W - 140, small_font, 3)):
        draw.text((75, y + idx * 26), line, fill="#202020", font=small_font)
    img.save(path)


def draw_footer(c, page_num):
    w, _ = landscape(letter)
    c.setStrokeColor(BORDER_GREY)
    c.setLineWidth(0.4)
    c.line(0.45 * inch, 0.36 * inch, w - 0.45 * inch, 0.36 * inch)
    c.setFillColor(colors.HexColor("#666666"))
    c.setFont("Helvetica", 7)
    c.drawString(0.45 * inch, 0.22 * inch, TITLE)
    c.drawRightString(w - 0.45 * inch, 0.22 * inch, f"Page {page_num}")


def draw_paragraph(c, text, x, y, width, style):
    p = para(text, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def draw_bullets(c, items, x, y, width, style, max_items=None):
    for item in items[: max_items or len(items)]:
        if isinstance(item, tuple):
            text = f"<b>{item[0]}</b> - {item[1]}"
        else:
            text = f"- {item}"
        y = draw_paragraph(c, text, x, y, width, style) - 3
    return y


def section(c, title, x, y, width):
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, title)
    c.setStrokeColor(ACCENT_GOLD)
    c.line(x, y - 3, x + width, y - 3)
    return y - 8


def draw_header(c, theory, page_kind):
    w, h = landscape(letter)
    c.setFillColor(DARK_NAVY if not theory["session"].startswith("Week 9") else MED_BLUE)
    c.rect(0.4 * inch, h - 0.72 * inch, w - 0.8 * inch, 0.52 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.55 * inch, h - 0.42 * inch, f"{theory['session']} | {strip_tags(theory['title'])} | {page_kind}")
    c.setFont("Helvetica-Oblique", 7.6)
    c.drawString(0.55 * inch, h - 0.60 * inch, f"Source: {strip_tags(theory['source'])[:145]}")
    c.drawRightString(w - 0.55 * inch, h - 0.60 * inch, f"Author(s): {strip_tags(theory['author'])[:85]}")


def draw_cover(c):
    w, h = landscape(letter)
    c.setTitle(f"{TITLE} {VERSION}")
    y = h - 0.55 * inch
    y = draw_paragraph(c, TITLE, 0.7 * inch, y, w - 1.4 * inch, styles["CoverTitle"]) - 2
    y = draw_paragraph(c, f"{COURSE} | {INSTRUCTOR} | Spring 2026 | UC San Diego GPS", 0.7 * inch, y, w - 1.4 * inch, styles["CoverSub"]) - 8
    desc = (
        "This reference consolidates the GPCO 403 theory spine in syllabus order, beginning from the existing midterm theory reference and extending through Ricardian trade, Heckscher-Ohlin, firm-level trade, tariffs, WTO rules, preferential trade agreements, and the 2018 tariff evidence. "
        "Each theory receives a two-page unit: a text page for mechanism and exam use, followed by an analytical visual page with caption, unit references, and disclosure."
    )
    c.setFillColor(LIGHT_GREY)
    c.roundRect(0.75 * inch, y - 0.55 * inch, w - 1.5 * inch, 0.5 * inch, 6, fill=1, stroke=0)
    draw_paragraph(c, desc, 0.92 * inch, y - 0.12 * inch, w - 1.84 * inch, styles["Small"])
    y -= 0.75 * inch
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75 * inch, y, "Hyperlinked Table of Contents")
    y -= 0.16 * inch
    col_w = (w - 1.5 * inch - 0.25 * inch) / 2
    left_x = 0.75 * inch
    right_x = left_x + col_w + 0.25 * inch
    rows = (len(THEORIES) + 1) // 2
    for i, theory in enumerate(THEORIES):
        x = left_x if i < rows else right_x
        yy = y - (i if i < rows else i - rows) * 0.19 * inch
        label = f"{i + 1}. {theory['session']} - {strip_tags(theory['title'])}"
        p = Paragraph(f'<a href="#{theory["anchor"]}" color="#2C5282">{escape(label)}</a>', styles["TOC"])
        p.wrap(col_w, 20)
        p.drawOn(c, x, yy - 9)
    c.setStrokeColor(BORDER_GREY)
    c.line(0.75 * inch, 0.78 * inch, 3.7 * inch, 0.78 * inch)
    disclosure = (
        f"Generated with {MODEL} via the Claudia agent system. Course: GPCO 403, {INSTRUCTOR}, UC San Diego GPS. "
        "Always verify against official course materials and readings. This document is a study aid and does not substitute for careful reading of the assigned texts."
    )
    draw_paragraph(c, disclosure, 0.75 * inch, 0.68 * inch, w - 1.5 * inch, styles["Small"])
    draw_footer(c, 1)
    c.showPage()


def draw_text_page(c, theory, page_num):
    w, h = landscape(letter)
    c.bookmarkPage(theory["anchor"], fit="XYZ", left=0, top=h)
    c.addOutlineEntry(strip_tags(theory["title"]), theory["anchor"], level=0)
    draw_header(c, theory, "Theory")
    margin = 0.55 * inch
    gap = 0.28 * inch
    col_w = (w - 2 * margin - gap) / 2
    y_left = h - 0.92 * inch
    y_right = y_left
    y_left = section(c, "SITUATION", margin, y_left, col_w)
    y_left = draw_paragraph(c, theory["situation"], margin, y_left, col_w, styles["Body"]) - 7
    y_left = section(c, "CORE INTUITION", margin, y_left, col_w)
    y_left = draw_paragraph(c, strip_tags(theory["intuition"]), margin, y_left, col_w, styles["Body"]) - 7
    y_left = section(c, "ASSUMPTIONS", margin, y_left, col_w)
    y_left = draw_bullets(c, short_items(theory["assumptions"], 4), margin + 8, y_left, col_w - 8, styles["BodySmall"]) - 5
    y_left = section(c, "IMAGE MAP", margin, y_left, col_w)
    y_left = draw_paragraph(c, theory["visual"]["caption"], margin, y_left, col_w, styles["Caption"]) - 5

    x2 = margin + col_w + gap
    y_right = section(c, "KEY CONCEPTS / TERMINOLOGY", x2, y_right, col_w)
    y_right = draw_bullets(c, short_items(theory["concepts"], 7), x2 + 8, y_right, col_w - 8, styles["BodySmall"]) - 6
    half = (col_w - 0.18 * inch) / 2
    y_sw = y_right
    y_sw = section(c, "STRENGTHS", x2, y_sw, half)
    draw_bullets(c, short_items(theory["strengths"], 3), x2 + 8, y_sw, half - 8, styles["BodySmall"])
    y_ww = y_right
    y_ww = section(c, "WEAKNESSES", x2 + half + 0.18 * inch, y_ww, half)
    draw_bullets(c, short_items(theory["weaknesses"], 3), x2 + half + 0.18 * inch + 8, y_ww, half - 8, styles["BodySmall"])
    draw_footer(c, page_num)
    c.showPage()


def draw_visual_page(c, theory, page_num):
    w, h = landscape(letter)
    anchor = theory["anchor"] + "_visual"
    c.bookmarkPage(anchor, fit="XYZ", left=0, top=h)
    c.addOutlineEntry("Visual: " + strip_tags(theory["title"]), anchor, level=1)
    draw_header(c, theory, "Visual and References")
    margin = 0.55 * inch
    img_top = h - 0.92 * inch
    img_h = 4.25 * inch
    img_w = 6.8 * inch
    c.drawImage(ImageReader(str(theory["asset"])), margin, img_top - img_h, width=img_w, height=img_h, preserveAspectRatio=True, mask="auto")
    x2 = margin + img_w + 0.28 * inch
    box_w = w - x2 - margin
    y = img_top
    y = section(c, "CAPTION / FOOTNOTE", x2, y, box_w)
    y = draw_paragraph(c, theory["visual"]["caption"], x2, y, box_w, styles["Caption"]) - 10
    y = section(c, "APA REFERENCES", x2, y, box_w)
    for ref in theory["references"][:4]:
        y = draw_paragraph(c, ref, x2 + 8, y, box_w - 8, styles["Ref"]) - 3
    y = section(c, "UNIT DISCLOSURE", x2, y - 2, box_w)
    disclosure = (
        f"Generated for: Edgar Agunias | Date: {DATE} | Model: {MODEL} | "
        f"Sources: {strip_tags(theory['source'])}; course memory and study guides | Agent: Plutus"
    )
    draw_paragraph(c, disclosure, x2, y, box_w, styles["Small"])
    draw_footer(c, page_num)
    c.showPage()


def write_notes():
    lines = [
        f"# GPCO 403 Comprehensive Theory Reference {VERSION} Notes",
        "",
        "## Inventory",
        "",
        "Built from the visible midterm theory reference v1.4.2 and post-midterm study guides/readings in syllabus order.",
        "",
    ]
    for i, theory in enumerate(THEORIES, 1):
        lines.append(f"{i}. {theory['session']} - {theory['title']} - {theory['source']}")
    lines += [
        "",
        "## Source Status",
        "",
        "- Weeks 1-9 have assigned readings recorded in Plutus READINGS.md and syllabus_extracted.md.",
        "- Week 10 is listed in the local syllabus extraction as Trade Policy II / final roadmap with no new reading separately assigned.",
        "- No separate Weeks 10-11 reading files were present in the course folder at build time.",
        "",
        "## Output",
        "",
        f"- PDF: `{OUT.name}`",
        f"- Builder: `{Path(__file__).name}`",
        f"- Assets: `assets/{ASSET_DIR.name}/`",
        "",
        "## Verification Targets",
        "",
        f"- Expected page count: {1 + 2 * len(THEORIES)} pages.",
        f"- Expected theory units: {len(THEORIES)}.",
        "- Each theory has one PNG explainer asset and two PDF pages.",
        "- TOC entries and PDF sidebar bookmarks are generated.",
        "",
        "---",
        "Generated for: Edgar Agunias",
        f"Date: {DATE}",
        f"Model: {MODEL}",
        "Sources: GPCO 403 syllabus extraction, Plutus memory files, existing midterm theory reference builder/notes, and post-midterm study guides/readings",
        "Agent: Plutus",
        "---",
        "",
    ]
    NOTES_OUT.write_text("\n".join(lines), encoding="utf-8")


def build():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for theory in THEORIES:
        make_visual(theory)
    c = canvas.Canvas(str(OUT), pagesize=landscape(letter))
    draw_cover(c)
    page = 2
    for theory in THEORIES:
        draw_text_page(c, theory, page)
        page += 1
        draw_visual_page(c, theory, page)
        page += 1
    c.save()
    write_notes()
    print(f"Wrote {OUT}")
    print(f"Wrote {NOTES_OUT}")
    print(f"Theories: {len(THEORIES)} | Pages: {1 + 2 * len(THEORIES)} | Assets: {len(list(ASSET_DIR.glob('*.png')))}")


if __name__ == "__main__":
    build()
