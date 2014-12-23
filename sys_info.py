# -*- coding: utf8 -*-

import mongodb as database

'==样本状态操作=='

def get_sample_process_status(sample_hashvalue):
    return database.get_sample_process_status(sample_hashvalue)

def get_sample_ana_res(sample_hashvalue):
    return database.get_sample_ana_res(sample_hashvalue)

def get_sample_execute_para(sample_hashvalue):
    return database.get_sample_execute_para(sample_hashvalue)

def update_sample_ana_res(sample_hashvalue, ana_res):
    database.update_sample_ana_res(sample_hashvalue, ana_res)

def update_sample_process_status(sample_hashvalue, status):
    database.update_sample_process_status(sample_hashvalue, status)

def update_sample_execute_para(sample_hashvalue, para):
    database.update_sample_execute_para(sample_hashvalue, para)

def add_sample_status(sample_status):
    database.add_sample_status(sample_status)

'==样本状态操作==END=='


'==分析队列操作=='

def read_queue(vm_type, flag):
    return database.read_queue(vm_type, flag)

def get_sample_config(sample_hashvalue, vm_type):
    return database.get_sample_config(sample_hashvalue, vm_type)

def add_sample_to_queue(sample_info, vm_type):
    database.add_sample_to_queue(sample_info, vm_type)

def del_sample_from_queue(sample_hashvalue, vm_type):
    database.del_sample_from_queue(sample_hashvalue, vm_type)

def update_sample_checked_flag_in_queue(sample_hashvalue, vm_type, flag):
    database.update_sample_checked_flag_in_queue(
            sample_hashvalue,
            vm_type,
            flag)

'==分析队列操作==END=='


'==虚拟机列表操作=='
def get_idle_vms(vm_type):
    return database.get_idle_vms(vm_type)

def get_vm_info(vm_hashvalue, vm_type):
    return database.get_vm_info(vm_hashvalue, vm_type)

def get_vms_status(vm_type):
    return database.get_vms_status(vm_type)

def add_vm_to_vmlist(vm_type, vm_info):
    database.add_vm_to_vmlist(vm_type, vm_info)

def del_vm_from_vmlist(vm_hashvalue, vm_type):
    database.del_vm_from_vmlist(vm_hashvalue, vm_type)

def update_vm_status(vm_hashvalue, vm_type, status):
    database.update_vm_status(vm_hashvalue, vm_type, status)

def reset_vmlist(vm_type):
    database.reset_vmlist(vm_type)

def reset_vm_status(vm_hashvalue, vm_type):
    database.reset_vm_status(vm_hashvalue, vm_type)

def clear_vmlist(vm_type):
    database.clear_vmlist(vm_type)

def update_vm_counter(vm_hashvalue, vm_type):
    database.update_vm_counter(vm_hashvalue, vm_type)

def update_vm_interval(vm_hashvalue, vm_type, interval):
    database.update_vm_interval(vm_hashvalue, vm_type, interval)

'==虚拟机列表操作==END=='

"==日志存储=="
def pack(logfile, pcapfile, ssfile, strfile, hashvalue):
    return database.pack(logfile, pcapfile, ssfile, strfile, hashvalue)

def store_log(data):
    return database.store_log(data)

def read_log(hashvalue):
    return database.read_log(hashvalue)

"==日志存储==END=="

if  __name__ == '__main__':
    pass


