from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = Path(__file__).resolve().parent / "GPCO 403_Midterm_Theory_Reference_v1.3.0.pdf"
TITLE = "GPCO 403 Midterm Theory Reference"
DATE = "2026-04-29"
MODEL = "GPT-5.5 (medium reasoning)"

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
ACCENT_GOLD = colors.HexColor("#C69C3F")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
WARM_AMBER = colors.HexColor("#FFF5E6")
TEXT = colors.HexColor("#202020")
OVERFLOW_LOG = []


def clean(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace(" -- ", " - ")
    return text


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


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=DARK_NAVY, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=9, leading=11, alignment=TA_CENTER, textColor=TEXT, spaceAfter=6))
styles.add(ParagraphStyle("Desc", parent=styles["Normal"], fontSize=8.5, leading=10.5, textColor=TEXT))
styles.add(ParagraphStyle("TOC", parent=styles["Normal"], fontSize=8.4, leading=10.2, leftIndent=0, spaceAfter=1, textColor=MED_BLUE))
styles.add(ParagraphStyle("Foot", parent=styles["Normal"], fontSize=7, leading=8.2, textColor=colors.HexColor("#666666")))
styles.add(ParagraphStyle("HeaderWhite", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11.4, leading=13, textColor=colors.white))
styles.add(ParagraphStyle("HeaderSmall", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=7.2, leading=8.1, textColor=colors.HexColor("#E8EEF8")))
styles.add(ParagraphStyle("Section", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=7.85, leading=8.75, textColor=DARK_NAVY, spaceBefore=1.8, spaceAfter=0.9))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=6.25, leading=7.08, textColor=TEXT, spaceAfter=1.0))
styles.add(ParagraphStyle("RefBullet", parent=styles["Normal"], fontSize=5.72, leading=6.42, leftIndent=8, firstLineIndent=-5, spaceAfter=0.45))
styles.add(ParagraphStyle("ExamApp", parent=styles["Normal"], fontSize=5.62, leading=6.35, leftIndent=8, firstLineIndent=-5, spaceAfter=0.4, textColor=TEXT))
styles.add(ParagraphStyle("ColumnHead", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=6.7, leading=7.5, textColor=DARK_NAVY, alignment=TA_CENTER))


THEORIES = [
    {
        "session": "Weeks 1-2",
        "title": "National Income Accounting and Open-Economy GDP",
        "source": "International Economics, Ch. 16, Sections 16.1-16.3; GPCO 403 Lectures 1-2",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "Use this when a politician claims a trade deficit means the country is poorer: the first move is to separate production, expenditure, income, and cross-border payments.",
        "intuition": "National accounting is the measurement language for international macro. <b>GDP</b> measures newly produced final goods and services on domestic soil; <b>GNDI</b> adds net foreign income and transfers received by residents; <b>GNE</b> measures spending by home residents. The core open-economy move is to stop treating production, income, and spending as the same object. Home can spend more than it produces by importing and borrowing, or produce more than it spends by exporting and lending. The identity is therefore not a moral claim about deficits; it is the accounting map that tells you which margin must be checked next.",
        "exam_applications": [
            "2021 short answer: in the GPS/car supply-chain example, domestically produced intermediates are not counted separately; GDP rises by the exported final car minus the imported tires, $20,000 - $400 = $19,600.",
            "2021 stale-bread example: extra wages alone do not raise GDP if unsold output generates no revenue; labor income rises but bakery profits fall by the same amount.",
        ],
        "concepts": [
            ("GDP", "Market value of final goods and services newly produced inside the country during a period. It is a production concept, not a direct measure of resident welfare or purchasing power."),
            ("GNE", "Gross national expenditure: C + I + G, or spending by home residents and government on consumption, investment, and purchases. In an open economy it can exceed GDP when imports and foreign borrowing fill the gap."),
            ("GNDI", "Gross national disposable income: income available to residents after adding net factor income from abroad and net transfers. This is closer to resident resources than GDP alone."),
            ("Net exports", "Exports minus imports. It is the goods-and-services component that connects domestic production to foreign demand and domestic expenditure to foreign supply."),
            ("Final goods", "Goods counted at the end-use stage so intermediate inputs are not counted repeatedly. This is why the value of flour is not counted again inside the value of bread."),
            ("Value added", "Firm output minus intermediate inputs. Adding value added across firms gives GDP from the production side without double-counting supply chains."),
            ("Open-economy identity", "GDP equals domestic expenditure plus net exports under the expenditure approach. Rearranging the identity shows where foreign transactions enter the national accounts."),
        ],
        "assumptions": [
            "Market prices can aggregate unlike goods into one measure.",
            "Final and intermediate goods can be separated cleanly.",
            "Domestic production and national ownership are analytically distinct.",
            "Accounting identities organize data; by themselves they do not prove causation.",
            "The time period, price basis, and currency units are consistent across GDP, expenditure, and trade data.",
        ],
        "strengths": [
            "Prevents category mistakes in trade-deficit arguments.",
            "Connects macro data to exchange-rate and current-account questions.",
            "Gives exam answers a clean starting identity before interpretation.",
            "Separates production-side stories from spending-side and income-side stories.",
        ],
        "weaknesses": [
            "GDP is not welfare, distribution, or sustainability.",
            "Market prices miss household production and some quality changes.",
            "Identities say what must add up, not why behavior changed.",
            "Aggregates can hide who gains, who loses, and whether foreign borrowing finances investment or consumption.",
        ],
    },
    {
        "session": "Week 2",
        "title": "Current Account and Balance of Payments Identity",
        "source": "International Economics, Ch. 12, Section 12.2 and Ch. 16, Sections 16.3-16.5; GPCO 403 Lecture 3",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "When the United States runs a current-account deficit, the balancing entry is a capital or financial-account surplus: foreigners are acquiring claims on U.S. assets.",
        "intuition": "The <b>current account</b> records net payments from trade, income, and transfers. The <b>balance of payments</b> is double-entry accounting: every international transaction has an offsetting entry, so current-account imbalances must be matched by capital/financial-account movements, reserve changes, or statistical discrepancy. A deficit is not simply money disappearing; it means home residents, firms, or the government are receiving goods/income now while foreigners receive financial claims or asset ownership. The exam intuition is: always ask what claim is created on the other side of the ledger.",
        "exam_applications": [
            "Practice BOP drill: an import is a CA debit, but the payment method creates the offsetting FA credit/debit; always write both sides before choosing an answer.",
            "2025 answer key: foreign countries investing in U.S. infrastructure is FDI and a positive financial-account entry, not a current-account transfer.",
            "2025 answer key: a direct payment to the U.S. Treasury with no asset/liability received is a positive unilateral transfer in the current account.",
        ],
        "concepts": [
            ("Current account", "CA = NX + NFIA + NUT: trade balance, net factor income from abroad, and net unilateral transfers. It records net payments associated with current production, income, and transfers."),
            ("Financial account", "Net acquisition of financial assets and liabilities across borders. It shows whether home residents are buying foreign assets or foreigners are buying home assets."),
            ("Capital account", "Usually small; records capital transfers and nonproduced nonfinancial assets."),
            ("Net lending/borrowing", "CA surplus means net lending to the world; CA deficit means net borrowing."),
            ("World CA sum", "Global current-account balances sum to zero, ignoring measurement error."),
            ("Double-entry accounting", "Each transaction creates a credit and debit, forcing the BOP to balance."),
            ("Statistical discrepancy", "The measured wedge that reconciles imperfect data. It is an accounting residual, not a theory of behavior."),
        ],
        "assumptions": [
            "Transactions are recorded consistently as credits/debits.",
            "The rest of the world is the counterpart for every cross-border transaction.",
            "Measurement error is recognized but not treated as economic substance.",
            "Official categories are meaningful enough to distinguish trade, income, transfers, reserves, and asset flows.",
        ],
        "strengths": [
            "Explains why CA deficits are financed rather than free-standing losses.",
            "Clarifies exam questions asking what must happen in FA/KA when CA changes.",
            "Links trade balances to capital flows and external wealth.",
            "Forces precise language: deficit in one account implies offsetting surplus elsewhere.",
        ],
        "weaknesses": [
            "Does not say whether a deficit is good or bad without context.",
            "Can hide composition: FDI, portfolio flows, reserves, and debt have different risks.",
            "Data revisions and statistical discrepancy can obscure the clean identity.",
            "The identity itself cannot distinguish sustainable borrowing from crisis-prone borrowing.",
        ],
    },
    {
        "session": "Week 2",
        "title": "Savings-Investment Gap and Twin Deficits",
        "source": "International Economics, Ch. 16, Section 16.4; GPCO 403 Lecture 3",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "If national saving falls below domestic investment, the country must borrow from abroad, so the current account moves into deficit.",
        "intuition": "The current account is also the national saving-investment gap: <b>CA = S - I</b>. If the economy invests more than it saves, the extra resources must come from abroad; if it saves more than it invests, it lends abroad. Splitting saving into private and government components gives <b>CA = (S<sub>p</sub> - I) + (T - G)</b>. This is the logic behind twin-deficits arguments: a larger fiscal deficit can reduce national saving and widen the current-account deficit, but only if private saving, investment, interest rates, and capital flows do not offset it.",
        "exam_applications": [
            "Formula check: Equations_Midterm_1 and the practice set both reinforce S - I = CA and CA = (S - I) + (T - G); use it after computing GNDI/GNE or a fiscal/private balance.",
            "Closed-economy contrast: if TB, NFIA, and CA are zero, then S = I; the open-economy exam move is identifying the foreign-financing gap.",
        ],
        "concepts": [
            ("National saving", "S = Y - C - G: income not consumed privately or publicly. It is the domestic resource pool available for investment or foreign lending."),
            ("Private saving", "S<sub>p</sub> = Y - T - C: after-tax private income not consumed. It can rise in response to expected future taxes, weakening a simple twin-deficits story."),
            ("Government saving", "T - G: tax revenue minus government purchases. A fiscal deficit is negative government saving."),
            ("Saving-investment gap", "CA = S - I. This form translates a trade/current-account question into domestic macro behavior."),
            ("Twin deficits", "Fiscal deficit and current-account deficit moving together through national saving. It is a conditional prediction, not an automatic law."),
            ("Capital inflow", "Foreign financing that lets domestic spending exceed income. It appears as foreign acquisition of domestic claims."),
            ("Crowding out/in", "Fiscal changes can alter interest rates, private saving, and investment, so the final CA effect depends on behavioral response."),
        ],
        "assumptions": [
            "The identity is measured over the same period and currency units.",
            "Private behavior may or may not offset public dissaving.",
            "Investment demand and saving supply are jointly determined, not mechanically separate.",
            "International capital markets can finance the gap rather than forcing immediate spending adjustment.",
        ],
        "strengths": [
            "Turns fiscal-policy questions into a clear current-account framework.",
            "Explains why a CA deficit can finance productive investment or excess consumption.",
            "Useful for decomposing data in short-answer questions.",
            "Highlights why the same CA deficit can have different meanings depending on S, I, and G.",
        ],
        "weaknesses": [
            "Causality can run through many channels, not just fiscal deficits.",
            "Ricardian offset or private saving shifts can weaken twin-deficit predictions.",
            "Does not assess debt sustainability by itself.",
            "Short-run capital-flow shocks can move the current account without a simple fiscal-policy origin.",
        ],
    },
    {
        "session": "Weeks 3-4",
        "title": "External Wealth and Valuation Effects",
        "source": "International Economics, Ch. 17, Section 17.1; GPCO 403 Lectures 4 and 6",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "A country can run a current-account deficit but still see external wealth improve if its foreign assets rise in value or its liabilities fall in domestic-currency terms.",
        "intuition": "External wealth is a stock: foreign assets owned by home residents minus home assets owned by foreigners. The current account changes that stock through net lending or borrowing, but the stock also moves through <b>valuation effects</b>: asset-price changes, exchange-rate changes, write-downs, and composition effects. This is why a country's external position cannot be read from the trade deficit alone. The United States can borrow heavily yet see offsetting wealth changes if its foreign assets earn high returns or if dollar-denominated liabilities shift value differently from foreign-currency assets.",
        "exam_applications": [
            "2025 answer key: capital gains and exchange-rate-driven changes in external wealth are valuation effects, not new financial flows.",
            "2025 U.S. balance-sheet example: dollar depreciation raises the dollar value of foreign-currency assets while dollar-denominated liabilities stay fixed, so U.S. external wealth rises all else equal.",
            "Practice LRBC setup: external wealth changes by the trade balance plus interest on initial wealth before adding any valuation terms.",
        ],
        "concepts": [
            ("External wealth", "Net foreign assets: home ownership of foreign assets minus foreign ownership of home assets. Positive external wealth means the country is a net creditor."),
            ("Flow vs stock", "CA is a flow over a period; external wealth is a stock at a point in time. Flows accumulate, but revaluation can move the stock independently."),
            ("Valuation effects", "Capital gains/losses from asset prices and exchange-rate changes. They explain why the NIIP can change even when the current account is small."),
            ("Exorbitant privilege", "U.S. ability to borrow in dollars and hold higher-yield or differently denominated foreign assets. It can improve returns relative to simple debtor status."),
            ("NIIP", "Net international investment position, the statistical measure of external wealth. It is the balance-sheet counterpart to the current account."),
            ("Currency denomination", "Whether assets and liabilities are priced in home or foreign currency. Depreciation helps or hurts depending on which side of the balance sheet is exposed."),
            ("Return differential", "Different rates of return on external assets and liabilities. It can let wealth evolve differently from cumulative borrowing.",
            ),
        ],
        "assumptions": [
            "Asset positions can be valued at market prices.",
            "Currency denomination matters for gains/losses after exchange-rate changes.",
            "Stocks update through both flows and revaluation, not flows alone.",
            "External assets and liabilities can be meaningfully classified by maturity, risk, and currency.",
        ],
        "strengths": [
            "Explains why CA flows and wealth stocks need not move one-for-one.",
            "Makes exchange-rate movements relevant for national balance sheets.",
            "Fits exam vocabulary around capital gains and external wealth.",
            "Improves crisis analysis by asking who owes what, in which currency, and at what maturity.",
        ],
        "weaknesses": [
            "Requires good data on asset composition, currency, and market value.",
            "Can make sustainability look better temporarily without fixing borrowing behavior.",
            "Country-level wealth analogies to households can mislead.",
            "Valuation gains can reverse quickly during market stress, so they are not the same as durable solvency.",
        ],
    },
    {
        "session": "Week 4",
        "title": "Intertemporal Trade and Consumption Smoothing",
        "source": "International Economics, Ch. 17, Section 17.1; GPCO 403 Lecture 6",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "After a temporary disaster, a country can borrow from abroad to avoid a sharp consumption collapse, then repay when output recovers.",
        "intuition": "International borrowing and lending is trade across time. Borrowers gain purchasing power today and promise repayment later; lenders sacrifice current purchasing power for future repayment. The welfare logic is strongest for temporary shocks and high-return investment: a country does not need to cut consumption one-for-one when income temporarily falls, and it can import capital goods before domestic saving is sufficient. The constraint is the intertemporal budget condition: borrowing is useful only if future income, saving, or returns can service the debt.",
        "exam_applications": [
            "Lecture 6: use present value to compare borrowing today with repayment tomorrow; future trade surpluses must be large enough in PV terms to support current borrowing.",
            "Lecture 6: the long-run budget constraint/no-Ponzi logic says debt cannot grow forever without repayment; the natural borrowing constraint binds when nobody will lend more resources.",
            "2025 Thailand tsunami: the current account can fall after a temporary disaster because exports/tourism fall and reconstruction imports rise; aid transfers and borrowing help smooth consumption.",
        ],
        "concepts": [
            ("Intertemporal trade", "Exchange of present goods for future goods through borrowing and lending. A current-account deficit imports present purchasing power; a surplus exports it."),
            ("Consumption smoothing", "Using borrowing/saving to make consumption less volatile than income. It is efficient when shocks are temporary and repayment is credible."),
            ("Temporary shock", "A shock worth smoothing because future income can support repayment. Natural disasters or commodity-price dips are classic examples."),
            ("Permanent shock", "A lasting income change that requires consumption adjustment. Borrowing against a permanent loss delays the adjustment and can worsen debt."),
            ("Intertemporal budget constraint", "Present value of spending must be consistent with present value of resources. It rules out endless debt rollover without future surpluses."),
            ("Investment financing", "Borrowing can be efficient if it funds projects whose returns exceed financing costs. The CA deficit then reflects capital accumulation, not only consumption."),
            ("Sudden stop", "A sharp loss of foreign financing that forces abrupt current-account adjustment and often recession.",
            ),
        ],
        "assumptions": [
            "Capital markets allow cross-border borrowing and lending.",
            "Borrowers can credibly repay or pledge future income.",
            "Temporary and permanent shocks can be distinguished well enough for policy.",
            "Borrowing costs reflect risk and do not suddenly jump in a way that invalidates planned smoothing.",
        ],
        "strengths": [
            "Explains why CA deficits can be efficient after temporary bad shocks.",
            "Connects global imbalances to savings, investment, and risk-sharing motives.",
            "Gives a welfare reason for international capital mobility.",
            "Helps distinguish good deficits that finance future capacity from fragile deficits that fund current consumption.",
        ],
        "weaknesses": [
            "Real markets face default risk, sudden stops, and political constraints.",
            "Permanent shocks make borrowing a delay, not a solution.",
            "Overborrowing can create crisis vulnerability.",
            "Distribution matters: the borrowers who gain today may not be the taxpayers or workers who pay later.",
        ],
    },
    {
        "session": "Week 3",
        "title": "Exchange-Rate Basics and Cross-Rate Arbitrage",
        "source": "International Economics, Ch. 12, Section 12.1; GPCO 403 Lecture 6 and Lecture 7 PPP Slides",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "If yen per dollar and pesos per dollar are quoted, yen per peso is the ratio of those two dollar exchange rates; a wrong cross-rate creates triangular arbitrage.",
        "intuition": "An exchange rate is a relative price of two monies, so direction matters. Appreciation/depreciation depends on the quote convention: more home currency per foreign currency means a home depreciation under one convention but the same movement can look inverted under the reciprocal convention. Cross rates use a vehicle currency to compare two non-dollar currencies, and arbitrage forces direct and indirect conversion paths to yield the same final amount. The exam pattern is mechanical but unforgiving: write units before calculating, cancel units, and only then interpret the movement.",
        "exam_applications": [
            "Practice and 2025 answer key: cross rates are ratios of the two quotes against the common vehicle currency; write units and cancel them before interpreting appreciation/depreciation.",
            "Lecture 7: triangular arbitrage disappears only when the direct trade and indirect vehicle-currency path yield the same final currency amount.",
        ],
        "concepts": [
            ("Nominal exchange rate", "Price of one currency in terms of another. Always write the quote as units of currency per unit of currency before interpreting it."),
            ("Appreciation", "A currency becomes more valuable. In home/foreign terms, home appreciation means fewer home units are needed to buy one foreign unit."),
            ("Depreciation", "A currency becomes less valuable. In home/foreign terms, home depreciation means more home units are needed to buy one foreign unit."),
            ("Cross rate", "Exchange rate between two currencies inferred through a third currency. It is a unit-cancellation exercise, not a memory exercise."),
            ("Vehicle currency", "Major currency, often the U.S. dollar, used as an intermediary in trades. It reduces the number of bilateral markets needed."),
            ("Triangular arbitrage", "Profit from inconsistent direct and indirect exchange rates. Buying low and selling high across three currencies should close the inconsistency."),
            ("Bid-ask spread", "The gap between buying and selling quotes. It creates a band in which apparent arbitrage may not be profitable."),
        ],
        "assumptions": [
            "Transaction costs and bid-ask spreads are small enough for arbitrage.",
            "Currencies can be freely exchanged or capital controls are absent.",
            "Quotes are contemporaneous and comparable.",
            "The trader can execute all legs fast enough that prices do not move before completion.",
        ],
        "strengths": [
            "High-probability multiple-choice calculation skill.",
            "Builds intuition for parity conditions and no-arbitrage logic.",
            "Forces disciplined unit conversion.",
            "Makes later PPP and interest-parity formulas less mysterious because all are relative-price conditions.",
        ],
        "weaknesses": [
            "Quote conventions easily flip intuition.",
            "Real markets include spreads, settlement risk, and restrictions.",
            "Arbitrage equalizes prices only within trading frictions.",
            "It explains price consistency, not the deeper macro forces moving exchange rates.",
        ],
    },
    {
        "session": "Week 3",
        "title": "Interest Parity and Forward Exchange Rates",
        "source": "International Economics, Ch. 13, Sections 13.1-13.4; Study Guide for GPCO 403 Midterm Spring 2025",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley",
        "situation": "An investor comparing dollar and euro deposits must account for interest rates and the expected or contracted future exchange rate, not just today’s spot rate.",
        "intuition": "Parity conditions extend no-arbitrage logic to financial assets. <b>Covered interest parity</b> uses a forward contract to lock in the future exchange rate, so equivalent-risk deposits should yield the same return after currency conversion; if not, investors can borrow in one currency, invest in the other, and cover the exchange-rate risk. <b>Uncovered interest parity</b> replaces the contracted forward rate with the expected future spot rate, so it is a theory of expected returns, expectations, and risk premia rather than a guaranteed arbitrage condition.",
        "exam_applications": [
            "Practice CIP: a Dutch investor gets EUR1,050 at 5% at home but EUR1,111 in Britain with forward cover when F/S = 1.65/1.5 and i* = 1%, so covered arbitrage exists.",
            "2025 Brazil CD: compare final USD values after converting USD to BRL, earning 2.25%, and converting back at expected 5.75 BRL/USD; higher foreign interest can beat mild depreciation.",
            "Breakeven shortcut: the real cannot depreciate by more than roughly the interest differential, 2.25% - 0.75% = 1.5%, before the real CD loses to the dollar CD.",
        ],
        "concepts": [
            ("Spot rate", "Exchange rate for immediate currency delivery. It is the starting price for converting principal today."),
            ("Forward rate", "Exchange rate contracted today for future delivery. It removes exchange-rate uncertainty from the future conversion leg."),
            ("CIP", "Covered interest parity: equal risk-free returns once forward cover is included. The covered return includes the interest rate and the locked-in forward conversion."),
            ("UIP", "Uncovered interest parity: expected returns equalize using the expected future spot rate. It predicts currency movements only if risk premia and expectation errors are not doing the work."),
            ("Forward premium", "Forward rate above the spot rate under a given quote convention. Interpret only after writing the units."),
            ("Exchange-rate expectation", "Belief about future currency value that enters uncovered returns. Expectations can shift immediately with news."),
            ("Risk premium", "Extra expected return investors require to hold currency risk. It is one reason UIP can fail empirically."),
            ("Covered arbitrage", "Borrow, convert, invest, and forward-cover to exploit a CIP deviation. Competition should erase the profit when markets function well."),
        ],
        "assumptions": [
            "Comparable assets have similar default and liquidity risk.",
            "Capital can move across borders.",
            "Forward contracts are enforceable for CIP; expectations are rational enough for UIP tests.",
            "Transaction costs, collateral constraints, and regulatory frictions are small enough not to absorb parity deviations.",
        ],
        "strengths": [
            "Explains links among interest rates, spot rates, forward rates, and expectations.",
            "CIP is a strong benchmark for arbitrage in integrated markets.",
            "Useful for interpreting policy-rate changes and currency pressure.",
            "Clarifies why a high-interest currency is not automatically a free lunch once exchange-rate movements are included.",
        ],
        "weaknesses": [
            "UIP often performs poorly empirically because risk premia and expectations matter.",
            "CIP can break during crises or balance-sheet constraints.",
            "Quote conventions can reverse premium/discount language.",
            "Parity equations are clean, but real assets differ in liquidity, default risk, taxes, and capital controls.",
        ],
    },
    {
        "session": "Week 5",
        "title": "Exchange-Rate Regimes and Crisis Balance Sheets",
        "source": "Study Guide for GPCO 403 Midterm Spring 2025; GPCO 403 Lecture 6; Dollar-Denominated Public Debt in Asia and Latin America",
        "author": "Kyle Handley; Paulina Restrepo-Echavarria and Praew Grittayaphong",
        "situation": "If a government borrows in dollars but earns tax revenue in local currency, depreciation raises the local-currency burden of repayment and can turn FX movement into fiscal stress.",
        "intuition": "Exchange-rate regimes shape how prices adjust and where crisis pressure appears. Floating rates adjust through the currency price; pegs require reserves, interest-rate defense, or capital controls; managed regimes sit between those poles. Balance-sheet exposure matters because assets, revenues, and liabilities may be denominated in different currencies. A depreciation can improve export competitiveness and close external gaps, but the same depreciation can worsen solvency when governments, banks, or firms owe foreign-currency debt against local-currency income.",
        "exam_applications": [
            "2021 Korea payable: a U.S. firm owing 50 billion won can hedge by buying won now and investing in won assets or by buying a forward contract for won delivery at a preset rate.",
            "Lecture 6 emerging-market limit: poorer countries often pay a risk premium on government debt, private debt, equity, and FDI, making consumption smoothing harder in downturns.",
            "U.S. contrast: exorbitant privilege means the United States can often borrow low and hold higher-return/riskier foreign assets; do not generalize that privilege to emerging markets.",
        ],
        "concepts": [
            ("Floating regime", "Exchange rate moves mainly with market forces. Adjustment occurs through the currency, though authorities may still intervene occasionally."),
            ("Peg", "Government/central bank commits to a fixed exchange rate. Credibility depends on reserves, policy willingness, and market beliefs."),
            ("Managed float", "Authorities intervene without a strict fixed parity. It can smooth volatility while preserving some exchange-rate flexibility."),
            ("Capital controls", "Restrictions on currency or financial-account transactions. They can slow pressure but may create distortions and credibility costs."),
            ("Currency mismatch", "Assets/revenues and liabilities are denominated in different currencies. Depreciation hurts borrowers whose liabilities are in foreign currency."),
            ("Dollar-denominated debt", "Debt owed in dollars, creating repayment risk after local depreciation. The local-currency value of debt rises when the local currency weakens."),
            ("Reserve defense", "Using foreign-exchange reserves to support a peg or smooth depreciation. Reserves buy time but are finite."),
            ("Balance-sheet channel", "Exchange-rate movements affect net worth directly through currency denomination, not only through trade competitiveness."),
        ],
        "assumptions": [
            "Regime commitments are credible only if reserves/policy support them.",
            "Balance-sheet effects depend on denomination, maturity, and hedging.",
            "Market participants can reassess default and devaluation risk quickly.",
            "Domestic borrowers cannot perfectly hedge all foreign-currency exposure.",
        ],
        "strengths": [
            "Connects exchange-rate theory to crisis questions and institutions.",
            "Explains why depreciation can help trade but hurt borrowers.",
            "Makes asset/liability composition central rather than treating CA alone as crisis measure.",
            "Shows why the same shock can be manageable under one balance-sheet structure and disastrous under another.",
        ],
        "weaknesses": [
            "Regime labels can hide substantial intervention.",
            "Crisis timing depends on expectations and politics, not just accounting exposure.",
            "Policy tradeoffs differ across countries with reserve-currency privilege.",
            "The framework identifies vulnerability but does not by itself forecast the trigger date of a crisis.",
        ],
    },
    {
        "session": "Week 5",
        "title": "Law of One Price",
        "source": "International Economics, Ch. 14, Section 14.1; GPCO 403 Lectures 7-8; GPCO 403 Week 4 Reference",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "If the same iPhone costs $1,000 in the United States and EUR950 in France at $0.90/EUR, the French price is $855, so LOOP predicts arbitrage pressure unless frictions explain the gap.",
        "intuition": "The <b>law of one price</b> says the same tradable good should sell for the same price in two places once prices are expressed in one currency. If the common-currency prices differ, arbitrageurs should buy where the good is cheap and sell where it is expensive until the price gap closes. In practice, LOOP is best used as a benchmark with a no-arbitrage band: shipping, taxes, tariffs, product differences, resale limits, and local market power create wedges that allow price gaps to persist without pure profit.",
        "exam_applications": [
            "Lecture 7: LOOP is a goods-market no-arbitrage condition; the same good can deviate inside trade-cost bands because shipping, tariffs, taxes, VAT, and resale frictions absorb the gap.",
            "Lecture 7: even tradable-looking goods embed nontraded labor, distribution, rent, and services, so common-currency equality is the benchmark, not the expectation.",
        ],
        "concepts": [
            ("LOOP", "P<sub>home</sub> = E x P<sub>foreign</sub> for the same good under frictionless arbitrage. The exact formula depends on the exchange-rate quote convention."),
            ("Common-currency price", "Foreign price converted into home currency before comparison. Most exam errors come from comparing prices before this conversion."),
            ("Arbitrage band", "Price gap can persist up to the cost of moving/exchanging goods. Inside the band, arbitrage is not profitable."),
            ("Tradable good", "A good that can be shipped or resold across markets. LOOP is strongest for homogeneous, easily transported goods."),
            ("Pricing to market", "Firms charge different prices across countries because markets are segmented. It weakens the simple arbitrage prediction."),
            ("Trade costs", "Shipping, tariffs, taxes, insurance, time, and compliance costs that drive a wedge between locations."),
            ("Market segmentation", "Legal, logistical, or strategic barriers that prevent buyers from freely reselling across borders."),
        ],
        "assumptions": [
            "Goods are identical and tradable.",
            "Markets are competitive.",
            "No transport costs, taxes, tariffs, or trade barriers.",
            "Arbitrageurs can buy and resell freely.",
            "Exchange rates and prices are measured at the same time and with the same units.",
        ],
        "strengths": [
            "Clearest one-good benchmark for exchange-rate mispricing.",
            "Directly testable through common-currency price calculations.",
            "Builds the intuition for PPP.",
            "Good exam device for explaining whether a price gap is arbitrage or a friction.",
        ],
        "weaknesses": [
            "Fails often for differentiated goods and local services.",
            "Trade costs make equality too strict.",
            "Market power and regulations can sustain price gaps.",
            "Even for identical goods, taxes, warranties, distribution contracts, and timing can explain deviations.",
        ],
    },
    {
        "session": "Week 5",
        "title": "Purchasing Power Parity and the Real Exchange Rate",
        "source": "International Economics, Ch. 14, Section 14.1; GPCO 403 Lectures 7-8; GPCO 403 Week 4 Reference",
        "author": "Robert C. Feenstra and Alan M. Taylor; Kyle Handley; Plutus",
        "situation": "If inflation is higher at home than abroad, relative PPP predicts home-currency depreciation so baskets remain comparably priced over the long run.",
        "intuition": "<b>PPP</b> generalizes LOOP from one good to a basket. Absolute PPP says a common-currency basket should cost the same across countries; the <b>real exchange rate</b> measures the relative price of foreign to home baskets. Relative PPP focuses on changes: if home inflation exceeds foreign inflation, home currency should depreciate enough to keep relative purchasing power from drifting permanently. The crucial exam nuance is that PPP is a long-run goods-market anchor, not a short-run exchange-rate forecast; financial flows, expectations, sticky prices, and nontraded goods can dominate in the short run.",
        "exam_applications": [
            "2021 Mongolia: nominal depreciation alone is not enough; compare the exchange-rate change with cumulative inflation. Relative PPP asks whether the real price of travel changed after both price levels move.",
            "Lecture 7: absolute PPP often fails in levels, but relative PPP is useful as a long-run inflation/exchange-rate benchmark; q should be roughly stable, not necessarily equal to 1.",
            "Unit caution: overvalued means local goods are expensive relative to the PPP benchmark and should eventually depreciate, but only after checking which currency is in the numerator.",
        ],
        "concepts": [
            ("Absolute PPP", "Common-currency price levels equalize: q = 1 under the chosen quote convention. It is a level condition and usually too strict empirically."),
            ("Real exchange rate", "q = E x P<sub>foreign</sub> / P<sub>home</sub>; relative price of baskets. Interpret q only after confirming the quote convention."),
            ("Real depreciation", "Home goods become cheaper relative to foreign goods. It can increase competitiveness if quantities respond."),
            ("Real appreciation", "Home goods become more expensive relative to foreign goods. It can reduce net exports if demand is price-sensitive."),
            ("Relative PPP", "Percent change in E approximately equals home inflation minus foreign inflation. It is a change condition and often performs better than absolute PPP."),
            ("Law-of-one-price foundation", "PPP inherits the arbitrage logic of LOOP but applies it to a broad basket rather than a single good."),
            ("Long-run anchor", "PPP works better over longer horizons than month-to-month movements because goods prices adjust slowly and financial shocks dominate short horizons."),
            ("Balassa-Samuelson logic", "Richer countries may have higher nontraded-service prices, so their price levels can look high without implying simple currency overvaluation."),
        ],
        "assumptions": [
            "Consumption baskets are comparable across countries.",
            "Goods-market arbitrage links prices across borders.",
            "Nontraded inputs and local taxes do not dominate the basket.",
            "Inflation and exchange-rate measures use consistent quote conventions.",
            "Price adjustment is sufficiently flexible over the horizon being analyzed.",
        ],
        "strengths": [
            "Connects inflation differentials to exchange-rate movements.",
            "Provides a benchmark for overvaluation/undervaluation.",
            "Explains why high-inflation currencies tend to depreciate in the long run.",
            "Gives a disciplined way to separate nominal exchange-rate movements from real competitiveness changes.",
        ],
        "weaknesses": [
            "Short-run exchange rates are driven by finance, expectations, and shocks.",
            "Nontraded goods, trade costs, and quality differences break basket equality.",
            "Income-level differences can bias simple PPP comparisons.",
            "Using the wrong basket, base year, or quote convention can reverse the interpretation.",
        ],
    },
    {
        "session": "Week 5",
        "title": "Big Mac Index as Applied PPP",
        "source": "The Big Mac Index; 2026-04-27 PPP, LOOP, and Big Mac One-Page Summary; GPCO 403 Week 4 Reference",
        "author": "The Economist; Plutus",
        "situation": "If a Big Mac is cheaper abroad after converting to dollars, that currency looks undervalued against the dollar under a simple PPP benchmark.",
        "intuition": "The Big Mac Index makes PPP visible by comparing one standardized product across countries. It asks whether the market exchange rate makes a Big Mac equally priced in dollar terms, then labels currencies overvalued or undervalued relative to the implied PPP exchange rate. The index is useful because it turns an abstract basket theory into one familiar good, but its flaws are the lesson: a Big Mac contains nontraded labor, rent, electricity, distribution, taxes, and local pricing strategy, so deviations from PPP are expected and should be interpreted as rough signals, not precise mispricing.",
        "exam_applications": [
            "2025 iPhone/Big Mac style: convert to one currency first. If the foreign price is lower in dollars, the foreign good is cheaper and the currency looks undervalued under the simple benchmark.",
            "Lecture 7: Big Mac deviations teach PPP limits: VAT, nontraded inputs, distribution costs, trade barriers, income levels, and market power can all justify price gaps.",
        ],
        "concepts": [
            ("Implied PPP exchange rate", "Local Big Mac price divided by U.S. Big Mac price under the relevant quote. It is the exchange rate that would equalize Big Mac prices."),
            ("Overvaluation", "Currency buys too much in dollar terms relative to the Big Mac benchmark. The actual exchange rate makes the foreign Big Mac too expensive in common currency."),
            ("Undervaluation", "Currency buys too little in dollar terms relative to the benchmark. The actual exchange rate makes the foreign Big Mac too cheap in common currency."),
            ("Common-currency comparison", "Convert the local price into dollars before judging cheap or expensive. This is the operational bridge from LOOP to PPP."),
            ("Nontraded inputs", "Local costs such as labor and rent embedded in a tradable-looking product. These costs vary systematically by income level."),
            ("Income adjustment", "Richer countries often have higher service costs, affecting Big Mac prices. Adjusted versions try to separate income effects from currency mispricing."),
            ("Single-good index", "A deliberately simple proxy for PPP. Its simplicity makes it memorable but also limits inference."),
        ],
        "assumptions": [
            "Big Macs are sufficiently comparable across countries.",
            "The product’s traded and nontraded inputs are not too different across markets.",
            "The observed exchange rate and prices refer to the same time period.",
            "Local taxes, market strategy, and input costs do not swamp the exchange-rate signal.",
        ],
        "strengths": [
            "Memorable way to practice common-currency price comparisons.",
            "Shows over/undervaluation logic quickly.",
            "Highlights why PPP is useful but imperfect.",
            "Easy to deploy in an exam as an intuitive example of absolute PPP and its limits.",
        ],
        "weaknesses": [
            "One product is not a representative consumption basket.",
            "Local costs and taxes matter a lot.",
            "Fast-food pricing strategies and quality differences contaminate the signal.",
            "A cheap Big Mac does not automatically mean a currency should immediately appreciate.",
        ],
    },
]


AUTHOR_CONTEXT = {
    "National Income Accounting and Open-Economy GDP": "Feenstra and Taylor write from the modern open-economy macro tradition, where the point of the national accounts is to discipline arguments about globalization with identities that separate production, expenditure, income, and ownership. Handley's early lectures use that framework for a policy environment in which trade deficits and supply chains are often discussed loosely in public debate.",
    "Current Account and Balance of Payments Identity": "The balance-of-payments framework is the international macro bookkeeping system used by institutions such as the IMF and central banks after decades of cross-border trade and capital-flow growth. Feenstra and Taylor teach it as a double-entry ledger so students do not mistake a current-account deficit for money vanishing from the country.",
    "Savings-Investment Gap and Twin Deficits": "This page comes from the national-income-identity side of Feenstra and Taylor, not from a single political claim. The twin-deficits idea became especially salient in U.S. policy debates when fiscal deficits, foreign borrowing, and current-account deficits moved together, but the course treats it as a conditional accounting-and-behavior mechanism.",
    "External Wealth and Valuation Effects": "The external-wealth material reflects the post-1990s world of large gross asset positions, reserve-currency privilege, and balance sheets that can move even when trade flows are modest. Feenstra and Taylor emphasize this because modern globalization is about portfolios and valuation changes as much as trade in goods.",
    "Intertemporal Trade and Consumption Smoothing": "Intertemporal trade is the open-economy version of consumption smoothing: countries borrow and lend across time. The source environment is the international-capital-market setting where temporary shocks, disasters, investment needs, and credibility determine whether borrowing is welfare-improving or crisis-prone.",
    "Exchange-Rate Basics and Cross-Rate Arbitrage": "The exchange-rate basics are drawn from the market microstructure and no-arbitrage foundation of international finance. Handley's lectures use cross-rate problems because the modern FX market quotes many currencies through vehicle currencies, especially the dollar, and small unit mistakes flip the economics.",
    "Interest Parity and Forward Exchange Rates": "Interest parity comes from international finance's no-arbitrage tradition. Covered parity is closest to a market-pricing condition in deep forward markets; uncovered parity is a weaker expectations theory used in an environment where interest-rate differences, expected depreciation, and risk premia all compete.",
    "Exchange-Rate Regimes and Crisis Balance Sheets": "The regime and crisis page combines Handley's midterm review with recent policy concern over dollar-denominated debt in emerging markets. The author environment is one of financially open economies where pegs, managed floats, reserve defenses, and currency mismatches can turn exchange-rate movements into fiscal or banking stress.",
    "Law of One Price": "The law of one price is the goods-market no-arbitrage benchmark behind PPP. Feenstra and Taylor present it in a global trade environment where arbitrage is real but never frictionless: transport costs, taxes, product differences, and market segmentation explain why the benchmark is useful even when literal equality fails.",
    "Purchasing Power Parity and the Real Exchange Rate": "PPP is an old international-macro benchmark repurposed in modern courses as a long-run anchor, not a short-run forecast. Feenstra, Taylor, and Handley use it to connect inflation, nominal exchange rates, and real competitiveness in a world where goods prices adjust slowly and financial markets move quickly.",
    "Big Mac Index as Applied PPP": "The Economist's Big Mac Index is journalistic rather than a formal academic model, introduced to make PPP concrete for non-specialists. Its environment is comparative, public-facing international economics: it turns exchange-rate misalignment into a familiar sandwich comparison while revealing the limits of single-good PPP.",
}


def plain(text):
    text = re.sub(r"<sub>(.*?)</sub>", r"\1", text)
    text = re.sub(r"<super>(.*?)</super>", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("—", "-").replace("–", "-").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip()


def wrap_line(c, text, width, font="Helvetica", size=12):
    words = plain(text).split()
    lines = []
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if c.stringWidth(trial, font, size) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def brief(text, limit=180):
    text = plain(text)
    first_sentence = re.split(r"(?<=[.!?])\s+", text)[0]
    if len(first_sentence) <= limit:
        return first_sentence
    return first_sentence[: limit - 1].rsplit(" ", 1)[0] + "."


def draw_box(c, x, y_top, w, h, title, paragraphs, fill=None, border=BORDER_GREY, title_color=DARK_NAVY):
    c.saveState()
    if fill:
        c.setFillColor(fill)
        c.rect(x, y_top - h, w, h, fill=1, stroke=0)
    c.setStrokeColor(border)
    c.setLineWidth(0.45)
    c.rect(x, y_top - h, w, h, fill=0, stroke=1)
    c.setFillColor(title_color)
    c.setFont("Helvetica-Bold", 9.6)
    c.drawString(x + 6, y_top - 13, title)
    y = y_top - 29
    overflow = []
    for para_text in paragraphs:
        if isinstance(para_text, tuple):
            bullet_title, body = para_text
            text = f"{bullet_title}: {brief(body)}"
            prefix = "- "
        else:
            text = para_text if title in {"SITUATION + MECHANISM", "AUTHOR / SOURCE CONTEXT", "Use"} else brief(para_text)
            prefix = ""
        font = "Helvetica"
        size = 12
        leading = 13.35
        lines = wrap_line(c, text, w - 14, font, size)
        if prefix and lines:
            lines[0] = prefix + lines[0]
        for line in lines:
            if y < y_top - h + 9:
                overflow.append(line)
                continue
            c.setFillColor(TEXT)
            c.setFont(font, size)
            c.drawString(x + 7, y, line)
            y -= leading
        y -= 3
    if overflow:
        OVERFLOW_LOG.append((title, len(overflow), overflow[0]))
    c.restoreState()
    return overflow


def draw_footer(c, page_num):
    w, _h = landscape(letter)
    c.saveState()
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(0.32 * inch, 0.24 * inch, TITLE)
    c.drawRightString(w - 0.32 * inch, 0.24 * inch, f"Page {page_num}")
    c.restoreState()


def top_concepts(theory, n=3):
    return theory["concepts"][:n]


def top_items(items, n=4):
    return items[:n]


def draw_cover(c):
    w, h = landscape(letter)
    margin = 0.38 * inch
    c.setFillColor(DARK_NAVY)
    c.rect(0, h - 1.05 * inch, w, 1.05 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, h - 0.48 * inch, "GPCO 403 Midterm Theory Reference")
    c.setFont("Helvetica", 12)
    c.drawCentredString(w / 2, h - 0.75 * inch, "International Economics | Prof. Kyle Handley | UCSD GPS | Spring 2026")
    desc = (
        "Version 1.3.0 rebuilds the v1.2.0 reference with 12pt body text, fuller theory-page explanation, "
        "and source context at the start of each theory. History of Warfare material remains skipped. "
        "Landscape pages, tight margins, and compact blocks preserve one page per theory."
    )
    draw_box(c, margin, h - 1.35 * inch, w - 2 * margin, 0.95 * inch, "Use", [desc], fill=LIGHT_GREY)
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, h - 2.38 * inch, "Table of Contents")
    y = h - 2.68 * inch
    for i, theory in enumerate(THEORIES, 1):
        anchor = slugify(theory["title"])
        c.bookmarkHorizontalAbsolute(anchor + "_toc", 0, y)
        c.setFillColor(MED_BLUE)
        c.setFont("Helvetica", 11.4)
        label = f"{i}. {theory['session']} - {theory['title']}"
        c.drawString(margin, y, label)
        c.linkRect("", anchor, (margin, y - 2, w - margin, y + 12), relative=0, thickness=0, color=MED_BLUE)
        y -= 20
    c.setStrokeColor(BORDER_GREY)
    c.line(margin, 0.72 * inch, margin + 2.8 * inch, 0.72 * inch)
    foot = (
        f"Generated with {MODEL} via the Claudia agent system. Course: GPCO 403 International Economics, "
        "Prof. Kyle Handley, UC San Diego School of Global Policy and Strategy. Always verify against official "
        "course materials and readings; this is a study aid, not a substitute for assigned texts."
    )
    c.setFillColor(colors.HexColor("#666666"))
    c.setFont("Helvetica", 8.2)
    y = 0.54 * inch
    for line in wrap_line(c, foot, w - 2 * margin, "Helvetica", 8.2):
        c.drawString(margin, y, line)
        y -= 9.5
    draw_footer(c, 1)
    c.showPage()


def draw_theory(c, theory, page_num):
    w, h = landscape(letter)
    margin = 0.27 * inch
    usable_w = w - 2 * margin
    anchor = slugify(theory["title"])
    c.bookmarkPage(anchor, fit="XYZ", left=0, top=h)
    c.addOutlineEntry(theory["title"], anchor, level=0)
    c.setFillColor(DARK_NAVY)
    c.rect(margin, h - 0.62 * inch, usable_w, 0.44 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin + 8, h - 0.36 * inch, f"{theory['session']} | {theory['title']}")
    c.setFont("Helvetica-Oblique", 8.4)
    c.drawString(margin + 8, h - 0.53 * inch, plain(f"{theory['source']} - {theory['author']}")[:150])

    top_y = h - 0.76 * inch
    context_h = 1.02 * inch
    draw_box(c, margin, top_y, usable_w, context_h, "AUTHOR / SOURCE CONTEXT", [AUTHOR_CONTEXT[theory["title"]]], fill=LIGHT_GREY)

    col_gap = 7
    col_w = (usable_w - 2 * col_gap) / 3
    y2 = top_y - context_h - 7
    main_h = 3.82 * inch
    lower_h = 1.46 * inch
    c1 = margin
    c2 = margin + col_w + col_gap
    c3 = margin + 2 * (col_w + col_gap)
    main_left_w = (usable_w - col_gap) * 0.59
    main_right_w = usable_w - col_gap - main_left_w
    right_x = margin + main_left_w + col_gap

    mechanism = [
        theory["situation"],
        plain(theory["intuition"]) + " Exam logic: write the identity, parity condition, or balance-sheet channel first; then explain the mechanism and the violated assumption."
    ]
    draw_box(c, c1, y2, main_left_w, main_h, "SITUATION + MECHANISM", mechanism, fill=None)
    draw_box(c, right_x, y2, main_right_w, 1.78 * inch, "KEY TERMS", top_concepts(theory, 2), fill=None)
    exam_items = theory.get("exam_applications", [])
    draw_box(c, right_x, y2 - 1.78 * inch - 7, main_right_w, main_h - 1.78 * inch - 7, "EXAM LOGIC", top_items(exam_items, 2), fill=None)

    y3 = y2 - main_h - 7
    draw_box(c, c1, y3, col_w, lower_h, "ASSUMPTIONS", top_items(theory["assumptions"], 2), fill=WARM_AMBER)
    draw_box(c, c2, y3, col_w, lower_h, "STRENGTHS", top_items(theory["strengths"], 2), fill=LIGHT_BLUE)
    draw_box(c, c3, y3, col_w, lower_h, "WEAKNESSES", top_items(theory["weaknesses"], 2), fill=WARM_AMBER)
    draw_footer(c, page_num)
    c.showPage()


def draw_references(c, page_num):
    w, h = landscape(letter)
    margin = 0.45 * inch
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, h - 0.7 * inch, "References")
    refs = [
        "Feenstra, R. C., & Taylor, A. M. (2021). International economics (5th ed.). Worth Publishers.",
        "Handley, K. (2026). GPCO 403 syllabus 2026 [Course syllabus]. UC San Diego School of Global Policy and Strategy.",
        "Handley, K. (2026). GPCO 403 International Economics lecture slides and midterm review materials [Course materials]. UC San Diego School of Global Policy and Strategy.",
        "Restrepo-Echavarria, P., & Grittayaphong, P. (2021, August 3). Dollar-denominated public debt in Asia and Latin America. Federal Reserve Bank of St. Louis: On the Economy Blog.",
        "The Economist. (n.d.). The Big Mac index.",
    ]
    y = h - 1.08 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 12)
    for ref in refs:
        for line in wrap_line(c, ref, w - 2 * margin, "Helvetica", 12):
            c.drawString(margin, y, line)
            y -= 14
        y -= 7
    disclosure = (
        f"---\nGenerated for: Edgar Agunias\nDate: {DATE}\nModel: {MODEL}\n"
        "Sources: GPCO 403 syllabus/course memory; v1.2.0 theory reference and notes; existing Week 4 reference and Apr. 27 PPP/LOOP one-pager; machine-readable Spring 2021 and 2025 midterm answer keys, practice questions, Lecture 6, Lecture 7 PPP, and formula-check files listed in the sibling v1.3.0 notes.\n"
        "Agent: Plutus\n---"
    )
    y -= 8
    c.setFont("Helvetica", 11.2)
    for paragraph in disclosure.split("\n"):
        for line in wrap_line(c, paragraph, w - 2 * margin, "Helvetica", 11.2):
            c.drawString(margin, y, line)
            y -= 13
    draw_footer(c, page_num)
    c.showPage()


def build():
    OVERFLOW_LOG.clear()
    c = canvas.Canvas(str(OUT), pagesize=landscape(letter))
    c.setTitle(TITLE + " v1.3.0")
    draw_cover(c)
    for i, theory in enumerate(THEORIES, start=2):
        draw_theory(c, theory, i)
    draw_references(c, len(THEORIES) + 2)
    c.save()
    if OVERFLOW_LOG:
        for title, count, first_line in OVERFLOW_LOG:
            print(f"OVERFLOW {title}: {count} clipped lines; first={first_line}")
        raise SystemExit(1)


if __name__ == "__main__":
    build()
