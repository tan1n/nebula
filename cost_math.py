from math import ceil


def led_count(pos):
    return ceil((pos*0.0254)*30) - 1


size = 24
hz = ceil((size*.875))  # width in inch
vt = ceil((size*.49))  # height in inch
costs = {
    'esp_price': 190,
    # 'buckle': 11*4,
    'l_con': 13*2,
    'led_cabble': 28,
    'led_price': (led_count(hz)+led_count(vt)*2)*(157/30),
    'shell': 55,
    'usb': 55,
    'others': 30
}
total_cost = sum(costs.values())
print(total_cost)
print(led_count(hz), led_count(vt),
      ((led_count(hz)+led_count(vt))*2)-led_count(hz))
