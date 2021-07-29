
def test_login(app):
    app.login("administrator", "root")
    assert app.is_logged_in_as("администратор")