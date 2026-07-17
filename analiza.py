import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'port': 3306,
    'database': 'park_rozrywki',
    'use_pure': False #lub True w przypadku Segmentation fault
}

db = mysql.connector.connect(**config)

def analiza_rentownosci():
    sql = """
    SELECT 
        a.Nazwa_atrakcji,
        COUNT(u.ID_uzycia) AS Liczba_uzyc,
        ROUND(
            (SELECT SUM(Kwota) FROM transakcje WHERE Typ_transakcji = 'przychod') / 
            (SELECT COUNT(*) FROM uzycie_atrakcji) * COUNT(u.ID_uzycia)
        , 2) AS Przychod_PLN,
        ROUND(
            IFNULL((SELECT SUM(k.Kwota) FROM Koszty_dzialalnosci k WHERE k.ID_atrakcji = a.ID_atrakcji), 0) +
            ((SELECT SUM(k2.Kwota) FROM Koszty_dzialalnosci k2 WHERE k2.ID_atrakcji IS NULL) / (SELECT COUNT(*) FROM Atrakcje))
        , 2) AS Koszty_Calkowite,
        (SELECT COUNT(*) FROM Awarie_atrakcji aw WHERE aw.ID_atrakcji = a.ID_atrakcji) AS Dni_Awarii
    FROM Atrakcje a
    LEFT JOIN Uzycie_atrakcji u ON a.ID_atrakcji = u.ID_atrakcji
    GROUP BY a.ID_atrakcji
    ORDER BY Liczba_uzyc DESC;
    """
    
    df = pd.read_sql(sql, db)
    df['Zysk'] = df['Przychod_PLN'] - df['Koszty_Calkowite']
    df['Czy_Oplacalna'] = df['Zysk'].apply(lambda x: 'TAK' if x > 0 else 'NIE')
    df.to_csv("wyniki_analiza/rentownosc.csv", index=False)

    print("\n--- ANALIZA RENTOWNOŚCI ATRAKCJI ---")
    print(df.to_string(index=False))
    return df

def generuj_wykres_klientow():
    sql = """
    SELECT 
        DATE_FORMAT(Data_przyjazdu, '%Y-%m') AS Miesiac,
        COUNT(DISTINCT ID_goscia) AS Liczba_Klientow
    FROM wizyty
    GROUP BY Miesiac
    ORDER BY Miesiac;
    """
    
    df = pd.read_sql(sql, db)
    
    if df.empty:
        return

    plt.figure(figsize=(15, 8))
    sns.set_style("whitegrid")
    
    chart = sns.barplot(x='Miesiac', y='Liczba_Klientow', data=df, color='skyblue', alpha=0.8)
    plt.plot(range(len(df)), df['Liczba_Klientow'], marker='o', color='pink', linewidth=2.2, label='Trend')
    
    for p in chart.patches:
        chart.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points')

    plt.title('Liczba obsłużonych klientów w czasie')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('wyniki_analiza/raport_trend.png')
    plt.close()
    plt.show()

def raport_bezpieczenstwa():
    sql = """
    SELECT 
        a.Nazwa_atrakcji,
        uzycia.Liczba_Przejazdow,
        IFNULL(zdarzenia.Liczba_Wypadkow, 0) AS Liczba_Wypadkow,
        ROUND((IFNULL(zdarzenia.Liczba_Wypadkow, 0) * 100.0) / NULLIF(uzycia.Liczba_Przejazdow, 0), 2) AS Wskaznik_Wypadkowosci
    FROM Atrakcje a
    LEFT JOIN (
        SELECT ID_atrakcji, COUNT(*) AS Liczba_Przejazdow 
        FROM uzycie_atrakcji 
        GROUP BY ID_atrakcji
    ) AS uzycia ON a.ID_atrakcji = uzycia.ID_atrakcji
    LEFT JOIN (
        SELECT ID_atrakcji, COUNT(*) AS Liczba_Wypadkow 
        FROM wypadki 
        GROUP BY ID_atrakcji
    ) AS zdarzenia ON a.ID_atrakcji = zdarzenia.ID_atrakcji
    ORDER BY Wskaznik_Wypadkowosci DESC;
    """
    
    df = pd.read_sql(sql, db)
    
    def ocena_stanu(w):
        if w > 2.0: return "WYMAGANA KONTROLA"
        if w > 0.5: return "WZMOCNIONY NADZÓR"
        return "OK"
            
    df['Zalecenia'] = df['Wskaznik_Wypadkowosci'].apply(ocena_stanu)
    
    print("\n--- STAN BEZPIECZEŃSTWA ---")
    print(df.to_string(index=False))
    df.to_csv("wyniki_analiza/bezpieczenstwo.csv", index=False)
    return df

def statystyki_geograficzne():
    sql = """
    SELECT 
        k.Kraj, 
        COUNT(DISTINCT g.ID_goscia) AS Liczba_Gosci,
        ROUND(AVG(c.Cena), 2) AS Srednia_Cena
    FROM goscie g
    JOIN adres a ON g.ID_adresu = a.ID_adresu
    JOIN miasta m ON a.ID_miasta = m.ID_miasta
    JOIN kraj k ON m.ID_kraju = k.ID_kraju
    JOIN wizyty w ON g.ID_goscia = w.ID_goscia
    JOIN cennik_biletow c ON w.ID_biletu = c.ID_biletu
    GROUP BY k.Kraj
    ORDER BY Liczba_Gosci DESC
    LIMIT 5;
    """
    df = pd.read_sql(sql, db)
    print("\n--- TOP 5 KRAJÓW ---")
    print(df.to_string(index=False))
    df.to_csv("wyniki_analiza/geograficzne.csv", index=False)
    return df

def statystyki_biletow():
    sql = """
    SELECT 
        c.Rodzaj_biletu, 
        COUNT(w.ID_wizyty) AS Sprzedano,
        ROUND(SUM(c.Cena), 2) AS Suma_Przychod
    FROM cennik_biletow c
    LEFT JOIN wizyty w ON c.ID_biletu = w.ID_biletu
    GROUP BY c.Rodzaj_biletu
    ORDER BY Suma_Przychod DESC;
    """
    print("\n--- PRZYCHODY Z BILETÓW ---")
    df = pd.read_sql(sql, db)
    print(df.to_string(index=False))
    df.to_csv("wyniki_analiza/bilety.csv", index=False)
    return df

def analiza_lojalnosci():
    sql = """
    SELECT 
        CASE 
            WHEN Liczba_Wizyt = 2 THEN '2 wizyty'
            WHEN Liczba_Wizyt = 3 THEN '3 wizyty'
            WHEN Liczba_Wizyt > 3 THEN 'Więcej niż 3'
        END AS lb_Odwiedzin,
        COUNT(*) AS Ile_Osob
    FROM (
        SELECT ID_goscia, COUNT(ID_wizyty) AS Liczba_Wizyt
        FROM wizyty
        GROUP BY ID_goscia
    ) AS dane
    WHERE Liczba_Wizyt >= 2
    GROUP BY lb_Odwiedzin;
    """
    print("\n--- GOŚCIE POWRACAJĄCY ---")
    df = pd.read_sql(sql, db)
    print(df.to_string(index=False))
    df.to_csv("wyniki_analiza/lojalnosc.csv", index=False)
    return df

def demografia_wiekowa():
    sql = """
    SELECT 
        ROUND(AVG(2026 - YEAR(Data_urodzenia)), 1) AS Sredni_Wiek,
        MIN(2026 - YEAR(Data_urodzenia)) AS Najmlodszy,
        MAX(2026 - YEAR(Data_urodzenia)) AS Najstarszy,
        COUNT(*) AS Liczba_Gosci
    FROM goscie;
    """
    df = pd.read_sql(sql, db)
    print("\n--- DEMOGRAFIA ---")
    print(df.to_string(index=False))
    
    sredni_wiek = df['Sredni_Wiek'].iloc[0]
    print(f"\nŚredni wiek odwiedzających: {sredni_wiek}")
    df.to_csv("wyniki_analiza/demografia.csv", index=False)
    return df

def wynik_finansowy_parku():
    sql = """
    SELECT 
        Typ_transakcji,
        SUM(Kwota) AS Suma
    FROM transakcje
    GROUP BY Typ_transakcji;
    """

    df = pd.read_sql(sql, db)
    przychody = df.loc[df['Typ_transakcji'] == 'przychod', 'Suma'].sum()
    koszty = df.loc[df['Typ_transakcji'] == 'wydatek', 'Suma'].sum()
    zysk = przychody - koszty
    marza = (zysk / przychody) * 100 if przychody > 0 else 0
    wynik = pd.DataFrame({
        "Kategoria": [
            "Przychody całkowite",
            "Koszty całkowite",
            "Zysk netto",
            "Marża (%)"
        ],
        "Wartość": [
            round(przychody,2),
            round(koszty,2),
            round(zysk,2),
            round(marza,2)
        ]
    })

    print("\n--- WYNIK FINANSOWY PARKU ---")
    print(wynik.to_string(index=False))

    wynik.to_csv("wyniki_analiza/wynik_finansowy.csv", index=False)

    return wynik

def wykres_finanse():
    df = pd.read_csv("wyniki_analiza/wynik_finansowy.csv")
    df = df[df['Kategoria'] != "Marża (%)"]
    plt.figure(figsize=(8,5))
    sns.barplot(
        data=df,
        x="Kategoria",
        y="Wartość"
    )
    plt.title("Wynik finansowy parku")
    plt.ylabel("Kwota [PLN]")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("wyniki_analiza/finanse.png")
    plt.close()

def trend_finansowy():
    sql = """
    SELECT
        DATE_FORMAT(Data_Transakcji, '%Y-%m') AS Miesiac,
        Typ_transakcji,
        SUM(Kwota) AS Kwota
    FROM transakcje
    GROUP BY Miesiac, Typ_transakcji
    ORDER BY Miesiac;
    """

    df = pd.read_sql(sql, db)
    tabela = df.pivot_table(
        index="Miesiac",
        columns="Typ_transakcji",
        values="Kwota",
        aggfunc="sum",
        fill_value=0
    )

    if "przychod" not in tabela.columns:
        tabela["przychod"] = 0

    if "wydatek" not in tabela.columns:
        tabela["wydatek"] = 0

    tabela["Zysk"] = tabela["przychod"] - tabela["wydatek"]
    tabela = tabela.reset_index()
    tabela.rename(columns={
        "przychod": "Przychody",
        "wydatek": "Koszty"
    }, inplace=True)

    print("\n--- TREND FINANSOWY ---")
    print(tabela.to_string(index=False))

    tabela.to_csv("wyniki_analiza/trend_finansowy.csv",index=False)
    plt.figure(figsize=(14,7))
    plt.plot(
        tabela["Miesiac"],
        tabela["Przychody"],
        marker="o",
        label="Przychody"
    )
    plt.plot(
        tabela["Miesiac"],
        tabela["Koszty"],
        marker="o",
        label="Koszty"
    )
    plt.plot(
        tabela["Miesiac"],
        tabela["Zysk"],
        marker="o",
        label="Zysk")
    plt.title("Trend przychodów, kosztów i zysku w czasie")
    plt.xlabel("Miesiąc")
    plt.ylabel("Kwota [PLN]")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("wyniki_analiza/trend_finansowy.png")
    plt.close()

    return tabela

if __name__ == "__main__":
    analiza_rentownosci()
    raport_bezpieczenstwa()
    generuj_wykres_klientow()
    statystyki_geograficzne()
    statystyki_biletow()
    analiza_lojalnosci()
    demografia_wiekowa()
    wynik_finansowy_parku() 
    wykres_finanse()
    trend_finansowy()
    db.close()