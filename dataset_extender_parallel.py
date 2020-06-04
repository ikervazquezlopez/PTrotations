import sys
import os
import cv2
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import multiprocessing as mp

log_file = "log.txt"

hugin_lib_path = "D:/WorkSoftware/Hugin/bin/"
pto_gen = join(hugin_lib_path, "pto_gen.exe")
pano_modify = join(hugin_lib_path, "pano_modify.exe")
hugin_executor = join(hugin_lib_path, "hugin_executor.exe")

rotations = [-90, -67, -45, -22, 22, 45, 67, 90]

pano_w = 3328
pano_h = 1664

input_dir = "./"
output_dir = "./"

pool = mp.Pool(mp.cpu_count())

def convert_filename_png(filename):
    return filename.split('.')[0] + ".png"

def convert_filename_pto(filename):
    return filename.split('.')[0] + ".pto"


def process_panorama(f):
    print("Processing: {}".format(f))
    path = join(input_dir, f)
    fname = f.split('.')[0]

    # Generate Hugin project file
    os.system("{cmd} {input} >>{log} 2>&1".format(cmd=pto_gen, input=path, log=log_file)) # This generates a pto file with name f.pto
    pto_file = convert_filename_pto(f)

    # Save rotation 0 image
    os.system("{cmd} --canvas={w}x{h} {input} >>{log} 2>&1".format(cmd=pano_modify, w=pano_w, h=pano_h, input=join(input_dir,pto_file), log=log_file))
    pto_file = fname + "_mod.pto"
    os.system("{cmd} --stitching {input} >>{log} 2>&1".format(cmd=hugin_executor, input=join(input_dir,pto_file), log=log_file))

    # Move the image to the output directory
    out_f = "{} - {}.tif".format(fname, fname)
    out_f = join(input_dir, out_f)
    tgt_f = "{name}_{y}_{p}_{r}.tif".format(name=fname, y=0, p=0, r=0)
    tgt_f = join(output_dir, tgt_f)
    os.rename(r"{output}".format(output=out_f), r"{target}".format(target=tgt_f))

    # Change .tif image to .png format
    img = cv2.imread(tgt_f)
    cv2.imwrite(convert_filename_png(tgt_f), img)
    os.remove(tgt_f)

    # Rotate the image multiple times
    for r in rotations:
        # Rotate image
        pto_file = convert_filename_pto(f)
        os.system("{cmd} --rotate=0,{pitch},0 --canvas={w}x{h} {input} >>{log} 2>&1".format(cmd=pano_modify, pitch=r, w=pano_w, h=pano_h, input=join(input_dir,pto_file), log=log_file))
        pto_file = fname + "_mod.pto"
        os.system("{cmd} --stitching {input} >>{log} 2>&1".format(cmd=hugin_executor, input=join(input_dir,pto_file), log=log_file))

        # Move the image to the output directory
        out_f = "{} - {}.tif".format(fname, fname)
        out_f = join(input_dir, out_f)
        tgt_f = "{name}_{y}_{p}_{r}.tif".format(name=fname, y=0, p=r, r=0)
        tgt_f = join(output_dir, tgt_f)
        os.rename(r"{output}".format(output=out_f), r"{target}".format(target=tgt_f))

        # Change .tif image to .png format
        img = cv2.imread(tgt_f)
        cv2.imwrite(convert_filename_png(tgt_f), img)
        os.remove(tgt_f)



if __name__ == '__main__':

    if isfile(log_file):
        os.remove(log_file)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    onlyfilespaths = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]


    pool.map_async(process_panorama, onlyfilespaths)

    pool.close()
    pool.join()
