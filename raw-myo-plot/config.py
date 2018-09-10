import json

# Filename for output
CONFIG_FILE = 'myo.config'

def config():
    # Function for creating config file for user
    
    # Gets SDK path from user
    sdk_path = input(r'Filepath to MYO SDK bin folder (Ex. C:\Users\YOU\Documents\myo-sdk-win-0.9.0\bin): ')
    
    # Formats into dict to be output as JSON
    out = {'sdk_path': sdk_path}
    
    # Outputs data
    _f = open(CONFIG_FILE, 'w')
    json.dump(out, _f)
    _f.close()
    print('Config file saved!')
    
def load_config(test=0):
    # Function for loading previously created config file
    
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError('%s FILE NOT FOUND. MUST RUN config.py TO SETUP THIS FILE' % CONFIG_FILE)
    _f = open(CONFIG_FILE, 'r')
    out = json.loads(_f.read())
    
    if test:
        print('\n\nLoading config file tested and successful...\nContents: %s' % out)
        
    return out
    
if __name__ == '__main__':
    # If this file is run, config file is to be set up then tests load_config
    config()
    load_config()