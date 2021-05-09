import boto3
import os
import re

from functools import lru_cache

BUCKET_NAME = "optimus-experiments"
DOWNLOAD_DIR = "/tmp/"


def make_download_path(filename):
    return os.path.join(DOWNLOAD_DIR, filename)


def make_optimus_evaluated_path(filename):
    return os.path.join(DOWNLOAD_DIR, filename)


def is_remote_file(filename):
    return filename.startswith("s3://")


@lru_cache(maxsize=0)
def get_client():
    return boto3.client("s3")


def get_file(s3_filename):
    r = re.match(r"s3://(.*)", s3_filename)
    if not r:
        raise Exception("S3 filenames must be of the form s3://<filename>")
    f = r.group(1)
    path, filename = os.path.split(f)
    client = get_client()
    download_path = make_download_path(filename)
    print("Downloading file from {} to {}".format(f, download_path))
    client.download_file("optimus-experiments", f, make_download_path(filename))
    return download_path


def put_file(local_filename, s3_filename):
    r = re.match(r"s3://(.*)", s3_filename)
    if not r:
        raise Exception("S3 filenames must be of the form s3://<filename>")
    f = r.group(1)
    client = get_client()
    print("Uploading file to {}".format(f))
    return client.upload_file(local_filename, "optimus-experiments", f)


def to_remote_filename(local_filename):
    return "s3://{}".format(local_filename)


def to_remote_optimus_evaluated_filename(local_filename):
    optimus_remote_path = "optimus_evaluated/{}".format(local_filename)
    return to_remote_filename(optimus_remote_path)


def to_remote_scored_filename(local_filename):
    remote_path = "scored/{}".format(local_filename)
    return to_remote_filename(remote_path)
