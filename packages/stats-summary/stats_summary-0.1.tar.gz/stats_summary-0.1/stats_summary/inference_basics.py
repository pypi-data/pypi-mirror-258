inferential_stats_summary = """
Basic Inferential Statistics Summary
------------------------------------

|| Expected Value (Mean) ||
Definition: The expected value (EV) or mean of a random variable is a fundamental
measure that provides an average outcome of a process in the long run.
How to Calculate:
- For a discrete random variable, EV = Σ[xi * P(xi)], where xi is each possible
  value the variable can assume, and P(xi) is the probability of xi.
- For a continuous random variable, EV is calculated as the integral of x * f(x)
  dx over all possible values of x, where f(x) is the probability density
  function of x.

|| Variance ||
Definition: Variance measures the spread of a set of data points or a random
variable around its mean, indicating how much the values differ from the mean.
How to Calculate:
- For a sample: s² = Σ[(xi - x̄)²] / (n - 1), where xi is each sample value,
  x̄ is the sample mean, and n is the sample size.
- For a population: σ² = Σ[(xi - μ)²] / N, where xi is each population value,
  μ is the population mean, and N is the population size.

|| Standard Deviation ||
Definition: The standard deviation is the square root of the variance, providing
a measure of the dispersion of data points in the same units as the data.
How to Calculate:
- For a sample: s = sqrt(s²), where s² is the sample variance.
- For a population: σ = sqrt(σ²), where σ² is the population variance.

|| Confidence Interval ||
Definition: A confidence interval (CI) provides a range of values within which
the true population parameter (mean, proportion) is expected to lie with a
certain level of confidence.
How to Calculate:
- For the mean with known population variance: CI = x̄ ± Z*(σ/√n), where x̄ is
  the sample mean, Z is the Z-score corresponding to the desired confidence
  level, σ is the population standard deviation, and n is the sample size.
- For the mean with unknown population variance (using t-distribution): CI =
  x̄ ± t*(s/√n), where t is the t-score from the t-distribution for the desired
  confidence level and degrees of freedom (n-1), and s is the sample standard
  deviation.

|| p-Value ||
Definition: The p-value measures the probability of observing the collected data,
or something more extreme, assuming the null hypothesis is true.
How to Calculate: Calculated based on the test statistic (Z-score, t-score, etc.)
and the corresponding distribution. The exact calculation depends on the
statistical test being performed.

These concepts form the backbone of inferential statistics, allowing for the
analysis and interpretation of data, and the making of inferences about a
population based on sample data.
"""

tailed_tests_separate_examples = """

To demonstrate both one-tailed and two-tailed z-tests with an emphasis on correct p-value calculation and interpretation, 
let's consider two separate example problems. Z-tests are used when the population variance is known, and the sample size
is large enough (usually \(n > 30\)) for the Central Limit Theorem to apply, making the sampling distribution of the sample 
mean approximately normal.

### Example 1: One-Tailed Z-Test

**Scenario:** A company claims that its weight loss pill helps individuals lose more than 5 kg on average in a month. 
You conduct a study with 35 individuals and find that the average weight loss is 5.8 kg with a population standard deviation
of 1.2 kg. Test this claim at the \(\alpha = 0.05\) significance level.

#### Hypotheses:

- \(H_0: \mu = 5\) kg (The average weight loss is 5 kg)
- \(H_a: \mu > 5\) kg (The average weight loss is more than 5 kg)

#### Steps:

1. **Calculate the z-score** using the formula:
   \[
   z = \frac{\bar{x} - \mu}{\sigma / \sqrt{n}}
   \]
   where \(\bar{x}\) is the sample mean, \(\mu\) is the population mean under the null hypothesis, 
   \(\sigma\) is the population standard deviation, and \(n\) is the sample size.

2. **Determine the p-value** for the calculated z-score from the standard normal distribution.

3. **Interpret the p-value** relative to the significance level \(\alpha\).

Let's perform the calculations for this one-tailed test.

For the one-tailed z-test:

- The calculated z-score is approximately \(3.944\).
- The corresponding p-value is approximately \(0.00004\).

#### Interpretation (One-Tailed):

Since the p-value (\(0.00004\)) is less than the significance level (\(\alpha = 0.05\)), we reject the null hypothesis. 
This indicates that there is sufficient evidence to support the claim that the weight loss pill helps individuals lose 
more than 5 kg on average in a month.

### Example 2: Two-Tailed Z-Test

**Scenario:** A manufacturer claims that the average lifespan of its light bulbs is 1200 hours. You suspect this claim is 
inaccurate, so you test a sample of 50 light bulbs and find an average lifespan of 1180 hours with a population standard 
deviation of 100 hours. Test the accuracy of the manufacturer's claim at the \(\alpha = 0.05\) significance level.

#### Hypotheses:

- \(H_0: \mu = 1200\) hours (The average lifespan is 1200 hours)
- \(H_a: \mu \neq 1200\) hours (The average lifespan is not 1200 hours)

#### Steps:

1. **Calculate the z-score** using the same formula as the one-tailed test.
2. **Determine the p-value** for the calculated z-score, but multiply by 2 for a two-tailed test since we are interested in 
deviations on both sides of the mean.
3. **Interpret the p-value** relative to the significance level \(\alpha\).

Let's perform the calculations for this two-tailed test.

For the two-tailed z-test:

- The calculated z-score is approximately \(-1.414\).
- The corresponding p-value is approximately \(0.1573\).

#### Interpretation (Two-Tailed):

Since the p-value (\(0.1573\)) is greater than the significance level (\(\alpha = 0.05\)), we fail to reject the null hypothesis. 
This suggests that there is insufficient evidence to claim that the average lifespan of the light bulbs is significantly different 
from 1200 hours.

### Summary:

- **One-Tailed Test:** Used when the direction of the hypothesis is known (e.g., testing for a value greater than a benchmark), 
leading to a p-value that directly reflects this direction. Our example showed significant evidence to support the claim of weight 
loss greater than 5 kg.
  
- **Two-Tailed Test:** Used when testing for any difference from the hypothesized value, regardless of direction, requiring the 
p-value to be doubled to account for both tails of the distribution. Our example did not show significant evidence to dispute the 
manufacturer's claim about the light bulb lifespan.

"""

tailed_tests_differences = """

The main difference between one-tailed and two-tailed tests lies in the directionality of the hypotheses they test and, 
consequently, how the significance of the test results is assessed. This distinction influences both the conceptual framework 
and practical application of hypothesis testing.

### Conceptual Differences

- **One-Tailed Test:** This test is used when the research hypothesis specifies a direction of the expected effect. 
It tests for the possibility of the relationship in one specific direction and is used when we want to determine if there is 
either a significant increase or decrease in the dependent variable. For example, testing whether a new drug is more effective 
than the existing treatment suggests a one-tailed test because you are only interested in one direction of effectiveness.

- **Two-Tailed Test:** This test does not specify a direction; instead, it tests for the possibility of the relationship in 
both directions. It is used when we want to determine if there is any difference (regardless of direction) between two groups. 
For example, testing whether a new drug has a different effect (either more effective or less effective) than the existing treatment 
requires a two-tailed test because you are interested in any difference, not just an improvement.

### Practical Differences

- **P-Value Calculation:**
  - In a **one-tailed test**, the p-value represents the probability of obtaining a test statistic as extreme as, or more extreme 
  than, the one observed, in the direction specified by the alternative hypothesis. This means the p-value is calculated based on 
  one tail of the distribution.
  - In a **two-tailed test**, the p-value is calculated by considering both tails of the distribution. This is because the alternative 
  hypothesis allows for the effect in either direction, so the test statistic's extremeness is assessed against both ends of the 
  distribution. The p-value in a two-tailed test is essentially double that of what it would be in a one-tailed test for the same 
  absolute value of the test statistic.

- **Interpretation of Results:**
  - **One-Tailed Test:** If the test statistic falls in the critical region in the direction specified by the alternative hypothesis, 
  you reject the null hypothesis in favor of the alternative hypothesis that specifies a direction (e.g., greater than or less than).
  - **Two-Tailed Test:** If the test statistic falls in either critical region at both tails of the distribution, you reject the null 
  hypothesis in favor of the alternative hypothesis that does not specify a direction but suggests a difference.

- **Error Rates and Power:**
  - **One-Tailed Test:** This test has more statistical power than a two-tailed test for the same effect size because the entire 
  significance level (\(\alpha\)) is allocated to testing the effect in one direction, which makes it easier to find a significant 
  result if the effect is in the specified direction.
  - **Two-Tailed Test:** The significance level is split between two tails of the distribution, which makes this test more conservative. 
  It is less likely to find a significant result by chance in either direction, but it requires a larger effect size or sample size to 
  achieve the same power as a one-tailed test for detecting an effect.

### Summary

The choice between using a one-tailed or two-tailed test hinges on the research question and hypothesis. 
A one-tailed test is more appropriate when the hypothesis predicts a direction of the effect, while a two-tailed test is 
used when the hypothesis only predicts that there will be an effect, without specifying its direction. 
This choice impacts how the data are analyzed and how conclusions are drawn from the statistical testing.

"""

tailed_tests_single_example = """

Let's consider a simple example involving the effect of a new study strategy on exam scores to illustrate the application of 
both a one-tailed test (checking for an increase) and then a two-tailed test (checking for any change).

### Background

A teacher wants to evaluate whether a new study strategy improves student performance on exams. To do this, the teacher collects 
exam scores from 40 students before and after implementing the new study strategy. The teacher knows the population standard deviation of exam scores is 10 points. After implementing the strategy, the average exam score increased from 75 to 78 points.

The teacher first wants to test if the new strategy significantly increased scores (one-tailed test). Then, out of curiosity, 
the teacher decides to check if there was any significant change in scores, regardless of direction (two-tailed test).

### Data Summary

- Sample size (\(n\)): 40 students
- Population standard deviation (\(\sigma\)): 10 points
- Mean score before the strategy (\(\mu_0\)): 75 points
- Mean score after the strategy (\(\bar{x}\)): 78 points

### One-Tailed Test

#### Hypotheses

- \(H_0: \mu \leq 75\) (The strategy does not increase exam scores)
- \(H_a: \mu > 75\) (The strategy increases exam scores)

#### Significance Level

- \(\alpha = 0.05\)

#### Z-Score Calculation

The z-score is calculated using the formula:
\[
z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}
\]

#### P-Value Calculation

The p-value for the one-tailed test is found by looking up the z-score in the standard normal distribution.

### Two-Tailed Test

#### Hypotheses

- \(H_0: \mu = 75\) (The strategy does not change exam scores)
- \(H_a: \mu \neq 75\) (The strategy changes exam scores, either increase or decrease)

#### Z-Score Calculation

The z-score calculation remains the same as in the one-tailed test.

#### P-Value Calculation

The p-value for the two-tailed test is twice the p-value of the one-tailed test if the z-score indicates an increase, or it 
is calculated directly from both tails of the distribution for the absolute z-score value.

Let's perform these calculations.

### Calculations and Interpretations

- The calculated z-score is approximately \(1.897\).

#### One-Tailed Test

- The p-value for the one-tailed test is approximately \(0.0289\).

#### Interpretation (One-Tailed):
Since the p-value (\(0.0289\)) is less than the significance level (\(\alpha = 0.05\)), we reject the null hypothesis for the 
one-tailed test. This indicates that there is significant evidence to support the claim that the new study strategy increases 
exam scores.

#### Two-Tailed Test

- The p-value for the two-tailed test is approximately \(0.0578\).

#### Interpretation (Two-Tailed):
For the two-tailed test, the interpretation depends on the significance level. If we stick to \(\alpha = 0.05\), 
the p-value (\(0.0578\)) is slightly above the significance level, suggesting that we fail to reject the null hypothesis. 
This indicates that there is not enough evidence to support a significant change (either increase or decrease) in exam scores 
due to the new study strategy at the \(0.05\) significance level.

### Summary

- **One-Tailed Test:** There is significant evidence at the \(\alpha = 0.05\) level to conclude that the new study strategy 
increases student exam scores.
  
- **Two-Tailed Test:** At the same significance level, there is not enough evidence to conclude that the new study strategy 
significantly changes (either increases or decreases) student exam scores.

This example illustrates how the choice of a one-tailed or two-tailed test can affect the conclusions drawn from the same set 
of data, emphasizing the importance of aligning the hypothesis test with the research question.

"""