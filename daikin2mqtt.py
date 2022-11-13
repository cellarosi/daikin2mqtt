import yaml
import argparse

from paho.mqtt.client import Client
from daikinapi import Daikin

def _load_config(path):

    with open(path, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    return cfg

   
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get info from Daikin AC to mqtt.')
    parser.add_argument('--config',  default='config.yaml',
                        help='yaml config file. Default config.yaml')
    args = parser.parse_args()
    
    config = _load_config(args.config)

    API = Daikin(config['daikin']['host'])

    client = Client(client_id = config['mqtt']['client_id'])
    client.username_pw_set(username=config['mqtt']['auth']['username'],password=config['mqtt']['auth']['password'])
    client.connect(config['mqtt']['host'])

    client.publish(topic = "{}/{}".format(config['mqtt']['client_id'], config['mqtt']['topic']['inside_temperature']), payload = API.inside_temperature) 
    client.publish(topic = "{}/{}".format(config['mqtt']['client_id'], config['mqtt']['topic']['outside_temperature']), payload = API.outside_temperature) 
