# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 19:05:44 2024

@author: Hanhe Lin
"""

import pandas as pd
import numpy as np

z_ratings_all = []
ratings_all = []


tb = pd.read_csv("pilot_study.csv")

for i in range(1,12):
    ratings = tb.iloc[:,i].to_numpy()
    ratings_all.append(ratings)
    z_ratings = (ratings - np.mean(ratings))/np.std(ratings)
    #z_ratings = (z_ratings - np.min(z_ratings))/(np.max(z_ratings)-np.min(z_ratings)) 
    z_ratings_all.append(z_ratings)

    
print(z_ratings_all)
ratings_all = np.array(ratings_all)
z_ratings_all = np.array(z_ratings_all)

mos = np.mean(ratings_all,axis=0)

print(mos)

z_mos = np.mean(z_ratings_all,axis=0)

#print(ratings_all.shape)
print(z_ratings_all)
print(z_mos)

import numpy as np
from scipy import stats
res_list = []

for i in range(11):
    res,_ = stats.pearsonr(ratings_all[i,:], mos) 
    res_list.append(res)

print(np.array(res_list))