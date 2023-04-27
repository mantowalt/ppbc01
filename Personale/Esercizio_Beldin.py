nomi = ('Beldin', 'Fedor', 'Reynaud')
Cognomi = ('Malonga', 'Massala', 'Ngoma')
Lista = []
for nome, cognome in zip(nomi, Cognomi):
    Lista.append({'nome': nomi, 'cognome': Cognomi})
print(Lista)