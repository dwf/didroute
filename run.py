import yaml
from didroute.api import VoipMS
import didroute.app

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=argparse.FileType('r'),
                        help='Config for didroute.')
    args = parser.parse_args()
    config = yaml.load(args.config)
    didroute.app.api = VoipMS(**config['credentials'])
    did = config['dids'][0]
    didroute.app.did_id = did['id']
    didroute.app.did_routes = did['routes']
    # I have no idea if this is a good idea or not. I am not running this
    # on a public web server. Maybe you shouldn't either.
    didroute.app.app.secret_key = str(hash(str(config)))
    didroute.app.app.run(**config['server'])
