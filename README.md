# Continous-Integration

Program symuluje działanie Continous Integration.
Zarządza pulą testów, które uruchomi, gdy wykryje nowa zmiane w <REPOZYTORIUM> gitowym danego <USERNAME>.



### Uruchomienie nowej puli testow skryptem:
CI.py


### Wygenerownie raportu o wszystkich pulach testow skryptem:
report_manager.py


### Ustawienia własne:
By obserwować inne repozytorium pod kątem nowych zmian należy w pliku CI.py podać nowy USERNAME, REPOSITORY_NAME i GITHUB_TOKEN.
  Wygenerowanie githubowego tokena:
  https://github.com/settings/tokens
  
  
 ### Wymagane narzędzia:
-Python3
-Flask
-requests

 instalacja:
 pip install --upgrade -r requirements.txt
	


