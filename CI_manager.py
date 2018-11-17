"""
CI_manager.py:

Program symuluje działanie Continous Integration.
Zarządza pulą testów, które uruchomi, gdy wykryje nowa zmiane w <REPOZYTORIUM> gitowym.
By wygenerowac raport o wszystkich pulach testow nalezy uruchomic skrypt 'report_manager.py'

Wymagane narzędzia:
-Python3

-Flask
	instalacja:
	pip3 install Flask, requests



"""
from time import sleep
from subprocess import Popen, check_output
from github import *
from tests_suite_manager import *

GITHUB_TOKEN = "72faa47f2280b202f8b2b2b7169369b2857138a9"
USERNAME = "Project-temporary-user"
REPOSITORY_NAME = 'watching-repository'

if __name__ == '__main__':
    tests_to_launch = [1, 4, 6, 7, 10, 22, 32, 33, 51]

    token = GITHUB_TOKEN
    username = USERNAME
    controlled_repository = REPOSITORY_NAME
    commit_number = 2

    time_to_wait_for_commits = 30
    delay = 5

    spammer = Popen(['commits_spammer.sh', token, username, controlled_repository, commit_number])
    print("INFO: Started commits generator")

    print("INFO: Creating github session...")
    github_session = create_github_session(GITHUB_TOKEN)
    print("INFO: Created github session")

    timer = 0
    while time_to_wait_for_commits > timer:
        print("INFO: Checking if were introduced new changes on github...")
        commits_date = get_get_dates_of_all_commits_from_github(github_session,
                                                                USERNAME,
                                                                REPOSITORY_NAME,
                                                                GITHUB_TOKEN)
        if is_newer_commit(commits_date):
            print("INFO: Detected new changes. Launching tests.")
            launch_tests(tests_to_launch)
            print("INFO: Finished tests")
        else:
            sleep(delay)
            timer += delay
    print("INFO: Finished waiting for new changes on github")
    spammer.terminate()
    output = check_output(["python", "report_manager.py"])
    print(output)