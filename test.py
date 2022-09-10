import json
config_file = open('config.json');
configs = json.load(config_file);
print( 'Hola' if configs['display_size'] == '' else 'Heda')
configs['display_size'] = 15;
with open('config.json','w') as file:
    json.dump(configs,file)
print(configs)