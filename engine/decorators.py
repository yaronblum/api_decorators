import requests
from pprint import pprint
from typing import Dict
from engine import exceptions


request_config: Dict = {
    "base_api": "https://reqres.in/api/",
    "urls": {
            "list_users": "users?page={}",
            "login_user": "login",
    }
}

# updating request_config w/ keys sharing the same value
request_config['urls'].update(dict.fromkeys({
    "get_user_by_id", "get_user_by_name", "get_user_by_avatar"
}, 'users/{}'))


def get_request_wrapper(func):
    def _handle_request(args):
        response = requests.get(''.join([
            request_config['base_api'],
            request_config['urls'][func.__name__].format(args)
        ]))

        return response

    def _handle_list_user_request():
        counter = 1
        timeout = 5

        while counter <= timeout:

            response = _handle_request(args=counter)

            if not response.json().get('data', None):
                break

            func.__dict__[f'page_number_{counter}'] = response.json()['data']

            counter += 1

    def _handle_get_user_id_request(_user_id):
        response = _handle_request(_user_id)

        if response.status_code == 404:
            func.__dict__[response.status_code] = response.reason

        else:
            func.__dict__['user_data'] = response.json()['data']
            response = _handle_request(_user_id)

            if response.status_code == 404:
                func.__dict__[response.status_code] = response.reason

            else:
                func.__dict__['user_data'] = response.json()['data']

    def inner_wrapper(*args, **kwargs):
        func.__dict__.clear()

        if func.__name__ == 'list_users':
            _handle_list_user_request()

        elif func.__name__ in ('get_user_by_id', 'get_user_avatar'):

            _user_id = kwargs.get('user_id', None)
            _handle_get_user_id_request(_user_id=_user_id)

        return func.__dict__

    return inner_wrapper


def post_request_wrapper(func):
    def _request_handler(user_id=None):
        _function_data = {
            'login': request_config['urls'][func.__name__],
            'update_user_data': request_config['urls'][func.__name__].format
        }

        if func.__name__ == 'update_user_data':
            if not user_id:
                raise exceptions.BadPostRequestParams()

        return request_config['urls'][func.__name__].format(user_id)

    def inner_wrapper(*args, **kwargs):
        request_data = dict()
        user_id = kwargs.get('user_id', None)

        if func.__name__ == 'login_user':
            request_data = {
                "email": kwargs.get('email'),
                "password": kwargs.get('password')
            }

        elif func.__name__ == 'update_user_data':
            request_data = kwargs.get('data', None)

        response = requests.post(
            ''.join([request_config["base_api"], _request_handler(user_id=user_id)]),
            data=request_data
        )

        func.__dict__ = response.json()

        return func.__dict__

    return inner_wrapper
