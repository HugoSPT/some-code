import twitter
import json
from collections import Counter
from prettytable import PrettyTable

CONSUMER_KEY       = "<consumer_key>"
CONSUMER_SECRET    = "<consumer_secret>"
OAUTH_TOKEN        = "<token>"
OAUTH_TOKEN_SECRET = "<token_secret>"

WORLD_WOE_ID = 1
US_WOE_ID    = 23424977


#connecting to twitter
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

##### getting world and us trends ####
world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
us_trends = twitter_api.trends.place(_id=US_WOE_ID)

#store the important data in sets
world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])
us_trends_set = set([trend['name'] for trend in us_trends[0]['trends']])

common_trends = world_trends_set.intersection(us_trends_set)

#Lets check one of the trends
#### so let's collect some search results ####
q = list(common_trends)[0]
count = 100

search_results = twitter_api.search.tweets(q=q, count=count)
statuses = json.loads(json.dumps(search_results['statuses']))

for _ in range(5):
	print("Lenght of statutes", len(statuses))
	try:
		next_results = search_results['search_metadata']['next_results']
	except KeyError as e:
		print("No more results")
		break

	kwargs = dict([kv.split('=') for kv in next_results[1:].split('&')])
	search_results = twitter_api.search.tweets(**kwargs)
	for status in json.loads(json.dumps(search_results['statuses'])):
	    statuses.append(status)

#let's get some text, usernames, hashtags
status_text = [status['text'] for status in statuses]
screen_names = [user_mention['screen_name'] for status in statuses for user_mention in status['entities']['user_mentions']]
hashtags = [hashtag['text'] for status in statuses for hashtag in status['entities']['hashtags']]
words = [w for t in status_text for w in t.split()]

print(json.dumps(status_text[0:10], indent=1))
print(json.dumps(screen_names[0:5], indent=1))
print(json.dumps(hashtags[0:5], indent=1))
print(json.dumps(words[0:5], indent=1))

for label, data in (('Word', words), 
                ('Screen name', screen_names), 
                ('Hashtag', hashtags)):

    pt = PrettyTable(field_names=[label, 'Count'])
    c = Counter(data)
    [pt.add_row(kv) for kv in c.most_common()[:10]]
    pt.align[label], pt.align['Count'] = 'l', 'r'
    print(pt)
    

def lexical_diversity(tokens):
    return 1.0 * len(set(tokens)) / len(tokens) #number of unique words / number of total words
    
def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0 * total_words / len(statuses)

print("Lexical diversity for words: ", lexical_diversity(words))
print("Lexical diversity for screen_names: ", lexical_diversity(screen_names))
print("Lexical diversity for hashtags: ",lexical_diversity(hashtags))
print("Average words: ", average_words(status_text))
print

retweets = set([
	(status['retweet_count'], status['retweeted_status']['user']['screen_name'], status['text']) 
	for status in statuses if 'retweeted_status' in status
])

pt = PrettyTable(field_names=['Count', 'Screen name', 'Text'])
[pt.add_row(row) for row in sorted(retweets, reverse=True)[:5]]
pt.max_width['Text'] = 50
pt.align = 'l'
print(pt)
