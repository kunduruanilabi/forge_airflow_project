from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 10),
    'retries': 1,
}

# Create the DAG
with DAG(
    dag_id='docker_python_slim_dag',
    default_args=default_args,
    schedule_interval='@daily',  
    catchup=False,
) as dag:
    
  # Bash command to configure sudoers for passwordless `apt install docker-ce`
    # configure_sudoers = BashOperator(
    #     task_id='configure_sudoers',
    #     bash_command="""
    #    curl -fsSL https://get.docker.com -o get-docker.sh
    #     """
    # )

    # Example task to install docker-ce using sudo without a password
    install_docker = BashOperator(
        task_id='install_docker_ce',
        bash_command='sudo -u airflow install -y docker-ce',
    )
    # Define a Bash command task to pull the Python slim image
    pull_python_slim_image = BashOperator(
        task_id='pull_python_slim_image',
        bash_command='docker pull python:3.9-slim',  # Pulling Python slim image
    )

    # Define another task to run a command in the pulled Python slim image
    run_command_in_docker = BashOperator(
        task_id='run_command_in_docker',
        bash_command='docker run --rm python:3.9-slim python -c "print(\'Hello from inside the Python slim Docker container!\')"',
    )

    # Set task dependencies
    install_docker >> pull_python_slim_image >> run_command_in_docker

# The DAG is now ready to be executed.