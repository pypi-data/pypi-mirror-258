code_snippet = """
    \033[1m\033[94m[PROPORTION]\033[0m

    \033[92mimport numpy as np
    from scipy.stats import norm\033[0m

    # Sample sizes
    n1, n2 = 1200, 1500

    # Number of successes (purchases)
    x1, x2 = 150, 180

    # Proportions of successes
    p1, p2 = x1 / n1, x2 / n2

    # Pooled proportion
    pooled_p = (x1 + x2) / (n1 + n2)

    # Standard error of the difference in proportion
    std_error = np.sqrt(pooled_p * (1 - pooled_p) * (1/n1 + 1/n2))

    # Z-score
    z_score = (p1 - p2) / std_error

    # P-value (two-tailed test)
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    # \033[93mprint(f"Z-score: {z_score}")
    # print(f"P-value: {p_value}")\033[0m

    \033[1m\033[94m[MEAN 2 IND. SAMPLES]\033[0m

    \033[92mimport numpy as np
    from scipy.stats import norm\033[0m

    # Given sample means and standard deviations
    mean1, std_dev1, n1 = 100, 15, 1200  # Sample 1: mean, standard deviation, and size
    mean2, std_dev2, n2 = 105, 20, 1500  # Sample 2: mean, standard deviation, and size

    # Calculate the standard error of the difference in mean
    std_error_diff = np.sqrt((std_dev1**2 / n1) + (std_dev2**2 / n2))

    # Calculate the Z-score for the difference in means
    z_score = (mean1 - mean2) / std_error_diff

    # Calculate the p-value (two-tailed test)
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    \033[93mprint(f"Z-score: {z_score}")
    print(f"P-value: {p_value}")\033[0m

    \033[1m\033[94m[POP X SAMPLE]\033[0m

    z_score = (sample_mean - population_mean) / (population_std_dev / np.sqrt(sample_size))
    p_value = 2 * (1 - norm.cdf(abs(z_score)))
"""