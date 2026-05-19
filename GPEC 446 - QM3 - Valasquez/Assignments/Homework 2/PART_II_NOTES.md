# Homework 2 Part II Notes

## Source and Design

Paper: Angrist, J. D., & Lavy, V. (1999). Using Maimonides' Rule to Estimate the Effect of Class Size on Scholastic Achievement. Quarterly Journal of Economics, 114(2), 533-575. https://doi.org/10.1162/003355399556061

The local `rdd_paper.pdf` is a scan-only PDF, so direct text extraction returned blank pages. For the intro answer, use the paper metadata and abstract from the QJE/NBER pages together with the assignment-provided PDF. The intro frames the problem as a class-size causal inference problem: parents, teachers, and scholars care about class size, but ordinary observational comparisons can mix class-size effects with nonrandom school and family characteristics.

Draft answer for Question 1: A simple OLS regression of test scores on class size is likely endogenous because class size is not randomly assigned. Schools with smaller classes may also differ in parental resources, neighborhood income, school quality, teacher quality, peer composition, religious status, and the share of disadvantaged students. If advantaged families sort into schools with smaller classes, OLS would make small classes look more beneficial than they truly are, so the class-size coefficient would be too negative. A competing bias is compensatory placement: schools may assign smaller classes to weaker or more disadvantaged students, which would make small classes look less beneficial. The most intuitive omitted-variable concern in this setting is family/school advantage, so I would expect naive OLS to overstate the benefit of small classes unless the data show strong compensatory assignment.

## Question 2

The histogram is saved as `outputs/part_ii/hist_school_enrollment.png`. There is no visually obvious bunching immediately below 40 in this data, so the histogram does not strongly suggest that parents choose schools strategically around Maimonides' Rule. If parents were manipulating enrollment to obtain smaller classes, we would expect suspicious piling up just above or below rule thresholds.

## Question 3

RDD plots are saved as `outputs/part_ii/rdd_classize_cutoff40.png`, `outputs/part_ii/rdd_avgmath_cutoff40.png`, and `outputs/part_ii/rdd_avgverb_cutoff40.png`. The class-size plot should show the first-stage drop at 40. The math and verbal plots show whether achievement jumps at the same cutoff; if scores rise where class size falls, that supports the smaller-class interpretation, but the evidence should be described as local to schools near 40 students.

## Question 4 Manual Local Regression

Manual estimates use schools/classes with enrollment below 80 and a bandwidth of 10 students around the 40-student cutoff. This bandwidth keeps the comparison local while retaining observations on both sides of the cutoff.

        outcome cutoff bandwidth  estimate std_error      p_value n_left
1       avgmath     40        10  4.261135  2.570426 9.832313e-02     96
2       avgverb     40        10  4.319230  2.294697 6.068496e-02     96
3      classize     40        10 -7.107493  1.445179 1.384699e-06     96
4 disadvantaged     40        10  4.818804  4.368414 2.707917e-01     96
  n_right unique_schools_left unique_schools_right
1     236                  86                  131
2     236                  86                  131
3     236                  86                  131
4     236                  86                  131

## Question 4 rdrobust

  outcome cutoff estimate_conventional se_conventional ci95_low_conventional
1 avgmath     40              2.938782        3.752691             -4.416358
2 avgverb     40              3.623401        3.706055             -3.640333
  ci95_high_conventional bandwidth_left bandwidth_right n_left n_right
1               10.29392       7.901030        7.901030     70     172
2               10.88713       8.186282        8.186282     79     198

## Question 5 Falsification Test

I used covariate smoothness in `disadvantaged` as the falsification test. Because disadvantage is predetermined relative to the class-size rule, it should not jump discontinuously at 40 if observations just below and just above the cutoff are comparable. A meaningful discontinuity would imply that the RD estimate may be mixing class-size effects with a change in student composition.

        outcome cutoff bandwidth estimate std_error   p_value n_left n_right
4 disadvantaged     40        10 4.818804  4.368414 0.2707917     96     236
  unique_schools_left unique_schools_right
4                  86                  131

---
Generated for: Edgar Agunias
Date: 2026-05-18
Model: GPT-5 Codex
Sources: `grade5.dta`, `Homework 2_ Panel & RDD.pdf`, local scan-only `rdd_paper.pdf`, QJE/NBER metadata for Angrist and Lavy (1999)
Agent: Hephaestus assisting Tyche
---
