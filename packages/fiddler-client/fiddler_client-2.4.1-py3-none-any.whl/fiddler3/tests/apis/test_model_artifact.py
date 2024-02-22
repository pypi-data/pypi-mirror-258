import io
import os
import shutil
import tarfile
from http import HTTPStatus
from pathlib import Path

import pytest
import responses

from fiddler3.entities.job import Job
from fiddler3.entities.model import Model
from fiddler3.exceptions import NotFound
from fiddler3.schemas.deployment_params import DeploymentParams
from fiddler3.tests.apis.test_model import API_RESPONSE_200, API_RESPONSE_404
from fiddler3.tests.constants import JOB_ID, MODEL_ID, MODEL_NAME, PROJECT_NAME, URL

ARTIFACT_202_RESPONSE = {
    'data': {'job': {'id': JOB_ID, 'name': 'Deploy artifact model - manual'}},
    'api_version': '3.0',
    'kind': 'NORMAL',
}
MODEL_ARTIFACT_JOB_API_RESPONSE_200 = {
    'api_version': '3.0',
    'kind': 'NORMAL',
    'data': {
        'name': 'Deploy artifact model - manual',
        'id': JOB_ID,
        'status': 'SUCCESS',
        'progress': 100.0,
        'error_message': None,
        'error_reason': None,
    },
}

DOWNLOAD_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': f'Model artifact not found for {PROJECT_NAME}/{MODEL_NAME}',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Model artifact not found for {PROJECT_NAME}/{MODEL_NAME}',
                'help': '',
            }
        ],
    }
}
DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}

BASE_TEST_DIR = f'{Path(__file__).resolve().parent.parent}'
MODEL_DIR = os.path.join(BASE_TEST_DIR, 'artifact_test_dir')


@responses.activate
def test_add_model_artifact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/models/{MODEL_ID}/deploy-artifact',
        json=ARTIFACT_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=MODEL_ARTIFACT_JOB_API_RESPONSE_200,
    )

    job_obj = model.add_artifact(
        model_dir=MODEL_DIR, deployment_params=DeploymentParams(**DEPLOYMENT_PARAMS)
    )
    assert isinstance(job_obj, Job)


@responses.activate
def test_add_model_artifact_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/models/{MODEL_ID}/deploy-artifact',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(NotFound):
        model.add_artifact(
            model_dir=MODEL_DIR, deployment_params=DeploymentParams(**DEPLOYMENT_PARAMS)
        )


@responses.activate
def test_update_model_artifact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.put(
        url=f'{URL}/v3/models/{MODEL_ID}/deploy-artifact',
        json=ARTIFACT_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=MODEL_ARTIFACT_JOB_API_RESPONSE_200,
    )
    job_obj = model.update_artifact(
        model_dir=MODEL_DIR, deployment_params=DeploymentParams(**DEPLOYMENT_PARAMS)
    )

    assert isinstance(job_obj, Job)


@responses.activate
def test_update_model_artifact_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )

    model = Model.get(id_=MODEL_ID)
    responses.put(
        url=f'{URL}/v3/models/{MODEL_ID}/deploy-artifact',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        model.update_artifact(
            model_dir=MODEL_DIR, deployment_params=DeploymentParams(**DEPLOYMENT_PARAMS)
        )


@responses.activate
def test_download_model_artifact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    output_dir = os.path.join(BASE_TEST_DIR, 'test_download')
    tar_file_path = os.path.join(BASE_TEST_DIR, 'artifact.tar')
    with tarfile.open(tar_file_path, 'w:gz') as tar:
        tar.add(MODEL_DIR, arcname=os.path.basename(MODEL_DIR))
    with open(tar_file_path, 'rb') as tar_file:
        data = io.BufferedReader(tar_file)
        responses.get(url=f'{URL}/v3/models/{MODEL_ID}/download-artifact', body=data)
        model.download_artifact(output_dir=output_dir)
    shutil.rmtree(str(output_dir))
    os.remove(tar_file_path)


@responses.activate
def test_download_model_artifact_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)
    output_dir = os.path.join(BASE_TEST_DIR, 'test_download')
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/download-artifact',
        json=DOWNLOAD_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        model.download_artifact(output_dir=output_dir)
