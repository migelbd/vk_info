from typing import Optional

import questionary
import vk_api
from vk_api.vk_api import VkApiMethod


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = questionary.password('Укажите код').ask()
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


class VkAPIError(Exception):
    pass


class VkAPI:

    def __init__(self, login: str, password: str, config_filename='vk_config.v2.json'):
        self._api = None
        self._login = login
        self._pass = password
        self._config_filename = config_filename

    def auth(self):
        vk_session = vk_api.VkApi(
            self._login, self._pass,
            # функция для обработки двухфакторной аутентификации
            auth_handler=auth_handler,
            config_filename=self._config_filename
        )
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        self._api: VkApiMethod = vk_session.get_api()

    @property
    def api(self) -> Optional[VkApiMethod]:
        if self._api:
            return self._api
        raise VkAPIError('API не задано')

    def get_is_member(self, group_id: str, *user_ids):
        res = self.api.groups.isMember(group_id=group_id, user_ids=user_ids)

        return {it.get('user_id'): bool(it.get('member')) for it in res}

    def get_topic_members(self, group_id: str, topic_id: str):
        offset = 0
        count = 100
        comments = self.api.board.getComments(group_id=group_id, topic_id=topic_id, offset=offset, count=count)
        total = comments.get('count')
        items: list = comments.get('items', [])

        if total > 100:
            while (total - offset) > 100:
                offset += 100
                comments = self.api.board.getComments(group_id=group_id, topic_id=topic_id, offset=offset, count=count)
                items.extend(comments.get('items', []))
        return [it.get('from_id') for it in items if not str(it.get('from_id')).startswith('-')]

    def get_user_info(self, *user_ids, **kwargs):
        return self.api.users.get(user_ids=user_ids, fields=kwargs.get('fields', ['can_write_private_message']))

