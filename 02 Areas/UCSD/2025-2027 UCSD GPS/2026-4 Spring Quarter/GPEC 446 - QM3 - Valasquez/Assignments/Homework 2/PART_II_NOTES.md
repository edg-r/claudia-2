# Homework 2 Part II Notes

## Source and Design

Paper: Angrist, J. D., & Lavy, V. (1999). Using Maimonides' Rule to Estimate the Effect of Class Size on Scholastic Achievement. Quarterly Journal of Economics, 114(2), 533-575. https://doi.org/10.1162/003355399556061

## Question 2

The histogram is saved as `hist_school_enrollment.png`. There is no visually obvious bunching immediately below 40 in this data, so the histogram does not strongly suggest that parents choose schools strategically around Maimonides' Rule.

## Question 3

RDD plots are saved as `rdd_classize_cutoff40.png`, `rdd_avgmath_cutoff40.png`, and `rdd_avgverb_cutoff40.png`. The class-size plot should show the first-stage drop at 40. The math and verbal plots show whether achievement jumps at the same cutoff.

## Question 4 Manual Local Regression

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

I used covariate smoothness in `disadvantaged` as the falsification test. Because disadvantage is predetermined relative to the class-size rule, it should not jump discontinuously at 40 if observations just below and just above the cutoff are comparable.

        outcome cutoff bandwidth estimate std_error   p_value n_left n_right
4 disadvantaged     40        10 4.818804  4.368414 0.2707917     96     236
  unique_schools_left unique_schools_right
4                  86                  131

---
Generated for: Edgar Agunias
Date: 2026-05-24
Model: GPT-5 Codex
Sources: grade5.dta; Homework 2 Panel & RDD prompt; Angrist and Lavy (1999)
Agent: Tyche
---
