# services/partido/project/tests/test_users.py


import json
import unittest

from project import db

from project.api.models import User

from project.tests.base import BaseTestCase


def add_user(nombre, email, password, apellido, fechaNacimiento, genero):
        user = User(
            nombre=nombre, email=email, password=password,
            apellido=apellido, fechaNacimiento=fechaNacimiento,
            genero=genero
            )
        db.session.add(user)
        db.session.commit()
        return user


class TestUserService(BaseTestCase):
    def test_user(self):
        response = self.client.get('/user/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_user(self):
        with self.client:
            response = self.client.post(
                '/user',
                data=json.dumps({
                    'nombre': 'sol',
                    'email': 'solmamani@upeu.edu.pe',
                    'password': 'palteas2106',
                    'apellido': 'apellido',
                    'fechaNacimiento': 'fechaNacimiento',
                    'genero': 'genero'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'solmamani@upeu.edu.pe ha sido agregado!', data['mensaje'])
            self.assertIn('satisfactorio', data['estado'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/user',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_user_invalid_json_keys(self):
        """
        Asegurando de que se produce un error si el objeto JSON no tiene
        un key de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/user',
                data=json.dumps({'email': 'solmamani@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                '/user',
                data=json.dumps({
                    'nombre': 'sol',
                    'email': 'solmamani@upeu.edu.pe',
                    'password': 'palteas2106',
                    'apellido': 'apellido',
                    'fechaNacimiento': 'fechaNacimiento',
                    'genero': 'genero'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/user',
                data=json.dumps({
                    'nombre': 'sol',
                    'email': 'solmamani@upeu.edu.pe',
                    'password': 'palteas2106',
                    'apellido': 'apellido',
                    'fechaNacimiento': 'fechaNacimiento',
                    'genero': 'genero'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Disculpe. Este email ya existe.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_user(self):
        user = add_user(
            'abigail',
            'abisolcita@gmail.com',
            'palteas2106',
            'mamani',
            '21/06/98',
            'femenino'
        )
        with self.client:
            response = self.client.get(f'/user/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('abigail', data['data']['nombre'])
            self.assertIn('abisolcita@gmail', data['data']['email'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_user_no_id(self):
        """Asegurando de que se lanze un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/user/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_user_incorrect_id(self):
        """Asegurando de que se lanze un error si el id no existe."""
        with self.client:
            response = self.client.get('/user/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_all_user(self):
        user = add_user(
            'abigail',
            'abisolcita@gmail.com',
            'palteas2106',
            'mamani',
            '21/06/98',
            'femenino'
        )
        user = add_user(
            'sol',
            'solmamani@upeu.edu.pe',
            'palteas2106', 'mamani',
            '21/06/98',
            'femenino')
        print(user)
        with self.client:
            response = self.client.get('/user')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['user']), 2)
            self.assertIn('abigail', data['data']['user'][0]['nombre'])
            self.assertIn(
                'abisolcita@gmail.com', data['data']['user'][0]['email'])
            self.assertIn('sol', data['data']['user'][1]['nombre'])
            self.assertIn(
                'solmamani@upeu.edu.pe', data['data']['user'][1]['email'])
            self.assertIn('satisfactorio', data['estado'])

    def test_main_no_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos los usuarios', response.data)
        self.assertIn(b'<p>No user!</p>', response.data)

    def test_main_with_user(self):
        user = add_user(
            'abigail',
            'abisolcita@gmail.com',
            'palteas2106',
            'mamani',
            '21/06/98',
            'femenino'
        )
        user = add_user(
            'sol',
            'solmamani@upeu.edu.pe',
            'palteas2106', 'mamani',
            '21/06/98',
            'femenino')
        print(user)
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'sol', response.data)
            self.assertIn(b'abigail', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    nombre='sol', email='solmamani@upeu.edu.pe',
                    password='password', apellido='mamani',
                    fechaNacimiento='21/06/98', genero='femenino'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'sol', response.data)


if __name__ == '__main__':
    unittest.main()
