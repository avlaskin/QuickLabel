import os
import csv


class ImageHandler:
    """This class handles files, selection and CSV.
    """

    def __init__(self):
        self.images = []
        self.loaded = False
        self.image_scores = [0]
        self.lastError = ""
        self.csv_delimiter = ";"
        self.csv_quotes = '"'

    @property
    def numImages(self):
        return len(self.images)

    def scan_dir(self, dir_name):
        self.get_files(dir_name)
        self.image_scores = [0] * self.numImages
        for i in range(self.numImages):
            self.image_scores[i] = 0

    def get_files(self, dir_name, update_load=True):
        """Given a directory `dir_name`, recursively scans for image
        files, appending their paths to `self.images`"""
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
            ext = fa[-1].lower()
            if ext in ('jpg', 'png', 'jpeg'):
                self.images.append(f)
            else:
                # This recurrency is to support nested dirs
                if os.path.isdir(f):
                    self.get_files(f, False)
        if update_load:
            self.loaded = True

    def toggle_file(self, index):
        """Increments file values in the UI by 1"""
        self.image_scores[index] = self.image_scores[index] + 1
        if self.image_scores[index] > 5:
            self.image_scores[index] = 0

    def nullify_file(self, index):
        """Sets file values in the UI to 0"""
        self.image_scores[index] = 0

    def export_labels(self, file_name):
        with open(file_name, 'w', newline='') as csvfile:
            label_writer = csv.writer(csvfile, delimiter=self.csv_delimiter,
                                      quotechar=self.csv_quotes, quoting=csv.QUOTE_MINIMAL)
            for i in range(self.numImages):
                f_name = self.images[i]
                label = str(self.image_scores[i])
                label_writer.writerow([f_name, label])

    def import_labels(self, file_name):
        if os.path.isfile(file_name):
            with open(file_name, 'r') as csvfile:
                label_reader = csv.reader(csvfile, delimiter=self.csv_delimiter, quotechar=self.csv_delimiter)
                for row in label_reader:
                    print(row[0])
                    print(row[1])
                    try:
                        index = self.images.index(row[0])
                    except ValueError:
                        self.lastError = "We are loading the wrong labels file."
                        print("We are loading the wrong labels file.")
                        return
                    if index > 0:
                        self.image_scores[index] = int(row[1])
