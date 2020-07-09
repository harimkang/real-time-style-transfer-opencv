# real-time-style-transfer-opencv

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://davinci-ai.tistory.com/)

![git_logo2](https://user-images.githubusercontent.com/38045080/86984908-d3409100-c1ca-11ea-8bf2-f2b450037a25.PNG)

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

And Use Buttons and Icon:

![image](https://user-images.githubusercontent.com/38045080/87044268-454bc100-c231-11ea-9632-d3f62b502437.png)

- Buttons: Click to switch the video to the painter's style. The button is blue in the On state and the photo in the Off state. Currently, there are Gogh, Kandinsky, Monet, Picasso, Na Hye-suk and Super Mario painting styles.
- Icon: The icon is available when you are in Style Transfer (when a certain button is On), and if Style Transfer is applied only to the background, it is switched to apply to people other than the background. The reverse is also possible.

### Customizing the code
- Adding Style:

1. Add the image of the style you want to add to the folder.
![image](https://user-images.githubusercontent.com/38045080/87045078-68c33b80-c232-11ea-9bc4-24423f53cd5d.png)

2. You can edit style_img in StyleTransfer class in style_transfer.py
![image](https://user-images.githubusercontent.com/38045080/87045600-0880c980-c233-11ea-9a11-264b9a0fb45c.png)

3. Adding Button - In Button setting function of ButtonManager class in Button.py, you can add Button object like other buttons.
![image](https://user-images.githubusercontent.com/38045080/87045844-53024600-c233-11ea-9ff7-78ca040300bd.png)

Below is an example of adding btn10.
```python
btn10 = Button("Button's Name")
btn_list = [btn, btn2, btn3, btn4, btn5, btn6, btn7, btn10]
self.add_button_list(btn_list)
```

### Todos

 - FPS improvement
 
### Blog Posting
- [Davinci-AI](https://davinci-ai.tistory.com/)

## Team
![real-time](https://user-images.githubusercontent.com/38045080/86984202-e4889e00-c1c8-11ea-8521-c115c42d302b.png)

The project was conducted at the Korea Lab of Artificial Intelligence and formed a team called Mevia.
- Harim Kang
- Dahsom Jang
- Yujin Nam

![ezgif com-webp-to-png](https://user-images.githubusercontent.com/38045080/86984248-02560300-c1c9-11ea-8102-93ba35c05987.png)

License
----

MIT


**From MEVIA**
