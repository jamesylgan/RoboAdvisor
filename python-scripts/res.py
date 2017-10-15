import requests
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests.packages.urllib3
from datetime import date, time, datetime
from dateutil import parser
import sys
import operator
import wikipedia
import random

requests.packages.urllib3.disable_warnings()

# Risk (0 is Not Risky, 1 is risky) - oneYearRisk
# upMonths, highDate, highReturn, 

try:
	ticker = sys.argv[2]
	typeOfInfo = sys.argv[1]
except:
	typeOfInfo = ""
	ticker = ""

if typeOfInfo == "learn":

	if len(ticker) > 5:
		r = requests.post('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + ticker + '&region=1&lang=en', verify=False)
		try:
			tickerSym = r.json()['ResultSet']['Result'][0]["symbol"]
			tickerName = r.json()['ResultSet']['Result'][0]["name"]
		except:
			print("Sorry, I couldn't find the company you were looking for, try asking for a different one.")
	else:
		r = requests.post('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + ticker + '&region=1&lang=en', verify=False)
		tickerSym = ticker
		try:
			tickerName = r.json()['ResultSet']['Result'][0]["name"]
		except:
			print("Sorry, I couldn't find the ticker you were looking for, try asking for a different one.")

	r = requests.post('http://www.blackrock.com/tools/hackathon/performance?identifiers=' + ticker, verify=False)

	response = r.status_code


	if response == 200:
			

		response = r.json()
		try:
			json_data = response['resultMap']['RETURNS'][0]
		except:
			print("Sorry, something went wrong.")
		else:

			if parser.parse(str(json_data['highDate'])) == datetime.today():
				highTime = 1
			else:
				highTime = 0
				#Hardcoding for now
				highTime = 1

			dateString = str(datetime.today().strftime('%Y%m%d'))
			#Hardcoding for now
			dateString = "20171005"
			returnsMap = json_data["returnsMap"]
			stockInfo = returnsMap[dateString]
			upPercentage = json_data['upMonthsPercent']
			totalMonths = json_data['totalMonths']
			returnsType = json_data['returnsType']

			speechOutput = "Sure, you wanted information on " + tickerName + ". "

			if highTime == 1:
				speechOutput += "It's currently at it's highest price. "

			speechOutput += "It typically goes up " + str(round((upPercentage * 100), 2)) + "% of the time, based on the " + str(totalMonths) + " months we have the data for. "

			speechOutput += "It usually offers returns " + returnsType.lower() + ". "

			print(speechOutput)




if typeOfInfo == "suggest":
	try:
		userRisk = float(sys.argv[2]) / 100
	except TypeError:
		print("Sorry, something went wrong")
	else:
		stocks = {"FAS": 0.2575014180477766, "NUGT": -0.3284053538569262, "JNUG": -0.446238207851139, "SPXL": 0.012620865889218577, "TZA": -0.1513687523533683, "TNA": 0.03149774417126344, "ERX": -0.5713949061922216, "LABU": -0.5942805569218961, "SOXL": 0.015344449453916354, "TECL": 0.00459357643653409, "SPXS": -0.11044403154731945, "DUST": -0.3264048381533426, "TMV": -0.11683258913563795, "EDC": 0.47550538439362, "YINN": -0.7701972794092574, "KNOW": 0.024827884842545965, "CURE": 0.011583803585153924, "FAZ": -0.1627178209109875, "RUSL": -0.25557448284110545, "QQQE": 0.030410179688276046, "JDST": -0.37430079195644433, "GUSH": -0.35497411378568827, "LABD": -0.40011212305983074, "BRZU": -0.3256745578141255, "INDL": -0.35038791340958336, "CWEB": 0.10318508474483176, "TMF": 0.15581258611153617, "EDZ": -0.16872379322972803, "CHAU": -0.36511687455374475, "ZMLP": -0.1501350085229348, "DRN": 0.011684495181002298, "CHAD": -0.4881587824920303, "LLSP": 0.0978863970887298, "EURL": -1.4485928719040453, "MIDU": 0.009341208339719288, "ERY": -0.16538274474671322, "GASL": -0.2528550210204951, "SOXS": -0.1511688079283782, "DFEN": 0.10992326086058926, "YANG": -0.17737330977432128, "DRIP": -0.4397341216745512, "SPDN": -0.08812981541575476, "DPST": 0.2736567960823178, "RETL": 0.01140502933793034, "DZK": 0.1547439381872885, "TYO": -0.06903623052893068, "RUSS": -0.2560728594619288, "TECS": -0.12263334815212483, "NAIL": 0.3917275154664243, "LBJ": -0.23380016311548873, "DRV": -0.1335896239149698, "IBLN": 0.13573582365547027, "COM": -0.24235669725106312, "KORU": 0.9334330671969054, "EUFL": 0.05133288037433155, "JPNL": 0.18234435970605697, "TYD": 0.06140316706316329, "LLSC": 0.13648861386050443, "GASX": -0.3394700975508985, "MIDZ": -0.12668050377584075, "TYBS": -0.07512355360581704, "SHNY": -0.2697385166506409, "EUXL": 0.37364939669089803, "SPUU": 0.07233170581839027, "DPK": -0.14232275640802405, "HYDD": -0.06778939654166674, "WDRW": -0.2047033178245166, "SMLL": 0.12893069918502315, "TPOR": 0.48702302909726036, "DUSL": 0.23651454756510054, "SAGG": -0.03858701403961297, "UTSL": 0.8359137469735004, "GWPH": 0.003650099551545385, "POOL": 0.004140460590899768, "CRED": 0.02236014635064959, "WDFC": 0.004949316953484515, "ICLR": 0.0026387946377423076, "ADP": 0.0033206348253841437, "MPWR": 0.0024949977051286396, "INCY": 0.0026617071361969237, "PNQI": 0.01726512840531326, "CASY": 0.002976913998069725, "ISRL": 0.0033471756651081088, "MAR": 0.003674675466200682, "NXPI": 0.003680276454960356, "ATHN": 0.012612255439290582, "LOGM": 0.005543648802380053, "EMB": 0.030735250461383118, "SINA": 0.024357459415326407, "FFIV": 0.004574298963149222, "VONE": 0.020767408525152492, "VTHR": 0.021314620989997562, "CGNX": 0.003316185718708699, "EA": 0.01852504262420475, "CHKP": 0.004257858701392607, "ADSK": 0.0036537846278192954, "ERIE": 0.004887219914091815, "VTWO": 0.030815552515182185, "ANAT": 0.019721623600847563, "UTHR": 0.0025225932198746364, "LANC": 0.0038487497773095807, "TQQQ": 0.005985932734933243, "TECH": 0.005879486771682402, "VRTS": 0.002602605576469359, "NDSN": 0.0033308445863868123, "TSRO": 0.005960222903570885, "ALNY": 0.003037012671854298, "SBNY": 0.004298155747213095, "IEI": 0.020728012755011096, "PBYI": 0.013155031524108981, "MIDD": 0.001384447746438741, "IAC": 0.0053135830294540245, "TLT": 0.02229745634916743, "ROLL": 0.003076652195966813, "PRFZ": 0.033877245468511376, "FISV": 0.002323794768856645, "HTHT": 0.006317276699952284, "ANSS": 0.0016739908456407627, "VONG": 0.018794603736853797, "VTWG": 0.029977730027870738, "JJSF": 0.002912136327946103, "BLUE": 0.013873940501086805, "OLED": 0.00394168182101762, "MSTR": 0.01718103015163755, "BBH": 0.02158086337728944, "WINA": 0.003777420237357617, "CELG": 0.0009919667348696854, "CME": 0.002432127474774824, "ALGT": 0.005855495540336601, "ALXN": 0.0010158283878509147, "JAZZ": 0.007384781981878746, "WYNN": 0.004981278180895024, "LGND": 0.06872754073699551, "INTU": 0.0029078726825635544, "SAFM": 0.005048082288675095, "QQQ": 0.032529041952041024, "MLAB": 0.0012841723169108037, "EXPE": 0.003936636669243581, "ESLT": 0.002027750063419315, "SBAC": 0.0014916731557046065, "CBRL": 0.004482849962061862, "CTAS": 0.004917681055483665, "CVCO": 0.00357377045054887, "JKI": 0.019566835559866807, "VRTX": 0.002176164330472054, "ADBE": 0.0029161865962789185, "SHPG": 0.004095627204973078, "AAPL": 0.00022822196563484522, "WLTW": 0.013492045944967045, "IDXX": 0.00165735938797728, "COST": 0.002710652092755524, "SOXX": 0.04907936264854685, "IJT": 0.015503639435680555, "FB": 0.006817567341956059, "ABMD": 0.0015229714385273368, "ASML": 0.0017851900517696548, "AMGN": 0.006107867021709705, "SIVB": 0.005095629867124458, "ICUI": 0.00370591316417211, "LRCX": 0.0035123346465623655, "MKTX": 0.0027153606649028008, "ITIC": 0.004317409426427848, "HIFS": 0.003426260871334981, "ALGN": 0.003735980864857325, "NVDA": 0.0013518112865196887, "ULTI": 0.0016880009538917126, "IPGP": 0.004180335801910465, "ULTA": 0.00470908790714449, "NFLX": 0.0009026788600262959, "LFUS": 0.00478047030428968, "WINS": 0.008502353461390017, "ILMN": 0.0005348032340149603, "CHDN": 0.004041866101708474, "ORLY": 0.0017562157502836004, "DHIL": 0.0005104779034009816, "MSG": 0.0033021159440818014, "STMP": 0.0016305554689835693, "COKE": 0.004148292696137934, "DJCO": 0.005213365059151153, "ESGR": 0.02510483865291651, "TREE": 0.0010859617714693303, "MELI": 0.004593233294294244, "AVGO": 0.0013124437205190697, "COHR": 0.0024969773821618847, "ONEQ": 0.015793239712912015, "BIDU": 0.00211110507146443, "NTES": 0.0009478996612241509, "CACC": 0.001999308203515781, "CSGP": 0.0032583455189123126, "IBB": 0.027543386855983277, "BIIB": 0.004171583855643967, "TSLA": 0.0023215390109828315, "CHTR": 0.0018031479045374122, "ISRG": 0.0004297443002592299, "NWLI": 0.01614572047535163, "UHAL": 0.0015902950529979637, "FCNCA": 0.007973672318505194}

		sorted_stocks = sorted(stocks.items(), key=operator.itemgetter(1))

		d = {k: v for k, v in stocks.items() if (userRisk - 0.01) <= v <= (userRisk + 0.01)}
		sorted_returned_stocks = sorted(d.items(), key=operator.itemgetter(1))
		fullString = "Based on your risk assessment, here are some stocks that you might like: "

		if len(sorted_returned_stocks) > 5:
			for stock in sorted_returned_stocks[:4]:
				fullString += random.choice(sorted_returned_stocks)[0] + ", "
		else:
			for stock in sorted_returned_stocks:
				fullString += random.choice(sorted_returned_stocks)[0]

		fullString += " To learn more about these stocks, ask me something like, 'Tell me about Apple'."

		print(fullString)

if typeOfInfo == "info":
	if len(ticker) > 5:
		r = requests.post('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + ticker + '&region=1&lang=en', verify=False)
		try:
			tickerSym = r.json()['ResultSet']['Result'][0]["symbol"]
			tickerName = r.json()['ResultSet']['Result'][0]["name"]
		except:
			print("Sorry, I couldn't find the company you were looking for, try asking for a different one.")
	else:
		r = requests.post('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + ticker + '&region=1&lang=en', verify=False)
		tickerSym = ticker
		try:
			tickerName = r.json()['ResultSet']['Result'][0]["name"]
		except:
			print("Sorry, I couldn't find the ticker you were looking for, try asking for a different one.")
	searches = wikipedia.search(tickerName)

	if len(searches) == 0:
		print("Sorry, I didn't find any info on " + ticker)
	else:
		print("Okay, here's some info about " + tickerName + ". " + wikipedia.summary(tickerName, sentences=4))

if typeOfInfo == "":
	print("Sorry, I didn't understand what you meant.")