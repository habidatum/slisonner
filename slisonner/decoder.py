from zipfile import ZipFile
import lz4f
import numpy as np
import json
from io import BytesIO


def decode_slison_bytes(slison_bytes):
    decode_slison(BytesIO(slison_bytes))


def decode_slison(file):
    with ZipFile(file) as slison_zip:
        meta_filename, data_filename = parse_slison_content(slison_zip)
        slice_meta = extract_slice_meta(slison_zip, meta_filename)
        value_type = slice_meta['valueType']
        slice_data = extract_slice_data(slison_zip, data_filename,
                                        value_type)
    return slice_data, slice_meta


def parse_slison_content(slison_zip):
    slison_meta_file = [filename for filename in slison_zip.namelist()
                        if '.json' in filename][0]
    slison_data_file = [filename for filename in slison_zip.namelist()
                        if '.slice' in filename][0]
    return slison_meta_file, slison_data_file


def extract_slice_meta(slison_zip, meta_filename):
    with slison_zip.open(meta_filename) as slice_meta_file:
        meta = json.loads(slice_meta_file.read().decode())
    return meta


def extract_slice_data(slison_zip, data_filename, value_type):
    with slison_zip.open(data_filename) as slice_file:
        data = lz4f.decompressFrame(slice_file.read(),
                                    dCtx=lz4f.createDecompContext())
        slice_data = np.frombuffer(data['decomp'], dtype=value_type)
    return slice_data

