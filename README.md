# NSFW

1、基于`Caffe`，`open_nsfw`识别NSFW图片  
2、使用框架 `Flask`  
3、依赖：Python2.7

## Install

1、docker build

```
docker build -t nsfw2 .
```

2、docker run

```
docker run -it --privileged -e FLASK_APP=nsfw.py -p 10022:80 -v {nsfw_path}:/workspace nsfw2 flask run -h 0.0.0.0 -p 80
```

`nsfw_path`为仓库根目录路径

3、api


http://localhost:10022/ck?u=https%3A%2F%2Fdun.163.com%2Fpublic%2Fres%2Fweb%2Fcase%2Fsexy_danger_2.jpg%3Fe30b03637bcdd08e499d5c5b8033276b

入参

`u` 图片链接编码地址（urlencode）