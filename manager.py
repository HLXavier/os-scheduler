from logger import Logger


IN = 'IN'
OUT = 'OUT'

FIRST_FIT = 'ff'
BEST_FIT = 'bf'
WORST_FIT = 'wf'
CIRCULAR_FIT = 'cf'


class Manager:

    def __init__(self, space, log_strategy):
        self.space = space
        self.memory = [(None, space)]

        self.fits = {
            FIRST_FIT: self.first_fit,
            BEST_FIT: self.best_fit,
            WORST_FIT: self.worst_fit,
            CIRCULAR_FIT: self.circular_fit
        }

        self.last = 0

        # offset of the pointer from the end of the self.last block
        # used to keep track of the pointer when it's in the middle
        # of a block
        self.margin = 0

        self.logger = Logger(log_strategy)
    

    def simulate(self, commands, fit):
        fit = self.fits[fit]

        for command in commands:
            op, pid, size = command

            if op == IN:
                pos = fit(size)

                if pos != None:
                    self.add(pid, size, pos)
                else:
                    print("ESPAÇO INSUFICIENTE DE MEMÓRIA")
            
            if op == OUT:
                self.remove(pid)
            
            self.logger.log(command, self.memory, self.space)


    def add(self, pid, size, pos):
        _, free = self.memory[pos]
        self.last = pos

        if free > size:
            self.memory.insert(pos, (pid, size))
            self.memory[pos+1] = (None, free-size)

        if free == size:
            self.memory[pos] = (pid, size)

    
    def compact(self, pos1, pos2):
        _, size1 = self.memory[pos1]
        _, size2 = self.memory[pos2]

        self.memory[pos1] = (None, size1 + size2)
        self.memory.pop(pos2)


    def remove(self, pid):
        for pos in range(len(self.memory)):
            mem_pid, mem_size = self.memory[pos]

            if mem_pid == pid:
                # empty the block
                self.memory[pos] = (None, mem_size)
                self.last = pos

                next = pos + 1
                prev = pos - 1

                # join the emptied block with it's
                # immediate right neighbor
                if next < len(self.memory):
                    next_pid, next_size = self.memory[next]
                    if next_pid == None:
                        self.compact(pos, next)
                        self.margin = next_size
                
                # join the emptied block with it's
                # immediate left neighbor
                if prev >= 0:
                    prev_pid, _ = self.memory[prev]
                    if prev_pid == None:
                        self.compact(pos, prev)
                        self.last -= 1

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
        margin = self.margin
        self.margin = 0

        # try to insert in the self.last block
        if margin >= size:

            # split the self.last block in two at the margin
            _, mem_size  = self.memory[self.last]
            self.memory.insert(self.last, (None, mem_size - margin))
            self.memory[self.last+1] = (None, margin)

            # return the index of the second block that resulted from
            # the split, the program will be inserted at the beginning
            # of that second block
            return self.last+1

        # if the margin is smaller than the size, we cannot insert
        # the program in the self.last block and must search for a new one
        
        start = self.last + 1
        for pos in range(start, start + len(self.memory)):

            cur_pid, cur_size = self.memory[pos % len(self.memory)]
            if cur_pid == None and cur_size >= size:
                return pos % len(self.memory)
        
        return None
