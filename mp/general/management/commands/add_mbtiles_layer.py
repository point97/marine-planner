from django.core.management.base import BaseCommand, CommandError
from data_manager.models import Layer, Theme
import json
import requests


class Command(BaseCommand):
    args = 'host layer_name'
    help = 'Add the <name> MBTiles layer from <host>'

    def handle(self, *args, **options):
        if len(args) < 2:
            self.stderr.write('Missing arguments')
            return 
        
        host = args[0]
        layer_name = args[1]
        rpc_url = 'http://%s/api/' % host
        tile_pattern = "http://" + host + "%s"
        
        command = {
            'json-rpc': '2.0',
            'method': 'dataset_get',
            'params': [layer_name],
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
        
        if response.get('error'):
            msg = response['error'].get('message')
            self.stderr.write(msg)
            return 
        
        layer = response['result']
        layer['url'] = tile_pattern % layer['url']
        layer['preview'] = tile_pattern % layer['preview']
        self.stdout.write(json.dumps(layer))
        
        

        theme = Theme.objects.get(name='Tiles')
        
        new_layer = Layer()
        new_layer.name = layer['name']
        new_layer.layer_type = 'XYZ'
        new_layer.url = layer['url']
        new_layer.save()
        new_layer.themes.add(theme)
        
        self.stdout.write('')
