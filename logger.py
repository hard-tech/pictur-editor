logFile = 'command.log'

def log(msg):
    """
    
    """

    with open(logFile, 'a') as f:
        f.write(msg + '\n')

def show_log():
    try:
        with open(logFile, 'r') as f:
            print(f.read())
    except FileNotFoundError as e:
        print(f'Cannot open {logFile}. error={e}')