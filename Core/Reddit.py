import praw
import random
import itertools

import prawcore
from praw import *

def main():
    print("--------------------")
    print("asdf " + random_hot_post(''))
    print("--------------------")



def random_hot_post(subreddit, limit):

    r = praw.Reddit(user_agent='Discord Bot', client_id='byorb8K1SwaO1g', client_secret='qFBAtKZuQfvWcOhmO495ia7BH68')
    submissions = r.subreddit(subreddit).hot(limit=limit)

    if submissions is None:
        return None

    num = random.randrange(1, limit) - 1

    try:
        hot_page = list(itertools.islice(submissions, limit))
        if len(hot_page) == 0:
            return 'Failed to find post matching parameters.'
        random_page = hot_page[num]
    except:
        return None

    if random_page.stickied:
        return random_hot_post(subreddit, limit + 1)

    if subreddit != 'shitpost':
        return random_page.url

    linked_post = r.submission(url=random_page.url)
    return linked_post.url


def getCosplay(message, client):
    limit = 30
    r = praw.Reddit(user_agent='Discord Bot', client_id='byorb8K1SwaO1g', client_secret='qFBAtKZuQfvWcOhmO495ia7BH68')
    try:
        searchTerms = message.content.split(" ")[1]
        searchTerms.replace('_', ' ')
        submissions = r.subreddit('cosplay').search(searchTerms, limit=limit)

    except IndexError:
        submissions = r.subreddit('cosplay').hot(limit=limit)

    num = random.randrange(1, limit) - 1

    hot_page = list(itertools.islice(submissions, limit))

    if len(hot_page) == 0:
        return 'Failed to find post matching parameters.'

    random_page = hot_page[num]

    if random_page.stickied:
        return getCosplay(message, client)

    return random_page.url

def getCosplayGirl(message, client):
    limit = 30
    r = praw.Reddit(user_agent='Discord Bot', client_id='byorb8K1SwaO1g', client_secret='qFBAtKZuQfvWcOhmO495ia7BH68')

    try:
        searchTerms = message.content.split(" ")[1]
        searchTerms.replace('_', ' ')
        submissions = r.subreddit('cosplaygirls').search(searchTerms, limit=limit)

    except IndexError:
        submissions = r.subreddit('cosplaygirls').hot(limit=limit)

    num = random.randrange(1, limit) - 1

    hot_page = list(itertools.islice(submissions, limit))

    if len(hot_page) == 0:
        return 'Failed to find post matching parameters.'
    random_page = hot_page[num]

    if random_page.stickied:
        return getCosplay(message, client)

    return random_page.url
