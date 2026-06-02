from __future__ import annotations

import importlib.util
import textwrap
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
COURSE_DIR = BASE_DIR.parent
MIDTERM_BUILDER = BASE_DIR / "build_midterm_theory_reference.py"
OUT = BASE_DIR / "GPCO410_theory_reference_v1.0.0.pdf"
NOTES_OUT = BASE_DIR / "GPCO410_theory_reference_v1.0.0_notes.md"
ASSET_DIR = BASE_DIR / "assets" / "GPCO410_theory_reference_v1.0.0"
ASSET_DISPLAY_DIR = "Study Guides/assets/GPCO410_theory_reference_v1.0.0"

TITLE = "GPCO 410 Theory Reference"
COURSE = "GPCO 410 International Politics & Security"
DATE = "2026-05-31"
MODEL = "GPT-5 (Codex)"

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


def load_midterm_theories():
    spec = importlib.util.spec_from_file_location("midterm_ref", MIDTERM_BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module.theories


def ref(text: str) -> str:
    return text


PER_THEORY_REFERENCES = {
    "w1_strategic_choice": [
        ref("Lake, D. A., & Powell, R. (1999). International relations: A strategic-choice approach. In D. A. Lake & R. Powell (Eds.), <i>Strategic choice and international relations</i> (pp. 3-38). Princeton University Press."),
        ref("Muthoo, A. (1999). <i>Bargaining theory with applications</i>. Cambridge University Press."),
    ],
    "w2_preferences_signaling": [
        ref("Frieden, J. A. (1999). Actors and preferences in international relations. In D. A. Lake & R. Powell (Eds.), <i>Strategic choice and international relations</i> (pp. 39-76). Princeton University Press."),
        ref("Schelling, T. C. (1966). <i>Arms and influence</i>. Yale University Press."),
        ref("Milner, H. V. (1997). <i>Interests, institutions, and information: Domestic politics and international relations</i>. Princeton University Press."),
    ],
    "w3_fearon": [
        ref("Fearon, J. D. (1995). Rationalist explanations for war. <i>International Organization, 49</i>(3), 379-414. https://doi.org/10.1017/S0020818300033324"),
    ],
    "w3_powell": [
        ref("Powell, R. (2006). War as a commitment problem. <i>International Organization, 60</i>(1), 169-203. https://doi.org/10.1017/S0020818306060061"),
    ],
    "w3_cases": [
        ref("Morrow, J. D. (1999). The strategic setting of choices: Signaling, commitment, and negotiation in international politics. In D. A. Lake & R. Powell (Eds.), <i>Strategic choice and international relations</i> (pp. 77-114). Princeton University Press."),
        ref("Woods, K. M., Lacey, J., & Murray, W. (2006). Saddam's delusions: The view from the inside. <i>Foreign Affairs, 85</i>(3), 2-26."),
        ref("Yetiv, S. A. (1997). The Persian Gulf crisis: A case study in foreign policy analysis. <i>Political Science Quarterly, 112</i>(1), 67-88."),
    ],
    "w4_audience_costs": [
        ref("Fearon, J. D. (1994). Domestic political audiences and the escalation of international disputes. <i>American Political Science Review, 88</i>(3), 577-592. https://doi.org/10.2307/2944796"),
    ],
    "w4_selectorate": [
        ref("Bueno de Mesquita, B., Morrow, J. D., Siverson, R. M., & Smith, A. (1999). An institutional explanation of the democratic peace. <i>American Political Science Review, 93</i>(4), 791-807. https://doi.org/10.2307/2586113"),
    ],
    "w4_public_opinion": [
        ref("Herrmann, R. K., Tetlock, P. E., & Visser, P. S. (1999). Mass public decisions to go to war: A cognitive-interactionist framework. <i>American Political Science Review, 93</i>(3), 553-573. https://doi.org/10.2307/2585574"),
    ],
    "w4_civil_war": [
        ref("Blattman, C., & Miguel, E. (2010). Civil war. <i>Journal of Economic Literature, 48</i>(1), 3-57. https://doi.org/10.1257/jel.48.1.3"),
        ref("Walter, B. F. (2009). Bargaining failures and civil war. <i>Annual Review of Political Science, 12</i>, 243-261. https://doi.org/10.1146/annurev.polisci.10.101405.135301"),
    ],
    "w5_walter": [
        ref("Walter, B. F. (2002). <i>Committing to peace: The successful settlement of civil wars</i>. Princeton University Press."),
    ],
    "w5_democratization": [
        ref("Cederman, L.-E., Hug, S., & Krebs, L. F. (2010). Democratization and civil war: Empirical evidence. <i>Journal of Peace Research, 47</i>(4), 377-394. https://doi.org/10.1177/0022343310368336"),
    ],
}


def build_theories():
    theories = []
    for t in load_midterm_theories():
        theories.append({
            "id": t["id"],
            "session": t["session"],
            "title": t["title"],
            "author": t["author"],
            "situation": t["situation"],
            "intuition": t["intuition"],
            "concepts": t["concepts"][:7],
            "assumptions": t["assumptions"][:4],
            "strengths": t["strengths"][:4],
            "weaknesses": t["weaknesses"][:4],
            "caption": f"Mechanism: {t['visual']['graph']} Key assumption: the analyst can specify actors and incentives clearly enough to map the sequence. Strength/limit cue: the diagram highlights the mechanism but abstracts from messy multi-actor politics.",
            "visual_labels": [t["title"].split("/")[0][:28], "Mechanism", "Assumption", "Limit"],
            "references": PER_THEORY_REFERENCES.get(t["id"], []),
            "priority": t["session"].startswith(("W5",)),
        })

    theories.extend([
        {
            "id": "w6_nuclear_coercion",
            "session": "W6",
            "title": "Nuclear Weapons and Coercive Diplomacy",
            "author": "Winning with the Bomb - Kyle Beardsley & Victor Asal; The Korean Conundrum - Ted Galen Carpenter & Doug Bandow",
            "situation": "North Korea can extract concessions not because nuclear use is likely, but because even a small chance of escalation raises U.S. expected costs.",
            "intuition": "Nuclear weapons alter crisis bargaining by changing expected costs. Beardsley and Asal argue that nuclear actors are especially advantaged against nonnuclear opponents because the possibility of full escalation makes the opponent more willing to back down and shortens crises. Carpenter and Bandow make the same credibility problem concrete in Korea: Pyongyang uses nuclear ambiguity, brinkmanship, and escalation risk to make U.S. military options costly. The exam move is to ask whether the bomb gives leverage through capability, risk manipulation, or opponent fear, and whether that leverage disappears under symmetric nuclear conditions.",
            "concepts": [
                ("Asymmetric nuclear dyad", "One side has nuclear weapons and the other does not; Beardsley and Asal find the nuclear actor gains bargaining advantages here."),
                ("Expected cost", "The probability-weighted cost of crisis escalation; nuclear weapons can raise severity while lowering perceived probability."),
                ("Coercive diplomacy", "Threats or limited pressure used to make an opponent concede or change policy."),
                ("Brinkmanship", "Manipulating the risk of uncontrolled escalation to improve bargaining leverage."),
                ("Nuclear ambiguity", "Keeping opponents uncertain about capability, doctrine, or willingness to escalate."),
                ("Symmetric nuclear dyad", "Both sides possess nuclear weapons, reducing unilateral coercive advantage."),
            ],
            "assumptions": [
                "Opponents believe nuclear escalation has catastrophic costs.",
                "The nuclear actor can make escalation risk visible without automatically triggering war.",
                "Crisis outcomes depend on bargaining leverage as well as material capability.",
                "Nuclear asymmetry matters more than nuclear possession alone.",
            ],
            "strengths": [
                "Explains why weak states may seek nuclear leverage.",
                "Connects nuclear politics to the same costly-signaling framework used elsewhere in the course.",
                "Distinguishes deterrence from compellence and bargaining success.",
                "Fits North Korea crisis bargaining and U.S. restraint.",
            ],
            "weaknesses": [
                "Actual nuclear use is so costly that threats may lack credibility.",
                "Symmetric nuclear crises can produce stalemate rather than clear advantage.",
                "Domestic politics and alliance guarantees can distort simple dyadic predictions.",
                "Selection into nuclear crises makes causal inference difficult.",
            ],
            "caption": "Mechanism: nuclear capability raises the opponent's expected cost of resisting. Key assumption: the target treats even low-probability escalation as politically intolerable. Strength/limit cue: strongest in asymmetric dyads, weaker when both sides can retaliate.",
            "visual_labels": ["Nuclear asymmetry", "Expected cost", "Concession", "Symmetry limit"],
            "references": [
                ref("Beardsley, K., & Asal, V. (2009). Winning with the bomb. <i>Journal of Conflict Resolution, 53</i>(2), 278-301. https://doi.org/10.1177/0022002708330386"),
                ref("Carpenter, T. G., & Bandow, D. (2004). <i>The Korean conundrum: America's troubled relations with North and South Korea</i>. Palgrave Macmillan."),
            ],
            "priority": True,
        },
        {
            "id": "w7_suicide_terrorism",
            "session": "W7.2",
            "title": "Strategic Logic of Suicide Terrorism",
            "author": "The Strategic Logic of Suicide Terrorism - Robert A. Pape",
            "situation": "The Tamil Tigers and Hamas used suicide attacks to convince democratic targets that continued military presence would be more costly than withdrawal.",
            "intuition": "Pape argues that suicide terrorism is strategic coercion, not simply irrational fanaticism. Suicide campaigns are designed to compel democratic states to withdraw military forces from territory the attackers treat as homeland. The tactic's brutality is part of its signal: organizations try to show that they can keep imposing civilian pain and that members are resolved enough to die for the campaign. For exam use, the narrow defensible claim is that foreign military occupation, especially by a democracy and across identity difference, can make suicide terrorism strategically attractive as a coercive tactic.",
            "concepts": [
                ("Suicide terrorism", "An attack in which the perpetrator's death is necessary for mission success."),
                ("Coercion", "Violence meant to change the target's policy, often by raising expected future costs."),
                ("Democratic vulnerability", "Pape's claim that democracies are more susceptible because civilian casualties generate public pressure."),
                ("Territorial concession", "The policy outcome suicide campaigns often seek: withdrawal from territory."),
                ("Costly signal", "The attack demonstrates resolve and willingness to absorb extreme costs."),
                ("Campaign", "A sustained sequence of attacks tied to an organizational political objective."),
            ],
            "assumptions": [
                "Terrorist organizations are strategic actors with political goals.",
                "Democratic targets respond to civilian casualty pressure.",
                "The group can sustain attacks long enough for coercive pressure to accumulate.",
                "The target can identify a concession, usually withdrawal, that would reduce attacks.",
            ],
            "strengths": [
                "Moves analysis away from pure fanaticism explanations.",
                "Connects terrorism to coercive bargaining and signaling.",
                "Explains why weaker actors target civilians in democracies.",
                "Provides concrete policy stakes around occupation and withdrawal.",
            ],
            "weaknesses": [
                "May overstate the causal role of occupation.",
                "Underplays organizational rivalry, ideology, and recruitment dynamics.",
                "Success is hard to measure when concessions have multiple causes.",
                "Policy implications depend heavily on research design.",
            ],
            "caption": "Mechanism: suicide attacks signal resolve and impose civilian costs to compel withdrawal. Key assumption: democratic publics translate civilian pain into policy pressure. Strength/limit cue: powerful strategic reframing, but causality depends on comparison cases.",
            "visual_labels": ["Occupation", "Suicide signal", "Public cost", "Withdrawal?"],
            "references": [
                ref("Pape, R. A. (2003). The strategic logic of suicide terrorism. <i>American Political Science Review, 97</i>(3), 343-361. https://doi.org/10.1017/S000305540300073X"),
            ],
            "priority": True,
        },
        {
            "id": "w7_design_inference",
            "session": "W7.3",
            "title": "Design, Inference, and Selection Bias",
            "author": "Design, Inference, and the Strategic Logic of Suicide Terrorism - Scott Ashworth, Joshua D. Clinton, Adam Meirowitz & Kristopher W. Ramsay; Pape reply",
            "situation": "If we only study suicide attacks, we cannot know why some occupied groups choose suicide tactics while others resist without suicide terrorism.",
            "intuition": "Ashworth and coauthors do not mainly offer a rival terrorism theory; they teach a research-design warning. Pape's suicide-terrorism data sample on the dependent variable, meaning the data include cases where suicide terrorism occurred but not comparable cases where groups faced occupation and did not use suicide tactics. That design can describe observed suicide campaigns, but it cannot identify the risk of suicide terrorism or the causes of tactic adoption. Pape's reply narrows the claim by defending the universe of suicide terrorism and later comparisons. For GPCO 410, this is the methodological page: patterns among observed cases are not automatically causal mechanisms.",
            "concepts": [
                ("Sampling on the dependent variable", "Studying only cases where the outcome occurred, making causes hard to identify."),
                ("Comparison set", "The non-outcome cases needed to estimate risk or causal effect."),
                ("Bounds", "Limits on what can be inferred from incomplete designs."),
                ("Causal inference", "The step from association to a credible claim about what produced the outcome."),
                ("Universe of cases", "The full population the analyst claims to study."),
                ("Policy inference", "A recommendation that can fail if based on a biased design."),
            ],
            "assumptions": [
                "Causal claims require variation in both outcome and non-outcome cases.",
                "Observed patterns can be descriptive without being causal.",
                "Policy prescriptions depend on knowing how risk changes across choices.",
                "The relevant unit is often the organization or occupation case, not the individual attack.",
            ],
            "strengths": [
                "Provides a clean methodological check for all empirical readings.",
                "Prevents overclaiming from dramatic cases.",
                "Shows why case selection matters for security policy.",
                "Pairs well with Blattman and Miguel's causality cautions.",
            ],
            "weaknesses": [
                "Does not itself explain why terrorism occurs.",
                "Can feel negative if not paired with an alternative design.",
                "May understate the value of complete descriptive data on rare events.",
                "Requires technical care to explain under exam time limits.",
            ],
            "caption": "Mechanism: missing non-suicide comparison cases block causal inference. Key assumption: observed and unobserved groups differ in ways that matter. Strength/limit cue: excellent design critique, but not a substantive terrorism mechanism by itself.",
            "visual_labels": ["Observed attacks", "Missing cases", "Inference bound", "Policy risk"],
            "references": [
                ref("Ashworth, S., Clinton, J. D., Meirowitz, A., & Ramsay, K. W. (2008). Design, inference, and the strategic logic of suicide terrorism. <i>American Political Science Review, 102</i>(2), 269-273. https://doi.org/10.1017/S0003055408080167"),
                ref("Pape, R. A. (2008). Methods and findings in the study of suicide terrorism. <i>American Political Science Review, 102</i>(2), 275-277. https://doi.org/10.1017/S0003055408080179"),
            ],
            "priority": True,
        },
        {
            "id": "w8_terrorism_strategies",
            "session": "W8.1",
            "title": "Kydd and Walter's Five Terrorism Strategies",
            "author": "The Strategies of Terrorism - Andrew H. Kydd & Barbara F. Walter",
            "situation": "Al-Qaida's 9/11 attacks can be read as both attrition against U.S. presence and provocation designed to produce a broad U.S. military response.",
            "intuition": "Kydd and Walter define terrorism as strategic costly signaling by weak actors. Terrorist groups lack the power to impose outcomes directly, so they try to manipulate beliefs of governments, civilians, rival groups, or supporters. Their five strategies are attrition, intimidation, provocation, spoiling, and outbidding. The core exam move is diagnostic: identify which audience the violence targets and which belief it is meant to change. Counterterrorism fails when states answer the wrong strategy, such as using indiscriminate force against provocation or treating outbidding as simple attrition.",
            "concepts": [
                ("Attrition", "Convince the target that continuing a policy is too costly."),
                ("Intimidation", "Convince civilians that the group can punish disobedience and the state cannot protect them."),
                ("Provocation", "Trigger state overreaction that radicalizes the group's constituency."),
                ("Spoiling", "Undermine trust in peace talks or moderates."),
                ("Outbidding", "Prove greater resolve than rival groups to win constituency support."),
                ("Audience split", "Different terrorist strategies signal to different audiences."),
            ],
            "assumptions": [
                "Terrorist groups are too weak to win by direct force.",
                "Violence can alter beliefs despite moral revulsion.",
                "Targets and constituencies update from costly attacks.",
                "Groups choose tactics with an audience and political goal in mind.",
            ],
            "strengths": [
                "Gives a usable five-part diagnostic for terrorism cases.",
                "Links terrorism directly to signaling theory.",
                "Produces strategy-specific policy responses.",
                "Explains why state overreaction can help terrorists.",
            ],
            "weaknesses": [
                "Real attacks can serve multiple strategies at once.",
                "Organizations may be factional, ideological, or opportunistic.",
                "Audience reactions are difficult to predict.",
                "Moral and psychological dynamics are secondary to strategy.",
            ],
            "caption": "Mechanism: violence changes beliefs for a specific audience. Key assumption: the audience can interpret the signal and alter behavior. Strength/limit cue: strong diagnostic typology, but attacks often combine strategies.",
            "visual_labels": ["Attrition", "Provocation", "Spoiling", "Outbidding"],
            "references": [
                ref("Kydd, A. H., & Walter, B. F. (2006). The strategies of terrorism. <i>International Security, 31</i>(1), 49-80. https://doi.org/10.1162/isec.2006.31.1.49"),
            ],
            "priority": True,
        },
        {
            "id": "w8_stein_regimes",
            "session": "W8.2",
            "title": "Regimes: Coordination vs. Collaboration",
            "author": "Coordination and Collaboration: Regimes in an Anarchic World - Arthur A. Stein",
            "situation": "NATO members need coordination to standardize expectations and collaboration to stop free-riding on collective defense.",
            "intuition": "Stein argues that regimes emerge when self-interested states shift from independent to joint decision-making. The reason depends on the game structure. Dilemmas of common interests require collaboration because actors want a cooperative outcome but each has incentive to defect or free ride. Dilemmas of common aversions require coordination because actors primarily need convergent expectations to avoid a mutually bad outcome. This distinction helps prevent lazy institution talk: some institutions need monitoring and enforcement, while others mainly need shared rules and focal points.",
            "concepts": [
                ("Regime", "A move from independent to joint decision-making under agreed rules."),
                ("Common interests", "Actors prefer mutual cooperation but face incentives to cheat."),
                ("Collaboration", "Institutionalized cooperation requiring monitoring or enforcement."),
                ("Common aversions", "Actors disagree over ideals but share a desire to avoid a bad outcome."),
                ("Coordination", "Converging on expectations, standards, or rules."),
                ("Free-riding", "Enjoying collective benefits while undercontributing."),
            ],
            "assumptions": [
                "States are self-interested actors under anarchy.",
                "Institutions arise because they solve strategic problems, not because states become altruistic.",
                "The analyst can distinguish cheating incentives from expectation-alignment problems.",
                "Joint decision-making can improve payoffs relative to independent action.",
            ],
            "strengths": [
                "Clear typology for international institutions.",
                "Explains why different problems require different institutional designs.",
                "Fits NATO, arms control, standards, and trade regimes.",
                "Works well with game-theory foundations.",
            ],
            "weaknesses": [
                "Real regimes mix coordination and collaboration.",
                "Domestic ratification and institutional politics can be underplayed.",
                "The theory can make regime creation look smoother than it is.",
                "Power asymmetries may shape which rules become focal.",
            ],
            "caption": "Mechanism: regimes change independent choices into joint decisions. Key assumption: actors can identify whether the obstacle is cheating or miscoordination. Strength/limit cue: elegant typology, but real institutions often mix both dilemmas.",
            "visual_labels": ["Common interest", "Collaboration", "Common aversion", "Coordination"],
            "references": [
                ref("Stein, A. A. (1982). Coordination and collaboration: Regimes in an anarchic world. <i>International Organization, 36</i>(2), 299-324. https://doi.org/10.1017/S0020818300018968"),
            ],
            "priority": True,
        },
        {
            "id": "w8_gourevitch_governance",
            "session": "W8.3",
            "title": "The Governance Problem",
            "author": "The Governance Problem in International Relations - Peter A. Gourevitch",
            "situation": "Turkey's delay of Finland and Sweden's NATO accession shows how consensus rules become bargaining leverage once institutional rules distribute power.",
            "intuition": "Gourevitch warns that institutions are not neutral containers. If rules shape outcomes, actors will fight over rules. The governance problem is therefore the politics of institutional design, control, vetoes, thresholds, agenda power, and enforcement. Strong institutions can channel conflict through procedures; weak or contested institutions push actors back toward bargaining power, persuasion, or violence. In collective security, the key question is not only whether members share a goal, but who controls the rules through which that goal is pursued.",
            "concepts": [
                ("Governance problem", "Conflict over the rules that govern collective action."),
                ("Rules as distributive objects", "Procedures allocate power and benefits, so actors contest them."),
                ("Veto leverage", "The ability to block an institutional outcome to extract concessions."),
                ("Institutional design", "The choice of rules, thresholds, authority, and enforcement procedures."),
                ("Rule contestation", "Political struggle over how the institution itself works."),
                ("Process broker", "An actor such as a secretary general who manages institutional bargaining."),
            ],
            "assumptions": [
                "Actors understand that rules affect payoffs.",
                "Institutions have distributive consequences.",
                "Power can operate through procedure, not only material force.",
                "Rules are stable enough to matter but contested enough to be political.",
            ],
            "strengths": [
                "Explains bargaining inside institutions rather than outside them.",
                "Clarifies why vetoes and procedures matter.",
                "Pairs naturally with Stein's regime theory.",
                "Excellent for NATO accession and collective-security cases.",
            ],
            "weaknesses": [
                "May understate norm internalization and institutional loyalty.",
                "Can make all institutional behavior look self-interested.",
                "Needs a concrete rule to avoid becoming vague.",
                "Does not alone predict which actor wins the governance fight.",
            ],
            "caption": "Mechanism: because rules distribute payoffs, actors bargain over the rules. Key assumption: procedural power is valuable and recognized. Strength/limit cue: strong for veto politics, weaker for norm-driven compliance.",
            "visual_labels": ["Rule", "Veto", "Bargain", "Outcome"],
            "references": [
                ref("Gourevitch, P. A. (1999). The governance problem in international relations. In D. A. Lake & R. Powell (Eds.), <i>Strategic choice and international relations</i> (pp. 137-164). Princeton University Press."),
            ],
            "priority": True,
        },
        {
            "id": "w9_lake_statebuilding",
            "session": "W9",
            "title": "Statebuilding, Legitimacy, and the Statebuilder's Dilemma",
            "author": "Building Legitimate States, Ch. 1 - David A. Lake",
            "situation": "Post-2003 Iraq shows why external statebuilding fails when the intervener's strategic interests pull the host government away from a domestically legitimate social order.",
            "intuition": "Lake argues that statebuilding requires both a monopoly on violence and legitimacy. Legitimacy is built when groups vest relationally specific assets in a social order and become a compliance constituency that defends it. External statebuilders can help by guaranteeing order near the host society's political center, but they face a dilemma: any actor willing to pay the high cost of statebuilding usually has strategic interests, so it backs loyalists who undermine local legitimacy. Exit deadlines then make the problem worse by discouraging long-term investment in the new order.",
            "concepts": [
                ("Monopoly on violence", "The state's effective control over coercive force."),
                ("Legitimacy", "Quasi-voluntary compliance rooted in ideological and vested interests."),
                ("Relationally specific assets", "Investments valuable under a particular social order and costly to move elsewhere."),
                ("Compliance constituency", "Groups that defend a regime because their assets are vested in it."),
                ("Predatory state", "Monopoly on violence without legitimacy."),
                ("Factionalized state", "Legitimacy claims without a stable monopoly on violence."),
                ("Statebuilder's dilemma", "External strategic interests undermine the legitimacy they need to build."),
            ],
            "assumptions": [
                "Durable states need both coercive capacity and legitimacy.",
                "Actors invest when they believe the social order will endure.",
                "External statebuilders are strategic, not neutral.",
                "Exit timelines affect local expectations and investment.",
            ],
            "strengths": [
                "Connects state capacity to legitimacy and investment behavior.",
                "Explains why foreign statebuilding often fails despite resources.",
                "Gives a useful state typology for Iraq, Somalia, and Myanmar.",
                "Pairs well with Walter's third-party guarantee problem.",
            ],
            "weaknesses": [
                "Can economize legitimacy in ways that underplay identity and memory.",
                "External neutrality may be impossible in practice.",
                "The theory is strongest at high-level diagnosis, less detailed on local institution design.",
                "Compliance constituencies can also defend exclusionary orders.",
            ],
            "caption": "Mechanism: legitimacy grows when actors vest assets in a durable order. Key assumption: the statebuilder can credibly guarantee that order. Strength/limit cue: explains intervention failure, but legitimacy is not only economic investment.",
            "visual_labels": ["Monopoly", "Legitimacy", "Vesting", "Dilemma"],
            "references": [
                ref("Lake, D. A. (2016). <i>The statebuilder's dilemma: On the limits of foreign intervention</i>. Cornell University Press."),
            ],
            "priority": True,
        },
        {
            "id": "w10_institutions_constraints",
            "session": "W10",
            "title": "Institutions as Constraints on Strategic Choice",
            "author": "Institutions as Constraints on Strategic Choice - Ronald Rogowski",
            "situation": "A leader's foreign-policy strategy is filtered through domestic institutions that aggregate interests, constrain choices, and sometimes survive even when they are inefficient.",
            "intuition": "Rogowski asks whether institutions independently affect foreign policy or merely reflect deeper material pressures. Realist logic expects bad institutions to reform or perish under international competition. Rogowski's counterpoint is that competition is often not ruthless enough to eliminate inefficient institutions quickly, so domestic rules can persist and shape strategy. Institutions aggregate preferences, structure veto points, and constrain leaders' feasible choices. This closes the course loop: strategic choice still matters, but strategies are chosen inside institutional environments that are partly sticky, political, and historically inherited.",
            "concepts": [
                ("Institutional constraint", "A domestic or organizational rule that limits feasible strategies."),
                ("Preference aggregation", "How individual or group interests become policy."),
                ("Endogenous institutions", "Rules shaped by deeper power, technology, or competition."),
                ("Exogenous institutions", "Rules treated as independent constraints for a given analysis."),
                ("Veto point", "A procedural barrier that can block or reshape policy."),
                ("Institutional persistence", "The survival of rules even when they are inefficient or maladapted."),
            ],
            "assumptions": [
                "Institutions can be sticky over the time horizon being studied.",
                "Foreign policy is made through domestic aggregation and constraint.",
                "International competition is not always strong enough to erase inefficient rules.",
                "Analysts must decide whether institutions are causes or outcomes in the model.",
            ],
            "strengths": [
                "Brings domestic institutions back into strategic choice.",
                "Prevents treating the state as a frictionless unitary actor.",
                "Links public opinion, selectorate logic, and governance rules.",
                "Useful for final-exam questions asking how institutions shape strategy.",
            ],
            "weaknesses": [
                "Can be hard to separate institutional effect from underlying preferences.",
                "Risk of treating institutions as both cause and outcome.",
                "Less predictive without specifying which institutional rule matters.",
                "Short-run constraints and long-run adaptation can point in different directions.",
            ],
            "caption": "Mechanism: institutions aggregate preferences and narrow feasible strategies. Key assumption: rules persist long enough to constrain choice. Strength/limit cue: restores domestic politics, but causal direction can blur.",
            "visual_labels": ["Preferences", "Institutions", "Strategy set", "Foreign policy"],
            "references": [
                ref("Rogowski, R. (1999). Institutions as constraints on strategic choice. In D. A. Lake & R. Powell (Eds.), <i>Strategic choice and international relations</i> (pp. 115-136). Princeton University Press."),
            ],
            "priority": True,
        },
    ])
    return theories


styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=DARK_NAVY, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=9.4, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=8))
styles.add(ParagraphStyle("Box", parent=styles["Normal"], fontSize=8.2, leading=10.4, textColor=colors.HexColor("#222222")))
styles.add(ParagraphStyle("TOC", parent=styles["Normal"], fontSize=7.8, leading=9.2, leftIndent=9, firstLineIndent=-9, spaceAfter=0.3))
styles.add(ParagraphStyle("Header", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=colors.white))
styles.add(ParagraphStyle("HeaderSub", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=7.4, leading=8.8, textColor=colors.HexColor("#EAF2FF")))
styles.add(ParagraphStyle("Section", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=9.5, leading=11, textColor=DARK_NAVY, spaceBefore=5, spaceAfter=2))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=8.7, leading=10.6, spaceAfter=3))
styles.add(ParagraphStyle("Caption", parent=styles["Normal"], fontSize=7.2, leading=8.7, textColor=colors.HexColor("#333333"), spaceAfter=3))
styles.add(ParagraphStyle("TheoryBullet", parent=styles["Normal"], fontSize=8.2, leading=9.8, leftIndent=9, firstLineIndent=-6, spaceAfter=1.3))
styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=6.8, leading=8, textColor=colors.HexColor("#555555")))
styles.add(ParagraphStyle("Ref", parent=styles["Normal"], fontSize=7.4, leading=8.8, leftIndent=9, firstLineIndent=-9, spaceAfter=1.6))


def p(txt, style="Body"):
    return Paragraph(txt.replace("&", "&amp;"), styles[style])


def bullet_items(items):
    return [Paragraph(f"- <b>{term}</b> - {body}", styles["TheoryBullet"]) for term, body in items]


def plain_bullets(items):
    return [Paragraph(f"- {item}", styles["TheoryBullet"]) for item in items]


def header_table(t):
    data = [[Paragraph(f"{t['session']} - {t['title']}", styles["Header"])], [Paragraph(t["author"], styles["HeaderSub"])]]
    tbl = Table(data, colWidths=[7.05 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MED_BLUE if t["priority"] else DARK_NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tbl


def section(title, flowables):
    return [Paragraph(title, styles["Section"])] + flowables


def font(size=34, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_centered(draw, xy, text, fnt, fill):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2), text, font=fnt, fill=fill)


def make_visual(t):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / f"{t['id']}.png"
    w, h = 1600, 900
    img = PILImage.new("RGB", (w, h), "#F7FAFC")
    d = ImageDraw.Draw(img)
    navy = "#1B2A4A"
    blue = "#2C5282"
    gold = "#C69C3F"
    grey = "#D8DEE9"
    dark = "#1F2937"
    title_font = font(42, True)
    label_font = font(33, True)
    small_font = font(24)

    d.rectangle([0, 0, w, 96], fill=navy)
    d.text((48, 28), t["title"][:62], font=title_font, fill="white")
    d.text((48, 112), "mechanism map", font=small_font, fill=blue)

    labels = (t.get("visual_labels") or ["Actor", "Choice", "Belief", "Outcome"])[:4]
    xs = [230, 610, 990, 1370]
    y = 405
    for i, (x, label) in enumerate(zip(xs, labels)):
        fill = "#FFFFFF" if i != 2 else "#FFF5E6"
        outline = blue if i != 3 else gold
        d.rounded_rectangle([x - 150, y - 88, x + 150, y + 88], radius=22, fill=fill, outline=outline, width=5)
        wrapped = textwrap.wrap(label, width=16)[:2]
        for j, line in enumerate(wrapped):
            draw_centered(d, (x, y - 14 + j * 38), line, label_font, dark)
        if i < 3:
            d.line([x + 160, y, xs[i + 1] - 165, y], fill=gold, width=7)
            d.polygon([(xs[i + 1] - 165, y), (xs[i + 1] - 190, y - 15), (xs[i + 1] - 190, y + 15)], fill=gold)

    d.rounded_rectangle([105, 665, 1495, 800], radius=18, fill="#EBF4FF", outline=grey, width=3)
    caption = t["caption"].split(" Strength/limit cue:")[0].replace("Mechanism: ", "")
    for i, line in enumerate(textwrap.wrap(caption, width=94)[:3]):
        d.text((145, 690 + i * 32), line, font=small_font, fill=dark)
    d.text((145, 825), "Assumption + limit are stated in the image caption below the figure.", font=font(20), fill="#4B5563")
    img.save(path)
    return path


def visual_block(t):
    asset = make_visual(t)
    image = Image(str(asset), width=7.05 * inch, height=3.97 * inch)
    return [
        image,
        Spacer(1, 4),
        Paragraph(t["caption"], styles["Caption"]),
        Paragraph(f"Asset: {ASSET_DISPLAY_DIR}/{asset.name}", styles["Small"]),
    ]


def theory_pages(t):
    page_a = [
        BookmarkAnchor(t["id"], f"{t['session']} - {t['title']}"),
        header_table(t),
        Spacer(1, 5),
    ]
    page_a += section("SITUATION", [p(t["situation"])])
    page_a += section("CORE INTUITION", [p(t["intuition"])])
    page_a += section("EXPLANATORY IMAGE", visual_block(t))

    page_b = [header_table({**t, "title": t["title"] + " (Reference Page)"})]
    page_b += section("KEY CONCEPTS, KEYWORDS & TERMINOLOGY", bullet_items(t["concepts"]))
    page_b += section("ASSUMPTIONS", plain_bullets(t["assumptions"]))
    col_w = (7.05 * inch - 8) / 2
    strengths = [Paragraph("<b>Strengths</b>", styles["Body"])] + plain_bullets(t["strengths"])
    weaknesses = [Paragraph("<b>Weaknesses / Limits</b>", styles["Body"])] + plain_bullets(t["weaknesses"])
    sw = Table([[strengths, weaknesses]], colWidths=[col_w, col_w])
    sw.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
        ("BACKGROUND", (1, 0), (1, 0), WARM_AMBER),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ("LINEAFTER", (0, 0), (0, -1), 0.5, BORDER_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    page_b += [Paragraph("STRENGTHS / WEAKNESSES", styles["Section"]), sw]
    page_b += section("APA REFERENCE ANCHORS", [Paragraph(r, styles["Ref"]) for r in t["references"]])
    return page_a + [PageBreak()] + page_b


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(doc.leftMargin, 0.38 * inch, TITLE)
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_notes(theories):
    lines = [
        "# GPCO 410 Theory Reference v1.0.0 - Source Notes",
        "",
        "## Deliverable",
        f"- PDF: `{OUT.name}`",
        f"- Builder: `{Path(__file__).name}`",
        f"- Asset folder: `{ASSET_DISPLAY_DIR}/`",
        "- Scope: comprehensive course theory/reference guide in syllabus order, using the existing midterm theory reference as the W1-W5 starting point and adding late-quarter units from local course guides/readings.",
        "",
        "## Inventory",
    ]
    for t in theories:
        lines.append(f"- {t['session']}: {t['title']} -- {t['author']}")
    lines += [
        "",
        "## Files Checked",
        "- `Course Admin/syllabus_extracted.md`",
        "- `Study Guides/GPCO410_Midterm_Theory_Reference_v1.3.1_notes.md`",
        "- `Study Guides/build_midterm_theory_reference.py`",
        "- `Study Guides/2026-05-11_gpco410_week7_nuclear_terrorism_1pager.md`",
        "- `Study Guides/2026-05-18_gpco410_week8_terrorism_collective_security_1pager.md`",
        "- `Study Guides/2026-05-20_gpco410_week8_terrorism_collective_security_class_prep.md`",
        "- `Study Guides/2026-05-27_lake_building_legitimate_states_ch1_summary.md`",
        "- `_agent/THEORIES.md`, `_agent/AGENT_CONTEXT.md`, `_agent/FEEDBACK.md`",
        "",
        "## Verification",
        "- Built with ReportLab.",
        "- One generated PNG explanatory image per theory unit.",
        "- Two pages of space per theory unit.",
        "",
        "---",
        "Generated for: Edgar Agunias",
        f"Date: {DATE}",
        f"Model: {MODEL}",
        "Sources: GPCO 410 syllabus extraction, existing midterm theory reference builder/notes, Athena memory, late-quarter local study guides and readings",
        "Agent: Athena",
        "---",
    ]
    NOTES_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build():
    theories = build_theories()
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
        "Comprehensive course theory reference built from the existing W1-W5 midterm reference and late-quarter GPCO 410 study materials. Each theory receives two pages: a mechanism/intuitive page with an explanatory image, followed by a reference page with deployable terms, assumptions, strengths, limits, and APA anchors. Calibrated for Praether/Ali's strategic-choice grammar: actors, preferences, strategies, beliefs, payoffs, and the no-deal mechanism.",
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
    story += [box, Spacer(1, 5), Paragraph("Table of Contents", styles["Section"])]
    for t in theories:
        story.append(Paragraph(f'<a href="#{t["id"]}">{t["session"]} - {t["title"]}</a>', styles["TOC"]))
    story += [
        Spacer(1, 5),
        HRFlowable(width="35%", thickness=0.5, color=BORDER_GREY, hAlign="LEFT"),
        Paragraph(
            f"Generated with {MODEL} via the Claudia agent system. Prepared for Edgar Agunias, {COURSE}, Prof. Lauren Prather, UC San Diego GPS. Always verify against official course materials and assigned readings. This document is a study aid and does not substitute for careful reading of the assigned texts.",
            styles["Small"],
        ),
        PageBreak(),
    ]
    for idx, t in enumerate(theories):
        if idx:
            story.append(PageBreak())
        story.extend(theory_pages(t))

    all_refs = []
    seen = set()
    for t in theories:
        for r in t["references"]:
            plain = r.replace("<i>", "").replace("</i>", "")
            if plain not in seen:
                all_refs.append(r)
                seen.add(plain)
    story += [
        PageBreak(),
        Paragraph("References", ParagraphStyle("RefsTitle", parent=styles["Heading1"], textColor=DARK_NAVY, fontSize=16, leading=19)),
        Spacer(1, 8),
    ]
    story += [Paragraph(r, styles["Ref"]) for r in sorted(all_refs, key=lambda x: x.replace("<i>", "").split(",")[0])]
    story += [
        Spacer(1, 12),
        HRFlowable(width="35%", thickness=0.5, color=BORDER_GREY, hAlign="LEFT"),
        Paragraph("---", styles["Small"]),
        Paragraph("Generated for: Edgar Agunias", styles["Small"]),
        Paragraph(f"Date: {DATE}", styles["Small"]),
        Paragraph(f"Model: {MODEL}", styles["Small"]),
        Paragraph("Sources: GPCO 410 syllabus extraction; existing midterm theory reference v1.3.1 notes and builder; Athena AGENT_CONTEXT, FEEDBACK, and THEORIES; late-quarter local study guides/readings for nuclear coercion, terrorism, regimes, governance, statebuilding, and institutions.", styles["Small"]),
        Paragraph("Agent: Athena", styles["Small"]),
        Paragraph("---", styles["Small"]),
    ]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    build_notes(theories)


if __name__ == "__main__":
    build()
