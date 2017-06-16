from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.fast_layers import *
from cs231n.layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian with standard     #
        # deviation equal to weight_scale; biases should be initialized to zero.   #
        # All weights and biases should be stored in the dictionary self.params.   #
        # Store weights and biases for the convolutional layer using the keys 'W1' #
        # and 'b1'; use keys 'W2' and 'b2' for the weights and biases of the       #
        # hidden affine layer, and keys 'W3' and 'b3' for the weights and biases   #
        # of the output affine layer.                                              #
        ############################################################################
        C, H, W = input_dim

        stride = 1
        pad = (filter_size - 1) // 2
        pool_height = 2
        pool_width = 2
        pool_stride = 2

        H_prime = int((H - filter_size + 2 * pad) / stride + 1)
        W_prime = int((W - filter_size + 2 * pad) / stride + 1)
        H_pool = int((H_prime - pool_height) / pool_stride + 1)
        W_pool = int((W_prime - pool_width) / pool_stride + 1)
        affine_input = H_pool * W_pool * num_filters

        # print('H_pool:', H_pool)
        # print('W_pool:', W_pool)

        # Convolutional layer
        self.params['W1'] = np.random.normal(0, weight_scale,
                                             [num_filters, C, filter_size, filter_size])
        self.params['b1'] = np.zeros(num_filters)

        # Affine layer
        self.params['W2'] = np.random.normal(0, weight_scale, [affine_input, hidden_dim])
        self.params['b2'] = np.zeros(hidden_dim)

        # Affine layer
        self.params['W3'] = np.random.normal(0, weight_scale, [hidden_dim, num_classes])
        self.params['b3'] = np.zeros(num_classes)

        # for k in self.params.keys():
        #     print(k, self.params[k].shape)
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        ############################################################################
        # print('W1 {} b1 {}'.format(W1.shape, b1.shape))
        # print('W2 {} b2 {}'.format(W2.shape, b2.shape))
        # print('W3 {} b3 {}'.format(W3.shape, b3.shape))
        out1, cache1 = conv_relu_pool_forward(X, W1, b1, conv_param, pool_param)
        out2, cache2 = affine_relu_forward(out1, W2, b2)
        scores, cache3 = affine_forward(out2, W3, b3)
        # print('out1 {}'.format(out1.shape))
        # print('out2 {}'.format(out2.shape))
        # print('out3 {}'.format(scores.shape))
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net, #
        # storing the loss and gradients in the loss and grads variables. Compute  #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        ############################################################################
        loss, dx = softmax_loss(scores, y)
        nl = 3
        regularizers = [np.sum(np.square(self.params['W' + str(i)]) / 2)
                        for i in range(1, nl + 1)]
        loss += self.reg * sum(regularizers)
        dx, dw, db = affine_backward(dx, cache3)
        grads['W3'] = dw + self.reg
        grads['b3'] = db
        dx, dw, db = affine_relu_backward(dx, cache2)
        grads['W2'] = dw + self.reg
        grads['b2'] = db
        dx, dw, db = conv_relu_pool_backward(dx, cache1)
        grads['W1'] = dw + self.reg
        grads['b1'] = db
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads
