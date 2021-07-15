import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


mill = pd.read_feather("feather.feather")

scenario = mill.columns[1:7]

measure = mill.columns.symmetric_difference(scenario)

X = mill.columns.symmetric_difference(["VB", "RUL", "case"])

f = "VB ~ " + ' + '.join([col for col in X])

result = pd.DataFrame(columns=['iteration', 'method', 'rmse', 'rrse'])
performance = pd.DataFrame(columns=['method', 'meanRMSE', 'meanRRSE'])
error = pd.DataFrame(columns=['iteration', 'case', 'run', 'Taylor', 'NN'])

# take out Case 1
# esclusione Case 1 (mostra VB non monotono)
mill = mill[(mill.case != 1)]

# suddivisione Case per materiale (m1=CastIron,m2=Steel) con relativi DOC e feed
# case<-unique(dplyr::select(mill,case,DOC,feed,material1))
# case_m1<-dplyr::filter(case, material1==1)
# case_m2<-dplyr::filter(case, material1==0)
# n_case_train_for_m<-6

case = mill[['case', 'DOC', 'feed', 'material1']]
case_m1 = case[case['material1'] == 1]
case_m2 = case[case['material1'] == 0]
n_case_train_for_m = 6

#for (k in 1:10) {
# inizializzazione variabili con i Case per il train di ogni materiale
# train_m1<-dplyr::filter(mill,case==0)
# train_m2<-dplyr::filter(mill,case==0)
# train_m1<-rbind(train_m1,dplyr::filter(mill,case==sample(case_m1$case,1)))


for k in range(1, 10):
    train_m1 = mill[mill['case'] == 0]
    train_m2 = mill[mill['case'] == 0]
   ## train_m1 =

jjj


#x = data.loc[:, ['run'], ['DOC']]
#y = data.loc[:, ['VB']].values


#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)



