import functools

import click
from rich.table import Table

from app.vk import VkError


def get_table_users(rows: list) -> Table:
    tb = Table()
    tb.add_column('ID')
    tb.add_column('Имя')
    tb.add_column('Можно писать?')
    tb.add_column('URL')

    def get_name(value):
        if value.get('last_name'):
            return f'{value.get("first_name")} {value.get("last_name")}'
        return value.get('first_name')

    def gen_row(v):
        return list(map(str, [
            v['id'],
            get_name(v),
            'Да' if bool(u.get('can_write_private_message')) else 'Нет',
            f'https://vk.com/id{v["id"]}'
        ]))

    for u in rows:
        tb.add_row(*gen_row(u))

    return tb


def get_table_users_topic(rows: list) -> Table:
    tb = Table()
    tb.add_column('ID')
    tb.add_column('Имя')
    tb.add_column('Можно писать?')
    tb.add_column('В группе')
    tb.add_column('URL')

    def get_name(value):
        if value.get('last_name'):
            return f'{value.get("first_name")} {value.get("last_name")}'
        return value.get('first_name')

    def gen_row(v):
        return list(map(str, [
            v['id'],
            get_name(v),
            '[green]Да[/green]' if bool(u.get('can_write_private_message')) else '[red]Нет[/red]',
            '[green]Да[/green]' if bool(u.get('member')) else '[red]Нет[/red]',
            f'https://vk.com/id{v["id"]}'
        ]))

    for u in rows:
        tb.add_row(*gen_row(u))

    return tb


def handle_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except VkError as e:
            click.echo(e)

    return wrapper
