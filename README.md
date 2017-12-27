# Continous-Integration

Program symuluje działanie Continous Integration.
Zarządza pulą testów, które uruchomi, gdy wykryje nowa zmiane w <REPOZYTORIUM> gitowym danego <USERNAME>.
Następnie drugim skryptem można wygenerować raport w .html z informacją o zachowaniu ostatniej puli, względem poprzednich.



# Uruchomienie nowej puli testow skryptem:
CI.py


# Wygenerownie raportu o wszystkich pulach testow skryptem:
report_manager.py


# Ustawienia własne:
By obserwować inne repozytorium pod kątem nowych zmian należy w pliku CI.py podać nowy USERNAME, REPOSITORY_NAME i GITHUB_TOKEN.
  Wygenerowanie githubowego tokena:
  https://github.com/settings/tokens
  
  
 # Wymagane narzędzia:
-Python3
-Flask
 instalacja:
 pip3 install Flask
	


# Szczególowa dokumentacja poszczególnych funkcji znajduje się w plikach .html:
CI.html,
github.html,
report_manager.html,
tests_suite_manager.html
