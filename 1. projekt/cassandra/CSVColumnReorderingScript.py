import pandas as pd
import os

# Nastavte cestu k vašemu .csv souboru
csv_file_path = 'data.csv'
modified_file_path = 'modified_data.csv'

# Seznam sloupců, které chcete ponechat a setřídit
desired_columns = ['objectid','name','globalid','code','owner','so2_1h','no2_1h','co_8h','pm10_1h','o3_1h','pm10_24h','pm2_5_1h','actualized']

# Načtení .csv souboru do DataFrame s explicitním nastavením kódování na "UTF-8"
df = pd.read_csv(csv_file_path, encoding='utf-8')

# Odstranění sloupců, které nejsou v seznamu desired_columns
df = df[desired_columns]

# Pokud modifikovaný soubor již existuje, smažte ho
if os.path.exists(modified_file_path):
    os.remove(modified_file_path)

# Přeformátování sloupce 'actualized' z aktuálního formátu na požadovaný formát
df['actualized'] = pd.to_datetime(df['actualized'], format='%Y/%m/%d %H:%M:%S+%f')

# Přeformátování sloupce 'actualized' do nového formátu
df['actualized'] = df['actualized'].dt.strftime('%Y-%m-%d %H:%M:%S.%f%z')

# Uložte upravený DataFrame zpět do .csv souboru
df.to_csv(modified_file_path, index=False, encoding='utf-8')