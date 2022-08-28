import math
import os

import cv2
import numpy as np
import onnxruntime
from download import download, saveBase
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

sess = onnxruntime.InferenceSession("nsfw.onnx")
sess.set_providers(["CPUExecutionProvider"])
input_name_1 = sess.get_inputs()[0].name
output_name_1 = sess.get_outputs()[0].name
CATEGORIES = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

try:
    os.mkdir(os.path.join(os.getcwd(), saveBase))
except Exception as r:
    pass


def predictionImg(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    inImgNp = np.expand_dims(resized, axis=0).astype(np.float32)
    inImgNp /= 255
    result = sess.run([output_name_1], {input_name_1: inImgNp})
    r = {}
    for i, c in enumerate(CATEGORIES):
        r[c] = math.floor(result[0][0][i] * 100)
    return r


@app.route("/")
def index():
    return "首页"


@app.route('/remote', methods=['POST'])
def remote():  # put application's code here
    data = request.get_json()  # 获取 JSON 数据
    if data:
        url = data.get("url", "")
        if url.startswith("http"):
            # 下载图片
            success, imgPath, fileName = download(url)
            if success:
                return jsonify(predictionImg(imgPath))
            return jsonify({"detail": "下载图片出错"}), 400
    return jsonify({"detail": "参数错误"}), 400


@app.route("/predict", methods=['POST'])
def predict():
    f = request.files.get("file")
    if f.filename != "":
        # 最主要的过滤有攻击性的文件名
        filename = secure_filename(f.filename)
        savePath = os.path.join(saveBase, filename)
        f.save(savePath)
        return jsonify(predictionImg(savePath))
    return jsonify({"detail": "获取文件失败"}), 400


if __name__ == '__main__':
    app.run()
