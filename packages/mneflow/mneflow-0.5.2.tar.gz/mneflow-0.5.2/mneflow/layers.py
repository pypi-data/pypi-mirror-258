# -*- coding: utf-8 -*-
"""
Defines mneflow.layers for mneflow.models.

@author: Ivan Zubarev, ivan.zubarev@aalto.fi
"""
#TODO: keras compatible layers
#TODO: pooling layer

#import functools
import tensorflow as tf
from tensorflow.keras.initializers import Constant
from tensorflow.keras.activations import relu
from tensorflow.keras import constraints as k_con, regularizers as k_reg
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import numpy as np

bias_const = 0.1
bias_traiable = True

class BaseLayer(tf.keras.layers.Layer):
    def __init__(self, size, nonlin, specs, **args):
        super(BaseLayer, self).__init__(**args)
        self.size = size
        self.nonlin = nonlin
        self.specs = specs
        # self.specs.setdefault('l1_lambda', 0.)
        # self.specs.setdefault('l2_lambda', 0.)
        # self.specs.setdefault('l1_scope', [])
        # self.specs.setdefault('l2_scope', [])
        # self.specs.setdefault('maxnorm_scope', [])

    def _set_regularizer(self):
        if self.scope in self.specs['l1_scope'] or 'weights' in self.specs['l1_scope']:
            reg = k_reg.l1(self.specs['l1_lambda'])
            print('Setting reg for {}, to l1'.format(self.scope))
        elif self.scope in self.specs['l2_scope'] or 'weights' in self.specs['l2_scope']:
            reg = k_reg.l2(self.specs['l2_lambda'])
            print('Setting reg for {}, to l2'.format(self.scope))
        else:
            reg = None
        return reg

    def _set_constraints(self, axis=0):
        if self.scope in self.specs['unitnorm_scope']:
            constr = k_con.UnitNorm(axis=axis)
            print('Setting constraint for {}, to UnitNorm'.format(self.scope))
        else:
            constr = None
        return constr


class Dense(BaseLayer, tf.keras.layers.Layer):


    """
    Fully-connected layer
    
    """
    def __init__(self, scope='fc', size=None, nonlin=tf.identity, specs={},
                 **args):
        self.scope = scope
        super(Dense, self).__init__(size=size, nonlin=nonlin, specs=specs,
             **args)
        self.constraint = self._set_constraints()
        self.reg = self._set_regularizer()

    # def get_config(self):
    #     config = self.get_config()
    #     config.update({'scope': self.scope, 'size': self.size,
    #                    'nonlin': self.nonlin})
        # return config

    def build(self, input_shape):
        super(Dense, self).build(input_shape)
        # print(input_shape)
        self.flatsize = np.prod(input_shape[1:])
        #print(self.scope, ':::', )

        self.w = self.add_weight(shape=[self.flatsize, self.size],
                                 initializer='he_uniform',
                                 regularizer=self.reg,
                                 constraint=self.constraint,
                                 trainable=True,
                                 name='fc_weights',
                                 dtype=tf.float32)

        self.b = self.add_weight(shape=[self.size],
                                 initializer=Constant(bias_const),
                                 regularizer=None,
                                 trainable=bias_traiable,
                                 name='fc_bias',
                                 dtype=tf.float32)

        print("Built: {} input: {}".format(self.scope, input_shape))


    def call(self, x, training=None):
        """
        Dense layer currying, to apply layer to any input tensor `x`
        """
        while True:
            with tf.name_scope(self.scope):
                if len(x.shape) > 2:  # flatten if input is not 2d array
                    x = tf.reshape(x, [-1, self.flatsize])
                tmp = tf.matmul(x, self.w) + self.b
                tmp = self.nonlin(tmp, name='out')
                #print(self.scope, ": output :", tmp.shape)
                return tmp


class DeMixing(BaseLayer):
    """
    Spatial demixing Layer
    
    """
    
    def __init__(self, scope="dmx", size=None, nonlin=tf.identity, axis=-1,
                 specs={},  **args):
        self.scope = scope
        self.axis = axis
        super(DeMixing, self).__init__(size=size, nonlin=nonlin, specs=specs,
             **args)

    # def get_config(self):
    #     config = super(DeMixing, self).get_config()
    #     config.update({'scope': self.scope, 'size': self.size,
    #                    'nonlin': self.nonlin, 'axis': self.axis})
    #     return config

    def build(self, input_shape):

        super(DeMixing, self).build(input_shape)
        self.constraint = self._set_constraints(axis=0)
        self.reg = self._set_regularizer()

        self.w = self.add_weight(
                shape=(input_shape[self.axis], self.size),
                initializer='he_uniform',
                regularizer=self.reg,
                constraint = self.constraint,
                trainable=True,
                name='dmx_weights',
                dtype=tf.float32)

        self.b_in = self.add_weight(shape=([self.size]),
                                    initializer=Constant(bias_const),
                                    regularizer=None,
                                    trainable=bias_traiable,
                                    name='bias',
                                    dtype=tf.float32)
        print("Built: {} input: {}".format(self.scope, input_shape))

    #@tf.function
    def call(self, x, training=None):
        """ 
        """
        while True:
            with tf.name_scope(self.scope):
                try:
                    demix = tf.tensordot(x, self.w, axes=[[self.axis], [0]],
                                         name='dmx')
                    demix = self.nonlin(demix + self.b_in)
                    #print(self.scope, ": output :", demix.shape)
                    return demix
                except(AttributeError):
                    input_shape = x.shape
                    self.build(input_shape)

class SquareSymm(BaseLayer):
    """
    SquaredSymmetric Layer
    
    """
    def __init__(self, scope='ssym', size=None, nonlin=tf.identity, axis=1,
                 specs={},  **args):
        self.scope = scope
        self.axis = axis
        super(SquareSymm, self).__init__(size=size, nonlin=nonlin, specs=specs,
             **args)


    def build(self, input_shape):

        super(SquareSymm, self).build(input_shape)
        self.constraint = self._set_constraints(axis=0)
        self.reg = self._set_regularizer()

        self.w = self.add_weight(
                shape=(input_shape[self.axis], self.size),
                initializer='he_uniform',
                regularizer=self.reg,
                constraint = self.constraint,
                trainable=True,
                name='ssym_weights',
                dtype=tf.float32)

        self.b_in = self.add_weight(shape=([self.size]),
                                    initializer=Constant(0.1),
                                    regularizer=None,
                                    trainable=True,
                                    name='bias',
                                    dtype=tf.float32)
        print("Built: {} input: {}".format(self.scope, input_shape))

    #@tf.function
    def call(self, x, training=None):
        """ 
        """
        while True:
            with tf.name_scope(self.scope):
                try:
                    d1 = tf.tensordot(x, self.w, axes=[[1], [0]],
                                         name='smx') #output
                    d2 = tf.tensordot(d1, self.w, axes=[[1], [0]],
                                         name='smx')
    
                    demix = self.nonlin(d2 + self.b_in)
                    return demix
                except(AttributeError):
                    input_shape = x.shape
                    self.build(input_shape)
                    

class LFTConv(BaseLayer):
    """
    Stackable temporal convolutional layer, interpreatble (LF)
    
    """
    
    def __init__(self, scope='tconv', size=32,  nonlin=tf.nn.relu,
                 filter_length=7, pooling=2, padding='SAME', specs={},
                 **args):
        self.scope = scope
        super(LFTConv, self).__init__(size=size, nonlin=nonlin, specs=specs,
             **args)
        self.size = size
        self.filter_length = filter_length
        self.padding = padding

    # def get_config(self):

    #     config = super(LFTConv, self).get_config()
    #     config.update({'scope': self.scope,
    #                    'filter_length': self.filter_length,
    #                    'nonlin': self.nonlin, 'padding': self.padding})
    #    return config

    def build(self, input_shape):
        super(LFTConv, self).build(input_shape)
        self.constraint = self._set_constraints(axis=1)
        self.reg = self._set_regularizer()
        shape = [1, self.filter_length, input_shape[-1], 1]
        self.filters = self.add_weight(shape=shape,
                                       initializer='he_uniform',
                                       regularizer=self.reg,
                                       constraint=self.constraint,
                                       trainable=True,
                                       name='tconv_weights',
                                       dtype=tf.float32)

        self.b = self.add_weight(shape=([input_shape[-1]]),
                                 initializer=Constant(bias_const),
                                 regularizer=None,
                                 trainable=bias_traiable,
                                 name='bias',
                                 dtype=tf.float32)
        print("Built: {} input: {}".format(self.scope, input_shape))

    #@tf.function
    def call(self, x, training=None):
        """ 
        """
        while True:
            with tf.name_scope(self.scope):
                try:
                    conv = tf.nn.depthwise_conv2d(x,
                                                  self.filters,
                                                  padding=self.padding,
                                                  strides=[1, 1, 1, 1],
                                                  data_format='NHWC')
                    conv = self.nonlin(conv + self.b)

                    #print(self.scope, ": output :", conv.shape)
                    return conv
                except(AttributeError):
                    input_shape = x.shape
                    self.build(input_shape)


class VARConv(BaseLayer):
    """
    Stackable temporal convolutional layer
    """
    
    def __init__(self, scope='tconv', size=32,  nonlin=tf.nn.relu,
                 filter_length=7, pooling=2, padding='SAME', specs={},
                 **args):
        self.scope = scope
        super(VARConv, self).__init__(size=size, nonlin=nonlin, specs=specs,
             **args)
        self.size = size
        self.filter_length = filter_length
        self.padding = padding


    # def get_config(self):

    #     config = super(VARConv, self).get_config()
    #     config.update({'scope': self.scope,
    #                    'filter_length': self.filter_length,
    #                    'nonlin': self.nonlin, 'padding': self.padding})
    #    return config

    def build(self, input_shape):
        print("input_shape:", input_shape)
        super(VARConv, self).build(input_shape)

        self.constraint = self._set_constraints()
        self.reg = self._set_regularizer()
        shape = [1, self.filter_length, input_shape[-1], self.size]
        self.filters = self.add_weight(shape=shape,
                                       initializer='he_uniform',
                                       regularizer=self.reg,
                                       constraint=self.constraint,
                                       trainable=True,
                                       name='tconv_weights',
                                       dtype=tf.float32)

        self.b = self.add_weight(shape=([input_shape[-1]]),
                                 initializer=Constant(bias_const),
                                 regularizer=None,
                                 trainable=bias_traiable,
                                 name='bias',
                                 dtype=tf.float32)
        print("Built: {} input: {}".format(self.scope, input_shape))

    #@tf.function
    def call(self, x, training=None):
        """ 
        """
        while True:
            with tf.name_scope(self.scope):
                try:
                    conv = tf.nn.conv2d(x, self.filters,
                                        padding=self.padding,
                                        strides=[1, 1, 1, 1],
                                        data_format='NHWC')

                    conv = self.nonlin(conv + self.b)
                    #print(self.scope, ": output :", conv.shape)
                    return conv
                except(AttributeError):
                    input_shape = x.shape
                    self.build(input_shape)
                    #print(self.scope, 'building from call')


class TempPooling(BaseLayer):
    def __init__(self, scope='pool', stride=2, pooling=2, specs={},
                 padding='SAME', pool_type='max', **args):
        self.scope = '_'.join([pool_type, scope])
        super(TempPooling, self).__init__(size=None, nonlin=None, specs=specs,
                                          **args)
        self.strides = [1, 1, stride,  1]
        self.kernel = [1, 1, pooling,  1]

        self.padding = padding
        self.pool_type = pool_type

    #@tf.function
    def call(self, x):
        """
        """
        if self.pool_type == 'avg':
            pooled = tf.nn.avg_pool2d(
                                x,
                                ksize=self.kernel,
                                strides=self.strides,
                                padding=self.padding,
                                data_format='NHWC')
        else:
            pooled = tf.nn.max_pool2d(
                                x,
                                ksize=self.kernel,
                                strides=self.strides,
                                padding=self.padding,
                                data_format='NHWC')
        #print(self.scope, ": output :", pooled.shape)
        return pooled

    def build(self, input_shape):
        super(TempPooling, self).build(input_shape)
        self.built = True


    # def get_config(self):
    #     config = super(TempPooling, self).get_config()
    #     config.update({'scope': self.scope,
    #                    'pool_type': self.pool_type,
    #                    'stride': self.strides, 'pooling': self.pooling,
    #                    'padding': self.padding})
    #     return config



class LSTM(tf.keras.layers.LSTM):
    def __init__(self, scope='lstm', size=32, nonlin='tanh', dropout=0.0,
                 recurrent_activation='tanh', recurrent_dropout=0.0,
                 use_bias=True, unit_forget_bias=True,
                 kernel_regularizer=None, bias_regularizer=None,
                 return_sequences=True, stateful=False, unroll=False, **args):
        super(LSTM, self).__init__(name=scope,
                                     units=size,
                                     activation=nonlin,
                                     dropout=dropout,
                                     recurrent_activation=recurrent_activation,
                                     recurrent_dropout=recurrent_dropout,
                                     use_bias=use_bias,
                                     unit_forget_bias=unit_forget_bias,
                                     kernel_regularizer=kernel_regularizer,
                                     # kernel_initializer='glorot_uniform',
                                     # recurrent_initializer='orthogonal',
                                     bias_regularizer=bias_regularizer,
                                     return_sequences=return_sequences,
                                     stateful=stateful,
                                     unroll=unroll,
                                     **args)
        self.scope = scope
        self.size = size
        self.nonlin = nonlin
        print(self.scope, 'init : OK')

    # def get_config(self):
    #     config = super(LSTM, self).get_config()
    #     config.update({'scope': self.scope, 'size': self.size,
    #                    'nonlin': self.nonlin})
    #     return config

    def build(self, input_shape):
        # print(self.scope, 'build : OK')
        super(LSTM, self).build(input_shape)

    @tf.function
    def call(self, inputs, mask=None, training=None, initial_state=None):
        # print(self.scope, inputs.shape)
        return super(LSTM, self).call(inputs, mask=mask, training=training,
                                        initial_state=initial_state)




if __name__ == '__main__':
    print('Reloaded')

