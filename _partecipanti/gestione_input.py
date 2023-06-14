# By TORFIS

TIPI_NUMERICI = {
    'decimale': float,
    'intero': int
}

def leggi_numero(messaggio, tipo, minimo=None, massimo=None):
    if any((minimo, massimo)) and minimo >= massimo:
        raise ValueError("L'argomento passato 'minimo' deve essere minore di 'massimo'.")
    if tipo not in TIPI_NUMERICI:
        raise ValueError(f"L'argomento passato 'tipo' può essere solo {TIPI_NUMERICI.keys()}.")
    
    while True:
        valore = input(messaggio) or 0
        
        try:
            valore = TIPI_NUMERICI[tipo](valore)
            
            if minimo is not None and valore < minimo:
                print(f"ERRORE: il valore minimo consentito è < {minimo} >")
                continue
            if massimo is not None and valore > massimo:
                print(f"ERRORE: il valore massimo consentito è < {massimo} >")
                continue
                
            return valore
        
        except ValueError:
            print(f"ERRORE: inserisci un valore {tipo} valido, hai inserito < {valore} >")

def leggi_stringa(messaggio, lunghezza_minima, lunghezza_massima, caratteri_validi):
    while True:
        stringa = input(messaggio)
        
        if lunghezza_minima is not None and len(stringa) < lunghezza_minima:
            print(f"ERRORE: la stringa deve essere lunga almeno <{lunghezza_minima}>")
            continue
        
        if lunghezza_massima is not None and len(stringa) > lunghezza_massima:
            print(f"ERRORE: la stringa deve essere lunga al massimo <{lunghezza_massima}>")
            continue
        
        if caratteri_validi is not None:
            # controllo dei caratteri validi
            trovato = False
            for carattere in stringa:
                if carattere not in caratteri_validi:
                    trovato = True
                    break
            
            if trovato:
                print(f"ERRORE: la stringa non può contenere il carattere '{carattere}'.\n"
                      f"I caratteri validi sono: {caratteri_validi}")
                continue
        
        return stringa

# Esempio di utilizzo
# testo = leggi_stringa("Risposta yes o no: ", 2, 3, "YyesNno")
# valore = leggi_float("Inserisci un numero decimale: ", None, 177)
