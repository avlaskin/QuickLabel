# -------------------------------------------------------------------------------
# Name:         Object labeling tool
# Created:      28/01/2018
# Author:       Alexey Vlaskin
# Description:  This tool made for the labeling images at scale.
# -------------------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox as tkMessageBox
from PIL import Image, ImageTk, ImageDraw
from threading import Thread
import queue
from handler import ImageHandler

# Ideally we would want to set those from the UI. But for now it will do.
# Configuration for paths:
IMAGE_DIR = './images/'
LABELS_FILE = 'labels.csv'


class GridModel:
    """Class for grid configuration of images.
    """

    def __init__(self, cells_w, cells_h, cell_size):
        self.gridShape = (cells_w, cells_h)
        self.cellSize = cell_size
        self.cellPadding = 5
        self.canvasShape = (self.cellPadding + self.gridShape[0] * (cell_size + self.cellPadding),
                            self.cellPadding + self.gridShape[1] * (cell_size + self.cellPadding))


class ScreenStateModel():
    def __init__(self):
        self.page = 0
        self.maxPage = 0


class Labeler:
    """Class for UI to label images.
    """

    def __init__(self, master, input_dir, label_file='labels.csv', cells_shape=(8, 5), cell_size=200):
        self.callback_queue = queue.Queue()
        self.handler = ImageHandler()
        self.screenModel = ScreenStateModel()
        self.gridModel = GridModel(cells_shape[0], cells_shape[1], cell_size)
        self.tkimages = []
        self.label_file = label_file
        self.current_selected_index = -1

        self.parent = master
        self.parent.title("Image Labeling Tool")
        self.parent.bind("<Key-Right>", self.next_screen)
        self.parent.bind("<Key-Left>", self.previous_screen)
        self.parent.bind("e", self.export_pressed)
        self.parent.bind("0", self.zero_pressed)

        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)

        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouse_left_click)
        self.mainPanel.bind("<Button-2>", self.mouse_right_click)
        self.mainPanel.bind("<Motion>", self.mouse_move)
        self.mainPanel.grid(row=1, column=0, columnspan=4, sticky=W + N)
        self.mainPanel.config(width=self.gridModel.canvasShape[0],
                              height=self.gridModel.canvasShape[1])
        self.frameEdges = self.mainPanel.create_rectangle(0, 0,
                                                          self.gridModel.canvasShape[0],
                                                          self.gridModel.canvasShape[1], fill='green')
        # Top Control Panel GUI
        self.controlPanel = Frame(self.frame)
        self.controlPanel.grid(row=0, column=0, columnspan=4, sticky=N + W)
        self.controlPanel.config(width=self.gridModel.canvasShape[0])

        self.topLabel = Label(self.controlPanel, text='Found images: %d' % self.handler.length, width=40)
        self.topLabel.grid(row=0, column=0, sticky=W)

        self.exportButton = Button(self.controlPanel, text='Export Labels!', width=20, command=self.export_pressed)
        self.exportButton.grid(row=0, column=1, padx=50, sticky=N + S)

        self.infoButton = Button(self.controlPanel, text='Info', width=5, command=self.info_pressed)
        self.infoButton.grid(row=0, column=2, sticky=W + E)

        self.fileLabel = Label(self.controlPanel, text='', width=40)
        self.fileLabel.grid(row=0, column=3, padx=10, sticky=E)

        # Load images in the another thread
        self.thread = Thread(target=self.scan_directory, args=(input_dir,))
        self.thread.start()
        self.parent.after(1, self.check_loaded)

    def check_loaded(self):
        try:
            callback = self.callback_queue.get(False)  # doesn't block
            callback()
            self.update_ui()
        except queue.Empty:  # raised when queue is empty
            self.topLabel.config(text='Found images: %d' % self.handler.get_images_len())
            self.parent.after(1, self.check_loaded)

    def scan_directory(self, input_dir):
        self.handler.scan_dir(input_dir)
        self.callback_queue.put(self.update_ui)

    def update_ui(self):
        cells_shape = self.gridModel.gridShape
        if len(self.handler.lastError) > 0:
            self.topLabel.config(text='ERROR!: %s' % self.handler.lastError)
        if self.handler.get_images_len() > 0:
            self.topLabel.config(text='Found images: %d' % self.handler.get_images_len())
            self.screenModel.maxPage = int(1 + self.handler.get_images_len() / (cells_shape[0] * cells_shape[1]))
            self.load_all_images()

    def next_screen(self, _):
        if self.screenModel.page + 1 < self.screenModel.maxPage:
            self.screenModel.page += 1
            self.load_all_images()

    def previous_screen(self, _):
        if self.screenModel.page - 1 >= 0:
            self.screenModel.page -= 1
            self.load_all_images()

    def export_pressed(self, event=None):
        self.topLabel.config(text='Exporting labels to {}...'.format(self.label_file))
        self.handler.export_labels(self.label_file)
        self.topLabel.config(text='Exporting labels to {} is Done!'.format(self.label_file))

    def info_pressed(self, event=None):
        m = "Here is how we us this tool:\n" \
            "\n0. Put your dataset images into ./images/ or specify another folder in labeler.py" \
            "\n The app automatically loads this folder.\n" \
            "\n1. Use arrow buttons to page screens. " \
            "\nPrev: <- \nNext: ->\n" \
            "\n2. Click on images to select those that have the object on them." \
            "\n3. After all done, press Export button to export labels file." \
            "\n4. Click right button to make the value 0." \
            "\n5. Click several times to increase the value up to 5." \
            "\n6. Last selected image can be set to 0 by pressing '0'." \
            "\n7. After all done, press Export button or 'e' to export labels file." \
            "\n8. File labels.csv will be created after all done."
        tkMessageBox.showinfo("Usage", message=m)

    def zero_pressed(self, event=None):
        if self.current_selected_index > 0:
            overall_index = self.current_selected_index
            self.handler.nullify_file(overall_index)
            self.reload_image(-1, -1, overall_index)

    def get_index_from_mouse(self, x, y):
        if self.handler.length == 0:
            return 0, 0, 0
        shift = self.get_image_shift()
        x_index = int((x - self.gridModel.cellPadding) / (self.gridModel.cellSize + self.gridModel.cellPadding))
        y_index = int((y - self.gridModel.cellPadding) / (self.gridModel.cellSize + self.gridModel.cellPadding))
        overall_index = shift + x_index + y_index * self.gridModel.gridShape[0]
        return x_index, y_index, overall_index

    def mouse_left_click(self, event):
        x_index, y_index, overall_index = self.get_index_from_mouse(event.x, event.y)
        if overall_index >= self.handler.length:
            return
        self.handler.toggle_file(overall_index)
        self.current_selected_index = overall_index
        self.reload_image(x_index, y_index)

    def mouse_right_click(self, event):
        x_index, y_index, overall_index = self.get_index_from_mouse(event.x, event.y)
        if overall_index >= self.handler.length:
            return
        self.handler.nullify_file(overall_index)
        self.reload_image(x_index, y_index)

    def mouse_move(self, event):
        x_index, y_index, overall_index = self.get_index_from_mouse(event.x, event.y)
        if overall_index >= self.handler.length:
            return
        self.fileLabel.config(text='File: %s' % self.handler.images[overall_index])

    def reload_image(self, x, y, overall_index=-1):
        shift = self.get_image_shift()
        if overall_index > 0:
            y = int((overall_index - shift) / self.gridModel.gridShape[0])
            x = overall_index - shift - y * self.gridModel.gridShape[0]
        s = self.gridModel.cellSize
        padding = self.gridModel.cellPadding
        overall_index = shift + x + y * self.gridModel.gridShape[0]
        if overall_index >= self.handler.get_images_len():
            return
        position_x = padding + x * (s + padding)
        position_y = padding + y * (s + padding)
        self.load_image(self.handler.images[overall_index],
                        position_x,
                        position_y,
                        width=s, height=s)

    def get_image_shift(self):
        return self.screenModel.page * self.gridModel.gridShape[0] * self.gridModel.gridShape[1]

    def load_all_images(self):
        z = self.get_image_shift()
        s = self.gridModel.cellSize
        padding = self.gridModel.cellPadding
        self.tkimages = []
        for i in range(self.gridModel.gridShape[1]):
            for j in range(self.gridModel.gridShape[0]):
                self.load_image(self.handler.images[z], padding + j * (s + padding),
                                padding + i * (s + padding), width=s, height=s)
                z += 1
                if z >= self.handler.get_images_len():
                    return

    def load_image(self, image_path, x_offset, y_offset, width=50, height=50):
        try:
            img = Image.open(image_path)
        except OSError:
            img = Image.new('RGB', (self.gridModel.cellSize, self.gridModel.cellSize), color='yellow')
            d = ImageDraw.Draw(img)
            d.text((10, 10), "BROKEN IMAGE", fill=(0, 0, 255))
        img = img.resize((width, height), Image.ANTIALIAS)
        # img.thumbnail((width, height), Image.ANTIALIAS)
        tkimg = ImageTk.PhotoImage(img)
        self.tkimages.append(tkimg)
        index = self.handler.images.index(image_path)
        value = self.handler.selected[index]
        if index >= 0:
            self.mainPanel.create_image(x_offset, y_offset, image=tkimg, anchor=NW)
        if self.handler.selected[index] > 0:
            # Draw selection if needed
            lw = 2
            self.mainPanel.create_line(x_offset + lw, y_offset + lw,
                                       x_offset + width - lw, y_offset + lw,
                                       x_offset + width - lw, y_offset + height - lw,
                                       x_offset + lw, y_offset + height - lw,
                                       x_offset + lw, y_offset + lw,
                                       width=lw * 2,
                                       fill='red')
            # Draw label to show selected value
            self.mainPanel.create_text(x_offset + width - lw * 10, y_offset + height - lw * 10, fill='red',
                                       text='%d' % value)


if __name__ == '__main__':
    root = Tk()
    tool = Labeler(root, IMAGE_DIR, label_file=LABELS_FILE)
    root.resizable(width=True, height=True)
    root.mainloop()
