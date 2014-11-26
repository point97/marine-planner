import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.exceptions import FieldError


class PlanningUnitsTests(unittest.TestCase):
    
    def setUp(self):
        self.user = 'nobody'
        self.password = 'password'
        self.email = 'nobody@nowhere.io'
        User.objects.create_superuser(self.user, self.email, self.password)
    
    def tearDown(self):
        User.objects.all().delete()
    
    def testMP414(self):
        return
        c = Client()
        c.login(username=self.user, password=self.password)
        params = {
            'user': None,
            'input_parameter_depth': True,
            'input_min_depth': 10,
            'input_max_depth': 50,
            'input_depth': 0,
            'name': 'Johnny B Goode',
            'description': 'Way back up in the woods among the evergreens' 
        }
        
        response = c.post('/features/scenario/form/', params)

        self.assertEqual(response.status_code, 200)
        
    def testLeaseBlockFormValid(self):
        c = Client()
        c.login(username=self.user, password=self.password)
        params = {
            'user': None,
            'name': 'Polly',
            'description': 'Have a seed', 
            'bathy_avg': False, 
            'bathy_avg_input': 0, 
            'bathy_avg_min': 0, 
            'bathy_avg_max': 0, 
            'wind_avg': True, 
            'wind_avg_input': 0, 
            'wind_avg_min': 200, 
            'wind_avg_max': 400, 
            'subs_mind': False, 
            'subs_mind_input': 0, 
            'subs_mind_min': 0, 
            'subs_mind_max': 0, 
            'coast_avg': False, 
            'coast_avg_input': 0, 
            'coast_avg_min': 0, 
            'coast_avg_max': 0, 
            'mangrove_p': False, 
            'mangrove_p_input': 0, 
            'mangrove_p_min': 0, 
            'mangrove_p_max': 0, 
            'coral_p_': False, 
            'coral_p_input': 0, 
            'coral_p_min': 0, 
            'coral_p_max': 0, 
            'subveg_p': False, 
            'subveg_p_input': 0, 
            'subveg_p_max': 0, 
            'subveg_p_min': 0, 
            'protarea_p': False, 
            'protarea_p_input': 0, 
            'protarea_p_min': 0, 
            'protarea_p_max': 0, 
            'pr_apc_p': False, 
            'pr_apc_p_input': 0, 
            'pr_apc_p_min': 0, 
            'pr_apc_p_max': 0, 
            'pr_ape_p': False, 
            'pr_ape_p_input': 0, 
            'pr_ape_p_min': 0, 
            'pr_ape_p_max': 0, 
            'vi_apc_p': False, 
            'vi_apc_p_input': 0, 
            'vi_apc_p_min': 0, 
            'vi_apc_p_max': 0, 
        }
        
        response = c.post('/features/scenario/form/', params)

        self.assertEqual(response.status_code, 201)
        
