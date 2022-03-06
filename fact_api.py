from pprint import pprint
from engine import decorators
from typing import Dict, AnyStr


class RequestsDispatcher:
    @staticmethod
    @decorators.get_request_wrapper
    def list_users() -> Dict:
        """
        iterate over response, per page until reached end-of-list
        :return Response
        """
        pass

    @staticmethod
    @decorators.get_request_wrapper
    def get_user_by_id(user_id: AnyStr) -> Dict:
        """
        :param user_id: string
        :return: dict of user-data
        """
        pass

    @staticmethod
    @decorators.post_request_wrapper
    def login_user(email: AnyStr, password: AnyStr) -> Dict:
        """
        :param email: string
        :param password: string
        :return: post request w/ successful token
        """
        pass

    @staticmethod
    @decorators.post_request_wrapper
    def update_user_data(user_id: AnyStr, data: Dict):
        """
        :param user_id: string
        :param data: dict
        :return:
        """
        pass

    @staticmethod
    @decorators.get_request_wrapper
    def get_user_avatar(self, user_id):
        """
        :param self:
        :param user_id:
        :return:
        """
        pass


if __name__ == '__main__':
    a = RequestsDispatcher()
    pprint(a.get_user_by_id(user_id='1'))
    pprint(a.get_user_by_id(user_id='2'))

    counter = 1
    res = a.get_user_by_id(user_id='1')
    while res.get('user_data', None):
        pprint(res)
        counter += 1
        res = a.get_user_by_id(user_id=str(counter))

    # pprint(RequestsDispatcher().get_user_avatar())
    print(a.login_user(email='eve.holt@reqres.in', password='cityslicka'))
    print(a.login_user(email='eve.holt@req1res.in', password='cityslicka'))
