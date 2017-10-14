import json
import requests
requests.packages.urllib3.disable_warnings()

stocks = ["GWPH", "POOL", "CRED", "WDFC", "ICLR", "ADP", "MPWR", "INCY", "PNQI", "CASY", "ISRL", "MAR", "NXPI", "ATHN", "LOGM", "EMB", "SINA", "FFIV", "VONE", "VTHR", "CGNX", "EA", "CHKP", "ADSK", "ERIE", "VTWO", "ANAT", "UTHR", "LANC", "TQQQ", "TECH", "VRTS", "NDSN", "TSRO", "ALNY", "SBNY", "IEI", "PBYI", "MIDD", "IAC", "TLT", "ROLL", "PRFZ", "FISV", "HTHT", "ANSS", "VONG", "VTWG", "JJSF", "BLUE", "OLED", "MSTR", "BBH", "WINA", "CELG", "CME", "ALGT", "ALXN", "JAZZ", "WYNN", "LGND", "INTU", "SAFM", "QQQ", "MLAB", "EXPE", "ESLT", "SBAC", "CBRL", "CTAS", "CVCO", "JKI", "VRTX", "ADBE", "SHPG", "AAPL", "WLTW", "IDXX", "COST", "SOXX", "IJT", "FB", "ABMD", "ASML", "AMGN", "SIVB", "ICUI", "LRCX", "MKTX", "ITIC", "HIFS", "ALGN", "NVDA", "ULTI", "IPGP", "ULTA", "NFLX", "LFUS", "WINS", "ILMN", "CHDN", "ORLY", "DHIL", "MSG", "STMP", "COKE", "DJCO", "ESGR", "TREE", "MELI", "AVGO", "COHR", "ONEQ", "BIDU", "NTES", "CACC", "CSGP", "IBB", "BIIB", "TSLA", "CHTR", "ISRG", "NWLI", "UHAL", "FCNCA", "IRDMB", "REGN", "EQIX", "ATRI", "GOOG", "AMZN", "GOOGL", "PCLN"]

text_file = open("Output.txt", "w")
stockList = dict()
text_file.write("{")

for stock in stocks:
	r = requests.post('http://www.blackrock.com/tools/hackathon/performance?identifiers=' + stock, verify=False)

	response = r.json()
	json_data = response['resultMap']['RETURNS'][0]
	returnsMap = json_data['returnsMap']
	dateString = '20171001'
	stockInfo = list(returnsMap)[-1]
	stockInfo = returnsMap[stockInfo]
	#print(stockInfo)
	sinceStartDate = stockInfo['sinceStartDate']

	sinceStartDateRisk = stockInfo['sinceStartDateRisk']

	calulation = sinceStartDateRisk / sinceStartDate

	string = stock + ": " + str(calulation) + ", "
	text_file.write(string)


text_file.write("}")



text_file.close()

