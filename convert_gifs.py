from pathlib import Path
import os
from PIL import Image
import numpy as np

# check for windows
from PIL.GifImagePlugin import GifImageFile

from utils import file_utils

slash = "\\" if os.name == 'nt' else "/"
current_folder = ""
src_folder = "assets-src" + slash
target_folder = "assets-target" + slash
src_type = "GIF"
target_type = "png"


def convert_frame_to_transparent(imageObject: GifImageFile) -> Image:
    """
    https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color
    replaces #FFFFFF (white) with #00000000 (clear)
    """
    rgbaImage: Image = imageObject.convert('RGBA')

    data = np.array(rgbaImage)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[...][white_areas.T] = (0, 0, 0, 0)  # Transpose back needed

    return Image.fromarray(data)


def convert_gifs():
    # maintains folder structure
    path_list = file_utils.get_files_in_folder_by_file_extension(current_folder + src_folder, src_type)
    for path in path_list:
        print("Converting", path.name, "...")
        # find GIFs and create folder destinations
        src_file = str(path)
        target_file = src_file.replace(src_folder, current_folder + target_folder)
        target_file = target_file.replace("." + src_type.upper(), "")
        target_file = target_file.replace("." + src_type.lower(), "")
        Path(target_file).mkdir(parents=True, exist_ok=True)
        target_file_prefix = target_file + slash + os.path.basename(target_file)

        # convert the GIF
        imageObject: GifImageFile = Image.open(src_file)
        for frame in range(0, imageObject.n_frames):
            imageObject.seek(frame)
            destination_file = '%s-%d.%s' % (target_file_prefix, frame, target_type)
            rgbaImage = convert_frame_to_transparent(imageObject)
            rgbaImage.save(destination_file)
            print("Saved", destination_file)


convert_gifs()
