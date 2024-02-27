import asyncio
import json
import os
import shutil
import stat
import sys
import zipfile
from pathlib import Path

import ezkl
import requests

from spectral_cli import PLUMBER_URL

model_dir = str(Path('./model').resolve())
model_p = "./model"
model_onnx_path = str(Path(model_p + '/model.onnx').resolve())
model_compiled_path = str(Path(model_p + '/model.ezkl').resolve())
legacy_model_compiled_path = str(Path(model_p + '/compiled_model.onnx').resolve())

model_settings_path = str(Path(model_p + '/settings.json').resolve())
model_local_commitment_path = str(Path('./local-commitment.json').resolve())
model_witness_path = str(Path(model_p + '/witness.json').resolve())
model_vk_path = str(Path(model_p + '/model_vk.vk').resolve())
model_pk_path = str(Path(model_p + '/model_pk.pk').resolve())
model_srs_path = str(Path(model_p + '/kzg.srs').resolve())
model_proof_path = str(Path(model_p + '/zkml_hashed_proof.pf').resolve())
model_cal_path = str(Path(model_p + '/cal_data.json').resolve())
# cmd line args
model_input_path = './model/input.json'
model_input_path = './input.json'

zip_name = './model.zip'


def zip_files(files, zip_name='./model.zip'):
    with zipfile.ZipFile(zip_name, 'w') as zip_file:
        for file in files:
            add_file(zip_file, file, os.path.basename(file))
    return zip_name


def add_file(zip_file, path, zip_path=None):
    permission = 0o555 if os.access(path, os.X_OK) else 0o444
    zip_info = zipfile.ZipInfo.from_file(path, zip_path)
    zip_info.date_time = (2019, 1, 1, 0, 0, 0)
    zip_info.external_attr = (stat.S_IFREG | permission) << 16
    with open(path, "rb") as fp:
        zip_file.writestr(
            zip_info,
            fp.read(),
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        )


def upload_file_to_ipfs(path, ipfs_api_key):
    service_url = f'{PLUMBER_URL}/api/v1/ipfs'
    return upload_file_to_service(path, service_url, ipfs_api_key)


def upload_file_to_service(file_path, url, auth_token):
    with open(file_path, 'rb') as file:
        response = requests.post(url, data=file, headers={
                                 'Authorization': f'Bearer {auth_token}'})
    if response.status_code == 200:
        return response.text
    else:
        return None


def cleanup(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def generate_settings_file(onnx_model_path, input_json_path):
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    cleanup([model_srs_path, model_vk_path, model_settings_path, zip_name])
    run_args = ezkl.PyRunArgs()
    run_args.input_visibility = 'public'
    run_args.param_visibility = 'public'
    run_args.output_visibility = 'public'
    model_onnx_path = onnx_model_path
    try:
        res = ezkl.gen_settings(
            model_onnx_path, model_settings_path, py_run_args=run_args)
        if res:
            print('Settings successfully generated')
    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)

    async def f():
        res = await ezkl.calibrate_settings(input_json_path, model_onnx_path, model_settings_path,
                                            'resources')
        if res:
            print('Settings successfully calibrated')
        else:
            print('Settings calibration failed')
    asyncio.run(f())

    shutil.copy(model_settings_path, model_local_commitment_path)
    return model_local_commitment_path


def dump_model(onnx_model_path, input_json_path, ipfs_api_key):
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    cleanup([model_srs_path, model_vk_path, model_settings_path, zip_name])
    run_args = ezkl.PyRunArgs()
    run_args.input_visibility = 'public'
    run_args.param_visibility = 'public'
    run_args.output_visibility = 'public'
    model_onnx_path = onnx_model_path
    try:
        res = ezkl.gen_settings(
            model_onnx_path, model_settings_path, py_run_args=run_args)
        if res:
            print('Settings successfully generated')
    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)

    async def f():
        res = await ezkl.calibrate_settings(input_json_path, model_onnx_path, model_settings_path,
                                            'resources')
        if res:
            print('Settings successfully calibrated')
        else:
            print('Settings calibration failed')
    asyncio.run(f())

    try:
        res = ezkl.compile_circuit(
            model_onnx_path, model_compiled_path, model_settings_path)
        if res:
            cleanup([legacy_model_compiled_path])
            print('Model successfully compiled')
    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)

    res = ezkl.get_srs(model_srs_path, model_settings_path)
    try:
        res = ezkl.setup(model_compiled_path, model_vk_path,
                         model_pk_path, model_srs_path)
        if res:
            print('EZKL Setup was successful\n')
    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)

    path = zip_files([model_srs_path, model_vk_path,
                     model_settings_path, input_json_path])

    service_url = f'{PLUMBER_URL}/api/v1/ipfs'
    ipfs_hash = upload_file_to_service(path, service_url, ipfs_api_key)
    if ipfs_hash:
        print(f"Commitment successfully uploaded to IPFS: {ipfs_hash}")
    else:
        print("Commitment upload to IPFS failed.")
    return ipfs_hash


def generate_proof(data, compiled_model_path, prover_key_path, settings_path, srs_path, cwd, mock_first=True, prefix=""):
    input_path = os.path.join(cwd, f"{prefix}input.json")
    witness_path = os.path.join(cwd, f"{prefix}witness.json")
    proof_path = os.path.join(cwd, f"{prefix}proof.json")

    json.dump(data, open(input_path, "w"))
    _generate_witness(input_path, compiled_model_path, witness_path)
    zk_output = _calculate_zk_output(witness_path, settings_path)
    if mock_first: _generate_mock(witness_path, compiled_model_path)
    return (zk_output, _generate_proof(witness_path, compiled_model_path, prover_key_path, srs_path, proof_path))


def _generate_witness(input_path, compiled_model_path, witness_path):
    ezkl.gen_witness(data=input_path, model=compiled_model_path, output=witness_path)


def _calculate_zk_output(witness_path, settings_path):
    with open(witness_path, 'r') as witness_file:
        witness = json.load(witness_file)
    zk_output_felt = witness['outputs']
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)
    return ezkl.vecu64_to_float(zk_output_felt[0][0], settings['model_output_scales'][0])


def _generate_mock(witness_path, compiled_model_path):
    ezkl.mock(witness=witness_path, model=compiled_model_path)


def _generate_proof(witness_path, compiled_model_path, prover_key_path, srs_path, proof_path):
    res = ezkl.prove(witness=witness_path,
                    model=compiled_model_path,
                    pk_path=prover_key_path,
                    proof_path=proof_path,
                    srs_path=srs_path,
                    proof_type="single")
    if res:
        return proof_path
