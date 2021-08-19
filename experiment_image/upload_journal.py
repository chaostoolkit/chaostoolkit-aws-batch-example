import os
from datetime import datetime

import boto3


def upload_journal():
    s3 = boto3.client("s3")
    with open("/home/svc/experiments/journal.json", "rb") as journal:
        s3.upload_fileobj(
            journal,
            os.environ["JOURNAL_BUCKET"],
            f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.json",
        )


if __name__ == "__main__":
    upload_journal()
