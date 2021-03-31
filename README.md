# Konsola Operatorska

## Przygotowanie środowiska
### Moduły
Aplikacja wymaga zainstalowanego pythona3, testowana była na wersjach 3.8.5 oraz 3.8.8, odpowiednio na Ubuntu i Windows 7.
Do poprawnego działania wymagane będą też poniższe moduły:
- tkinter oraz tkinter.messagebox
- json
- requests

Zwykle są one instalowane razem z pythonem, ale zdarzają się wyjątki.
#### Ubuntu
Ubuntu nie wymaga instalacji pythona, ponieważ język instalowany jest wraz z systemem.
Może być wymagana osobna instalacja modułów tkinter oraz requests. Jednym ze sposobów jest użycie package managera pip:
```bash
  apt install python3-pip
  pip3 install tk
  pip3 install requests
```
Alternatywnie:
```bash
  apt install python-tk
  apt install python-requests
```
#### Windows 7
Instalacja pythona na Windowsie może przebiegać na wiele sposobów. Najlepiej zacząć [tutaj](https://www.python.org/downloads/ "Download Python").
Wersja 3.6 i nowsze zawierają wszystkie potrzebne moduły, dlatego nie trzeba ich instalować.

### Symulator
Aplikacja pozwala na wpisanie własnego adresu, z którego uzyskiwany będzie plik JSON, pod warunkiem, że będzie w formacie podobnym do tego w udostępnionym symulatorze testowym.

## Pobranie i uruchomienie aplikacji
Repozytorium można pobrać z githuba jako plik .zip lub używając gita:
```bash
  git clone "https://github.com/rambo42/op_console.git"
```
Którego można pobrać i zainstalować [stąd](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Ważne jest aby pliki op_console.py, godclass_n_aux.py i folder icons wszystkie znajdowały się w tym samym folderze.

Teraz wystarczy przygotwać preferowane źródło danych i uruchomić plik op_console.py.
Na Windowsie wystarczy kliknąć na plik w eksploratorze, na Ubuntu moża uruchomić go w terminalu za pomocą komendy
```bash
  python3 op_console.py
```
po przejściu do katalogu zawierającego pliki.

Aplikacja umożliwia sprecyzowanie adresu, z którego pochodzą dane oraz sortowania po cechach urządzeń.
Ze względu na ograniczenia tkintera pod względem renderowania plików html nie było możliwe załączenie mapy zachowując wybraną architekturę.

## Credits
Ikony pochodzą z thenounproject.com

Attribution:
- voice by Andrejs Kirma from the Noun Project
- signal by nopixel from the Noun Project
- station by ghayn from the Noun Project
- Car by agus raharjo from the Noun Project
- Phone by Silviu Ojog from the Noun Project
- Car by Adrien Coquet from the Noun Project
- loading by DinosoftLab from the Noun Project
- terminal by Free Icons from the Noun Project

Icons were cropped as permitted by the use license
