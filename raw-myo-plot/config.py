import json, os

# Filename for output
CONFIG_FILE = 'myo.config'

def config():
    # Function for creating config file for user
    
    # Gets SDK path from user
    sdk_path = input('Filepath to MYO SDK bin folder. MYO SDK is included within this repo'
                        r'(Ex. C:\Users\YOU\Documents\myo-sdk-win-0.9.0\bin): ')
    
    if os.path.exists(CONFIG_FILE):
        out = load_config()
        out.update({'sdk_path': sdk_path})
    else:
        # Formats into dict to be output as JSON
        out = {'sdk_path': sdk_path}
    
    # Outputs data
    save_config(out)
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
    
def save_config(config_dict):
    # Function to save dictionary of config data
    
    _f = open(CONFIG_FILE, 'w')
    json.dump(config_dict, _f)
    _f.close()
    
    print('Config file saved!')
    
if __name__ == '__main__':
    # If this file is run, config file is to be set up then tests load_config
    config()
    load_config()