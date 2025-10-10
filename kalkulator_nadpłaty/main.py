# import math

# nadplata = 2000  # zł
# kwota_kredytu = 426526.11  # zł
# oprocentowanie = 0.0853  # roczne oprocentowanie

# # Konwersja oprocentowania na miesięczną stopę
# oprocentowanie_miesieczne = oprocentowanie / 12

# # Obliczamy liczbę okresów spłaty po nadpłacie
# liczba_okresow_spłaty = -math.log(1 - (nadplata / kwota_kredytu) * oprocentowanie_miesieczne) / math.log(1 + oprocentowanie_miesieczne)

# # Zaokrąglamy do pełnych miesięcy
# liczba_okresow_spłaty = round(liczba_okresow_spłaty)

# # Aktualna liczba miesięcy
# aktualna_liczba_miesiecy = 336  # liczba miesięcy do listopada 2048

# # Całkowita liczba miesięcy po nadpłacie
# calkowita_liczba_miesiecy = aktualna_liczba_miesiecy + liczba_okresow_spłaty

# # Obliczamy datę spłaty po nadpłacie
# rok = 2048 - (calkowita_liczba_miesiecy // 12)
# miesiac = 1 + (calkowita_liczba_miesiecy % 12)

# print(f"Całkowita liczba miesięcy po nadpłacie: {calkowita_liczba_miesiecy} miesięcy.")
# print(f"Przewidywana data spłaty po nadpłacie: {miesiac}/{rok}")

#v2 
from datetime import datetime, timedelta
import calendar

def oblicz_raty(saldo, oprocentowanie, okres):
    r = oprocentowanie / 12 / 100
    rata = saldo * (r * (1 + r) ** okres) / ((1 + r) ** okres - 1)
    return rata

def oblicz_date_splaty(kwota_kredytu, oprocentowanie, okres_kredytowania, nadplata_miesieczna, ostatnia_data):
    saldo_do_splaty = kwota_kredytu
    r = oprocentowanie / 12 / 100
    miesieczna_rata = kwota_kredytu * (r * (1 + r) ** okres_kredytowania) / ((1 + r) ** okres_kredytowania - 1)
    data_splaty = datetime.strptime(ostatnia_data, "%Y-%m-%d")

    while saldo_do_splaty > 0:
        kwota_odsetek = saldo_do_splaty * (oprocentowanie / 12 / 100)
        kwota_kapitalu = miesieczna_rata - kwota_odsetek
        saldo_do_splaty -= kwota_kapitalu + nadplata_miesieczna

        if saldo_do_splaty > 0:
            dni_w_miesiacu = calendar.monthrange(data_splaty.year, data_splaty.month)[1]
            data_splaty += timedelta(days=dni_w_miesiacu)

    return data_splaty, miesieczna_rata, saldo_do_splaty

def podaj_informacje(kwota_kredytu, oprocentowanie, okres_kredytowania, ostatnia_data):
    saldo_do_splaty = kwota_kredytu
    pozostalo_rat = okres_kredytowania
    rata_kapitalowa = 0
    rata_odsetkowa = 0
    miesieczna_rata = oblicz_raty(kwota_kredytu, oprocentowanie, okres_kredytowania)

    for _ in range(okres_kredytowania):
        kwota_odsetek = saldo_do_splaty * (oprocentowanie / 12 / 100)
        kwota_kapitalu = miesieczna_rata - kwota_odsetek
        saldo_do_splaty -= kwota_kapitalu

        rata_kapitalowa += kwota_kapitalu
        rata_odsetkowa += kwota_odsetek

    print("\nAktualna sytuacja kredytowa:")
    print(f"Wysokość raty: {miesieczna_rata:.2f} zł")
    print(f"Pozostało rat: {pozostalo_rat}")
    print(f"Saldo do spłaty: {saldo_do_splaty:.2f} zł")
    print(f"Rata kapitałowa: {rata_kapitalowa:.2f} zł")
    print(f"Rata odsetkowa: {rata_odsetkowa:.2f} zł")

    return saldo_do_splaty, pozostalo_rat, miesieczna_rata

def przelicz_nadplate(miesieczna_rata, saldo_do_splaty, okres_kredytowania, nadplata_miesieczna):
    nowy_okres_kredytowania = okres_kredytowania
    nowa_rata_bez_skrocenia = oblicz_raty(saldo_do_splaty, oprocentowanie, okres_kredytowania)

    if nadplata_miesieczna < nowa_rata_bez_skrocenia:
        nowa_rata_z_skroceniem = oblicz_raty(saldo_do_splaty, oprocentowanie, nowy_okres_kredytowania)
        oszczednosc_miesieczna_z_skroceniem = miesieczna_rata - nowa_rata_z_skroceniem
        oszczednosc_roczna_z_skroceniem = oszczednosc_miesieczna_z_skroceniem * 12
        oszczednosc_calkowita_z_skroceniem = oszczednosc_miesieczna_z_skroceniem * nowy_okres_kredytowania

        print("\nSkutek nadpłaty kredytu:")
        print("1) Jeśli zmniejszasz raty:")
        print(f"Nowa rata: {nowa_rata_bez_skrocenia:.2f} zł")
        print(f"Miesięczna oszczędność: {nadplata_miesieczna:.2f} zł")
        print(f"Roczna oszczędność: {nadplata_miesieczna * 12:.2f} zł")
        print(f"Oszczędność na całym kredycie: {nadplata_miesieczna * okres_kredytowania:.2f} zł")

        print("\n2) Jeśli skracasz okres kredytowania:")
        print(f"Rata bez zmian: {nowa_rata_z_skroceniem:.2f} zł")
        print(f"Liczba rat: {nowy_okres_kredytowania}")
        print(f"Skrócenie okresu o: {okres_kredytowania - nowy_okres_kredytowania} miesięcy")  # Zmieniłem pozostalo_rat na okres_kredytowania
        print(f"Oszczędność na całym kredycie: {oszczednosc_calkowita_z_skroceniem:.2f} zł")
    else:
        print("Nadpłata jest większa niż pozostałe saldo kredytu. Kredyt zostanie spłacony wcześniej.")

# Pobierz dane od użytkownika
kwota_kredytu = float(input("Jaką kwotę jeszcze musisz spłacić? "))
oprocentowanie = float(input("Podaj oprocentowanie Twojego kredytu: "))
okres_kredytowania = int(input("Podaj okres kredytowania w miesiącach: "))
ostatnia_data = input("Kiedy zapłacisz ostatnią ratę? (w formacie YYYY-MM-DD): ")

# Dodaj zmienną nadplata_miesieczna
nadplata_miesieczna = 0

# Zapytaj użytkownika, czy chce nadpłacić kredyt

czy_nadplacic = input("Czy chcesz dokonać nadpłaty kredytu? (tak/nie): ").lower()

if czy_nadplacic == "tak":
    nadplata_miesieczna = float(input("Podaj kwotę nadpłaty miesięcznej: "))
    # Wywołaj funkcję obliczającą datę spłaty kredytu
    data_splaty, miesieczna_rata, saldo_do_splaty = oblicz_date_splaty(kwota_kredytu, oprocentowanie, okres_kredytowania, nadplata_miesieczna, ostatnia_data)
    print(f"\nPrzy regularnym nadpłacaniu, kredyt zostanie spłacony około {data_splaty.strftime('%Y-%m-%d')}.")
    przelicz_nadplate(miesieczna_rata, saldo_do_splaty, okres_kredytowania, nadplata_miesieczna)
else:
    print("Dziękujemy za skorzystanie z naszego programu.")
