risk = requests.post('http://www.blackrock.com/tools/hackathon/security-data?identifiers=' + ticker,
  data = {
	"identifiers": "MSFT"
  }, verify=False)

riskresponse = risk.status_code

if riskresponse == 200:
	riskresponse = risk.json()
	try:
		json_data = riskresponse['resultMap']
	except:
		print(risk.text)
	else:
		analyticsMap = json_data['SECURITY'][0]

		name = analyticsMap["securityName"]

		speechOutput = name

		print(speechOutput)






