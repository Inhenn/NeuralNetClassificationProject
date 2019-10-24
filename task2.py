# -*- coding: utf-8 -*-
"""Task2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WeDKXmmqtv89a5LwGhSU9NiJ4HfrRfF5
"""

import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation,merge,add, Conv2D, Flatten,MaxPooling2D
from keras.wrappers.scikit_learn import KerasClassifier, KerasRegressor
from sklearn.model_selection import GridSearchCV
from sklearn import datasets
from sklearn.model_selection import StratifiedShuffleSplit
from keras import regularizers
from keras.utils import to_categorical
import numpy as np
from keras.layers import Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.datasets import mnist
import cv2
import keras
from keras.layers.normalization import BatchNormalization
from keras.layers import Input, Dense
from keras.models import Model
import matplotlib.pyplot as plt 
import os
import imageio
from keras.preprocessing.image import ImageDataGenerator

import pickle
from google.colab import drive
drive.mount('/content/drive')

"""# Task2

load data
"""

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(60000, 784)

X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
num_classes = 10
# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

"""baseline model"""

model1 = Sequential([
    Dense(512, input_shape=(784,)),
    Activation('relu'),
    Dense(32, input_shape=(784,)),
    Activation('relu'),
    Dense(num_classes),
    Activation('softmax')])
model1.compile("adam", "categorical_crossentropy", metrics=['accuracy'])

history_callback = model1.fit(X_train, y_train, batch_size=128,
                             epochs=20, verbose=1, validation_split=1/6)
pd.DataFrame(history_callback.history).plot()
score =model1.evaluate(X_test,y_test)
print('evaluation score on the testset',score[1])

"""model with dropout has an accuracy of 0.982 in the testing set, which is very similar to the model without dropout."""

model2 = Sequential([
    Dense(512, input_shape=(784,),),
    Activation('relu'),
    Dropout(rate = 0.2),
    Dense(32, input_shape=(784,)),
    Activation('relu'),
    Dropout(rate = 0.2),
    Dense(num_classes),
    Activation('softmax')])
model2.compile("adam", "categorical_crossentropy", metrics=['accuracy'])

history_callback = model2.fit(X_train, y_train, batch_size=128,
                             epochs=20, verbose=1, validation_split=1/6)
pd.DataFrame(history_callback.history).plot()
score = model2.evaluate(X_test,y_test)
print('evaluation score on the testset',score[1])

"""Model with batch normalization gets a worse accuracy on the testing set, but the result is still close to the 2 models above"""

inputs = Input(shape=(784,))
x1 = Dense(64, activation='relu')(inputs)
x = BatchNormalization()(x1)
x = Dense(64, activation='relu')(x)
x = BatchNormalization()(x)
skip2 = add([x,x1])
predictions = Dense(10, activation='softmax')(skip2)

model3 = Model(inputs=inputs, outputs=predictions)
model3.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
history_callback = model3.fit(X_train, y_train, batch_size=128,
                             epochs=20, verbose=1, validation_split=1/6)
pd.DataFrame(history_callback.history).plot()
score = model3.evaluate(X_test,y_test)
print('evaluation score on the testset',score[1])

"""# Task3 preprocessing"""

# !unzip "drive/My Drive/Colab Notebooks/Applied Machine Learning/task3.zip" -d "drive/My Drive/Colab Notebooks/Applied Machine Learning/task3files"

os.getcwd()

os.chdir('/content/drive/My Drive/Colab Notebooks/Applied Machine Learning/task3files')

folder_ls = os.listdir()
folder_ls0 = [x+'/0' for x in folder_ls if x[0].isdigit()]
folder_ls1 = [x+'/1' for x in folder_ls if x[0].isdigit()]
folder_ls = folder_ls0 + folder_ls1

folder_ls

file0_ls = []
file1_ls = []
count = 0
for f in folder_ls:
  
  try:
    for img in os.listdir(path=f):
          print(count)
          count += 1
          filename = f+'/'+img

          if int(f[-1])==0:
              file0_ls.append(filename)
          elif int(f[-1])==1:
              file1_ls.append(filename)
  except:
      print('e')
      pass

image_ls = []
class_ls = []
image0_ls = []
image1_ls = []

"""## Since this dataset is very large, it is slow if we load all the png files and sample them into training. Here, I only collect the file name/path of each picture and I sample from this collection. After sampling the file names, I then load those sampled picture files into numpy array. For this task, I only sample 10000 pictures for each class. Although this is a small sample, it is enough for my models to get a good result."""

print('class 0 image number loaded is ',len(file0_ls))
print('class 1 image number loaded is ',len(file1_ls))

with open('img0_fnm.pkl','wb') as f:
     pickle.dump(np.array(file0_ls), f)
with open('img1_fnm.pkl','wb') as f:
     pickle.dump(np.array(file1_ls), f)

"""The total image numbers are too large and the number of class0 and class1 images are not equal. So, we only random sample 10000 images for each class for our training and testing purpose. In this case, our training and testing dataset is also balanced."""

file0_sample = np.random.choice(file0_ls, 10000,replace = False)
file1_sample = np.random.choice(file1_ls, 10000,replace = False)

img0_ls = [cv2.imread(f) for f in file0_sample]
img1_ls = [cv2.imread(f) for f in file1_sample]

with open('imgsample0.pkl','wb') as f:
     pickle.dump(np.array(img0_ls), f)
with open('imgsample1.pkl','wb') as f:
     pickle.dump(np.array(img1_ls), f)

img0_ls = pickle.load( open( "imgsample0.pkl", "rb" ) )
img1_ls = pickle.load( open( "imgsample1.pkl", "rb" ) )

"""make sure all images in this sample has size (50,50,3) otherwise we reshape it into (50,50,3)

Here is one reshape example.
"""

imgreshape_ls = pickle.load( open( "imgsample0.pkl", "rb" ) )
original_img = [s  for s in imgreshape_ls if s.shape!=(50, 50, 3)][2]
print('original image shape',original_img.shape)
plt.imshow(original_img)
plt.show()
reshaped_img = cv2.resize(original_img, (50,50), interpolation = cv2.INTER_CUBIC)
print('reshaped image shape',reshaped_img.shape)
plt.imshow(reshaped_img)
plt.show()

img0_ls = [cv2.resize(s, (50,50), interpolation = cv2.INTER_CUBIC) if s.shape!=(50, 50, 3) else s for s in img0_ls ]
img1_ls = [cv2.resize(s, (50,50), interpolation = cv2.INTER_CUBIC) if s.shape!=(50, 50, 3) else s for s in img1_ls ]

"""Build a tiny sample of data to test the neural net. Contains 10 images 5 of each class. Then we do train test split. Since all our samples are randomly drawed from our image pool, we can just take first 80% data as training and last 20% data as testing."""

input_shape = (50,50,3)
shuffle_idx = np.random.permutation(16000)# mix the image class

tiny_input = np.array(img0_ls[:5]+ img1_ls[:5])
tiny_target =np.array([0,0,0,0,0,1,1,1,1,1])
X_train = np.array(img0_ls[:8000]+ img1_ls[:8000])[shuffle_idx]
X_test = np.array(img0_ls[8000:]+ img1_ls[8000:])
y_test =to_categorical(np.array([0 for i in range(2000)]+[1 for i in range(2000)]))
y_train =to_categorical(np.array([0 for i in range(8000)]+[1 for i in range(8000)])[shuffle_idx])

"""# Task 3.1
## This is the first cnn model for the baseline, it has 2 conv2D layers and 2 Dense layers. It uses BatchNormalization and works really well. It gets an accuracy of 71% in the testing set
"""

cnn = Sequential()
cnn.add(Conv2D(64, kernel_size=(5, 5),
               activation='relu',
               input_shape=input_shape))
cnn.add(BatchNormalization())
cnn.add(MaxPooling2D(pool_size=(2, 2)))
cnn.add(Conv2D(32, (3, 3), activation='relu'))
cnn.add(BatchNormalization())

cnn.add(MaxPooling2D(pool_size=(2, 2)))
cnn.add(Flatten())
cnn.add(Dense(64, activation='relu'))
cnn.add(BatchNormalization())

cnn.add(Dense(2, activation='softmax'))
cnn.compile("adam", "categorical_crossentropy", metrics=['accuracy'])

history_callback = cnn.fit(X_train,y_train,epochs=15,validation_split=.1)
pd.DataFrame(history_callback.history).plot()
score = cnn.evaluate(X_test,y_test)
print('evaluation score on the test set', score[1])

"""# Task 3.2

## Here we use ImageDataGenerator to random shift, zoom, rotate and flip our graph to argument the data. As we can see from the result, we get an accuracy of 79% in testing dataset, which is higher than the accuracy in the model not using any argument data in Task 3.1
"""

datagen = ImageDataGenerator(width_shift_range=0.1, height_shift_range=0.1,zoom_range=0.1,rotation_range=45,horizontal_flip=True,vertical_flip=True)
history_callback = cnn.fit_generator(datagen.flow(X_train, y_train),
                    steps_per_epoch=len(X_train)/32, epochs=15)
pd.DataFrame(history_callback.history).plot()
score = cnn.evaluate(X_test,y_test)
print('evaluation score on the test set', score[1])

"""## This is a deep residual network including 6 layers of cnn. We only train it 10 epoches so that we can see the difference between using residule network v.s. not using residule network. As we can see, the accuracy is around 80% which is slightly higher than the shallow network in task 3.1"""

inputs = Input(input_shape)
layer_num = 2



conv1_1 = Conv2D(32, (3, 3), activation='relu',
                     padding='same')(inputs)
conv1_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv1_1)

maxpool1 = MaxPooling2D(pool_size=(2, 2))(conv1_2)
BN1 = BatchNormalization()(maxpool1)

conv2_1 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(BN1)
conv2_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv2_1)
skip2 = add([maxpool1, conv2_2])

maxpool2 = MaxPooling2D(pool_size=(2, 2))(skip2)

BN2 = BatchNormalization()(maxpool2)
    


conv3_1 = Conv2D(32, (3, 3), activation='relu',
                     padding='same')(BN2)
conv3_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv2_1)

maxpool3 = MaxPooling2D(pool_size=(2, 2))(conv3_2)
BN3 = BatchNormalization()(maxpool3)

conv4_1 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(BN3)
conv4_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv4_1)
skip4 = add([maxpool3, conv4_2])

maxpool4 = MaxPooling2D(pool_size=(2, 2))(skip4)

BN4 = BatchNormalization()(maxpool4)
    
conv5_1 = Conv2D(32, (3, 3), activation='relu',
                     padding='same')(BN4)
conv5_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv5_1)

maxpool5 = MaxPooling2D(pool_size=(2, 2))(conv5_2)
BN5 = BatchNormalization()(maxpool5)

conv6_1 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(BN5)
conv6_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv6_1)
skip6 = add([maxpool5, conv6_2])

maxpool6 = MaxPooling2D(pool_size=(2, 2))(skip6)

BN6 = BatchNormalization()(maxpool6)
    


flat = Flatten()(BN6)
dense = Dense(64, activation='relu')(flat)
predictions = Dense(2, activation='softmax')(dense)
model = Model(inputs=inputs, outputs=predictions)
model.compile("adam", "categorical_crossentropy", metrics=['accuracy'])

history_callback = model.fit(X_train,y_train,epochs=10,validation_split=.1)
pd.DataFrame(history_callback.history).plot()
score = model.evaluate(X_test,y_test)
print('evaluation score on the test set', score[1])

"""## This is the same deep model from above except it is removes the residual connections. As expected, it gets worse result compared to the model using residual, which indicates this kind of deep neural network would not be able to learn if we don't use residual connections"""

inputs = Input(input_shape)
layer_num = 2



conv1_1 = Conv2D(32, (3, 3), activation='relu',
                     padding='same')(inputs)
conv1_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv1_1)

maxpool1 = MaxPooling2D(pool_size=(2, 2))(conv1_2)
BN1 = BatchNormalization()(maxpool1)

conv2_1 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(BN1)
conv2_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv2_1)

maxpool2 = MaxPooling2D(pool_size=(2, 2))(conv2_2)

BN2 = BatchNormalization()(maxpool2)
    


conv3_1 = Conv2D(32, (3, 3), activation='relu',
                     padding='same')(BN2)
conv3_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv2_1)

maxpool3 = MaxPooling2D(pool_size=(2, 2))(conv3_2)
BN3 = BatchNormalization()(maxpool3)

conv4_1 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(BN3)
conv4_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv4_1)

maxpool4 = MaxPooling2D(pool_size=(2, 2))(conv4_2)

BN4 = BatchNormalization()(maxpool4)
    





conv5_1 = Conv2D(32, (3, 3), activation='relu',
                     padding='same')(BN4)
conv5_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv5_1)

maxpool5 = MaxPooling2D(pool_size=(2, 2))(conv5_2)
BN5 = BatchNormalization()(maxpool5)

conv6_1 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(BN5)
conv6_2 = Conv2D(32, (3, 3), activation='relu',
                 padding='same')(conv6_1)

maxpool6 = MaxPooling2D(pool_size=(2, 2))(conv6_2)

BN6 = BatchNormalization()(maxpool6)
    


flat = Flatten()(BN6)
dense = Dense(64, activation='relu')(flat)
predictions = Dense(2, activation='softmax')(dense)
model = Model(inputs=inputs, outputs=predictions)
model.compile("adam", "categorical_crossentropy", metrics=['accuracy'])

history_callback = model.fit(X_train,y_train,epochs=10,validation_split=.1)
pd.DataFrame(history_callback.history).plot()
score = model.evaluate(X_test,y_test)
print('evaluation score on the test set', score[1])