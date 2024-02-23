import json
from hdbcli import dbapi
# from pyspark.sql import SparkSession
import pandas as pd
import datetime
from .logger import Logger
from pkg_resources import resource_stream



class DbConnection:

    def __init__(self, package_name=None,url=None):
        self.logger = Logger.get_instance()
        if package_name is not None:
            try:
                self.config = json.load(resource_stream(package_name, 'config.json'))
            except Exception as e:
                self.logger.error('Error loading config.json in package: %s', e)
                raise
        else:
            if url is None:
                url = 'config.json'
            try:
                with open(url, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                self.logger.error("Unable to load the config.json from the url '{}'".format(url))
                self.logger.error(e)
                raise
        self.connection = self._get_connection()
        self.cursor = None


    def _get_connection(self):

        #optional arguments
        if "encrypt" not in self.config:
            self.config["encrypt"] = "true"
        if "sslValidateCertificate" not in self.config:
            self.config["sslValidateCertificate"] = "false"
        if "disableCloudRedirect" not in self.config:
            self.config["disableCloudRedirect"] = "true"
        if "communicationTimeout" not in self.config:
            self.config["communicationTimeout"] = "0"
        if "autocommit" not in self.config:
            self.config["autocommit"] = "true"
        if "sslUseDefaultTrustStore" not in self.config:
            self.config["sslUseDefaultTrustStore"] = "true"

        return dbapi.connect(
            address=self.config["address"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            schema=self.config["schema"],
            encrypt=self.config["encrypt"],
            sslValidateCertificate=self.config["sslValidateCertificate"],
            disableCloudRedirect=self.config["disableCloudRedirect"],
            communicationTimeout=self.config["communicationTimeout"],
            autocommit=self.config["autocommit"],
            sslUseDefaultTrustStore=self.config["sslUseDefaultTrustStore"]
        )

    def get_schema_views(self):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            query = "SELECT %s, %s  FROM %s WHERE %s = '%s' " % ("VIEW_NAME", "VIEW_TYPE", "VIEWS", "SCHEMA_NAME", self.config['schema'])  
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
        except Exception as e:
            self.logger.error('error occured during query execution %s', e)
            self.connection.rollback()
            raise
        return  res, column_headers

    def get_table_size(self, table_name):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        schema = self.config['schema']
        sqlQuery=""" SELECT COUNT(*) FROM "{}"."{}" """.format(schema,table_name)
        try:
            cursor.execute(sqlQuery)
            res = cursor.fetchall()
            return res
        except Exception as e:
            self.logger.error('error occured during query execution %s', e)
            self.connection.rollback()
            raise

    def get_data_with_headers(self, table_name, size=1):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        rows = self.get_table_size(table_name)
        dataset_size = int(rows[0][0]*size)
        schema = self.config['schema']
        sqlQuery=""" SELECT TOP {} * FROM "{}"."{}"  """.format(str(dataset_size),schema,table_name)
        try:
            cursor.execute(sqlQuery)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during query execution %s', e)
            self.connection.rollback()
            raise
    
    # def get_data_with_headers_pyspark(self, table_name, size=1):
    #     try:
    #         data,column_headers=self.get_data_with_headers(table_name,size)
    #     except Exception as e:
    #         self.logger.error('error occured during query execution. %s', e)
    #         self.connection.rollback()
    #         raise
    #     try:
    #         pandas_df=pd.DataFrame(data, columns=column_headers)
    #         spark = SparkSession.builder.getOrCreate()
    #         spark_df = spark.createDataFrame(data=pandas_df)
    #         return spark_df
    #     except Exception as e:
    #         self.logger.error('error occured while retrieving the data as PySpark dataframe.Use the "get_data_with_headers" method to get the data. %s', e)
    #         self.connection.rollback()
    #         raise
    
    def execute_query(self, query):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            if query.split()[0].lower()!="select":
                raise Exception("The ‘execute_query’ and ‘execute_query_pyspark’ methods supports ‘select’ SQL statements only. For other SQL statements, use the appropriate methods by referring the documentation.")
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during query execution: %s', e)
            self.connection.rollback()
            raise
    
    # def execute_query_pyspark(self, query):
    #     try:
    #         data,column_headers=self.execute_query(query)
    #     except Exception as e:
    #         self.logger.error('error occured during query execution: %s', e)
    #         self.connection.rollback()
    #         raise
    #     try:
    #         pandas_df=pd.DataFrame(data, columns=column_headers)
    #         spark = SparkSession.builder.getOrCreate()
    #         spark_df = spark.createDataFrame(data=pandas_df)
    #         return spark_df
    #     except Exception as e:
    #         self.logger.error('error occured while retrieving the data as PySpark dataframe.Use the "execute_query" method to get the data: %s', e)
    #         self.connection.rollback()
    #         raise

    def create_table(self, query):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            if 'INSERTED_AT' in query:
                raise Exception('\nQuery Error: A column name provided was a duplicate of the automatically added INSERTED_AT timestamp column.\nPlease refer to documentation on more information about this generated column and/or change the name of the duplicated column provided in the query.')
            timestamp_column = ', INSERTED_AT TIMESTAMP NOT NULL'
            query = query.rstrip()[:-1] + timestamp_column + ')'
            self.logger.info("creating table...")
            self.logger.info(query)
            cursor.execute(query)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during query execution, doing rollback %s', e)
            self.connection.rollback()
            raise

    def drop_table(self, table_name):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            query = """ DROP TABLE "{}" """.format(table_name)
            self.logger.info("deleting table...")
            cursor.execute(query)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during query execution, doing rollback %s', e)
            self.connection.rollback()
            raise
            
            
    def insert_into_table(self, table_name, table_values):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            self.logger.info('inserting into table...')
            column_names = ', '.join(list(table_values.columns))
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            bound_values = column_names.replace(', ', ', ' + ':')
            bound_values = ':' + bound_values + ', :INSERTED_AT'
            sql=""" INSERT INTO "{}" """.format(table_name)
            sql+= ' (' + column_names + ', INSERTED_AT) VALUES (' + bound_values + ')'
            self.logger.info(sql)
            for index, row in table_values.iterrows():
                temp_dict = row.to_dict()
                temp_dict['INSERTED_AT'] = timestamp
                cursor.execute(sql, temp_dict)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during query execution, doing rollback %s', e)
            self.connection.rollback()
            raise
    
    def get_view_metadata(self,view_name):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            schema = self.config['schema']
            self.logger.info("Retrieving metadata of the view '%s' in schema '%s'",view_name,schema)
            query="SELECT POSITION, COLUMN_NAME, DATA_TYPE_NAME, LENGTH, IS_NULLABLE, SCALE, DEFAULT_VALUE, INDEX_TYPE, GENERATION_TYPE, COMMENTS FROM VIEW_COLUMNS WHERE SCHEMA_NAME = '{}' and VIEW_NAME='{}' ORDER BY POSITION".format(schema,view_name)
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during query execution %s', e)
            self.connection.rollback()
            raise

    
    def get_view_by_name(self,view_name):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            schema = self.config['schema']
            self.logger.info("Searching for views with name '%s' in schema '%s'",view_name,schema)
            view_name=view_name.lower()
            query = "SELECT VIEW_NAME, VIEW_TYPE FROM VIEWS WHERE SCHEMA_NAME = '{}' and lower(VIEW_NAME) like '%{}%'".format(schema,view_name)
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during query execution %s', e)
            self.connection.rollback()
            raise

    def delete_from_table(self,table_name,where_clause=None):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            self.logger.info("Deleting from table '%s'",table_name)
            query=""" DELETE FROM "{}" """.format(table_name)
            query+=("" if where_clause is None else " WHERE "+where_clause)
            self.logger.info("The delete query is: %s",query)
            cursor.execute(query)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during query execution, doing rollback %s', e)
            self.connection.rollback()
            raise
    
    def update_table(self,table_name,set_clause,where_clause=None):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            self.logger.info("Updating table '%s'",table_name)
            query=""" UPDATE "{}" """.format(table_name)
            query+=" SET "+set_clause+("" if where_clause is None else " WHERE "+where_clause)
            self.logger.info("The update query is: %s",query)
            cursor.execute(query)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during query execution, doing rollback %s', e)
            self.connection.rollback()
            raise
    
    def alter_table(self,table_name,clause):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            self.logger.info("Altering the table '%s'",table_name)
            query=""" ALTER TABLE "{}" """.format(table_name)
            query+=clause
            self.logger.info("The alter query is: %s",query)
            cursor.execute(query)
        except Exception as e:
            self.logger.error('error occured during query execution, doing rollback %s', e)
            self.connection.rollback()
            raise
    

    def get_table_metadata(self,table_name):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            self.logger.info("Retrieving metadata of the table '%s'.",table_name)
            query="SELECT POSITION, COLUMN_NAME, DATA_TYPE_NAME, LENGTH, IS_NULLABLE, SCALE, DEFAULT_VALUE, INDEX_TYPE, GENERATION_TYPE, COMMENTS FROM TABLE_COLUMNS WHERE TABLE_NAME='{}' ORDER BY POSITION".format(table_name)
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during query execution %s', e)
            self.connection.rollback()
            raise
    
    def get_user_tables(self):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            query="SELECT TABLE_NAME,SCHEMA_NAME,TABLE_TYPE,COMMENTS,CREATE_TIME FROM TABLES WHERE SCHEMA_NAME='{}'".format(self.config['user'])
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during query execution %s', e)
            self.connection.rollback()
            raise