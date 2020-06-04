import sys
import os
import cv2
from os import listdir
from os.path import isfile, join, isdir


if __name__ == '__main__':


    files_count = int(sys.argv[1])
    input_dir = sys.argv[2]
    output_dir = sys.argv[3]

    if not isdir(output_dir):
        os.mkdir(output_dir)

    onlyfilespaths = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    onlyfilespaths = onlyfilespaths[:files_count]

    print("Copying {} files from {} to {}".format(len(onlyfilespaths), input_dir, output_dir))
    for f in onlyfilespaths:
        src_f = join(input_dir, f)
        dst_f = join(output_dir, f)
        os.system("copy {} {}".format(src_f, dst_f))
        
