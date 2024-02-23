import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from classifier_model import __version__ as _version
from classifier_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config
import boto3
import io

def load_from_s3(file_name: str) -> pd.DataFrame:
    REGION = 'us-east-1'
    ACCESS_KEY_ID = 'AKIAZRZBBO5ZHCDQ64VF'
    SECRET_ACCESS_KEY = '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'
    BUCKET_NAME = 'heart-dissease-data-bucket'
    KEY = f'{file_name}'
    s3c = boto3.client(
        's3', 
        region_name = REGION,
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
    )
    obj = s3c.get_object(Bucket=BUCKET_NAME , Key=KEY)
    dataframe = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
    return dataframe

def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe

def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()

