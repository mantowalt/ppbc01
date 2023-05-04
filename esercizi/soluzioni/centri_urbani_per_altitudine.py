import sys
import csv
import json
from pathlib import Path
# from optparse import OptionParser

if __name__ != '__main__':
    raise ImportError('Questo script non può essere importato come modulo. '
        'Va eseguito come script. Eseguire con opzione --help per accedere '
        'alla guida.')

# Preparo i valori di default
DEFS = {
    'h_min': float('-inf'),
    'h_max': float('inf'),
    'encoding_in': 'latin-1',
    'encoding_out': 'utf-8',
    'csv_delimiter_in': ';',
    'csv_delimiter_out': ';',
}

# Leggo gli argomenti provenienti da sys.argv
args_list = sys.argv

if len(args_list) == 3:
    # Preparo gli oggetti path-like
    file_Path_in = Path(args_list[1])
    file_Path_out = Path(args_list[2])
else:
    raise ValueError(f'Sono stati passati {len(args_list)-1} argomenti, ma ne '
        'sono richiesti 2 (oltre al nome di questo script): il file di input '
        'e il file di output.')


def read_csv(file, h_min, h_max, delimiter):
    tot_comuni = tot_abitanti = 0
    record_filtrati = [] 
    reader_obj = csv.DictReader(file, delimiter=delimiter)
    for record in reader_obj:
        if h_min < int(record["QUOTA LOCALITA'"]) < h_max:
            tot_comuni += 1
            tot_abitanti += int(record["ABITANTI LOCALITA'"])
            record_filtrati.append(record)
    return {
        'tot_comuni': tot_comuni,
        'tot_abitanti': tot_abitanti,
        'records': record_filtrati
    }

def read_json(file, h_min, h_max):
    tot_comuni = tot_abitanti = 0
    record_filtrati = [] 
    json_list = json.load(file)
    for record in json_list:
        if h_min < record["QUOTA LOCALITA'"] < h_max:
            tot_comuni += 1
            tot_abitanti += record["ABITANTI LOCALITA'"]
            record_filtrati.append(record)
    return {
        'tot_comuni': tot_comuni,
        'tot_abitanti': tot_abitanti,
        'records': record_filtrati
    }


def write_csv(file, records):
    intestazioni = records[0].keys()
    file_writer = csv.DictWriter(file, delimiter=csv_delimiter_out, 
                                 lineterminator='\n', fieldnames=intestazioni)
    file_writer.writeheader()  # scrive la riga di intestazione
    file_writer.writerows(records)

def write_json(file, records):
    json.dump(records, file, indent=2)


def check_file_suffix(suffix, tipo):
    if suffix not in ['.csv', '.json']:
        raise ValueError(f'Il file di {tipo} può essere solo di tipo CSV o '
            'JSON. Il controllo viene fatto sulla estensione del file.')

# Leggo le estensioni dei file di input e output
suffix_in = file_Path_in.suffix.lower()
suffix_out = file_Path_out.suffix.lower()

# Controllo le estensioni
check_file_suffix(suffix_in, 'INPUT')
check_file_suffix(suffix_out, 'OUTPUT')


# Inizializzo il Report a None
report = None

# Template del messaggio di input
default_msg = ('Inserire %s e premi Invio. Se vuoi mantenere il valore di '
               'default [%s], premi solo Invio: ')

# Richiedo all'utente di inserire i parametri, poponendogli di accettare il
# valore di default se non vuole modificarlo
h_min = float(input(default_msg % ('H MIN in metri s.l.m.', DEFS['h_min']))
    or DEFS['h_min'])
h_max = float(input(default_msg % ('H MAX in metri s.l.m.', DEFS['h_max']))
    or DEFS['h_max'])

encoding_in = input(default_msg % 
    ('la Codifica di caratteri per il file di Input', DEFS['encoding_in'])) \
    or DEFS['encoding_in']
encoding_out = input(default_msg % 
    ('la Codifica di caratteri per il file di Output', DEFS['encoding_out'])) \
    or DEFS['encoding_out']

# Nel caso sia un file CSV, chiede anche i separatori
if suffix_in == '.csv':
    csv_delimiter_in = input(default_msg % 
        ('il separatore per il file CSV di input', DEFS['csv_delimiter_in'])) \
        or DEFS['csv_delimiter_in']
    csv_delimiter_out = input(default_msg % 
        ('il separatore per il file CSV di input', DEFS['csv_delimiter_out'])) \
        or DEFS['csv_delimiter_out']


# Ora che abbiamo tutti gli elementi pronti, possiamo partire a eseguire
# l'algoritmo principale.
try:
    with file_Path_in.open('r', encoding=encoding_in) as file_in:
        if suffix_in == '.csv':
            report = read_csv(file_in, h_min, h_max, csv_delimiter_in)
        elif suffix_in == '.json':
            report = read_json(file_in, h_min, h_max)
except Exception as error:
    error.add_note("Si è verificato un errore durante l'apertura del file "
                    "di input.")
    # print('Si è verificato un errore con il file di input ', type(error), ': ', error)
    raise

if report is not None:
    with file_Path_out.open('w', encoding=encoding_out) as file_out:
        if suffix_out == '.csv':
            write_csv(file_out, report['records']), 
        elif suffix_out == '.json':
            write_json(file_out, report['records'])
    print('Il file di OUTPUT è stato creato. Si trova in: ', file_Path_out.resolve())
else:
    print('Si è verificato un errore non previsto. Si prega di contattare il '
          'Supporto Tecnico e riportare il presente errore. Grazie.')