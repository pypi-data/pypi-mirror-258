# Import the necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns

# helps in text preprocessing
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# helps in model building
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.layers import Embedding
from tensorflow.keras.optimizers import RMSprop

# split data into train and test set
from sklearn.model_selection import train_test_split

# Metrics
from sklearn import metrics                            # sklearn metrics module implements utility functions to measure classification performance
from sklearn.metrics import confusion_matrix           # Computes confusion matrix to evaluate the accuracy of a classification.
from sklearn.metrics import accuracy_score             # Performance measure – Accuracy
from sklearn.metrics import precision_score            # Computes the precision: the ability of the classifier not to label as positive a sample that is negative
from sklearn.metrics import recall_score               # Computes the recall: the ability of the classifier to find all the positive samples
from sklearn.metrics import f1_score                   # Computes the weighted average of the precision and recall
from sklearn.metrics import classification_report

# Import the data set as a pandas DataFrame
df = pd.read_csv('spam.csv', delimiter=',', encoding='latin-1')
df.head(8)

df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
df

# Mapping spam as 1 and Non spam as 0
df['v1'] = df['v1'].map( {'spam': 1, 'ham': 0} )
df.head()

X = df['v2'].values
y = df['v1'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

t = Tokenizer()
t.fit_on_texts(X_train)
encoded_train = t.texts_to_sequences(X_train)
encoded_test = t.texts_to_sequences(X_test)
print(encoded_train[0:4])

max_length=8
padded_train = pad_sequences(encoded_train, maxlen=max_length, padding='post')
padded_test = pad_sequences(encoded_test, maxlen=max_length, padding='post')
padded_train.shape

vocab_size = len(t.word_index) + 1

# define the model
model = Sequential()

# Model is Built with vocabulary size as the input size.
model.add(Embedding(vocab_size, 24, input_length=max_length))
model.add(SimpleRNN(24, return_sequences=False))
model.add(Dense(1, activation='sigmoid'))

# compile the model
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

# fit the model
model.fit(x=padded_train, y=y_train, epochs=50,
         validation_data=(padded_test, y_test), verbose=1)

# prediction
pred = (model.predict(padded_test) > 0.5).astype("int32")
pred

cm=confusion_matrix(y_test, pred,labels=[0, 1])
df_cm = pd.DataFrame(cm, index = [i for i in ["Actual Ham","Actual Spam"]],
                  columns = [i for i in ["Predicted Ham","Predicted Spam"]])
plt.figure(figsize = (7,5))
plt.title('Confusion Matrix')
sns.heatmap(df_cm, annot=True ,fmt='g');

# Classification Report
print('\n Classification Report : \n',metrics.classification_report(y_test, pred))
a = accuracy_score(y_test, pred)
p = precision_score(y_test, pred)
r = recall_score(y_test, pred)
f = f1_score(y_test, pred)

# Performance metrics
print("Accuracy   : ",round(a,2))
print("Precision  : ",round(p,2))
print("Recall     : ",round(r,2))
print("F1 score   : ",round(f,2))

# prediction of a new input

#sms = ["hello! how are you? im visiting mom next week"]
sms = ["You've Won! Winning an unexpected prize sounds great"]
sms_proc = t.texts_to_sequences(sms)
sms_proc = pad_sequences(sms_proc, maxlen=max_length, padding='post')
pred = (model.predict(sms_proc)>0.5).astype("int32").item()
print(pred)
