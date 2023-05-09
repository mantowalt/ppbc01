import csv

anno = 2011
superficie = 150
cap = (10126, 10127, 10134)
numero_attivita = 0

with open ('Comune-di-Torino---Attivita-commerciali.csv', encoding='latin-1') as file_in:
    reader_obj = csv.DictReader(file_in, delimiter=';')

    for linea in reader_obj:
        if int(linea["Anno inizio attivita"]) >= anno:
            if linea["Mq tot locale"].isdigit():
                if int(linea["Mq tot locale"])>= superficie:
                        if int(linea["Cap"]) in cap:
                        
                            numero_attivita += 1

print('Numero di attività commerciali trovate:', numero_attivita)