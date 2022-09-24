import pymysql

class Database():
    '''
        Description:
            database demo to store images in MySQL
        Attributes:
            None
    '''

    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(host=host, user=user, password=password,
                                          database=database)
        self.cursor = self.connection.cursor()
        print('登录成功')

    def create_image_table(self):
        sql = "create table if not exists picture (id char(10), image longblob, label int);"

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.Error:
            print(pymysql.Error)

    def create_model_table(self):
        sql = "create table if not exists model (model_name char(100), model longblob);"

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.Error:
            print(pymysql.Error)

    def insert_model(self, model_name, model):
        sql = "insert into model(model_name,model) values (%s,%s)"
        self.cursor.execute(sql, (model_name, model))
        self.connection.commit()

    def insert_image(self, id, image):
        sql = "insert into picture(id,image) values (%s,%s)"
        self.cursor.execute(sql, (id, image))
        self.connection.commit()

    def update_label(self, id, label):
        sql = "update picture set label = (%s) where id = (%s) "
        self.cursor.execute(sql, (label, id))
        self.connection.commit()


    def get_image(self, id):
        sql = 'select image from picture where id = (%s)'
        try:
            self.cursor.execute(sql, id)
            image = self.cursor.fetchone()[0]
            return image
        except pymysql.Error:
            print(pymysql.Error)
        except IOError:
            print(IOError)

    def get_model(self, model_name):
        sql = 'select model from model where model_name = (%s)'
        try:
            self.cursor.execute(sql, model_name)
            model = self.cursor.fetchone()[0]
            return model
        except pymysql.Error:
            print(pymysql.Error)
        except IOError:
            print(IOError)

    def get_label(self, id):
        sql = 'select label from picture where id = (%s)'
        try:
            self.cursor.execute(sql, id)
            label = self.cursor.fetchone()[0]
            return label
        except pymysql.Error:
            print(pymysql.Error)
        except IOError:
            print(IOError)

    def __del__(self):
        self.connection.close()
        self.cursor.close()
        print('退出成功')