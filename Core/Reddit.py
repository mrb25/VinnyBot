import praw
import random
import itertools

from praw import *


def main():
    print("--------------------")
    print("asdf " + random_hot_post(''))
    print("--------------------")



def random_hot_post(subreddit, limit):

    r = praw.Reddit(user_agent='Discord Bot', client_id='byorb8K1SwaO1g', client_secret='qFBAtKZuQfvWcOhmO495ia7BH68')
    submissions = r.subreddit(subreddit).hot(limit=limit)

    num = random.randrange(1, limit) - 1

    hot_page = list(itertools.islice(submissions, limit))

    random_page = hot_page[num]

    if random_page.stickied:
        return random_hot_post(subreddit, limit + 1)

    if subreddit != 'shitpost':
        return random_page.url

    linked_post = r.submission(url=random_page.url)
    return linked_post.url
