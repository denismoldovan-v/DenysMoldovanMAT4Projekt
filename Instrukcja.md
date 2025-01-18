
## Przewodnik instalacji wymaganych narzędzi

### Wymagane biblioteki

Kod wymaga następujących bibliotek:

- `collections` (wbudowana w Pythona, nie wymaga instalacji)
- `matplotlib`
- `pandas`

### Instalacja bibliotek

Aby zainstalować wymagane biblioteki, należy wykonać poniższe kroki:

#### Krok 1: Upewnienie się, że Python jest zainstalowany

1. Pobrać Pythona z oficjalnej strony: [https://www.python.org/](https://www.python.org/)
2. Zainstalować Pythona, wybierając opcję "Add Python to PATH" podczas instalacji.

#### Krok 2: Instalacja biblioteki `matplotlib`

1. Otworzyć terminal (lub wiersz poleceń).
2. Wpisać poniższą komendę i nacisnąć Enter:
   ```
   pip install matplotlib
   ```

#### Krok 3: Instalacja biblioteki `pandas`

1. W terminalu wpisać następującą komendę:
   ```
   pip install pandas
   ```

### Weryfikacja instalacji

Po zakończeniu instalacji można sprawdzić, czy biblioteki zostały zainstalowane poprawnie. W tym celu należy wykonać następujące kroki:

1. Otworzyć terminal lub wiersz poleceń.
2. Uruchomić interpreter Pythona, wpisując:
   ```
   python
   ```
3. W Pythonie wpisać poniższe polecenia:
   ```python
   import matplotlib
   import pandas
   ```
4. Jeśli nie pojawią się żadne błędy, instalacja została przeprowadzona pomyślnie.

### Uwagi końcowe

Jeśli podczas instalacji pojawią się błędy, należy upewnić się, że:

- Zainstalowana jest najnowsza wersja Pythona.
- `pip` (menedżer pakietów Pythona) działa poprawnie. Można zaktualizować `pip`, wpisując:
  ```
  python -m pip install --upgrade pip
  ```

Jeśli pojawiają się jakiekolwiek pytania lub są problemy, warto sprawdzić dokumentację na [https://pip.pypa.io/](https://pip.pypa.io/).
