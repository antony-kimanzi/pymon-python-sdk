import time
from pymon import monitor

# NOTE: Put the ping token from your Postman test here!
# (You can copy it from your Spring Boot database or Postman response)
import os
os.environ["PYMON_API_KEY"] = "6sFUMQbpiMlNSX4_tF_yp3TrT8fX3-_fVLxEAUQXSMo"

# 2. Make sure the base URL is correct
os.environ["PYMON_API_BASE_URL"] = "http://localhost:8080/api/v1"


@monitor("my-test-job")
def successful_job():
    print("Running successful job...")
    time.sleep(1)  # Simulate some work
    print("Job complete!")


@monitor("my-test-job")
def failing_job():
    print("Running failing job...")
    time.sleep(1)
    # Simulate a database failure
    raise ConnectionError("Could not connect to the database server")


if __name__ == "__main__":
    print("--- Testing Success ---")
    successful_job()

    print("\n--- Testing Failure ---")
    try:
        failing_job()
    except Exception as e:
        print(f"Caught expected error: {e}")
