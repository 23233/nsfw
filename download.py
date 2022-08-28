import os
import logging

import requests
from tqdm import tqdm
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO  # 设置日志输出格式
                    , format="%(asctime)s - %(name)s - %(levelname)-8s - %(filename)-8s : %(lineno)s line - %(message)s"
                    # 日志输出的格式, -8表示占位符，让输出左对齐，输出长度都为8位
                    , datefmt="%Y-%m-%d %H:%M:%S"  # 时间输出的格式
                    )

saveBase = "./tmp"


def download(url: str):
    a = urlparse(url)
    fileName = os.path.basename(a.path)
    savePath = os.path.join(saveBase, fileName)
    # 用流stream的方式获取url的数据
    resp = requests.get(url, stream=True, timeout=60, headers={"User-Agent": "resok.cn/nsfw/fetch v1.0"})
    if resp.status_code != 200:
        logging.warning("下载文件 %s 响应码错误 %d", url, resp.status_code)
        return False, "", ""
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', 0))
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(savePath, 'wb') as file, tqdm(
            desc="download " + fileName,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    return True, savePath, fileName
