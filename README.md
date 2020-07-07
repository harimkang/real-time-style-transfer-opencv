# real-time-style-transfer-opencv

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://davinci-ai.tistory.com/)

This project shows the streaming of open-cv by applying the style-transfer to the background (or person) except the person (or background) in real time using a web-cam connected to a laptop or computer.

  - Basic streaming function
  - Camera zoom function, capture function, video recording function
  - Style conversion function using Open-CV dedicated UI button
  - Provides a function to apply style (background-to-person) using icons

> Style Transfer can be applied by using a pre-trained model or by training yourself. There are many sources and sites that provide the ability to convert images, but there are few sources that are easily applied in real time, and in order to realize a simple idea that applies only to backgrounds other than people, we need to customize it to start the project.

### Environment

real-time-style-transfer-opencv was developed using the following library version:

* [Python3] - 3.7.4
* [Tensorflow] - 2.0.0
* [opencv-python] - 4.1.2.30

and [window 10] Environment

### Installation

real-time-style-transfer-opencv require [python3](https://www.python.org/) v3+ and [tensorflow](https://www.tensorflow.org/) v2+ to run.

Install the dependencies.

```sh
$ pip install opencv-python
$ pip intall tensorflow==2.0.0
```

Clone Repository...

```sh
$ mkdir project
$ cd project
$ git clone https://github.com/harim4422/real-time-style-transfer-opencv.git
$ cd real-time-style-transfer-opencv
```

### Models

real-time-style-transfer-opencv requires a model that segmentes people and a style transfer model.

| Model | README |
| ------ | ------ |
| Style Transfer | [magnta/arbitrary-image-stylization-v1-256](https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2)|
| People Segmentation | [U-Net][PlGh] |


### Start Project

Just Start:
```sh
$ python Camera.py
```

### Step
- To Do


### Todos

 - FPS improvement
 
### Blog Posting
- [Davinci-AI](https://davinci-ai.tistory.com/)

## Team

The project was conducted at the Korea Institute of Artificial Intelligence and formed a team called [Mevia].
- Harim Kang
- Dahsom Jang
- Yujin Nam


License
----

MIT


**From MEVIA**
