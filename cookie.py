import  requests
from pyquery import PyQuery as pq
class Login(object):
    def __init__(self):
        self.headers={
            'Host': 'api.github.com',

            'Referer': 'https:// github.com /login',
            'User - Agent': 'Mozilla / 5.0(WindowsNT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 57.0.2987  .133 Safari / 537.36'
        }
        self.login_url="https://github.com/login"
        self.login_session='https://github.com/session'
        self.login_setting='https://github.com/settings/profile'
        self.session=requests.Session()
        self.Password='qq60872141'
        self.emali='602872141@qq.com'
    def get_token(self):
        response = self.session.get( self.login_url)
        print(response.status_code)
        if response.status_code == 200:
            doc = pq(response.text)
            py_query = doc('.application-main #js-pjax-container #login > form > input[type="hidden"]:nth-child(2)')
            return py_query.attr('value')

    def login(self,token):
        post_data={
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': token,
            'login': self.emali,
            'password': self.Password
        }
        session_post = self.session.post(self.login_session, data=post_data)
        print(session_post.status_code)
        if session_post.status_code == 200 :
            print('200————session_post')
        session_get = self.session.get(self.login_setting)
        if session_get.status_code == 200:
            print('gool')
    def main(self):
        token = self.get_token()
        self.login(token)

if __name__=='__main__':
    login=Login()
    login.main()