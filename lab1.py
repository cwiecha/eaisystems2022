import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from tensorflow.keras.models import Sequential
from tensorflow.keras import regularizers
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, Dropout
from pandas.api.types import is_string_dtype
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import copy

min_values = {}
max_values = {}
score_template = {}
data = 0
data_train = 0
data_valid = 0
x_train = 0
y_train = 0
x_val = 0
y_val = 0
model = 0

print('starting up credit score app')

def normalize(col, df, training):
    global max_values, min_values

    result = df.copy()
    if training == True:
        max_values[col] = df.max()
        min_values[col] = df.min()
    result = (df - min_values[col]) / (max_values[col] - min_values[col])
    return result

def fixup(data, training):
    labels = data.columns
    # lets go through column 2 column
    for col in labels:
        if is_string_dtype(data[col]):
            if col == 'Risk':
                # we want 'Risk' to be a binary variable
                data[col] = pd.factorize(data[col])[0]
                continue
            # the other categorical columns should be one-hot encoded
            data = pd.concat([data, pd.get_dummies(data[col], prefix=col)], axis=1)
            data.drop(col, axis=1, inplace=True)
        else:
            data[col] = normalize(col, data[col], training)
    return data


def setup(training_data):
    global x_train, y_train, x_val, y_val, score_template, data, data_train, data_valid, min_values, max_values
    print('Setup credit score data')

    min_values = {}
    max_values = {}
    score_template = {}
    data = 0
    data_train = 0
    data_valid = 0
    x_train = 0
    y_train = 0
    x_val = 0
    y_val = 0

    data = pd.read_csv(training_data,index_col=0,sep=',')
    data = fixup(data, True)

    # move 'Risk' back to the end of the df
    data = data[[c for c in data if c not in ['Risk']] + ['Risk']]

    for col in data.columns:
        if col != 'Risk':
            score_template[col] = 0

    data_train = data.iloc[:800]
    data_valid = data.iloc[800:]
    x_train = data_train.iloc[:,:-1]
    y_train = data_train.iloc[:,-1]
    x_val = data_valid.iloc[:,:-1]
    y_val = data_valid.iloc[:,-1]

    return "Setup done"

def build():
    global model

    sgd = optimizers.SGD(lr=0.03, decay=0, momentum=0.9, nesterov=False)

    model = Sequential()
    model.add(Dense(units=50, activation='tanh', input_dim=24, kernel_initializer='glorot_normal', bias_initializer='zeros'))#, kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dropout(0.35))
    model.add(Dense(units=1, activation='sigmoid', kernel_initializer='glorot_normal', bias_initializer='zeros'))
    model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

def train():
    model.fit(x_train.values, y_train.values, validation_data=(x_val.values, y_val.values), epochs=30, batch_size=128)

    y_pred = (model.predict( x_val.values ) > 0.5).astype("int32")

    #sns.heatmap(confusion_matrix(y_val,y_pred),annot=True,fmt='.5g')
    print('Confusion matrix on validation data is {}'.format(confusion_matrix(y_val, y_pred)))
    print('Precision Score on validation data is {}'.format(precision_score(y_val, y_pred, average='weighted')))

    return "Train done"

def score(args):
    age = args.get('Age')
    sex = args.get('Sex')
    job = args.get('Job')
    housing = args.get('Housing')
    savings = args.get('Saving acounts')
    checking = args.get('Checking account')
    amount = args.get('Credit amount')
    duration = args.get('Duration')
    purpose = args.get('Purpose')

    x_score_array = [[ int(age), sex, int(job), housing, savings, checking, int(amount), int(duration), purpose  ]]
    x_score_cols = ['Age', 'Sex', 'Job', 'Housing', 'Saving accounts', 'Checking account', 'Credit amount', 'Duration', 'Purpose']
    df = pd.DataFrame( x_score_array, columns = x_score_cols )
    x_score = fixup( df, False )

    for col in x_score.columns:
        score_template[col] = x_score.get(col)[0]
    print( score_template )

    x_score_list = list(score_template.values())
    x_score_args = [ x_score_list ]
    print(x_score_args)

    raw_pred = model.predict( x_score_args )
    y_pred = ( raw_pred > 0.5).astype("int32")

    print( " prediction is ", y_pred )

    return "Score done"
