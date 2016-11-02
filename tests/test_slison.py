from slisonner import decoder, encoder
from tests import mocker
from tempfile import mkdtemp
from shutil import rmtree


def test_full_encode_decode_cycle():
    temp_out_dir = mkdtemp()
    slice_id = 86400
    x_size, y_size = 10, 16

    temp_slice_path = mocker.generate_slice(x_size, y_size, 'float32')

    slice_meta_encoded, slison_filepath = encoder.encode_slice(
        filepath=temp_slice_path,
        slice_duration=300,
        timestamp=slice_id,
        layer_id='london',
        x_size=x_size,
        y_size=y_size,
        value_type='float32',
        out_dir=temp_out_dir)
    slice_data, slice_meta_decoded = decoder.decode_slison(slison_filepath)

    for key, encoded_value in slice_meta_encoded.items():
        assert encoded_value == slice_meta_decoded[key]

    rmtree(temp_out_dir)
