# encoding: utf-8
from enum import Enum
KD01_SSH_USER = 'keydriver'
KD01_SSH_PWD = '123456'

LOGIN_HEADER_BASE = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36'
}

MysqlUrl = {
    "kd01_mysql_uri": "mysql+pymysql://airflow:EEE@qxxtg123@192.168.100.199:3306/airflow2_for_source_code",
    "kd02_mysql_uri": "mysql+pymysql://airflow:EEE@qxxtg123@10.200.15.131:3306/airflow-local",
    "kd03_mysql_uri": "mysql+pymysql://airflow:EEE@qxxtg123@192.168.100.201:3306/airflow",
    "kd05_mysql_uri": "mysql+pymysql://airflow:EEE@qxxtg123@10.200.15.133:3306/airflow"
}
ssh_server_login = {}


class AirflowRequestApi(Enum):
    LOGIN_URL_BASE = 'http://{}:28080/admin/airflow/login'
    # request.type : POST
    # 创建dag
    CREAT_DAG_API_BASE = 'http://{}:28080/admin/dagcreationmanager/api?api=update_dag&dag_name='
    # 触发dag执行
    TRIGGER_DAG_API_BASE = 'http://{host}:28080/admin/airflow/trigger?dag_id={dag_id}&origin=http://{host}:28080/admin/'
    # airflow删除dag
    AIRFLOW_DELETE_API = 'http://{host}:28080/admin/airflow/delete?dag_id={dag_name}'
    # 开启/关闭dag
    PAUSE_DAG_BASE = 'http://{host}:28080/admin/airflow/paused?is_paused={is_paused}&dag_id={dag_id}'
    # dag url
    DAG_URL_BASE = 'http://{}:28080/admin/airflow/tree?dag_id='

    # request.type : GET
    # dcmp插件删除dag
    DELETE_DAG_API_BASE = 'http://{host}:28080/admin/dagcreationmanager/api?api=delete_dag&dag_name={dag_id}'


AirflowLoginConf = {
    "kd01": {
        "root": {"username": "afroot01", "pwd": "seekdata01"},
        "model": {"username": "model01", "pwd": "seekdata01"}
    },
    "kd02": {
        "root": {"username": "afroot02", "pwd": "seekdata02"},
        "model": {"username": "model02", "pwd": "seekdata02"}
    },
    "kd03": {
        "root": {"username": "afroot03", "pwd": "seekdata03"},
        "model": {"username": "model03", "pwd": "seekdata03"}
    },
    "kd04": {
        "root": {"username": "afroot04", "pwd": "seekdata04"},
        "model": {"username": "model04", "pwd": "seekdata04"}
    },
    "kd05": {
        "root": {"username": "afroot05", "pwd": "seekdata05"},
        "model": {"username": "model05", "pwd": "seekdata05"}
    },

    "192.168.100.199": {
        "root": {"username": "afroot01", "pwd": "seekdata01"},
        "model": {"username": "model01", "pwd": "seekdata01"}
    },
    "192.168.100.201": {
        "root": {"username": "afroot03", "pwd": "seekdata03"},
        "model": {"username": "model03", "pwd": "seekdata03"}
    },
    "10.200.15.132": {
        "root": {"username": "afroot04", "pwd": "seekdata04"},
        "model": {"username": "model04", "pwd": "seekdata04"}
    },
    "10.200.15.133": {
        "root": {"username": "afroot05", "pwd": "seekdata05"},
        "model": {"username": "model05", "pwd": "seekdata05"}
    }
}

