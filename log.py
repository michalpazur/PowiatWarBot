def log_info(info):
    with open('log.txt', 'a') as f:
        f.write('{}\n'.format(info))

def log_error(error):
    log_info('[Error!]\n{}'.format(error))