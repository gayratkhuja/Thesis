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

case = mill[['case', 'DOC', 'feed', 'material1']].drop_duplicates()


case_m1 = case[case['material1'] == 1]
case_m2 = case[case['material1'] == 0]
n_case_train_for_m = 6


#Cross Validation con 10 iterazioni (valore empirico da letteratura)
#for (k in 1:10) {
# inizializzazione variabili con i Case per il train di ogni materiale
# train_m1<-dplyr::filter(mill,case==0)
# train_m2<-dplyr::filter(mill,case==0)
# train_m1<-rbind(train_m1,dplyr::filter(mill,case==sample(case_m1$case,1)))
# train_m2 < -rbind(train_m2, dplyr::filter(mill, case == sample(case_m2$case, 1)))


for k in range(1, 10):
    train_m1 = mill[mill['case'] == 0]
    train_m2 = mill[mill['case'] == 0]

    train_m1 = pd.concat([train_m1, mill[mill["case"] == case_m1["case"].sample(1).iloc[0]]])
    train_m2 = pd.concat([train_m2, mill[mill["case"] == case_m1["case"].sample(1).iloc[0]]])

    for j in range(2, 4):
        c = case_m1["case"].sample(1).iloc[0]

        parametri = case_m1[case_m1["case"] == c][["DOC", "feed"]]

        while(len(pd.merge(train_m1[["DOC", "feed"]], parametri, how='inner').index)!=0):
            c = case_m1["case"].sample(1).iloc[0]
            parametri = case_m1[case_m1["case"] == c][["DOC", "feed"]]
        train_m1 = pd.concat([train_m1,mill[mill["case"] == c]])
    if(n_case_train_for_m-4>0):
        for j in range(1,n_case_train_for_m-4):

            while(1):
                print('adasd')
                c = case_m1["case"].sample(1).iloc[0]
                print(c)
                if not (train_m1["case"].isin([c]).any()):
                    break

        train_m1 = pd.concat([train_m1, mill[mill["case"] == c]])


print(train_m1)
train_m1.to_excel("output.xlsx")
#scelta 3 Case in modo casuale (in aggiunta al Case selezionato con l'inizializzazione)
  #tot 4 Case per materiale per il train (su 7 complessivi) e i restanti 3 per il test
  #con la condizione di non avere Case con coppia (DOC,feed) uguale nel train set
#  for (j in 2:4) {
 #   repeat{
 #   c<-sample(case_m1$case,1)
 #   parametri<-select(dplyr::filter(case_m1,case==c), DOC,feed)
  #  if(nrow(match_df(select(train_m1,DOC,feed),parametri))==0){
  #    break}
 #   }
 #   train_m1<-rbind(train_m1,dplyr::filter(mill,case==c))
#  }
#if (n_case_train_for_m - 4 > 0) {for (j in 1:(n_case_train_for_m - 4)){
#    repeat
#{
#   c < -sample(case_m1$case, 1)
#if (!c % in % train_m1$case){
#break}}
#train_m1 < -rbind(train_m1, dplyr::filter(mill, case == c))}}

#x = data.loc[:, ['run'], ['DOC']]
#y = data.loc[:, ['VB']].values


#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)



