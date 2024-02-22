import codecs
import pathlib
import shutil

import httplib2
from bs4 import BeautifulSoup
from configobj import ConfigObj
from googleapiclient import discovery
from loguru import logger
from markdown2 import Markdown
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

SCOPE = "https://www.googleapis.com/auth/blogger"

CREDENTIAL_STORAGE_DIR = str(pathlib.Path.home().joinpath(".md_to_blog"))
CREDENTIAL_STORAGE_PATH = str(
    pathlib.Path(CREDENTIAL_STORAGE_DIR).joinpath("credential.storage")
)
CONFIG_PATH = str(pathlib.Path(CREDENTIAL_STORAGE_DIR).joinpath("config"))

CLIENT_SECRET = pathlib.Path(CREDENTIAL_STORAGE_DIR).joinpath("client_secret.json")


def extract_article(fn):
    with codecs.open(fn, "r", "utf_8") as fp:
        html = fp.read()
        html = html.replace("<!doctype html>", "")
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select("title")[0].text
        article = soup.select("body")[0]
        return {"title": title, "content": article.prettify()}


def authorize_credentials():

    storage = Storage(CREDENTIAL_STORAGE_PATH)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, storage, http=http)
    return credentials


def get_blogger_service():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = (
        "https://{api}.googleapis.com/$discovery/rest?" "version={apiVersion}"
    )
    service = discovery.build(
        "blogger", "v3", http=http, discoveryServiceUrl=discoveryUrl
    )
    return service


def validate_credential_path():
    target_dir: pathlib.Path = pathlib.Path(CREDENTIAL_STORAGE_DIR)
    if not target_dir.exists():
        target_dir.mkdir()

    target_path: pathlib.Path = pathlib.Path(CREDENTIAL_STORAGE_PATH)
    if not target_path.exists():
        target_path.touch()


def check_config():

    target_path: pathlib.Path = pathlib.Path(CONFIG_PATH)
    if not target_path.exists():
        logger.info("config not exists. it will make new config")
        config = ConfigObj()
        config.filename = str(target_path)
        config["BLOG_ID"] = ""
        config.write()


def set_blogid(value):
    config = ConfigObj(str(pathlib.Path(CONFIG_PATH)))
    config["BLOG_ID"] = value
    config.write()


def get_blogid():
    config = ConfigObj(str(pathlib.Path(CONFIG_PATH)))
    return config["BLOG_ID"]


def set_client_secret(fn):
    shutil.copy(fn, CLIENT_SECRET)


def upload_to_blogspot(title, fn, BLOG_ID):
    validate_credential_path()
    service = get_blogger_service()
    users = service.users()
    thisuser = users.get(userId="self").execute()
    logger.info(
        "This user's display name is: %s" % thisuser["displayName"]
    )  # Changed print to logger
    posts = service.posts()
    with codecs.open(fn, "r", "utf_8") as fp:
        markdowner = Markdown(extras=["highlightjs-lang", "fenced-code-blocks", "html-classes", ""])
        html = markdowner.convert(fp.read())
        payload = {"title": title, "content": html}
        posts.insert(blogId=BLOG_ID, body=payload, isDraft=False).execute()

    # if os.path.exists("output"):
    #     shutil.rmtree("output")
    # os.makedirs("output")
    # basename = os.path.basename(fn)
    # name_body = os.path.splitext(basename)[0]
    # logger.info(f"basename:{basename}")  # Changed print to logger
    # os.system(
    #     f"""generate-md --layout jasonm23-markdown --input {fn} --output output"""
    # )
    # payload = extract_article(os.path.join("output", f"{name_body}.html"))

def upload_html_to_blogspot(title, fn, BLOG_ID):
    validate_credential_path()
    service = get_blogger_service()
    users = service.users()
    thisuser = users.get(userId="self").execute()
    logger.info(
        "This user's display name is: %s" % thisuser["displayName"]
    )  # Changed print to logger
    posts = service.posts()
    with codecs.open(fn, "r", "utf_8") as fp:
        html = fp.read()
        payload = {"title": title, "content": html}
        posts.insert(blogId=BLOG_ID, body=payload, isDraft=False).execute()
