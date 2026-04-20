import unittest
from main import db, create_app
from main.models import User, Prediction, Feedback

class TestConfig:
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test'


class VehicleIQTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Destroy temp database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ---------- Helper Methods ----------

    def register(self, username, email, password, confirm_password):
        return self.client.post(
            '/register',
            data=dict(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password
            ),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.client.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    # ---------- Basic Route Tests ----------

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    # ---------- Authentication Tests ----------

    def test_user_registration(self):
        response = self.register('testuser', 'test@example.com', 'password123', 'password123')

        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')

        # Duplicate username
        response = self.register('testuser', 'other@example.com', 'password123', 'password123')
        self.assertEqual(response.status_code, 200)

        # Password mismatch
        response = self.register('newuser', 'new@example.com', 'password123', 'wrongpass')
        self.assertEqual(response.status_code, 200)

    def test_user_login_logout(self):
        username = 'loginuser'
        email = 'login@example.com'
        password = 'secret_password'

        self.register(username, email, password, password)

        # Login
        response = self.login(email, password)
        self.assertEqual(response.status_code, 200)
        self.assertIn(username.encode(), response.data)

        # Logout
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign', response.data)

        # Wrong password
        response = self.login(email, 'wrongpassword')
        self.assertEqual(response.status_code, 200)

    # ---------- Access Control ----------

    def test_predict_requires_login(self):
        response = self.client.get('/predict', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    # ---------- Feature Tests ----------

    def test_feedback_submission(self):
        self.register('feedbacker', 'fb@example.com', 'pass', 'pass')
        self.login('fb@example.com', 'pass')

        response = self.client.post(
            '/feedback',
            data=dict(rating=5, message='Great app!'),
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            fb = Feedback.query.filter_by(message='Great app!').first()
            self.assertIsNotNone(fb)
            self.assertEqual(fb.rating, 5)

    def test_prediction_submission(self):
        self.register('predictor', 'predict@example.com', 'pass', 'pass')
        self.login('predict@example.com', 'pass')

        data = {
            'model_year': 2020,
            'milage': 15000,
            'transmission': '1',
            'condition': '1',
            'cc': 1500,
            'age': 4,
            'power_steering': '1',
            'push_start': '1',
            'car_model': 'model_toyota axio g grade',
            'fuel_type': 'fuel_type_petrol',
            'location': 'location_colombo',
            'vehicle_type': 'car/sedan_car',
            'color': 'ext_col_pearl white'
        }

        response = self.client.post('/predict', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            prediction = Prediction.query.filter_by(
                model='model_toyota axio g grade'
            ).first()

            self.assertIsNotNone(prediction)
            self.assertEqual(prediction.model_year, '2020')

    def test_account_update(self):
        self.register('oldname', 'old@example.com', 'pass', 'pass')
        self.login('old@example.com', 'pass')

        response = self.client.post(
            '/account',
            data=dict(username='newname', email='new@example.com'),
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            user = User.query.filter_by(username='newname').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'new@example.com')


if __name__ == '__main__':
    unittest.main()