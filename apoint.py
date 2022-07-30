import network

def open_ap():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='scope')
    ap.config(password='scopescope')
    ap.active(True)
    return ap

if __name__ == "__main__":
    open_ap()