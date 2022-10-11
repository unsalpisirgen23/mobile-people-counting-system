from __future__ import print_function, absolute_import, division

import os
import zipfile
import time
import numpy as np
import tensorflow as tf
from TrainerNormal import Trainer

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def main(img_folder, img_prefix, zip_intermedia_results=True):
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.8)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

    trainer = Trainer(sess)
    trainer.test(img_folder, [img_prefix],
                 './results')
    os.system('python2 ./DataUtil'
              % (os.path.join(img_folder, img_prefix + '_volume_out1.mat'),
                 os.path.join(img_folder, img_prefix + '_normal_01.png')))

    suffixes = ['__normal_0.png']
    if zip_intermedia_results:
     
        for suffix in suffixes:
            z.write(img_dir[:-4] + suffix)
            os.remove(img_dir[:-4] + suffix)
        z.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='path to image file')
    args = parser.parse_args()
    img_dir = args.file
    if not (img_dir.endswith('.png') or img_dir.endswith('.jpg')):
        print('Unsupport image format!!!')
        raise ValueError

    img_folder, img_name = os.path.split(img_dir)
    main(img_folder, img_name[:-4] + '_')
