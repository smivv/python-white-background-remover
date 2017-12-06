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

    conn = sqlite3.connect('../db/caresymbols.db')
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
            data.append((255-item[0], 255-item[1], 255-item[2], item[3]))

        img.putdata(data)
        stream = io.BytesIO()
        img.save(stream, format="PNG")

        cursor.execute('UPDATE caresymbols SET symbol = ? WHERE _id = ?', (sqlite3.Binary(stream.getvalue()), row[0]))

        logging.info('%s image removed..' % row[0])
    cursor.close()
    conn.commit()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--path', default='/',
        help='Path where images are placed.')

    logging.info('Path argument passed..')

    parser.add_argument(
        '--new_path', default='removed/',
        help='Path where removed images will be placed.')

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
