def convert_line(line):
    command = line.replace(" ", "").replace("(", " ").replace(")", " ").replace(",", " ")

    if len(command.split()) > 2:
        op, pid, size = command.split()
        return op, pid, int(size)
    
    op, pid = command.split()
    return op, pid


def convert_file(file):
    case = open(f'cases/{file}', 'r')
    return [convert_line(line) for line in case]