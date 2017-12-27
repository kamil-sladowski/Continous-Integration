"""
CI.py:

Program symuluje działanie Continous Integration.
Zarządza pulą testów, które uruchomi, gdy wykryje nowa zmiane w <REPOZYTORIUM> gitowym.
By wygenerowac raport o wszystkich pulach testow nalezy uruchomic skrypt 'report_manager.py'

Wymagane narzędzia:
-Python3

-Flask
	instalacja:
	pip3 install Flask


"""
__all__ = ['GITHUB_TOKEN', 'USERNAME']
from github import *
from report_manager import *
from tests_suite_manager import *
from report_manager import *

GITHUB_TOKEN = "0062fd369d696c70223ef271d3997a90c5d5987a"
USERNAME = "kamilo116"

if __name__ == '__main__':
    tests_to_launch = [1, 4, 6, 7, 10, 22, 32, 33, 51]
    print("INFO: Creating github session...")
    github_session = create_github_session(GITHUB_TOKEN)
    print("INFO: Created github session")
    all_commit_dates = get_all_commit_dates(github_session, USERNAME, GITHUB_TOKEN)
    if is_newer_commit(all_commit_dates):
        launch_tests(tests_to_launch)
        print("INFO: Finished tests")

