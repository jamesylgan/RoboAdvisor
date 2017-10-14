#!/usr/bin/python3

import requests
import json
import pprint

r = requests.post('https://www.blackrock.com/tools/hackathon/portfolio-analysis',
    data = {
        'betaPortfolios' :  "SNP500",
        'calculateExposures' :  "true",
        'calculatePerformance' :  "true",
        'positions' :  "AAPL~25|ITOT~25|AGG~25|EFAV~25|",
        'riskFreeRatePortfolio' :  "LTBILL1-3M"
    })

status = r.status_code

if status == 200:
    res = r.json()
    # print(res[0]['resultMap']['PORTFOLIOS']['portfolios']['analyticsMap']['returnOnAssets'])
    print(res['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['analyticsMap']['returnOnEquity'])
    