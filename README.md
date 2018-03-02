# Image labeling tool

## Description

This cross-platform GUI tool was made to label image data set for deep learning models training.

- Inputs: directory with image files, can be nested, and possibly labeling CSV file.
- Outputs: labels.csv file with structure: _"path_to_image_file" ; number_
- Number can represent either how many objects are there on an image or class identifier.
- Ex.: "./test/0flower/bu Pink (Custom).JPG;2"

*NOTE*: Loading images was separated into it's own thread to not lock the screen while loading.
Potentially you can add a bit of code to even start labeling images while loading is in progress.

*NOTE*: Potentially more specific object rectangles labeling can be added.

*NOTE*: Tested with Python 3.6.4.

## Installation

Run pip install -r requirements.txt. For MacOS there is only one requirement (pillow). And to run ```python quickLabel.py```.
 Alternatevely:
```
pip install quickLabel
```

## Usage

Here is how we us this tool:
- Default directory for files: './images'. Can be changed in the app, then press "Load".
- Default labels file: './labels.csv'. Can be changed in top section of quickLabel.py.
- Use arrow buttons to page screens. Prev: "<-", Next: "->"".
- Left click on an image to select those that have the object on them.
- Click right button to make the value 0.
- Click several times to increase the value up to 5.
- Last selected image can be set to 0 by pressing '0'.
- After all done, press Export button to export labels file.
- File labels.csv will be created after all done.
