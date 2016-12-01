from zipfile import ZipFile
from sys import byteorder
from io import BytesIO
from os import path
import numpy as np
import lz4f
import json


def encode_slice_file(filepath, out_dir, **kwargs):
    slice_data = load_slice(filepath, kwargs['value_type'])
    slice_meta, slison = encode_slice(slice_data, **kwargs)
    slison_filepath = save_slison(slison, out_dir,
                                  slice_meta['id'])
    return slice_meta, slison_filepath


def encode_slice(slice_data, **kwargs):
    compressed_slice_data = compress_slice(slice_data)
    slice_meta = get_slice_meta(slice_data, compressed_slice_data, kwargs)
    slice_meta['metrics'] = get_slice_metrics(slice_data)
    slison_data = pack_slice(compressed_slice_data, slice_meta)
    slison = slison_data.getvalue()
    return slice_meta, slison


def load_slice(filepath, value_type):
    with open(filepath) as infile:
        slice_data = np.fromfile(infile, dtype=value_type)
    return slice_data


def compress_slice(slice_data):
    compressed_slice_data = lz4f.compressFrame(slice_data)
    return compressed_slice_data


def get_slice_meta(slice_data, compressed_slice_data, params):
    meta = {}

    meta['endian'] = byteorder
    meta['lz4-compatible'] = True

    meta['duration'] = params['slice_duration']

    meta['ts'] = params['timestamp']
    meta['id'] = str(params['timestamp'])
    meta['layerId'] = params['layer_id']

    meta['rawSize'] = slice_data.nbytes
    meta['compressedSize'] = len(compressed_slice_data)
    meta['size'] = [params['x_size'], params['y_size']]
    meta['valueType'] = params['value_type']

    return meta


def get_slice_metrics(slice_data):
    metrics = {}

    metrics['max'] = np.max(slice_data).item()
    metrics['min'] = np.min(slice_data).item()
    metrics['average'] = float(np.average(slice_data))

    return metrics


def pack_slice(compressed_slice_data, slice_meta):
    '''

    :param compressed_slice_data:
    :param slice_meta:
    :return: a BytesIO object, that contains a zip directory of slice and meta
    '''
    slice_id = slice_meta['id']

    container = BytesIO()
    zip_archive = ZipFile(container, mode='w')

    # 1. Add slice data
    add_data_to_zip(compressed_slice_data, '{}.slice'.format(slice_id),
                    zip_archive)
    # 2. Add slice json meta
    slice_meta_bytes = json.dumps(slice_meta).encode()
    add_data_to_zip(slice_meta_bytes, '{}.json'.format(slice_id),
                    zip_archive)

    return container


def add_data_to_zip(data, filename, zip_archive):
    file = BytesIO(data)
    zip_archive.writestr(filename, file.getvalue())


def save_slison(slison, out_dir, slison_id):
    out_filepath = path.join(out_dir, '{}.slison'.format(slison_id))
    with open(out_filepath, 'wb') as f:
        f.write(slison)
    return out_filepath
