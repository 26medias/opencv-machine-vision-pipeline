import numpy as np
from tensorflow.keras.layers import Layer, InputSpec
import keras.utils.conv_utils as conv_utils
import tensorflow as tf
import tensorflow.keras.backend as K

from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import gradio as gr
from huggingface_hub import from_pretrained_keras

from PIL import Image
import cv2

def depth_norm(x, maxDepth):
    return maxDepth / x


def predict(model, images, minDepth=10, maxDepth=1000, batch_size=2):
    # Support multiple RGBs, one RGB image, even grayscale
    if len(images.shape) < 3: images = np.stack((images, images, images), axis=2)
    if len(images.shape) < 4: images = images.reshape((1, images.shape[0], images.shape[1], images.shape[2]))
    # Compute predictions
    predictions = model.predict(images, batch_size=batch_size)
    # Put in expected range
    return np.clip(depth_norm(predictions, maxDepth=maxDepth), minDepth, maxDepth) / maxDepth


def load_images(image_files):
    loaded_images = []
    for file in image_files:
        x = np.clip(file.reshape(480, 640, 3) / 255, 0, 1)
        loaded_images.append(x)
    return np.stack(loaded_images, axis=0)



def normalize_data_format(value):
    if value is None:
        value = K.image_data_format()
    data_format = value.lower()
    if data_format not in {'channels_first', 'channels_last'}:
        raise ValueError('The `data_format` argument must be one of '
                         '"channels_first", "channels_last". Received: ' +
                         str(value))
    return data_format



class BilinearUpSampling2D(Layer):
    def __init__(self, size=(2, 2), data_format=None, **kwargs):
        super(BilinearUpSampling2D, self).__init__(**kwargs)
        self.data_format = normalize_data_format(data_format)
        self.size = conv_utils.normalize_tuple(size, 2, 'size')
        self.input_spec = InputSpec(ndim=4)

    def compute_output_shape(self, input_shape):
        if self.data_format == 'channels_first':
            height = self.size[0] * input_shape[2] if input_shape[2] is not None else None
            width = self.size[1] * input_shape[3] if input_shape[3] is not None else None
            return (input_shape[0],
                    input_shape[1],
                    height,
                    width)
        elif self.data_format == 'channels_last':
            height = self.size[0] * input_shape[1] if input_shape[1] is not None else None
            width = self.size[1] * input_shape[2] if input_shape[2] is not None else None
            return (input_shape[0],
                    height,
                    width,
                    input_shape[3])

    def call(self, inputs):
        input_shape = K.shape(inputs)
        if self.data_format == 'channels_first':
            height = self.size[0] * input_shape[2] if input_shape[2] is not None else None
            width = self.size[1] * input_shape[3] if input_shape[3] is not None else None
        elif self.data_format == 'channels_last':
            height = self.size[0] * input_shape[1] if input_shape[1] is not None else None
            width = self.size[1] * input_shape[2] if input_shape[2] is not None else None

        return tf.image.resize(inputs, [height, width], method=tf.image.ResizeMethod.BILINEAR)

    def get_config(self):
        config = {'size': self.size, 'data_format': self.data_format}
        base_config = super(BilinearUpSampling2D, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}
print('Loading model...')
model = from_pretrained_keras("keras-io/monocular-depth-estimation", custom_objects=custom_objects, compile=False)
print('Successfully loaded model...')

def infer(image):
    inputs = load_images([image])
    outputs = predict(model, inputs)
    plasma = plt.get_cmap('plasma')
    rescaled = outputs[0][:, :, 0]
    rescaled = rescaled - np.min(rescaled)
    rescaled = rescaled / np.max(rescaled)
    image_out = plasma(rescaled)[:, :, :3]
    return image_out

def getDepth(frame, params):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = np.asarray(img)
    depth = infer(img)
    depth = (depth*255).astype('uint8')
    depth = cv2.cvtColor(depth, cv2.COLOR_RGB2BGR)
    return depth