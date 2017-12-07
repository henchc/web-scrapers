import requests
from bs4 import BeautifulSoup
from urllib import parse
import json
import pickle
import time
import re
import glob


class BasicSkillsCollege:

    def __init__(self, college):

        self.sess = requests.session()
        self.url = 'http://datamart.cccco.edu/Outcomes/BasicSkills_Cohort_Tracker.aspx'
        self.init_req = self.sess.get(self.url)
        self.init_req_soup = BeautifulSoup(self.init_req.content, 'html5lib')
        self.init_states = {tag['name']: tag['value']
                            for tag in self.init_req_soup.select('input[name^=__]')}
        self.college = college
        print(self.college)

    def parse_params(self, r):
        lst = re.search(r'\[.+\]', r.text).group()
        terms = lst.replace(
            '"',
            '').replace(
            '[',
            '').replace(
            ']',
            '').replace(
                "'",
            "").split(',')
        terms = [x.strip() for x in terms]

        tps = []
        for i in range(len(terms)):
            if (i + 2) % 2 == 0:
                tps.append((terms[i + 1], terms[i]))

        return tps

    def get_s_terms(self):
        data = self.init_states
        data['__CALLBACKID'] = 'ASPxRoundPanel1$ASPxComboBoxSTerm'
        data['__CALLBACKPARAM'] = 'c0:LECC|0;;LBCRI|4;0:-2;'
        data['DXScript'] = '1_243,1_138,1_237,1_164,1_141,1_135,1_226,1_234,1_162,1_170,1_161,1_229,1_159,1_227,1_165,1_143,1_176,1_151,1_232,1_149,7_50,7_53,7_48,7_52,1_235,1_218,1_228,1_210,1_184,1_136'
        data['DXCss'] = '0_224,1_28,0_226,0_115,1_10,0_117,0_143,7_2,0_145,../css/styles.css,../css/navigation-mininav.css,../css/design01.css,../css/footer-without-dark-container.css'
        data['ASPxRoundPanel1$ASPxComboBoxColl'] = self.college[0]
        data['ASPxRoundPanel1_ASPxComboBoxColl_VI'] = self.college[1]
        data['ASPxRoundPanel1$ASPxComboBoxColl$DDD$L'] = self.college[1]

        req = self.sess.post(self.url, data=data)

        sterms = self.parse_params(req)
        spring_2006 = [x[0] for x in sterms].index('Spring 2006')
        sterms = sterms[:spring_2006 + 1][::-1]

        return (data, sterms)

    def get_skills(self):
        data, sterms = self.get_s_terms()
        data['__CALLBACKID'] = 'ASPxRoundPanel1$ASPxComboBoxBSSub'
        data['ASPxRoundPanel1$ASPxComboBoxSTerm'] = sterms[0][0]
        data['ASPxRoundPanel1_ASPxComboBoxSTerm_VI'] = sterms[0][1]
        data['ASPxRoundPanel1$ASPxComboBoxSTerm$DDD$L'] = sterms[0][1]
        data['ASPxRoundPanel1$ASPxComboBoxETerm'] = sterms[0][0]
        data['ASPxRoundPanel1_ASPxComboBoxETerm_VI'] = sterms[0][1]
        data['ASPxRoundPanel1$ASPxComboBoxETerm$DDD$L'] = sterms[0][1]

        req = self.sess.post(self.url, data=data)
        skills = self.parse_params(req)

        return (data, sterms, skills)

    def get_levels(self):
        data, sterms, skills = self.get_skills()
        college_params = []
        for i in range(len(sterms)):
            params = {}
            for i2 in range(len(sterms) - i):
                for i3 in range(len(skills)):
                    if "ESL" not in skills[i3][0]:
                        params['sterm'] = sterms[i]
                        params['eterm'] = sterms[i2 + i]
                        params['skill'] = skills[i3]
                        data['__CALLBACKID'] = 'ASPxRoundPanel1$ASPxComboBoxPL'
                        data['ASPxRoundPanel1$ASPxComboBoxSTerm'] = params[
                            'sterm'][0]
                        data['ASPxRoundPanel1_ASPxComboBoxSTerm_VI'] = params[
                            'sterm'][1]
                        data['ASPxRoundPanel1$ASPxComboBoxSTerm$DDD$L'] = params[
                            'sterm'][1]
                        data['ASPxRoundPanel1$ASPxComboBoxETerm'] = params[
                            'eterm'][0]
                        data['ASPxRoundPanel1_ASPxComboBoxETerm_VI'] = params[
                            'eterm'][1]
                        data['ASPxRoundPanel1$ASPxComboBoxETerm$DDD$L'] = params[
                            'eterm'][1]
                        data['ASPxRoundPanel1$ASPxComboBoxBSSub'] = params[
                            'skill'][0]
                        data['ASPxRoundPanel1_ASPxComboBoxBSSub_VI'] = params[
                            'skill'][1]
                        data['ASPxRoundPanel1$ASPxComboBoxBSSub$DDD$L'] = params[
                            'skill'][1]

                        req = self.sess.post(self.url, data=data)

                        try:
                            levels = self.parse_params(req)

                            for l in levels:
                                params['sterm'] = sterms[i]
                                params['eterm'] = sterms[i2 + i]
                                params['skill'] = skills[i3]
                                params['level'] = l
                                college_params.append(params)
                                params = {}

                        except:
                            pass

        pickle.dump(
            college_params,
            open('./pickles/' + self.college[0] + '.pkl', 'wb'))
        return college_params

    def dl_csv(self):
        config = pickle.load(
            open(
                './pickles/' +
                self.college[0] +
                '.pkl',
                'rb'))
        num_configs = len(config)

        params_json = json.load(open('pickles/dump.HAR'))
        params1 = {parse.unquote(d['name']): parse.unquote(d['value']) for d in params_json[
            'log']['entries'][-6]['request']['postData']['params']}
        params2 = {parse.unquote(d['name']): parse.unquote(d['value']) for d in params_json[
            'log']['entries'][-1]['request']['postData']['params']}

        headers = {d['name']: d['value'] for d in params_json[
            'log']['entries'][-1]['request']['headers']}
        del headers['Content-Length']
        del headers['Cookie']

        cookies = {'Cookie': 'ASP.NET_SessionId' + '=' +
                   self.init_req.cookies.get_dict()['ASP.NET_SessionId']}
        self.sess.headers.update(cookies)

        data = self.init_states

        for k in data.keys():
            params1[k] = data[k]
            params2[k] = data[k]

        for i, c in enumerate(config):
            print(i, num_configs, c)

            for p in (params1, params2):
                p['ASPxRoundPanel1$ASPxComboBoxColl'] = self.college[0]
                p['ASPxRoundPanel1_ASPxComboBoxColl_VI'] = self.college[1]
                p['ASPxRoundPanel1$ASPxComboBoxColl$DDD$L'] = self.college[1]
                p['ASPxRoundPanel1$ASPxComboBoxSTerm'] = c['sterm'][0]
                p['ASPxRoundPanel1_ASPxComboBoxSTerm_VI'] = c['sterm'][1]
                p['ASPxRoundPanel1$ASPxComboBoxSTerm$DDD$L'] = c['sterm'][1]
                p['ASPxRoundPanel1$ASPxComboBoxETerm'] = c['eterm'][0]
                p['ASPxRoundPanel1_ASPxComboBoxETerm_VI'] = c['eterm'][1]
                p['ASPxRoundPanel1$ASPxComboBoxETerm$DDD$L'] = c['eterm'][1]
                p['ASPxRoundPanel1$ASPxComboBoxBSSub'] = c['skill'][0]
                p['ASPxRoundPanel1_ASPxComboBoxBSSub_VI'] = c['skill'][1]
                p['ASPxRoundPanel1$ASPxComboBoxBSSub$DDD$L'] = c['skill'][1]
                p['ASPxRoundPanel1$ASPxComboBoxPL'] = c['level'][0]
                p['ASPxRoundPanel1_ASPxComboBoxPL_VI'] = c['level'][1]
                p['ASPxRoundPanel1$ASPxComboBoxPL$DDD$L'] = c['level'][1]

            params2['__EVENTTARGET'] = 'buttonSaveAs'
            params2['listExportFormat'] = '1'

            # need to start sesh
            r = self.sess.post(self.url, data=params1)

            # now get full report
            r = self.sess.post(self.url, data=params2)

            with open("data/" + self.college[0] + '-' + c['sterm'][1] + '-' + c['eterm'][1] + '-' + c['skill'][1] + '-' + c['level'][1] + '.csv', 'w') as f:
                f.write(r.text)

            pickle.dump(config[i + 1:],
                        open('./pickles/' + self.college[0] + '.pkl', 'wb'))

            time.sleep(1)

if __name__ == "__main__":
    colleges = pickle.load(open('./pickles/college_list.pkl', 'rb'))
    colleges = colleges[:5]

    for c in colleges:
        if not './pickles/' + c[0] + '.pkl' in glob.glob('./pickles/*.pkl'):
            BasicSkillsCollege((c[0], c[1])).get_levels()

        BasicSkillsCollege((c[0], c[1])).dl_csv()
