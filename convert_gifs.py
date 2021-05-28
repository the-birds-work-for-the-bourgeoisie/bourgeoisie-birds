from pathlib import Path
import os
from PIL import Image


current_folder = ""
src_folder = "assets-src/"
target_folder = "assets-target/"
src_type = "GIF"
target_type = "png"


def convert_gifs():
    # maintains folder structure
    path_list = Path(current_folder + src_folder).glob('**/*.' + src_type)
    for path in path_list:

        # find GIFs and create folder destinations
        src_file = str(path)
        target_file = src_file.replace(src_folder, current_folder + target_folder)
        target_file = target_file.replace("." + src_type, "")
        Path(target_file).mkdir(parents=True, exist_ok=True)
        target_file_prefix = target_file + "/" + os.path.basename(target_file)

        # convert the GIF
        imageObject = Image.open(src_file)
        for frame in range(0, imageObject.n_frames):
            imageObject.seek(frame)
            imageObject.save('%s%d.%s' % (target_file_prefix, frame, target_type))


convert_gifs()
