import os
import traceback
import psycopg2
from datetime import datetime

class ErrorHandling:
    def __init__(self, usr, pwd, bd_pg, bd_port,bd_procesos, bd_company, table_name):
        self.usr = usr
        self.pwd = pwd
        self.bd_pg = bd_pg
        self.bd_port = bd_port
        self.bd_procesos = bd_procesos
        self.bd_company = bd_company
        self.table_name = table_name

    def handle_error(self):
        outdir_error = './errors/'
        if not os.path.exists(outdir_error):
            os.mkdir(outdir_error)
        
        tb = traceback.format_exc()
        with open(f'{outdir_error}/{self.table_name}.txt', 'w') as f:
            f.write(tb)

        try:
            connection = psycopg2.connect(user=self.usr,
                                          password=self.pwd,
                                          host=self.bd_pg,
                                          port=self.bd_port,
                                          database=self.bd_procesos)
            today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            cursor = connection.cursor()
            qry_add_data_comp_net_pt1 = "INSERT INTO public.procesos (proceso,accion,estado,fecha) "
            qry_add_data_comp_net_pt2 = f"VALUES ('{self.bd_company.upper()}','{self.table_name.upper()}','ERROR','{today}');"
            qry_add_data_comp_net_final = qry_add_data_comp_net_pt1 + qry_add_data_comp_net_pt2
            print(qry_add_data_comp_net_final)
            cursor.execute(qry_add_data_comp_net_final)
            connection.commit()
        except psycopg2.Error as e:
            print("Error while connecting to PostgreSQL", e)
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()


