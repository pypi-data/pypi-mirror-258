import sys

import click

from .libs.blogger import (
    check_config,
    get_blogger_service,
    get_blogid,
    set_blogid,
    set_client_secret,
    upload_html_to_blogspot,
    upload_to_blogspot,
)
from .libs.click_order import CustomOrderGroup
from .libs.markdown import convert


@click.command(
    cls=CustomOrderGroup,
    order=[
        "set_blogid",
        "get_blogid",
        "convert",
        "refresh_auth",
        "set_client_secret",
        "publish",
    ],
)
def mdb():
    click.echo("markdown to blogger\nresult:\n\n")


@mdb.command("set_blogid", help="Set the blog ID.1")
@click.argument("blogid")
def run_set_blogid(blogid):
    check_config()
    set_blogid(blogid)


@mdb.command("get_blogid", help="show blog id")
def run_get_blogid():
    check_config()
    print(get_blogid())


@mdb.command("convert", help="마크다운 파일을 html로 변경합니다. ")
@click.option(
    "--input", "-i", "input_", required=True, help="markdown filename to convert"
)
@click.option("--output", "-o", "output_", required=True, help="html filename to save")
def run_convert(input_, output_):
    convert(input_, output_)


@mdb.command("set_client_secret", help="client_secret.json을 저장합니다.")
@click.argument("filename")
def run_set_client_secret(filename):
    set_client_secret(filename)


@mdb.command("refresh_auth", help="구글에 authentication을 refresh 합니다. ")
def run_refresh_auth():
    sys.argv[1] = "--noauth_local_webserver"
    get_blogger_service()


@mdb.command("publish", help="마크다운 파일을 blogger에 발행합니다.")
@click.option("--title", "-t", required=True, help="블로그제목")
@click.argument("filename")
def run_publish(title, filename):
    """Publish Markdown File filename"""
    blog_id = get_blogid()
    upload_to_blogspot(title, filename, blog_id)


@mdb.command("publish_html")
@click.argument("filename")
@click.option("--title", "-t", required=True, help="블로그제목")
def run_publish_html(title, filename):
    blog_id = get_blogid()
    upload_html_to_blogspot(title, filename, blog_id)
