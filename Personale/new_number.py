file = open('numbers.txt', 'a')

for i in range(2, 11):
    file.write(str(i) + ' ')

file.close()