from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import timedelta,datetime

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'docker_python_version',
    default_args=default_args,
    description='A simple DAG to run python --version in Docker',
    schedule_interval=None,  # This DAG does not have a schedule and is meant to run manually
    start_date=datetime(2024, 10, 9),
    catchup=False,  # Do not run past executions
)

# Define the DockerOperator task
docker_task = DockerOperator(
    task_id='run_python_version',
    image='python:3.9',  # Docker image from Docker Hub
    command='python --version',  # The command to execute inside the container
    auto_remove=True,  # Automatically remove the container once the task is complete
    dag=dag,
)

# Define task sequence (optional if you have more tasks)
docker_task
