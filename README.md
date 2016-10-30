# mobilität finden

Das Projekt mobilität finden ist auf [mobilitaet-finden.de](https://mobilitaet-finden.de/) zu finden.

# Eingesetzte Software

mobilität ist eine WSGI-Applikation mit folgenden Komponenten:
- Flask
- Python
- ElasticSearch
- MySQL
- Gulp
- Bower
- npm

Die Applikation wird via gunicorn, Nginx und supervisord bereitgestellt.

# Zusätzliche Importmodule

Um weitere Daten in die Plattform zu integrieren, muss ein weiteres Importmodul im Ordner /sync angelegt werden. Die Identifikation erfolgt über das Datenbankfeld `slug`.