CREATE DATABASE IF NOT EXISTS Park_Rozrywki;
USE Park_Rozrywki;

CREATE TABLE  IF NOT EXISTS Ubezpieczenia (
  ID_ubezpieczenia   INT          NOT NULL AUTO_INCREMENT,
  Opis_ubezpieczenia TEXT         NOT NULL,
  Cena               DECIMAL(6,2) NOT NULL,
  PRIMARY KEY (ID_ubezpieczenia)
) COMMENT 'Dostepne do wyboru ubezpieczenia.';


CREATE TABLE IF NOT EXISTS Cennik_biletow (
  ID_biletu     INT          NOT NULL AUTO_INCREMENT,
  Rodzaj_biletu VARCHAR(25)  NOT NULL,
  Opis_biletu   TEXT         NOT NULL,
  Cena          DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (ID_biletu)
) COMMENT 'Informacje na temat cen wstepu.';


CREATE TABLE IF NOT EXISTS Kraj (
  ID_kraju INT         NOT NULL AUTO_INCREMENT,
  Kraj     VARCHAR(50) NOT NULL,
  PRIMARY KEY (ID_kraju)
) COMMENT 'Kraje zamieszkania naszych klientow oraz pracownikow.';


CREATE TABLE IF NOT EXISTS Miasta (
  ID_miasta INT         NOT NULL AUTO_INCREMENT,
  Miasto    VARCHAR(50) NOT NULL,
  ID_kraju  INT         NOT NULL,
  PRIMARY KEY (ID_miasta),
  FOREIGN KEY (ID_kraju) REFERENCES Kraj(ID_kraju)
) COMMENT 'Miasta zamieszkania naszych klientow oraz pracownikow.';


CREATE TABLE IF NOT EXISTS Adres (
  ID_adresu INT          NOT NULL AUTO_INCREMENT,
  Adres     VARCHAR(100) NOT NULL,
  ID_miasta INT          NOT NULL,
  PRIMARY KEY (ID_adresu),
  FOREIGN KEY (ID_miasta) REFERENCES Miasta(ID_miasta)
) COMMENT 'Adresy zamieszkania naszych klientow oraz pracownikow.';


CREATE TABLE IF NOT EXISTS Goscie (
  ID_goscia      INT         NOT NULL AUTO_INCREMENT,
  Imie           VARCHAR(25) NOT NULL,
  Nazwisko       VARCHAR(25) NOT NULL,
  Data_urodzenia DATE        NOT NULL,
  ID_adresu      INT         NOT NULL,
  PRIMARY KEY (ID_goscia),
  FOREIGN KEY (ID_adresu) REFERENCES Adres(ID_adresu)
) COMMENT 'Tabela z informacjami na temat gosci parku rozrywki.';


CREATE TABLE IF NOT EXISTS Pracownicy (
  ID_pracownika     INT          NOT NULL AUTO_INCREMENT,
  Imie              VARCHAR(25)  NOT NULL,
  Nazwisko          VARCHAR(25)  NOT NULL,
  Data_urodzenia    DATE         NOT NULL,
  Data_zatrudnienia DATE         NOT NULL,
  ID_adresu         INT          NOT NULL,
  Pensja            DECIMAL(6,2) NOT NULL,
  PRIMARY KEY (ID_pracownika),
  FOREIGN KEY (ID_adresu) REFERENCES Adres(ID_adresu)
) COMMENT 'Tabela z informacjami o pracownikach parku.';


CREATE TABLE IF NOT EXISTS Wizyty (
  ID_wizyty        INT                          NOT NULL AUTO_INCREMENT,
  Typ_wizyty       ENUM('stacjonarna','zdalna') NOT NULL,
  Data_przyjazdu   DATE                         NOT NULL,
  Data_wyjazdu     DATE                         NULL    ,
  ID_goscia        INT                          NOT NULL,
  ID_biletu        INT                          NOT NULL,
  ID_ubezpieczenia INT                          NOT NULL,
  PRIMARY KEY (ID_wizyty),
  FOREIGN KEY (ID_goscia) REFERENCES Goscie(ID_goscia),
  FOREIGN KEY (ID_biletu) REFERENCES Cennik_biletow(ID_biletu),
  FOREIGN KEY (ID_ubezpieczenia) REFERENCES Ubezpieczenia(ID_ubezpieczenia)
) COMMENT 'Dane na temat wizyt odbytych przez naszych gosci.';


CREATE TABLE IF NOT EXISTS Atrakcje (
  ID_atrakcji    INT         NOT NULL AUTO_INCREMENT,
  Nazwa_atrakcji VARCHAR(30) NOT NULL,
  Opis_atrakcji  TEXT        NULL    ,
  PRIMARY KEY (ID_atrakcji)
) COMMENT 'Atrakcje udostępnione gosciom w naszym parku.';


CREATE TABLE IF NOT EXISTS Przeglady_atrakcji (
  ID_przegladu   INT  NOT NULL AUTO_INCREMENT,
  Data_przegladu DATE NOT NULL,
  ID_atrakcji    INT  NOT NULL,
  PRIMARY KEY (ID_przegladu),
  FOREIGN KEY (ID_atrakcji) REFERENCES Atrakcje(ID_atrakcji)
) COMMENT 'Dane na temat przegladow naszych atrakcji.';


CREATE TABLE IF NOT EXISTS Awarie_atrakcji (
  ID_awarii   INT  NOT NULL AUTO_INCREMENT,
  Opis_awarii TEXT NULL    ,
  ID_atrakcji INT  NOT NULL,
  PRIMARY KEY (ID_awarii),
  FOREIGN KEY (ID_atrakcji) REFERENCES Atrakcje(ID_atrakcji)
) COMMENT 'Tabela z informacjami na temat awarii atrakcji.';


CREATE TABLE IF NOT EXISTS Uzycie_atrakcji (
  ID_uzycia      INT      NOT NULL AUTO_INCREMENT,
  ID_atrakcji    INT      NOT NULL,
  ID_wizyty      INT      NOT NULL,
  Godzina_uzycia DATETIME NOT NULL,
  PRIMARY KEY (ID_uzycia),
  FOREIGN KEY (ID_atrakcji) REFERENCES Atrakcje(ID_atrakcji),
  FOREIGN KEY (ID_wizyty) REFERENCES Wizyty(ID_wizyty)
) COMMENT 'Tabela przechowujaca dane na temat uzycia konkretnej atrakcji przez danego goscia.';


CREATE TABLE IF NOT EXISTS Typy_wypadkow (
  ID_rodz_wyp INT  NOT NULL AUTO_INCREMENT,
  Opis        TEXT NOT NULL,
  PRIMARY KEY (ID_rodz_wyp)
) COMMENT 'Rodzaje wypadkow jakie moga się przydarzyc naszym gościom (te, ktore podlegaja ubezpieczeniom).';


CREATE TABLE IF NOT EXISTS Wypadki (
  ID_wypadku    INT  NOT NULL AUTO_INCREMENT,
  ID_rodz_wyp   INT  NOT NULL,
  ID_goscia     INT  NOT NULL,
  ID_pracownika INT  NOT NULL,
  Data_wypadku  DATE NOT NULL,
  ID_atrakcji   INT  NULL    ,
  PRIMARY KEY (ID_wypadku),
  FOREIGN KEY (ID_rodz_wyp) REFERENCES Typy_wypadkow(ID_rodz_wyp),
  FOREIGN KEY (ID_goscia) REFERENCES Goscie(ID_goscia),
  FOREIGN KEY (ID_pracownika) REFERENCES Pracownicy(ID_pracownika)
) COMMENT 'Wszelkie dostepne informacje na temat wypadkow w parku.';


CREATE TABLE IF NOT EXISTS Koszty_dzialalnosci (
  ID_kosztu     INT           NOT NULL AUTO_INCREMENT,
  Opis          TEXT          NULL    ,
  Kwota         DECIMAL(18,2) NOT NULL,
  Data_wydatku  DATE          NOT NULL,
  ID_atrakcji   INT           NULL    ,
  ID_pracownika INT           NULL    ,
  PRIMARY KEY (ID_kosztu),
  FOREIGN KEY (ID_atrakcji) REFERENCES Atrakcje(ID_atrakcji),
  FOREIGN KEY (ID_pracownika) REFERENCES Pracownicy(ID_pracownika)
) COMMENT 'Wszystkie dotychczas poniesione koszty.';


CREATE TABLE IF NOT EXISTS Transakcje (
  ID_transakcji   INT                        NOT NULL AUTO_INCREMENT,
  Typ_transakcji  ENUM('przychod','wydatek') NOT NULL,
  Opis_transakcji TEXT                       NULL    ,
  Data_transakcji DATE                       NOT NULL,
  Kwota           DECIMAL(18,2)              NOT NULL,
  ID_wizyty       INT                        NULL    ,
  ID_kosztu       INT                        NULL    ,
  PRIMARY KEY (ID_transakcji),
  FOREIGN KEY (ID_wizyty) REFERENCES Wizyty(ID_wizyty),
  FOREIGN KEY (ID_kosztu) REFERENCES Koszty_dzialalnosci(ID_kosztu)
) COMMENT 'Informacje o transakcjach finansowych.';

ALTER TABLE Ubezpieczenia
ADD COLUMN Nazwa_ubezpieczenia VARCHAR(50) NOT NULL AFTER ID_ubezpieczenia;

ALTER TABLE Przeglady_atrakcji
ADD COLUMN Wynik_przegladu ENUM('POZYTYWNY', 'NEGATYWNY') NOT NULL;

ALTER TABLE Awarie_atrakcji
ADD COLUMN Data_awarii DATE NOT NULL AFTER ID_awarii;

ALTER TABLE Pracownicy
MODIFY Pensja DECIMAL(8,2) NOT NULL; 