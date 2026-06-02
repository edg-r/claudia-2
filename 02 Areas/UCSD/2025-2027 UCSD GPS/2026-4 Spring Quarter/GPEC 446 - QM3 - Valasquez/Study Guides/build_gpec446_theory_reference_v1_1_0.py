from pathlib import Path
from textwrap import wrap

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
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE = Path(__file__).resolve().parent
COURSE = BASE.parent
PROJECT = "gpec446_theory_reference_v1.1.0"
ASSET_DIR = BASE / "assets" / PROJECT
OUT = BASE / "GPEC446_theory_reference_v1.1.0.pdf"
NOTES = BASE / "GPEC446_theory_reference_v1.1.0_notes.md"
TITLE = "GPEC 446 Theory and Methods Reference"
MODEL = "GPT-5 Codex"

DARK = colors.HexColor("#1B2A4A")
BLUE = colors.HexColor("#2C5282")
GREEN = colors.HexColor("#EAF7EF")
AMBER = colors.HexColor("#FFF5E6")
LIGHT = colors.HexColor("#F6F7F9")
GREY = colors.HexColor("#5E6673")
BORDER = colors.HexColor("#C9D1D9")


class BookmarkAnchor(Flowable):
    def __init__(self, name, title=""):
        super().__init__()
        self.width = 0
        self.height = 0
        self.name = name
        self.title = title

    def draw(self):
        self.canv.bookmarkPage(self.name, fit="XYZ", left=0, top=self.canv._pagesize[1])
        if self.title:
            self.canv.addOutlineEntry(self.title, self.name, level=0)


def para(text, style):
    return Paragraph(text, style)


def bullets(items, style, bullet="bullet"):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=7) for i in items],
        bulletType=bullet,
        leftIndent=10,
        bulletFontSize=5,
        spaceBefore=0,
        spaceAfter=0,
    )


def font(size=28, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_wrapped(draw, text, xy, width, fnt, fill=(35, 45, 60), spacing=8):
    x, y = xy
    avg = max(fnt.getlength("abcdefghijklmnopqrstuvwxyz") / 26, 7)
    chars = max(int(width / avg), 12)
    for line in wrap(text, chars):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def arrow(draw, start, end, fill=(44, 82, 130), width=5):
    draw.line([start, end], fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    # Small triangular arrowhead, enough for these schematic assets.
    if abs(x2 - x1) >= abs(y2 - y1):
        sign = 1 if x2 > x1 else -1
        pts = [(x2, y2), (x2 - sign * 18, y2 - 10), (x2 - sign * 18, y2 + 10)]
    else:
        sign = 1 if y2 > y1 else -1
        pts = [(x2, y2), (x2 - 10, y2 - sign * 18), (x2 + 10, y2 - sign * 18)]
    draw.polygon(pts, fill=fill)


def box(draw, xy, text, fill=(245, 248, 252), outline=(44, 82, 130), text_fill=(25, 38, 65)):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=3)
    f = font(30, bold=True)
    lines = wrap(text, 16)
    total = len(lines) * 38
    y = y1 + ((y2 - y1) - total) / 2
    for line in lines:
        w = f.getlength(line)
        draw.text((x1 + ((x2 - x1) - w) / 2, y), line, font=f, fill=text_fill)
        y += 38


def save_diagram(unit):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / f"{unit['anchor']}.png"
    img = Image.new("RGB", (1400, 760), "white")
    draw = ImageDraw.Draw(img)
    title_font = font(34, bold=True)
    small = font(25)
    draw.rectangle((0, 0, 1400, 80), fill=(27, 42, 74))
    draw.text((42, 22), unit["image_title"], font=title_font, fill="white")
    kind = unit["image_kind"]

    if kind == "dag":
        positions = [(190, 210, 390, 330), (600, 210, 800, 330), (1010, 210, 1210, 330)]
        for xy, label in zip(positions, unit["labels"][:3]):
            box(draw, xy, label)
        arrow(draw, (390, 270), (600, 270))
        arrow(draw, (800, 270), (1010, 270))
        if len(unit["labels"]) > 3:
            box(draw, (600, 470, 800, 590), unit["labels"][3], fill=(255, 245, 230), outline=(198, 156, 63))
            arrow(draw, (700, 470), (700, 330), fill=(198, 156, 63))
        draw_wrapped(draw, unit["image_note"], (130, 635), 1140, small, fill=(70, 75, 85))

    elif kind == "timeline":
        y = 360
        draw.line((130, y, 1270, y), fill=(44, 82, 130), width=7)
        xs = [230, 520, 810, 1100]
        for x, label in zip(xs, unit["labels"]):
            draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(198, 156, 63))
            draw_wrapped(draw, label, (x - 95, y + 38), 190, small, fill=(25, 38, 65))
        if "Parallel" in unit["image_title"] or "Event" in unit["image_title"]:
            draw.line((210, 250, 1120, 190), fill=(52, 133, 89), width=5)
            draw.line((210, 500, 1120, 440), fill=(175, 80, 80), width=5)
        draw_wrapped(draw, unit["image_note"], (120, 620), 1160, small, fill=(70, 75, 85))

    elif kind == "equation":
        y = 175
        for label in unit["labels"]:
            box(draw, (155, y, 1245, y + 95), label, fill=(246, 247, 249), outline=(201, 209, 217))
            y += 125
        draw_wrapped(draw, unit["image_note"], (130, 635), 1140, small, fill=(70, 75, 85))

    elif kind == "cutoff":
        draw.line((140, 600, 1260, 600), fill=(80, 80, 80), width=3)
        draw.line((700, 130, 700, 635), fill=(198, 156, 63), width=5)
        draw.text((660, 640), "cutoff", font=small, fill=(120, 90, 30))
        draw.line((170, 500, 680, 420), fill=(44, 82, 130), width=6)
        draw.line((720, 300, 1230, 220), fill=(44, 82, 130), width=6)
        draw.ellipse((670, 410, 690, 430), fill=(44, 82, 130))
        draw.ellipse((710, 290, 730, 310), fill=(44, 82, 130))
        draw.text((545, 350), "local jump", font=font(32, bold=True), fill=(25, 38, 65))
        draw_wrapped(draw, unit["image_note"], (130, 635), 1140, small, fill=(70, 75, 85))

    elif kind == "support":
        draw.rectangle((180, 230, 1220, 520), fill=(246, 247, 249), outline=(201, 209, 217), width=3)
        draw.rectangle((350, 270, 780, 480), fill=(235, 247, 239), outline=(52, 133, 89), width=4)
        draw.rectangle((620, 270, 1050, 480), fill=(235, 244, 255), outline=(44, 82, 130), width=4)
        draw.text((440, 330), unit["labels"][0], font=font(32, bold=True), fill=(52, 133, 89))
        draw.text((730, 390), unit["labels"][1], font=font(32, bold=True), fill=(44, 82, 130))
        draw.text((620, 535), unit["labels"][2], font=font(28, bold=True), fill=(25, 38, 65))
        draw_wrapped(draw, unit["image_note"], (130, 635), 1140, small, fill=(70, 75, 85))

    else:
        x = 160
        for label in unit["labels"]:
            box(draw, (x, 250, x + 240, 390), label)
            x += 310
        draw_wrapped(draw, unit["image_note"], (130, 635), 1140, small, fill=(70, 75, 85))

    img.save(path)
    return path


UNITS = [
    {
        "anchor": "identification",
        "week": "Week 1",
        "title": "Causal Inference and Identification",
        "reading": "Angrist & Pischke, Ch. 1; QM3 L1",
        "image_kind": "dag",
        "image_title": "Identification = comparison plus assumption",
        "labels": ["Policy", "Outcome", "Causal claim", "Missing counterfactual"],
        "image_note": "The causal claim is stronger than the observed policy-outcome association because it needs a credible substitute for the missing counterfactual.",
        "situation": "A social program is followed by higher schooling, but Edgar must decide whether the comparison reveals the program's effect or just who selected into it.",
        "intuition": "Causal inference in QM3 is a design problem before it is a calculation problem. A policy effect compares what happened under treatment with what would have happened to the same unit without treatment. Because one potential outcome is missing, each method in the course is a different strategy for making the observed comparison stand in for that missing world.",
        "terms": ["<b>Counterfactual</b> - the unobserved outcome a unit would have had under the other treatment state.", "<b>Identification</b> - the logic that lets an observed comparison recover a causal quantity.", "<b>Estimand</b> - the target effect, such as ATE, ATT, ITT, or LATE.", "<b>Research design</b> - the source of variation that makes treatment plausibly exogenous."],
        "assumptions": ["The comparison group represents the missing counterfactual.", "Treatment status or timing is not chosen because of unobserved potential outcomes.", "Outcomes and treatment are measured consistently across units.", "No spillovers alter other units' outcomes unless the design models them."],
        "strengths": ["Forces every empirical claim to name the comparison and assumption.", "Connects all later methods under one counterfactual language.", "Keeps significance and causal identification conceptually separate."],
        "limits": ["Cannot by itself prove an assumption is true.", "Requires detailed institutional knowledge of assignment, timing, or eligibility.", "A large dataset can still estimate a biased comparison precisely."],
        "refs": ["Angrist & Pischke (2014, Ch. 1)", "QM3 Lecture 1"],
    },
    {
        "anchor": "potential_outcomes",
        "week": "Week 2",
        "title": "Potential Outcomes, ATE, ATT, and Selection",
        "reading": "Angrist & Pischke, Ch. 1; QM3 L2",
        "image_kind": "equation",
        "image_title": "Observed difference = effect plus selection",
        "labels": ["Y_i = D_i Y_i(1) + (1-D_i)Y_i(0)", "ATE = E[Y_i(1)-Y_i(0)]", "Naive gap = ATT + selection bias"],
        "image_note": "The equation separates the causal effect from pre-existing treated-control differences in untreated potential outcomes.",
        "situation": "Program participants earn more than nonparticipants, but they may have earned more even without the program.",
        "intuition": "The potential-outcomes framework says each unit has Y(1) and Y(0), but only one is observed. The naive treated-control gap is therefore not automatically a treatment effect. It equals an effect for treated units plus a selection term if treated and untreated people differ in their untreated potential outcomes.",
        "terms": ["<b>ATE</b> - average effect for the whole population.", "<b>ATT</b> - average effect among treated units.", "<b>Selection bias</b> - difference in untreated potential outcomes between treated and control groups.", "<b>SUTVA</b> - no interference and stable treatment versions.", "<b>ITT</b> - effect of assignment or eligibility rather than receipt."],
        "assumptions": ["To read the raw gap as causal, treatment must be independent of potential outcomes.", "The untreated control outcome must represent treated units' missing untreated outcome.", "Treatment has the same meaning across units.", "Spillovers are absent or explicitly part of the estimand."],
        "strengths": ["Gives precise language for what is observed and missing.", "Prevents confusing a descriptive group gap with a causal effect.", "Handles heterogeneity by distinguishing ATE, ATT, ITT, and LATE."],
        "limits": ["The framework names the missing data problem but does not solve it alone.", "Different estimands can diverge sharply with heterogeneous effects.", "Take-up problems require extra care before scaling ITT to TOT."],
        "refs": ["Angrist & Pischke (2014, Ch. 1)", "QM3 Lecture 2"],
    },
    {
        "anchor": "randomization",
        "week": "Week 1 / Week 8",
        "title": "Random Assignment, Blocking, and ITT",
        "reading": "Gerber & Green, Ch. 3; QM3 Lab 1",
        "image_kind": "timeline",
        "image_title": "Randomization creates balance in expectation",
        "labels": ["Baseline", "Random assign", "Treatment", "Outcome"],
        "image_note": "The design separates treatment assignment from potential outcomes; blocking improves precision by randomizing within meaningful strata.",
        "situation": "A lottery assigns households to receive a program offer, making the offer group comparable to the control group in expectation.",
        "intuition": "Randomization solves selection by assigning treatment independently of potential outcomes. Blocking or stratification randomizes within baseline groups, which can improve precision when those groups predict outcomes. When compliance is imperfect, the clean randomized contrast is the ITT: the effect of assignment, offer, or eligibility.",
        "terms": ["<b>Random assignment</b> - treatment status is assigned by a chance mechanism.", "<b>Balance</b> - treatment and control groups have similar baseline covariates in expectation.", "<b>Blocking</b> - randomize within pre-treatment strata.", "<b>ITT</b> - effect of being assigned or offered treatment.", "<b>Power</b> - probability of detecting an effect of a given size."],
        "assumptions": ["The randomization protocol is followed.", "Attrition is not differential in a way related to potential outcomes.", "There is no interference across assigned groups.", "Blocking variables are measured before treatment."],
        "strengths": ["Most transparent solution to selection bias.", "Simple difference in means is design-based and easy to explain.", "Blocking can reduce variance and reassure readers about subgroup balance."],
        "limits": ["External validity may be narrow.", "Noncompliance changes the estimand from receipt to assignment.", "Attrition and spillovers can erode the clean design."],
        "refs": ["Gerber & Green (2012, Ch. 3)", "QM3 Lab 1"],
    },
    {
        "anchor": "ols_cia",
        "week": "Week 2",
        "title": "OLS, Controls, CIA, and Common Support",
        "reading": "Angrist & Pischke, Ch. 2; QM3 L3-L4",
        "image_kind": "support",
        "image_title": "Selection on observables needs overlap",
        "labels": ["Controls", "Treated", "Common support"],
        "image_note": "Regression and matching compare like with like only where treated and untreated units both exist at similar covariate values.",
        "situation": "To estimate returns to college type, compare students with similar observed applications, scores, and backgrounds.",
        "intuition": "OLS with controls is a conditional comparison. The coefficient on treatment compares treated and untreated units with the same included covariates in the model's linear structure. This becomes causal only under the Conditional Independence Assumption (CIA): after conditioning on observed X, treatment is as good as random. Common support adds that the like-for-like comparison actually exists in the data.",
        "terms": ["<b>OLS</b> - linear projection that minimizes squared residuals.", "<b>CIA</b> - potential outcomes are independent of treatment conditional on observed covariates.", "<b>Common support</b> - every relevant X value has both treated and control observations.", "<b>Interaction</b> - allows an effect or slope to vary by group.", "<b>Demeaning</b> - centers a variable so coefficients are evaluated at a meaningful baseline."],
        "assumptions": ["All confounders are observed and correctly conditioned on.", "Controls are pre-treatment.", "Treated/control overlap is adequate.", "The functional form does not create misleading extrapolation."],
        "strengths": ["Uses observational data when experiments are unavailable.", "Makes comparisons more credible than raw mean gaps when rich pre-treatment X exists.", "Interactions clarify heterogeneous effects."],
        "limits": ["Unobserved confounding remains the central weakness.", "Adding many controls does not prove CIA.", "Poor support makes estimates model-driven rather than comparison-driven."],
        "refs": ["Angrist & Pischke (2014, Ch. 2)", "QM3 Lectures 3-4"],
    },
    {
        "anchor": "ovb",
        "week": "Week 3",
        "title": "OVB, Bad Controls, and Simultaneity",
        "reading": "QM3 L4-L5; exercise notation",
        "image_kind": "dag",
        "image_title": "Omitted confounders travel through the error term",
        "labels": ["Treatment X", "Outcome Y", "Estimate", "Omitted W"],
        "image_note": "Bias appears when W affects Y and is correlated with X; bad controls are downstream variables that should not be conditioned on.",
        "situation": "Schooling may predict wages partly because ability affects both schooling choices and earnings.",
        "intuition": "OVB gives the sign and size logic for why a short regression is biased. The short coefficient equals the causal effect plus the omitted variable's effect on Y times the omitted variable's relationship with X. Simultaneity is a related endogeneity problem where X and Y determine each other, as in policing and crime.",
        "terms": ["<b>Short regression</b> - excludes the confounder.", "<b>Long regression</b> - includes the confounder.", "<b>Bias</b> - beta_short minus beta_long.", "<b>Bad control</b> - post-treatment or collider variable.", "<b>Simultaneity</b> - reverse or joint causality between X and Y."],
        "assumptions": ["The omitted variable is pre-treatment and correlated with X.", "The omitted variable affects Y after controlling for X.", "The bias formula uses the correct causal ordering.", "A valid design is needed when simultaneity drives endogeneity."],
        "strengths": ["Excellent diagnostic for sign-of-bias questions.", "Professor's Cov/Var notation makes bias arithmetic explicit.", "Clarifies why controls must be chosen conceptually."],
        "limits": ["Hard to quantify without data on the omitted variable.", "Does not solve endogeneity by itself.", "Bad controls can introduce bias even in randomized settings."],
        "refs": ["QM3 Lectures 4-5", "Valasquez exercise handouts"],
    },
    {
        "anchor": "matching",
        "week": "Week 6",
        "title": "Matching and Propensity Scores",
        "reading": "Syllabus Week 6 additional readings; QM3 concept notes",
        "image_kind": "support",
        "image_title": "Matching trims comparison to credible overlap",
        "labels": ["Matched controls", "Treated units", "Overlap region"],
        "image_note": "The method works by comparing treated units to observationally similar untreated units, so CIA and support carry the identification burden.",
        "situation": "Compare treated job-training participants to nonparticipants with similar age, prior earnings, education, and employment histories.",
        "intuition": "Matching makes the selection-on-observables logic visible. Instead of relying only on a regression functional form, it constructs a comparison group that resembles treated units on observed pre-treatment covariates. Propensity-score matching compresses many covariates into the probability of treatment given X, but the causal claim remains CIA plus common support.",
        "terms": ["<b>Exact/nearest-neighbor matching</b> - pairs treated units with similar controls.", "<b>Propensity score</b> - P(D=1|X).", "<b>Balance</b> - matched treated and control groups look similar on X.", "<b>Caliper</b> - maximum allowed matching distance.", "<b>ATT focus</b> - many matching designs estimate effects for treated units with matches."],
        "assumptions": ["Selection is fully captured by observed covariates.", "Common support exists after matching.", "Covariates are pre-treatment.", "Balance diagnostics are satisfactory after matching."],
        "strengths": ["Transparent about which observations are comparable.", "Reduces extrapolation relative to a broad regression.", "Balance tables make the design easier to audit."],
        "limits": ["Cannot fix unobserved confounding.", "Results can depend on matching algorithm and trimming choices.", "Poor support means some treated units have no credible comparison."],
        "refs": ["GPEC 446 syllabus Week 6", "Tyche concept notes"],
    },
    {
        "anchor": "iv",
        "week": "Week 3",
        "title": "Instrumental Variables, Wald, and 2SLS",
        "reading": "Angrist & Pischke, Ch. 3; QM3 L5",
        "image_kind": "dag",
        "image_title": "IV isolates treatment variation from an instrument",
        "labels": ["Instrument Z", "Treatment D", "Outcome Y", "Confounder U"],
        "image_note": "Z must shift D but affect Y only through D; U may confound D and Y, but must not be related to Z.",
        "situation": "A school voucher lottery affects attendance at private school, and attendance affects achievement.",
        "intuition": "IV is for treatment variables contaminated by endogeneity. A valid instrument creates variation in treatment that is unrelated to unobserved potential outcomes. The Wald estimator divides the reduced-form effect of the instrument on the outcome by the first-stage effect of the instrument on treatment. 2SLS generalizes that logic with regression.",
        "terms": ["<b>Instrument</b> - variable that shifts treatment but is otherwise exogenous.", "<b>First stage</b> - effect of Z on D.", "<b>Reduced form</b> - effect of Z on Y.", "<b>Wald estimator</b> - reduced form divided by first stage.", "<b>2SLS</b> - predicts D using Z, then regresses Y on predicted D."],
        "assumptions": ["Relevance: Z changes D.", "Independence: Z is as-good-as-random.", "Exclusion: Z affects Y only through D.", "No weak instrument problem; first stage is strong enough."],
        "strengths": ["Targets a causal effect when treatment is endogenous.", "Works well with lotteries, eligibility rules, distance, or policy shocks.", "Wald form is intuitive for binary instruments."],
        "limits": ["Exclusion is often untestable.", "Weak instruments create biased and unstable estimates.", "The estimand is often local, not the full ATE."],
        "refs": ["Angrist & Pischke (2014, Ch. 3)", "QM3 Lecture 5"],
    },
    {
        "anchor": "late",
        "week": "Week 3",
        "title": "LATE, Compliance Types, and AIR Assumptions",
        "reading": "Angrist & Imbens; Angrist & Pischke, Ch. 3; QM3 L6",
        "image_kind": "equation",
        "image_title": "IV identifies the effect for compliers",
        "labels": ["Compliers: D(1)=1, D(0)=0", "Always-takers / never-takers: not moved by Z", "LATE = E[Y(1)-Y(0) | complier]"],
        "image_note": "The instrument reveals causal effects only for people whose treatment status changes because of the instrument.",
        "situation": "PACES voucher offers affect schooling only for students who attend private school if offered and do not if not offered.",
        "intuition": "The Angrist-Imbens-Rubin LATE framework explains what IV estimates when treatment effects vary and compliance is imperfect. Under independence, relevance, exclusion, and monotonicity, the Wald/IV coefficient is the Local Average Treatment Effect for compliers. Always-takers and never-takers help determine the first stage but do not reveal treatment effects because their treatment status is unchanged by the instrument.",
        "terms": ["<b>Complier</b> - takes treatment only when encouraged.", "<b>Always-taker</b> - takes treatment regardless of Z.", "<b>Never-taker</b> - never takes treatment.", "<b>Defier</b> - does the opposite of assignment.", "<b>Monotonicity</b> - rules out defiers."],
        "assumptions": ["Instrument is independent of potential outcomes and compliance types.", "First stage is nonzero.", "Exclusion restriction holds.", "Monotonicity: no defiers."],
        "strengths": ["Clarifies IV's real estimand under heterogeneity.", "Prevents overclaiming ATE when only compliers are moved.", "Gives precise language for incomplete take-up."],
        "limits": ["LATE may not generalize to always-takers, never-takers, or policy expansions.", "Compliance types are latent.", "Monotonicity and exclusion remain substantive assumptions."],
        "refs": ["Angrist et al. (1996)", "Angrist & Pischke (2014, Ch. 3)", "QM3 Lecture 6"],
    },
    {
        "anchor": "panel_fe",
        "week": "Week 4",
        "title": "Panel Data, First Differences, and Fixed Effects",
        "reading": "Wooldridge, Ch. 13; QM3 L7-L8",
        "image_kind": "timeline",
        "image_title": "Panel methods remove time-invariant unit traits",
        "labels": ["Unit i pre", "Unit i post", "Within change", "Compare changes"],
        "image_note": "FE and first differences use within-unit variation, removing stable confounders such as geography, culture, or baseline ability.",
        "situation": "Compare each country to itself before and after a governance change rather than comparing rich and poor countries in levels.",
        "intuition": "Panel data follow the same units over time. Fixed effects absorb all time-invariant unit differences, while time fixed effects absorb shocks common to all units in a period. First differences subtract each unit's prior outcome from its later outcome. In two periods, first differences and unit fixed effects are closely linked; both shift the design from cross-sectional levels to within-unit changes.",
        "terms": ["<b>Unit fixed effect</b> - absorbs stable unit-specific factors.", "<b>Time fixed effect</b> - absorbs common shocks by period.", "<b>First difference</b> - changes Y and X over time.", "<b>Within estimator</b> - uses deviations from unit means.", "<b>TWFE</b> - includes both unit and time fixed effects."],
        "assumptions": ["Unobserved confounders are time-invariant or controlled by period effects.", "Treatment timing is not driven by time-varying omitted shocks.", "Sufficient within-unit variation exists.", "Standard errors account for within-unit dependence."],
        "strengths": ["Controls for all stable unit characteristics without measuring them.", "Natural bridge to DiD.", "Useful for country, school, person, or state panels."],
        "limits": ["Cannot remove time-varying confounders.", "FE estimates can be noisy if little within variation exists.", "Lagged outcomes and dynamic treatment timing require care."],
        "refs": ["Wooldridge (2020, Ch. 13)", "QM3 Lectures 7-8"],
    },
    {
        "anchor": "did",
        "week": "Week 4",
        "title": "Two-Period Difference-in-Differences",
        "reading": "Angrist & Pischke, Ch. 5; QM3 L7-L8",
        "image_kind": "timeline",
        "image_title": "Parallel trends supply the untreated counterfactual",
        "labels": ["Pre", "Post", "Treated change", "Control change"],
        "image_note": "DiD subtracts the control group's trend from the treated group's trend; the key assumption is parallel untreated trends.",
        "situation": "A road-repair program starts in treated towns, and controls provide the trend treated towns would have followed absent repair.",
        "intuition": "DiD compares changes over time rather than levels. The four-number estimator is the treated group's post-pre change minus the control group's post-pre change. The treatment effect is the interaction coefficient in a treated-by-post regression. DiD permits permanent level differences between groups; what it needs is that untreated trends would have moved in parallel.",
        "terms": ["<b>Parallel trends</b> - treated and controls would have had equal untreated outcome changes.", "<b>Post</b> - period after treatment starts.", "<b>Treated x Post</b> - DiD interaction and treatment effect.", "<b>No anticipation</b> - units do not change behavior before treatment because of future treatment.", "<b>Common shocks</b> - time effects shared by both groups."],
        "assumptions": ["Parallel trends in untreated potential outcomes.", "No anticipation before treatment.", "Composition of groups is stable over time.", "No group-specific shocks coincide with treatment."],
        "strengths": ["Simple and memorable four-number logic.", "Controls for fixed group differences and common time shocks.", "Pre-trend plots can make the assumption more credible."],
        "limits": ["Parallel trends is not directly testable.", "Differential shocks can mimic treatment effects.", "Serial correlation and few clusters complicate inference."],
        "refs": ["Angrist & Pischke (2014, Ch. 5)", "QM3 Lectures 7-8"],
    },
    {
        "anchor": "event_study",
        "week": "Week 5",
        "title": "Event Studies and Staggered Adoption",
        "reading": "Wooldridge, Ch. 14; QM3 L9",
        "image_kind": "timeline",
        "image_title": "Event time checks pre-trends and dynamics",
        "labels": ["Lead -2", "Lead -1 omitted", "Event 0", "Lags +1,+2"],
        "image_note": "Leads diagnose whether treated units were already diverging before treatment; lags trace dynamic effects after treatment.",
        "situation": "States adopt a policy in different years, so event time aligns them relative to adoption rather than calendar year.",
        "intuition": "Event studies extend DiD by estimating coefficients for periods before and after treatment. Pre-treatment leads should be close to zero if parallel trends is plausible. Post-treatment lags show whether effects grow, fade, or persist. With staggered adoption, naive TWFE can mix clean comparisons with already-treated units used as controls, creating Goodman-Bacon weighting problems when effects are heterogeneous.",
        "terms": ["<b>Lead</b> - event-study coefficient before treatment.", "<b>Lag</b> - coefficient after treatment.", "<b>Omitted period</b> - reference event time, often -1.", "<b>Staggered adoption</b> - units start treatment in different periods.", "<b>Goodman-Bacon decomposition</b> - TWFE as weighted two-by-two DiD comparisons."],
        "assumptions": ["No pre-trend in untreated potential outcomes.", "No anticipation.", "Comparison groups are not already contaminated by treatment.", "Heterogeneous effects are handled with appropriate estimators or interpretation."],
        "strengths": ["Visual diagnostic for credibility.", "Shows dynamic treatment effects.", "Clarifies timing and anticipation problems."],
        "limits": ["Insignificant pre-trends do not prove parallel trends.", "TWFE can be biased under heterogeneous effects and staggered timing.", "Event-study bins and omitted period choices affect presentation."],
        "refs": ["Wooldridge (2020, Ch. 14)", "Goodman-Bacon (2021)", "QM3 Lecture 9"],
    },
    {
        "anchor": "ddd_continuous",
        "week": "Week 5",
        "title": "DDD, Continuous-Treatment DiD, and Falsification",
        "reading": "QM3 L10",
        "image_kind": "equation",
        "image_title": "Triple differences subtract one more comparison",
        "labels": ["DiD among affected group", "minus DiD among placebo group", "DDD removes shared group-time confounding"],
        "image_note": "DDD adds a third comparison dimension; falsification tests ask whether the design finds effects where none should exist.",
        "situation": "A policy should affect young workers but not older workers, so older workers provide a placebo difference-in-differences.",
        "intuition": "Triple differences add a third dimension to remove confounding that affects treated and control units differently over time but similarly across a placebo group. Continuous-treatment DiD replaces a binary policy switch with treatment intensity. Falsification tests, placebo outcomes, placebo groups, and pre-period fake treatments probe whether the design is detecting the hypothesized mechanism or a broader shock.",
        "terms": ["<b>DDD</b> - difference of two DiD estimates.", "<b>Placebo group</b> - group that should not respond to treatment.", "<b>Continuous treatment</b> - dose or intensity rather than 0/1 policy.", "<b>Falsification test</b> - checks for effects where theory predicts none.", "<b>Threats to DiD</b> - differential shocks, composition changes, anticipation, spillovers."],
        "assumptions": ["The third-difference group captures the confounding trend but is not treated by the mechanism.", "Treatment intensity is not driven by unobserved outcome shocks.", "Placebo tests are linked to the actual theory of change.", "Spillovers across comparison dimensions are limited."],
        "strengths": ["Useful when simple parallel trends is implausible.", "Falsification tests sharpen the causal story.", "Continuous treatment captures policy dose variation."],
        "limits": ["DDD assumptions are harder to explain and verify.", "Placebo success does not prove the main assumption.", "Continuous DiD may require stronger functional-form assumptions."],
        "refs": ["QM3 Lecture 10", "Tyche panel-data notes"],
    },
    {
        "anchor": "synthetic_control",
        "week": "Week 6",
        "title": "Synthetic Control",
        "reading": "Syllabus Week 6 additional readings; Abadie et al.",
        "image_kind": "timeline",
        "image_title": "Synthetic control builds a weighted counterfactual",
        "labels": ["Pre-period fit", "Treatment", "Treated path", "Synthetic path"],
        "image_note": "Weights are chosen to match the treated unit before treatment; post-treatment divergence is interpreted as the effect.",
        "situation": "Estimate the effect of a state policy by comparing the treated state to a weighted combination of untreated states that matched it pre-policy.",
        "intuition": "Synthetic control is a transparent case-study design for one or a few treated units. It constructs a weighted average of untreated units that closely tracks the treated unit before treatment. If the pre-treatment fit is strong and no untreated donor is affected by the policy, the post-treatment gap between the treated unit and its synthetic counterpart estimates the treatment effect.",
        "terms": ["<b>Donor pool</b> - untreated units available to construct the synthetic control.", "<b>Weights</b> - nonnegative contributions from donor units.", "<b>Pre-treatment fit</b> - how well the synthetic unit matches before treatment.", "<b>Placebo tests</b> - apply the method to untreated units.", "<b>Post-treatment gap</b> - treated outcome minus synthetic outcome after treatment."],
        "assumptions": ["A weighted combination of donors can approximate the treated unit's untreated path.", "No donor units are contaminated by spillovers.", "No simultaneous shock hits only the treated unit at treatment time.", "Pre-treatment fit is strong over relevant predictors and outcomes."],
        "strengths": ["Excellent visual counterfactual for policy case studies.", "Less reliant on parametric regression form.", "Placebo tests are intuitive."],
        "limits": ["Weak pre-fit undermines credibility.", "Requires enough suitable donor units.", "Inference is less standard than in large-sample regressions."],
        "refs": ["Abadie et al. (2010)", "GPEC 446 syllabus Week 6"],
    },
    {
        "anchor": "rdd",
        "week": "Week 7",
        "title": "Regression Discontinuity Design",
        "reading": "Angrist & Pischke, Ch. 4; QM3 Lab 6",
        "image_kind": "cutoff",
        "image_title": "RDD estimates the jump at a cutoff",
        "labels": ["Running variable", "Cutoff", "Jump"],
        "image_note": "Units just above and below the threshold are assumed comparable except for treatment probability.",
        "situation": "Class-size rules or school-enrollment thresholds assign treatment when enrollment crosses a cutoff.",
        "intuition": "RDD exploits a rule that changes treatment at a known threshold of a running variable. Near the cutoff, units on either side are assumed similar except for treatment status. Sharp RDD has treatment jump from 0 to 1; fuzzy RDD has a discontinuous increase in treatment probability and uses the cutoff as an instrument.",
        "terms": ["<b>Running variable</b> - score or forcing variable that determines eligibility.", "<b>Cutoff</b> - threshold where assignment changes.", "<b>Continuity</b> - potential outcomes evolve smoothly through the cutoff absent treatment.", "<b>Bandwidth</b> - local window around the cutoff.", "<b>McCrary/density test</b> - checks sorting around the cutoff."],
        "assumptions": ["Potential outcomes are continuous at the cutoff.", "Units cannot precisely manipulate the running variable.", "The model is local to the cutoff.", "No other policy changes exactly at the same threshold."],
        "strengths": ["Highly credible local design when rules are strict.", "Graphical diagnostics are intuitive.", "Fuzzy RDD connects cleanly to IV."],
        "limits": ["Estimates are local to units near the cutoff.", "Bandwidth and polynomial choices matter.", "Manipulation or bunching near the cutoff threatens validity."],
        "refs": ["Angrist & Pischke (2014, Ch. 4)", "QM3 Lab 6"],
    },
    {
        "anchor": "experiments2",
        "week": "Week 9",
        "title": "Covariate Adjustment, ANCOVA, and Noncompliance",
        "reading": "Gerber & Green, Ch. 4; QM3 Lab 7",
        "image_kind": "equation",
        "image_title": "Adjustment improves precision after randomization",
        "labels": ["Y = alpha + tau D + gamma X + e", "Interacted ANCOVA: D*(X - mean X)", "Noncompliance: assignment effect vs receipt effect"],
        "image_note": "Covariates are not needed for unbiasedness in a clean experiment, but pre-treatment prognostic covariates can improve precision.",
        "situation": "A field experiment randomizes outreach, but baseline turnout history strongly predicts the outcome and some assigned people do not comply.",
        "intuition": "In randomized experiments, covariate adjustment is mainly about precision, not identification. Pre-treatment covariates that predict outcomes can reduce residual variance. Gerber and Green emphasize careful adjustment, blocking, and interpretation under noncompliance. Interacted ANCOVA with demeaned covariates is safer when treatment effects vary because it lets covariate-outcome relationships differ by treatment arm.",
        "terms": ["<b>Prognostic covariate</b> - baseline variable predictive of the outcome.", "<b>ANCOVA</b> - post-treatment outcome regressed on treatment and baseline covariates.", "<b>Interacted adjustment</b> - treatment interacted with centered covariates.", "<b>Noncompliance</b> - assigned status differs from received treatment.", "<b>Power gain</b> - smaller standard errors from explaining outcome variation."],
        "assumptions": ["Covariates are measured before treatment.", "Random assignment remains the source of identification.", "Attrition and noncompliance are addressed with ITT or IV logic.", "Interactions are included when heterogeneity makes simple adjustment risky."],
        "strengths": ["Improves precision without changing the core randomized design.", "Clarifies assignment versus receipt effects.", "Connects experiments to IV when assignment encourages take-up."],
        "limits": ["Post-treatment covariates create bias.", "Small samples can make adjustment fragile.", "Treatment-on-treated effects need stronger assumptions than ITT."],
        "refs": ["Gerber & Green (2012, Ch. 4)", "QM3 Lab 7"],
    },
    {
        "anchor": "time_series",
        "week": "Week 10",
        "title": "Time Series, Lags, Stationarity, and Unit Roots",
        "reading": "Wooldridge, Ch. 10-11",
        "image_kind": "timeline",
        "image_title": "Time-series regression depends on persistence",
        "labels": ["Z_t", "Z_t-1", "Y_t", "Long-run effect"],
        "image_note": "Lag models trace dynamic effects, but unit roots and serial dependence can make ordinary regression misleading.",
        "situation": "Estimate how monetary policy or GDP shocks affect outcomes over several periods, not just immediately.",
        "intuition": "Time-series data are ordered and dependent. Finite distributed lag models separate immediate and delayed effects; the long-run propensity sums lag coefficients. Valid OLS needs an exogeneity condition appropriate to time, weak dependence, and often stationarity. Unit roots break those conditions and can produce spurious regressions unless the series are differenced or otherwise modeled correctly.",
        "terms": ["<b>FDL model</b> - includes current and lagged values of X.", "<b>Impact propensity</b> - immediate effect.", "<b>Long-run propensity</b> - sum of lag effects.", "<b>Strict exogeneity</b> - errors unrelated to regressors in all time periods.", "<b>Unit root</b> - nonstationary process with persistent shocks."],
        "assumptions": ["The relevant exogeneity condition holds for the regressors.", "Series are stationary or transformed appropriately.", "Weak dependence allows large-sample approximations.", "Serial correlation is handled in inference."],
        "strengths": ["Captures delayed policy effects.", "Separates short-run and long-run responses.", "Gives diagnostics for spurious correlations in trending data."],
        "limits": ["Unit roots can make regressions look significant when unrelated.", "Feedback and lagged dependent variables weaken strict exogeneity.", "Small time-series samples are fragile."],
        "refs": ["Wooldridge (2020, Chs. 10-11)", "Tyche concept notes"],
    },
]


REFERENCES = [
    "Abadie, A., Diamond, A., & Hainmueller, J. (2010). Synthetic control methods for comparative case studies: Estimating the effect of California's tobacco control program. <i>Journal of the American Statistical Association, 105</i>(490), 493-505.",
    "Angrist, J. D., Imbens, G. W., & Rubin, D. B. (1996). Identification of causal effects using instrumental variables. <i>Journal of the American Statistical Association, 91</i>(434), 444-455.",
    "Angrist, J. D., & Pischke, J.-S. (2014). <i>Mastering 'metrics: The path from cause to effect</i>. Princeton University Press.",
    "Gerber, A. S., & Green, D. P. (2012). <i>Field experiments: Design, analysis, and interpretation</i>. W. W. Norton.",
    "Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment timing. <i>Journal of Econometrics, 225</i>(2), 254-277.",
    "Wooldridge, J. M. (2020). <i>Introductory econometrics: A modern approach</i> (7th ed.). Cengage Learning.",
]


DEEP_SNAPSHOTS = {
    "identification": {
        "estimand": "Usually ATE/ATT/ITT; first name the population and treatment contrast before choosing a method.",
        "id_logic": "Observed comparison + design assumption = credible stand-in for the missing potential outcome.",
        "readout": "Ask: who supplies Y(0) for treated units, and why would they have followed the same outcome path?",
        "diagnostics": "Assignment rule audit; balance or pre-trend checks when available; placebo outcomes/groups; institutional timing story.",
        "fails": "If the comparison group is selected on unobserved potential outcomes, precision only makes the wrong contrast sharper.",
        "interpretation": "Do not say 'causal' until the estimand, comparison, and identifying assumption are all explicit.",
        "example": "Bono Familias / schooling: raw participant gains are not causal unless nonparticipants proxy the treated counterfactual.",
    },
    "potential_outcomes": {
        "estimand": "ATE = population mean effect; ATT = effect for treated; ITT = effect of assignment; TOT/LATE for takers/compliers.",
        "id_logic": "Decompose the observed treated-control gap into causal effect plus selection in untreated potential outcomes.",
        "readout": "Naive gap = E[Y(1)|D=1] - E[Y(0)|D=0]; causal only if the missing E[Y(0)|D=1] is recovered.",
        "diagnostics": "Baseline covariate imbalance; attrition by treatment status; spillover checks; estimand clarity under heterogeneous effects.",
        "fails": "Selection bias appears when treated units would have had different Y(0) even without treatment.",
        "interpretation": "State whose effect is being estimated; heterogeneous effects make ATE, ATT, ITT, and LATE non-interchangeable.",
        "example": "PACES voucher: offer, take-up, and attendance produce different causal quantities.",
    },
    "randomization": {
        "estimand": "Difference in mean potential outcomes under assignment; with noncompliance, the design first identifies ITT.",
        "id_logic": "Random assignment makes D independent of potential outcomes in expectation, so controls reveal the missing counterfactual.",
        "readout": "Simple mean difference estimates the assignment effect; blocking changes precision, not the core estimand.",
        "diagnostics": "Randomization record; baseline balance; attrition table; compliance/take-up rates; cluster structure for SEs.",
        "fails": "Differential attrition, spillovers, or protocol violations break the clean assignment-to-outcome comparison.",
        "interpretation": "Report ITT as the policy-relevant offer/eligibility effect unless extra assumptions justify receipt effects.",
        "example": "Week 1 lottery exercise: an 11 pp offer effect with 65% take-up is ITT, not the effect on takers.",
    },
    "ols_cia": {
        "estimand": "Conditional ATE/ATT inside the covariate support represented in the sample and model.",
        "id_logic": "After conditioning on pre-treatment X, treatment is as-good-as-random within comparable covariate cells.",
        "readout": "The coefficient is a weighted conditional comparison, not magic deconfounding by adding variables.",
        "diagnostics": "Support/overlap plots; covariate balance; sensitivity to controls; functional-form checks; leverage/outlier review.",
        "fails": "Unobserved confounders, bad controls, or extrapolated cells turn the regression coefficient into a model artifact.",
        "interpretation": "Say 'conditional association' unless CIA and support are defended with substantive design knowledge.",
        "example": "Dale-Krueger-style college comparisons: applicants with similar admissions sets make the comparison more plausible.",
    },
    "ovb": {
        "estimand": "Difference between short-regression coefficient and the coefficient that would hold after valid confounder adjustment.",
        "id_logic": "Bias needs two links: omitted W affects Y, and W is correlated with X.",
        "readout": "Professor notation: c1 = Cov(Y,W)/Var(W), c2 = Cov(W,X)/Var(X), Bias = c1 x c2.",
        "diagnostics": "Sign-of-bias table; causal ordering; pre/post-treatment status of controls; compare short vs long regressions.",
        "fails": "Controls that are mediators, colliders, or outcomes of treatment can create bias instead of removing it.",
        "interpretation": "Use OVB to reason directionally; do not treat it as a fix unless W is measured and valid to condition on.",
        "example": "Schooling/earnings: ability can create upward bias if it raises both education and wages.",
    },
    "matching": {
        "estimand": "Usually ATT for treated observations that remain on common support after trimming/matching.",
        "id_logic": "Matched controls approximate treated units' missing Y(0) using observed pre-treatment similarity.",
        "readout": "Matching is design preprocessing; the causal claim is still CIA plus overlap, not the matching algorithm itself.",
        "diagnostics": "Standardized mean differences; propensity-score overlap; matched sample size; caliper sensitivity; balance after matching.",
        "fails": "Hidden bias remains if selection operates through motivation, ability, or other unobserved determinants.",
        "interpretation": "Report effects for the matched population; trimmed treated units narrow external validity.",
        "example": "Job-training participants matched to nonparticipants on prior earnings and employment histories.",
    },
    "iv": {
        "estimand": "With heterogeneous effects and monotonicity, IV identifies LATE for compliers moved by Z.",
        "id_logic": "Use only the part of D shifted by Z; divide Z's outcome effect by Z's treatment effect.",
        "readout": "Wald = reduced form / first stage; 2SLS is the same logic with regression machinery.",
        "diagnostics": "First-stage coefficient and F-statistic; balance by Z; exclusion story; reduced-form sign; weak-IV robust inference.",
        "fails": "If Z affects Y outside D, is correlated with U, or weakly shifts D, IV can be worse than OLS.",
        "interpretation": "Describe the instrument-induced treatment margin, not the average effect for everyone.",
        "example": "PACES lottery offer as Z, private-school attendance as D, achievement as Y.",
    },
    "late": {
        "estimand": "Local Average Treatment Effect for compliers: E[Y(1)-Y(0) | D(1)>D(0)].",
        "id_logic": "AIR assumptions isolate the subgroup whose treatment status changes when the instrument changes.",
        "readout": "Always-takers and never-takers affect take-up rates but reveal no treatment contrast from Z.",
        "diagnostics": "Take-up by assignment; monotonicity plausibility; exclusion audit; complier-share size; subgroup interpretation.",
        "fails": "Defiers, direct assignment effects, or instrument-dependent potential outcomes invalidate the LATE interpretation.",
        "interpretation": "Complier effects may be exactly policy-relevant for encouragement designs but not for universal mandates.",
        "example": "Voucher compliers are students who attend private school only if they win the offer.",
    },
    "panel_fe": {
        "estimand": "Within-unit effect of changes in X on changes in Y, net of stable unit traits and common period shocks.",
        "id_logic": "Subtract stable unobserved heterogeneity through unit FE/demeaning or first differences.",
        "readout": "FE asks whether a unit's outcome changes when its own treatment/predictor changes.",
        "diagnostics": "Within variation; unit/time FE necessity; clustered SEs; serial correlation; time-varying confounder checks.",
        "fails": "Time-varying shocks correlated with treatment timing remain in the error term.",
        "interpretation": "The coefficient is not identified by between-unit level differences once unit FE are included.",
        "example": "Country governance panel: compare a country to itself before/after institutional change.",
    },
    "did": {
        "estimand": "ATT for treated group after treatment under parallel untreated trends.",
        "id_logic": "Controls supply the treated group's untreated trend; permanent level differences are allowed.",
        "readout": "DiD = (Y_T,post - Y_T,pre) - (Y_C,post - Y_C,pre) = treated x post coefficient.",
        "diagnostics": "Pre-trend graph; placebo treatment date; composition checks; cluster-robust SEs; shock narrative.",
        "fails": "Differential shocks, anticipation, spillovers, or changing group composition can masquerade as treatment effects.",
        "interpretation": "Read the interaction as the extra post-period change among treated units relative to controls.",
        "example": "Road-repair towns: untreated control-town trend stands in for treated towns' missing untreated trend.",
    },
    "event_study": {
        "estimand": "Dynamic ATT by event time; under staggered adoption, estimand depends on comparison set/estimator.",
        "id_logic": "Align units around treatment timing to inspect pre-treatment leads and post-treatment lags.",
        "readout": "Leads near zero support, but do not prove, parallel trends; lags show effect dynamics.",
        "diagnostics": "Event-time plot; omitted-period choice; binning; never/not-yet-treated controls; Goodman-Bacon decomposition concerns.",
        "fails": "Already-treated controls and heterogeneous effects can produce negative or misleading TWFE weights.",
        "interpretation": "Explain each coefficient relative to the omitted pre-period and the chosen comparison group.",
        "example": "States adopt a policy in different years; calendar-time FE remove common shocks, event time tracks adoption.",
    },
    "ddd_continuous": {
        "estimand": "Additional treatment effect for the affected subgroup beyond a comparable placebo subgroup's DiD.",
        "id_logic": "Subtract away group-time confounding that affects treated and control units similarly in the placebo dimension.",
        "readout": "DDD = DiD(affected) - DiD(placebo); continuous DiD replaces treatment with dose/intensity.",
        "diagnostics": "Placebo subgroup logic; fake outcomes; fake dates; dose-response plausibility; spillover checks.",
        "fails": "If the placebo group is itself affected or does not share the confounding trend, the third difference misleads.",
        "interpretation": "Use DDD to sharpen a mechanism claim, not as automatic insurance against all DiD threats.",
        "example": "Policy should affect young workers but not older workers; older workers benchmark broader labor-market shocks.",
    },
    "synthetic_control": {
        "estimand": "Case-specific ATT for the treated unit after intervention, relative to its weighted donor counterfactual.",
        "id_logic": "A weighted donor pool reproduces the treated unit's pre-treatment path and predictors.",
        "readout": "Post-treatment gap = treated outcome - synthetic outcome; credibility starts with pre-treatment fit.",
        "diagnostics": "Pre-fit RMSPE; donor weights; leave-one-out checks; in-space/in-time placebos; donor contamination audit.",
        "fails": "Poor pre-fit, treated-only shocks, or contaminated donors make the synthetic path a weak counterfactual.",
        "interpretation": "Treat as a transparent comparative case design, with inference based on placebo gaps rather than standard t-tests.",
        "example": "California tobacco-control policy compared to a weighted blend of untreated states.",
    },
    "rdd": {
        "estimand": "Local treatment effect at the cutoff; fuzzy RDD identifies a cutoff-local LATE for compliers.",
        "id_logic": "Near the threshold, units just above and below are comparable except for treatment probability.",
        "readout": "Sharp RDD = discontinuity in Y; fuzzy RDD = jump in Y divided by jump in treatment probability.",
        "diagnostics": "Outcome scatter/binned plot; density/manipulation test; covariate continuity; bandwidth sensitivity; local-linear fit.",
        "fails": "Sorting, other rules at the cutoff, or flexible polynomials can manufacture a jump.",
        "interpretation": "Do not generalize far from the cutoff without a separate external-validity argument.",
        "example": "Angrist-Lavy class-size rule: enrollment cutoffs shift class size locally.",
    },
    "experiments2": {
        "estimand": "ITT under assignment; precision-adjusted ATE under randomization; IV/LATE if assignment instruments receipt.",
        "id_logic": "Randomization identifies the assignment contrast; pre-treatment covariates can reduce unexplained variance.",
        "readout": "Covariate adjustment should not change the story dramatically; interacted ANCOVA protects against slope heterogeneity.",
        "diagnostics": "Pre-analysis plan; baseline covariate timing; attrition; compliance; robust/HC SEs; adjusted vs unadjusted estimates.",
        "fails": "Post-treatment adjustment, selective attrition, or interpreting receipt effects without IV assumptions breaks the design.",
        "interpretation": "Separate design-based identification from model-based precision gains.",
        "example": "Outreach experiment: baseline turnout predicts Y, while assigned contact differs from actual contact.",
    },
    "time_series": {
        "estimand": "Impact and long-run propensities: immediate and cumulative response of Y to current/lagged X.",
        "id_logic": "Use temporal ordering plus exogeneity/stationarity assumptions to interpret dynamic regression coefficients.",
        "readout": "Long-run propensity is the sum of distributed-lag coefficients when the model is stable.",
        "diagnostics": "Time plot; autocorrelation; unit-root/stationarity tests; residual serial correlation; lag-length sensitivity.",
        "fails": "Trending or unit-root series can generate spurious significance even when variables are unrelated.",
        "interpretation": "Distinguish short-run shock effects from persistent long-run changes, and be cautious with feedback.",
        "example": "GDP or monetary-policy shock models where outcomes adjust across several periods.",
    },
}

for unit in UNITS:
    unit.update(DEEP_SNAPSHOTS[unit["anchor"]])


styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=25, textColor=DARK, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=9, leading=11, textColor=GREY, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle("TOC", parent=styles["Normal"], fontSize=8.6, leading=10.2, textColor=BLUE, spaceAfter=0.5))
styles.add(ParagraphStyle("Header", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12, leading=14, textColor=colors.white))
styles.add(ParagraphStyle("HeaderSub", parent=styles["Normal"], fontSize=8.4, leading=10, textColor=colors.HexColor("#E8EEF6")))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.2, leading=11.1, spaceAfter=3))
styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=7.8, leading=9.2, spaceAfter=2))
styles.add(ParagraphStyle("Dense", parent=styles["Normal"], fontSize=7.35, leading=8.45, spaceAfter=1.2))
styles.add(ParagraphStyle("DenseLabel", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.45, leading=8.6, textColor=DARK, spaceAfter=1))
styles.add(ParagraphStyle("Tiny", parent=styles["Normal"], fontSize=7, leading=8.3, textColor=GREY))
styles.add(ParagraphStyle("Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=DARK, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle("SectionTight", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=9.2, leading=10.4, textColor=DARK, spaceBefore=2, spaceAfter=1))


def header_table(unit):
    title = f"{unit['week']} | {unit['title']}"
    rows = [[Paragraph(title, styles["Header"])], [Paragraph(unit["reading"], styles["HeaderSub"])]]
    t = Table(rows, colWidths=[7.2 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def strengths_table(unit):
    left = bullets(unit["strengths"], styles["Small"])
    right = bullets(unit["limits"], styles["Small"])
    t = Table(
        [[Paragraph("<b>Strengths / best use</b>", styles["Small"]), Paragraph("<b>Diagnostics / limits</b>", styles["Small"])], [left, right]],
        colWidths=[3.46 * inch, 3.46 * inch],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GREEN),
        ("BACKGROUND", (1, 0), (1, -1), AMBER),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def snapshot_table(unit):
    rows = [
        [Paragraph("<b>Estimand</b>", styles["DenseLabel"]), Paragraph(unit["estimand"], styles["Dense"])],
        [Paragraph("<b>Identification logic</b>", styles["DenseLabel"]), Paragraph(unit["id_logic"], styles["Dense"])],
        [Paragraph("<b>Readout</b>", styles["DenseLabel"]), Paragraph(unit["readout"], styles["Dense"])],
    ]
    t = Table(rows, colWidths=[1.32 * inch, 5.58 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GREEN),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.2, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def application_table(unit):
    rows = [
        [Paragraph("<b>Diagnostics</b>", styles["DenseLabel"]), Paragraph(unit["diagnostics"], styles["Dense"])],
        [Paragraph("<b>What fails</b>", styles["DenseLabel"]), Paragraph(unit["fails"], styles["Dense"])],
        [Paragraph("<b>Interpretation</b>", styles["DenseLabel"]), Paragraph(unit["interpretation"], styles["Dense"])],
        [Paragraph("<b>Course example</b>", styles["DenseLabel"]), Paragraph(unit["example"], styles["Dense"])],
    ]
    t = Table(rows, colWidths=[1.18 * inch, 5.72 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), AMBER),
        ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.2, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)
    canvas.drawString(0.55 * inch, 0.38 * inch, TITLE)
    canvas.drawRightString(7.95 * inch, 0.38 * inch, str(canvas.getPageNumber()))
    canvas.restoreState()


def build_story(image_paths):
    story = []
    story += [
        Paragraph(TITLE, styles["CoverTitle"]),
        Paragraph("GPEC 446 - Quantitative Methods 3 | Spring 2026 | Professor Mateo Vasquez-Cortes", styles["CoverSub"]),
    ]
    desc = (
        "This reference synthesizes the course's causal inference theory, core models, diagnostics, and readings in syllabus order. "
        "It starts from the existing QM3 midterm methods and lecture references, extends to late-term methods, and gives every concept unit exactly two pages of study space with one analytical image."
    )
    box_tbl = Table([[Paragraph(desc, styles["Small"])]], colWidths=[7.2 * inch])
    box_tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.5, BORDER), ("PADDING", (0, 0), (-1, -1), 7)]))
    story += [box_tbl, Spacer(1, 8), Paragraph("<b>Hyperlinked Contents</b>", styles["Section"])]
    for i, unit in enumerate(UNITS, start=1):
        story.append(Paragraph(f'<a href="#{unit["anchor"]}">{i}. {unit["week"]} - {unit["title"]}</a>', styles["TOC"]))
    story += [
        Spacer(1, 6),
        HRFlowable(width="35%", thickness=0.5, color=BORDER, hAlign="LEFT"),
        Paragraph("Generated with GPT-5 Codex via the Claudia agent system for GPEC 446. Always verify against official course materials and readings; this is a study aid, not a substitute for assigned texts or class notes.", styles["Tiny"]),
        PageBreak(),
    ]

    story += [
        Paragraph("<b>Inventory and Scope Note</b>", styles["Section"]),
        Paragraph("Syllabus order used: Week 1 randomization and causal inference; Week 2 potential outcomes and regression; Week 3 IV and LATE; Weeks 4-5 panel data, DiD, event studies, and extensions; Week 6 matching and synthetic control; Week 7 RDD; Weeks 8-9 field experiments; Week 10 time series.", styles["Body"]),
        Paragraph("v1.1.0 revision principle: keep the exact two-page-per-concept rhythm, but make every unit more application-dense. Each concept now includes a compact snapshot of the estimand, identification logic, model/readout, diagnostics, failure mode, interpretation rule, and a course-style example.", styles["Body"]),
        Paragraph("Starting sources checked: QM3_Midterm_Methods_Reference_v1.2.0, QM3_Midterm_Lecture_Reference_v1.5.0, syllabus extraction, Tyche concept notes, lecture slides L1-L10, labs, and local handouts. Known source gap: Week 6 lists 'Additional readings' but no exact matching/synthetic-control readings were available locally, so those units are course-method syntheses rather than reading-specific summaries.", styles["Body"]),
        Spacer(1, 3),
        Table(
            [[
                Paragraph("<b>Read each unit as a research-design checklist</b><br/>1. Name the estimand. 2. Identify who supplies the missing counterfactual. 3. State the identifying assumption. 4. Diagnose the assumption. 5. Interpret only for the population and margin the design actually identifies.", styles["Dense"]),
                Paragraph("<b>Core causal vocabulary across the guide</b><br/>Counterfactual, potential outcomes, selection bias, common support, exogeneity, exclusion, monotonicity, fixed effects, parallel trends, no anticipation, local treatment effect, stationarity.", styles["Dense"]),
            ]],
            colWidths=[3.45 * inch, 3.45 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), GREEN),
                ("BACKGROUND", (1, 0), (1, 0), AMBER),
                ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]),
        ),
        Spacer(1, 6),
        Paragraph("<b>Concept coverage map</b>", styles["SectionTight"]),
        Table(
            [
                [Paragraph("<b>Experimental or as-if random assignment</b>", styles["DenseLabel"]), Paragraph("Random assignment, blocking, ITT, covariate adjustment, noncompliance, IV/LATE, fuzzy RDD.", styles["Dense"])],
                [Paragraph("<b>Selection on observables</b>", styles["DenseLabel"]), Paragraph("OLS with controls, CIA, common support, matching, propensity scores, balance diagnostics.", styles["Dense"])],
                [Paragraph("<b>Selection on unobservables via timing/rules</b>", styles["DenseLabel"]), Paragraph("Panel FE/FD, DiD, event studies, DDD, synthetic control, sharp/fuzzy RDD.", styles["Dense"])],
                [Paragraph("<b>Dynamic dependence</b>", styles["DenseLabel"]), Paragraph("Time-series lags, impact and long-run propensities, stationarity, unit roots, serial correlation.", styles["Dense"])],
            ],
            colWidths=[2.15 * inch, 4.75 * inch],
            style=TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.2, BORDER),
                ("BACKGROUND", (0, 0), (0, -1), LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]),
        ),
        PageBreak(),
    ]

    for unit in UNITS:
        story += [BookmarkAnchor(unit["anchor"], unit["title"]), header_table(unit), Spacer(1, 6)]
        story.append(Paragraph("<b>Situation / use case.</b> " + unit["situation"], styles["Body"]))
        img = RLImage(str(image_paths[unit["anchor"]]), width=6.85 * inch, height=2.72 * inch)
        story += [img, Paragraph("<b>Image map.</b> " + unit["image_note"], styles["Small"])]
        story.append(Paragraph("<b>Core intuition.</b> " + unit["intuition"], styles["Body"]))
        story.append(snapshot_table(unit))
        story.append(PageBreak())

        story += [header_table(unit), Spacer(1, 6)]
        story.append(Paragraph("<b>Key concepts and terminology</b>", styles["SectionTight"]))
        story.append(bullets(unit["terms"], styles["Small"]))
        story.append(Paragraph("<b>Assumptions</b>", styles["SectionTight"]))
        story.append(bullets(unit["assumptions"], styles["Small"]))
        story.append(Paragraph("<b>Strengths, diagnostics, and limitations</b>", styles["SectionTight"]))
        story.append(strengths_table(unit))
        story.append(Paragraph("<b>Application snapshot</b>", styles["SectionTight"]))
        story.append(application_table(unit))
        story.append(Paragraph("<b>APA/source anchor.</b> " + "; ".join(unit["refs"]) + ".", styles["Small"]))
        story.append(PageBreak())

    story.append(Paragraph("<b>References</b>", styles["Section"]))
    for ref in REFERENCES:
        story.append(Paragraph(ref, styles["Small"]))
    story += [
        Spacer(1, 8),
        HRFlowable(width="45%", thickness=0.5, color=BORDER, hAlign="LEFT"),
        Paragraph("<b>Disclosure</b>", styles["Section"]),
        Paragraph("Generated for: Edgar Agunias<br/>Date: 2026-06-01<br/>Model: GPT-5 Codex<br/>Sources: GPEC 446 syllabus, lecture slides L1-L10, labs and handouts, Tyche memory and concept notes, existing QM3 midterm methods/lecture references, Angrist & Pischke, Gerber & Green, Wooldridge, and cited method references.<br/>Agent: Tyche", styles["Small"]),
    ]
    return story


def write_notes():
    lines = [
        "# GPEC446_theory_reference_v1.1.0 Notes",
        "",
        "## Sources checked",
        "- `Course Admin/syllabus_extracted.md` and `QM3_Syllabus.pdf`",
        "- `Study Guides/QM3_Midterm_Methods_Reference_v1.2.0.pdf` and notes",
        "- `Study Guides/QM3_Midterm_Lecture_Reference_v1.5.0.pdf` and notes",
        "- `_agent/AGENT_CONTEXT.md`, `FEEDBACK.md`, and `CONCEPT_NOTES.md`",
        "- Lecture slides `Lectures/QM3_L1_Intro.pdf` through `QM3_L10_Panel4.pdf`",
        "- Labs and handouts for randomization, causal inference, IV, DiD/FE/FD, RDD, and fuzzy RDD",
        "",
        "## v1.1.0 density improvements",
        "- Preserved the 16-unit syllabus order and exact two-page-per-concept rhythm from v1.0.0.",
        "- Reduced image vertical footprint on each first concept page and added a compact three-row snapshot: estimand, identification logic, and readout/formula interpretation.",
        "- Added an application snapshot to each second concept page covering diagnostics, what fails when assumptions fail, interpretation discipline, and a course-style example.",
        "- Expanded the inventory/scope page so it functions as a research-design checklist and concept coverage map instead of a sparse transition page.",
        "- Kept text in compact but readable styles; no formulas were pushed into tiny or overflow-prone blocks.",
        "",
        "## Unit inventory",
    ]
    for i, unit in enumerate(UNITS, start=1):
        lines.append(f"{i}. {unit['week']} - {unit['title']} ({unit['reading']})")
    lines += [
        "",
        "## Known source gap",
        "Week 6 lists matching and synthetic control with `Additional readings`, but no exact local reading files or reading titles were available. The matching and synthetic-control units are therefore synthesized from the syllabus, Tyche concept notes, and standard method references.",
        "",
        "## Image generation",
        f"Analytical PNG assets were generated with PIL into `{ASSET_DIR.relative_to(COURSE)}`. Each unit has one image and an image-map caption in the PDF.",
        "",
        "---",
        "Generated for: Edgar Agunias",
        "Date: 2026-06-01",
        f"Model: {MODEL}",
        "Sources: GPEC 446 syllabus, lecture slides, labs/handouts, existing QM3 reference guides, Tyche memory, and cited readings",
        "Agent: Tyche",
        "---",
    ]
    NOTES.write_text("\n".join(lines) + "\n")


def main():
    image_paths = {unit["anchor"]: save_diagram(unit) for unit in UNITS}
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.52 * inch,
        bottomMargin=0.58 * inch,
        title=TITLE,
        author="Tyche",
    )
    doc.build(build_story(image_paths), onFirstPage=footer, onLaterPages=footer)
    write_notes()
    print(OUT)
    print(NOTES)


if __name__ == "__main__":
    main()
