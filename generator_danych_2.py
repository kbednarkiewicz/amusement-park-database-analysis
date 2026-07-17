import pandas as pd
import random
import mysql.connector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

random.seed(222)


con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port=3306,
    database="park_rozrywki",
    use_pure=False #lub True w przypadku Segmentation fault
)

mycursor = con.cursor(buffered=True)


imiona_z = pd.read_csv("3_-_Wykaz_imion_żeńskich_nadanych_dzieciom_urodzonym_w_2024_r._wg_pola_imię_pierwsze__statystyka_ogólna_dla_całej_Polski.csv",
                       encoding="utf-8")
imiona_z_pop = imiona_z.nlargest(150, "LICZBA_WYSTĄPIEŃ")["IMIĘ_PIERWSZE"].tolist()
imiona_m = pd.read_csv("3_-_Wykaz_imion_męskich_nadanych_dzieciom_urodzonym_w_2024_r._wg_pola_imię_pierwsze__statystyka_ogólna_dla_całej_Polski.csv",
                       encoding="utf-8")
imiona_m_pop = imiona_m.nlargest(150, "LICZBA_WYSTĄPIEŃ")["IMIĘ_PIERWSZE"].tolist()
nazwiska_z = pd.read_csv("nazwiska_żeńskie-osoby_żyjące_efby1gw.csv", encoding="utf-8", sep=',')
nazwiska_z_pop = nazwiska_z.nlargest(150, "Liczba")["Nazwisko aktualne"].tolist()
nazwiska_m = pd.read_csv("nazwiska_męskie-osoby_żyjące.csv", encoding="utf-8", sep=',')
nazwiska_m_pop = nazwiska_m.nlargest(150, "Liczba")["Nazwisko aktualne"].tolist()

data_projektu = datetime(2026, 1, 18)
dzisiaj = data_projektu.date()

def generowanie_dat(data_start, data_koniec):
    roznica = data_koniec - data_start
    losowe_dni = random.randint(0, roznica.days)
    return data_start + timedelta(days=losowe_dni)

def generowanie_pracownikow(liczba):
    mycursor.execute("SELECT COUNT(*) FROM adres")
    liczba_adresow = mycursor.fetchone()[0]

    lista_dat_zatr=[]
    for i in range(liczba):
        lista_dat_zatr.append(generowanie_dat(datetime(2022,1,1), datetime(2025,12,31)))

    lista_dat_zatr.sort()
        
    sql = "INSERT INTO Pracownicy (Imie, Nazwisko, Data_urodzenia, Data_zatrudnienia, ID_adresu, Pensja) VALUES (%s, %s, %s, %s, %s, %s)"
    for i in range(liczba):
        plec=random.choice(['K','M'])
        if plec == 'K':
            imie, nazwisko = random.choice(imiona_z_pop).capitalize(), random.choice(nazwiska_z_pop).capitalize()
        else:
            imie, nazwisko = random.choice(imiona_m_pop).capitalize(), random.choice(nazwiska_m_pop).capitalize()
        urodziny=generowanie_dat(datetime(1961,1,1), datetime(2008,12,31)).date()
        zatrudnienie=lista_dat_zatr[i]
        pensja=round(random.uniform(4806,12000),2)
        id_adresu=random.randint(1, liczba_adresow) 

        mycursor.execute(sql, (imie, nazwisko, urodziny, zatrudnienie, id_adresu, pensja))
    con.commit()



def generowanie_atrakcji():
    lista_atrakcji=[("Diabelski Młyn", "Rodzaj karuzeli obracającej się na poziomej osi"),
                    ("Smocza Kolejka", "Kolejka górska z motywem smoka"),
                    ("Lodowy Labirynt", "Fascynująca przygoda w ogromnej chłodni w temperaturze -5 stopni z lodowymi rzeźbami"),
                    ("Bajkowa Kraina","Zamknięty plac zabaw z torem przeszkód dla najmłodszych"),
                    ("Uwaga, dinozaur!", "Park edukacyjny z blisko 80 figurami dinozaurów w naturalnych rozmiarach"),
                    ("Powrót do przeszłości", "Wystawa edukująca na temat wierzeń i obyczajów pogan"),
                    ("Wróżba, nie drużba", "Wróżenie z fusów dla 2 osób"),
                    ("Zaginiona Kopalnia", "Interaktywna kolejka w ciemnościach z efektami pirotechnicznymi"),
                    ("Podniebny Surfing", "Ekstremalna karuzela rzucająca pasażerów w przeciążenia 4G"),
                    ("Statek Widmo", "Wahadło stylizowane na stary galeon, wznoszące się pod kątem 90 stopni"),
                    ("Zabójcza Przejażdżka", "Mega coaster o wysokości 85 m i prędkości 150km/h"),
                    ("Skok Wiary", "Wieża swobodnego spadku o wysokości 70 metrów z widokiem na cały park stylizowana na lodową ścianę z Północy (Gra o tron)"),
                    ("Labirynt Królewskiej Przystani", "Interaktywny spacer po ogrodach pełen zagadek i ukrytych przejść, zakończony repliką Żelaznego Tronu"),
                    ("Uczta u Freyów", "Dom strachów oparty na motywie 'Krwawych Godów'- tylko dla osób o mocnych nerwach (16+)"),
                    ("Bitwa o Czarny Nurt", "Atrakcja wodna (Splash Battle), gdzie uczestnicy strzelają z armatek wodnych do wybuchających zielonym dymem celów.")]

    for nazwa, opis in lista_atrakcji:
        mycursor.execute("INSERT INTO Atrakcje (Nazwa_atrakcji, Opis_atrakcji) VALUES (%s, %s)", (nazwa, opis))
        id_atrakcji=mycursor.lastrowid

    con.commit()



def generowanie_przegladow(liczba):
    mycursor.execute("SELECT ID_atrakcji FROM Atrakcje")
    wszystkie_id = [row[0] for row in mycursor.fetchall()]

    opisy_awarii=["Przegrzanie silnika głównego napędu.", "Zablokowanie wagonika na wysokości 15 metrów.", "Wylanie napoju gazowanego na panel sterowania.",
                "Wykrycie poluzowanej śruby w konstrukcji nośnej.", "Awaria systemu hamowania magnetycznego.", "Zakleszczenie pasów bezpieczeństwa",
                "Niestabilne zasilanie w sektorze fontann.", "Pęknięcie liny wyciągowej (system awaryjny zadziałał).", "Uszkodzenie fotokomórki na wejściu.",
                "Wandalizm: guma do żucia w mechanizmie bramki.", "Niespodziewany błąd oprogramowania sterującego (Blue Screen).", "Zbyt wysoki poziom hałasu podczas pracy łożysk.",
                "Zepsucie się grzałki w chłodni.", "Przepalenie bezpiecznika oświetlenia nocnego.", "Usterka czujnika bezpieczeństwa przy barierkach wejściowych.",
                "Konieczność wymiany zużytych elementów ciernych hamulca.", "Awaria systemu nagłośnienia i komunikatów głosowych.", "Zabrudzenie układu optycznego skanera biletów.",
                "Nieszczelność w układzie pneumatycznym (spadek ciśnienia).", "Przerwanie obwodu w sterowniku oświetlenia dekoracyjnego.", "Zablokowanie mechanizmu obrotowego przez ciało obce.",
                "Zużycie paska klinowego w module napędowym.", "Błąd synchronizacji efektów specjalnych z ruchem wagonika.", "Przeciążenie sieci elektrycznej w godzinach szczytu.",
                "Wykrycie luzów na przegubach konstrukcji pomocniczej.", "Niestabilne działanie klimatyzacji w kabinie operatora.","Konieczność awaryjnego restartu systemu operacyjnego sterownika PLC.", 
                "Uszkodzenie uszczelki w układzie hydraulicznym podnośnika.", "Wibracje o niestandardowej częstotliwości podczas pracy jałowej."] 

    lista_dat=[]
    for i in range(liczba):
        lista_dat.append(generowanie_dat(datetime(2023,1,1), datetime(2025,12,31)))

    lista_dat.sort()

    for i in range(liczba):
        id_atrakcji = random.choice(wszystkie_id)
        data_przeg = lista_dat[i]
        wynik = random.choice([
    "POZYTYWNY",
    "POZYTYWNY",
    "POZYTYWNY",
    "POZYTYWNY",
    "NEGATYWNY"])
        mycursor.execute("INSERT INTO Przeglady_atrakcji (Data_przegladu, ID_atrakcji, Wynik_przegladu) VALUES (%s, %s, %s)", (data_przeg, id_atrakcji, wynik))
        
        if wynik == "NEGATYWNY":
            opis_usterki = random.choice(opisy_awarii)
            mycursor.execute("INSERT INTO Awarie_atrakcji (Data_awarii, Opis_awarii, ID_atrakcji) VALUES (%s, %s, %s)", (data_przeg, opis_usterki, id_atrakcji))
            
    con.commit()



def generowanie_kosztow(liczba):
    wszystkie_wydatki = []
    
    mycursor.execute("SELECT ID_atrakcji, Data_przegladu, Wynik_przegladu FROM Przeglady_atrakcji")
    przeglady = mycursor.fetchall()

    mycursor.execute("SELECT ID_pracownika, Data_zatrudnienia, Pensja FROM Pracownicy")
    pracownicy = mycursor.fetchall()

    koszty_male = ["Środki czystości", "Smary i oleje", "Wymiana żarówek", "Bilety do drukarek (rolki)", "Artykuły biurowe"]
    koszty_srednie = ["Części zamienne", "Szkolenie BHP", "Odzież robocza"]
    koszty_duze = ["Faktura za energię elektryczną", "Klimatyzacja", "Woda i ścieki", "Ubezpieczenie OC obiektu", "Marketing", 
                   "Podatek od nieruchomości"]


    for id_atr, data_przeg, wynik in przeglady:
        if hasattr(data_przeg, 'date'): data_przeg = data_przeg.date()
        opis_przegladu = f"Opłata za przegląd techniczny"
        koszt_kontroli = round(random.uniform(150.0, 500.0), 2)
        wszystkie_wydatki.append((opis_przegladu, koszt_kontroli, data_przeg, id_atr, None))

        if wynik == "NEGATYWNY":
            data_serwisu = data_przeg + timedelta(days=1)
            kwota = round(random.uniform(800,2000),2)
            opis = f"Naprawa awaryjna po przeglądzie"
            wszystkie_wydatki.append((opis, kwota, data_serwisu, id_atr, None))
        
        elif random.choice([True, False]):
            data_serwisu = data_przeg
            kwota = round(random.uniform(200, 800), 2)
            opis = f"Smarowanie i konserwacja rutynowa"
            wszystkie_wydatki.append((opis, kwota, data_serwisu, id_atr, None))

    for id_prac, data_zatr, pensja in pracownicy:
        if hasattr(data_zatr, 'date'): data_zatr = data_zatr.date()
        nastepny_mies = data_zatr + relativedelta(months=1)
        data_wypl = nastepny_mies.replace(day=10)
        while data_wypl <= dzisiaj:
            wszystkie_wydatki.append((f"Wynagrodzenie pracownika", pensja, data_wypl, None, id_prac))
            data_wypl += relativedelta(months=1)

    for i in range(liczba):
        kategoria = random.choice(["mala", "mala", "mala", "mala", "srednia", "srednia", "duza"])
        data = generowanie_dat(datetime(2022,1,1), datetime(2025,12,31))
        if hasattr(data, 'date'): data = data.date()

        if kategoria == "mala":
            opis = random.choice(koszty_male)
            kwota = round(random.uniform(100,300), 2)
            wszystkie_wydatki.append((opis, kwota, data, None, None))
        elif kategoria == "srednia":
            opis = random.choice(koszty_srednie)
            kwota = round(random.uniform(500,2000), 2)
            wszystkie_wydatki.append((opis, kwota, data, None, None))
        else:
            opis = random.choice(koszty_duze)
            kwota = round(random.uniform(3000, 10000), 2)
            wszystkie_wydatki.append((opis, kwota, data, None, None))


    wszystkie_wydatki.sort(key=lambda x: x[2])
    mycursor.executemany("INSERT INTO Koszty_dzialalnosci (Opis, Kwota, Data_wydatku, ID_atrakcji, ID_pracownika) VALUES (%s, %s, %s, %s, %s)", wszystkie_wydatki)
    
    con.commit()


generowanie_pracownikow(15)
generowanie_atrakcji()
generowanie_przegladow(100)
generowanie_kosztow(150)


poczatek_kwarantanny = datetime(2023, 6, 1).date()
koniec_kwarantanny = datetime(2023, 12, 31).date()

def generowanie_gosci(liczba):
    mycursor.execute("SELECT ID_adresu FROM Adres")
    wszystkie_id = [row[0] for row in mycursor.fetchall()]
    sql = "INSERT INTO goscie (Imie, Nazwisko, Data_urodzenia, ID_adresu) VALUES (%s, %s, %s, %s)"
    for i in range(liczba):
        plec = random.choice(['K','M'])
        if plec == 'K':
            imie = random.choice(imiona_z_pop).capitalize()
            nazwisko = random.choice(nazwiska_z_pop).capitalize()
        else:
            imie = random.choice(imiona_m_pop).capitalize()
            nazwisko = random.choice(nazwiska_m_pop).capitalize()
        aktualny_rok = data_projektu.year
        data_urodzenia = generowanie_dat(
    datetime(aktualny_rok - 70, 1, 1),
    datetime(aktualny_rok - 3, 12, 31)).date()
        id_adresu = random.choice(wszystkie_id)
        mycursor.execute(sql, (imie, nazwisko, data_urodzenia, id_adresu))
    con.commit()

generowanie_gosci(20000)

def oblicz_wiek(data_urodzenia, data_wizyty):
    return data_wizyty.year - data_urodzenia.year - ((data_wizyty.month, data_wizyty.day) < (data_urodzenia.month, data_urodzenia.day))

def generowanie_wizyt(liczba):
    mycursor.execute("SELECT ID_goscia, Data_urodzenia FROM goscie")
    goscie = mycursor.fetchall()
    mycursor.execute("SELECT ID_ubezpieczenia FROM ubezpieczenia")
    ubezpieczenia = [row[0] for row in mycursor.fetchall()] 
    sql = "INSERT INTO wizyty (Typ_wizyty, Data_przyjazdu, Data_wyjazdu, ID_goscia, ID_biletu, ID_ubezpieczenia) VALUES (%s, %s, %s, %s, %s, %s)"

    lista_wizyt=[]
    for i in range(liczba):
        id_goscia, data_urodzenia = random.choice(goscie)
        wiek_min = 3
        data_min = data_urodzenia + relativedelta(years=wiek_min)
        data_przyjazdu = generowanie_dat(
    max(datetime(2022,1,1), datetime(data_min.year,1,1)),
    data_projektu
).date()
        if data_przyjazdu > dzisiaj:
            data_przyjazdu = dzisiaj
        dlugosc = random.randint(1, 7)
        data_wyjazdu = min(data_przyjazdu + timedelta(days=dlugosc), dzisiaj)
        wiek = oblicz_wiek(data_urodzenia, data_przyjazdu)    
        if wiek < 18 or wiek >= 65:
            id_biletu = 2  
        else:
            los = random.random()
            if los < 0.15:
                id_biletu = 3      
            elif los < 0.30:
                id_biletu = 4  
            else:
                id_biletu = 1  
        if poczatek_kwarantanny <= data_przyjazdu <= koniec_kwarantanny:
            typ_wizyty = "zdalna"
        else:
            typ_wizyty = "zdalna" if random.random() < 0.05 else "stacjonarna"
        id_ubezpieczenia = random.choice(ubezpieczenia) if random.random() < 0.35 else 1
        lista_wizyt.append((typ_wizyty, data_przyjazdu, data_wyjazdu, id_goscia, id_biletu, id_ubezpieczenia))
    lista_wizyt.sort(key=lambda x: x[1])
    for wizyta in lista_wizyt:
        mycursor.execute(sql, wizyta)
    con.commit()

generowanie_wizyt(25000)


def generowanie_uzycia_atrakcji():
    mycursor.execute('''SELECT w.ID_wizyty, w.ID_goscia, w.Data_przyjazdu, 
                     w.Data_wyjazdu, g.Data_urodzenia
                     FROM wizyty w JOIN goscie g 
                     ON w.ID_goscia = g.ID_goscia''')
    wizyty = mycursor.fetchall()    
    mycursor.execute("SELECT ID_atrakcji FROM atrakcje")
    atrakcje = [row[0] for row in mycursor.fetchall()]
    sql = "INSERT INTO uzycie_atrakcji (ID_atrakcji, ID_wizyty, Godzina_uzycia) VALUES (%s, %s, %s)"
    for id_wizyty, id_goscia, data_przyjazdu, data_wyjazdu, data_urodzenia in wizyty:
        wiek = oblicz_wiek(data_urodzenia, data_przyjazdu)
        if wiek <= 5:        
            dostepne_atrakcje = [4, 5]
        elif wiek <= 11:
            dostepne_atrakcje = [1, 2, 4, 5, 6, 7, 8, 10, 12, 13, 15]
        else:
            dostepne_atrakcje = atrakcje
        liczba_atrakcji = random.randint(1,7) 
        for i in range(liczba_atrakcji):
            id_atrakcji = random.choice(dostepne_atrakcje)
            roznica_dni = max((data_wyjazdu - data_przyjazdu).days,0)
            dzien_atrakcji = data_przyjazdu + timedelta(days=random.randint(0, roznica_dni))
            godzina = random.randint(10, 20)
            minuta = random.randint(0, 59)
            sekunda = random.randint(0, 59)
            godz_uzycia = datetime.combine(dzien_atrakcji, datetime.min.time()) + timedelta(hours=godzina, minutes=minuta, seconds=sekunda)
            mycursor.execute(sql, (id_atrakcji, id_wizyty, godz_uzycia))
    con.commit()
generowanie_uzycia_atrakcji()


def generowanie_typow_wypadkow():
        sql = "INSERT INTO typy_wypadkow (Opis) VALUES (%s)"
        opisy = ["Upadek z wysokości", "Potknięcie się lub poślizgnięcie",
                 "Zasłabnięcie, udar słoneczny lub odwodnienie",
                 "Reakcja alergiczna", "Zaklinowanie w ruchomych elementach atrakcji", 
                 "Inne", "Awaria systemów"]
        for opis in opisy:
            mycursor.execute(sql, (opis,))
        con.commit()

generowanie_typow_wypadkow()


def generowanie_wypadkow():
    mycursor.execute('''SELECT w.ID_wizyty, w.ID_goscia, 
                     w.Data_przyjazdu, w.Data_wyjazdu, w.Typ_wizyty FROM wizyty w''')
    wizyty = mycursor.fetchall()    
    mycursor.execute("SELECT ID_pracownika FROM pracownicy")
    pracownicy = [row[0] for row in mycursor.fetchall()]
    mycursor.execute("SELECT ID_rodz_wyp FROM typy_wypadkow")
    typy_wypadkow = [row[0] for row in mycursor.fetchall()]
    
    sql = '''INSERT INTO wypadki 
             (ID_rodz_wyp, ID_goscia, ID_pracownika, Data_wypadku, ID_atrakcji) 
             VALUES (%s, %s, %s, %s, %s)'''

    for id_wizyty, id_goscia, data_przyjazdu, data_wyjazdu, typ_wizyty in wizyty:
        if random.random() < 0.04:
            if typ_wizyty == "zdalna":
                id_rodzaju_wypadku = typy_wypadkow[-1]
            else:
                id_rodzaju_wypadku = random.choice(typy_wypadkow[:-1])
            id_pracownika = random.choice(pracownicy)
            roznica_dni = max((data_wyjazdu - data_przyjazdu).days, 0)
            data_wypadku = data_przyjazdu + timedelta(days=random.randint(0, roznica_dni))
            mycursor.execute("SELECT ID_atrakcji FROM uzycie_atrakcji WHERE ID_wizyty=%s", (id_wizyty,))
            atrakcje = [row[0] for row in mycursor.fetchall()]
            id_atrakcji = random.choice(atrakcje) 
            mycursor.execute(sql, (id_rodzaju_wypadku, id_goscia, id_pracownika, data_wypadku, id_atrakcji))
    con.commit()

generowanie_wypadkow()

def generowanie_transakcji():
    mycursor.execute("SELECT ID_kosztu, Opis, Kwota, Data_wydatku FROM koszty_dzialalnosci")
    koszty = mycursor.fetchall()
    sql = '''INSERT INTO transakcje 
             (Typ_transakcji, Opis_Transakcji, Data_Transakcji, Kwota, ID_wizyty, ID_kosztu) 
             VALUES (%s, %s, %s, %s, %s, %s)'''
    transakcje = []
    for id_kosztu, opis, kwota, data_wydatku in koszty:
        transakcje.append(("wydatek", opis, data_wydatku, kwota, None, id_kosztu))

    mycursor.execute('''SELECT w.ID_wizyty, w.ID_biletu, w.ID_ubezpieczenia, w.Data_przyjazdu,
                               b.Opis_biletu, b.Cena, u.Nazwa_ubezpieczenia, u.Cena
                        FROM wizyty w
                        JOIN cennik_biletow b ON w.ID_biletu = b.ID_biletu
                        JOIN ubezpieczenia u ON w.ID_ubezpieczenia = u.ID_ubezpieczenia''')
    wizyty = mycursor.fetchall()
    
    for id_wizyty, id_biletu, id_ubezpieczenia, data_przyjazdu, opis_biletu, cena_biletu, nazwa_ubezp, cena_ubezp in wizyty:
        transakcje.append(("przychod", f"Sprzedaż: {opis_biletu}", data_przyjazdu, cena_biletu, id_wizyty, None))
        transakcje.append(("przychod", f"Sprzedaż: Ubezpieczenie {nazwa_ubezp}", data_przyjazdu, cena_ubezp, id_wizyty, None))

    transakcje.sort(key=lambda x: x[2])
    for transakcja in transakcje:
        mycursor.execute(sql, transakcja)
    con.commit()

generowanie_transakcji()  


mycursor.close()
con.close()