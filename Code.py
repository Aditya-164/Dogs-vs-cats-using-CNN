

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout

#Data improting & Preprocessing

model_train = keras.utils.image_dataset_from_directory(
    directory = '/content/train',
    labels='inferred',
    label_mode = 'int',
    batch_size=32,
    image_size=(256,256)
)

model_validation = keras.utils.image_dataset_from_directory(
    directory = '/content/test',
    labels='inferred',
    label_mode = 'int',
    batch_size=32,
    image_size=(256,256)
)
# Normalizing
def process(image,label):
    image = tf.cast(image/255. ,tf.float32)
    return image,label

model_train = model_train.map(process)
model_validation = model_validation.map(process)

#Building the Model
model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1,activation='sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history = model.fit(model_train,epochs=10,validation_data=model_validation)

#Plot

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()
plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

#Testing:

import cv2
test_img1=cv2.imread('/content/test/cats/cat.10007.jpg')
plt.imshow(test_img1)

test_img2=cv2.imread('/content/test/dogs/dog.100.jpg')
plt.imshow(test_img2)
test_img1.shape
test_img1=cv2.resize(test_img1,(256,256))
test_input1 = test_img1.reshape((1,256,256,3))
test_img2.shape
test_img2=cv2.resize(test_img2,(256,256))
test_input2 = test_img2.reshape((1,256,256,3))

result=[0]*2
result[0]=model.predict(test_input1)
result[1]=model.predict(test_input2)

for x in range(2):
  if result[x]==0:
    print("Cat")
  else:
    print("Dog")
