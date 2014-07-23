from django.core.management.base import BaseCommand, CommandError
import json
import requests


class Command(BaseCommand):
    args = 'host'
    help = 'List available MBTiles layers from <host>'

    def handle(self, *args, **options):
        if len(args) < 1:
            self.stderr.write('Missing <host> argument')
            return 
        
        host = args[0]
        rpc_url = 'http://%s/api/' % host
        tile_pattern = "http://" + host + "%s"
        
        command = {
            'json-rpc': '2.0',
            'method': 'dataset_list',
            'id': 42,
        }
        
        headers = {'content-type': 'application/json'}

        r = requests.post(rpc_url, data=json.dumps(command), headers=headers)
        if r.status_code != 200: 
            self.stderr.write("Something went wrong (status = %d)" % r.status_code)
            return
    
        response = r.json()
        assert 'result' in response
        assert 'id' in response
        assert response['id'] == 42
        assert 'jsonrpc' in response
        assert response['jsonrpc'] == "2.0"
        
        self.stdout.write("Available layers: ")
        for layer in response['result']:
            xyx_url = tile_pattern % layer['url']
                     
            
            self.stdout.write("%s, %s" % (layer['name'], xyx_url))
                
        self.stdout.write('')
