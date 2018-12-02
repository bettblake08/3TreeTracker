""" This module hosts the image manager class that handles the manipulation
    of all images.
"""
import os
from PIL import Image


class ImageManager:
    BASE_DIR = os.path.dirname(__file__)
    UPLOAD_DIRECTORY = os.path.join(BASE_DIR, '../../public/repo/upload')

    @classmethod
    def create_thumbnails(cls, current_file):
        if not cls.resize_and_crop(current_file, (150, 150)):
            return False

        if not cls.resize_and_crop(current_file, (300, 300)):
            return False

        return True

    @classmethod
    def resize(cls, current_file, width, height):
        file_name = "thumb_" + str(width) + "_" + str(height) + ".jpg"
        in_file = os.path.join(
            cls.UPLOAD_DIRECTORY,
            current_file.name + "." + current_file.fileType)

        out_file = os.path.join(
            cls.UPLOAD_DIRECTORY,
            current_file.name,
            file_name)

        if not os.path.exists(os.path.dirname(out_file)):
            os.makedirs(os.path.dirname(out_file))

        try:
            image = Image.open(in_file)
            image.thumbnail((width, height), Image.ANTIALIAS)
            image.save(out_file, "JPEG")
            return True
        except IOError:
            return False

    @classmethod
    def resize_and_crop(cls, current_file, size, crop_type='middle'):
        """
            Resize and crop an image to fit the specified size.
            args:
                img_path: path for the image to resize.
                modified_path: path to store the modified image.
                size: `(width, height)` tuple.
                crop_type: can be 'top', 'middle' or 'bottom', depending on this
                    value, the image will cropped getting the 'top/left', 'midle' or
                    'bottom/rigth' of the image to fit the size.
            raises:
                Exception: if can not open the file in img_path of there is problems
                    to save the image.
                ValueError: if an invalid `crop_type` is provided.
        """
        file_name = "thumb_" + str(size[0]) + "_" + str(size[1]) + ".jpg"
        img_path = os.path.join(
            cls.UPLOAD_DIRECTORY,
            current_file.name + "." + current_file.fileType)

        modified_path = os.path.join(
            cls.UPLOAD_DIRECTORY,
            current_file.name,
            file_name)

        if not os.path.exists(os.path.dirname(modified_path)):
            os.makedirs(os.path.dirname(modified_path))

        # If height is higher we resize vertically, if not we resize horizontally
        image = Image.open(img_path)
        # Get current and desired ratio for the images
        img_ratio = image.size[0] / float(image.size[1])
        ratio = size[0] / float(size[1])
        # The image is scaled/cropped vertically or horizontally depending on the ratio
        if ratio > img_ratio:
            image = image.resize(
                (int(size[0], size[0] * image.size[1]) / int(image.size[0])),
                Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, image.size[0], size[1])
            elif crop_type == 'middle':
                box = (0, (image.size[1] - size[1]) / 2,
                       image.size[0], (image.size[1] + size[1]) / 2)
            elif crop_type == 'bottom':
                box = (0, image.size[1] - size[1],
                       image.size[0], image.size[1])
            else:
                return False
                #raise ValueError('ERROR: invalid value for crop_type')

            image = image.crop(box)
        elif ratio < img_ratio:
            image = image.resize(
                (int(size[1] * image.size[0] / image.size[1]), int(size[1])),
                Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, size[0], image.size[1])
            elif crop_type == 'middle':
                box = ((image.size[0] - size[0]) / 2, 0,
                       (image.size[0] + size[0]) / 2, image.size[1])
            elif crop_type == 'bottom':
                box = (image.size[0] - size[0], 0,
                       image.size[0], image.size[1])
            else:
                return False
                #raise ValueError('ERROR: invalid value for crop_type')
            image = image.crop(box)
        else:
            image = image.resize(
                (size[0], size[1]),
                Image.ANTIALIAS)
            # If the scale is the same, we do not need to crop
        image.save(modified_path)

        return True
