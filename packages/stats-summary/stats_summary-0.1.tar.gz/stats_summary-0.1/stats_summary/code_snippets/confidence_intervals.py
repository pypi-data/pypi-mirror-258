code_snippet = """
\033[1m\033[94m[CONFIDENCE INTERVAL FOR A SINGLE SAMPLE MEAN]\033[0m

\033[92mimport numpy as np
from scipy.stats import t\033[0m

# Sample data
sample = np.array([120, 115, 130, 140, 135, 150, 125, 138, 145, 155])

# Sample mean and standard deviation
sample_mean = np.mean(sample)
sample_std = np.std(sample, ddof=1)

# Sample size and degrees of freedom
n = len(sample)
df = n - 1

# Confidence level (95%)
alpha = 0.05

# T-critical value for 95% confidence
t_critical = t.ppf(1 - alpha/2, df)

# Margin of error
margin_error = t_critical * (sample_std / np.sqrt(n))

# Confidence interval
ci_lower = sample_mean - margin_error
ci_upper = sample_mean + margin_error

\033[93mprint(f"95% Confidence Interval: ({ci_lower}, {ci_upper})")\033[0m

\033[1m\033[94m[CONFIDENCE INTERVAL FOR THE DIFFERENCE BETWEEN TWO INDEPENDENT SAMPLE MEANS]\033[0m

\033[92mimport numpy as np
from scipy.stats import t\033[0m

# Sample data
mean1, std_dev1, n1 = 100, 10, 30  # Sample 1: mean, standard deviation, and size
mean2, std_dev2, n2 = 110, 15, 30  # Sample 2: mean, standard deviation, and size

# Calculate the standard error of the difference in means
std_error_diff = np.sqrt((std_dev1**2 / n1) + (std_dev2**2 / n2))

# Degrees of freedom
df = min(n1 - 1, n2 - 1)

# Confidence level (95%)
alpha = 0.05

# T-critical value for 95% confidence
t_critical = t.ppf(1 - alpha/2, df)

# Margin of error
margin_error = t_critical * std_error_diff

# Confidence interval
ci_lower = (mean1 - mean2) - margin_error
ci_upper = (mean1 - mean2) + margin_error

\033[93mprint(f"95% Confidence Interval for Difference Between Means: ({ci_lower}, {ci_upper})")\033[0m

\033[1m\033[94m|||||||||||||||| CONFIDENCE INTERVAL FOR MEAN OF PAIRED SAMPLES ||||||||||||||||||\033[0m

\033[92mimport numpy as np
from scipy.stats import t\033[0m

# Data for paired samples
before = np.array([200, 220, 210, 240, 230])
after = np.array([210, 230, 205, 245, 235])

# Calculate the differences
diffs = after - before

# Calculate the mean and standard deviation of the differences
mean_diff = np.mean(diffs)
std_diff = np.std(diffs, ddof=1)

# Sample size and degrees of freedom
n = len(diffs)
df = n - 1

# Confidence level (95%)
alpha = 0.05

# T-critical value for 95% confidence
t_critical = t.ppf(1 - alpha/2, df)

# Margin of error
margin_error = t_critical * (std_diff / np.sqrt(n))

# Confidence interval
ci_lower = mean_diff - margin_error
ci_upper = mean_diff + margin_error

\033[93mprint(f"95% Confidence Interval for Mean Difference: ({ci_lower}, {ci_upper})")\033[0m
"""
