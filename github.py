"""
Skrypt zwiera wszystkie funkcje potrzebne do pobrania danych z danego <REPOZYTORIUM>, urzytkownika <USER> z github.com

W celu autoryzacji wymagane jest wczesniejsze wygenerowanie tokena w github.com,
by moc zdalnie logowac sie do repozytorium.
"""

__all__ = ['format_date', 'create_github_session', 'get_all_commit_dates', 'is_newer_commit']
import requests
import json
import re

HISTORY_FILE = "commits_history.txt"


class GitConnectionError(Exception): pass


def format_date(commit_date):
    """
    Formatuje dane do formy y-m-dTh:m:sZ

    :param commit_date: Niesformatowana data commitu
    :return: Data po sformatowaniu
    """
    commit_date = re.findall(r'\d+', commit_date)
    return commit_date[:3]


def create_github_session(token):
    """
    Funkcja generuje zapytanie do strony github.com, do określonego <REPOZYTORIUM>, <USER> użytkownika.
    
    :param token:
    :raises GitConnectionError
    :return objekt nawiazanej sesji:
    """
    s = requests.Session()
    g = s.get('https://api.github.com/user', headers={"Authorization": "token " + token})
    if '200' in g.headers['Status']:
        return s
    else:
        raise GitConnectionError


def get_all_commit_dates(session, username, token):
    """
    Na otrzymanym obiekcie session wywoluje zapytanie typu GET.

    W odpowiedzi uzyskuje dane w formacie JSON, o przykładowej zawartości:

    {'sha': '4ea3d3260d921dac85c8b4f3dc31c198e684bb33', 
    'commit': {'author': {'name': 'kamilo116', 'email': 'kamil.sladowski@gmail.com', 'date': '2017-12-02T22:08:52Z'},
    'committer': {'name': 'kamilo116', 'email': 'kamil.sladowski@gmail.com', 'date': '2017-12-02T22:08:52Z'}, 'message': 'created readme',
    'tree': {'sha': 'a555d0f851d5f531d3769094abcf3f7aa3661728', 'url': 'https://api.github.com/repos/kamilo116/tmp-repo/git/trees/a555d0f851d5f531d3769094abcf3f7aa3661728'},
    'url': 'https://api.github.com/repos/kamilo116/tmp-repo/git/commits/4ea3d3260d921dac85c8b4f3dc31c198e684bb33', 'comment_count': 0,
    'verification': {'verified': False, 'reason': 'unsigned', 'signature': None, 'payload': None}},

    'url': 'https://api.github.com/repos/kamilo116/tmp-repo/commits/4ea3d3260d921dac85c8b4f3dc31c198e684bb33',
    'html_url': 'https://github.com/kamilo116/tmp-repo/commit/4ea3d3260d921dac85c8b4f3dc31c198e684bb33',
    'comments_url': 'https://api.github.com/repos/kamilo116/tmp-repo/commits/4ea3d3260d921dac85c8b4f3dc31c198e684bb33/comments',
    'author': {'login': 'kamilo116', 'id': 8524812,  ...}

    Z każdegu uzyskanego w ten sposób commitu potrzeba wyciągnąć datę, przez odwołanie do:
    [commit']['author']['date']


    :param session: Sesja nawiazana z repozytorium githabowym danego uzytkownika
    :param username: Nazwa uzytkownika, do ktorego nalezy dane repozytorium
    :param token: Token uwierzytelniajacy
    :return: Lista z datami wszystkich commitow danego repozytorium
    """
    commits = session.get('https://api.github.com/repos/' + username + '/tmp-repo/commits',
                          headers={"Authorization": "token " + token})
    all_commit_dates = []
    commits_json_data = json.loads(commits.text)
    for next_commit in commits_json_data:
        all_commit_dates.append(next_commit['commit']['author']['date'])
    return all_commit_dates


def is_newer_commit(all_commit_dates) -> bool:
    """
    Wybiera z listy commitow (all_commit_dates) daty, ktore sa wieksze od tej zapisanej w HISTORY_FILE.
    Jezeli znajdzie takie daty, to funkcja zwraca True.

    :param all_commit_dates: Daty wszystkich commitow.
    :return: Informacja o wystapieniu nowych commitow.
    """
    with open(HISTORY_FILE, 'r') as f:
        last_commit_date = f.readline()
        print("INFO: Last remembered commit's date: ", last_commit_date)
        all_commit_dates = list(filter(lambda d: d > last_commit_date, all_commit_dates))
        try:
            last_commit_date = all_commit_dates[0]
            print("INFO: After {0} was new commit: {1}".format(last_commit_date, last_commit_date))
            with open(HISTORY_FILE, 'w') as f:
                f.write(last_commit_date + '\n')
            return True
        except IndexError:
            print("WARNING: There hasn't been any commits since ", last_commit_date)
        return False
