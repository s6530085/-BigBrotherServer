# coding=UTF-8
__author__ = 'study_sun'

import random

def geneRandomDistinctList(totalCount, minValue, maxValue):
    return geneRandomDistinctListExclude([], totalCount, minValue, maxValue)

def geneRandomDistinctListExclude(exclude, totalCount, minValue, maxValue):
    sourceList = list(exclude)
    while (len(sourceList) < totalCount):
        while (1):
            r = random.choice(range(minValue,maxValue))
            if not (r in sourceList):
                sourceList.append(r)
                break
    sourceList.sort()
    return sourceList

