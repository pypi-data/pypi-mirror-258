code_snippet = """
    \033[1m\033[94m|||||||||||||||||||||||||||| MEAN 2 IND. SAMPLES |||||||||||||||||||||||||||||||||||||\033[0m

    \033[92mimport numpy as np
    from scipy.stats import t\033[0m

    # Given sample means, standard deviations, and sizes
    mean1, std_dev1, n1 = 100, 15, 30  # Sample 1: mean, standard deviation, and size
    mean2, std_dev2, n2 = 105, 20, 30  # Sample 2: mean, standard deviation, and size

    # Calculate the standard error of the difference in means
    std_error_diff = np.sqrt((std_dev1**2 / n1) + (std_dev2**2 / n2))

    # Calculate the degrees of freedom
    df = min(n1 - 1, n2 - 1)

    # Calculate the t-score for the difference in means
    t_score = (mean1 - mean2) / std_error_diff

    # Calculate the p-value (two-tailed test)
    p_value = 2 * (1 - t.cdf(abs(t_score), df))

    \033[93mprint(f"T-score: {t_score}")
    print(f"P-value: {p_value}")\033[0m

    \033[1m\033[94m|||||||||||||||||||||||||||| MEAN PAIRED SAMPLES |||||||||||||||||||||||||||||||||||||\033[0m

    \033[92mimport numpy as np
    from scipy.stats import t\033[0m

    # Data for paired samples
    before = np.array([100, 105, 98, 87, 110])
    after = np.array([108, 110, 99, 89, 115])

    # Calculate the differences
    diffs = after - before

    # Calculate the mean of the differences
    mean_diff = np.mean(diffs)

    # Calculate the standard deviation of the differences
    std_diff = np.std(diffs, ddof=1)

    # Sample size
    n = len(diffs)

    # Degrees of freedom
    df = n - 1

    # Calculate the t-score
    t_score = mean_diff / (std_diff / np.sqrt(n))

    # Calculate the p-value (two-tailed test)
    p_value = 2 * (1 - t.cdf(abs(t_score), df))

    \033[93mprint(f"T-score: {t_score}")
    print(f"P-value: {p_value}")\033[0m

    \033[1m\033[94m||||||||||||||||||||||||||||| SINGLE SAMPLE VS POPULATION MEAN |||||||||||||||||||||||\033[0m

    \033[92mimport numpy as np
    from scipy.stats import t\033[0m

    # Sample data
    sample = np.array([100, 102, 104, 98, 96, 101, 99, 103, 97, 105])

    # Population mean
    pop_mean = 100

    # Sample mean and standard deviation
    sample_mean = np.mean(sample)
    sample_std = np.std(sample, ddof=1)

    # Sample size and degrees of freedom
    n = len(sample)
    df = n - 1

    # Calculate the t-score
    t_score = (sample_mean - pop_mean) / (sample_std / np.sqrt(n))

    # Calculate the p-value (two-tailed test)
    p_value = 2 * (1 - t.cdf(abs(t_score), df))

    \033[93mprint(f"T-score: {t_score}")
    print(f"P-value: {p_value}")\033[0m
"""
