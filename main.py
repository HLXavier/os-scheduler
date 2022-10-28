from reader import convert_file


IN = 'IN'
OUT = 'OUT'

FIRST_FIT = 'ff'
BEST_FIT = 'bf'
WORST_FIT = 'wf'
CIRCULAR_FIT = 'cf'


file = 'case1'
commands = convert_file(file)

size = 16
memory = [(None, size)]

def add(pid, size, pos):
    _, free = memory[pos]

    if free > size:
        memory.insert(pos, (pid, size))
        memory[pos+1] = (None, free-size)

    if free == size:
        memory[pos] = (pid, size)


def first_fit(pid, size):
    for pos in range(len(memory)):
        cur_pid, _ = memory[pos]
        if cur_pid == None:
            add(pid, size, pos)
            return
            
    print("ESPAÇO INSUFICIENTE DE MEMÓRIA")


def compact(pos1, pos2):
    _, size1 = memory[pos1]
    pid2, size2 = memory[pos2]

    if pid2 == None:
        memory[pos1] = (None, size1 + size2)
        memory.pop(pos2)


def remove(pid):
    for pos in range(len(memory)):
        mem_pid, mem_size = memory[pos]

        if mem_pid == pid:
            memory[pos] = (None, mem_size)

            next = pos + 1
            prev = pos - 1

            if next < len(memory):
                compact(pos, next)
            
            if prev > 0:
                compact(pos, prev)

            return
    
    print("PROCESSO NÃO ENCONTRADO")
            

for command in commands:
    if command[0] == IN:
        first_fit(*command[1:])
    
    if command[0] == OUT:
        remove(*command[1:])
    
    print(memory)
