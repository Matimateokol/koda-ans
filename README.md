# koda-ans

Implementacja bezstratnego kodeka Asymmetric Numeral Systems (rANS).  
Projekt demonstruje praktyczne zastosowanie kodowania entropijnego oraz analizy statystycznej danych, łącząc zagadnienia teoretyczne z zakresu teorii informacji z praktyczną implementacją algorytmu kompresji.

---

## Opis projektu

Celem projektu jest implementacja algorytmu range Asymmetric Numeral Systems (rANS), który służy do bezstratnej kompresji danych. rANS jest nowoczesną metodą kodowania entropijnego, oferującą bardzo dobrą skuteczność kompresji przy jednoczesnym zachowaniu relatywnie prostej struktury obliczeniowej.

Program umożliwia kodowanie i dekodowanie obrazów w skali szarości zapisanych w formacie PGM. Wykorzystany w projekcie model statystyczny nie jest narzucony z góry, lecz budowany dynamicznie na podstawie danych wejściowych. Takie podejście pozwala na lepsze dopasowanie procesu kodowania do rzeczywistego rozkładu symboli w danych.

Projekt zawiera również narzędzia do:
- obliczania entropii Shannona w celu analizy teoretycznej granicy kompresji,
- analizy rozkładów symboli za pomocą histogramów,
- weryfikacji poprawności kodowania i dekodowania poprzez porównanie danych wejściowych i wyjściowych.

---

## Opis algorytmu

Algorytm rANS koduje dane w postaci pojedynczego stanu liczbowego, który jest aktualizowany dla kolejnych symboli na podstawie modelu statystycznego. Każdy symbol jest mapowany na odpowiedni przedział liczbowy zgodnie z jego częstością występowania oraz dystrybuantą skumulowaną.

Parametry algorytmu:
- N – rozmiar przedziału, określający liczbę bitów wykorzystywanych w operacjach modulo,
- R – próg renormalizacji stanu, zapewniający stabilność obliczeń.

Funkcja kodująca:
C(x, s) = floor(x / f(s)) · 2^N + (x mod f(s)) + cdf(s)

Funkcja dekodująca:
D(x', s) = f(s) · floor(x' / 2^N) + (x' mod 2^N) − cdf(s)

Renormalizacja stosowana jest zarówno podczas kodowania, jak i dekodowania. Jej celem jest utrzymanie stanu w bezpiecznym zakresie liczbowym oraz zapewnienie jednoznaczności procesu odwrotnego.

---

## Wymagania

Do uruchomienia projektu wymagany jest interpreter Python w wersji 3.x oraz biblioteki NumPy i Pillow (PIL), które wykorzystywane są odpowiednio do obliczeń numerycznych oraz obsługi obrazów.

- Python 3.x  
- NumPy  
- Pillow (PIL)  

Opcjonalnie, w celu wyświetlania informacji o postępie przetwarzania danych, można zainstalować bibliotekę tqdm:  
pip install tqdm

---

## Uruchamianie programu

Program uruchamiany jest z poziomu konsoli poleceniem:  
python3 main.py

Po uruchomieniu aplikacji użytkownik wybiera tryb działania programu:
1. Wybierz tryb działania:
   - 1 – koder (kompresja),
   - 2 – dekoder (dekompresja).
2. Podaj nazwę pliku znajdującego się w katalogu:
   ./data/obrazy_testowe

Program prowadzi użytkownika krok po kroku przez proces kodowania lub dekodowania danych.

---

## Dane wyjściowe

W wyniku kodowania generowany jest plik z rozszerzeniem .rans, który zawiera wszystkie informacje niezbędne do poprawnego przeprowadzenia procesu dekodowania.

Kodowanie generuje plik z rozszerzeniem .rans, który zawiera:
- sygnaturę formatu umożliwiającą identyfikację pliku,
- częstości symboli tworzące model statystyczny,
- rozmiar oryginalnych danych,
- nagłówek obrazu,
- zakodowany strumień danych.

Dekodowanie odtwarza oryginalny plik .pgm. Program automatycznie sprawdza poprawność rekonstrukcji poprzez porównanie plików bit-po-bicie, co potwierdza bezstratny charakter kompresji.

---

## Testy

W projekcie zaimplementowano zestaw testów umożliwiających analizę jakości danych oraz poprawności działania algorytmu.

Testy entropii – obliczanie entropii Shannona dla danych syntetycznych oraz obrazów testowych:  
python3 -m tests.entropy_tests

Testy histogramów – generowanie i analiza histogramów rozkładów symboli:  
python3 -m tests.histogram_tests

Wygenerowane obrazy histogramów zapisywane są w katalogu:  
tests/outputs/

---

## Struktura projektu

Struktura projektu została zaprojektowana w sposób czytelny i logiczny, ułatwiający dalszy rozwój oraz analizę kodu.

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

Implementacja realizuje bezstratną kompresję danych, co oznacza, że dane po dekodowaniu są identyczne z danymi wejściowymi. Przeprowadzona analiza entropii oraz histogramów potwierdza zgodność uzyskanych wyników z teorią informacji oraz poprawność działania zaimplementowanego algorytmu. Projekt może stanowić podstawę do dalszych eksperymentów związanych z kodowaniem entropijnym lub rozbudowy o bardziej zaawansowane modele statystyczne.
