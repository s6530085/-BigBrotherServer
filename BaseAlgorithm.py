# coding=UTF-8
__author__ = 'study_sun'

import random

def geneRandomDistinctList(totalCount, minValue, maxValue):
    return geneRandomDistinctListPrefer([], totalCount, minValue, maxValue)

def geneRandomDistinctListPrefer(prefer, totalCount, minValue, maxValue):
    return geneRandomDistinctListPrefer(prefer, [], totalCount, minValue, maxValue)

def geneRandomDistinctListPrefer(prefer, exclude, totalCount, minValue, maxValue):
    sourceList = list(prefer)
    while (len(sourceList) < totalCount):
        while (1):
            r = random.choice(range(minValue,maxValue))
            if not (r in sourceList):
                if not (r in exclude):
                    sourceList.append(r)
                    break
    sourceList.sort()
    return sourceList