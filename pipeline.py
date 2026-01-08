from prefect import flow, task
import subprocess


@task
def extract():
    subprocess.run(["python", "extract.py"], check=True)


@task
def transform():
    subprocess.run(["python", "transform.py"], check=True)


@task
def load():
    subprocess.run(["python", "load.py"], check=True)


@flow(name="chess-data-pipeline")
def chess_pipeline():
    extract()
    transform()
    load()


if __name__ == "__main__":
    chess_pipeline()
