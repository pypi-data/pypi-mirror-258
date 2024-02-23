# -*- coding:utf-8 -*-
"""
# File       : core.py
# Time       ：2024/2/23 13:40
# Author     ：andy
# version    ：python 3.9
"""
import json
import uuid

import requests
from .comments import TIMEOUT, MODELS_URL, PROMPTS_URL, KGS_URL, LOCAL_URL, ONLINE_URL
from .protocol import ModelCard, ModelList, FinalResponse, PromptCard, PromptList, KGList, KGCard, \
    ChatCompletionResponseChoice, ChatMessage, ChatCompletionResponseUsage, ChatCompletionResponse
from .utils import create_token

class FengChao:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    @staticmethod
    def models() -> FinalResponse:
        """
        查看支持的模型列表
        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = requests.request("GET", MODELS_URL, headers=headers, timeout=TIMEOUT)
        except Exception as e:
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            model = json.loads(response.text)
            model_card = [ModelCard(id=m.get('id'), owned_by=m.get('owned_by'), mode=m.get('mode'),
                                    price=m.get('price'), unit=m.get('unit'), max_token=m.get('unit'),
                                    channel=m.get('channel')) for m in model['data']]
            return FinalResponse(data=ModelList(data=model_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    @staticmethod
    def prompts() -> FinalResponse:
        """
        查看支持的指令列表
        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = requests.request("GET", PROMPTS_URL, headers=headers, timeout=TIMEOUT)
        except Exception as e:
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            prompt = json.loads(response.text)
            prompt_card = [PromptCard(id=p.get('id'), prefix=p.get('prefix'), prompt=p.get('prompt'),
                                    system=p.get('system')) for p in prompt['data']]
            return FinalResponse(data=PromptList(data=prompt_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    @staticmethod
    def kgs() -> FinalResponse:
        """
        查看支持的知识库列表
        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = requests.request("GET", KGS_URL, headers=headers, timeout=TIMEOUT)
        except Exception as e:
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            kg = json.loads(response.text)
            kg_card = [KGCard(id=k.get('id'), desc=k.get('desc')) for k in kg['data']]
            return FinalResponse(data=KGList(data=kg_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    def check_model_channel(self, model):
        model_list = self.models()
        if model_list.status == 200:
            for model_card in model_list.data.data:
                if model_card.id == model:
                    return model_card.channel
        return None

    @staticmethod
    def prepare_chat_result(response):
        choices = ChatCompletionResponseChoice(
            index=response['choices'][0]['index'],
            message=ChatMessage(role=response['choices'][0]['message']['role'],
                                content=response['choices'][0]['message']['content']),
            finish_reason=response['choices'][0]['finish_reason']
        )
        usage = ChatCompletionResponseUsage(
            prompt_tokens=response['usage']['prompt_tokens'],
            completion_tokens=response['usage']['completion_tokens'],
            total_tokens=response['usage']['total_tokens']
        )
        chunk = ChatCompletionResponse(request_id=response['request_id'], model=response['model'], choices=[choices],
                                       usage=usage, status=200, msg="执行成功", knowledge=response['knowledge'])
        return chunk

    def invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        try:
            response = requests.request("POST", url, json=payload, headers=headers, timeout=TIMEOUT)
        except Exception as e:
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:  # 请求正常
            result = json.loads(response.text)
            if result['status'] == 200:  # 响应正常
                result = self.prepare_chat_result(result)
                return FinalResponse(data=result)
            else:  # 响应异常
                return FinalResponse(status=result['status'], msg=result['msg'])
        else:  # 请求异常
            return FinalResponse(status=response.status_code, msg=response.text)

    @staticmethod
    def async_invoke_chat(url:str, headers:dict, payload:dict) -> FinalResponse:
        try:
            response = requests.request("POST", url, json=payload, headers=headers, timeout=TIMEOUT)
        except Exception as e:
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:  # 请求正常
            result = json.loads(response.text)
            if result['status'] == 200:  # 响应正常
                return FinalResponse(data=result['choices'][0]['message']['content'])
            else:  # 响应异常
                return FinalResponse(status=result['status'], msg=result['msg'])
        else:  # 请求异常
            return FinalResponse(status=response.status_code, msg=response.text)

    def sse_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        try:
            response = requests.request("POST", url, json=payload, headers=headers, timeout=TIMEOUT)
        except Exception as e:
            yield FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        else:
            if response.status_code == 200: # 请求正常
                for chunk in response.iter_lines(decode_unicode=True):
                    if chunk.startswith(":") or not chunk:
                        continue
                    field, _p, value = chunk.partition(":")
                    if field == "data":
                        result = json.loads(value)
                        if result['status'] == 200: # 响应正常
                            result = self.prepare_chat_result(result)
                            yield FinalResponse(data=result)
                        else: # 响应异常
                            yield FinalResponse(status=result['status'], msg=result['msg'])
            else: # 请求异常
                yield FinalResponse(status=response.status_code, msg=response.text)


    def chat(self, model: str, query = None, request_id = None, system=None, prompt=None, is_sensitive=True,
             task_id=None, history=None, do_sample=True, temperature=0.8, top_p=0.75, max_tokens=256,
             mode='invoke', knowledge=None) -> FinalResponse:
        token = create_token(self.api_key, self.secret_key)
        if history is None:
            history = []
        if request_id is None:
            request_id = uuid.uuid1().__str__()
        if mode == 'async_result' and task_id is None: raise ValueError("task_id不能为空")
        headers = {
            "content-type": "application/json",
            "Authorization": token
        }
        payload = {
            'model':model,
            'query':query,
            'request_id':request_id,
            'system':system,
            'prompt':prompt,
            'is_sensitive':is_sensitive,
            'task_id':task_id,
            'history':history,
            'do_sample':do_sample,
            'temperature':temperature,
            'top_p':top_p,
            'max_tokens':max_tokens,
            'knowledge':knowledge,
            'mode':mode
        }
        url = LOCAL_URL if self.check_model_channel(model) == "本地模型" else ONLINE_URL
        if mode == 'invoke':
            return self.invoke_chat(url, headers, payload)
        elif mode == 'async':
            return self.async_invoke_chat(url, headers, payload)
        elif mode == 'async_result':
            return self.invoke_chat(url, headers, payload)
        elif mode == 'stream':
            return self.sse_chat(url, headers, payload)
        else:
            raise "{}不支持的模式".format(mode)

