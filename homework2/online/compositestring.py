#!/usr/bin/python3
import fileinput
import copy

words = ['June', 
        'june', 
        'JanWerner',
        'janwerner',
        'Jan', 
        'jan', 
        'Werner', 
        'werner',
        'jjwerner', 
        'Male',
        'male',
        'ResearchEngineer',
        'researchengineer',
        'Research', 
        'research', 
        'Engineer', 
        'engineer', 
        'ChapelHill',
        'chapelhill',
        'Chapel',
        'chapel',
        'Hill',
        'hill',
        'UniversityofNorthCarolinaatChapelHill',
        'UniversityOfNorthCarolinaAtChapelHill',
        'universityofnorthcarolinaatchapelhill',
        'UniversityofNorthCarolinaChapelHill',
        'UniversityOfNorthCarolinaChapelHill',
        'universityofnorthcarolinachapelhill',
        'UniversityNorthCarolinaChapelHill', 
        'universitynorthcarolinachapelhill',
        'UniversityofNorthCarolina',
        'universityofnorthcarolina',
        'UniversityNorthCarolina',
        'universitynorthcarolina',
        'NorthCarolina',
        'northcarolina',
        'University',
        'university'
        'North',
        'north',
        'Carolina',
        'carolina',
        'UNCCH', 
        'uncch', 
        'UNC', 
        'unc', 
        'VanderbiltUniversity', 
        'vanderbiltuniversity', 
        'Vanderbilt',
        'vanderbilt',
        'VU', 
        'vu', 
        'NicolausCopernicusUniversity', 
        'nicolauscopernicusuniversity', 
        'NicolausCopernicus',
        'nicolauscopernicus', 
        'Nicolaus', 
        'nicolaus', 
        'Copernicus',
        'copernicus',
        'NCU', 
        'ncu']
endings = ['6', '06', '617', '0617', '17']
newwords = []

idx1 = 0
for word in words:
    for end in endings:
        print(''.join([word, end]))
        for word2 in words:
            print(''.join([word, word2, end]))
            # for word3 in words:
            #     print(''.join([word, word2, word3, end]))



