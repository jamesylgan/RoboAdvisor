#!/usr/bin/python3

import requests
import json
import pprint
import sys

def main():
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
        print(res['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['analyticsMap']['returnOnEquity'])
        sys.stdout.flush()

if __name__ == '__main__':
    main()
