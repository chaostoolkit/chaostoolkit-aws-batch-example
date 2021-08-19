FROM chaostoolkit/chaostoolkit:latest

RUN pip install chaostoolkit-aws

RUN mkdir /home/svc/experiments

COPY experiments /home/svc/experiments
COPY run_experiment.sh /home/svc/experiments/
COPY upload_journal.py /home/svc/experiments/

WORKDIR /home/svc/experiments

ENTRYPOINT [ "sh", "run_experiment.sh" ]
