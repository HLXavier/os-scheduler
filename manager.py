IN = 'IN'
OUT = 'OUT'

FIRST_FIT = 'ff'
BEST_FIT = 'bf'
WORST_FIT = 'wf'
CIRCULAR_FIT = 'cf'


class Manager:

    def __init__(self, space):
        self.space = space
        self.memory = [(None, space)]
        self.fits = {
            FIRST_FIT: self.first_fit,
            BEST_FIT: self.best_fit,
            WORST_FIT: self.worst_fit,
            CIRCULAR_FIT: self.circular_fit
        }
    

    def simulate(self, commands, fit):
        fit = self.fits[fit]

        for command in commands:
            if command[0] == IN:
                _, pid, size = command
                pos = fit(size)

                if pos != None:
                    self.add(pid, size, pos)
                else:
                    print("ESPAÇO INSUFICIENTE DE MEMÓRIA")

                str_command = f'{command[0]}({pid}, {size})'
            
            if command[0] == OUT:
                self.remove(command[1])
                str_command = f'{command[0]}({command[1]})'

            str_memory = ' | '.join([f'{pid}:{size}' for pid, size in self.memory])
            print(f'{str_command:<10} | {str_memory} |')


    def add(self, pid, size, pos):
        _, free = self.memory[pos]

        if free > size:
            self.memory.insert(pos, (pid, size))
            self.memory[pos+1] = (None, free-size)

        if free == size:
            self.memory[pos] = (pid, size)

    
    def compact(self, pos1, pos2):
        _, size1 = self.memory[pos1]
        pid2, size2 = self.memory[pos2]

        if pid2 == None:
            self.memory[pos1] = (None, size1 + size2)
            self.memory.pop(pos2)


    def remove(self, pid):
        for pos in range(len(self.memory)):
            mem_pid, mem_size = self.memory[pos]

            if mem_pid == pid:
                self.memory[pos] = (None, mem_size)

                next = pos + 1
                prev = pos - 1

                if next < len(self.memory):
                    self.compact(pos, next)
                
                if prev >= 0:
                    self.compact(pos, prev)

                return
        
        print("PROCESSO NÃO ENCONTRADO")


    # --- FIT STRATEGIES ---
    def first_fit(self, size):
        for pos in range(len(self.memory)):
            cur_pid, cur_size = self.memory[pos]
            if cur_pid == None and cur_size >= size:
                return pos
        
        return None


    def best_fit(self, size):
        min_pos = None
        min_size = None

        for pos in range(len(self.memory)):
            cur_pid, cur_size = self.memory[pos]
            if cur_pid == None and cur_size >= size:
                if min_pos == None or min_size > cur_size:
                    min_pos = pos
                    min_size = cur_size 
        
        return min_pos


    def worst_fit(self, size):
        max_pos = None
        max_size = None

        for pos in range(len(self.memory)):
            cur_pid, cur_size = self.memory[pos]
            if cur_pid == None and cur_size >= size:
                if max_pos == None or max_size < cur_size:
                    max_pos = pos
                    max_size = cur_size 
        
        return max_pos


    def circular_fit(self, size):
        return
