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
        return "???"

def FileExist(owner, repo, path):
        url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/{path}'

    
        response = requests.get(url)

        if response.status_code == 200:
            return True
        else:
            return False

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
        return content.text or content.content
    else:
        print(f'Error: {response.status_code}')
        print(response.json())
        return "FILE_DOES_NOT_EXIST_OR_IS_UNKNOWN"

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

    response = requests.put(url, headers=headers, data=json.dumps(payload))

    if response.status_code in [200, 201]:
        return True
    else:
        print(f'Error: {response.status_code}')
        print(response.json())
        return False

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

        if response.status_code == 200:
            return True
        else:
            return False

def AddLine(token, owner, repo, path, content):

    oldcon = GetContent(token, owner, repo, path)

    if oldcon:
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
            "content": text_to_base64(oldcon + "\n" + content),
            "sha": GetSha(token, owner, repo, path)
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return True
        else:
            return False


token = 'YOUR_TOKEN_HERE' # Your API Token -> https://github.com/settings/tokens/new (select repo, project)
owner = 'NtReadVirtualMemory' # Your Name
repo = 'Testing-Shit' # Repo Name
path = 'FinalTestIG' # Name of your File

print("Create File")
CreateFile(token, owner, repo, path, "Hello")
print("File Exist:", FileExist(owner, repo, path))
print("Get Content")
GetContent(token, owner, repo, path)
print("Updating...")
UpdateFile(token, owner, repo, path, "Hello2")
print("Adding Line...")
AddLine(token, owner, repo, path, "LOL")
print("Done!")
