import pandas as pd

#sopprime gli errori che riguardano le estensioni dei dati contenuti nei fogli excel
import warnings
warnings.simplefilter("ignore")

# input data del lavoro che vogliamo inviare
data_invio = '15/05/2023'
# data_invio = input('Inserire la (dd/mm/yyyy) data dei lavori che si desiderano inviare: ')
from datetime import datetime
date = datetime.strptime(data_invio, "%d/%m/%Y")
if not date:
    print('inserire una data valida')
else:
    # apre foglio candidati
    file_path = "./ACE10001_C-Lab_HR/DB C-Lab (HRR).xlsx"
    foglio_candidati = pd.read_excel(file_path, sheet_name= 'Candidati')
    # localizziamo le righe che contengono la data
    posizione_data = foglio_candidati[foglio_candidati['Data invio CV al cliente'].eq(data_invio)]  # @MOD !!
    # copiare le righe che ci interessano nel file da inviare
    righe_candidati_da_copiare = foglio_candidati.loc[posizione_data.index]

    anagskill_ids = set(righe_candidati_da_copiare['Id candidato'].values)  # @MOD !!


    # # cercare nel foglio anagskill i dati dei candidati selezionati
    foglio_anagskill = pd.read_excel(file_path, sheet_name= 'AnagSkill')
    anagskill_transfer = pd.DataFrame()

    for anagskill_id in anagskill_ids:
        candidato_data = foglio_anagskill[foglio_anagskill['Progr Interno'].eq(anagskill_id)]  # @MOD !!
        righe_anagskill_da_copiare = foglio_anagskill.loc[candidato_data.index]
        anagskill_transfer = pd.concat([anagskill_transfer, righe_anagskill_da_copiare])
    anagskill_transfer = pd.DataFrame(anagskill_transfer)
    print(anagskill_transfer)
    # for y, q in foglio_anagskill.iterrows():
    #     valore = q['Progr Interno']
    #     if valore in anagskill_ids:
    #         anagskill_transfer = foglio_anagskill.loc(q.index)
    #         cognome = q['Cognome']
    #         nome = q['Nome']
    #         cognome_nome = cognome + '_' + nome
    #         nomi_curriculum = []
    #         percorso_cv = './ACE10001_C-Lab_HR/CV al Cliente/CV/cv_' + cognome_nome + '.pdf'
    #         print(percorso_cv)
                
    new_file_path = "./ACE10001_C-Lab_HR/DB C-Lab (TransferX).xlsx"
    # righe_candidati_da_copiare.to_excel(writer, index=False, sheet_name='Candidati')
    
    with pd.ExcelWriter(new_file_path) as writer:
        righe_candidati_da_copiare.to_excel(writer, index=False, sheet_name='Candidati')
        anagskill_transfer.to_excel(writer, index=False, sheet_name= 'AnagSkill')