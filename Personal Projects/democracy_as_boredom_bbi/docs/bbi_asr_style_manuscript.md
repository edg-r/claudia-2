# Democracy as Boredom: Measuring Institutional Constraint in Presidential Speech

Edgar Agunias  
University of California, San Diego

## Abstract

Research on democratic erosion often measures the language of danger: populism, nationalism, authoritarianism, crisis, enemies, and personalist legitimation. Less attention has been paid to the opposite rhetorical form, the ordinary institutional language through which constrained executives justify action. This paper develops a pilot measure, the Bureaucratic Boredom Index (BBI), to capture procedural, administrative, and legalistic language in U.S. presidential speech. Drawing on 309 inaugural addresses and State of the Union documents from the American Presidency Project, I construct two transparent dictionaries: one for procedural constraint language and one for charismatic sovereignty language. The main score subtracts standardized charismatic language from standardized procedural language. Results show that State of the Union documents score substantially higher than inaugural addresses, that major-war periods are associated with lower BBI scores, and that the highest-scoring speeches are often administratively specific policy messages. These findings do not show that the BBI measures democracy directly. Rather, they suggest that institutional constraint may leave a measurable rhetorical trace in the mundane language of agencies, budgets, law, reports, programs, and implementation.

**Keywords:** democracy, presidential rhetoric, text as data, institutions, populism, political sociology

## Introduction

Democracy is usually measured through institutions: elections, rights, judicial independence, legislative oversight, civil liberties, and constraints on executive power. These measures are indispensable. Yet democracy also has a rhetorical dimension. It does not only structure who gets power. It structures how power must justify itself. A constrained executive must speak through institutions, procedures, agencies, budgets, legal authority, and implementation. A less constrained or more personalistic executive has stronger incentives to speak through destiny, unity, crisis, enemies, betrayal, and direct identification with "the people."

This paper develops a pilot measure of that difference. I call the measure the Bureaucratic Boredom Index (BBI). The phrase is intentionally plain. The index is not designed to valorize dull speech or to claim that boredom is democratic in itself. Rather, it treats bureaucratic language as a possible textual trace of institutional constraint. In democratic settings, executive power often has to pass through statutes, courts, committees, appropriations, agencies, regulations, audits, reports, and programs. These are not the charismatic materials of political drama. They are the language of constrained authority.

The contribution is conceptual and methodological. Existing speech-based measures are often strongest at detecting illiberal or personalist language. They identify threats, enemies, populist claims, authoritarian discourse, or the leader's direct bond with the people. The BBI reverses the question. Instead of asking whether leaders sound dangerous, it asks whether leaders sound institutionally constrained. Can we measure the procedural rhetoric through which executive action is represented as legal, administrative, accountable, and implementable?

I test this approach on a U.S. presidential corpus. The United States is not a cross-national test of democracy. It is a pilot case with a long speech record, stable constitutional institutions, major changes in the administrative state, and recurrent crises. Using 309 speeches from 1789 to 2026, I score inaugural addresses and State of the Union documents for procedural constraint language and charismatic sovereignty language. I then examine differences across speech type, historical time, divided government, war periods, and recession periods.

The findings are preliminary but suggestive. State of the Union documents score much higher than inaugural addresses. Major-war periods are associated with lower BBI scores, consistent with the expectation that presidents turn toward existential and charismatic language during national emergencies. Divided government is positively associated with BBI in the preliminary model, though only weakly. Recession periods do not show a clear negative relationship. The strongest result is genre: institutional reporting and policy messages are more bureaucratically boring than inaugural performances of national unity.

The point is not that high BBI proves democracy or that low BBI proves authoritarianism. The point is narrower: democratic constraint may discipline executive rhetoric into recognizable procedural forms. Measuring those forms can help identify the positive, institutional side of democratic language, not just its breakdown.

## Presidential Speech and Institutional Constraint

Political sociology and political science have long treated speech as more than ornament. Presidential rhetoric helps construct publics, define crises, assign responsibility, and legitimate authority. Work on the rhetorical presidency shows that U.S. presidential speech changes systematically over time. Lim (2002) argues that presidential rhetoric became more conversational, assertive, democratic, abstract, and anti-intellectual across American history. Savoy (2017) similarly demonstrates that presidential style can be studied computationally over long periods. These studies establish presidential speech as a measurable corpus, but they are not primarily designed to capture institutional constraint.

Research on populism and authoritarian discourse moves closer to the question of democratic erosion. Bonikowski and Gidron (2016) treat populism as a measurable style rather than a fixed leader identity. Bonikowski, Luo, and Stuhler (2022) extend this logic by measuring populism, nationalism, and authoritarianism in U.S. campaign rhetoric with neural language models. Cross-national projects such as the Global Populism Database show that leader speech can be coded comparatively for people-versus-elite claims, moralized anti-establishment rhetoric, and crisis framing.

Related work on personalist legitimation and authoritarian discourse also links speech to executive constraint. Brunkert and von Soest (2023) show that personalist legitimacy claims can anticipate deterioration in executive constraints. Mochtak (2025) develops a language-model approach to detecting authoritarian discourse in political speeches. These studies are valuable precisely because leaders reveal something about power through how they justify it.

The BBI builds from this literature but shifts the measurement target. Most speech measures of democratic danger detect charismatic, illiberal, nationalist, or personalist rhetoric. The BBI asks whether constrained rule has its own detectable rhetoric. If charismatic sovereignty language elevates destiny, greatness, betrayal, enemies, crisis, restoration, and the people as a unified body, procedural constraint language points to Congress, law, courts, statutes, agencies, budgets, implementation, oversight, reports, programs, federalism, consultation, and compliance.

This inversion matters because democratic stability may be rhetorically ordinary. The language of constraint is often unglamorous. It appears in the forms of rule-governed action: reporting to Congress, asking for appropriations, implementing programs, complying with law, coordinating agencies, reviewing regulations, and evaluating outcomes. These practices are not democracy in themselves. Bureaucratic authoritarian regimes can also speak administratively. But in a democratic setting, procedural language can mark the channels through which executive power is disciplined.

## Hypotheses

The analysis is organized around four expectations.

**Institutional Constraint Hypothesis.** Presidents operating under stronger institutional constraint should produce higher BBI scores because they must justify action through institutions, procedures, oversight, and implementation.

**Crisis Rhetoric Hypothesis.** Crisis and war periods should reduce BBI scores because presidents use more existential, charismatic, and national-unity language during emergencies.

**Administrative State Hypothesis.** Modern presidents should use more procedural language than early presidents because the administrative state expanded over time.

**Personalism Hypothesis.** More personalistic rhetorical moments should score lower on BBI than institutionally deferential moments, even within the same constitutional system.

These hypotheses are not tests of regime type. They are tests of whether the BBI behaves in ways consistent with a theory of rhetorical institutional constraint.

## Data and Measures

The corpus contains 309 U.S. presidential speeches from the American Presidency Project. It includes 63 inaugural addresses and 246 State of the Union or written annual message documents from 1789 to 2026. Each observation includes president, date, year, title, speech type, source URL, raw text, cleaned text, word count, and BBI scoring fields.

I added contextual metadata after the initial scoring pipeline. Presidential party is coded from Britannica's presidents table. Congress control is coded from the Wikipedia table on party divisions of United States Congresses, producing a divided or unified government indicator. Recession is coded from the FRED USREC monthly recession indicator. GDP is coded from FRED quarterly GDP in current-dollar billions, using the nearest prior quarter. Major-war periods are manually coded date intervals for major U.S. wars, including the War of 1812, Mexican-American War, Civil War, Spanish-American War, World War I, World War II, Korean War, Vietnam War, Persian Gulf War, Afghanistan War, and Iraq War.

Metadata coverage is uneven by design. Party is populated for all 309 speeches. Congress control status is populated for all 309 speeches. Major-war status is populated for all 309 speeches, with 59 speeches falling in a major-war period. Recession status is available for 226 speeches, reflecting the FRED historical series. GDP is available for 110 speeches, beginning in 1947. GDP is therefore exported for future analysis but not used in the main model table.

The BBI uses two transparent dictionaries. The procedural constraint dictionary includes terms such as law, constitution, court, Congress, committee, statute, implementation, regulation, budget, appropriation, oversight, audit, report, review, agency, federal, state, local, program, evaluation, compliance, consultation, bipartisan, amendment, authorization, interagency, and administrative. The charismatic sovereignty dictionary includes terms such as destiny, rebirth, greatness, betrayal, enemy, sacrifice, glory, humiliation, corrupt, purity, strength, weakness, crisis, invasion, threat, restore, save, movement, loyalty, will of the people, the people, national will, enemies within, and foreign enemies.

For each speech, I calculate procedural and charismatic term counts per 1,000 words. The main index is:

```text
BBI_z = z(procedural terms per 1,000 words) - z(charismatic terms per 1,000 words)
```

Higher scores indicate more procedural constraint language relative to charismatic sovereignty language. Lower scores indicate more charismatic sovereignty language relative to procedural constraint language.

## Analytic Strategy

The analysis proceeds in three steps. First, I describe the distribution of BBI scores across speech types and historical contexts. Second, I inspect the highest and lowest scoring speeches as a validation check. Third, I estimate preliminary linear models predicting BBI. The first model uses year and speech type. The second uses president and speech type. The third uses divided government, major-war period, recession indicator, and speech type. Separate models predict procedural language and charismatic language as dependent variables.

These models are descriptive. The corpus is U.S.-only, and the metadata are not designed for causal identification. Speech type is also a major source of confounding: inaugural addresses and State of the Union documents are institutionally different genres. The models are therefore best read as checks on whether BBI behaves plausibly, not as causal estimates of institutional constraint.

## Findings

### Speech Type Is the Clearest Divide

State of the Union documents are much more bureaucratically boring than inaugural addresses. The mean BBI for inaugural addresses is -1.66, compared with 0.43 for State of the Union documents. This difference is substantively large and theoretically sensible. Inaugural addresses are ritual performances of national meaning. They are built for unity, destiny, collective renewal, and presidential voice. State of the Union documents are more often reports, policy agendas, budgetary appeals, and administrative accounts. They are structurally closer to the institutional work of governing.

The component scores show the same pattern. Inaugural addresses average 7.27 procedural terms per 1,000 words and 8.22 charismatic terms per 1,000 words. State of the Union documents average 14.0 procedural terms per 1,000 words and 4.95 charismatic terms per 1,000 words. The BBI is therefore not only picking up more procedural language in State of the Union documents. It is also picking up less charismatic sovereignty language.

This finding supports the core idea that institutional genre matters. The same presidency can speak in different rhetorical registers depending on whether the president is performing national unity or reporting through institutions.

![Figure 1. Bureaucratic Boredom Index by speech type.](../outputs/figures/05_bbi_by_speech_type.png)

![Figure 2. Bureaucratic Boredom Index over time.](../outputs/figures/01_bbi_over_time.png)

### Major-War Periods Lower BBI

The strongest contextual result concerns war. Speeches outside major-war periods average 0.26 on BBI. Speeches during major-war periods average -1.09. In the preliminary regression model, the major-war indicator is associated with a 1.28-point decrease in BBI, net of speech type, divided government, and recession. The estimate is statistically clear in this descriptive model.

This pattern is consistent with the crisis rhetoric hypothesis. War draws presidents toward language of threat, sacrifice, national will, strength, weakness, and collective destiny. These terms are not necessarily anti-democratic. Democratic executives often use them in legitimate emergencies. But they do shift rhetoric away from ordinary procedural accountability and toward existential national framing.

The result also cautions against overinterpreting low BBI. A low score can reflect crisis genre rather than authoritarian inclination. Woodrow Wilson's 1917 inaugural address and James Madison's 1814 annual message are among the lowest-scoring speeches, but their scores must be read in relation to wartime context.

![Figure 3. Procedural constraint language over time.](../outputs/figures/03_procedural_score_over_time.png)

![Figure 4. Charismatic sovereignty language over time.](../outputs/figures/04_charismatic_score_over_time.png)

### Divided Government Is Associated with Higher BBI, Weakly

Speeches during divided government average 0.45 on BBI, compared with -0.29 during unified government. In the preliminary model, divided government is associated with a 0.32-point increase in BBI, though the estimate is weak and should not be overread. The direction is still theoretically interesting. When presidents face an opposition-controlled chamber, they may have stronger incentives to speak through Congress, law, budgets, consultation, programs, and implementation.

This is only a first pass. The current divided-government measure is coded at the Congress level and does not capture intra-term changes, narrow chamber margins, coalition dynamics, or informal legislative bargaining. Still, the direction of the association is consistent with the possibility that institutional friction leaves a rhetorical trace.

### Recession Does Not Lower BBI in This Pilot

The recession indicator is not clearly associated with lower BBI. In the descriptive averages, recession-month speeches score somewhat higher than non-recession speeches among the subset with recession data. In the model, the recession estimate is small and statistically unclear. This does not necessarily contradict the crisis rhetoric hypothesis. Economic crises may produce both charismatic crisis language and procedural policy language. Presidents may describe economic pain while also discussing programs, budgets, agencies, and legislation. The BBI may therefore treat recessions differently from war.

GDP is not included in the main model because coverage begins in 1947 and would drop most of the long historical corpus. It is included in the dataset for future postwar models.

### Extremes Show the Index's Logic and Its Limits

The highest-scoring speech is Richard Nixon's March 8, 1973 "State of the Union Message to the Congress on Community Development," with a BBI of 5.03. It contains 45.89 procedural terms per 1,000 words and 4.35 charismatic terms per 1,000 words. Other high-scoring speeches include Jimmy Carter's late-1970s State of the Union messages and another Nixon community-development message. These are precisely the kinds of documents the index should identify: administratively specific policy messages about programs, agencies, budgets, and implementation.

The lowest-scoring speech is Jimmy Carter's January 20, 1977 inaugural address, with a BBI of -5.54. Donald Trump's January 20, 2017 inaugural address is close behind at -5.32. Other low-scoring speeches include Woodrow Wilson's 1917 inaugural address, Theodore Roosevelt's 1905 inaugural address, and Madison's 1814 annual message. These speeches emphasize unity, renewal, destiny, threat, greatness, or national purpose more than procedural governance.

The Carter result is especially useful as a warning. Carter's 1977 inaugural address is not authoritarian. Its low BBI reflects inaugural genre and moralized democratic language, not democratic erosion. This is why BBI should be interpreted as a measure of rhetorical constraint, not regime type.

![Figure 5. Highest-BBI speeches.](../outputs/figures/06_top_10_highest_bbi.png)

![Figure 6. Lowest-BBI speeches.](../outputs/figures/07_top_10_lowest_bbi.png)

![Figure 7. Procedural versus charismatic language.](../outputs/figures/09_procedural_vs_charismatic.png)

## Discussion

The BBI reveals a simple but important pattern: democratic rhetoric is not only about values, inclusion, or popular sovereignty. It is also about procedure. Some of the most institutionally revealing language in presidential speech is not stirring. It is administrative. It names agencies, programs, reports, budgets, laws, and implementation. This kind of language is easy to ignore because it lacks drama. But that lack of drama may be analytically meaningful.

The analysis also shows why the index must be interpreted relationally. Charismatic language is not inherently anti-democratic. Inaugural addresses often call the nation together through moral and symbolic language. Wartime speeches often rely on sacrifice, threat, and unity. Conversely, procedural language is not inherently democratic. Bureaucratic authoritarian regimes can produce dense administrative speech. The BBI therefore measures a rhetorical form, not a regime classification.

The most promising use of the BBI is comparative and diagnostic. Within a corpus, it can identify speeches that lean unusually far toward procedural constraint or charismatic sovereignty. Across time, it can show how administrative governance changes rhetorical style. Across countries, if validated carefully, it could test whether executive constraint is associated with more institutionalized speech. The measure is especially useful when paired with close reading and external institutional data.

This project also contributes to broader sociological debates about legitimacy. Leaders do not merely hold power. They narrate what kind of power they hold. A president who repeatedly speaks through law, reports, appropriations, agencies, and oversight is narrating power as institutionally mediated. A president who repeatedly speaks through enemies, betrayal, destiny, greatness, and direct unity with the people is narrating power as charismatic and sovereign. The BBI offers one way to make that distinction measurable.

## Limitations

The pilot has several limitations. First, the corpus is U.S.-only. It cannot establish whether the BBI tracks democracy cross-nationally. Second, the dictionary method is transparent but blunt. Words such as "state," "people," "great," and "program" can mean different things in different contexts. Third, the metadata are preliminary. War periods are broad major-war intervals. Recession is monthly and does not capture all political crises. GDP is only available from 1947 onward. Divided government is coded from Congress-level party control and does not capture every shift in legislative power.

Fourth, the BBI is genre-sensitive. This is both a finding and a limitation. Inaugurals and State of the Union documents are not interchangeable. Future work should model genre more carefully and add other speech types, such as major national addresses, campaign speeches, executive orders, and crisis speeches.

Finally, the index requires qualitative validation. The validation exports identify high, middle, low, and random samples for close reading. Those speeches should be hand-coded before the dictionary is treated as stable.

## Conclusion

This paper asked whether presidential speeches can be scored for bureaucratic boredom as a proxy for the rhetorical presence of institutional constraint. The answer is cautiously yes. The BBI does not measure democracy directly, and it should not be used as a regime classifier. But it does identify a meaningful rhetorical contrast between procedural constraint language and charismatic sovereignty language.

In the U.S. pilot corpus, State of the Union documents score much higher than inaugural addresses, major-war periods lower BBI, and divided government is weakly associated with higher BBI. The highest-scoring speeches are administratively dense policy messages. The lowest-scoring speeches are often ceremonial, wartime, or intensely symbolic. These patterns suggest that institutional constraint can leave a linguistic trace, not in the language of democratic ideals alone, but in the ordinary vocabulary of governed power.

Democratic language may be healthiest not when charisma disappears, but when charisma does not permanently replace procedure. Bureaucratic boredom is not democracy. But it may be one of the sounds democracy makes when power has to explain itself through institutions.

## References

American Presidency Project. n.d. *Welcome to the American Presidency Project*. University of California, Santa Barbara. https://www.presidency.ucsb.edu/

Baturo, Alexander, Niheer Dasandi, and Slava J. Mikhaylov. 2017. "Understanding State Preferences with Text as Data: Introducing the UN General Debate Corpus." *Research & Politics* 4(2):1-9. https://doi.org/10.1177/2053168017712821

Bonikowski, Bart, and Noam Gidron. 2016. "The Populist Style in American Politics: Presidential Campaign Rhetoric, 1952-1996." *Social Forces* 94(4):1593-1621. https://doi.org/10.1093/sf/sov120

Bonikowski, Bart, Yuval Luo, and Oscar Stuhler. 2022. "Politics as Usual? Measuring Populism, Nationalism, and Authoritarianism in U.S. Presidential Campaigns, 1952-2020 with Neural Language Models." *Sociological Methods & Research* 51(4). https://doi.org/10.1177/00491241221122317

Brunkert, Lennart, and Christian von Soest. 2023. "Praising the Leader: Personalist Legitimation Strategies and the Deterioration of Executive Constraints." *Democratization* 30(3):419-439. https://doi.org/10.1080/13510347.2022.2150760

Federal Reserve Bank of St. Louis. 2026. *Gross Domestic Product [GDP]*. FRED. https://fred.stlouisfed.org/series/GDP

Federal Reserve Bank of St. Louis. 2026. *NBER Based Recession Indicators for the United States from the Period Following the Peak through the Trough [USREC]*. FRED. https://fred.stlouisfed.org/series/USREC

Grimmer, Justin, and Brandon M. Stewart. 2013. "Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts." *Political Analysis* 21(3):267-297. https://doi.org/10.1093/pan/mps028

Lim, Elvin T. 2002. "Five Trends in Presidential Rhetoric: An Analysis of Rhetoric from George Washington to Bill Clinton." *Presidential Studies Quarterly* 32(2):328-348. https://doi.org/10.1111/j.0360-4918.2002.00223.x

Mochtak, Michal. 2025. "Chasing the Authoritarian Spectre: Detecting Authoritarian Discourse with Large Language Models." *European Journal of Political Research*. https://doi.org/10.1111/1475-6765.12740

Savoy, Jacques. 2017. "Analysis of the Style and the Rhetoric of the American Presidents over Two Centuries." *Glottometrics* 38:55-76.

Varieties of Democracy Institute. 2026. *The V-Dem Dataset, Version 16*. University of Gothenburg. https://www.v-dem.net/data/the-v-dem-dataset/

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5 Codex
Sources: ASR sample article in inbox; American Presidency Project corpus; generated BBI datasets, figures, and model tables; Britannica presidents table; Wikipedia party divisions of United States Congresses; FRED GDP and USREC; references listed above
Agent: Hephaestus
---
