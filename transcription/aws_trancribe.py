import boto3
from botocore.exceptions import ClientError
import logging
import time
from common import *
import json
import requests

BUCKET = 'dcm-automatic-transcription'
TRANSCRIPTS_DIR = from_data_root('aws-transcripts/', create_if_needed=True)[:-1]


def upload_file_to_bucket(local_fpath, bucket_fpath):
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_fpath, BUCKET, bucket_fpath)


def transcribe(audio_fpath, language_code):
    """
    :param language_code: e.g. 'en-US', or 'en-GB'
    """
    audio_rel_fpath = audio_fpath.split('recordings/')[1]
    job_name = f'transcribe-{audio_rel_fpath.replace("/", "__")}'
    print(f'Using job name "{job_name}" and bucket fpath "{audio_rel_fpath}"')

    print(f'Uploading "{audio_fpath}" to "{audio_rel_fpath}" in "{BUCKET}" bucket')
    upload_file_to_bucket(audio_fpath, audio_rel_fpath)
    print('Done')

    transcribe = boto3.client('transcribe')

    # delete job with the same name, if exists
    tr_jobs = transcribe.list_transcription_jobs()['TranscriptionJobSummaries']
    if job_name in [job['TranscriptionJobName'] for job in tr_jobs]:
        print(f'Job with namme {job_name} already exists, deleting the old one...')
        transcribe.delete_transcription_job(job_name)

    # start the transcription
    print(f'Starting the transcription job {job_name}')
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{BUCKET}/{audio_rel_fpath}'},
        MediaFormat=DEF_AUDIO_SUFFIX[1:],
        LanguageCode=language_code
    )

    # wait till finished
    before = time.time()
    MAX_SEC = 60*10 # 10 min
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in [
            'COMPLETED',
            'FAILED'
        ]:
            break

        if time.time() - before > MAX_SEC:
            logging.error(f'Transcription is taking longer than {MAX_SEC}s')
            logging.error(f'Terminating job {job_name}')
            transcribe.delete_transcription_job(job_name)
            raise TimeoutError('Transcription took too long')

        time.sleep(5)
    after = time.time()
    print(f'Done transcribing ({after - before:.2f}s)')

    # get and save the transcript
    url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    response = requests.get(url)

    json_ending = audio_rel_fpath.replace(DEF_AUDIO_SUFFIX, ".json")
    transcript_fpath = f'{TRANSCRIPTS_DIR}/{json_ending}'

    create_directories_if_necessary(transcript_fpath)
    transcript = response.json()
    with open(transcript_fpath, 'w') as f:
        json.dump(transcript, f)

    return transcript
