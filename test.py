import json
# config_file = open('config.json');
# configs = json.load(config_file);
# print( 'Hola' if configs['display_size'] == '' else 'Heda')
# configs['display_size'] = 15;
# with open('config.json','w') as file:
#     json.dump(configs,file)
# print(configs)
import subprocess


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


print(process_exists('nebula.exe'))
