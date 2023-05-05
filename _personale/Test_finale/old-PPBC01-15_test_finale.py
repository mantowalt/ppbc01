# PPBC01-15 Russo Salvatore
# Tset finale
# FILTRARE UN FILE DI ATTIVITA COMMERCIALI CON I SEGUENTI DATI:
# 'ANNO INIZIO ATTIVITA' + 'MQ TOT LOCALE' + 'CAP'


import csv

tot_attivita = 0
tot_mq = 0
tot_finale= 0
cap1=10126
cap2=10127
cap3=10134
file_name = './Comune-di-Torino---Attivita-commerciali.csv'

with open(file_name, encoding='latin-1') as file_in:
    reader_obj = csv.DictReader(file_in, delimiter=';') 
                                                        
    for linea in reader_obj:                            
        if int(linea["ANNO INIZIO ATTIVITA"]) >= 2011:                                                    
            tot_attivita += 1                              
            if int(linea["MQ TOT LOCALE"]) > 150:
                tot_mq += 1  
                if int(linea["CAP"]) == cap1 and cap2 and cap3:
                    tot_finale += 1  
                                                              

print('RISULTATO DELLA RICERCA:')
print('--------------------------------------------------------------------------')
print('N. di attività che hanno iniziato dopo il 2011:', tot_attivita)
print('di queste hanno una metratura sopra i 150mq:', tot_mq)
print('e che sono ubicati nei cap (', cap1,'-',cap2,'-',cap3,'): ', tot_finale)
