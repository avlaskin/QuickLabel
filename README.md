# Image labeling tool

## Description

This cross-platform GUI tool was made to label image data set which will have just two classes.
Potentially more specific object rectangle labeling can be added.

- Inputs: directory with image files, can be nested
- Outputs: labels.csv file with structure: "path_to_image_file" ; number
- Ex: "./test/0flower/bu Pink (Custom).JPG;2"

*NOTE*: Loading images was separated into it's own thread to not lock the screen while loading.
Potentially you can add a bit of code to even start labeling images while loading is in progress.

## Installation

Just run pip install -r requirements.txt. For MacOS there is only one requirement: pillow.
Tested with Python 3.6.4.

## Usage

Here is how we us this tool:
- Default directory for files: './images'. Can be changed in top section of labeler.py.
- Default labels file: './labels.csv'. Can be changed in top section of labeler.py.
- Use arrow buttons to page screens. Prev: "<-", Next: "->"".
- Left click on an image to select those that have the object on them.
- Click right button to make the value 0.
- Click several times to increase the value up to 5.
- Last selected image can be set to 0 by pressing '0'.
- After all done, press Export button to export labels file.
- File labels.csv will be created after all done.
