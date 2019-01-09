import sys
import time

import requests

from bs4 import BeautifulSoup

if __name__ == '__main__':
    studentid = ''

    kaochangid = ''

    Zjk = []

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': '192.168.252.29',
        'Cache - Control': 'max - age = 0',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36 '
    }

    mmp = requests.get(url='http://192.168.252.29/ksxt/ksonline/index.jsp')  # 获得jsessionio

    JSESSIONID = str(mmp.cookies).split(' ')[1].split('JSESSIONID=')[1]

    cookies = {'inanstime_ks': '',  # 不知道干啥的
               'inansti_ks': '',  # 不知道干啥的
               'JSESSIONID': JSESSIONID,  # 用于登录
               'login': '201710143001',  # 无用
               'jiaozhichu_brower': 'p'  # 不知道干啥的
               }

    username = input('请输入账号（输完回车）：')

    password = input('请输入密码（输完回车）：')

    loginF = {'id': username, 'password': password, 'jurl': ''}

    login = requests.post(url='http://192.168.252.29/ksxt/login/ksonline/LoginAction.do', cookies=cookies, data=loginF)

    list_q = requests.post(url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=examListMain&type=1',
                           cookies=cookies)  # 获得考试的id

    list_Bea = BeautifulSoup(list_q.text, 'html.parser')
    for mesa in list_Bea.find_all('tr'):
        if mesa.get('onclick') is not None:
            ty = str(mesa.get('onclick'))
            Zjk.append(ty.split("_h5('")[1].split("'")[0])
    # print(Zjk)
    for iii in range(0, 10):
        for examid in Zjk:
            dati = []
            daan = {}
            num = 1
            titi = {}
            filena = open(examid + '.txt', 'a+', encoding='utf-8')
            body = {'examid': examid}
            first = requests.post(url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=initKsKs', data=body,
                                  cookies=cookies)  # 进行试卷初始化
            data_getStudentid = {'op': 'null', 'examid': examid, 'examtype': '3', 'studentid': ''}
            r = requests.post(
                url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=kaochang&type=confirm&examid=' + examid + '&examtype=3&studentid=&lx=3',
                cookies=cookies, data=data_getStudentid, timeout=500)
            r.encoding = 'UTF-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            # print(r.text)
            for link in soup.find_all('td', class_='tdbk'):
                studentid = link['onclick'].split('\'')[3]
                kaochangid = link['onclick'].split('\'')[5]
            data_Account = {'type': 'confirm', 'studentid': studentid, 'kssj': '1', 'kaochangid': kaochangid,
                            'examtype': '3',
                            'examid': examid}
            account = requests.post(url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=account',
                                    data=data_Account, cookies=cookies, timeout=500)
            data_saveAccount = {'zb': '', 'type': '1', 'studentid': studentid, 'kaochangid': kaochangid, 'examtype': '3',
                                'examid': examid}
            saveAccount = requests.post(url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=saveSignAccount',
                                        data=data_saveAccount, cookies=cookies, timeout=500)
            data_ans1 = {'type': '1', 'type': '1', 'studentid': studentid, 'studentid': studentid, 'sort': 'null', 'p': 'p',
                         'examtype': '3', 'examid': examid, 'examid': examid}

            data_getlist = {'examid': examid, 'examtype': 'null', 'studentid': studentid, 'sort': '1'}

            quelist = requests.post(
                url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=getQuestionList&type=1',
                data=data_getlist, cookies=cookies)
            # print(quelist.text)
            bealist = BeautifulSoup(quelist.text, 'html.parser')
            for assd in bealist.find_all('li', class_='on'):
                for adds in assd.find('span', class_='dis1023_ item'):
                    if adds == '单选题' or adds == '判断题' or adds == '多选题':
                        for sssort in assd.find_all('a'):
                            # print(sssort.get('onclick').split("click_ti('")[1].split("'")[0])
                            sort = sssort.get('onclick').split("click_ti('")[1].split("'")[0]
                            if sort == '1':
                                ans1 = requests.post(
                                    url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=selectQuestiontimu&anscount=1',
                                    data=data_ans1, cookies=cookies, timeout=500)
                                qu1 = BeautifulSoup(ans1.text, 'html.parser')
                                ques = qu1.find('div', id='timu_text')
                                # print('第' + sort + '题：' + ques.text)
                                balana = ''
                                for bitch in qu1.find_all('a', class_='unselectkey'):
                                    # print('选项：' + bitch.text, file=filena)
                                    balana += str(bitch.text)
                                titi[sort] = ques.text + '选项：' + balana
                                # print("选项: %s" % titi['1'])
                            else:
                                sort = str(int(sort) - 1)
                                data_getrequests = {'examid': examid, 'examtype': '3', 'studentid': studentid,
                                                    'result_show': 'A', 'ts': '',
                                                    'timedjs': '01:20:34', 'usetime': '', 'singletimeiv': '300',
                                                    'notsave': '0',
                                                    'tixingv': '2',
                                                    'tihaov': '6',
                                                    'anscount': '0', 'type': '1', 'typeid': '7', 'choosexx': '4',
                                                    'systype': '2',
                                                    'result': 'A',
                                                    'sort': sort,
                                                    'sort_flag': 'down', 'subjectid': 'null', 'sort_up': '', 'mark_bj': '0',
                                                    'tik': '',
                                                    'tir': '',
                                                    'tip': '',
                                                    'studentupfile': '', 'questionid': '23771', 'val': 'null'
                                                    }
                                question = requests.post(
                                    url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=selectQuestiontimu',
                                    headers=headers, data=data_getrequests, cookies=cookies, timeout=500)
                                qu = BeautifulSoup(question.text, 'html.parser')
                                ques = qu.find('div', id='timu_text')
                                # print('第' + str(int(sort) + 1) + '题：' + ques.text)
                                balana = ''
                                for bitch in qu.find_all('a', class_='unselectkey'):
                                    # print('选项：' + bitch.text, file=filena)
                                    balana += str(bitch.text)
                                titi[str(int(sort) + 1)] = ques.text + '选项：' + balana
                                # print("选项: %s" % titi[str(int(sort) + 1)])
                                num += 1
                    if adds == '填空题':
                        for sssort in assd.find_all('a'):
                            # print(sssort.get('onclick').split("click_ti('")[1].split("'")[0])
                            sort = sssort.get('onclick').split("click_ti('")[1].split("'")[0]
                            sort = str(int(sort) - 1)
                            data_getrequests = {'val': 'null', 'usetime': '', 'typeid': '7', 'type': '1', 'ts': '',
                                                'tixingv': '7',
                                                'tir': '', 'tip': '', 'timedjs': '01:59:47', 'tik': '', 'tihaov': '31',
                                                'text': 'AAA @`_~@AAA @`_~@AAA @`_~@AAA @`_~@',
                                                'systype': '7', 'subjectid': 'null', 'studentupfile': '',
                                                'studentid': studentid,
                                                'sort_up': '', 'sort_flag': 'down', 'sort': sort, 'singletimeiv': '8',
                                                'result': 'AAA @`_~@AAA @`_~@AAA @`_~@AAA @`_~@AAA @`_~@AAA @`_~@AAA @`_~@AAA @`_~@',
                                                'questionid': '76600', 'notsave': '0', 'mark_bj': '0',
                                                'examtype': 'null', 'examid': examid,
                                                'editorValue': 'lalalalalala<div></div>',
                                                'choosexx': '1',
                                                'anscount': '0',
                                                'note': 'AAA',
                                                'note': 'AAA',
                                                'note': 'AAA',
                                                'note': 'AAA'
                                                }
                            question = requests.post(
                                url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=selectQuestiontimu',
                                headers=headers, data=data_getrequests, cookies=cookies, timeout=500)
                            qu = BeautifulSoup(question.text, 'html.parser')
                            ques = qu.find('div', id='timu_text')
                            # print('第' + sort + '题：' + ques.text)
                            titi[sort] = ques.text
                            # print("选项: %s" % titi[sort])
                    if adds == '简答题':
                        for sssort in assd.find_all('a'):
                            # print(sssort.get('onclick').split("click_ti('")[1].split("'")[0])
                            sort = sssort.get('onclick').split("click_ti('")[1].split("'")[0]
                            sort = str(int(sort) - 1)
                            dati.append(str(int(sort) + 1))
                            data_getrequests = {'val': 'null', 'usetime': '', 'typeid': '7', 'type': '1', 'ts': '',
                                                ';tixingv': '7',
                                                'tir': '', 'tip': '', 'timedjs': '01:59:47', 'tik': '', 'tihaov': '31',
                                                'text': 'lalalalalala',
                                                'systype': '7', 'subjectid': 'null', 'studentupfile': '',
                                                'studentid': studentid,
                                                'sort_up': '', 'sort_flag': 'down', 'sort': sort, 'singletimeiv': '8',
                                                'result': 'lalalala@`_~@全错@`_~@0', 'questionid': '76600', 'notsave': '0',
                                                'mark_bj': '0',
                                                'examtype': 'null', 'examid': examid, 'editorValue': 'lalalala<div></div>',
                                                'choosexx': '1',
                                                'anscount': '0'}
                            question = requests.post(
                                url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=selectQuestiontimu',
                                headers=headers, data=data_getrequests, cookies=cookies, timeout=500)
                            qu = BeautifulSoup(question.text, 'html.parser')
                            ques = qu.find('div', id='timu_text')
                            if ques is not None:
                                # print('第' + str(int(sort) + 1) + '题：' + ques.text)
                                titi[str(int(sort) + 1)] = ques.text
                                # print("选项: %s" % titi[str(int(sort) + 1)])

            data_getAnswer = {'type': '1', 'studentid': studentid, 'sort': '6', 'kh': 'null', 'examid': examid}
            answer = requests.post(url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=commit',
                                   cookies=cookies,
                                   data=data_getAnswer, timeout=500)
            ans_soup = BeautifulSoup(answer.text, 'html.parser')
            nums = '1'
            for ans in ans_soup.find_all('span', class_='dis481'):
                if '您' in ans.text:
                    Madedaan = str(ans.text).replace('										', '').replace('\r\n', '').split('您')[0]
                    daan[nums] = '*********答案：'+Madedaan
                    nums = str(int(nums)+1)
            for num in dati:
                for ans in ans_soup.find_all('span', id='stfx_' + str(num)):
                    # print('第' + str(num) + '题：\n' + ans.text)
                    daan[str(num)] = '^^^^^^^答案：'+ans.text
            # print(titi)
            # print(daan)
            # print(dati)
            try:
                for outi in titi.keys():
                    print('第'+outi+'题： '+str(titi[outi]+daan[outi]).replace(" ", ""), file=filena)
            except BaseException:
                continue
            filena.close()
