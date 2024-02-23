code_snippet = """

    reaction_times = [ 5.2, 4.8, 6.1, 5.7, 5.4, 5.9, 4.9, 5.3, 6.2, 5.8 ]

    # scipy.stats.kstest(reaction_times, scipy.stats.norm.cdf, N=len(reaction_times)) #wrong call
    scipy.stats.kstest(reaction_times, 'norm', args=(np.mean(reaction_times), np.std(reaction_times, ddof=1))) #correct call

"""