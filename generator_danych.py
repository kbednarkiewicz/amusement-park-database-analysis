import pycountry
from faker import Faker
import random

random.seed(222)
fake = Faker('pl_PL')
fake.seed_instance(222)

def gen_kraje(liczba):
    wszystkie_kraje = list(pycountry.countries)
    polska = pycountry.countries.get(alpha_2='PL')
    reszta_swiata = [k for k in wszystkie_kraje if k.alpha_2 != 'PL']
    kraje = [polska] + random.sample(reszta_swiata, liczba - 1)
    
    komendy_sql = []

    for i, panstwo in enumerate(kraje, 1):
        nazwa = panstwo.name.replace("'", "''")
        
        sql = f"INSERT INTO kraj (ID_kraju, Kraj) VALUES ({i}, '{nazwa}');"
        komendy_sql.append(sql)
    
    return komendy_sql, len(kraje)

lista_komend, lb_krajow = gen_kraje(30)

def gen_miasta(lb_krajow):
    komendy = []
    nr_id = 1

    for i in range(1, lb_krajow +1):
        for _ in range(3):
            miasto = fake.city().replace("'","''")
            sql = f"INSERT INTO miasta (ID_Miasta, Miasto, ID_Kraju) VALUES ({nr_id}, '{miasto}', {i});"
            komendy.append(sql)
            nr_id += 1
            
    return komendy, nr_id - 1

def gen_adresy(lb_adresow, max_id_miasta):
    komendy = []
    for i in range(1, lb_adresow + 1):
        ulica = fake.street_address().replace("'", "''")
        id_m = random.randint(1, max_id_miasta)
        
        sql = f"INSERT INTO adres (ID_adresu, Adres, ID_miasta) VALUES ({i}, '{ulica}', {id_m});"
        komendy.append(sql)
    return komendy

def gen_cennik_biletow():
    komendy = []
    bilety = [
        ('Normalny', 'Bilet wstępu dla osób dorosłych', 140.00),
        ('Ulgowy', 'Bilet dla dzieci, studentów i seniorów', 90.00),
        ('VIP', 'Bilet na wejście bez kolejek + strefa SPA', 390.00),
        ('Rodzinny', 'Bilet zawierający pakiet dla 2 dorosłych i 2 dzieci', 370.00)
    ]
    
    for i, (rodzaj, opis, cena) in enumerate(bilety, 1):
        sql = f"INSERT INTO cennik_biletow (ID_biletu, Rodzaj_biletu, Opis_biletu, Cena) VALUES ({i}, '{rodzaj}', '{opis}', {cena});"
        komendy.append(sql)
    return komendy

def gen_ubezpieczenia():
    komendy = []
    opcje = [
        ('Papa Smerf', 'NNW na terenie całego parku', 45.00),
        ('Anty-Grawitacja', 'Odszkodowanie, gdyby rollercoaster wystrzelił Cię w kosmos', 29.99),
        ('Ochrona Fryzury', 'Pokrycie kosztów fryzjera po jeździe rollercoasterem', 15.50),
        ('Anty-Podjadacz', 'Odszkodowanie za lody skradzione przez parkowe papugi', 5.99),
    ]
    
    for i, (nazwa, opis, cena) in enumerate(opcje, 1):
        sql = f"INSERT INTO ubezpieczenia (ID_ubezpieczenia,Nazwa_ubezpieczenia, Opis_ubezpieczenia, Cena) VALUES ({i}, '{nazwa}', '{opis}', {cena});"
        komendy.append(sql)
    return komendy


wylosowane_kraje, lb_k = gen_kraje(30)
wylosowane_miasta, lb_m = gen_miasta(lb_k)
wylosowane_adresy = gen_adresy(300, lb_m)
wylosowane_bilety = gen_cennik_biletow()
wylosowane_ubezp = gen_ubezpieczenia()

with open('dane_wygenerowane.sql', 'w', encoding='utf-8') as plik:
    plik.write("USE park_rozrywki;\n")
    plik.write("SET FOREIGN_KEY_CHECKS = 0;\n")

    plik.write("TRUNCATE TABLE adres;\n")
    plik.write("TRUNCATE TABLE miasta;\n")
    plik.write("TRUNCATE TABLE kraj;\n")
    plik.write("TRUNCATE TABLE cennik_biletow;\n")
    plik.write("TRUNCATE TABLE ubezpieczenia;\n\n")

    for wiersz in wylosowane_kraje: plik.write(wiersz + '\n')
    for wiersz in wylosowane_miasta: plik.write(wiersz + '\n')
    for wiersz in wylosowane_adresy: plik.write(wiersz + '\n')
    for wiersz in wylosowane_bilety: plik.write(wiersz + '\n')
    for wiersz in wylosowane_ubezp: plik.write(wiersz + '\n')
    plik.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")