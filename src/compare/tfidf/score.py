#!usr/bin/env python
# -*- coding:utf-8 _*-
from sklearn import svm
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time

def regression(train_x,train_label,text_x,text_label):
    clf=MultiOutputRegressor(svm.SVR(gamma='scale'))
    clf.fit(train_x,train_label)
    y_pred=pd.DataFrame(clf.predict(text_x))

    catagory=y_pred.shape[1]
    # Person=np.corrcoef(text_label.iloc[:,],y_pred,rowvar=False)
    # print(text_label.iloc[:,0])
    # print(text_label.shape)
    # print("Person: ")
    # print(Person.shape)
    RMSE=np.sqrt(mean_squared_error(text_label, y_pred,multioutput='raw_values'))


    result=[]
    for i in range(0,catagory):
        result.append(RMSE[i])
    return result



score_times=10
r_list=[x/10.0 for x in range(1,10)] #训练集比例


data_name="youtube"
model_name="tfidf"
input_feature="../../../results/features/"+data_name+"_feature_"+model_name+".txt"
# input_feature="../../../results/features/"+data_name+"_feature_"+model_name+".txt"
score_path="../../../results/scores/"+data_name+"_"+model_name+"_"

label_path="../../../data/regular_data/"+data_name+"_labels.txt"


all_results=[]
min_score=[]
max_score=[]
mean_score=[]



embeddings=pd.read_table(input_feature, sep=" ", header=None)

labels=pd.read_table(label_path,sep=" ", header=None)[[1,2,3,4,5]]

feature_size=embeddings.shape[1]
mer=pd.concat([embeddings,labels],axis=1)

for r in r_list:

    results=[] # 同一比例下，10次实验的结果
    for times in range(score_times):
        train,test=train_test_split(mer,test_size=1-r,shuffle=True)
        x_train=train.iloc[:,0:feature_size]
        y_train=train.iloc[:,feature_size:]
        x_test=test.iloc[:,0:feature_size]
        y_test=test.iloc[:,feature_size:]

        result = regression(x_train, y_train, x_test, y_test)
        results.append(result)
        # try:
        #
        #     print("lalaal")
        #     results.append(result)
        # except:
        #     continue
    results=pd.DataFrame(results)
    # print(results)
    # print(results.min())
    min_score.append(results.min())
    # print(min_score)
    # print(results.max())
    max_score.append(results.max())
    # print(max_score)
    # print(results.mean())
    mean_score.append(results.mean())
    # print(min_score)
    # time.sleep(1000)

    all_results.append(results)

min_score=pd.DataFrame(min_score)
max_score=pd.DataFrame(max_score)
mean_score=pd.DataFrame(mean_score)


mean_score.to_excel(score_path+'mean.xlsx',header=False,index=False)
max_score.to_excel(score_path+'max.xlsx',header=False,index=False)
min_score.to_excel(score_path+'min.xlsx',header=False,index=False)




all_results=pd.DataFrame(all_results)
all_results.to_excel(score_path+'all.xlsx',header=False,index=False)

"""mypersonality_doc2vec_max.txt
表示10个不同个训练集比例下，五个pesonality traits的scores
0.9748767900691874 0.8474221941013338 0.7213444979268856 0.820097443385993 0.6590513769846634
0.9362837324923726 0.8349038005869249 0.7414947637474162 0.8525305332844595 0.6312877341408027
0.9193370759351723 0.8743256175497187 0.7197313417995376 0.8075029347285488 0.6210693434073397
0.9306634511544076 0.8294324997613202 0.7032596297448571 0.788605820761687 0.628172370735271
0.9333746591858643 0.8607343245478672 0.7093972322045993 0.8204834232415124 0.6703116094810462
0.9627745656682262 0.8370628889857981 0.6928778301151146 0.7851086493405985 0.6419654423702391
0.9797260030910377 0.8571406143311673 0.7936200232186008 0.7888214534092551 0.6850726036235868
0.9956503537238948 0.8559830980484004 0.7011034491676258 0.7776900242649879 0.6731592130013722
0.940364219537855 0.8835964695423671 0.80397464893336 0.8706385141813485 0.7527204982197345
"""


"""mypersonality_doc2vec_all.txt
不同训练集比例下，每一次实验5个personality traits的scores
"          0         1         2         3         4
0  0.931406  0.804082  0.671787  0.763275  0.605189
1  0.854632  0.793082  0.670051  0.807921  0.599364
2  0.877293  0.789272  0.675945  0.729977  0.584900
3  0.942003  0.847422  0.697889  0.752774  0.617437
4  0.892737  0.804713  0.721344  0.752711  0.637245
5  0.925657  0.798577  0.669377  0.760112  0.612656
6  0.942361  0.801480  0.676711  0.757091  0.601115
7  0.889457  0.768251  0.666398  0.773633  0.594825
8  0.974877  0.786158  0.714793  0.820097  0.659051
9  0.886919  0.820220  0.680555  0.797983  0.599563"
"          0         1         2         3         4
0  0.878633  0.819047  0.696042  0.765206  0.569553
1  0.899176  0.793933  0.662199  0.758825  0.631288
2  0.866735  0.795585  0.676553  0.773940  0.604360
3  0.936284  0.784386  0.694294  0.772120  0.589699
4  0.869547  0.819261  0.675727  0.757465  0.608754
5  0.859661  0.811948  0.688895  0.729042  0.624338
6  0.879732  0.772930  0.675251  0.852531  0.601341
7  0.880630  0.824151  0.664144  0.740013  0.604793
8  0.858923  0.800115  0.678004  0.761362  0.601964
9  0.836598  0.834904  0.741495  0.741489  0.576388"
"          0         1         2         3         4
0  0.866013  0.771990  0.681921  0.753730  0.570191
1  0.889632  0.765918  0.684542  0.763334  0.561662
2  0.900746  0.827987  0.698591  0.807503  0.615817
3  0.881213  0.813129  0.703897  0.747874  0.599638
4  0.879510  0.749901  0.719731  0.721766  0.621069
5  0.919337  0.808912  0.715122  0.722874  0.589688
6  0.847035  0.874326  0.681029  0.737320  0.582682
7  0.890098  0.812207  0.680711  0.700453  0.610907
8  0.895165  0.785489  0.682732  0.763483  0.603036
9  0.863809  0.772638  0.672035  0.765927  0.586998"
"          0         1         2         3         4
0  0.879313  0.829432  0.682081  0.746316  0.555005
1  0.867703  0.756216  0.677393  0.770795  0.614303
2  0.832845  0.771914  0.643090  0.715333  0.571192
3  0.930663  0.766920  0.644476  0.788606  0.616930
4  0.859900  0.805611  0.647460  0.693338  0.628172
5  0.898465  0.778678  0.682112  0.724757  0.585868
6  0.904120  0.828610  0.670937  0.722512  0.599720
7  0.886802  0.799705  0.703260  0.707429  0.568117
8  0.909649  0.775876  0.642889  0.720118  0.599591
9  0.890637  0.768160  0.686266  0.747747  0.627467"
"          0         1         2         3         4
0  0.868140  0.744932  0.677030  0.743806  0.625210
1  0.863308  0.768442  0.670073  0.737086  0.614957
2  0.856180  0.814586  0.689430  0.738313  0.568978
3  0.902098  0.769580  0.599730  0.706403  0.575085
4  0.884210  0.826887  0.630197  0.687626  0.594173
5  0.867737  0.749635  0.645759  0.820483  0.585450
6  0.834743  0.764244  0.624675  0.798848  0.644962
7  0.893453  0.756403  0.640325  0.705986  0.577960
8  0.883673  0.761815  0.683431  0.759860  0.611161
9  0.933375  0.860734  0.709397  0.812420  0.670312"
"          0         1         2         3         4
0  0.820451  0.796773  0.641194  0.785109  0.641965
1  0.856755  0.799974  0.672051  0.752260  0.605913
2  0.866311  0.751925  0.652132  0.716328  0.582458
3  0.886100  0.753978  0.691743  0.718190  0.575482
4  0.871613  0.837063  0.635524  0.709142  0.627704
5  0.962775  0.780274  0.692878  0.755041  0.619830
6  0.899036  0.685080  0.626571  0.689495  0.603571
7  0.891898  0.797063  0.612811  0.728805  0.609763
8  0.870476  0.776227  0.682589  0.657239  0.546142
9  0.920432  0.704157  0.641723  0.740668  0.574057"
"          0         1         2         3         4
0  0.979726  0.763660  0.638771  0.660108  0.570625
1  0.844103  0.800285  0.728946  0.781886  0.530155
2  0.868622  0.848822  0.627797  0.788821  0.563260
3  0.878089  0.827551  0.647264  0.748553  0.563977
4  0.875314  0.711607  0.645749  0.702252  0.649757
5  0.894378  0.750905  0.793620  0.643650  0.532723
6  0.900347  0.857141  0.673977  0.704891  0.619206
7  0.891524  0.778057  0.641766  0.754572  0.685073
8  0.955542  0.766264  0.601309  0.768088  0.645685
9  0.836480  0.766853  0.700544  0.727764  0.629220"
"          0         1         2         3         4
0  0.893488  0.734863  0.661646  0.725502  0.651288
1  0.786891  0.669749  0.683545  0.720537  0.636530
2  0.896955  0.855983  0.701103  0.746030  0.536833
3  0.672052  0.771358  0.678002  0.754192  0.538930
4  0.891302  0.817470  0.690337  0.777690  0.628906
5  0.681639  0.742890  0.656463  0.668259  0.531636
6  0.834865  0.789427  0.668341  0.760980  0.519269
7  0.895753  0.630811  0.623116  0.687056  0.673159
8  0.995650  0.832404  0.629404  0.729935  0.535076
9  0.791011  0.730740  0.651727  0.687939  0.605345"
"          0         1         2         3         4
0  0.893978  0.637133  0.757938  0.840447  0.559648
1  0.880810  0.664908  0.604345  0.643715  0.498412
2  0.893508  0.883596  0.803975  0.775278  0.565307
3  0.940364  0.765255  0.618190  0.847724  0.630371
4  0.808019  0.761635  0.713996  0.737238  0.752720
5  0.813440  0.768077  0.575646  0.870639  0.667357
6  0.783693  0.786015  0.772378  0.783262  0.512101
7  0.846126  0.689925  0.641554  0.626210  0.629467
8  0.633524  0.856455  0.656084  0.658775  0.495559
9  0.783447  0.779404  0.703343  0.753171  0.557652"

"""
