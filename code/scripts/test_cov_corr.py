def test(portfolio):
    # test correlation(i, j) == cov(i, j) / (sd(i) * sd(j))
    for i in range(len(portfolio.assets)):
        for j in range(i + 1, len(portfolio.assets)):
            cov = portfolio.covariance_matrix.iloc[i, j]
            corr = portfolio.correlation_matrix.iloc[i, j]
            sd_i = portfolio.assets[i].sd
            sd_j = portfolio.assets[j].sd
            print("test_cov_corr")
            print(corr)
            print(cov / (sd_i * sd_j))
