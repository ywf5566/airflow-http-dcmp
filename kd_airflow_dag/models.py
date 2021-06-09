# encoding: utf-8
from datetime import datetime
from kd_airflow_dag import utils
import json
import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime, Text, create_engine)


class DcmpDagDatabase(object):
    def __init__(self, host):
        if host == "kd01" or host == "192.168.100.199":
            self.mysql_uri = utils.MysqlUrl["kd01_mysql_uri"]
        if host == "kd03" or host == "192.168.100.201":
            self.mysql_uri = utils.MysqlUrl["kd03_mysql_uri"]
        if host == "kd02" or host == "10.200.15.131":
            self.mysql_uri = utils.MysqlUrl["kd02_mysql_uri"]
        if host == "kd05" or host == "10.200.15.133":
            self.mysql_uri = utils.MysqlUrl["kd05_mysql_uri"]

    def get_dag_conf_by_name(self, dag_name):
        sql = 'select dag_name,conf from dcmp_dag_conf where dag_name="{}" order by version desc'.format(dag_name)
        connection = create_engine(self.mysql_uri)
        try:
            result = connection.execute(sql)
            # 如果能查到该dag-id的信息返回dict，否则返回None
            return json.loads(list(result.first())[1])
        except Exception as e:
            logging.exception("未查询到dag_name为{},错误信息{}".format(dag_name, e))
            return None

    def update_dag_state(self, dag_id, state):
        """
        :param dag_id: 传入要 更新状态的dag id，更新dag state后同时更新task instance 的状态
        :param state: 更新的状态
        :return: 返回sql操作结果
        """
        sql = """update dag_run set state='{}' where dag_id='{}' and state='running'"""
        task_sql = """update task_instance set state='{}' where dag_id='{}' and state='running'"""
        connection = create_engine(self.mysql_uri)
        result = 1
        while result is not 0:  # rowcount==0时代表没有running的dag
            try:
                connection.execute(task_sql.format(state, dag_id))
                result = connection.execute(sql.format(state, dag_id)).rowcount

            except Exception as e:
                logging.info("Airflow--更新dag 状态错误信息：{}".format(e))
                return False

        return True

    def get_dag_status(self, dag_name):
        sql = 'select dag_id,state,start_date from dag_run where dag_id="{}" order by start_date desc'.format(dag_name)
        connection = create_engine(self.mysql_uri)
        try:
            result = connection.execute(sql)
            return result.first()
        except Exception as e:
            logging.info(e)
            return None


class DcmpDagConf(declarative_base()):
    __tablename__ = "dcmp_dag_conf"

    id = Column(Integer, primary_key=True)
    dag_id = Column(Integer, index=True, nullable=False)
    dag_name = Column(String(250), index=True, nullable=False)
    action = Column(String(50), index=True, nullable=False)  # choices are create, update, delete
    version = Column(Integer, index=True, nullable=False)
    _conf = Column('conf', Text, default="{}", nullable=False)
    approver_user_id = Column(Integer)
    approver_user_name = Column(String(250))
    approved_at = Column(DateTime, index=True)
    creator_user_id = Column(Integer, nullable=False)
    creator_user_name = Column(String(250), nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.now)
