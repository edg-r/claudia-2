from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = Path(__file__).with_name("QM3_Midterm_Methods_Reference_v1.2.0.pdf")
TITLE = "QM3 Midterm Methods Reference"
MODEL = "GPT-5.5 (medium reasoning)"

DARK = colors.HexColor("#1B2A4A")
BLUE = colors.HexColor("#2C5282")
LIGHT = colors.HexColor("#F3F6FA")
GREEN = colors.HexColor("#EAF7EF")
AMBER = colors.HexColor("#FFF5E6")
GREY = colors.HexColor("#666666")


class BookmarkAnchor(Flowable):
    def __init__(self, name, title=""):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0
        self.name = name
        self.title = title

    def draw(self):
        self.canv.bookmarkPage(self.name, fit="XYZ", left=0, top=self.canv._pagesize[1])
        if self.title:
            self.canv.addOutlineEntry(self.title, self.name, level=0)


def p(txt, style):
    return Paragraph(txt, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=9) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=11,
        bulletFontSize=5,
        spaceBefore=0,
        spaceAfter=0,
    )


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        "CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=25,
        textColor=DARK,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        "CoverSub",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=GREY,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=9.2,
        leading=11,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=12,
        leading=13.4,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=12,
        leading=13.4,
        textColor=DARK,
        spaceBefore=5,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        "Header",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=13.5,
        textColor=colors.white,
    )
)
styles.add(
    ParagraphStyle(
        "HeaderSub",
        parent=styles["Normal"],
        fontSize=8.8,
        leading=10,
        textColor=colors.HexColor("#E8EEF6"),
    )
)
styles.add(
    ParagraphStyle(
        "TOC",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=12.5,
        textColor=BLUE,
        spaceAfter=1,
    )
)


methods = [
    {
        "anchor": "po",
        "title": "Potential Outcomes and Selection",
        "source": "Sources: Mastering 'Metrics: The Path from Cause to Effect (Angrist & Pischke); QM3 Lectures L1-L2 and Lab 1; Week 1 exercise source",
        "situation": "A program looks successful because treated units have higher outcomes, but the treated group may already have had better untreated potential outcomes.",
        "context": "The modern potential-outcomes language Edgar sees in QM3 comes from the Rubin causal model tradition, which formalized treatment effects as comparisons between multiple possible outcomes for the same unit. Angrist and Pischke write in the post-credibility-revolution environment of applied microeconometrics, where the central question is not whether a regression can be estimated, but whether the comparison behind it has a credible counterfactual.",
        "theory": "The potential-outcomes framework turns causal inference into a missing-data problem. Every unit has two possible outcomes, Y(1) under treatment and Y(0) without treatment, but we observe only one realized outcome because each unit is either treated or untreated. The central theory is that a causal effect is not a raw treated-control difference; it is a comparison between two potential outcomes for the same unit or comparable groups. Random assignment solves the problem by making the untreated potential outcomes of treated and control units comparable in expectation. Without that assignment logic, the naive difference bundles the treatment effect together with selection: treated units may differ before treatment in motivation, wealth, health, location, or other baseline traits.",
        "identification": "Identification asks how to replace the missing counterfactual. In a randomized experiment, the control group estimates the treated group's missing untreated outcome because treatment assignment is independent of potential outcomes. In observational data, Edgar must explain what institutional rule, design, or covariate structure makes the comparison as-if random. The estimand matters: ATE averages over everyone, ATT asks about those actually treated, ITT asks about assignment or eligibility, and LATE asks about compliers moved by an instrument.",
        "failure": "This design fails when treatment is chosen in response to expected outcomes, when units influence each other, or when the treatment itself is not stable across units. A job-training program, for example, may attract motivated participants; a village-level health intervention may spill over to untreated neighbors; and a program label may hide different treatment doses. Each failure changes the meaning of the treated-control comparison.",
        "interpretation": "A clean answer should say: the observed treated-control difference is causal only under the assignment assumption; otherwise it equals a causal effect plus selection. If the outcome is a rate, interpret differences in percentage points. If compliance is incomplete, report the ITT as the effect of being assigned or eligible, not the effect of actually receiving treatment.",
        "formula": "Unit effect: tau_i = Y_i(1) - Y_i(0). ATE = E[Y_i(1) - Y_i(0)]. ATT = E[Y_i(1) - Y_i(0)|D=1]. Naive difference = E[Y|D=1] - E[Y|D=0] = ATT + selection bias.",
        "moves": [
            "<b>Define the target first.</b> Say whether the question asks for ATE, ATT, ATC, ITT, or LATE before calculating.",
            "<b>Separate observed and counterfactual quantities.</b> We observe E[Y(1)|D=1] and E[Y(0)|D=0], but ATT also needs E[Y(0)|D=1].",
            "<b>Sign the selection bias.</b> Ask who enters treatment and whether their Y(0) is likely higher or lower than controls.",
            "<b>Use percentage points for rate outcomes.</b> 82% minus 71% is 11 pp, not 11 percent.",
        ],
        "concepts": [
            "<b>Fundamental problem.</b> The missing potential outcome prevents observing an individual causal effect directly.",
            "<b>Selection bias.</b> Baseline differences between treated and control units contaminate the naive comparison.",
            "<b>ITT.</b> Effect of assignment or eligibility, useful when take-up is incomplete.",
            "<b>SUTVA.</b> Treatment status for one unit should not alter another unit's outcome, and treatment must mean the same thing across units.",
        ],
        "assumptions": [
            "Random assignment or as-if random assignment: D is independent of potential outcomes.",
            "No interference/SUTVA: one unit's treatment does not change another unit's outcome.",
            "Stable treatment: treated and untreated states are well defined.",
            "Comparable measurement: outcomes are measured the same way in both groups.",
        ],
        "pitfalls": [
            "Calling a raw difference causal before explaining assignment.",
            "Mixing up ATE with ATT when treatment effects are heterogeneous.",
            "Treating ITT as the treatment-on-treated effect when many assigned units do not comply.",
            "Writing percent when the exercise asks for percentage points.",
        ],
        "example": "If the prompt says eligible households have an 82% school-enrollment rate and ineligible households have a 71% rate, the 11 percentage-point difference is not automatically the effect of the program. A strong answer asks whether eligibility was randomized or plausibly as-if random. If only 65% of eligible households took up the program, the 11 pp estimate is an ITT-style assignment or eligibility effect unless extra assumptions justify scaling it into an effect on takers.",
    },
    {
        "anchor": "ols",
        "title": "OLS, Controls, and Interactions",
        "source": "Sources: QM3 Lectures L3-L4 and Lab 2; Wooldridge-style regression notation from lecture/exercise source; Homework 1 code conventions",
        "situation": "A regression coefficient is easy to compute, but it is causal only if treatment is as-good-as-random after the included covariates.",
        "context": "The OLS material sits in the older econometrics textbook tradition associated with linear regression as the workhorse empirical model, but QM3 treats it through the newer causal-inference lens. Wooldridge-style notation helps Edgar read regression equations and assumptions; Angrist and Pischke's influence is the insistence that a coefficient is only as good as the comparison it represents.",
        "theory": "OLS is a conditional-comparison machine. In a simple regression, the slope summarizes how the average outcome changes with X. In a multiple regression, the coefficient on D compares units with different D values while holding the included controls fixed in the linear projection. That can remove confounding only when the remaining unobserved error is unrelated to D. Controls are therefore a research-design claim, not a magic cleanup step: they must be pre-treatment variables that make treated and control units comparable. Interactions extend the model by allowing the treatment effect or slope to differ across groups, which is why the main coefficient is conditional on the omitted/reference group or on the zero point of the interacted variable.",
        "identification": "The identification claim is conditional independence: once Edgar conditions on the chosen controls, the remaining treatment variation is unrelated to omitted determinants of the outcome. A regression table does not prove this. The argument must come from the policy setting: which variables were determined before treatment, which ones jointly predict treatment and outcomes, and whether treated and untreated units overlap after conditioning.",
        "failure": "Controls fail when they are post-treatment variables, colliders, bad proxies, or when they leave treated units compared to extrapolated controls outside common support. Interactions fail interpretively when the reference category or zero point is forgotten. A coefficient can be mathematically precise and still causally empty if the regression asks the wrong comparison.",
        "interpretation": "State the coefficient in the outcome's units, name the comparison group, and say exactly what is held fixed. For an interaction, b1 is the treatment effect only for the reference group; b3 is the additional difference for the interacted group; the full effect for that group is b1+b3. With logged outcomes, use approximate percent language only when the coefficient is small enough for that approximation.",
        "formula": "Simple OLS: beta_1 = Cov(X,Y) / Var(X). Conditional regression: Y = beta_0 + beta_1 D + beta_2 X + e. Interaction: Y = b0 + b1 D + b2 G + b3(D*G) + e.",
        "moves": [
            "<b>Coefficient interpretation.</b> State units, comparison group, and what is held fixed.",
            "<b>Conditional independence language.</b> Say that after controls, treatment variation must be unrelated to omitted determinants of Y.",
            "<b>Interactions.</b> b1 is the D effect when G=0; b3 is the additional D effect when G=1; D effect for G=1 is b1+b3.",
            "<b>Demeaning.</b> Center a continuous variable before interacting so the intercept/main dummy is interpretable at the average.",
        ],
        "concepts": [
            "<b>Regression control.</b> A way to compare treated and control units at the same value of X.",
            "<b>Reference category.</b> Dummy-variable coefficients are always relative to the omitted category.",
            "<b>Bad control.</b> A post-treatment variable or collider that can create bias rather than remove it.",
            "<b>Common support.</b> The model needs treated and control observations in overlapping covariate ranges.",
        ],
        "assumptions": [
            "Conditional independence: E[e|D,X]=0 after controls.",
            "Common support: treated and control units overlap in covariate space.",
            "Controls are pre-treatment, not downstream consequences of treatment.",
            "Functional form is adequate enough that the comparison being made is meaningful.",
        ],
        "pitfalls": [
            "Treating bad controls as harmless precision improvements.",
            "Interpreting an interaction coefficient as the full treatment effect.",
            "Ignoring the reference category for dummies.",
            "Saying 'holding everything constant' when only included covariates are held fixed.",
        ],
        "example": "If a regression of income mobility on neighborhood poverty adds race composition and commuting-zone fixed effects, Edgar should say the poverty coefficient compares tracts with different poverty rates within the same commuting-zone structure and included covariates. If the model includes poverty times majority-non-white, the poverty slope for majority-white tracts is the main poverty coefficient, while the majority-non-white slope is the main poverty coefficient plus the interaction. That interpretation comes before any causal claim.",
    },
    {
        "anchor": "ovb",
        "title": "Omitted Variable Bias and Simultaneity",
        "source": "Sources: QM3 Lecture L4 and Lab 2; Week 2 exercise source; exercises_gap_scan.md",
        "situation": "Schooling appears to raise wages, but ability or family background may be omitted and correlated with schooling.",
        "context": "OVB is the bridge between standard regression training and the causal-design turn in applied econometrics. It comes from the classical linear-model problem of endogeneity, but in QM3 it is used as a diagnostic language: explain precisely why the short regression is contaminated before reaching for an experiment, instrument, panel design, or better comparison group.",
        "theory": "OVB explains exactly when a short regression coefficient fails as a causal estimate. The short regression loads onto both the causal effect of treatment and the part of an omitted determinant that travels with treatment. The sign of the bias is the product of two relationships: how the omitted variable affects the outcome and how the omitted variable is correlated with treatment. Simultaneity is a related but sharper failure: X and Y determine each other at the same time, so the regressor is mechanically entangled with the error term. Adding ordinary controls rarely fixes simultaneity because the issue is reverse causality or equilibrium feedback, not merely a missing background trait.",
        "identification": "The key identification lesson is negative: a regression identifies the treatment effect only if omitted determinants are uncorrelated with the treatment or are correctly included as controls. The professor's preferred Cov/Var form turns that into exam arithmetic. Bias is positive when the omitted variable raises Y and is positively correlated with X, or when it lowers Y and is negatively correlated with X; it is negative when those signs differ.",
        "failure": "OVB reasoning fails when the omitted variable is post-treatment, measured after the causal channel has already operated, or conceptually part of the treatment effect rather than a confounder. Simultaneity fails differently: the problem is joint determination, so merely adding more controls may leave the regressor endogenous. In policy settings, prices and quantities, policing and crime, and schooling and earnings can all have this feedback structure.",
        "interpretation": "Use the sign table out loud: first sign the omitted variable's effect on Y, then sign its relationship with X, then multiply. If the estimated coefficient is 4 and the bias is +1.5, the corrected causal effect is 2.5. If the estimated coefficient is negative and the bias is positive, the true effect is even more negative after subtracting the positive bias.",
        "formula": "OVB = beta_short - beta_long = pi_1 * gamma. Professor/exercise form: bias = [Cov(Y,W)/Var(W)] * [Cov(W,X)/Var(X)]. True effect = estimated coefficient - bias.",
        "moves": [
            "<b>OVB sign.</b> Sign Cov(omitted,D), sign effect of omitted on Y, multiply.",
            "<b>Map notation.</b> In the professor's Cov/Var notation, c1 = Cov(Y,W)/Var(W) and c2 = Cov(W,X)/Var(X), so bias = c1*c2.",
            "<b>Bias recovery.</b> If given estimated coefficient and bias, recover true effect as estimated minus bias.",
            "<b>Simultaneity.</b> If Y affects X and X affects Y, say an external source of variation is needed to break the feedback loop.",
        ],
        "concepts": [
            "<b>Short regression.</b> Outcome on treatment without the omitted confounder.",
            "<b>Long regression.</b> Outcome on treatment plus the omitted/confounding variable.",
            "<b>Confounder.</b> A pre-treatment variable related to both treatment and outcome.",
            "<b>Reverse causality.</b> The outcome also causes the regressor, making the regressor endogenous.",
        ],
        "assumptions": [
            "The omitted variable is causally prior to the outcome and correlated with treatment.",
            "The long regression includes the confounder in the right conceptual direction and functional form.",
            "For simultaneity, an instrument, experiment, lag, or institutional rule supplies exogenous variation.",
            "Measurement error in the omitted variable is not quietly reintroducing confounding.",
        ],
        "pitfalls": [
            "Forgetting that positive bias can make a negative true effect look smaller in magnitude.",
            "Using pi/gamma notation without mapping it to the professor's Cov/Var notation.",
            "Calling simultaneity an ordinary omitted-control problem.",
            "Subtracting the estimated coefficient from the bias instead of estimated minus bias.",
        ],
        "example": "Suppose the short regression says schooling raises wages by 8, but ability is omitted. If ability raises wages and high-ability people get more schooling, the bias is positive, so the short coefficient is too high. If the exercise gives c1 = 3 and c2 = 0.5, bias = 1.5 and the corrected effect is 8 - 1.5 = 6.5. In a simultaneity prompt, such as police and crime, the answer should say the coefficient mixes crime's effect on policing with policing's effect on crime.",
    },
    {
        "anchor": "iv",
        "title": "Instrumental Variables, 2SLS, and LATE",
        "source": "Sources: Mastering 'Metrics: The Path from Cause to Effect (Angrist & Pischke), Ch. 3; AIR 1996; Imbens & Angrist 1994; QM3 Lectures L5-L6; week3_IV_exercise_v2.pdf",
        "situation": "Distance to college changes schooling, but should affect wages only through schooling if it is a valid instrument.",
        "context": "IV has older roots in simultaneous-equations econometrics, but QM3's version is filtered through the 1990s LATE revolution. Imbens and Angrist (1994) and Angrist, Imbens, and Rubin (1996) clarified that IV does not automatically recover a universal treatment effect; under monotonicity it identifies the average effect for compliers moved by the instrument. Angrist and Pischke present IV as a credibility tool when the source of treatment variation is external and explainable.",
        "theory": "IV replaces problematic treatment variation with the part of treatment shifted by an outside source Z. The first stage asks whether Z actually moves D; the reduced form asks whether Z moves Y; the Wald/2SLS estimate rescales the reduced-form outcome difference by the first-stage treatment difference. The theory is powerful because it can identify causal effects even when D is endogenous, but it buys this power with demanding assumptions. Under the AIR/LATE framework, a valid instrument identifies the effect for compliers: units whose treatment status changes because of the instrument. That is why IV often estimates LATE rather than ATE.",
        "identification": "The instrument must satisfy four separate ideas. Relevance says Z moves D and can be partly checked through the first stage. Independence says Z is as-if randomly assigned with respect to potential outcomes. Exclusion says Z affects Y only through D. Monotonicity says the instrument pushes treatment in one direction, ruling out defiers. Together, these assumptions define both the causal interpretation and the population for the estimate.",
        "failure": "IV fails if the first stage is weak, if the instrument directly affects the outcome, if it is correlated with omitted determinants of the outcome, or if the complier population is too narrow for the substantive question. Weak instruments are especially dangerous because the Wald denominator is small: noise and small violations get magnified. A strong first stage does not rescue a bad exclusion restriction.",
        "interpretation": "Interpret 2SLS as the causal effect of D for compliers induced by Z, in the units of Y per unit of D. The reduced form is not the treatment effect unless Z itself is the treatment. The first stage gives the compliance shift. The Wald estimate is reduced form divided by first stage, so a -6 percentage-point ITT divided by a 15 percentage-point treatment increase is a -40 percentage-point LATE for compliers.",
        "formula": "Wald/IV = reduced form / first stage = Cov(Y,Z) / Cov(D,Z). 2SLS: first regress D on Z and controls; second regress Y on predicted D and controls. LATE = ITT / compliance shift.",
        "moves": [
            "<b>Name each regression.</b> OLS, first stage, 2SLS, and reduced form are different objects.",
            "<b>Defend the assumptions separately.</b> Relevance is testable; independence, exclusion, and monotonicity are design arguments.",
            "<b>Units.</b> With log wages, a 0.100 coefficient is about a 10% wage change per added year of schooling.",
            "<b>Compliance arithmetic.</b> Anti-malarial exercise: ITT = 11% - 17% = -6 pp; first stage = 60% - 45% = 15 pp; LATE = -6/15 = -40 pp among compliers.",
        ],
        "concepts": [
            "<b>First stage.</b> Effect of instrument Z on treatment D; weak first stages make IV unstable.",
            "<b>Reduced form.</b> Effect of Z on outcome Y, before rescaling by take-up.",
            "<b>Exclusion restriction.</b> Z affects Y only through D; this is a substantive claim, not a regression output.",
            "<b>Compliers.</b> Units induced into treatment by Z; LATE is their average effect.",
        ],
        "assumptions": [
            "Relevance/first stage: Z changes D.",
            "Independence/as-if random: Z is not correlated with omitted determinants of Y.",
            "Exclusion: Z affects Y only through D.",
            "Monotonicity for LATE: no defiers.",
        ],
        "pitfalls": [
            "Using the manual fitted-value second stage for standard errors; use ivreg() for correct inference.",
            "Treating LATE as ATE without stating the complier population.",
            "Declaring exclusion testable from the data.",
            "Ignoring weak instruments because the first-stage sign is in the expected direction.",
        ],
        "example": "For the anti-malarial style exercise, treatment assignment lowers infection from 17% to 11%, so the reduced form or ITT is -6 pp. Assignment raises take-up from 45% to 60%, so the first stage is 15 pp. The Wald/LATE estimate is -6/15 = -40 pp for compliers. The identifying paragraph should then defend why assignment affects infection only through take-up, why assignment is as-if random, and why there are no defiers.",
    },
    {
        "anchor": "did",
        "title": "Difference-in-Differences",
        "source": "Sources: Mastering 'Metrics: The Path from Cause to Effect (Angrist & Pischke), Ch. 5; Wooldridge panel-data source from syllabus; Interpreting all beta's in DiD.pdf; Week 6 Exercises DiD FE FD.pdf",
        "situation": "Treated businesses start below controls, but the causal question is whether their change after training exceeds the control group's change.",
        "context": "DiD is an old comparative tool that became central in modern applied microeconometrics because it translates policy timing into a transparent counterfactual. Angrist and Pischke use it to show how panel comparisons can turn before/after data into a credible design; Wooldridge-style panel notation gives the regression version that Edgar sees in class and exercises.",
        "theory": "DiD is a before-after comparison cleaned by a comparison group. A simple before-after estimate confuses treatment with any time shock that would have happened anyway. A post-only treated-control estimate confuses treatment with baseline differences between groups. DiD subtracts both: it removes time-invariant treated-control gaps with the first difference and removes common time shocks with the control-group trend. The identifying assumption is not that treated and control units have the same levels; it is that, absent treatment, their trends would have moved in parallel.",
        "identification": "The comparison group estimates the treated group's missing untreated trend. That requires parallel trends, no differential contemporaneous shocks, stable group composition, and no anticipation or spillovers. In the two-by-two regression, the interaction coefficient is the DiD effect because Treat absorbs baseline group differences, Post absorbs common time shocks, and Treat x Post captures the extra treated-group change after treatment.",
        "failure": "DiD fails when treated and control groups were already trending differently, when treatment timing coincides with another shock targeted at the treated group, when people sort into or out of groups because of the policy, or when control units are indirectly treated. Pre-trend plots are evidence about plausibility, not a formal proof of the counterfactual.",
        "interpretation": "Interpret the estimate as the treated group's outcome change beyond the control group's change. Baseline differences are not fatal; differential untreated trends are. In regression form, b0 is the control pre mean, b1 is the pre-treatment treated-control gap, b2 is the control group's time trend, and b3 is the treatment effect under parallel trends.",
        "formula": "DiD = (Y_T,post - Y_T,pre) - (Y_C,post - Y_C,pre). Regression: Y_it = b0 + b1 Treat_i + b2 Post_t + b3(Treat_i*Post_t) + e_it.",
        "moves": [
            "<b>Compute the four cells.</b> Business example: (180-145) - (170-165) = 35 - 5 = 30.",
            "<b>Interpret all betas.</b> b0=control pre mean; b1=baseline treatment-control gap; b2=control time trend; b3=DiD treatment effect.",
            "<b>Use controls as the counterfactual trend.</b> The control group tells you what would have happened to treated units absent treatment if parallel trends is credible.",
            "<b>Separate levels from trends.</b> Baseline level differences are allowed; differential untreated trends are the problem.",
        ],
        "concepts": [
            "<b>Parallel trends.</b> The treated group's untreated counterfactual trend equals the control group's observed trend.",
            "<b>Two-by-two DiD.</b> Two groups and two periods; the treatment effect is the interaction coefficient.",
            "<b>Counterfactual trend.</b> The control group's change stands in for the treated group's missing untreated change.",
            "<b>Pre-trends.</b> Useful diagnostic evidence, but not a proof of the identifying assumption.",
        ],
        "assumptions": [
            "Parallel trends: without treatment, treated and control outcomes would have changed similarly.",
            "No other simultaneous shock differentially hits treated units at the treatment date.",
            "Stable composition of treated/control groups over time.",
            "No anticipation or spillovers that change behavior before treatment begins.",
        ],
        "pitfalls": [
            "Interpreting b1 as treatment effect; it is the pre-treatment difference.",
            "Believing pre-trends prove parallel trends; they only support plausibility.",
            "Using a post-only treated-control comparison when baseline targeting is visible.",
            "Ignoring policy timing when another shock occurs at the same time.",
        ],
        "example": "If treated businesses rise from 145 to 180 and controls rise from 165 to 170, the treated change is 35 and the control change is 5, so DiD = 30. The fact that treated businesses started lower is allowed; the design only needs the control change to represent the treated businesses' untreated counterfactual trend. A strong answer also asks whether training coincided with another treated-area shock or whether low-performing firms were selected because their trends were already improving.",
    },
    {
        "anchor": "fe_fd",
        "title": "Fixed Effects and First Differences",
        "source": "Sources: Wooldridge panel-data source from syllabus; QM3 Week 6 Exercises DiD FE FD.pdf; Lab R patterns",
        "situation": "Firm traits such as location or managerial quality are stable over time, so compare firms to themselves before and after treatment.",
        "context": "Fixed effects and first differences come from the panel-data econometrics toolkit, where repeated observations let researchers control for stable unobserved differences across units. Wooldridge's textbook treatment emphasizes the mechanics and assumptions; QM3 links those mechanics to DiD so Edgar can see when the same idea appears as demeaning, differencing, or a treatment-by-time interaction.",
        "theory": "Fixed effects and first differences are two ways to remove stable unit-level confounders. Unit fixed effects add a separate intercept for each unit, so identification comes from within-unit changes over time. First differences subtract the pre-period outcome from the post-period outcome, which directly eliminates any time-invariant unit trait. With exactly two periods, FE and FD are algebraically equivalent and line up with the two-by-two DiD estimator when treatment changes only for the treated group. With more periods or staggered timing, the design becomes more subtle because treatment timing, dynamic effects, and weighting can matter.",
        "identification": "The identification claim is within-unit: after removing unit fixed traits and common time shocks, remaining changes in treatment are as-if unrelated to time-varying shocks in the error term. Unit FE handles stable confounding; time FE handles shocks common to all units. The untreated counterfactual is built from each unit's own history plus the common time pattern.",
        "failure": "FE fails when the omitted confounder changes over time in a way correlated with treatment, when treatment is anticipated, when measurement changes across periods, or when treatment effects evolve dynamically but the model forces one average coefficient. In staggered adoption settings, two-way FE can mix comparisons that are not clean untreated counterfactuals, so the simple two-period equivalence should not be overgeneralized.",
        "interpretation": "Interpret beta as a within-unit effect: how the same unit's outcome changes when its treatment status changes, after absorbing stable unit differences and common period shocks. In a two-period first-difference model, Delta Y is the change in outcome and Delta D is the change in treatment. If treated units move from 0 to 1 and controls stay at 0, the coefficient on Delta D equals the DiD.",
        "formula": "FE: Y_it = alpha_i + lambda_t + beta D_it + e_it. FD with two periods: Delta Y_i = beta Delta D_i + Delta e_i. In a simple two-period setup, FE, FD, and DiD recover the same beta.",
        "moves": [
            "<b>Firm/unit fixed effects.</b> Absorb time-invariant unit traits such as baseline size, location, or culture.",
            "<b>Time fixed effects.</b> Absorb common shocks affecting everyone in the post period.",
            "<b>Two-period equivalence.</b> In the Week 6 business table, Delta D is 1 for treated firms and 0 for controls, so regressing Delta Y on Delta D gives the DiD.",
            "<b>Interpret within-unit variation.</b> FE asks whether the same unit changes when treatment changes, not whether treated units differ from untreated units in levels.",
        ],
        "concepts": [
            "<b>Unit fixed effect.</b> A unit-specific intercept capturing all stable observed and unobserved traits.",
            "<b>Time fixed effect.</b> A period-specific intercept capturing common shocks.",
            "<b>Within transformation.</b> Demeaning each unit over time to remove alpha_i.",
            "<b>First difference.</b> Subtracting period t-1 from period t to eliminate fixed unit traits.",
        ],
        "assumptions": [
            "Unobserved confounders are time-invariant or captured by time shocks.",
            "Treatment timing is as-good-as-random after unit and time fixed effects.",
            "No time-varying omitted factor both changes treatment and outcome.",
            "For more than two periods, additional weighting/timing issues may arise; equivalence is no longer automatic.",
        ],
        "pitfalls": [
            "Saying FE controls for everything; it controls for time-invariant unit factors.",
            "Forgetting that time-varying confounders remain a threat.",
            "Assuming two-period DiD logic carries unchanged into staggered adoption.",
            "Including only unit FE and forgetting common time shocks.",
        ],
        "example": "In a two-period firm table, first difference each firm's outcome: post minus pre. Stable firm quality, location, and management culture disappear because they are the same in both periods. If treated firms have Delta D = 1 and control firms have Delta D = 0, regressing Delta Y on Delta D recovers the same comparison as DiD. But if a treated firm's local demand also changes at the same time, first differencing does not remove that time-varying confounder.",
    },
    {
        "anchor": "exam",
        "title": "Exam Workflow: How to Answer Method Questions",
        "source": "Sources: GPEC 446 QM3 syllabus and lecture/exercise source set; generated lecture/lab/manual guides; Canvas IV and DiD exercises",
        "situation": "Most midterm prompts are policy scenarios with numbers; the grade is in naming the design, computing cleanly, and defending assumptions.",
        "context": "This page is Tyche's exam-method wrapper rather than a single author tradition. It draws from the course's lecture/exercise environment: Valasquez-Cortes and Vargas tend to ask for policy-context reasoning, clean arithmetic, coefficient interpretation, and explicit identification language rather than abstract theorem recall.",
        "theory": "Method questions usually test whether Edgar can move from a policy scenario to an identification argument. The calculation is often short, but it has to sit inside a causal claim: what comparison is being made, what estimand it targets, what population it applies to, and what assumption makes it credible. A strong answer names the method, writes the estimator in the problem's units, interprets the sign and magnitude in plain language, then states the sharpest threat to identification. That sequence prevents the common midterm failure of doing arithmetic without causal reasoning.",
        "identification": "Identification language should be method-specific. For potential outcomes, name random assignment or selection. For OLS, name conditional independence and common support. For OVB, sign the omitted channel. For IV, separate relevance, independence, exclusion, and monotonicity. For DiD/FE/FD, name parallel trends or no time-varying confounding. The best exam answers use the scenario's facts to evaluate the assumption.",
        "failure": "Exam answers fail when they only calculate, when they recite generic assumptions, when they confuse estimand and estimator, or when they ignore the population identified by the design. Another common failure is treating every coefficient as a treatment effect without checking reference categories, time periods, interaction terms, or compliance.",
        "interpretation": "Use a five-part sentence: 'This design estimates [estimand] for [population] by comparing [groups/times/compliers]. The estimate is [number] [units], meaning [plain-language causal interpretation], if [assumption] holds; the main threat is [scenario-specific failure].' That template keeps computation, interpretation, and identification in the same answer.",
        "formula": "Five-step answer: identify design -> name estimand -> compute estimator -> interpret in units -> state identifying assumption and threat.",
        "moves": [
            "<b>Start in words.</b> One sentence naming the causal problem and why the naive comparison may fail.",
            "<b>Then calculate.</b> Show the arithmetic: differences, ratios, or coefficient mapping.",
            "<b>Interpret precisely.</b> Include units, base group, time period, and population.",
            "<b>End with judgment.</b> Say what assumption must hold and one reason it might fail in the scenario.",
        ],
        "concepts": [
            "<b>Estimand.</b> The causal quantity being targeted: ATE, ATT, ITT, LATE, DiD effect, or within-unit effect.",
            "<b>Estimator.</b> The calculation or regression coefficient used to estimate that quantity.",
            "<b>Identification.</b> The assumptions that let the estimator be interpreted causally.",
            "<b>Threat.</b> The concrete way the identifying assumption could fail in the given scenario.",
        ],
        "assumptions": [
            "Use the method-specific assumption, not a generic 'no bias' sentence.",
            "When asked whether something is testable, distinguish first-stage/relevance from exclusion/parallel trends.",
            "Tie every estimate to the population it identifies: assigned units, treated units, compliers, or treated group trend.",
            "Use the source scenario's timing and institutional detail to assess plausibility.",
        ],
        "pitfalls": [
            "Skipping units on log outcomes or percentage-point outcomes.",
            "Writing formulas without interpreting them in the policy setting.",
            "Answering with R syntax when the prompt asks for causal reasoning.",
            "Stating assumptions as slogans without naming the actual comparison group.",
        ],
        "example": "A compact midterm answer can be three sentences: 'This is a DiD design because the prompt gives treated/control groups before and after a policy. The estimate is (treated post - treated pre) - (control post - control pre) = X units, interpreted as the treated group's extra post-policy change relative to the control group's trend. The causal interpretation requires parallel trends; it would fail if the treated group received another shock at the same time.' Swap in IV, OLS, OVB, or FE language as the scenario changes.",
    },
]


def header_table(title, source):
    data = [[Paragraph(title, styles["Header"])], [Paragraph(source, styles["HeaderSub"])]]
    t = Table(data, colWidths=[7.4 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), DARK),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def two_col(left_title, left_items, right_title, right_items):
    left = [p(f"<b>{left_title}</b>", styles["Body"]), bullets(left_items, styles["Small"])]
    right = [p(f"<b>{right_title}</b>", styles["Body"]), bullets(right_items, styles["Small"])]
    t = Table([[left, right]], colWidths=[3.62 * inch, 3.62 * inch])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (0, 0), GREEN),
                ("BACKGROUND", (1, 0), (1, 0), AMBER),
                ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#CCCCCC")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)
    canvas.drawString(doc.leftMargin, 0.35 * inch, TITLE)
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


story = []
story.append(Spacer(1, 0.12 * inch))
story.append(p(TITLE, styles["CoverTitle"]))
story.append(
    p(
        "GPEC 446 - Applied Data Analysis and Statistical Decision Making | Mateo Vasquez-Cortes | UC San Diego | Spring 2026",
        styles["CoverSub"],
    )
)
desc = Table(
    [
        [
            Paragraph(
                "Exam-ready methods reference for the May 5, 2026 in-class midterm. Version 1.2.0 uses 12pt body text and fuller method pages: each design now opens with author/source context, then expands the theory, identification logic, failure modes, interpretation, formulas, exam moves, vocabulary, assumptions, and likely mistakes. It builds from Tyche's existing lecture/lab/reference guides and calibrates to the Canvas exercises on IV, DiD, fixed effects, and first differences.",
                styles["Small"],
            )
        ]
    ],
    colWidths=[7.25 * inch],
)
desc.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.extend([desc, Spacer(1, 8), p("<b>Table of Contents</b>", styles["Section"])])
for idx, item in enumerate(methods, 1):
    story.append(p(f'<a href="#{item["anchor"]}">{idx}. {item["title"]}</a>', styles["TOC"]))
story.extend(
    [
        Spacer(1, 8),
        HRFlowable(width="35%", thickness=0.4, color=colors.HexColor("#BBBBBB"), hAlign="LEFT"),
        p(
            f"Generated with {MODEL} via the Claudia agent system. Always verify against official course materials and readings. This document is a study aid and does not substitute for careful reading of the assigned texts or instructor materials.",
            styles["Small"],
        ),
        PageBreak(),
    ]
)

for i, item in enumerate(methods):
    story.append(BookmarkAnchor(item["anchor"], item["title"]))
    story.append(header_table(f"{i+1}. {item['title']}", item["source"]))
    story.append(Spacer(1, 5))
    story.append(p("<b>Situation.</b> " + item["situation"], styles["Body"]))
    story.append(p("<b>Author/source context.</b> " + item["context"], styles["Body"]))
    story.append(p("<b>Theory behind the method.</b> " + item["theory"], styles["Body"]))
    story.append(p("<b>Identification logic.</b> " + item["identification"], styles["Body"]))
    story.append(p("<b>Failure modes.</b> " + item["failure"], styles["Body"]))
    story.append(p("<b>Interpretation.</b> " + item["interpretation"], styles["Body"]))
    story.append(p("<b>Core formula / estimator.</b> " + item["formula"], styles["Body"]))
    story.append(p("<b>Exam moves.</b>", styles["Section"]))
    story.append(bullets(item["moves"], styles["Body"]))
    story.append(Spacer(1, 3))
    story.append(two_col("Key Concepts", item["concepts"], "Assumptions to State", item["assumptions"]))
    story.append(Spacer(1, 3))
    story.append(two_col("Common Mistakes", item["pitfalls"], "Quick Check", [
        "Can you name the estimand before calculating?",
        "Can you explain the identifying assumption in the scenario's own facts?",
        "Can you state the estimate in correct units and population?",
    ]))
    story.append(Spacer(1, 4))
    story.append(p("<b>Exam mini-example.</b> " + item["example"], styles["Body"]))
    if i != len(methods) - 1:
        story.append(PageBreak())

story.extend(
    [
        PageBreak(),
        p("References", styles["Section"]),
        p(
            "Angrist, J. D., & Pischke, J.-S. (2014). <i>Mastering 'metrics: The path from cause to effect</i>. Princeton University Press.",
            styles["Small"],
        ),
        p(
            "Imbens, G. W., & Angrist, J. D. (1994). Identification and estimation of local average treatment effects. <i>Econometrica, 62</i>(2), 467-475.",
            styles["Small"],
        ),
        p(
            "Angrist, J. D., Imbens, G. W., & Rubin, D. B. (1996). Identification of causal effects using instrumental variables. <i>Journal of the American Statistical Association, 91</i>(434), 444-455.",
            styles["Small"],
        ),
        p(
            "Vasquez-Cortes, M. (2026). <i>GPEC 446 lecture, lab, and exercise materials</i>. UC San Diego.",
            styles["Small"],
        ),
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#BBBBBB")),
        p(
            f"Generated for: Edgar Agunias<br/>Date: 2026-04-29<br/>Model: {MODEL}<br/>Sources: QM3 lecture/lab/reference manuals, Mastering 'Metrics Ch. 3 and Ch. 5 references, exercises gap scan, syllabus extraction, and machine-readable Canvas PDFs in inbox/QM3<br/>Agent: Tyche",
            styles["Small"],
        ),
    ]
)

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=letter,
    rightMargin=0.4 * inch,
    leftMargin=0.4 * inch,
    topMargin=0.38 * inch,
    bottomMargin=0.45 * inch,
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
