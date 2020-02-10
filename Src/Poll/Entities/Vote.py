import time

class Vote(object):
    canVote = False
    timeOpened = time.time()
    resultDict = {}