from wsgiref.util import request_uri
import requests
import time

# vars: api endpoint
api_endpoint = "https://notify-api.line.me/api"

def check_line_notify_request(request_headers):
    """ LINE Notify 利用可否検証 API """

    request_url = f'{api_endpoint}/status'

    try:
        response = requests.get(request_url, headers=request_headers)
        response.raise_for_status() # If status code is other than 200, flush to exception handling

    except requests.exceptions.RequestException as e:
        print("RequestException for check_line_notify_request. ", e)

    except Exception as e:
        print("An unexpected error occurred while processing 'check_line_notify_request'.", e)

    else:
        print("'check_line_notify_request' was successfully processed.")

    finally:
        print(response.json())
        return response.status_code


def send_line_notify(request_headers, notification_message, file_list):
    """ LINE 通知 API """

    request_uri = f'{api_endpoint}/notify'
    request_body = {'message': f'message: {notification_message}'}

    try:
        for file_name in file_list:
            image_convert_dict = {"imageFile": open(f'./data/{file_name}', mode="rb")} # Image file reading -> binaryization -> dictionary format conversion
            response = requests.post(request_uri, headers=request_headers, data=request_body, files=image_convert_dict)
            response.raise_for_status()
            print(f'send: ./data/{file_name}')
            time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print("RequestException for send_line_notify. ", e)
        for file_name in file_list:
            print("[debug:send_line_notify]", file_name, e.args, e.request, e.response)

    except Exception as e:
        print("An unexpected error occurred while processing 'send_line_notify'.", e)

    else:
        print("'send_line_notify' was successfully processed.")

    finally:
        print(response.json())
        return response.status_code
