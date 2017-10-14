import requests
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Risk (0 is Not Risky, 1 is risky) - oneYearRisk
# upMonths, highDate, highReturn, 


r = requests.post('http://www.blackrock.com/tools/hackathon/portfolio-analysis',
  data = {
	'betaPortfolios' :  "SNP500",
	"calculateExpectedReturns" :  "true",
	"calculateExposures" :  "true",
	"calculatePerformance" :  "true",
	"calculateRisk" :  "true",
	"calculateStressTests" :  "true",
	"positions" :  "ISAAT~0.30|ORRYX~0.70",
	"riskFreeRatePortfolio" :  "LTBILL1-3M",
	"scenarios" :  "HIST_20081102_20080911,HIST_20110919_20110720,HIST_20130623_20130520,HIST_20140817_20140101,US10Y_1SD::APB,INF2Y_1SD::APB,USIG_1SD::APB,SPX_1SD::APB,DXY_1SD::APB"
})

response = r.status_code

if response == 200:
	response = r.json()

	json_data = response['resultMap']['PORTFOLIOS'][0]['portfolios'][0]


	analyticsMap = json_data['analyticsMap']

	listOfAnalytics = list()
	for title in analyticsMap.keys():
		listOfAnalytics.append(title)

	analyticValues = list()
	for analytic in listOfAnalytics:
		analytic = analyticsMap[analytic]
		name = analytic['name']
		value = analytic['value']
		harmonicMean = analytic['harmonicMean']

		analyticValues.append([name, value, harmonicMean])


	wantedAnalytic = input("What Analytic?: ")

	for analyticList in analyticValues:
		analytic = process.extractOne(analyticList[0], wantedAnalytic)
		print(analytic)

		print("Found Analytic: " + analyticList[0])
		print("Found Value: " + str(value))
		print("Found Harmonic Mean: " + str(harmonicMean))
		break

	expectedReturns = json_data['expectedReturns']
	exposures = json_data['exposures']
	holdings = json_data['holdings']
	returns = json_data['returns']
	riskData = json_data['riskData']
	weightAsFraction = json_data['weightAsFraction']
