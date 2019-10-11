import boto3
from botocore.exceptions import ClientError
import logging
import time
from common import *
import json
import requests
import pprint

BUCKET = 'dcm-automatic-transcription'
AWS_TRANSCRIPTS_DIR = from_data_root(
    'aws-transcripts/', create_if_needed=True
)[:-1]

# ---------------------------------------------------------------------
# --- Public
# ---------------------------------------------------------------------


def transcribe(audio_fpath, language_code, prefix='noprefix'):
    """
    :param language_code: e.g. 'en-US', or 'en-GB'
    """

    # get the job name and location where we'll upload the file in the bucket
    job_name = _get_job_name(prefix, audio_fpath)
    bucket_fpath = _get_bucket_fpath(prefix, audio_fpath)

    def _print(msg):
        print(f'{job_name}: {msg}')

    _print(f'\nUsing job name "{job_name}" and bucket fpath "{bucket_fpath}"')

    # upload the file to S3 bucket
    _print(
        f'\nUploading "{audio_fpath}" to "{bucket_fpath}" '
        f'in "{BUCKET}" bucket'
    )
    _upload_file_to_bucket(audio_fpath, bucket_fpath)

    # get the transcribing client
    transcribe_client = boto3.client('transcribe')

    # delete job with the same name, if exists
    _delete_existing_transcribe_job(transcribe_client, job_name)

    # start the transcription
    _print(f'\nStarting the transcription job "{job_name}"')
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{BUCKET}/{bucket_fpath}'},
        MediaFormat='mp3',
        LanguageCode=language_code
    )
    _print(f'\nTranscription started with response: {response}')

    # wait till it finishes
    before = time.time()
    status = _wait_for_transcribe_to_finish(transcribe_client, job_name)
    after = time.time()
    _print(f'Done transcribing ({after - before:.2f}s)')

    transcript_json = _get_transcript_from_status(status)
    _save_transcript(transcript_json, audio_fpath)

    return transcript_json


# ---------------------------------------------------------------------
# --- Implementation
# ---------------------------------------------------------------------


def _get_fname(audio_fpath):
    fname = os.path.basename(audio_fpath)
    fname = '.'.join(fname.split('.')[:-1])

    return fname


def _get_job_name(prefix, audio_fpath):
    fname = _get_fname(audio_fpath)
    job_name = f'tr--{prefix}--{fname.replace(" ", "_")}'

    return job_name


def _get_bucket_fpath(prefix, audio_fpath):
    return f'{prefix}--{_get_fname(audio_fpath)}'


def _upload_file_to_bucket(local_fpath, bucket_fpath):
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_fpath, BUCKET, bucket_fpath)


def _get_transcript_from_status(status):
    # TODO - this URL can be accessed publicly, find out if more secure way
    url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    response = requests.get(url)
    transcript_json = response.json()

    return transcript_json


def _save_transcript(transcript_json, audio_fpath):
    audio_rel_fpath = _get_fname(audio_fpath)
    json_ending = audio_rel_fpath.replace('.mp3', ".json")
    transcript_fpath = f'{AWS_TRANSCRIPTS_DIR}/{json_ending}'
    create_directories_if_necessary(transcript_fpath)

    with open(transcript_fpath, 'w') as f:
        json.dump(transcript_json, f)


def _wait_for_transcribe_to_finish(transcribe_client, job_name, max_minutes=10):
    start_time = time.time()
    max_sec = 60 * max_minutes

    while True:
        status = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        if status['TranscriptionJob']['TranscriptionJobStatus'] in [
            'COMPLETED',
            'FAILED'
        ]:
            break

        if time.time() - start_time > max_sec:
            logging.error(f'Transcription is taking longer than {max_sec}s')
            logging.error(f'Terminating job {job_name}')
            transcribe_client.delete_transcription_job(job_name)
            raise TimeoutError('Transcription took too long')

        time.sleep(5)

    return status


def _delete_existing_transcribe_job(transcribe_client, job_name):
    try:
        transcribe_client.delete_transcription_job(
            TranscriptionJobName=job_name
        )
        print(
            f'\nJob with name "{job_name}" already existed, so it was deleted'
        )
    except Exception as e:
        if not 'The requested job couldn\'t be found' in str(e):
            raise

