<!-- toc start: 3 [do not erase this comment] -->
**Table of contents**
- [Balloons burst](#balloons-burst)
	- [How to run](#how-to-run)
	- [How to use](#how-to-use)
	- [Dependencies](#dependencies)
	- [Used technologies](#used-technologies)
	- [Screenshot](#screenshot)
	- [External references](#external-references)
	- [Author](#author)
<!-- toc end [do not erase this comment] -->

# Balloons burst

I developed this simple project for the event "Futuro Remoto 2024" to show how the AI technologies work to the students of primary school, I used a pre trained model made by Google, in particular I've used a model named "finger landmark" included into the Mediapipe library of Google. This model is able to recognize the main points of our fingers and, in general, of the hands. I've used it to catch the touching between two specific fingers and then execute a specific action, in my case I have used five different gestures, the first four gestures are used to move the mouse cursor on the main four directions (up, down, left, right), the last gesture (when the user simulate the fist gesture) is used to emulate the left click button of the mouse.

The second part of my project consisted to an objective which used the features implemented with mediapipe, so I thought that hit the ballons on the screen was could be a good idea, and especially was easy to implement, in fact to develope this solution I've used HTML and CSS only.

## How to run

1. Run the file `main.py` to launch the AI model
1. Try the gestures on the main window who opened when you launch the python script
1. Don't close the python program, and open `index.html` on your main browser to launch the balloon game

## How to use

## Dependencies

* `OpenCV`
* `Mediapipe`
* `pyautogui`

## Used technologies

* Python
* HTML
* CSS

## Screenshot

## External references

* [Futuro Remoto](https://www.futuroremoto.eu/)
* [Mediapipe module](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=it)

## Author

Emilio Garzia, 2024