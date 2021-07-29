import json
import ftputil
import pytest
from application import Application

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        with open(file) as f:
            target = json.load(f)
    return target

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

#@pytest.fixture(scope = "session")
@pytest.fixture
def app(request):
    global fixture

    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        cur_url = target["web"]["baseUrl"]
        fixture = Application(browser=browser, base_url=target["web"]["baseUrl"])
    return fixture

@pytest.fixture(scope="session", autouse=True)
def configue_server(request,config):
    install_server_configuration(target['ftp']['host'], target['ftp']['username'], target['ftp']['password'])
    def fin():
        restore_server_configuration(target['ftp']['host'], target['ftp']['username'], target['ftp']['password'])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            remote.remove("config_defaults_inc.php")
        if remote.path.isfile("config_defaults_inc.php"):
            remote.rename("config_defaults_inc.php", "config_defaults_inc.php.bak")
        remote.upload("resources/config_defaults_inc.php", "config_defaults_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            if remote.path.isfile("config_defaults_inc.php"):
                remote.remove("config_defaults_inc.php")
            remote.rename("config_defaults_inc.php.bak", "config_defaults_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
