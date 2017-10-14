import requests
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests.packages.urllib3
from datetime import date, time, datetime
from dateutil import parser
import sys
requests.packages.urllib3.disable_warnings()

# Risk (0 is Not Risky, 1 is risky) - oneYearRisk
# upMonths, highDate, highReturn, 

try:
	ticker = sys.argv[1]
	typeOfInfo = sys.argv[2]
except:
	ticker = "Microsoft"
	typeOfInfo = "learn"




if typeOfInfo == "learn":

	r = requests.post('http://www.blackrock.com/tools/hackathon/performance?identifiers=' + ticker,
	  data = {
		"identifiers": "MSFT"
	  }, verify=False)

	response = r.status_code


	if response == 200:
		if len(ticker) > 5:
			r = requests.post('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + ticker + '&region=1&lang=en', verify=False)
			tickerName = r.json()['ResultSet']['Result'][0]["name"]
			print (r.text)

		response = r.json()
		try:
			json_data = response['resultMap']
		except:
			print(r.text)
		else:
			analyticsMap = json_data['query'][0]

			if parser.parse(str(analyticsMap['highDate'])) == datetime.today():
				highTime = 1
			else:
				highTime = 0
				#Hardcoding for now
				highTime = 1

			dateString = str(datetime.today().strftime('%Y%m%d'))
			#Hardcoding for now
			dateString = "20171005"
			returnsMap = analyticsMap["returnsMap"]
			stockInfo = returnsMap[dateString]
			upPercentage = analyticsMap['upMonthsPercent']
			totalMonths = analyticsMap['totalMonths']
			returnsType = analyticsMap['returnsType']

			r = requests.post('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + ticker + '&region=1&lang=en', verify=False)
			tickerName = r.json()['ResultSet']['Result'][0]["name"]
			print (r.text)


			speechOutput = "Sure, you wanted information on " + tickerName + ". "

			if highTime == 1:
				speechOutput += "It's currently at it's highest price. "

			speechOutput += "It typically goes up " + str(round((upPercentage * 100), 2)) + "% of the time, based on the " + str(totalMonths) + " months we have the data for. "

			speechOutput += "It usually offers returns " + returnsType.lower() + ". "

			print(speechOutput)










