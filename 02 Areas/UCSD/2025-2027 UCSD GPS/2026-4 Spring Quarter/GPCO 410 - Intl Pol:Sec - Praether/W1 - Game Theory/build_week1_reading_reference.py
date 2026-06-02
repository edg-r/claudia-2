from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit


PAGE_W, PAGE_H = landscape(letter)
MARGIN = 0.4 * inch
FOOTER_H = 0.28 * inch
HEADER_H = 0.64 * inch
BODY_TOP = PAGE_H - MARGIN - HEADER_H - 0.08 * inch
BODY_BOTTOM = MARGIN + FOOTER_H + 0.08 * inch
BODY_H = BODY_TOP - BODY_BOTTOM
GAP = 0.18 * inch
COL_W = (PAGE_W - 2 * MARGIN - 2 * GAP) / 3.0

DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
TEXT = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#4B5563")

TITLE = "Week 1 Strategic Readings Reference"
COURSE = "GPCO 410 - International Politics: Security"
TERM = "Week 1"
INSTRUCTOR = "Instructor not specified in source files"
INSTITUTION = "Institution not specified in source files"

READINGS = [
    {
        "slug": "mcmillan",
        "order": "Reading 1",
        "title": "The Art and Science of Strategy",
        "author": "John McMillan",
        "citation": "Chapter excerpt in Week 1_McMillan.pdf",
        "sections": [
            (
                "1. Author Background and Political Context",
                "McMillan was an economist who wrote for managers and policy readers trying to understand strategic interdependence without heavy formalism. This chapter reads like an introductory bridge from economics into applied strategy, written for an era shaped by globalization, corporate rivalry, and faith that formal tools could improve managerial judgment. It functions as a foundation rather than a narrow intervention: the point is to justify game theory as a practical way to think.",
            ),
            (
                "2. Big Picture (Macro Intuition)",
                "The puzzle is simple: why do smart actors keep making choices whose payoff depends on what others do next? McMillan argues that strategy matters whenever outcomes are jointly produced, not individually chosen. Without this lens, managers and policymakers treat rival behavior like background noise when it is actually part of the causal mechanism.",
            ),
            (
                "3. Core Theoretical Logic",
                "The mechanism starts from interdependence. A rational choice in a strategic setting is one made after forecasting how other players will react. Game theory helps by simplifying the setting, listing actions, and tracing how each actor's incentives depend on others' moves. The theory works best if actors are purposive, incentives are at least roughly knowable, and strategic responses are not pure chaos.",
            ),
            (
                "4. Key Concepts and Terms",
                "- Strategy: a plan formed under interdependence.\n- Interdependence: one actor's payoff depends on others' actions.\n- Rational behavior: purposeful, not omniscient, choice.\n- Game theory: structured analysis of strategic interaction.\n- Model: a simplification designed to isolate essential incentives.\n- Prediction: an estimate of likely responses, not perfect foresight.",
            ),
            (
                "5. Micro Dynamics, Edge Cases, and Counterfactuals",
                "The argument is weakest when preferences are unstable, organizations are fragmented, or actors cannot even identify the relevant game. If one firm faced no meaningful response from rivals or regulators, strategy would collapse back into ordinary optimization. Conversely, if several actors learn and adapt quickly, the 'correct' move may shift before the original model finishes describing the situation.",
            ),
            (
                "6. Empirical or Historical Evidence and Limitations",
                "McMillan mostly uses anecdotes, definitional discussion, and the history of game theory rather than formal empirical testing. That is fine for an introductory chapter, but it means the evidence demonstrates plausibility more than causal validation. The chapter teaches a way of seeing; it does not prove that this lens outperforms rivals across domains.",
            ),
            (
                "7. Critical Assessment of Assumptions and Weaknesses",
                "The chapter assumes purposive actors, intelligible incentives, and enough stability for prediction to matter. Those assumptions are often realistic in markets, but less so in bureaucracies or crises driven by ideology, confusion, or emotion. It also underplays power asymmetries and organizational politics: some actors do not just predict the game, they shape who is allowed to play.",
            ),
            (
                "8. Connection to Contemporary News or Policy Debates",
                "The reading helps explain current AI-platform competition and antitrust fights. Reuters reported an EU antitrust complaint over Google's AI Overviews on July 4, 2025, and a DOJ official said on Sept. 18, 2025 that antitrust scrutiny would track exclusion across the AI stack. McMillan's lens clarifies why firms act preemptively when rivals control key inputs, defaults, or distribution channels.",
            ),
            (
                "9. One-Paragraph Mental Model",
                "Think of strategy as driving with other drivers who are also anticipating you. McMillan is useful because he forces you to treat reactions as part of the environment, not as afterthoughts. Be skeptical when the road itself is changing fast, when preferences are unclear, or when institutions and identities matter more than payoff calculation.",
            ),
        ],
    },
    {
        "slug": "dixit-nalebuff",
        "order": "Reading 2",
        "title": "Anticipating Your Rival's Response",
        "author": "Avinash K. Dixit and Barry J. Nalebuff",
        "citation": "Thinking Strategically, chapter excerpt in Week 1_Dixit Nalebuff.pdf",
        "sections": [
            (
                "1. Author Background and Political Context",
                "Dixit and Nalebuff are economists known for translating game theory into usable strategic reasoning for business and policy audiences. Written in the early 1990s, the chapter reflects a moment when game theory was moving from formal economics into management, public policy, and everyday decision-making. Within their broader work, this is a foundational popularization: it teaches strategic logic before later, more elaborate cases.",
            ),
            (
                "2. Big Picture (Macro Intuition)",
                "The core problem is that people often treat an opponent's future move as uncertainty when it is actually a predictable response to current incentives. The chapter matters because many policy and market mistakes come from choosing an action in isolation rather than asking what sequence of reactions it triggers. Without that shift, entry deterrence, bargaining, and deterrence problems look random when they are structured.",
            ),
            (
                "3. Core Theoretical Logic",
                "Their mechanism is backward induction in plain English: look ahead to later nodes, predict what each player will do there, then reason back to the present move. Game trees make the logic visible. The theory requires players to understand the sequence, know or infer payoffs reasonably well, and expect others to act purposively. Once those assumptions fail, prediction becomes much less sharp.",
            ),
            (
                "4. Key Concepts and Terms",
                "- Sequential move game: actors move in turn.\n- Simultaneous move game: actors choose without seeing current choices.\n- Game tree: map of decision paths.\n- Look ahead and reason back: solve from future responses to present choice.\n- Payoffs: what each endpoint is worth to each actor.\n- Credible response: a future action that remains optimal when the moment comes.",
            ),
            (
                "5. Micro Dynamics, Edge Cases, and Counterfactuals",
                "The argument can break when later responses are not credible, when payoffs are private, or when repeated interaction makes reputation more important than one-shot logic. In the Newcleaners example, entry changes if Fastcleaners values a tough reputation for future markets. If the same interaction were simultaneous rather than sequential, backward reasoning alone would not solve the game.",
            ),
            (
                "6. Empirical or Historical Evidence and Limitations",
                "Evidence is pedagogical rather than systematic: Charlie Brown, entry deterrence, commuting choices, and chess. That makes the logic memorable, but it also means the chapter does not test how often real actors correctly infer payoffs or carry out the reasoning. It is strongest as a toolkit for disciplined thinking, not as a demonstrated empirical law.",
            ),
            (
                "7. Critical Assessment of Assumptions and Weaknesses",
                "The analysis leans heavily on stable preferences and fairly clear knowledge of how the game is structured. Real policy settings often contain multiple audiences, domestic constraints, and noisy signals that make the tree itself contested. The chapter also understates how emotions, norms, and misperception can keep actors from choosing the move that a clean game tree would imply.",
            ),
            (
                "8. Connection to Contemporary News or Policy Debates",
                "This chapter travels well to current tariff politics. Reuters described U.S.-South Korea tariff threats on Jan. 27, 2026 as a seesaw of threats, concessions, and investment promises. The strategic lesson is exactly Dixit and Nalebuff's: today's threat is not the endpoint; it is a move meant to shape the rival's next move, and the right analysis starts with the anticipated response.",
            ),
            (
                "9. One-Paragraph Mental Model",
                "Do not choose at the fork in front of you; choose after tracing the full path that fork creates. The chapter is powerful because it turns vague strategy talk into a sequence problem. Be skeptical when the tree is disputed, when players care about reputation or identity, or when future nodes are too uncertain to prune cleanly.",
            ),
        ],
    },
    {
        "slug": "muthoo",
        "order": "Reading 3",
        "title": "A Non-Technical Introduction to Bargaining Theory",
        "author": "Abhinay Muthoo",
        "citation": "World Economics 1(2), 2000",
        "sections": [
            (
                "1. Author Background and Political Context",
                "Muthoo is an economist associated with formal bargaining theory, and this article translates that literature for nontechnical readers shortly after his 1999 book on bargaining theory. The timing matters: it is written in a period defined by globalization, coalition politics, labor disputes, trade talks, and optimism about using formal economic logic to explain negotiation. This piece is a synthesis and public-facing refinement, not a radical departure.",
            ),
            (
                "2. Big Picture (Macro Intuition)",
                "The paper asks why actors who both gain from cooperation still delay, threaten, or fail to agree, and why the eventual deal divides gains unequally. That matters because many policy outcomes, from wage bargains to trade deals to war termination, hinge less on whether cooperation is valuable than on how the surplus is divided. Existing accounts that say 'they should just agree' miss the distributional fight.",
            ),
            (
                "3. Core Theoretical Logic",
                "A bargaining situation combines common interests and conflicting interests. Outcomes depend on bargaining frictions and fallback positions: impatience, breakdown risk, risk aversion, outside options, inside options, commitment tactics, and asymmetric information. These factors shift bargaining power by changing who can wait, who fears failure, and who has better alternatives. The logic assumes actors can rank outcomes and that these factors map into payoffs with reasonable stability.",
            ),
            (
                "4. Key Concepts and Terms",
                "- Bargaining situation: common gains plus conflict over terms.\n- Surplus: gains from cooperation above disagreement.\n- Impatience: cost of delay; patience raises bargaining power.\n- Outside option: payoff from leaving for another deal.\n- Inside option: payoff while bargaining continues without agreement.\n- Commitment tactic: costly signal that narrows room for concession.\n- Asymmetric information: one side knows something the other does not.",
            ),
            (
                "5. Micro Dynamics, Edge Cases, and Counterfactuals",
                "The theory weakens when bargaining is multilateral, when coercion or identity dominates material payoffs, or when institutions cap what strong actors can demand. A useful counterfactual is a setting with symmetric patience, transparent information, and low breakdown risk: Muthoo would predict faster agreement and a more even split. If public law or third-party guarantees improved weak actors' outside options, the distribution could shift sharply.",
            ),
            (
                "6. Empirical or Historical Evidence and Limitations",
                "Muthoo uses stylized cases rather than original data: house sales, labor disputes, coalition bargaining, trade negotiations, and war. These examples align well with the mechanism because they isolate surplus division and delay, but they do not adjudicate among rival explanations. Stronger confirmation would come from evidence linking variation in patience, options, or private information to measured bargaining outcomes.",
            ),
            (
                "7. Critical Assessment of Assumptions and Weaknesses",
                "The framework assumes negotiators are strategic and that bargaining power can be read off from costs, risk, and alternatives. That is analytically clean but often too narrow. It underplays norms, domestic legitimacy, coercion, and institutional veto players; it also treats many variables as exogenous when they are often politically produced. In real politics, actors often bargain over the rules, not just the surplus.",
            ),
            (
                "8. Connection to Contemporary News or Policy Debates",
                "Reuters' Jan. 27, 2026 account of U.S.-South Korea tariff bargaining fits the paper well: threats, delay, and disputed investment commitments are bargaining tools, not noise. Muthoo helps explain why time pressure and outside options matter so much. The theory struggles more when domestic politics alter what counts as an acceptable agreement, since negotiators may prefer audience approval to immediate economic efficiency.",
            ),
            (
                "9. One-Paragraph Mental Model",
                "Treat bargaining power like the ability to wait, walk away, or survive breakdown better than the other side. Muthoo is strongest when you need to explain delay, distribution, and leverage in a deal. Be skeptical when identities, institutions, or coercive asymmetries redefine the game more than patience and outside options do.",
            ),
        ],
    },
    {
        "slug": "lake-powell",
        "order": "Reading 4",
        "title": "International Relations: A Strategic-Choice Approach",
        "author": "David A. Lake and Robert Powell",
        "citation": "In Strategic Choice and International Relations (1999)",
        "sections": [
            (
                "1. Author Background and Political Context",
                "Lake and Powell are major international relations scholars working in the rationalist and political economy traditions. This 1999 chapter appears after the Cold War, when IR was saturated with paradigm fights among realism, liberalism, and constructivism. The chapter is agenda-setting: rather than offering one narrow theory, it proposes a research program that organizes IR around strategic interaction and microfoundations.",
            ),
            (
                "2. Big Picture (Macro Intuition)",
                "Their core complaint is that IR debates often revolve around labels instead of explaining concrete choices. They argue that the real object to explain is strategic interaction itself: actors choose while anticipating one another. Without this shift, the field keeps debating whether causes are domestic or systemic without seeing that many problems share the same strategic structure across those levels.",
            ),
            (
                "3. Core Theoretical Logic",
                "The framework starts with purposive actors embedded in environments defined by actions and information. Actors bring preferences and beliefs; environments shape what can be done and known. Analysis then asks how changing preferences, beliefs, actions, or information changes outcomes. This logic assumes purposiveness, analytic separation between actors and environments, and enough stability to infer how strategic settings aggregate into broader patterns.",
            ),
            (
                "4. Key Concepts and Terms",
                "- Strategic interaction: outcomes depend on mutually contingent choices.\n- Unit of analysis: the interaction, not a preselected actor.\n- Purposive action: actors pursue goals as best they can.\n- Preferences: ranking of outcomes.\n- Beliefs: expectations about others and uncertainty.\n- Information structure: what actors know or must infer.\n- Partial equilibrium: analyze one strategic setting without modeling everything at once.",
            ),
            (
                "5. Micro Dynamics, Edge Cases, and Counterfactuals",
                "The approach is most vulnerable when identities, norms, or institutions are endogenous to interaction rather than fixed inputs. A strong counterfactual is a constructivist setting in which actors' interests change through social interaction; then the strategic-choice framework only partially explains outcomes because preferences are no longer stable starting points. Likewise, if domestic fragmentation overwhelms purposive state action, predictions from a simple actor model can fail.",
            ),
            (
                "6. Empirical or Historical Evidence and Limitations",
                "This is a synthetic and programmatic chapter, not a single empirical test. Its evidence is intellectual: classic deterrence theory, the security dilemma, institutions, and international political economy are marshaled to show that a strategic-choice lens unifies scattered literatures. The limitation is obvious: the chapter demonstrates analytical reach more than empirical superiority.",
            ),
            (
                "7. Critical Assessment of Assumptions and Weaknesses",
                "The biggest assumption is that purposive action and stable preferences are good starting points. That often sharpens logic, but it can bracket precisely the processes constructivists care about: identity formation, norm internalization, and meaning. The framework also risks underestimating path dependence and power because it treats some background conditions as given when they are often products of prior domination.",
            ),
            (
                "8. Connection to Contemporary News or Policy Debates",
                "The reading is highly useful for current Taiwan deterrence debates. Reuters reported on March 20, 2026 that Taiwan's defense minister argued deterrence must raise the risks to Beijing; that is a textbook strategic-interaction claim about beliefs, capabilities, and expected responses. It also helps with NATO burden-sharing debates, where alliance politics can be read as recurring strategic problems rather than separate domestic and international stories.",
            ),
            (
                "9. One-Paragraph Mental Model",
                "Imagine IR as a board of linked strategic games rather than a contest between grand labels. Lake and Powell help you ask the right micro-level questions fast: who wants what, what can they do, what do they know, and how do expectations interact? Be skeptical when the board itself is socially constructed or rapidly changing.",
            ),
        ],
    },
]


def footer(c, page_num):
    c.setStrokeColor(BORDER_GREY)
    c.setLineWidth(0.4)
    c.line(MARGIN, MARGIN + FOOTER_H, PAGE_W - MARGIN, MARGIN + FOOTER_H)
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, MARGIN + 0.09 * inch, TITLE)
    page_label = str(page_num)
    w = stringWidth(page_label, "Helvetica", 8)
    c.drawString(PAGE_W - MARGIN - w, MARGIN + 0.09 * inch, page_label)


def draw_wrapped(c, text, x, y, width, font="Helvetica", size=7.2, leading=8.4, color=TEXT):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = []
    for raw in text.split("\n"):
        if raw.strip():
            lines.extend(simpleSplit(raw, font, size, width))
        else:
            lines.append("")
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_section(c, heading, body, x, y, width):
    y = draw_wrapped(c, heading, x, y, width, font="Helvetica-Bold", size=8.1, leading=9.0, color=DARK_NAVY)
    y -= 2
    if body.startswith("- "):
        for item in body.split("\n"):
            bullet_text = item[2:] if item.startswith("- ") else item
            lines = simpleSplit("- " + bullet_text, "Helvetica", 7.0, width)
            for line in lines:
                c.setFont("Helvetica", 7.0)
                c.setFillColor(TEXT)
                c.drawString(x, y, line)
                y -= 8.0
        y -= 3
        return y
    y = draw_wrapped(c, body, x, y, width, font="Helvetica", size=7.0, leading=8.0, color=TEXT)
    y -= 4
    return y


def draw_header(c, reading):
    c.setFillColor(MED_BLUE)
    c.rect(MARGIN, PAGE_H - MARGIN - HEADER_H, PAGE_W - 2 * MARGIN, HEADER_H, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN + 10, PAGE_H - MARGIN - 19, f"{reading['order']}  |  {reading['title']}")
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(MARGIN + 10, PAGE_H - MARGIN - 34, f"{reading['author']}  |  {reading['citation']}")


def draw_cover(c):
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(DARK_NAVY)
    c.drawString(MARGIN, PAGE_H - MARGIN - 8, TITLE)

    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT)
    c.drawString(MARGIN, PAGE_H - MARGIN - 28, f"{COURSE}  |  {TERM}")
    c.drawString(MARGIN, PAGE_H - MARGIN - 41, INSTRUCTOR)
    c.drawString(MARGIN, PAGE_H - MARGIN - 54, INSTITUTION)

    box_y = PAGE_H - MARGIN - 135
    box_h = 70
    c.setFillColor(LIGHT_GREY)
    c.setStrokeColor(BORDER_GREY)
    c.rect(MARGIN, box_y, PAGE_W - 2 * MARGIN, box_h, fill=1, stroke=1)
    desc = (
        "This reference manual summarizes all four readings in the folder using the user's requested nine-part macro-to-micro structure. "
        "Each reading receives exactly one page, with clickable navigation from this cover page and PDF outline bookmarks. "
        "Ordering is inferred from the Week 1 files: introductory strategy first, then sequential reasoning, bargaining theory, and finally the IR application."
    )
    draw_wrapped(c, desc, MARGIN + 10, box_y + box_h - 16, PAGE_W - 2 * MARGIN - 20, size=8.4, leading=10.0)

    toc_y = box_y - 24
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(DARK_NAVY)
    c.drawString(MARGIN, toc_y, "Table of Contents")
    toc_y -= 18

    for idx, reading in enumerate(READINGS, start=2):
        label = f"{reading['order']}: {reading['author']} - {reading['title']}"
        c.setFont("Helvetica", 9.2)
        c.setFillColor(MED_BLUE)
        c.drawString(MARGIN + 6, toc_y, label)
        link_w = stringWidth(label, "Helvetica", 9.2)
        c.linkAbsolute(
            "",
            reading["slug"],
            Rect=(MARGIN + 6, toc_y - 2, MARGIN + 6 + link_w, toc_y + 10),
            thickness=0,
        )
        c.setFillColor(MUTED)
        page_str = str(idx)
        c.drawRightString(PAGE_W - MARGIN, toc_y, page_str)
        toc_y -= 14

    foot_y = MARGIN + FOOTER_H + 18
    c.setStrokeColor(BORDER_GREY)
    c.setLineWidth(0.5)
    c.line(MARGIN, foot_y + 16, MARGIN + 120, foot_y + 16)
    footnote = (
        "Generated with Codex (GPT-5) as a study aid for Week 1 readings. "
        "Always verify against the assigned texts and official course materials. "
        "Instructor and institution fields were not recoverable from the source files."
    )
    draw_wrapped(c, footnote, MARGIN, foot_y + 8, PAGE_W - 2 * MARGIN, size=7.0, leading=8.2, color=MUTED)

    footer(c, 1)


def draw_reading_page(c, reading, page_num):
    c.bookmarkPage(reading["slug"])
    c.addOutlineEntry(f"{reading['order']}: {reading['author']}", reading["slug"], level=0)
    draw_header(c, reading)

    col_xs = [MARGIN, MARGIN + COL_W + GAP, MARGIN + 2 * (COL_W + GAP)]
    for idx, x in enumerate(col_xs):
        y = BODY_TOP
        for heading, body in reading["sections"][idx * 3:(idx + 1) * 3]:
            y = draw_section(c, heading, body, x, y, COL_W)
    footer(c, page_num)


def build(path):
    c = canvas.Canvas(path, pagesize=landscape(letter))
    c.setTitle(TITLE)
    draw_cover(c)
    c.showPage()
    for page_num, reading in enumerate(READINGS, start=2):
        draw_reading_page(c, reading, page_num)
        c.showPage()
    c.save()


if __name__ == "__main__":
    build("week1_strategic_readings_reference.pdf")
