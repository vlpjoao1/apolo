import requests


def api_login():
    payload = {
        'username': '0302226873',
        'password': '0302226873',
    }
    headers = {
        'Authorization': 'Token 09fcedfbb892e398b850da5877216cca94a5fe68'
    }
    r = requests.post('http://localhost:8000/api/login/', data=payload, headers=headers)
    if r.status_code == 200:
        items = r.json()
        print(items)
    else:
        print(r.text)


api_login()
