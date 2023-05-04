"""
Questo scipt permette di convertire un file dal fantomatico formato (di nostra
invenzione) FriendBirthDates, aka FBD, a un comunissimo file CSV.

Usage:
    ./converti_nomi_nascita.py [options] <input_file> <output_file>

Questo file può essere anche importato come un modulo e contiene le 
setuenti funzioni:

    * file_to_dict(file_path, anno_calcolo) - dato un file FBD, restituisce un
        dizionario nel formato {età: [nome, ...], ...}
    * dict_to_csv(file_path, in_dict, write_mode) - crea/aggiorna un file CSV, 
        a partire da un dizionario nel formato {età: [nome, ...], ...}
"""

from os import path
from datetime import date   # importo l'oggetto date dal modulo datetime

def file_to_dict(file_path, anno_calcolo=date.today().year):
    """
        Funzione per convertire un file nel celebre formato FriendBirthDates,
        aka FBD, in un dizionario Python nel formato {età: [nome, ...], ...}

    Args:
        file_path (str): il percorso al file FBD (usare lo slash '/' come
                         separatore delle directory).
        anno_calcolo (int): l'anno da considerarsi "corrente" per il calcolo
                         dell'età; se l'argomento è omesso, il valore di default
                         è l'anno corrente.

    Returns:
        Un dizionario contenente delle età come chiavi e liste di nomi come
        valori. {età: [nome, ...], ...}

    """
    res_dict = {}                               # inizializzo il dizionario

    with open(file_path, 'r', encoding='utf-8') as file:  # apro il file in lettura
        
        linea = file.readline()                 # leggo la prima riga

        while linea != '':                      # finché il file non è finito
            linea = linea.split()               # divido la riga in due usando il separatore
                                                #    di defalut e metto i "pezzi" in una lista
            anno_nascita = int(linea[1])        # converto il secondo elemento in integer
            eta = anno_calcolo - anno_nascita   # calcolo l'età della persona
            nome = linea[0].replace(':', '')    # ottengo il nome "pulito"
            if eta in res_dict:                 # se l’età è già presente
                res_dict[eta] += [nome]         # aggiungo il nome alla lista
            else:                               # altrimenti
                res_dict[eta] = [nome]          # creo una lista popolata già con un primo elemento
            linea = file.readline()             # leggo una nuova riga
                                                # (ora il ciclo while riparte e ricontrolla linea)
    return res_dict                             # restituisce il dizionario creato


def dict_to_csv(file_path, in_dict, mode):
    """
    Funzione per convertire un dizionario Python dal formato {età: [nome, ...], ...}
    in un file CSV.

    Args:
        file_path (str): il percorso al file (usare lo slash '/' come separatore delle directory).
        in_dict (dict): dizionario da usare come base di dati per la creazione del CSV.
        mode (str): "a" aggiunge nuovo contenuto al file oppure "w" sovrascrive
                    e inizializza un nuovo file.
    """
    if mode in [None, 'w', 'a']:          # se è stato passato un valore di mode consentito previsto
        if mode is None:                  # se il mode non è indicato
            if path.exists(file_path):    # se il file esiste già
                raise FileExistsError(    # solleva un errore
                    f'Il file "{path.abspath(file_path)}" è già esistente.')
            else:                         # altrimenti usa la modalità 'w'
                mode = 'w'
    else:                                      # altrimenti
        raise ValueError(                      # solleva un errore
            'Il parametro "write_mode" della funzione dict_to_csv() '
            f'può essere solo "None", "w" o "a" invece è stato passato "{mode}".')
    
    with open(file_path, mode, encoding='utf-8') as file_out:  # apro il file con il mode indicato
        if mode == 'w':                                # se la mode passata è 'w'
            file_out.write('Nome,Età\n')               # scrive la prima riga di intestazione
        elif mode == 'a':                              # se la mode passata è 'a'
            if not path.exists(file_path):             # se il percorso file non esiste
                file_out.write('Nome,Età\n')           # scrive la prima riga di intestazione
            elif not path.isfile(file_path):           # se il percorso esiste, ma non è un file
                raise ValueError(                      # solleva un errore
                    f'Il percorso indicato "{path.abspath(file_path)}" non è '
                    'un file. Non è possibile appendere del contenuto a un '
                    'oggetto che non è un file.')
        for key in in_dict:                                    # per ciascuna chiave del in_dict creato prima
            for nome in in_dict[key]:                          # per ciascun nome nella lista corrispondente
                file_out.write(nome + ',' + str(key) + '\n')   # scrive la riga contente la coppia nome,età


if __name__ == '__main__':              # se viene esegiuto come script
    from optparse import OptionParser   # importo la classe OptionParser
                                        #   (uno strumento più avanzato per leggere parametri e opzioni
                                        #   rispetto a sys.argv e crea l'opzione di help in automatico)
    
    # preparo una stringa di messaggio per l'Usage
    usage_msg = '%prog [options] <input_file> <output_file>'
    #      |--> './converti_nomi_nascita.py [options] <input_file> <output_file>'
    
    optparser = OptionParser(usage=usage_msg)  # creo l'oggetto optparser a partire dalla classe OptionParser
   
    # creo le opzioni disponibili per la command line
    optparser.add_option('-w', '--write', action='store_true',
                    help='Forza la sovrascrittura del file di destinazione '
                         'se questo esiste già, altrimenti lo crea.')
    optparser.add_option('-a', '--append', action='store_true',
                    help="Forza l'aggiunta del nuovo contenuto al fondo del file "
                         "se questo esiste già, altrimenti lo crea.")

    # ottengo le opzioni e gli argomenti da OptionParser.parse_args()
    (options, lista_args) = optparser.parse_args()

    qta_args = len(lista_args)                   # conto gli argomenti
    if qta_args != 2:                            # se gli argomenti non sono in numero corretto
        raise ValueError(                        # solleva un errore
            'Non è stato passato il numero corretto di argomenti allo scritp.' 
            'Lo script prevede 2 argomenti: il file di input e il file di output.')

    if options.append and options.write:         # se l'utente ha indicato entrambe le opzioni
        raise ValueError(                        # solleva un errore
            'Non puoi usare le opzioni "-w" e "-a" assieme.')
    else:                                        # altrimenti
        if options.write:                        # se è stato passato il parametro -w (o --write)
            mode = 'w'                           # imposta mode su 'w'
        elif options.append:                     # se è stato passato il parametro -a(o --append)
            mode = 'a'                           # imposta mode su 'a'
        else:                                    # se nessuna opzione è usata
            mode = None                          # imposta mode su None
        
    res_dict = file_to_dict(lista_args[0])       # converte il file di input in un dizionario
    dict_to_csv(lista_args[1], res_dict, mode)   # scrive il file CSV a partire da l dizionario
