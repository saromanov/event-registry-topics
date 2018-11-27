from eventregistry import *
import json

def queryCategory(category=None, 
	keywords=[], 
	concept=None, 
	dateStart=datetime.date(2017, 8, 27), 
	dateEnd=datetime.date(2017, 8, 29),
	locations=[],
	count=10,
	sortBy="sourceImportanceRank"
	):
	er = EventRegistry(apiKey = API_KEY)
	q = QueryArticles(
		lang="eng",
		# set the date limit of interest
		dateStart = dateStart, dateEnd = dateEnd,
		conceptUri=er.getConceptUri(concept),
		# find articles mentioning the company Apple
		categoryUri = er.getCategoryUri(category))
	# return the list of top 30 articles, including the concepts, categories and article image
	q.setRequestedResult(RequestArticlesInfo(sortBy="sourceImportanceRank", page = 1, count = count, returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(categories = True, image=True, socialScore=True, location=True, details=True, videos=True))))
	res = er.execQuery(q)
	return res

def queryEvents(category=None, 
	keywords=[], 
	concept=None, 
	dateStart=datetime.date(2017, 8, 23), 
	dateEnd=datetime.date(2017, 8, 29),
	locations=[],
	count=10,
	sortBy="sourceImportanceRank"
	):
	er = EventRegistry(apiKey = "1d3ce38b-3606-4bb3-94b5-904df0583c3c")
	q = QueryEvents(
		lang="eng",
		# set the date limit of interest
		dateStart = dateStart, dateEnd = dateEnd,
		conceptUri=er.getConceptUri(concept),
		# find articles mentioning the company Apple
		categoryUri = er.getCategoryUri(category))
	# return the list of top 30 articles, including the concepts, categories and article image
	q.setRequestedResult(RequestEventsInfo(sortBy=sortBy, page = 1, count = count, returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(categories = True, image=True, socialScore=True, location=True, details=True, videos=True))))
	res = er.execQuery(q)
	return res


def getTrendingCategories():
	er = EventRegistry(apiKey = "1d3ce38b-3606-4bb3-94b5-904df0583c3c")
	q = GetTrendingCategories(source = "news", count = 10,returnInfo = ReturnInfo(categoryInfo = CategoryInfoFlags(parentUri = True, childrenUris = True, trendingHistory = True)))
	ret = er.execQuery(q)
	return ret

def jsonProcessingArticles(data):
	'''
		getting articles from response 
	'''
	result = json.loads(data)
	articles = result['articles']
	return parseArticlesResponse(articles)

def jsonProcessingEvents(data):
	result = json.loads(data)
	events = result['events']
	return parseEventsResponse(events)

def parseArticlesResponse(data):
	'''
		parsing of response from event registry
	'''
	if 'articles' not in data:
		return
	data = data['articles']
	response = {'type': 'articles'}
	if 'totalResults' in data:
		response['total_results'] = data['totalResults']
	if 'pages' in data:
		response['pages'] = data['pages']
	if 'results' in data:
		articles_response = data['results']
		response['articles'] = list(processing_articles(articles_response))
	return response

def parseEventsResponse(data):
	'''
		parsing of response from event registry
	'''
	if 'events' not in data:
		return
	data = data['events']
	response = {'type': 'events'}
	if 'totalResults' in data:
		response['total_results'] = data['totalResults']
	if 'pages' in data:
		response['pages'] = data['pages']
	if 'results' in data:
		articles_response = data['results']
		response['events'] = list(processing_events(articles_response))
	return response

def processing_articles(articles):
	'''
		prepare response for articles
	'''

	for article in articles:
		yield {"url": article['url'], 'title': article['title'], 'date_time': article['dateTime'], 'sim': article['sim'], 'categories': article['categories']}

def processing_categories(categories):
	return {"label": category['label'] for category in categories}


def processing_events(events):
	'''
		prepare response for events
	'''

	for event in events:
		yield {"title": event['title']['eng'], "total_article_count": event['totalArticleCount'], 'summary': event['summary']['eng'], 'event_date': event['eventDate'], 'concepts': event['concepts'], 'categories': event['categories']}


def mockMethods():
	f = open('mockArticles.json', 'r')
	response = jsonProcessingArticles(f.read())
	return response

def mockEvents():
	f = open('mockEvents.json', 'r')
	response = jsonProcessingEvents(f.read())
	return response


#mockEvents()

#result = getTrendingCategories()
#print(result)