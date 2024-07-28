import requests
import json
import base64

# Thanks to Google btw ^^
def text_to_base64(text):
    text_bytes = text.encode('utf-8')
    base64_bytes = base64.b64encode(text_bytes)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def GetSha(token, owner, repo, path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        Sha = data["sha"]
        return Sha
    else:
        print(f'Error: {response.status_code}')
        print(response.json())

def GetContent(token, owner, repo, path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        RawLink = data["download_url"]
        content = requests.get(RawLink)
        return content
    else:
        print(f'Error: {response.status_code}')
        print(response.json())

def CreateFile(token, owner, repo, path, content):

    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    payload = {
        'message': "Commit by Python",
        'committer': {
            'name': "Python",
            'email': "NONE"
        },
        'content': text_to_base64(content)
    }

    print(payload)

    response = requests.put(url, headers=headers, data=json.dumps(payload))

    if response.status_code in [200, 201]:
        data = response.json()
        print(data)
    else:
        print(f'Error: {response.status_code}')
        print(response.json())

def UpdateFile(token, owner, repo, path, content):
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        data = {
            "message": "Update by Python",
            "committer": {
                "name": "Python",
                "email": "NONE"
            },
            "content": text_to_base64(content),
            "sha": GetSha(token, owner, repo, path)
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))

        print(response.status_code)
        print(response.json())

token = 'YOUR_TOKEN_HERE' # Your API Token -> https://github.com/settings/tokens/new (select repo, project)
owner = 'NtReadVirtualMemory' # Your Name
repo = 'Testing-Shit' # Repo Name
path = 'Test_Final_File' # Name of your File

GetContent(token, owner, repo, path)
CreateFile(token, owner, repo, path, "Hello")
UpdateFile(token, owner, repo, path, "Hello2")
