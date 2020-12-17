"""
Code will create csv files containing the results for the parameter tuning
"""


import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional, SimpleRNN, TimeDistributed
import pandas as pd
import numpy as np
import re
import gensim
import keras.optimizers as ko
import keras.losses as kl
from keras import optimizers
from sklearn.utils import class_weight
# import talos as ta
# from talos import Evaluate
import random
from tqdm import tqdm as tqdm
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_recall_fscore_support


# Write the file names for the vector embeddings
X = np.load('X_300.npy')
y = np.load('y_300.npy')
dim, num_feat = X.shape[1], X.shape[2]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

def get_sampleWeights(class_weights):
    sample_weights=np.random.rand(X_train.shape[0], X_train.shape[1])
    for i in range(X_train.shape[0]):
        for j in range(X_train.shape[1]):
            sample_weights[i][j]=class_weights[np.argmax(y_train[i][j])]
    return sample_weights
    
def rnn_model(params):

    model = Sequential()
    model.add(Bidirectional(SimpleRNN(params['layers'][0], return_sequences=True,activation='relu'), 
                                   input_shape=(dim, num_feat)))
    model.add(Bidirectional(SimpleRNN(params['layers'][1],return_sequences=True)))
    
    if len(params['layers']) > 2:
        model.add(Bidirectional(SimpleRNN(params['layers'][2],return_sequences=True)))
    if len(params['layers'])>3:
        model.add(Bidirectional(SimpleRNN(params['layers'][3],return_sequences=True)))
    
    model.add(Dense(3,activation=params['last_activation']))
    
    if params['optimizer'] == ko.SGD:
        optimizer = params['optimizer'](lr=params['lr'],momentum=params['momentum'])
    else:
        optimizer = params['optimizer'](lr=params['lr'])
        
    model.compile(loss = params['loss'], optimizer=optimizer,sample_weight_mode="temporal")
    return model


def lstm_model(params):

    model1 = Sequential()
    model1.add(Bidirectional(LSTM(params['layers'][0], return_sequences=True,activation='relu'), 
                                   input_shape=(dim, num_feat)))
    model1.add(Bidirectional(LSTM(params['layers'][1],return_sequences=True)))
    if len(params['layers']) > 2:
        model1.add(Bidirectional(LSTM(params['layers'][2],return_sequences=True)))
    if len(params['layers']) > 3:
        model1.add(Dense(3,activation='softmax'))
    
    if params['optimizer'] == ko.SGD:
        optimizer = params['optimizer'](lr=params['lr'],momentum=params['momentum'])
    else:
        optimizer = params['optimizer'](lr=params['lr'])
        
    
    model1.compile(loss = params['loss'], optimizer=optimizer,sample_weight_mode="temporal")
    return model1


def return_report(model):
    y_flat = list(np.argmax(y_test,2).flatten('F'))

    # Comment out the class weights if not working in the particular version
    # class_weights = class_weight.compute_class_weight('balanced', np.unique(y_flat),y_flat)
    class_weights = [1,20,20]

    # Setting the default epochs as 50, if taking less time increase the epochs
    epochs = 50

    # Set verbose 
    model.fit(X_train,y_train,epochs=epochs,sample_weight=get_sampleWeights(class_weights),verbose=1)
    out = model.predict(X_test)
    pred = np.argmax(out,2)
    report = classification_report(np.argmax(y_test,2).flatten('F'),pred.flatten('F'),output_dict=True)
    df = pd.DataFrame(report).transpose()
    return report


# Defining the default parameter set

params_set = [ {'lr' : [0.03,0.04,0.05,0.07,0.08,0.09,0.1],
    'momentum' : [0.6,0.7,0.8,0.9,1],
    'layers' : [60,50,45,40,35,30,25,20],
    'optimizer': ko.SGD,
    'loss':['categorical_crossentropy'],
    'last_activation': 'softmax'
}, {'lr' : [1e-5,3*1e-5,4*1e-5,5*1e-5,6*1e-5,7*1e-5,5*1e-6],
    'momentum' : [0.6],
    'layers' : [60,50,45,40,35,30,25,20],
    'optimizer': ko.Adam,
    'loss':['categorical_crossentropy'],
    'last_activation': 'softmax'
}]


def parameter_tuning(model):

    # Initialise the csv file
    with open(model.__name__+'_results.csv','w+') as f:
        writer = csv.writer(f)
        writer.writerow(['params','p1','r1','f1','p2','r2','f2'])
    results = {}

    # Max Iterations = 10000
    max_iter = 10000
    for i in tqdm(range(max_iter)):
        
        try:
            num = random.randint(0,1)
            num_layers = [2,3,4]
            
            params = {}
            random.shuffle(params_set[num]['lr'])
            random.shuffle(params_set[num]['momentum'])
            random.shuffle(params_set[num]['layers'])
            random.shuffle(num_layers)
            
            params['lr'] = params_set[num]['lr'][0]
            params['momentum'] = params_set[num]['momentum'][0]
            params['layers'] = params_set[num]['layers'][0:num_layers[0]]
            params['optimizer'] = params_set[num]['optimizer']
            params['last_activation'] = params_set[num]['last_activation']
            params['loss'] = params_set[num]['loss'][0]
            
            # If already checked skip
            if str(params) in results:
                continue
            
            report = return_report(rnn_model(params))
            results[str(params)] = 1
            
            row = {}
            row['params'] = str([str(params)])  
            for key in ['1','2']:
                for metric in report[key]:
                    if 'support' in metric:
                        continue
                    row[metric+"_"+key] = report[key][metric]
            # print(row)

            # Write to csv file
            with open(model.__name__+'_results.csv','a+') as f:
                writer = csv.writer(f)
                writer.writerow(list(row.values()))
        except:
            continue
        
    return

parameter_tuning(rnn_model)

# Uncomment if need to run
# parameter_tuning(lstm_model)