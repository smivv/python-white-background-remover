from PIL import Image
import argparse
import os.path
import logging

logging.basicConfig(level=logging.INFO)


def serve(config):

    threshold = int(config.threshold)

    filenames = []
    path = config.path
    new_path = config.new_path
    valid_images = ["." + f for f in config.valid_formats.split(',')]

    logging.info('Parameters parsed..')

    for filename in os.listdir(path):
        ext = os.path.splitext(filename)[1]
        if ext.lower() in valid_images:
            filenames.append(filename)

    for filename in filenames:

        ext = os.path.splitext(filename)[1].replace('.', '')
        img = Image.open(path + filename)
        img = img.convert("RGBA")

        datas = img.getdata()

        data = []

        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                data.append((255, 255, 255, 0))
            else:
                data.append(item)

        img.putdata(data)
        img.save(new_path + filename, ext)

        logging.info('%s image processed..' % filename)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--path', default='/',
        help='Path where images are placed.')

    logging.info('Path argument passed..')

    parser.add_argument(
        '--new_path', default='processed/',
        help='Path where processed images will be placed.')

    logging.info('New path argument passed..')

    parser.add_argument(
        '--valid_formats', required=False, default='jpg,jpeg,png',
        help='Valid formats of images. Default jpg, png.')

    logging.info('Valid formats argument passed..')

    parser.add_argument(
        '--threshold', required=False, default='225',
        help='Threshold. Default 225.')

    logging.info('Threshold argument passed..')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_args()

    logging.info('Processing started..')

    # Run service
    serve(config=args)
