import pandas as pd
import pymysql
import requests
import streamlit as st
import json


# function address
url_pkg = 'http://166.111.73.96:31112/function/pkg'
url_add = 'http://166.111.73.96:31112/function/add'
url_seq = 'http://166.111.73.96:31112/function/seq'

# First container  ---basic information
info = st.container()
# the Title of the website
title_1, title_2 = info.columns([3,1])
with title_1:
    st.write('''
    # OpenFaaS User Interface
    #### OpenFaaS UI URL: http://166.111.73.96:31112
    ''')
with title_2:
    st.image('./logo.png')


# Second container  --- Function add
func_add = st.container()
func_add.markdown('''
    # Function Name: add
    ##### URL: http://166.111.73.96:31112/function/add
    ##### <table><tr><td bgcolor=PowderBlue>Description: Input a string of integers separated by commas and return their sum.</td></tr></table>
    ##### Input Format: String
    ##### Output Format: Int
    ''', unsafe_allow_html=True)

func_add_invoke = func_add.button("invoke", help='Push this button to invoke the add function')
input = func_add.text_area('请输入字符串', help='the input for the *add* function', key='func_add_text_area')
if func_add_invoke:
    response = requests.get(url=url_add, data=input)
    func_add.write('Output:', help='the result from the function invoked')
    func_add.info(response.text)


# Third container  --- Function seq
func_seq = st.container()
func_seq.markdown('''
    # Function Name: seq
    ##### URL: http://166.111.73.96:31112/function/seq
    ##### <table><tr><td bgcolor=PowderBlue>Description: Input a string of arrays, and can realize sorting, cutting and reversing.</td></tr></table>
    ##### Input Format: json{*function:'sort' or 'cut' or 'reverse' *array:[list], method(for sort):'descend' or 'ascend', n(for cut): int}
    ##### Output Format: json
    ''', unsafe_allow_html=True)

func_seq_invoke = func_seq.button("invoke", help='Push this button to invoke the seq function')
input = func_seq.text_area('请输入json格式的参数或上传json文件', help='the input for the *seq* function', key='func_seq_text_area')
uploaded_file = func_seq.file_uploader("上传json文件",help="若同时输入json参数并上传json文件，以上传的json文件作为参数", key='func_seq_file_uploader')
if uploaded_file is not None:
     # To read file as bytes:
     input = uploaded_file.getvalue()
     input = str(input, encoding='gbk')
     func_seq.write(json.loads(input))

if func_seq_invoke:
    if uploaded_file is None and len(input) == 0:
        st.warning('Function missing parameters')
    else:
        response = requests.get(url=url_seq, data=input)
        func_seq.write('Output:', help='the result from the function invoked')
        func_seq.info(response.text)

# Fourth container  --- Function pkg
func_pkg = st.container()
func_pkg.markdown('''
    # Function Name: pkg
    ##### URL: http://166.111.73.96:31112/function/pkg
    ##### <table><tr><td bgcolor=PowderBlue>Description: Input an id of image, then read it from database and classify it.</td></tr></table>
    ##### Input Format: json{*image_id:string, *model_name:string}
    ##### Output Format: string
    ''', unsafe_allow_html=True)

func_pkg_invoke = func_pkg.button("invoke", help='Push this button to invoke the pkg function')
input = func_pkg.text_area('请输入json格式的参数或上传json文件', help='the input for the *pkg* function', key='func_pkg_text_area')
uploaded_file = func_pkg.file_uploader("上传json文件",help="若同时输入json参数并上传json文件，以上传的json文件作为参数", key='func_pkg_file_uploader')
if uploaded_file is not None:
     # To read file as bytes:
     input = uploaded_file.getvalue()
     input = str(input, encoding='gbk')
     func_pkg.write(json.loads(input))

if func_pkg_invoke:
    if uploaded_file is None and len(input) == 0:
        st.warning('Function missing parameters')
    else:
        response = requests.get(url=url_pkg, data=input)
        func_pkg.write('Output:', help='the result from the function invoked')
        func_pkg.info(response.text)


@st.experimental_singleton
def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='123456',
                                          database='openfaas_test')


@st.experimental_singleton
def get_cursor(_connection):
    return _connection.cursor()


# database connection
connection = get_db_connection()
cursor = get_cursor(connection)

# Fifth container --- Database
database_module = st.container()
database_module.markdown('''
    # Database UI
    ''')
sql = 'select * from info'
result = pd.read_sql_query(sql, connection)

cursor.execute('SHOW TABLES')
result = cursor.fetchall()
table_list = ['Please Select']
for i in result:
    table_list.append(i[0])

my_selectbox = database_module.selectbox("Please select the table", table_list)
if my_selectbox == 'info':
    sql = 'select * from info'
    database_module.write(pd.read_sql_query(sql, connection))
elif my_selectbox == 'picture':
    sql = 'select * from picture'
    database_module.write(pd.read_sql_query(sql, connection))
elif my_selectbox == 'model':
    sql = 'select model_name from model'
    database_module.write(pd.read_sql_query(sql, connection))

input = database_module.text_area('请输入sql语句进行执行', help='the sql for database', key='database_module_text_area')
database_module_execute = database_module.button("execute", help='Push this button to execute the sql')
if database_module_execute:
    cursor.execute(input)
    connection.commit()

st.session_state

