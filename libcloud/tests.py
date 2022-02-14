from django.test import TestCase



class BaseTest(TestCase):
    def setUp(self):
        self.register_url = '/register/'
        self.login_url = '/login/'
        self.user = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'Fineline94$',
            'password2': 'Fineline94$'
        }
        self.user_short_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'tes',
            'password2': 'tes',

        }
        self.user_unmatching_password = {

            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'teslatt',
            'password2': 'teslatto',

        }

        self.user_invalid_email = {

            'email': 'test.com',
            'username': 'username',
            'password1': 'teslatt',
            'password2': 'teslatto',
            'name': 'fullname'
        }
        return super().setUp()

class RegisterTest(BaseTest):
   def test_can_view_page_correctly(self):
       response=self.client.get(self.register_url)
       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'libcloud/register.html')

   def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user)
        self.assertEqual(response.status_code,302)

   def test_cant_register_user_withshortpassword(self):
        response=self.client.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,400)

   def test_cant_register_user_with_unmatching_passwords(self):
        response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
        self.assertEqual(response.status_code,400)
   def test_cant_register_user_with_invalid_email(self):
        response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
        self.assertEqual(response.status_code,400)

   def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400)

class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'libcloud/login.html')
    def test_login_success(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response= self.client.post(self.login_url,{
            'username':  self.user.get('username'),
            'password': self.user.get('password1')},format='text/html')
        self.assertEqual(response.status_code,302)
    def test_cantlogin_with_unverified_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response = self.client.post(self.login_url, {
            'username': 'wrong',
            'password': 'wrong'}, format='text/html')
        self.assertEqual(response.status_code,401)

    def test_cantlogin_with_no_username(self):
        response= self.client.post(self.login_url,{'password':'passwped','username':''},format='text/html')
        self.assertEqual(response.status_code,401)
    def test_cantlogin_with_no_password(self):
        response= self.client.post(self.login_url,{'username':'passwped','password':''},format='text/html')
        self.assertEqual(response.status_code,401)


