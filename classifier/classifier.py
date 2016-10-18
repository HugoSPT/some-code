import json
import sys
import re

stop_words = {}
training_words = {}

def populate_training_words(training_set):
    """
        Populate the words per topic from the training set.
        We only considered a word if its occurrence is equals or bigger than three

        Args:
            training_set: the set containing the training data
    """

    global training_words

    for article in training_set:
        occurrences = get_bag_words(tokenize_article(article['content']))

        if article['topic'] not in training_words:
            training_words[article['topic']] = set()

        relevant = True
        num_words = 0

        while relevant and num_words < len(occurrences)-1:
            training_words[article['topic']].add(occurrences[num_words][0])
            num_words += 1
            relevant = occurrences[num_words][1] >= 3

def tokenize_article(article):
    """
        Splits a text into words and cleans them.

        Args:
            article: th article to be splitted and cleaned

        Returns
            tokenized: a list containing all the valid words
    """

    lower_article = article.lower()

    tokenized = [re.sub("[^a-z0-9']+",'', word) 
                for word in article.split(' ')
                if word not in stop_words]

    return tokenized

def get_bag_words(tokenized_article):
    """
        Counts the number of occurrences for a given word.

        Args:
            tokenized_article: the list of words to be counted

        Returns:
            sorted_occurrences: the list containing the words sorted by number of occurrences
    """

    occurrences = {}

    for word in tokenized_article:
        occurrences[word] = occurrences[word] + 1 if word in occurrences else 1

    sorted_occurrences = sorted(occurrences.items(), key=lambda word: word[1], reverse=True)

    return sorted_occurrences

def categorize_article(occurrences):
    """
        Categorize an article comparing the most frequent words with the words in the training set
        In case of a tie, it is returning the topic that appears in first after sorting (read more in README.md)

        Args:
            occurrences: the list containing the words sorted by number of occurrences

        Returns:
            topics_score: the score obtained for each topic
            selected_topic: the topic with highest score
    """

    topics_score = {topic:0 for topic in training_words}

    for word in occurrences:
        for topic, words in training_words.items():
            if word[0] in words and word[1] >= 2:
                topics_score[topic] += word[1]

    selected_topic = sorted(topics_score.items(), key=lambda word: word[1], reverse=True)[0][0]
    
    return topics_score, selected_topic

if __name__ == '__main__':

    with open(sys.argv[1]) as f:
        articles = json.loads(f.read())['articles'] # Loads articles from the file given as argument

    with open('stop_words.json') as f:
        stop_words = json.loads(f.read())['stop_words'] # Loads the words to be ignored (includes punctuation as well)
    
    with open('training_set.json') as f:
        training_set = json.loads(f.read())['articles'] # Loads the training set

    populate_training_words(training_set)

    # Contains the cluster of artices and will be written in the end
    cluster = {}

    for article in articles:
        tokenized_article = tokenize_article(article['content'])
        occurrences = get_bag_words(tokenized_article)
        scores, topic = categorize_article(occurrences)

        article['scores'] = scores

        if topic not in cluster:
            cluster[topic] = []
        cluster[topic].append(article)


        print "Article title \"{}\" categorized as {}.".format(article['title'].encode('utf-8'), topic)
        print "Scores obtained: {}\n".format(scores)

    with open('results.json', 'w') as outfile:
        json.dump(cluster, outfile, indent=4)
        print "Clustering results written to results.json"



