# koda-ans

Implementacja bezstratnego kodeka Asymmetric Numeral Systems (rANS).  
Projekt demonstruje praktyczne zastosowanie kodowania entropijnego oraz analizy statystycznej danych.

---

## Opis projektu

Celem projektu jest implementacja algorytmu range Asymmetric Numeral Systems (rANS) służącego do bezstratnej kompresji danych.  
Program umożliwia kodowanie i dekodowanie obrazów w skali szarości (format PGM), wykorzystując model statystyczny budowany bezpośrednio na podstawie danych wejściowych.

Projekt zawiera również narzędzia do:
- obliczania entropii Shannona,
- analizy rozkładów symboli za pomocą histogramów,
- weryfikacji poprawności kodowania i dekodowania.

---

## Opis algorytmu

Algorytm rANS koduje dane w postaci pojedynczego stanu liczbowego, który jest aktualizowany dla kolejnych symboli na podstawie modelu statystycznego.

Parametry algorytmu:
- N – rozmiar przedziału (liczba bitów),
- R – próg renormalizacji stanu.

Funkcja kodująca:
C(x, s) = floor(x / f(s)) · 2^N + (x mod f(s)) + cdf(s)

Funkcja dekodująca:
D(x', s) = f(s) · floor(x' / 2^N) + (x' mod 2^N) − cdf(s)

Renormalizacja stosowana jest zarówno podczas kodowania, jak i dekodowania, aby utrzymać stan w bezpiecznym zakresie liczbowym.

---

## Wymagania

- Python 3.x  
- NumPy  
- Pillow (PIL)  

Opcjonalnie (wyświetlanie postępu działania programu):  
pip install tqdm

---

## Uruchamianie programu

Uruchom aplikację poleceniem:  
python3 main.py

Następnie:
1. Wybierz tryb działania:
   - 1 – koder (kompresja),
   - 2 – dekoder (dekompresja).
2. Podaj nazwę pliku znajdującego się w katalogu:
   ./data/obrazy_testowe

---

## Dane wyjściowe

Kodowanie generuje plik z rozszerzeniem .rans, który zawiera:
- sygnaturę formatu,
- częstości symboli,
- rozmiar oryginalnych danych,
- nagłówek obrazu,
- zakodowany strumień danych.

Dekodowanie odtwarza oryginalny plik .pgm.

Program automatycznie sprawdza poprawność rekonstrukcji poprzez porównanie plików bit-po-bicie.

---

## Testy

Testy entropii – obliczanie entropii Shannona dla danych syntetycznych oraz obrazów testowych:  
python3 -m tests.entropy_tests

Testy histogramów – generowanie i analiza histogramów rozkładów symboli:  
python3 -m tests.histogram_tests

Wygenerowane obrazy histogramów zapisywane są w katalogu:  
tests/outputs/

---

## Struktura projektu

koda-ans/
├── data/                 – dane wejściowe (obrazy i rozkłady testowe)  
├── entropy/              – implementacja entropii Shannona  
├── histogram/            – generowanie histogramów  
├── model/                – model statystyczny rANS  
├── tests/                – testy i analiza  
│   └── outputs/          – wygenerowane histogramy  
├── encoder_rans.py       – koder rANS  
├── decoder_rans.py       – dekoder rANS  
├── main.py               – punkt wejścia aplikacji  
└── README.md  

---

## Uwagi końcowe

- Implementacja realizuje bezstratną kompresję danych.  
- Dane po dekodowaniu są identyczne z danymi wejściowymi.  
- Analiza entropii i histogramów potwierdza zgodność wyników z teorią informacji.
