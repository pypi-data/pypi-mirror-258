import pymysql
from common.constants.database_config import HOST_DICT, PASSWD_DICT


def get_mpi_connection(env='test'):
    """
    获取ncpcs_mpi库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[env], port=4000, user="root", passwd=PASSWD_DICT[env],
                           db="ncpcs_mpi", charset="utf8")


def get_sibling_connection(env='test'):
    """
    获取ncpcs_sibling库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[env], port=4000, user="root", passwd=PASSWD_DICT[env],
                           db="ncpcs_sibling", charset="utf8")


def get_medical_data_analyze_connection(env='test'):
    """
    获取ncpcs_medical_data_analyze库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[env], port=4000, user="root", passwd=PASSWD_DICT[env],
                           db="ncpcs_medical_data_analyze", charset="utf8")


def get_tumour_stage_connection(env='test'):
    """
    获取ncpcs_solid_tumour_stage库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[env], port=4000, user="root", passwd=PASSWD_DICT[env],
                           db="ncpcs_tumour_stage", charset="utf8")


def get_tumor_connection(env='test'):
    """
    获取ncpcs_solid_tumour_stage库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[env], port=4000, user="root", passwd=PASSWD_DICT[env],
                           db="ncpcs_tumor", charset="utf8")