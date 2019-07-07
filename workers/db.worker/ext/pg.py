from nameko.extensions import DependencyProvider
import psycopg2


class PgService(DependencyProvider):

    def __init__(self, dsn):
        self.dsn = dsn

    #def get_dependency(self, worker_ctx):
    #    return psycopg2.connect(self.dsn)
    def get_dependency(self, worker_ctx):
        try:
            conn = psycopg2.connect(self.dsn)
        except Exception as e:    #psycopg2.OperationalError as e:
            #print('Unable to connect!\n{}').format(e)
            conn = None
            pass
        
        return conn

