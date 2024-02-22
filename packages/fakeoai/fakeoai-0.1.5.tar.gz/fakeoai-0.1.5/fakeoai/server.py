from flask import request, jsonify, g, session, render_template, Flask, redirect, url_for, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import timedelta
from dotenv import load_dotenv
from os.path import join, abspath, dirname
import time
import json
import requests

load_dotenv()

class FakeOAI(Flask):
    build_id = '3Ogfe3rbepk5p-l8Fm-xW'
    api_proxy = "https://api.fakeopenai.cn"

    def __init__(self):
        resource_path = abspath(join(dirname(__file__), 'flask'))
        super().__init__(__name__, static_url_path="",
            static_folder=join(resource_path, 'static'),
            template_folder=join(resource_path, 'templates'))
        self.config.from_prefixed_env()
        self.init_config()
        self.wsgi_app = ProxyFix(self.wsgi_app)
        self.errorhandler(404)(self.page_not_found)
        self.before_request(self._before_request)
        self.after_request(self._after_request)

        # 登录相关
        self.get('/auth/login')(self.auth_get)
        self.get('/auth/token_login')(self.token_login)
        self.post('/auth/login')(self.auth_post)
        self.get('/auth/logout')(self.logout)

        # 主要的页面
        self.get('/')(self.index)
        self.get('/chat')(self.chat)
        self.get('/c/<conversation_id>')(self.chat_conversation)

        # gpts相关
        self.get('/gpts')(self.gpts)
        self.get('/gpts/mine')(self.gpts_mine)
        self.get('/gpts/editor')(self.gpts_editor)
        self.get('/gpts/editor/<slug>')(self.gpts_editor_id)
        self.get('/g/<gpt_id>/c/<conversation_id>')(self.gpt_conversation)
        self.get('/g/<gizmoId>')(self.g_id)

        # 其他
        self.get('/api/auth/session')(self.auth_session)
        self.get('/share/<share_id>')(self.share)
        self.get('/_next/data/<path:url>')(self.next_data)

    def init_config(self):
        self.secret_key = 'lby20010429'
        self.config['SESSION_REFRESH_EACH_REQUEST'] = False
        self.config['SESSION_COOKIE_NAME'] = '_Secure-next-auth.session-token'
        self.config['SESSION_COOKIE_SECURE'] = not self.config['DEBUG']
        self.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        self.manager = self.config.get('MANAGER')
        self.social_link = self.config.get('SOCIAL_LINK')
        self.navigate_link_label = self.config.get('NAVIGATE_LINK_LABEL')

    def _chatgpt_proxy(self, url=None):
        return self.proxy_request(self.api_proxy)
        
    def _before_request(self):
        g.build_id = self.build_id
        g.access_token = session.get('accessToken')

    def _after_request(self, resp):
        resp.headers['X-Server'] = self.manager
        if not session.get('accessToken') and request.cookies.get('_Secure-next-auth.session'):
            session.clear()
        return resp
    
    def page_not_found(self, e):
        return self.render('_error', statusCode=404), 404
    
    def get_next_data(self, page: str, pageProps, query = {}):
        return {
            'props': {
                'pageProps': pageProps,
                '__N_SSP': True
            },
            'page': page,
            'query': query,
            'buildId': self.build_id,
            'assetPrefix': '',
            'isFallback': False,
            'gssp': True,
            'scriptLoader': [],
        }
    
    def get_page_props(self): 
        props = {
            'ageVerificationDeadline': None,
            'allowBrowserStorage': True,
            'canManageBrowserStorage': False,
            'geoOk': True,
            'isUserInCanPayGroup': True,
            'serviceAnnouncement': {
                'paid': {},
                'public': {},
            },
            'serviceStatus': {},
            'cfConnectingIp': '0.0.0.0',
            'serverPrimedAllowBrowserStorageValue': True,
            'showCookieConsentBanner': False,
            'userCountry': 'US',
        }
        if session.get('user'):
            props.update({
                'user': session.get('user'),
            })
        gizmoId = request.view_args.get('gizmoId') or request.args.get('gizmoId')
        if gizmoId and session.get('accessToken'):
            res = requests.get(f'{self.api_proxy}/backend-api/gizmos/{gizmoId}', headers={'Authorization':session['accessToken']})
            if res.status_code == 200:
                props.update({
                    'kind': 'chat_page',
                    'gizmo': json.loads(res.content)
                })
        return props
    
    def render(self, name: str, **kargs):
        try:
            white_list = ['auth/login', '_error']
            if session.get('accessToken') or name in white_list:
                if name == 'auth/login' and session.get('accessToken'):
                    return redirect(url_for('index'))
                pageProps = {}
                pageProps.update(self.get_page_props())
                pageProps.update(kargs)
                return render_template(f'{name}.html', __NEXT_DATA__=self.get_next_data(f'/{name}', pageProps, request.view_args), 
                    manager=self.manager, social_link=self.social_link, navigate_link_label=self.navigate_link_label)
            else:
                return redirect(url_for('auth_get'))
        except Exception as e:
            return jsonify({ 'detail': str(e) }), 500
        
    def set_session_info(self, info):
        session.update(info)
        self.permanent_session_lifetime = timedelta(seconds=info['user']['exp'] - int(time.time()))
        session.permanent = True 
        
    def auth_get(self):
        return render_template('auth.html', manager=self.manager, social_link=self.social_link)
    
    def token_login(self):
        try:
            access_token = request.args.get("access_token")
            if not access_token:
                raise Exception('access_token is required')
            res = requests.get(f'{self.api_proxy}/auth/token_login?access_token={access_token}')
            json_data: dict = json.loads(res.content)
            if not res.ok:
                raise Exception(json_data.get('detail'))
            self.set_session_info(json_data)
            return jsonify({'detail':'success'})
        except Exception as e:
            return jsonify({'detail':str(e)}), 500
    
    def auth_post(self):
        try:
            res = requests.post(f'{self.api_proxy}/auth/login', data=request.get_data(), headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }, cookies=request.cookies)
            json_data: dict = json.loads(res.content)
            if not res.ok:
                raise Exception(json_data.get('detail'))
            self.set_session_info(json_data)
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('auth.html', error=str(e)), 500
    
    def logout(self):
        session.clear()
        return redirect(url_for('auth_get'))
    
    def share(self, share_id):
        res = requests.get(f'{self.api_proxy}/backend-api/share/{share_id}', headers={'Authorization':session['accessToken']})
        if res.status_code == 200:
            share_detail = json.loads(res.content)
            return render_template('share/[[...shareParams]].html', __NEXT_DATA__=self.get_next_data('/share/[[...shareParams]]', {
                'serverPrimedAllowBrowserStorageValue': True,
                'isStorageComplianceEnabled': False,
                'sharedConversationId': share_id,
                'serverResponse': {
                    'type': 'data',
                    'data': share_detail,
                },
                'continueMode': False,
                'moderationMode': False,
                'chatPageProps': {},
                'plugins': None,
                'isGizmoLive': True,   
            }, { 'shareParams': [share_id] }))
        return
    
    def auth_session(self):
        return jsonify({ key: value for key, value in session.items() if key != '_permanent' })

    def index(self):
        return self.render('[[...default]]')
    
    def chat_conversation(self, conversation_id):
        return self.render('[[...default]]')
    
    def g_id(self, gizmoId):
        return self.render('g/[gizmoId]')
    
    def gpt_conversation(self, gpt_id, conversation_id):
        return self.render('g/[gizmoId]/c/[convId]')
    
    def gpts(self):
        return self.render('gpts')
    
    def gpts_mine(self):
        return self.render('gpts/mine')
    
    def gpts_editor(self):
        return self.render('gpts/editor')
    
    def gpts_editor_id(self, slug):
        return self.render('gpts/editor/[slug]')
    
    def chat(self):
        return redirect(url_for('index'))
        
    def next_data(self, url):
        response = make_response("{}")
        response.status_code = 200
        response.headers.add('X-Middleware-Skip', '1')
        response.headers.pop('Content-Type')
        return jsonify({
            '__N_SSP': True,
            'pageProps': self.get_page_props(),
        }) if session.get('accessToken') and request.headers.get('Purpose') != 'prefetch' else response