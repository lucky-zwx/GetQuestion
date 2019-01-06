import time

import requests

from bs4 import BeautifulSoup

if __name__ == '__main__':
    examid = ''

    studentid = ''

    sort = ''

    kaochangid = ''

    JSESSIONID = ''

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': '192.168.252.29',
        'Cache - Control': 'max - age = 0',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36 '
    }

    mmp = requests.get(url='http://192.168.252.29/ksxt/ksonline/index.jsp')
    JSESSIONID = str(mmp.cookies).split(' ')[1].split('JSESSIONID=')[1]

    cookies = {'inanstime_ks': '',  # 不知道干啥的
               'inansti_ks': '',  # 不知道干啥的
               'JSESSIONID': JSESSIONID,  # 用于登录
               'login': '201710143001',  # 无用
               'jiaozhichu_brower': 'p'  # 不知道干啥的
               }

    loginF = {'id': '201710143001', 'password': 'abk6745741', 'jurl': ''}

    login = requests.post(url='http://192.168.252.29/ksxt/login/ksonline/LoginAction.do', cookies=cookies, data=loginF)

    for times in range(0, 100):
        filena = open('./设备与维护.txt', 'a+', encoding='utf-8')
        examid = '969'
        body = {'examid': examid}
        first = requests.post(url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=initKsKs', data=body,
                              cookies=cookies)
        data_getStudentid = {'op': 'null', 'examid': examid, 'examtype': '3', 'studentid': ''}
        r = requests.post(
            url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=kaochang&type=confirm&examid=969&examtype=3&studentid=&lx=3',
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
        ans1 = requests.post(
            url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=selectQuestiontimu&anscount=1',
            data=data_ans1, cookies=cookies, timeout=500)
        qu1 = BeautifulSoup(ans1.text, 'html.parser')
        nums = 1
        for ques in qu1.find_all('div', id='timu_text'):
            print('问题' + str(nums) + '：' + ques.text, file=filena)
            for bitch in qu1.find_all('a', class_='unselectkey'):
                print('选项：'+bitch.text, file=filena)
            nums += 1
        for sorts in range(1, 31):
            sort = sorts
            data_getrequests = {'examid': examid, 'examtype': '3', 'studentid': studentid, 'result_show': 'A', 'ts': '',
                                'timedjs': '01:20:34', 'usetime': '', 'singletimeiv': '300', 'notsave': '0',
                                'tixingv': '2',
                                'tihaov': '6',
                                'anscount': '0', 'type': '1', 'typeid': '7', 'choosexx': '4', 'systype': '2',
                                'result': 'A',
                                'sort': sort,
                                'sort_flag': 'down', 'subjectid': 'null', 'sort_up': '', 'mark_bj': '0', 'tik': '',
                                'tir': '',
                                'tip': '',
                                'studentupfile': '', 'questionid': '23771', 'val': 'null'
                                }
            question = requests.post(
                url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=selectQuestiontimu',
                headers=headers, data=data_getrequests, cookies=cookies, timeout=500)
            qu = BeautifulSoup(question.text, 'html.parser')
            for ques in qu.find_all('div', id='timu_text'):
                print('问题' + str(nums) + '：' + ques.text, file=filena)
                for bitch in qu.find_all('a', class_='unselectkey'):
                    print('选项：' + bitch.text, file=filena)
                nums += 1
        for sorts in range(31, 39):
            sort = sorts
            data_getrequests = {'val': 'null', 'usetime': '', 'typeid': '7', 'type': '1', 'ts': '', ';tixingv': '7',
                                'tir': '', 'tip': '', 'timedjs': '01:59:47', 'tik': '', 'tihaov': '31', 'text': '朱文骁牛逼',
                                'systype': '7', 'subjectid': 'null', 'studentupfile': '', 'studentid': studentid,
                                'sort_up': '', 'sort_flag': 'down', 'sort': sort, 'singletimeiv': '8',
                                'result': '朱文骁牛逼@`_~@全错@`_~@0', 'questionid': '76600', 'notsave': '0', 'mark_bj': '0',
                                'examtype': 'null', 'examid': examid, 'editorValue': '朱文骁牛逼<div></div>',
                                'choosexx': '1',
                                'anscount': '0'}
            question = requests.post(
                url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=selectQuestiontimu',
                headers=headers, data=data_getrequests, cookies=cookies, timeout=500)
            qu = BeautifulSoup(question.text, 'html.parser')
            for ques in qu.find_all('div', id='timu_text'):
                print('问题' + str(nums) + '：' + ques.text, file=filena)
                # for bitch in qu.find_all('span', style=';font-family:宋体;font-size:14px'):
                #     print('选项：' + bitch.text)
                nums += 1
        data_getAnswer = {'type': '1', 'studentid': studentid, 'sort': '6', 'kh': 'null', 'examid': examid}
        answer = requests.post(url='http://192.168.252.29/ksxt/ksonline/KsOnlineAction.do?method=commit',
                               cookies=cookies,
                               data=data_getAnswer, timeout=500)
        ans_soup = BeautifulSoup(answer.text, 'html.parser')
        for ans in ans_soup.find_all('span', class_='dis481'):
            print(ans.text, file=filena)
        for num in range(31, 39):
            for ans in ans_soup.find_all('span', id='stfx_' + str(num)):
                print('第' + str(num) + '题：\n' + ans.text, file=filena)
        filena.close()
        time.sleep(5)
