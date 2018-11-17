"""
Modol odpowiada za symulowane tworzenie struktury katalogow, uruchamianie puli testow
i generowanie danych takich jak: losowy czas działania i reultat testu.
Dane, wraz z nazwą <KATALOG Z LOGAMI> sa zapisywane do pliku <POJEDYŃCZY RAPORT> w katalogu: <POJEDYŃCZA SUITA TESTOWA>

Struktura katalogow:
<all_tests>
-----<POJEDYŃCZA SUITA TESTOWA>
----------<POJEDYŃCZY RAPORT>
----------<KATALOG Z LOGAMI>
...
-----<POJEDYŃCZA SUITA TESTOWA>
----------<POJEDYŃCZY RAPORT>
----------<KATALOG Z LOGAMI>
...

"""


import os
import os.path
import time
from random import randint, choice

SUITE_TESTS_DIR_PREFIX = 'tests_suite'
ROOT_TESTS_DIR = 'all_tests'

class TestResult:
    """Przechowuje dane o rezultacie pojedynczego testu"""

    def __init__(self, id, is_passed, time_spend, log_file_dir='/'):
        self.id = str(id)
        self.is_passed = is_passed
        self.time_spend = str(time_spend)
        self.log_file_dir = log_file_dir

    def __str__(self):
        return self.id + '\t' + self.is_passed + '\t' + self.time_spend + '\t' + self.log_file_dir

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return self.__str__() + str(other)


def get_current_date():
    """ Pobiera aktuala date systemową, uzywana do nazywania katalogow"""

    current_date = time.strftime("%D_%H_%M")
    return current_date.replace('/', '_')

def create_dir(dirname, name):
    """
    Tworzy katalog 'name ' w danym 'dirname'

    :param diname:
    :param name:
    :return new_dir:
    """
    print("dirname " + dirname)
    print("name " + name)
    new_dir = os.path.join(dirname, name)
    try:
        os.stat(new_dir)
    except FileNotFoundError:
        os.mkdir(new_dir)
    return new_dir

def create_suite_tests_dir(dirname, date):
    """
    Tworzy glowny folder przechowywujacy rezultaty wszystkich testow uruchomionych w danej suicie

    :param dirname:
    :param date: Aktualna data systemowa:
    :return dirname: Polozenie folderu do umieszczania w nim danych o puli uruchomionych testow.
    """

    name = SUITE_TESTS_DIR_PREFIX + "__" + date
    return create_dir(dirname, name)

def create_single_test_dir(dirname, id, name):
    """
    Tworzy katalog dla logow z danego testu. Urzytkownik dostaje w raporcie nazwe tego katalogu

    :param dirname:
    :param id:
    :param name:
    :return: dirname:
    """

    name = 'test_' + id + '_runned_at_' + name
    return create_dir(dirname, name)

def create_single_test_log_file(dirname, date):
    """
    Tworzy plik tekstowy raportujacy infomacje o powodzeniu danego testu

    :param dirname:
    :param date:
    :return: new_file_name:
    """

    new_file_name = os.path.join(dirname, str('test_' + date + '.txt'))
    with open(new_file_name, 'w') as f:
        f.writelines("TEST PASSED TIME DIR\n")
    return new_file_name

def update_report_file(file_name, test_result):
    """
    Aktualizuje plik z raportem o dane z kolejnego zakonczonego testu

    :param file_name - nazwa pliku tekstowego, zawierajaca dane o rezultatach danego zestawu testów:
    :param test_resulty -> str; zawiera <id, rezultat, czas, katalog> pojedynczego testu:
    """

    with open(file_name, 'a') as f:
        s2 = test_result + '\n'
        f.writelines(s2)

def launch_single_test(id):
    """
    Symuluje uruchomienie testu o danym 'id'.
    Zwraca zasymulowana informacje o powodzeniu danego testu.

    :param id - Numer testu:
    :return: Obiekt zawierajacy dane o powodzeniu pojedynczego testu.
    """

    print("Info: Running test: " + id)
    dir = '//'
    time_spend = 0
    is_passed = choice([True, False])
    if is_passed:
        time_spend = randint(1, 1000)
    print("Info: Result "+ id + ": " + str(is_passed))
    return TestResult(id, str(is_passed), time_spend, dir)

def launch_tests(tests_to_launch):
    """
    Uruchamia nowy zestaw testow.

    :param tests_to_launch: lista testow do uruchomienia
    """

    current_date = get_current_date()
    curr_dir = os.path.dirname(os.getcwd())
    curr_dir = os.path.join(curr_dir, "Continous-Integration")
    all_tests = os.path.join(curr_dir, ROOT_TESTS_DIR) # curr_dir - powinno sie uruchamiac z ContinousIntegration
    suite_test_dir = create_suite_tests_dir(all_tests, current_date)
    print("INFO: Log files available in: ", suite_test_dir)
    file_name = create_single_test_log_file(suite_test_dir, current_date)
    for id in tests_to_launch:
        id = str(id)
        single_test_dir = create_single_test_dir(suite_test_dir, id, current_date)
        test_result = launch_single_test(id)
        test_result.log_file_dir = single_test_dir
        update_report_file(file_name, test_result)

