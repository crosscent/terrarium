from django.test import TestCase

from rest_framework.test import APIClient

class CircularPotTest(TestCase):
    """Tests all the calculations done for circular pot
    """
    
    def test_all_floats(self):
        """Use only floats in the GET parameters to circular pot
        """
        client = APIClient()
        response = client.get('/api/calculation/circular_pot/?pot_radius={0}&seed_radius={1}'.format(5.5, 1.5)).data
        self.assertEqual(response["cluster_count"], 9)

    def test_all_integers(self):
        """Use only floats in the GET parameters to circular pot
        """
        client = APIClient()
        response = client.get('/api/calculation/circular_pot/?pot_radius={0}&seed_radius={1}'.format(5, 1)).data
        self.assertEqual(response["cluster_count"], 17)
    
    def test_mix_float_integer(self):
        """Use both float and integer in the GET parameters to circular pot
        """
        client = APIClient()
        response = client.get('/api/calculation/circular_pot/?pot_radius={0}&seed_radius={1}'.format(5, 1.5)).data
        self.assertEqual(response["cluster_count"], 8)

    def test_seed_larger_than_pot(self):
        """When the seed cluster radius exceeds the pot radius
        """
        client = APIClient()
        response = client.get('/api/calculation/circular_pot/?pot_radius={0}&seed_radius={1}'.format(1, 5)).data
        self.assertEqual(response["cluster_count"], 0)

    def test_only_pot_radius(self):
        """When only the radius of the pot is provided
        """
        client = APIClient()
        response = client.get('/api/calculation/circular_pot/?pot_radius={0}'.format(5)).data
        self.assertTrue(isinstance(response, str))

class RectangularPotTest(TestCase):
    """Tests all the calculations done for circular pot
    """

    endpoint = '/api/calculation/rectangular_pot/'
    
    def test_all_floats(self):
        """Use only floats in the GET parameters to circular pot
        """
        client = APIClient()
        response = client.get(self.endpoint + '?pot_length={0}&pot_width={0}&seed_radius={1}'.format(5.5, 1.5)).data
        self.assertEqual(response["cluster_count"], 1)

    def test_all_integers(self):
        """Use only floats in the GET parameters to circular pot
        """
        client = APIClient()
        response = client.get(self.endpoint + '?pot_length={0}&pot_width={0}&seed_radius={1}'.format(10, 1)).data
        self.assertEqual(response["cluster_count"], 25)
    
    def test_mix_float_integer(self):
        """Use both float and integer in the GET parameters to circular pot
        """
        client = APIClient()
        response = client.get(self.endpoint + '?pot_length={0}&pot_width={0}&seed_radius={1}'.format(10.5, 0.75)).data
        self.assertEqual(response["cluster_count"], 49)

    def test_seed_larger_than_pot(self):
        """When the seed cluster radius exceeds the pot radius
        """
        client = APIClient()
        response = client.get(self.endpoint + '?pot_length={0}&pot_width={0}&seed_radius={1}'.format(1, 10)).data
        self.assertEqual(response["cluster_count"], 0)

    def test_only_pot_length(self):
        """When only the radius of the pot is provided
        """
        client = APIClient()
        response = client.get(self.endpoint + '?pot_length={0}'.format(10)).data
        self.assertTrue(isinstance(response, str))
