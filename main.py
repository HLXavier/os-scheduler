from sys import argv
from reader import read_file
from manager import Manager


if len(argv) < 3:
    print("ARGUMENTOS INVÁLIDOS")
    print("python main.py <arquivo> <tamanho da memória> <fit>")
    exit()
else:
    file = argv[1]
    space = argv[2]
    fit = argv[3]


print('-' * 38)
print(f'arquivo: {file} | espaço: {space} | fit: {fit}')
print('-' * 38)

commands = read_file(file)

manager = Manager(int(space))
manager.simulate(commands, fit)