#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib as mpl

# 自定义colormap
def colormap():
    return mpl.colors.LinearSegmentedColormap.from_list('cmap', ['#FFFFFF', '#98F5FF', '#00FF00', '#FFFF00','#FF0000', '#68228B'], 256)



from sklearn.metrics import pairwise_distances



data_name="youtube"
model_name="mairesse" # IFIDF
label_path="../../../data/regular_data/"+data_name+"_labels.txt"
graph_path="../../../results/graphs/"+data_name+"_"
figure_to_path="../../../results/figures/"+data_name+"_"+model_name+"_"






traits=pd.read_table(label_path,header=None,sep=" ")
# print(traits[[1,2,3,4,5]])

trait_sims=1-pairwise_distances(traits[[1,2,3,4,5]],metric='cosine')

sims=np.load(graph_path+"sims_"+model_name+".npy")





x=sims  #df_all["text_sim_tfidf_stopword_removed"]
y=trait_sims # df_all["traits_sim_cos"]

# x=np.reshape(x,(-1,x.shape[0]*x.shape[1]))[0]
# y=np.reshape(y,(-1,y.shape[0]*y.shape[1]))[0]
# print(x)
# ab=np.array([x,y])
# print("x: ")
# print(x)
# print("y: ")
# print(y)
# print("ab: ")
# print(ab)
# print("correlation: ")
# print(np.corrcoef(ab))
#
# time.sleep(1000)
#
#
#
#
#
#
#
#
#
#





z=abs(x-y)
xmin = x.min()
xmax = x.max()
ymin = y.min()
ymax = y.max()
fig, ax = plt.subplots(ncols=1)#, figsize=(7, 4))
hb = ax.hexbin(x, y,gridsize=(40,20), bins='log', cmap=colormap())



ax.axis([xmin, xmax, ymin, ymax])


plt.xlabel('texts similarity')
plt.ylabel('traits similarity')

ax.set_title("Text similarity vs Traits similarity Density Map\n")
cb = fig.colorbar(hb, ax=ax)
cb.set_label('log(N)')
plt.savefig(figure_to_path+"TextSimVSTraitSimDensMap_mairesse.jpg")
plt.show()

