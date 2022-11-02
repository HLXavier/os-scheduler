EMPTY = 'empty'
VERBOSE = 'verbose'

STRATEGIES = [EMPTY, VERBOSE]


class Logger:

    def __init__(self, strategy=EMPTY):
        self.strategies = {
            EMPTY: self.log_empty,
            VERBOSE: self.log_verbose
        }

        self.log = self.strategies[strategy]
        

    def command_to_str(self, command):
        if len(command) == 3:
            op, pid, size = command
            return f'{op}({pid}, {size})'
        else:
            op, pid = command
            return f'{op}({pid})'


    def log_empty(self, command, memory, space):
        str_command = self.command_to_str(command)

        str_memory = []
        for pid, size in memory:
            fix = '0' * (len(str(space)) - len(str(size)))
            segment = f'{fix}{size}'

            if pid == None:
                str_memory.append(segment)
        
        str_memory = ' | '.join(str_memory)
            
        print(f'{str_command:<10} | {str_memory} |')
    

    def log_verbose(self, command, memory, space):
            str_command = self.command_to_str(command)

            str_memory = []
            for pid, size in memory:
                fix = '0' * (len(str(space)) - len(str(size)))
                segment = f'({pid}) {fix}{size}'
                str_memory.append(segment)

            str_memory = ' | '.join(str_memory).replace('None', '-')
            
            print(f'{str_command:<10} | {str_memory} |')
