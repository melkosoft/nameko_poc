from flask import Flask
from nameko.standalone.rpc import ServiceRpcProxy
from dotenv import load_dotenv
import os
from multiprocessing import Pool

current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path="{}/.env".format(current_dir))

app = Flask(__name__)


def rpc_proxy(service):
    config = {'AMQP_URI': os.getenv('AMQP_URI')}
    return ServiceRpcProxy(service, config)

def task(func):
    return func()

@app.route('/')
def hello():
    return "Hello"


@app.route('/local')
def local_time():
    with rpc_proxy('local_time_service') as rpc:
        time = rpc.local()

    return time


@app.route('/db')
def db_time():
    with rpc_proxy('db_time_service') as rpc:
        time = rpc.db()

    return time

@app.route('/db2')
def db_time2():
    with rpc_proxy('db_time_service2') as rpc:
        time = rpc.db()

    return time

@app.route('/all')
def get_all():
    p = Pool(3)
    data = p.map(task,[local_time,db_time,db_time2])
    #return ",".join(map(str, data))
    return "Local: {}, Db:{}, Db2:{}".format(*data)

if __name__ == '__main__':
    app.run()
