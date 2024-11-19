import os

# api basic
line_notify_token = os.environ["LINE_NOTIFY_TOKEN"]
request_headers = {'Authorization': f'Bearer {line_notify_token}'}
http_status_success = 200

# utils
file_list = os.listdir(path="./data")
send_message = "test message from python."