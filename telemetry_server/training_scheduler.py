# Xerolux 2026
import schedule
import time
import logging
import os
import signal
import sys
import threading
from scripts.train_model import train_model

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("telemetry-trainer")

# Configuration
MODEL_DIR = os.environ.get("MODEL_DIR", "/app/models")
TARGET_MODELS = os.environ.get("TARGET_MODELS", "AERO_SLM").split(",")
TRAINING_TIME = os.environ.get("TRAINING_TIME", "03:00")  # 3 AM default

# Graceful shutdown
shutdown_event = threading.Event()


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("shutdown_signal_received", signal=sig)
    shutdown_event.set()
    sys.exit(0)


def run_training_job():
    logger.info("training_job_started")

    for model_name in TARGET_MODELS:
        model_name = model_name.strip()
        if not model_name:
            continue

        logger.info("training_model", model=model_name)

        safe_model_name = model_name.replace(" ", "_").replace("/", "_")
        output_file = os.path.join(MODEL_DIR, f"{safe_model_name}.pkl")

        try:
            success = train_model(model_name=model_name, output_file=output_file)

            if success:
                logger.info("training_successful", model=model_name)

                # Encrypt/Sign the model
                try:
                    from scripts.export_model import export_model

                    final_output_file = os.path.join(
                        MODEL_DIR, f"{safe_model_name}.enc"
                    )
                    export_model(input_file=output_file, output_file=final_output_file)

                    # Clean up raw pickle
                    if os.path.exists(output_file):
                        os.remove(output_file)
                        logger.info("cleaned_raw_pickle", file=output_file)
                except Exception as e:
                    logger.error("model_export_failed", model=model_name, error=str(e))
            else:
                logger.warning("training_failed_or_insufficient", model=model_name)

        except Exception as e:
            logger.error("training_exception", model=model_name, error=str(e))

    logger.info("training_job_finished")


def main():
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("scheduler_started")
    logger.info("target_models", models=TARGET_MODELS)
    logger.info("schedule", daily_at=TRAINING_TIME)

    # Schedule the job
    schedule.every().day.at(TRAINING_TIME).do(run_training_job)

    # Run once on startup if requested (e.g. for testing)
    if os.environ.get("RUN_ON_STARTUP", "false").lower() == "true":
        logger.info("running_initial_training")
        run_training_job()

    # Main loop with graceful shutdown
    while not shutdown_event.is_set():
        try:
            schedule.run_pending()

            # Sleep in 1-second increments to check shutdown condition
            for _ in range(60):
                if shutdown_event.is_set():
                    logger.info("shutting_down_gracefully")
                    return
                time.sleep(1)

        except Exception as e:
            logger.error("scheduler_loop_error", error=str(e))
            # Even on error, check for shutdown before continuing
            if shutdown_event.is_set():
                logger.info("shutting_down_after_error")
                return
            time.sleep(5)  # Wait a bit before retrying


if __name__ == "__main__":
    main()
