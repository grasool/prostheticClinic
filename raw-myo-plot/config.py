import json

CONFIG_FILE = 'myo.config'

def config():
    sdk_path = input(r'Filepath to MYO SDK bin folder (Ex. C:\Users\YOU\Documents\myo-sdk-win-0.9.0\bin): ')
    
    out = {'sdk_path': sdk_path}
    
    _f = open(CONFIG_FILE, 'w')
    json.dump(out, _f)
    _f.close()
    print('Config file saved!')
    
def load_config():
    _f = open(CONFIG_FILE, 'r')
    out = json.loads(_f.read())
    
    return out
    
if __name__ == '__main__':
    config()
    print(load_config())