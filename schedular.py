import schedule
import time
import subprocess
import sys
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler('pipeline.log', maxBytes=1_000_000, backupCount=3)
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[handler])

def run_pipeline():

    logging.info("Pipeline execution started")

    python_executable = sys.executable

    steps = ['pipeline/ingest.py', 'pipeline/transform.py', 'pipeline/load.py']

    for step in steps:
        result = subprocess.run([python_executable, step])

        if result.returncode != 0:
            logging.error(f"Pipeline step failed: {step} (exit code {result.returncode})")
            print(f"Pipeline failed at {step}, aborting run.")
            return

    logging.info("Pipeline execution completed")

    print("Pipeline executed successfully!")

# Run every 60 minutes
schedule.every(60).minutes.do(run_pipeline)

print("Scheduler started...")

logging.info("Scheduler started")

while True:
    schedule.run_pending()
    time.sleep(1)