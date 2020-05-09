from datetime import datetime

def log_info(info):
    print(info)
    with open('log.txt', 'a', encoding = 'utf-8') as f:
        f.write('{}\n'.format(info))

def log_error(error):
    log_info('[Error {}]\n{}'.format(datetime.now(), error))