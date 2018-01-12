# -*- coding:utf-8 -*-

import paramiko
import os
import json
import time
import urllib2
import MySQLdb as mysql


class ps_ef(object):
    """docstring for ps_ef"""

    def __init__(self, ip, port, user, passwd):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.connect("124.127.117.134",8944,'root','geth@123')
        self.client.connect(ip, port, user, passwd)

    def pyout(self):
        # 执行python命令的输出
        client = self.client
        base_dir = os.getcwd()
        cmd_filepath = base_dir + r"\web_u.txt"
        cmd_file = open(cmd_filepath, "r")
        cmd = cmd_file.read()
        stdin, stdout, stderr = client.exec_command(cmd)
        if stdout:
            for line in stdout:
                data = json.loads(line)
                return data
                # print(type(data))
                # total = data['total']/1024/1024
                # used = data['used']
                # print 'available: %s' % (data["available"]/1024/1024)
                # print 'used: %s' % (data['used']/1024/1024)
                # print 'mem_percent: %s' % (data['percent'])
                # print 'cpu_percent: %s' % (data['cpu_percent'])
        else:
            err = stderr.read()
            print 'error: %s' % err

    def close(self):
        client = self.client
        client.close()

connect = ps_ef(ip="124.127.117.134", port=8944, user='root', passwd='geth@123')
db = mysql.connect(user="root", passwd="fan123",db="flacon", charset="utf8")
db.autocommit(True)
c = db.cursor()
while True:
    data = connect.pyout()
    print data

    try:
        sql = "INSERT INTO `stat` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES('%s', '%d', '%d', '%d', '%s', '%d')" % (
        data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], int(data['Time']))
        ret = c.execute(sql)
    except mysql.IntegrityError:
        print 'error'

    # req = urllib2.Request("http://localhost:5000", json.dumps(data), {'Content-Type': 'application/json'})
    # f = urllib2.urlopen(req)
    # response = f.read()
    # print response
    # f.close()
    time.sleep(2)
c.close()
connect.close()

