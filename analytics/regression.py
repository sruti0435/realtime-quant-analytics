import statsmodels.api as sm

def hedge_ratio(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model.params[1]
