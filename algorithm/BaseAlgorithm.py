# coding=UTF-8
__author__ = 'study_sun'

import random

def geneRandomDistinctList(totalCount, minValue, maxValue):
    return geneRandomDistinctListPrefer([], totalCount, minValue, maxValue)

def geneRandomDistinctListPrefer(prefer, totalCount, minValue, maxValue):
    return geneRandomDistinctListPreferAndExclude(prefer, [], totalCount, minValue, maxValue)

def geneRandomDistinctListPreferAndExclude(prefer, exclude, totalCount, minValue, maxValue):
    sourceList = list(prefer)
    while (len(sourceList) < totalCount):
        while (1):
            r = random.choice(range(minValue,maxValue+1))
            if not (r in sourceList):
                if not (r in exclude):
                    sourceList.append(r)
                    break
    sourceList.sort()
    return sourceList
