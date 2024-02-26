#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:李智敏
# Wechat:anark919
# Date:2024-02-26 15:53
# Title:

import datetime


def monitor(ok: object = None, err: object = None, notice: object = print,return_ok = False,return_err=False) -> any:
    '''
    运行监控函数
    :param ok: 接收一个目标函数执行成功后，运行的函数，接收目标函数的返回值，可选参数，默认为None
    :param err: 接收一个目标函数执行失败后，运行的函数，接收目标函数对象和错误信息对象，可选参数，默认为None
    :param notice:接收一个通知函数，函数执行成功或者失败后，将函数执行的状态、函数对象、执行完成时间、函数参数，传递给通知函数。
    :param return_ok:是否返回最后ok函数执行结果，默认False，返回当前函数执行结果
    :param return_err:是否返回err函数执行结果，默认False，异常时返回None
    :return:返回函数执行结果
    '''

    def outwrapper(func):
        def wrapper(*args, **kwargs):
            status = True
            data = None
            try:
                data = func(*args, **kwargs)
                if ok:
                    d = ok(data) # 执行成功时执行
                    if return_ok:
                        data = d
            except Exception as e:
                status = False
                e_d = err(func, e,*args, **kwargs)  # 错误时执行
                if return_err:
                    data = e_d
            notice(status, func, datetime.datetime.now(), *args, **kwargs) if notice else ...  # 函数执行的情况反馈给指定的函数
            return data

        return wrapper

    return outwrapper

def workflows(func_list=[],err_funcs={},*args,**kwargs):
    '''
    工作流函数
    :param func_list:工作流执行函数列表，按索引执行流函数，上一个函数的值做为下一个函数的参数传入。
    :param err_funcs:流函数异常处理分支函数字典，默认为print。异常函数参考：例如：err(func, e,*args, **kwargs)
    :param args:起点流函数接收的位置参数
    :param kwargs:起点流函数接收的关键字参数
    :return:返回起点流函数执行结果
    '''
    def flows(func_list=[]):
        if func_list:
            func=func_list.pop(0)
            err = err_funcs.get(func,print)
            if func1 := flows(func_list):
                return monitor(ok=func1,err=err,return_ok=True)(func)
            return func
    if f:=flows(func_list):
        return f(*args,**kwargs)


if __name__ == '__main__':


    def a1(*args,**kwargs):
        print('上一个函数的结果',*args,**kwargs)
        return 1
    def a2(*args,**kwargs):
        print('上一个函数的结果',*args,**kwargs)
        raise ValueError('错误')
    def a3(*args,**kwargs):
        print('上一个函数的结果',*args,**kwargs)
        return 3

    @monitor(ok=a3)
    def err(func,e):
        print(f"函数:{func.__name__}报错:{e}")
        return '2323'
    print(workflows([a1,a2,a3],{a2:err},'xxxxx'))

