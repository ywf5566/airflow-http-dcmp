# encoding: utf-8
import requests
import json
from datetime import datetime, timedelta
import robobrowser
from kd_airflow_dag import utils
import logging
import re
import paramiko
from kd_airflow_dag.models import DcmpDagDatabase
from croniter import croniter

'''
通过Http请求的方式向airflow-dcmp插件进行Dag任务的管理
'''

SUCCESS = 'success'
FAILED = 'failed'


class HttpDcmp(object):
    """ 初始化需要传入的参数：host,(kd01 或者 192.168.100.199) """

    def __init__(self, host):
        self.host = host
        self.login_url = utils.LOGIN_URL_BASE.format(host)
        self.username = utils.get_username(host)
        self.password = utils.get_pwd(host)
        self.creat_dag_api = utils.CREAT_DAG_API_BASE.format(host)

    def get_cookies(self):
        browse = robobrowser.RoboBrowser(parser='lxml')
        browse.open(self.login_url)
        f = browse.get_form(action='/admin/airflow/login')
        # 登录的账号
        try:
            f['username'].value = self.username
            f['password'].value = self.password
            browse.submit_form(f)
            # 写入cookies
            login_header = utils.LOGIN_HEADER_BASE
            login_header["Cookie"] = 'widescreen=1; session=' + browse.session.cookies.values()[0]
            # 获取csrf-token
            rest = re.search('CSRF\s=\s".*"', str(browse.find_all()))
            list_str = list(rest.group())
            del list_str[0:8]
            list_str.pop()
            login_header["X-CSRFToken"] = ''.join(list_str)
            return login_header

        except Exception as e:
            logging.exception("登录信息有误！请检查输入的host信息是否正确！\n{}".format(e))

    """ 创建dag任务， """

    def creat_dag_request(self, newDag):
        """
        :param newDag:
        :return:
        """
        login_header = self.get_cookies()
        if not isinstance(newDag, dict):
            newDag = newDag.get_dict()
        session = requests.session()
        creat_api = self.creat_dag_api + newDag["dag_name"]
        res = session.post(url=creat_api, headers=login_header, data=json.dumps(newDag))
        print("创建任务post请求状态码：{}".format(res.status_code))

    def delete_dag_request(self, dag_name):
        """
        通过dcmp和airflow的api请求删除dag任务
        :param dag_name:
        :return:
        """
        login_header = self.get_cookies()
        dcmp_delete_api = utils.DELETE_DAG_API_BASE.format(host=self.host, dag_id=dag_name)
        airflow_delete_api = utils.AIRFLOW_DELETE_API.format(host=self.host, dag_name=dag_name)
        requests.get(url=dcmp_delete_api, headers=login_header)
        res = requests.post(url=airflow_delete_api, headers=login_header)
        print("删除{}任务get请求状态码：{}".format(dag_name, res.status_code))
        return res

    def trigger_dag_request(self, dag_name):
        """
        :param dag_name:
        :return:
        """
        login_header = self.get_cookies()
        trigger_api = utils.TRIGGER_DAG_API_BASE.format(host=self.host, dag_id=dag_name)

        res = requests.post(url=trigger_api, headers=login_header)
        print("触发{}任务执行post请求状态码：{}".format(dag_name, res.status_code))
        return res

    def kill_dag_by_dag_name(self, dag_name):
        """
        手动使一个dag的状态marked failed
        :param dag_name: 传入要 kill的 dag-name
        :return:
        """
        try:
            dcmpDag = DcmpDagDatabase(self.host)
            result = dcmpDag.update_dag_state(dag_id=dag_name, state=FAILED)
            return result

        except Exception as e:
            raise Exception(e)

    def ssh_excute_command(self, excute_command=None, dag_name=None):
        """
        :param excute_command:
        :param dag_name: command 和 name 两者传入一个，触发远程airflow的dag或者执行一条命令
        :return:
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, 22, utils.KD01_SSH_USER, utils.KD01_SSH_PWD, timeout=5)

            if not dag_name is None:
                stdin, stdout, stderr = ssh.exec_command(
                    'source /home/keydriver/airflow/bin/activate;airflow trigger_dag {}'.format(dag_name))

            if not excute_command is None:
                stdin, stdout, stderr = ssh.exec_command(excute_command)

            print(stdout.read().decode('utf-8'))
            ssh.close()

        except Exception as e:
            raise Exception("ssh执行命令错误信息：{}".format(e))

    def paused_the_dag(self, dag_name, is_paused):
        """
        :param dag_name:
        :param is_paused:
        :return:
        """
        login_header = self.get_cookies()
        is_paused = "true" if is_paused else "false"
        is_paused_url = utils.PAUSE_DAG_BASE.format(host=self.host, is_paused=is_paused, dag_id=dag_name)
        res = requests.post(url=is_paused_url, headers=login_header)
        print("开关任务{}post请求状态码：{}".format(dag_name, res.status_code))
        return res

    """ 下载数据运行的结果文件 """

    def download_result_file(self, remote_path, local_path):
        """
        :param remote_path:
        :param local_path:
        :return:
        """
        transport = paramiko.Transport(self.host, 22)
        transport.connect(username=utils.KD01_SSH_USER, password=utils.KD01_SSH_PWD)
        channel = paramiko.SFTPClient.from_transport(transport)
        channel.get(remote_path, local_path)
        transport.close()
        print("文件download from{}to{}".format(remote_path, local_path))

    def modif_dag_conf(self, dag_name, new_cron=None, new_command=None):
        """
        该方法用于修改一个dag的cron参数、command参数
        :param dag_name:
        :param new_cron:
        :param new_command:
        :return:
        """
        dcmpDag = DcmpDagDatabase(self.host)
        dagDic = dcmpDag.get_dag_conf_by_name(dag_name)
        if dagDic is not None:
            if new_cron is not None:
                dagDic["cron"] = new_cron
            else:
                dagDic["cron"] = 'None'
            if new_command is not None:
                dagDic["command"] = new_command
            self.creat_dag_request(dagDic)
        else:
            logging.exception("dag_id :{} 有误！".format(dag_name))

    """传入一个server 里的dag_name，返回dag的url"""

    def get_dag_name_url(self, dag_name):
        # 判断dag name是否存在
        return utils.DAG_URL_BASE.format(self.host) + dag_name


class HttpNewDag(object):

    def __init__(self, dag_name, tasks, cron=None, owner=None, start_date=None):
        self.dag_name = dag_name
        self.cron = cron
        if cron is None:
            """ 如果没有cron， start_date 默认设置为两天前"""
            self.cron = "None"
            self.start_date = str(datetime.now().replace(microsecond=0) - timedelta(days=2))
        else:
            """ 如果有cron，但是没有start_date，通过cron计算开始时间"""
            if start_date is None:
                self.start_date = str(croniter(cron, datetime.now()).get_prev(datetime))
            else:
                self.start_date = start_date
        self.owner = owner
        tasks_list = []
        for task in tasks:
            tasks_list.append(task.get_dict())
        self.tasks = tasks_list

    def get_dag_name(self):
        return self.dag_name

    def get_dict(self):
        return {"dag_name": self.dag_name, "cron": self.cron, "start_date": self.start_date, "tasks": self.tasks}


class HttpNewTask(object):
    """ 创建一个新的task，用于组装dag，默认执行本地bash命令，如需在别的服务器上执行，task_type为SSH，并带入SSH_conn_id """

    def __init__(self, task_name, command, upstreams=[], task_type="Bash", SSH_conn_id="undefined",
                 trigger_rule="all_success"):
        self.task_name = task_name
        """ task_type : [Bash, SSH, TriggerDagRun] """
        self.task_type = task_type
        self.command = command + " "
        self.upstreams = upstreams
        self.SSH_conn_id = SSH_conn_id
        self.trigger_rule = trigger_rule

    def get_dict(self):
        return {"task_name": self.task_name, "task_type": self.task_type, "command": self.command,
                "upstreams": self.upstreams, "SSH_conn_id": self.SSH_conn_id, "trigger_rule": self.trigger_rule}
