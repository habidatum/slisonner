from os import path
from zipfile import ZipFile
import lz4f
import numpy as np
import json


def decode_slison(filepath):
    slison_id = parse_path(filepath)

    with ZipFile(filepath) as slison_zip:
        slice_meta = extract_slice_meta(slison_zip, slison_id)
        value_type = slice_meta['valueType']
        slice_data = extract_slice_data(slison_zip, slison_id, value_type)
    return slice_data, slice_meta


def parse_path(full_path):
    slison_name = path.basename(full_path)
    slison_id = slison_name.split('.')[0]
    return slison_id


def extract_slice_meta(slison_zip, slison_id):
    with slison_zip.open('{}.json'.format(slison_id)) as slice_meta_file:
        meta = json.loads(slice_meta_file.read().decode())
    return meta


def extract_slice_data(slison_zip, slison_id, value_type):
    with slison_zip.open('{}.slice'.format(slison_id)) as slice_file:
        data = lz4f.decompressFrame(slice_file.read(),
                                    dCtx=lz4f.createDecompContext())
        slice_data = np.frombuffer(data['decomp'], dtype=value_type)
    return slice_data

