import csv
import ast
import configparser
import os




# 写入函数
def write_csv(file_name, data_list_name):
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data_list_name:
            writer.writerow(row)


def delete_file():
    file_list = ['trial_info', 'trial_pi_info', 'trial_site_info', 'trial_ec_info']
    for file_name in file_list:
        try:
            print('删除' + f'{file_name}')
            os.remove(f'data/{file_name}.csv')
        except OSError:
            print(f'{file_name}' + '不存在,跳过')
            pass


# 读取配置文件并处理数据
def read_conf(group_name, value_name, text):
    this_text = ''
    cf = configparser.ConfigParser()
    cf.read("replace.ini", encoding='utf-8')
    value = cf.get(group_name, value_name)
    cof_list = ast.literal_eval(value)
    for i in cof_list:
        this_text = text.replace(f'{i[0]}', f'{i[1]}').strip('\n').strip('\t')
        text = this_text
    return text


# 读配置文件
def read_config(group_name, value_name):
    cf = configparser.ConfigParser()
    cf.read("replace.ini", encoding='utf-8')
    value = cf.get(group_name, value_name)
    cof_list = ast.literal_eval(value)
    return cof_list

def get_ele_number( ele):
    num = len(ele)
    return num