import mss
import numpy as np
import cv2
# config_file = open('config.json');
# configs = json.load(config_file);
# print( 'Hola' if configs['display_size'] == '' else 'Heda')
# configs['display_size'] = 15;
# with open('config.json','w') as file:
#     json.dump(configs,file)
# print(configs)
# import subprocess


# def process_exists(process_name):
#     call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
#     # use buildin check_output right away
#     output = subprocess.check_output(call).decode()
#     # check in last line for process name
#     last_line = output.strip().split('\r\n')[-1]
#     # because Fail message could be translated
#     return last_line.lower().startswith(process_name.lower())

# print(process_exists('nebula.exe'))
# {'top': 350, 'left': 0, 'width': 350, 'height': 730}
# {'top': 0, 'left': 0, 'width': 1920, 'height': 350}
# {'top': 350, 'left': 1570, 'width': 350, 'height': 730}
with mss.mss() as sct:
    screen = np.array(
        sct.grab({'top': 350, 'left': 1570, 'width': 350, 'height': 730}))
    # img = cv2.resize(screen, res, interpolation=INTER_AREA)
    output = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    cv2.imshow('test', screen)
    # output = cv2.GaussianBlur(output, (5, 5), 0)
    cv2.waitKey(0)  # waits until a key is pressed
    cv2.destroyAllWindows()
