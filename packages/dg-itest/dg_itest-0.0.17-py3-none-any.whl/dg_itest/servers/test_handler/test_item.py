#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 18:25
# @Author  : yaitza
# @Email   : yaitza@foxmail.com
import json
import re
import time

import allure
import pytest
import jsonpath
import traceback
from pathlib import *
from dg_itest import local_test_res
from dg_itest.utils.logger import logger, log_attach
from dg_itest.utils.diff_helper import DiffHelper
from dg_itest.servers.dg_servers.dg_singleton import DgSingleton
from dg_itest.utils.cache import local_cache
from dg_itest.utils.replace import Replace

class TestItem(pytest.Item):
    def __init__(self, name, parent, values):
        super(TestItem, self).__init__(name, parent)
        self.name = name
        self.values = values
        self.request = self.values.get("request")
        self.validate = self.values.get("validate")
        self.expect = self.values.get('expect')
        self.test_case_status = 0

    @pytest.mark.xfail()
    def runtest(self):
        logger.info(f'execute case: {self.name}; url: {self.values.get("request").get("url")}')
        request_data = self.replace(self.values['request'])
        params = request_data.get("params")
        if "files" in params.keys():
            params.update({"files": self.get_files(params.get("files"))})
        request_data.pop("params")
        request_data.update(params)
        exec_flag, exec_count = False, 0
        # try: # 此处不应该捕获异常，否则pytest无法判断用例failed
        while exec_count < 10 and not exec_flag :  # 异步任务，轮询执行10次保证完成后进行校验
            api = DgSingleton().apis
            response = api.http_request(**request_data)
            self.assert_response(response)
            exec_flag = self.check_status()
            if exec_count > 0 or not exec_flag: time.sleep(30)
            exec_count += 1
        assert self.test_case_status == 0, 'test case failed!'
        # except Exception as ex:
        #     logger.error(traceback.format_exc())
        #     allure.attach(traceback.format_exc(), 'error details info')

    # todo 断言类型需要增加，目前只支持eq(相等), co(包含), sa(存储)。
    def assert_response(self, response):
        for item in self.validate:
            if "sa" in item.keys():  # save临时存储，后面用例可用
                sa_value = item.get("sa")
                for sa_item_key in sa_value.keys():
                    sa_item_value =  jsonpath.jsonpath(response.json(), sa_value.get(sa_item_key))
                    assert type(sa_item_value) is list and len(sa_item_value) > 0, '\n' + '未获取到值'
                    sa_item_keep_value = eval(f'{item.get("convert")}({sa_item_value[0]})') if item.get("convert") else sa_item_value[0]
                    log_attach(f'   local cache --> ${sa_item_key}$:{sa_item_keep_value} , cache type: {str(type(sa_item_keep_value))}', name='save local cache')
                    local_cache.put(f"${sa_item_key}$", sa_item_keep_value)
            if "eq" in item.keys():  # equal 判等
                validate_rule = item.get("eq")
                actual_result = jsonpath.jsonpath(response.json(), validate_rule)
                expect_result = jsonpath.jsonpath(self.expect.get('json'), validate_rule)

                if isinstance(actual_result, list) and isinstance(expect_result, list):
                    actual_result = sorted(actual_result)
                    expect_result = sorted(expect_result)
                log_attach(f'   equal check --> validate_rule: {validate_rule} ,\nactual_result: {actual_result};\nexpect_result: {expect_result}', name='equal assert')
                assert actual_result == expect_result, '\n' + DiffHelper.diff(str(actual_result), str(expect_result))
                self.test_case_status = self.test_case_status + 1 if actual_result != expect_result else self.test_case_status
            if "co" in item.keys():  # contains包含
                contains_rule = item.get('co')
                actual_result = jsonpath.jsonpath(response.json(), contains_rule)
                expect_result = self.expect.get('contains')
                log_attach(f'contains check --> validate_rule: {contains_rule} ,\nactual_result: {actual_result};\nexpect_result: {expect_result}', name='contains assert')
                assert  actual_result in json.dumps(expect_result), f'{actual_result} not in {expect_result}'

    def check_status(self):
        """
        校验接口返回状态
        由于接口存在异步执行，返回对应状态耗时较长，通过其状态校验，多次循环执行得到正确实际状态
        :return: 返回状态
        """
        status = True
        for item in self.validate:
            if 'cs' in item.keys():
                cs_value = item.get('cs')
                for cs_item_key in cs_value.keys():
                    status = status and local_cache[f"${cs_item_key}$"] == cs_value.get(cs_item_key)
        return status

    def replace(self, source):
        """
        替换对应参数中的${},#{}
        """
        source = Replace.replace_local_cache(source)
        source = Replace.replace_keyword(source)
        return source

    def get_files(self, files_array):
        """
        替换文件为文件流
        """
        all_resource_files = Path(local_test_res).rglob("*.*")
        files_buffer = []
        for file_name in files_array:
            file = [file_item for file_item in all_resource_files if file_item.name == file_name]
            if len(file) > 0:
                suffix = file[0].suffix
                if suffix in ['.jpg', '.jpeg', '.png']:
                    content_type = f'image/{suffix.lstrip(".")}'
                elif suffix in ['.pdf']:
                    content_type = f'application/{suffix.lstrip(".")}'
                elif suffix in ['.xlsx']:
                    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                elif suffix in ['.xls']:
                    content_type = 'application/vnd.ms-excel'
                else:
                    content_type = '*/*'

                files_buffer.append(('file', (file_name, open(file[0].resolve(), 'rb'), content_type)))
            else:
                continue
        return files_buffer

