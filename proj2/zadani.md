# Projekt - zadání 2. části

**Cílem této části projektu je vyzkoušet si:**

- provedení explorativní analýzy na zvolené datové sadě.
- úpravu datové sady do podoby vhodné pro dolování.

**Dostupné datové sady a možné dolovací úlohy:**

1. Datová sada **Most Streamed Spotify Songs 2023** – dostupná zde: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023
   Dolovací úloha: predikce oblíbenosti písně na základě ostatních atributů (např.: rytmus písně, tónina, mód písně apod.).
2. Datová sada **All countries details** – dostupná zde: https://www.kaggle.com/datasets/adityakishor1/all-countries-details
   Dolovací úlohy: predikce míry inflace nebo průměrné očekávané délky života na základě vhodných atributů nebo hledání skupin zemí s podobnou ekonomicko-politickou situací apod.
3. Datová sada **Students menthal health survey** – dostupná zde: https://www.kaggle.com/datasets/sonia22222/students-mental-health-assessments
   Dolovací úloha: klasifikace úrovně stresu/deprese/úzkosti na základě ostatních vhodných atributů.

**Způsob odevzdání (požadované výstupy):**

Výsledné řešení (jeden zip archiv) odevzdá pouze vedoucí týmu prostřednictvím IS VUT. Řešení bude obsahovat:

- Zdrojové kódy pro Vámi provedenou explorativní analýzu a zdrojové kódy pro úpravu datové sady do požadované podoby. Preferovaným programovacím jazykem je Python, ale můžete využít i Javu nebo jazyk R. Řešení je možné odevzdat i formou Jupyter notebooku.
- Dokumentaci obsahující výsledky explorativní analýzy a popis provedených úprav datové sady ve formátu pdf. K explorativní analýze bude dokumentace obsahovat odpovídající podkapitolu ke každému požadovanému bodu uvedenému níže. Pro prezentaci zjištěných informací využijte vhodné tabulky a grafy. Dále pro každou požadovanou úpravu datové sady uveďte, jakou metodu (jaké metody) jste použili, a zdůvodněte, proč jste vybrali právě tuto metodu (tyto metody).
- Obě výsledné varianty upravené datové sady ve formátu csv. Pro zmenšení velikosti odevzdávaného archivu odevzdejte pouze prvních 50 řádků těchto datových sad.

**Pokyny k řešení:**

1. Z dostupných datových sad si zvolte jednu datovou sadu, kterou se budete dále zabývat. Stáhněte si zvolenou datovou sadu z uvedeného zdroje a prostudujte si dostupné informace k této datové sadě.
2. Proveďte explorativní analýzu zvolené datové sady. Pro každý následující bod implementujte odpovídající sekci ve zdrojovém kódu a zjištěné výsledky popište v dokumentaci:
    - prozkoumejte jednotlivé atributy datové sady, jejich typ a hodnoty, kterých nabývají (počet hodnot, nejčastější hodnoty, rozsah hodnot atd.)
    - prozkoumejte rozložení hodnot jednotlivých atributů pomocí vhodných grafů, zaměřte se i na to, jak hodnota jednoho či dvou atributů ovlivní rozložení hodnot jiného atributu. Do dokumentace vložte alespoň 5 různých grafů, zobrazujících zjištěná rozložení hodnot. Použijte různé typy grafů (např. bodový graf, histogram, krabicový nebo houslový graf, graf složený z více podgrafů apod.) a věnujte se různým atributům. V dokumentaci také všechny grafy vhodně okomentujte – popište, jaké informace z nich můžeme vyčíst.
    - zjistěte, zda zvolená datová sada obsahuje nějaké odlehlé hodnoty. V dokumentaci popište, jakým způsobem jste odlehlé hodnoty detekovali, a jaké hodnoty jste objevili.
    - proveďte podrobnou analýzu chybějící hodnot. V dokumentaci popište celkový počet chybějících hodnot, počet objektů s více chybějícími hodnotami atd.
    - proveďte korelační analýzu numerických atributů (k analýze využijte grafy i korelační koeficienty).

3. Připravte 2 varianty datové sady vhodné pro dolovací algoritmy. Můžete uvažovat dolovací úlohu uvedenou u datové sady nebo navrhnout vlastní dolovací úlohy. V případě vlastní dolovací úlohy ji specifikujte v dokumentaci. V rámci přípravy datové sady proveďte následující kroky:
    - Z datové sady odstraňte atributy, které jsou pro danou dolovací úlohu irelevantní. V datové sadě, pokud možno, ponechte jak kategorické, tak i numerické atributy, atributy s chybějícími hodnotami a atributy s odlehlými hodnotami (pokud je původní datová sada obsahuje).
    - Vypořádejte se s chybějícími hodnotami. Pro odstranění těchto hodnot využijte alespoň dvě různé metody pro odstranění chybějících hodnot.
    - Vypořádejte se s odlehlými hodnotami, jsou-li v datové sadě přítomny.
    - Pro jednu variantu datové sady proveďte diskretizaci numerických atributů tak, aby výsledná datová sada byla vhodná pro algoritmy, které vyžadují na vstupu kategorické atributy.
    - Pro druhou variantu datové sady proveďte vhodnou transformaci kategorických atributů na numerické atributy. Dále pak proveďte normalizaci numerických atributů, které má smysl normalizovat. Výsledná datová sada by měla být vhodná pro metody vyžadující numerické vstupy.

**Závěrečné poznámky:**

- Při explorativní analýze vytvořte větší množství grafů a do dokumentace se snažte vybrat grafy, které ukazují nějaké zajímavé vztahy mezi atributy.
- Pokud máte nějakou jinou datovou sadu, kterou byste se rádi zabývali, tak mne prosím kontaktujte. Stejně tak, pokud budete chtít pro explorativní analýzu využít jiný nástroj, tak se ozvěte.