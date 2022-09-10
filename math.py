from math import ceil

def led_count(pos):
    return ceil((((pos/2)/12)/3.33)*30) - 1

size = 24
hz = ceil((size*.875)*2)
vt = ceil((size*.49)*2)
costs = {
    'esp_price' : 190,
    'buckle' : 11*4,
    'l_con' : 13*2,
    'led_cabble' :28,
    'led_price' : (((led_count(hz)+led_count(vt))*2-led_count(hz))/30)*157,
    'shell' : 60,
    'usb' : 30,
    # 'others' : 40
}
total_cost = sum(costs.values())
print(total_cost);
print(led_count(hz),led_count(vt),((led_count(hz)+led_count(vt))*2)-led_count(hz))
