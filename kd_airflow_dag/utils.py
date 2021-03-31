# encoding: utf-8
LOGIN_URL_BASE = 'http://{}:28080/admin/airflow/login'
LOGIN_USER_BASE = 'model{}'
LOGIN_PWD_BASE = 'seekdata{}'
KD01_SSH_USER = 'keydriver'
KD01_SSH_PWD = '123456'
LOGIN_HEADER_BASE = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36 '
}
KD01_MYSQL_URI = 'mysql+pymysql://airflow:EEE@qxxtg123@192.168.100.199:3306/airflow2_for_source_code'
KD02_MYSQL_URI = 'mysql+pymysql://airflow:EEE@qxxtg123@10.200.15.131:3306/airflow'
KD03_MYSQL_URI = 'mysql+pymysql://airflow:EEE@qxxtg123@192.168.100.201:3306/airflow'
# request.type : POST
CREAT_DAG_API_BASE = 'http://{}:28080/admin/dagcreationmanager/api?api=update_dag&dag_name='
TRIGGER_DAG_API_BASE = 'http://{host}:28080/admin/airflow/trigger?dag_id={dag_id}&origin=http://{host}:28080/admin/'
AIRFLOW_DELETE_API = 'http://{host}:28080/admin/airflow/delete?dag_id={dag_name}'
PAUSE_DAG_BASE = 'http://{host}:28080/admin/airflow/paused?is_paused={is_paused}&dag_id={dag_id}'
DAG_URL_BASE = 'http://{}:28080/admin/airflow/tree?dag_id='
# request.type : GET
DELETE_DAG_API_BASE = 'http://{host}:28080/admin/dagcreationmanager/api?api=delete_dag&dag_name={dag_id}'


def get_username(host):
    if host == "kd01" or host == "192.168.100.199":
        return LOGIN_USER_BASE.format("01")
    elif host == "kd03" or host == "192.168.100.201":
        return LOGIN_USER_BASE.format("03")
    elif host == "kd04" or host == "10.200.15.132":
        return LOGIN_USER_BASE.format("04")


def get_pwd(host):
    if host == "kd01" or host == "192.168.100.199":
        return LOGIN_PWD_BASE.format("01")
    elif host == "kd03" or host == "192.168.100.201":
        return LOGIN_PWD_BASE.format("03")
    elif host == "kd04" or host == "10.200.15.132":
        return LOGIN_PWD_BASE.format("04")
