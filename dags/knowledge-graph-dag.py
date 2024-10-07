from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import yaml
from src.pipeline.orchestrator import PipelineOrchestrator

# Load configuration
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Define DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'knowledge_graph_builder',
    default_args=default_args,
    description='Build and update knowledge graph from multiple sources',
    schedule_interval=timedelta(days=1),
)

def process_sources(**context):
    orchestrator = PipelineOrchestrator(config)
    for source in config['sources']:
        orchestrator.process_source(source)

process_task = PythonOperator(
    task_id='process_sources',
    python_callable=process_sources,
    provide_context=True,
    dag=dag,
)

process_task
