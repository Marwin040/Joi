import requests

def log_user(url):
    r = requests.get(url)

    # Check the status code
    if r.status_code == 200:
        try:
            # Attempt to decode the JSON response
            hey = r.json().get("cnt")
            print("Count:", hey)
        except ValueError:
            print("Response content is not valid JSON.")
            print("Response text:", r.text)
    else:
        print(f"Error: Received status code {r.status_code}")
        print("Response text:", r.text)

# Example usage
log_user("chatbot_logging.py")
