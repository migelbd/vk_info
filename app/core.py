import os
from collections import defaultdict

import click
import profig
import questionary
from click import Context
from rich.console import Console
from rich.table import Table

from app.helper import get_table_users, get_table_users_topic, handle_error
from app.vk import VkAPI

console = Console()

HOME_PATH = os.getenv('USERPROFILE') or os.getenv('HOME')

CFG_PATH = os.path.join(HOME_PATH, '.redmine.cfg')
CFG_VK_PATH = os.path.join(HOME_PATH, 'vk_config.v2.json')
cfg = profig.Config(CFG_PATH, encoding='utf-8')

cfg.init('vk.login', '')
cfg.init('vk.password', '')


@click.group('VkCli')
@click.pass_context
def cli(ctx: Context):
    ctx.ensure_object(dict)
    cfg.sync()
    if cfg.get('vk.login'):
        api = VkAPI(cfg.get('vk.login'), cfg.get('vk.password'), config_filename=CFG_VK_PATH)
        api.auth()
        ctx.obj['api'] = api
    else:
        ctx.obj['api'] = None


@cli.command()
def login():
    config_data = defaultdict(lambda: "")
    config_data['vk.login'] = questionary.text('Укажите логин').ask()
    config_data['vk.password'] = questionary.password('Укажите пароль').ask()

    cfg.update(config_data.items())
    cfg.sync()

    VkAPI(cfg.get('vk.login'), cfg.get('vk.password'), config_filename=CFG_VK_PATH).auth()


@cli.command()
@click.argument('user_id')
@click.pass_context
def user(ctx, user_id):
    api: VkAPI = ctx.obj['api']
    if not api:
        click.echo('API не инициализировано')

    users = api.get_user_info(user_id)

    console.print(get_table_users(users))


@cli.command()
@click.argument('topic_url')
@click.option('-n', '--not-in-group', is_flag=True)
@click.pass_context
@handle_error
def topic(ctx, topic_url, not_in_group):
    api: VkAPI = ctx.obj['api']
    if not api:
        click.echo('API не инициализировано')
    tp = str(topic_url).split('/')[-1]
    group_id, topic_id = tp.replace('topic-', '').split('_')

    user_ids = api.get_topic_members(group_id, topic_id)

    res = api.get_is_member(group_id, *user_ids)
    user_info = api.get_user_info(*user_ids)
    rows = []
    for u in user_info:
        rows.append({
            **u,
            'member': res.get(u.get('id'))
        })
    if not_in_group:
        console.print(get_table_users_topic([r for r in rows if not r.get('member')]))
    else:
        console.print(get_table_users_topic(rows))

