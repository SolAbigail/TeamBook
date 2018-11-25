# services/partido/project/tests/test_users.py
import json
import unittest

from project.tests.base import BaseTestCase


class TestPartidoService(BaseTestCase):
    """Prueba para el servicio partido."""

    def test_partido(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get('/partido/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_partido(self):

        with self.client:
            response = self.client.post(
                '/partido',
                data=json.dumps({
                    'nombre': 'Activate',
                    'fecha': '24/11/18',
                    'hora': '10:00 am',
                    'lugar': 'Universidad Peruana Union',
                    'descripcion': 'Lozas UPeU',
                    'deporte': 'BASQUET',
                    'cantJugadores': '10'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'Partido Activate ha sido agregado!', data['mensaje'])
            self.assertIn('satisfactorio', data['estado'])


if __name__ == '__main__':
    unittest.main()
