USE park_rozrywki;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE transakcje;
TRUNCATE TABLE koszty_dzialalnosci;
TRUNCATE TABLE uzycie_atrakcji;
TRUNCATE TABLE wypadki;
TRUNCATE TABLE wizyty;
TRUNCATE TABLE goscie;
TRUNCATE TABLE awarie_atrakcji;
TRUNCATE TABLE przeglady_atrakcji;
TRUNCATE TABLE pracownicy;
TRUNCATE TABLE adres;
TRUNCATE TABLE miasta;
TRUNCATE TABLE kraj;
TRUNCATE TABLE typy_wypadkow;
TRUNCATE TABLE atrakcje;
TRUNCATE TABLE ubezpieczenia;
TRUNCATE TABLE cennik_biletow;

SET FOREIGN_KEY_CHECKS = 1;