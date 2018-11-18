
"""
This project is a simulator, which trigger launching tests, when detects new changes on github repository.
After that, it takes results from those and previous 5 last runned test suites and generates report in html.

Every suite of tests generates on the end the .txt files with summary with single results.
(The tests are faked and results generated randomly - The goal of project was to implement only flow - how detect
changes and, collect final report and present in a readable way).
"""


from time import sleep
from subprocess import Popen, check_output
from github import *
from tests_suite_manager import *

GITHUB_TOKEN = "bc97f583fd2f18d81ddbacd5eadd6b8e7fa5b693"
USERNAME = "Project-temporary-user"
REPOSITORY_NAME = 'watching-repository'

if __name__ == '__main__':
    tests_to_launch = [1, 4, 6, 7, 10, 22, 32, 33, 51]
    spammer_file = 'commits_spammer.sh'
    token = GITHUB_TOKEN
    username = USERNAME
    controlled_repository = REPOSITORY_NAME
    commit_number = '2'

    time_to_wait_for_commits = 30
    delay = 5

    spammer = Popen([spammer_file, token, username, controlled_repository, commit_number], shell = True,
              stdin = None, stdout = None, stderr = None, close_fds = True)
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