import json
import urllib2
import requests
import unicodecsv
import time
import sys

def apirequest(url, user, token):
	data = []
	r = requests.get(url,auth=(user,token))
	while r.status_code == 429:
		time.sleep(10)
		r = requests.get(url,auth=(user,token))
	z = json.loads(r.text)
	if (r.status_code >= 400):
		print z['errorMessage']
		print 'Exiting...'
		sys.exit()
	data.append(z)
	if 'pages' in z:
		if 'next' in z['pages']:
			morepages = 1
			url = z['pages']['next']
			while morepages == 1:
				done = 0
				while done == 0:
					try:
						r = requests.get(url,auth=(user,token))
						done = 1
					except:
						done = 0
						print 'Error retrieving data, sleeping for 20 seconds before trying again'
						time.sleep(20)
				while r.status_code == 429:
					print 'Too many requests, sleeping for 30 seconds before trying again'
					done2 = 0
					time.sleep(30)
					while done2 == 0:
						try:
							r = requests.get(url,auth=(user,token))
							done2 = 1
						except:
							done2 = 0
							print 'Error retrieving data, sleeping for 20 seconds before trying again'
							time.sleep(20)
				z = json.loads(r.text)
				if (r.status_code >= 400):
					print z['errorMessage']
					print 'Exiting...'
					sys.exit()
				data.append(z)
				if 'next' in z['pages']:
					url = z['pages']['next']
				else:
					morepages = 0
	return data
	
def writecsv(dataset,targetfile):
	outfile = open(targetfile,"wb")
	writer = unicodecsv.writer(outfile)
	writer.writerows(dataset)
	outfile.close()

def formatagentdata(dataset):
	data = []
	data.append(['AgentId','AgentName','AgentType','Location','CountryId'])
	for page in dataset:
		for item in page['agents']:
			data.append([item['agentId'],item['agentName'],item['agentType'],item['location'],item['countryId']])
	return data

def formathttptest(dataset):
	data = []
	data.append(['TestId','TestName','TestType','TestTarget','TestInterval'])
	for page in dataset:
		for item in page['test']:
			data.append([item['testId'],item['testName'],item['type'],item['url'],item['interval']])
	return data
	
def formatpageloadtest(dataset):
	data = []
	data.append(['TestId','TestName','TestType','TestTarget','TestInterval','HttpInterval'])
	for page in dataset:
		for item in page['test']:
			data.append([item['testId'],item['testName'],item['type'],item['url'],item['interval'],item['httpInterval']])
	return data

def formattxtest(dataset):
	data = []
	data.append(['TestId','TestName','TestType','TestTarget','TestInterval','TotalSteps'])
	for page in dataset:
		for item in page['test']:
			data.append([item['testId'],item['testName'],item['type'],item['url'],item['interval'],item['totalSteps']])
	return data

def formatnetworktest(dataset):
	data = []
	data.append(['TestId','TestName','TestType','TestTarget','Protocol','TestInterval'])
	for page in dataset:
		for item in page['test']:
			data.append([item['testId'],item['testName'],item['type'],item['server'],item['protocol'],item['interval']])
	return data

def formatdnstracetest(dataset):
	data = []
	data.append(['TestId','TestName','TestType','TestTarget','TestInterval'])
	for page in dataset:
		for item in page['test']:
			data.append([item['testId'],item['testName'],item['type'],item['domain'],item['interval']])
	return data

def formatdnsservertest(dataset):
	data = []
	header = ['TestId','TestName','TestType','TestTarget','TestInterval']
	testinfo = dataset[0]['test'][0]
	dataline = [testinfo['testId'],testinfo['testName'],testinfo['type'],testinfo['domain'],testinfo['interval']]
	x = 1
	for dnsserv in testinfo['dnsServers']:
		servid = 'Server' + str(x) + 'Id'
		servname = 'Server' + str(x) + 'Name'
		header.append(servid)
		header.append(servname)
		dataline.append(dnsserv['serverId'])
		dataline.append(dnsserv['serverName'])
		x = x + 1
	data.append(header)
	data.append(dataline)
	return data

def formatbgptest(dataset):
	data = []
	data.append(['TestId','TestName','TestType','TestTarget'])
	for page in dataset:
		for item in page['test']:
			data.append([item['testId'],item['testName'],item['type'],item['prefix']])
	return data

def formathttpdata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','ServerIp','ResponseCode','NumRedirects','ErrorType','DnsTime','ConnectTime','SslTime','WaitTime','ReceiveTime','WireSize','ResponseTime','FetchTime','ErrorDetails'])
	thetestid = dataset[0]['web']['test']['testId']
	for page in dataset:
		if len(page['web']['httpServer']) > 0:
			for item in page['web']['httpServer']:
				if 'serverIp' in item:
					serverIp = item['serverIp']
				else:
					serverIp = ''
				if 'responseCode' in item:
					responseCode = item['responseCode']
				else:
					responseCode = ''
				if 'numRedirects' in item:
					numRedirects = item['numRedirects']
				else:
					NumRedirects = ''
				if 'errorType' in item:
					errorType = item['errorType']
				else:
					errorType = ''
				if 'dnsTime' in item:
					dnsTime = item['dnsTime']
				else:
					dnsTime = ''
				if 'connectTime' in item:
					connectTime = item['connectTime']
				else:
					connectTime = ''
				if 'sslTime' in item:
					sslTime = item['sslTime']
				else:
					sslTime = ''
				if 'waitTime' in item:
					waitTime = item['waitTime']
				else:
					waitTime = ''
				if 'receiveTime' in item:
					receiveTime = item['receiveTime']
				else:
					receiveTime = ''
				if 'wireSize' in item:
					wireSize = item['wireSize']
				else:
					wireSize = ''
				if 'responseTime' in item:
					responseTime = item['responseTime']
				else:
					responseTime = ''
				if 'fetchTime' in item:
					fetchTime = item['fetchTime']
				else:
					fetchTime = ''
				if 'errorDetails' in item:
					errorDetails = item['errorDetails']
				else:
					errorDetails = ''
				data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],serverIp,responseCode,numRedirects,errorType,dnsTime,connectTime,sslTime,waitTime,receiveTime,wireSize,responseTime,fetchTime,errorDetails])
	if len(data) == 1:
		print 'No data available for this time period'
		print 'Exiting...'
		sys.exit()
	return data

def formatpageloaddata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','ResponseTime','TotalSize','NumObjects','NumErrors','DomLoadTime','PageLoadTime'])
	thetestid = dataset[0]['web']['test']['testId']
	for page in dataset:
		if len(page['web']['pageLoad']) > 0:
			for item in page['web']['pageLoad']:
				if 'responseTime' in item:
					responseTime = item['responseTime']
				else:
					responseTime = ''
				if 'totalSize' in item:
					totalSize = item['totalSize']
				else:
					totalSize = ''
				if 'numObjects' in item:
					numObjects = item['numObjects']
				else:
					numObjects = ''
				if 'numErrors' in item:
					numErrors = item['numErrors']
				else:
					numErrors = ''
				if 'domLoadTime' in item:
					domLoadTime = item['domLoadTime']
				else:
					domLoadTime = ''
				if 'pageLoadTime' in item:
					pageLoadTime = item['pageLoadTime']
				else:
					pageLoadTime = ''
				data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],responseTime,totalSize,numObjects,numErrors,domLoadTime,pageLoadTime])
	if len(data) == 1:
		print 'No data available for this time period'
		print 'Exiting...'
		sys.exit()
	return data
	
def formattxsumdata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','TotalSteps','StepsCompleted','TransactionTime','ComponentErrors'])
	thetestid = dataset[0]['web']['test']['testId']
	for page in dataset:
		if len(page['web']['transaction']) > 0:
			for item in page['web']['transaction']:
				if 'totalSteps' in item:
					totalSteps = item['totalSteps']
				else:
					totalSteps = ''
				if 'stepsCompleted' in item:
					stepsCompleted = item['stepsCompleted']
				else:
					stepsCompleted = ''
				if 'transactionTime' in item:
					transactionTime = item['transactionTime']
				else:
					transactionTime = ''
				if 'componentErrors' in item:
					componentErrors = item['componentErrors']
				else:
					componentErrors = ''
				data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],totalSteps,stepsCompleted,transactionTime,componentErrors])
	if len(data) == 1:
		print 'No data available for this time period'
		print 'Exiting...'
		sys.exit()
	return data

def formatbgpdata(dataset):
	data = []
	data.append(['TestId','RoundId','Date','CountryId','PrefixId','Prefix','MonitorName','Reachability','Updates','PathChanges'])
	thetestid = dataset[0]['net']['test']['testId']
	for page in dataset:
		if len(page['net']['bgpMetrics']) > 0:
			for item in page['net']['bgpMetrics']:
				if 'countryId' in item:
					countryId = item['countryId']
				else:
					countryId = ''
				if 'prefixId' in item:
					prefixId = item['prefixId']
				else:
					prefixId = ''
				if 'prefix' in item:
					prefix = item['prefix']
				else:
					prefix = ''
				if 'monitorName' in item:
					monitorName = item['monitorName']
				else:
					monitorName = ''
				if 'reachability' in item:
					reachability = item['reachability']
				else:
					reachability = ''
				if 'updates' in item:
					updates = item['updates']
				else:
					updates = ''
				if 'pathChanges' in item:
					pathChanges = item['pathChanges']
				else:
					pathChanges = ''
				data.append([thetestid,item['roundId'],item['date'],countryId,prefixId,prefix,monitorName,reachability,updates,pathChanges])
	if len(data) == 1:
		print 'No data available for this time period'
		print 'Exiting...'
		sys.exit()
	return data

def formate2edata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','ServerIp','Server','Loss','MinLatency','AvgLatency','MaxLatency','Jitter'])
	thetestid = dataset[0]['net']['test']['testId']
	for page in dataset:
		if len(page['net']['metrics']) > 0:
			for item in page['net']['metrics']:
				if 'serverIp' in item:
					serverIp = item['serverIp']
				else:
					serverIp = ''
				if 'loss' in item:
					loss = item['loss']
				else:
					loss = ''
				if 'minLatency' in item:
					minLatency = item['minLatency']
				else:
					minLatency = ''
				if 'avgLatency' in item:
					avgLatency = item['avgLatency']
				else:
					avgLatency = ''
				if 'maxLatency' in item:
					maxLatency = item['maxLatency']
				else:
					maxLatency = ''
				if 'jitter' in item:
					jitter = item['jitter']
				else:
					jitter = ''
				data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],serverIp,item['server'],loss,minLatency,avgLatency,maxLatency,jitter])
	if len(data) == 1:
		print 'No data available for this time period'
		print 'Exiting...'
		sys.exit()
	return data

def formatpathsumdata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','ServerIp','Server','PathId','NumberofHops','IpAddress','ResponseTime'])
	thetestid = dataset[0]['net']['test']['testId']
	for page in dataset:
		for item in page['net']['pathVis']:
			if 'serverIp' in item:
				serverIp = item['serverIp']
			else:
				serverIp = ''
			for subitem in item['endpoints']:
				if 'pathId' in subitem:
					pathId = subitem['pathId']
				else:
					pathId = ''
				if 'numberOfHops' in subitem:
					numberOfHops = subitem['numberOfHops']
				else:
					numberOfHops = ''
				if 'ipAddress' in subitem:
					ipAddress = subitem['ipAddress']
				else:
					ipAddress = ''
				if 'responseTime' in subitem:
					responseTime = subitem['responseTime']
				else:
					responseTime = ''
				data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],serverIp,item['server'],pathId,numberOfHops,ipAddress,responseTime])
	return data

def formatdnstracedata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','Queries','FinalQueryTime','Mappings','ErrorDetails','Output'])
	thetestid = dataset[0]['dns']['test']['testId']
	for page in dataset:
		if len(page['dns']['trace']) > 0:
			for item in page['dns']['trace']:
				if 'queries' in item:
					queries = item['queries']
				else:
					queries = ''
				if 'finalQueryTime' in item:
					finalQueryTime = item['finalQueryTime']
				else:
					finalQueryTime = ''
				if 'mappings' in item:
					mappings = item['mappings']
				else:
					mappings = ''
				if 'errorDetails' in item:
					errorDetails = item['errorDetails']
				else:
					errorDetails = ''
				if 'output' in item:
					temp = item['output']
					output = temp.replace('\n','  /  ')
				else:
					output = ''
				data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],queries,finalQueryTime,mappings,errorDetails,output])
	if len(data) == 1:
		print 'No data available for this time period'
		print 'Exiting...'
		sys.exit()
	return data
	
def formatdnsservdata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','ServerId','Server','ResolutionTime','Mappings','ErrorDetails'])
	thetestid = dataset[0]['dns']['test']['testId']
	for page in dataset:
		if len(page['dns']['server']) > 0:
			for item in page['dns']['server']:
				if 'serverId' in item:
					serverId = item['serverId']
				else:
					serverId = ''
				if 'server' in item:
					server = item['server']
				else:
					server = ''
				if 'resolutionTime' in item:
					resolutionTime = item['resolutionTime']
				else:
					resolutionTime = ''
				if 'mappings' in item:
					mappings = item['mappings']
				else:
					mappings = ''
				if 'errorDetails' in item:
					errorDetails = item['errorDetails']
				else:
					errorDetails = ''
				data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],serverId,server,resolutionTime,mappings,errorDetails])
	if len(data) == 1:
		print 'No data available for this time period'
		print 'Exiting...'
		sys.exit()
	return data

def formatpathvisdata(dataset):
	data = []
	data.append(['TestId','RoundId','AgentId','AgentName','Date','ServerIp','Server','PathId','Hop','IpAddress','Prefix','rdns','Network','ResponseTime','Location'])
	thetestid = dataset[0]['net']['test']['testId']
	for page in dataset:
		for item in page['net']['pathVis']:
			if 'serverIp' in item:
				serverIp = item['serverIp']
			else:
				serverIp = ''
			for subitem in item['routes']:
				if 'pathId' in subitem:
					pathId = subitem['pathId']
				else:
					pathId = ''
				for hopitem in subitem['hops']:
					if 'hop' in hopitem:
						hop = hopitem['hop']
					else:
						hop = ''
					if 'ipAddress' in hopitem:
						ipAddress = hopitem['ipAddress']
					else:
						ipAddress = ''
					if 'prefix' in hopitem:
						prefix = hopitem['prefix']
					else:
						prefix = ''
					if 'rdns' in hopitem:
						rdns = hopitem['rdns']
					else:
						rdns = ''
					if 'network' in hopitem:
						network = hopitem['network']
					else:
						network = ''
					if 'responseTime' in hopitem:
						responseTime = hopitem['responseTime']
					else:
						responseTime = ''
					if 'location' in hopitem:
						location = hopitem['location']
					else:
						location = ''
					data.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],serverIp,item['server'],pathId,hop,ipAddress,prefix,rdns,network,responseTime,location])
	return data
	
def formattxdetaildata(dataset):
	pages = []
	steps = []
	pages.append(['TestId','RoundId','AgentId','AgentName','Date','TotalSteps','StepsCompleted','TransactionTime','ComponentErrors','PageNum','PageName','ComponentCount','ErrorCount','Duration'])
	steps.append(['TestId','RoundId','AgentId','AgentName','Date','TotalSteps','StepsCompleted','TransactionTime','ComponentErrors','PageNum','StepNum','Duration','Offset'])
	thetestid = dataset[0]['web']['test']['testId']
	for page in dataset:
		for item in page['web']['transaction']:
			if 'totalSteps' in item:
				totalSteps = item['totalSteps']
			else:
				totalSteps = ''
			if 'stepsCompleted' in item:
				stepsCompleted = item['stepsCompleted']
			else:
				stepsCompleted = ''
			if 'transactionTime' in item:
				transactionTime = item['transactionTime']
			else:
				transactionTime = ''
			if 'componentErrors' in item:
				componentErrors = item['componentErrors']
			else:
				componentErrors = ''
			for subitem in item['steps']:
				if 'pageNum' in subitem:
					pageNum = subitem['pageNum']
				else:
					pageNum = ''
				if 'stepNum' in subitem:
					stepNum = subitem['stepNum']
				else:
					stepNum = ''
				if 'duration' in subitem:
					duration = subitem['duration']
				else:
					duration = ''
				if 'offset' in subitem:
					offset = subitem['offset']
				else:
					offset = ''
				steps.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],totalSteps,stepsCompleted,transactionTime,componentErrors,pageNum,stepNum,duration,offset])
			for subthing in item['pages']:
				if 'pageNum' in subthing:
					pageNum = subthing['pageNum']
				else:
					pageNum = ''
				if 'pageName' in subthing:
					pageName = subthing['pageName']
				else:
					pageName = ''
				if 'componentCount' in subthing:
					componentCount = subthing['componentCount']
				else:
					componentCount = ''
				if 'errorCount' in subthing:
					errorCount = subthing['errorCount']
				else:
					errorCount = ''
				if 'duration' in subthing:
					duration = subthing['duration']
				else:
					duration = ''
				pages.append([thetestid,item['roundId'],item['agentId'],item['agentName'],item['date'],totalSteps,stepsCompleted,transactionTime,componentErrors,pageNum,pageName,componentCount,errorCount,duration])
	data = [steps,pages]
	return data

def getdetailedpaths(testid,user,token,baseurl,pathsummary):
	allpaths = []
	pathurl = baseurl + 'net/path-vis/' + testid + '/'
	x = 1
	for page in pathsummary:
		for item in page['net']['pathVis']:
			agid = str(item['agentId'])
			rndid = str(item['roundId'])
			targeturl = pathurl + agid + '/' + rndid + '.json'
			#if (x % 10) == 0:
			#	time.sleep(5)
			if (x % 100) == 0:
				print 'Retrieving detailed path data, please be patient...'
			p = apirequest(targeturl,user,token)
			x = x + 1
			allpaths.append(p[0])
	return allpaths

def gettxdetails(testid,user,token,baseurl,txsummary):
	alltx = []
	txurl = baseurl + 'web/transactions/' + testid + '/'
	x = 1
	for page in txsummary:
		for item in page['web']['transaction']:
			agid = str(item['agentId'])
			rndid = str(item['roundId'])
			targeturl = txurl + agid + '/' + rndid + '.json'
			#if (x % 10) == 0:
			#	time.sleep(5)
			if (x % 100) == 0:
				print 'Retrieving detailed transaction data, please be patient...'
			p = apirequest(targeturl,user,token)
			x = x + 1
			alltx.append(p[0])
	return alltx


	
baseurl = 'https://api.thousandeyes.com/'

if len(sys.argv) == 1:
	print '\n'
	print 'Usage => testid start_time end_time user_name user_token output_path pathsummary(optional) detailedpaths(optional - must use with pathsummary) bgp(optional - not required for bgp tests)'
	print '\n'
	print 'Use forward slashes for the path when running on Windows'
	sys.exit()
elif (len(sys.argv) < 7) or (len(sys.argv) > 10):
	print 'Invalid number of arguments'
	sys.exit()
else:
	testid = sys.argv[1]
	start_time = sys.argv[2]
	end_time = sys.argv[3]
	username = sys.argv[4]
	usertoken = sys.argv[5]
	outputpath = sys.argv[6]
	bgp = 'no'
	detailedpaths = 'no'
	pathsummary = 'no'
	netmeasurements = '0'
	if len(sys.argv) == 8:
		if (sys.argv[7] <> 'bgp') and (sys.argv[7] <> 'pathsummary'):
			print 'Invalid arguments'
			sys.exit()
		else:
			if (sys.argv[7] == 'bgp'):
				bgp = 'yes'
			elif (sys.argv[7] == 'pathsummary'):
				pathsummary = 'yes'
	if len(sys.argv) == 9:
		if ((sys.argv[7] <> 'pathsummary') and (sys.argv[8] <> 'detailedpaths')) or ((sys.argv[7] <> 'pathsummary') and (sys.argv[8] <> 'bgp')):
			print 'Invalid arguments'
			sys.exit()
		else:
			if (sys.argv[7] == 'pathsummary'):
				pathsummary = 'yes'
				if (sys.argv[8] == 'detailedpaths'):
					detailedpaths = 'yes'
				elif (sys.argv[8] == 'bgp'):
					bgp = 'yes'
	if len(sys.argv) == 10:
		if (sys.argv[7] <> 'pathsummary') and (sys.argv[8] <> 'detailedpaths') and (sys.argv[9] <> 'bgp'):
			print 'Invalid arguments'
			sys.exit()
		else:
			if (sys.argv[7] == 'pathsummary'):
				pathsummary = 'yes'
			if (sys.argv[8] == 'detailedpaths'):
				detailedpaths = 'yes'
			if (sys.argv[9] == 'bgp'):
				bgp = 'yes'
	timestring = '?from=' + start_time + '&to=' + end_time
	targeturl = baseurl + 'tests/' + testid + '.json'
	testdata = apirequest(targeturl,username,usertoken)
	print 'Test information retrieved...'
	testtype = testdata[0]['test'][0]['type']
	status = testdata[0]['test'][0]['enabled']
	if status == 0:
		print 'Test disabled, please enable this test before retreiving data'
		print 'Exiting...'
		sys.exit()
	print 'Test type => ' + testtype
	if testtype <> 'bgp':
		targeturl = baseurl + 'agents.json'
		agentlist = apirequest(targeturl,username,usertoken)
		print 'Agent list retrieved...'
		fagentlist = formatagentdata(agentlist)
		if outputpath.endswith('/'):
			outputfile = outputpath + testid + 'agents' + '.csv'
		else:
			outputfile = outputpath + '/' + testid + 'agents' + '.csv'
		writecsv(fagentlist,outputfile)
		print 'Agent information written to ' + outputfile
	if (testtype <> 'network') and (testtype <> 'http-server') and (testtype <> 'page-load') and (testtype <> 'dns-trace') and (testtype <> 'bgp') and (testtype <> 'dns-server') and (testtype <> 'transactions'):
		print 'Test type not yet implemented'
		sys.exit()
	else:
		if testtype == 'transactions':
			ftestdata = formattxtest(testdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'testinfo' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'testinfo' + '.csv'
			writecsv(ftestdata,outputfile)
			print 'Test information written to ' + outputfile
			targeturl = baseurl + 'web/transactions/' + testid + '.json' + timestring
			txsumdata = apirequest(targeturl,username,usertoken)
			print 'Transaction summary data retrieved...'
			ftxsumdata = formattxsumdata(txsumdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'txsum' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'txsum' + '.csv'
			writecsv(ftxsumdata,outputfile)
			print 'Transaction summary data written to ' + outputfile
			txdetaildata = gettxdetails(testid,username,usertoken,baseurl,txsumdata)
			print 'Detailed transaction data retrieved...'
			ftxdetaildata = formattxdetaildata(txdetaildata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'txstep' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'txstep' + '.csv'
			writecsv(ftxdetaildata[0],outputfile)
			print 'Transaction step details written to ' + outputfile
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'txpage' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'txpage' + '.csv'
			writecsv(ftxdetaildata[1],outputfile)
			print 'Transaction page details written to ' + outputfile
		if testtype == 'page-load':
			ftestdata = formatpageloadtest(testdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'testinfo' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'testinfo' + '.csv'
			writecsv(ftestdata,outputfile)
			print 'Test information written to ' + outputfile
			targeturl = baseurl + 'web/page-load/' + testid + '.json' + timestring
			pageloaddata = apirequest(targeturl,username,usertoken)
			print 'Page load metrics retrieved...'
			fpageloaddata = formatpageloaddata(pageloaddata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'pageload' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'pageload' + '.csv'
			writecsv(fpageloaddata,outputfile)
			print 'Page load metrics written to ' + outputfile
		if testtype == 'http-server':
			ftestdata = formathttptest(testdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'testinfo' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'testinfo' + '.csv'
			writecsv(ftestdata,outputfile)
			print 'Test information written to ' + outputfile
		if (testtype == 'http-server') or (testtype == 'page-load'):
			netmeasurements = str(testdata[0]['test'][0]['networkMeasurements'])
			print 'Network Measurements = ' + netmeasurements
			targeturl = baseurl + 'web/http-server/' + testid + '.json' + timestring
			httpdata = apirequest(targeturl,username,usertoken)
			print 'Http server metrics retrieved...'
			fhttpdata = formathttpdata(httpdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'httpserv' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'httpserv' + '.csv'
			writecsv(fhttpdata,outputfile)
			print 'Http server metrics written to ' + outputfile
		if testtype == 'network':
			netmeasurements = '1'
			ftestdata = formatnetworktest(testdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'testinfo' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'testinfo' + '.csv'
			writecsv(ftestdata,outputfile)
			print 'Test information written to ' + outputfile
		if testtype == 'bgp':
			bgp = 'yes'
			ftestdata = formatbgptest(testdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'testinfo' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'testinfo' + '.csv'
			writecsv(ftestdata,outputfile)
			print 'Test information written to ' + outputfile
		if testtype ==  'dns-trace':
			ftestdata = formatdnstracetest(testdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'testinfo' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'testinfo' + '.csv'
			writecsv(ftestdata,outputfile)
			print 'Test information written to ' + outputfile
			targeturl = baseurl + 'dns/trace/' + testid + '.json' + timestring
			dnstracedata = apirequest(targeturl,username,usertoken)
			print 'DNS trace metrics retrieved...'
			fdnstracedata = formatdnstracedata(dnstracedata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'dnstrace' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'dnstrace' + '.csv'
			writecsv(fdnstracedata,outputfile)
			print 'DNS trace metrics written to ' + outputfile
		if testtype == 'dns-server':
			ftestdata = formatdnsservertest(testdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'testinfo' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'testinfo' + '.csv'
			writecsv(ftestdata,outputfile)
			print 'Test information written to ' + outputfile
			netmeasurements = str(testdata[0]['test'][0]['networkMeasurements'])
			print 'Network Measurements = ' + netmeasurements
			targeturl = baseurl + 'dns/server/' + testid + '.json' + timestring
			dnsservdata = apirequest(targeturl,username,usertoken)
			print 'DNS server metrics retrieved...'
			fdnsservdata = formatdnsservdata(dnsservdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'dnsserv' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'dnsserv' + '.csv'
			writecsv(fdnsservdata,outputfile)
			print 'DNS server metrics written to ' + outputfile
		if (testtype == 'network') or (testtype == 'http-server') or (testtype == 'page-load') or (testtype == 'dns-server'):
			if netmeasurements == '1':
				targeturl = baseurl + 'net/metrics/' + testid + '.json' + timestring
				e2edata = apirequest(targeturl,username,usertoken)
				print 'End to end metrics retrieved...'
				fe2edata = formate2edata(e2edata)
				if outputpath.endswith('/'):
					outputfile = outputpath + testid + 'e2e' + '.csv'
				else:
					outputfile = outputpath + '/' + testid + 'e2e' + '.csv'
				writecsv(fe2edata,outputfile)
				print 'End-to-end metrics written to ' + outputfile
				if pathsummary == 'yes':
					targeturl = baseurl + 'net/path-vis/' + testid + '.json' + timestring
					pathsumdata = apirequest(targeturl,username,usertoken)
					print 'Path summary data retrieved...'
					fpathsumdata = formatpathsumdata(pathsumdata)
					if outputpath.endswith('/'):
						outputfile = outputpath + testid + 'pathsum' + '.csv'
					else:
						outputfile = outputpath + '/' + testid + 'pathsum' + '.csv'
					writecsv(fpathsumdata,outputfile)
					print 'Path summary data written to ' + outputfile
					if detailedpaths == 'yes':
						pathdetaildata = getdetailedpaths(testid,username,usertoken,baseurl,pathsumdata)
						print 'Detailed path data retrieved...'
						fpathdetaildata = formatpathvisdata(pathdetaildata)
						if outputpath.endswith('/'):
							outputfile = outputpath + testid + 'pathvis' + '.csv'
						else:
							outputfile = outputpath + '/' + testid + 'pathvis' + '.csv'
						writecsv(fpathdetaildata,outputfile)
						print 'Detailed path data written to ' + outputfile
		if bgp == 'yes':
			targeturl = baseurl + 'net/bgp-metrics/' + testid + '.json' + timestring
			bgpdata = apirequest(targeturl,username,usertoken)
			print 'BGP data retrieved...'
			fbgpdata = formatbgpdata(bgpdata)
			if outputpath.endswith('/'):
				outputfile = outputpath + testid + 'bgp' + '.csv'
			else:
				outputfile = outputpath + '/' + testid + 'bgp' + '.csv'
			writecsv(fbgpdata,outputfile)
			print 'BGP metrics written to ' + outputfile
				
		
		
			
			
		
	

		

	
	
	
