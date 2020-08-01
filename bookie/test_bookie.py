from bookie import app

# def test_create():
#     response = app.test_client().post('/bookie', data=dict(
#         text="create --quantity 100 --unit karma",
#         user_id="",
#         user_name="jonah",
#         response_url="",
#     ))
#     assert response.status_code == 200
#     assert response.data == b'Hello, World!'

# def test_help():
#     response = app.test_client().post('/bookie', data=dict(
#         text="help",
#         user_id="",
#         user_name="jonah",
#         response_url="",
#     ))
#     assert response.status_code == 200
#     assert response.data == b'Hello, World!'

def test_unknown():
    response = app.test_client().post('/bookie', data=dict(
        text="help",
        user_id="U",
        user_name="jonah",
        response_url="",
    ))
    assert response.status_code == 200
    assert response.data == b'Hello, World!'
