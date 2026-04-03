import requests
import os
from collections import defaultdict

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = os.environ["GITHUB_USER"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# средняя длина строки (можешь менять)
AVG_CHARS_PER_LINE = 40

def get_repos():
    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner"
        r = requests.get(url, headers=HEADERS)
        data = r.json()

        if not data:
            break

        repos.extend(data)
        page += 1

    return repos


def get_languages(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/languages"
    r = requests.get(url, headers=HEADERS)
    return r.json()


def main():
    repos = get_repos()
    totals = defaultdict(int)

    for repo in repos:
        langs = get_languages(repo["full_name"])

        for lang, bytes_ in langs.items():
            totals[lang] += bytes_

    # перевод в строки
    result = {}
    for lang, bytes_ in totals.items():
        lines = bytes_ // AVG_CHARS_PER_LINE
        result[lang] = lines

    # сортировка
    sorted_langs = sorted(result.items(), key=lambda x: x[1], reverse=True)

    # генерация markdown
    output = "## 📊 My Code Stats\n\n"
    for lang, lines in sorted_langs:
        output += f"- {lang}: {lines:,} lines\n"

    # запись
    with open("LANG_STATS.md", "w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
