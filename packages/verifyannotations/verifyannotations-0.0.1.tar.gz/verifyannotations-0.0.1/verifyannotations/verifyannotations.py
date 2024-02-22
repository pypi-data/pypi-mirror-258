import os
import random

import cv2


class VerifyDataAnnotations:
    def __init__(
        self,
        label_folder,
        raw_image_folder,
        output_image_folder,
        image_name_list_path,
        class_path,
    ):
        self.label_folder = label_folder
        self.raw_image_folder = raw_image_folder
        self.output_image_folder = output_image_folder
        self.image_name_list_path = image_name_list_path
        self.class_path = class_path

    def check_folders(self):
        # Check if label folder exists
        if not os.path.exists(self.label_folder):
            print("Error: Label folder does not exist.")
            return False

        # Check if raw image folder exists
        if not os.path.exists(self.raw_image_folder):
            print("Error: Raw image folder does not exist.")
            return False

        # Check if output folder exists, create if necessary
        if not os.path.exists(self.output_image_folder):
            os.makedirs(self.output_image_folder)

        # Check if label folder contains only text files
        label_files = os.listdir(self.label_folder)
        for file_name in label_files:
            if not file_name.endswith(".txt"):
                print("Error: Label folder should only contain text files.")
                return False

        # Check if raw image folder contains only image files
        image_files = os.listdir(self.raw_image_folder)
        image_extensions = [".bmp", ".jpg", ".jpeg", ".png"]
        for file_name in image_files:
            if not file_name.endswith(tuple(image_extensions)):
                print("Error: Raw image folder should only contain image files.")
                return False

        return True

    def plot_one_box(self, x, image, color=None, label=None, line_thickness=None):
        tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
        color = color or [random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
        cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        if label:
            tf = max(tl - 1, 1)
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)
            cv2.putText(
                image,
                label,
                (c1[0], c1[1] - 2),
                0,
                tl / 3,
                [225, 255, 255],
                thickness=tf,
                lineType=cv2.LINE_AA,
            )

    def draw_box_on_image(self, image_name, classes, colors):
        txt_path = os.path.join(self.label_folder, f"{image_name}.txt")
        image_path = os.path.join(self.raw_image_folder, f"{image_name}.bmp")
        save_file_path = os.path.join(self.output_image_folder, f"{image_name}.bmp")

        source_file = open(txt_path)
        image = cv2.imread(image_path)
        try:
            height, width, _ = image.shape
        except AttributeError:
            print(f"Error: Image {image_name}.bmp is invalid.")
            return 0

        box_number = 0
        for line in source_file:
            staff = line.split()
            class_idx = int(staff[0])

            x_center, y_center, w, h = (
                float(staff[1]) * width,
                float(staff[2]) * height,
                float(staff[3]) * width,
                float(staff[4]) * height,
            )
            x1 = round(x_center - w / 2)
            y1 = round(y_center - h / 2)
            x2 = round(x_center + w / 2)
            y2 = round(y_center + h / 2)

            self.plot_one_box(
                [x1, y1, x2, y2],
                image,
                color=colors[class_idx],
                label=classes[class_idx],
                line_thickness=None,
            )

            cv2.imwrite(save_file_path, image)

            box_number += 1
        return box_number

    def make_name_list(self):
        image_file_list = os.listdir(self.raw_image_folder)
        text_image_name_list_file = open(self.image_name_list_path, "w")

        for image_file_name in image_file_list:
            image_name, _ = os.path.splitext(image_file_name)
            text_image_name_list_file.write(image_name + "\n")

        text_image_name_list_file.close()

    def run_verification(self):
        if not self.check_folders():
            return

        self.make_name_list()

        classes = open(self.class_path).read().strip().split("\n")
        random.seed(42)
        colors = [
            [random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))
        ]

        image_names = open(self.image_name_list_path).read().strip().split()

        box_total = 0
        image_total = 0
        for image_name in image_names:
            box_num = self.draw_box_on_image(
                image_name,
                classes,
                colors,
            )
            box_total += box_num
            image_total += 1
            print("Box number:", box_total, "Image number:", image_total)
