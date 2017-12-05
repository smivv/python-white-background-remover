from PIL import Image
import argparse
import os.path
import logging
import sqlite3
import codecs
import base64, io

logging.basicConfig(level=logging.INFO)

SIZE = 192

def serve(config):

    threshold = int(config.threshold)

    conn = sqlite3.connect('../assets/caresymbols.db')
    cursor = conn.cursor()
    rows = cursor.execute('select _id, symbol from caresymbols')
    rows = cursor.fetchall()
    for row in rows:

        f = open('tmp.png', 'wb')
        f.write(row[1])
        f.close()

        img = Image.open('tmp.png')
        img = img.convert("RGBA")

        datas = img.getdata()

        data = []

        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                data.append((255, 255, 255, 0))
            else:
                data.append(item)

        img.putdata(data)
        stream = io.BytesIO()
        img.save(stream, format="PNG")

        cursor.execute('UPDATE caresymbols SET symbol = ? WHERE _id = ?', (sqlite3.Binary(stream.getvalue()), row[0]))
        
        logging.info('%s image processed..' % row[0])


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
