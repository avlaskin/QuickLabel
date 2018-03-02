import os
import csv


class ImageHandler:
    """This class handles files, selection and CSV.
    """

    def __init__(self):
        self.images = []
        self.length = 0
        self.loaded = False
        self.selected = [0]
        self.lastError = ""

    def scan_dir(self, dir_name):
        self.get_files(dir_name)
        self.length = len(self.images)
        self.selected = [0] * self.length
        for i in range(self.length):
            self.selected[i] = 0

    def get_images_len(self):
        return len(self.images)

    def get_files(self, dir_name, update_load=True):
        if update_load:
            self.loaded = False
            self.images = []

        if not os.path.isdir(dir_name):
            self.lastError = "Folder is not found: %s" % dir_name
            self.loaded = True
            return

        for filename in os.listdir(dir_name):
            f = os.path.join(dir_name, filename)
            fa = f.split('.')
            ext = fa[-1]
            if ext == "jpg" or ext == "jpeg" or ext == "JPEG" or ext == "JPG":
                self.images.append(f)
            else:
                # This recurrency is to support nested dirs
                if os.path.isdir(f):
                    self.get_files(f, False)
        if update_load:
            self.loaded = True

    def toggle_file(self, index):
        self.selected[index] = self.selected[index] + 1
        if self.selected[index] > 5:
            self.selected[index] = 0

    def nullify_file(self, index):
        self.selected[index] = 0

    def export_labels(self, file_name):
        with open(file_name, 'w', newline='') as csvfile:
            label_writer = csv.writer(csvfile, delimiter=';',
                                      quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(self.length):
                f_name = self.images[i]
                label = str(self.selected[i])
                label_writer.writerow([f_name, label])

