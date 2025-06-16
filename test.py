import requests

print(
    requests.post(
        "http://localhost:8000/tier",
        json={"game_name": "Hide On Bush", "tag_line": "KR1"},
    ).json()
)
