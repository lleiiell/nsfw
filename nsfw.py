from flask import Flask, jsonify, request

import urllib
from urllib2 import urlopen

import numpy as np
import caffe

import classify_nsfw

# Pre-load caffe model.
nsfw_net = caffe.Net("nsfw_model/deploy.prototxt",  # pylint: disable=invalid-name
                     "nsfw_model/resnet_50_1by2_nsfw.caffemodel", caffe.TEST)

# Load transformer
# Note that the parameters are hard-coded for best results
caffe_transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR

app = Flask(__name__)

@app.route('/ck')
def ck():

    u0 = u = ""

    try:
        u0 = request.args.get('u')
        u = urllib.unquote(u0).decode('utf8')

        handle = urlopen(u)
        image_data = handle.read()

        # Classify.
        scores = classify_nsfw.caffe_preprocess_and_compute(image_data, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=['prob'])

        # Scores is the array containing SFW / NSFW image probabilities
        # scores[1] indicates the NSFW probability
        # print "NSFW score:  " , scores[1]

        rt = {
            "code": 0,
            "msg": "",
            "data": {
                "score" : scores[1]
            }
        }
        return jsonify(rt)


    except Exception as e:
        msg = "%s, decode: %s, raw: %s" % (str(e), u, u0)
        rt = {
            "code": 500,
            "msg": msg,
            "data": {}
        }
        return jsonify(rt)