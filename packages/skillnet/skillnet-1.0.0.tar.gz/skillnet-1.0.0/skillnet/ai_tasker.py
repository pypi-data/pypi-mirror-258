class AITaskerClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_job_request(self, job_description):
        # In a real scenario, you would send this to a backend server
        # For demonstration, we'll just print it
        print(f"Sending job request with description: {job_description}")
        return "pending_job_id"  # Simulate a pending job ID response

