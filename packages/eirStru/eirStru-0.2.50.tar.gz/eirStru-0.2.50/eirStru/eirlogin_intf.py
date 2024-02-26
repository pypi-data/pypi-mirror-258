import aiohttp
from aiohttp import ClientSession

from eirStru import *


class LoginIntf:
    def __init__(self, host):
        self.host = host

    async def check_account_info(self, params: ParamsCheckAccount):
        """
        检查账号
        """
        url = f'{self.host}/check_account_info/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        data = params.model_dump_json()

        try:
            async with ClientSession() as cs:
                async with cs.post(url, headers=headers, data=data, verify_ssl=False) as resp:
                    r_json = await resp.json()
                    return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_failed, message=f'{e}')

    async def get_session(self, carrier_id, action: ActionType, account: str = None, bookingagent_id: str = None,
                          sub_code: str = None) -> SessionData:
        url = f'{self.host}/get_session/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        params = ParamsGetSession()
        params.carrier_id = carrier_id
        params.action = action
        params.account = account
        params.bookingagent_id = bookingagent_id
        params.sub_code = sub_code

        try:
            async with ClientSession() as cs:
                async with cs.post(url, headers=headers, data=params.model_dump_json(), verify_ssl=False) as resp:
                    r_json = await resp.json()
                    return SessionData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_failed, message=f'{e}')

    async def return_session(self, session_data: SessionData):
        url = f'{self.host}/get_session/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        try:
            async with ClientSession() as cs:
                async with cs.post(url, headers=headers, data=session_data.model_dump_json(), verify_ssl=False) as resp:
                    r_json = await resp.json()
                    return SessionData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_failed, message=f'{e}')

    async def check_session_count(self, carrier_id, order_dict):
        url = f'{self.host}/check_session_count/'

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {'carrier_id': carrier_id}

        try:
            async with ClientSession() as cs:
                async with cs.post(url, headers=headers, params=data, verify_ssl=False) as resp:
                    r_json = await resp.json()
                    return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_failed, message=f'{e}')

    async def get_session_summary(self, carrier_id):
        url = f'{self.host}/get_session_summary/'

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {'carrier_id': carrier_id}

        try:
            async with ClientSession() as cs:
                async with cs.post(url, headers=headers, params=data, verify_ssl=False) as resp:
                    r_json = await resp.json()
                    return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_failed, message=f'{e}')

    async def get_session_by_guid(self, carrier_id, action: ActionType, session_guid) -> SessionData:
        url = f'{self.host}/get_session_by_guid/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        params = ParamsGetSession(**{'carrier_id': carrier_id, 'action': action, 'session_guid': session_guid})

        try:
            async with ClientSession() as cs:
                async with cs.post(url, headers=headers, data=params.model_dump_json(), verify_ssl=False) as resp:
                    r_json = await resp.json()
                    return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_failed, message=f'{e}')

    async def get_valid_sessions(self, carrier_id, action: ActionType):
        url = f'{self.host}/get_valid_sessions/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        params = ParamsGetSession(**{'carrier_id': carrier_id, 'action': action})

        try:
            async with ClientSession() as cs:
                async with cs.post(url, headers=headers, data=params.model_dump_json(), verify_ssl=False) as resp:
                    r_json = await resp.json()
                    return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_failed, message=f'{e}')

    async def set_wx_message(self, title, message, openid_list=None):
        data = {'first': {'value': title,
                          'color': '#173177'},
                'keyword1': {'value': message,
                             'color': '#173177'},
                'keyword2': {'value': f'',
                             'color': '#173177'},
                'keyword3': {'value': f'',
                             'color': '#173177'},
                'remark': {'value': f'',
                           'color': '#173177'}}
        if not openid_list:
            openid_list = ['ouYVowI3kLgwVo6WEuKXvj0gGoD4', 'ouYVowBn4G5vxlnYS91pnPxUBLQ4']
        for openid in openid_list:
            await self.send_wx(openid, data)

    async def send_price_wx(self, openid_list, route: SpotData):
        data = {'first': {'value': f'新运价:{route.carrier_id} {route.from_port}-{route.to_port}'.upper(),
                          'color': '#173177'},
                'keyword1': {'value': f'{route.vessel}/{route.voyage}/{route.line}',
                             'color': '#173177'},
                'keyword2': {'value': f' etd:{route.etd} days:{route.days}',
                             'color': '#173177'},
                'keyword3': {'value': f'{route.ctntype} price ${route.price}',
                             'color': '#173177'},
                'remark': {'value': f'截港日:{route.cut_off_datetime} 截单日:{route.doc_closure_datetime}',
                           'color': '#173177'}}
        if not openid_list:
            openid_list = ['ouYVowI3kLgwVo6WEuKXvj0gGoD4', 'ouYVowBn4G5vxlnYS91pnPxUBLQ4']

        for openid in openid_list:
            await self.send_wx(openid, data)

    # async def send_order_wx(openid_list, route):
    #     if route.get('carrier_id') is None:
    #         carrier_id = ''
    #     else:
    #         carrier_id = route.get('carrier_id')
    #     price = route.get('price')
    #     from_port = route.get('from_port')
    #     to_port = route.get('to_port')
    #     ctn_type = route.get('ctn_type')
    #     vessel_name = route.get('vesselName')
    #     voyage_no = route.get('voyageNo')
    #     etd = route.get('etd')
    #     billno = route.get('billno')
    #     client_id = route.get('client_id')
    #
    #     data = {'first': {'value': f'新订单: {from_port}-{to_port},{ctn_type}\n订单号:{billno}'.upper(),
    #                       'color': '#173177'},
    #             'keyword1': {'value': vessel_name,
    #                          'color': '#173177'},
    #             'keyword2': {'value': f'{voyage_no}  {etd}',
    #                          'color': '#173177'},
    #             'keyword3': {'value': f'{carrier_id} ${price}',
    #                          'color': '#173177'},
    #             'remark': {'value': f'{client_id}',
    #                        'color': '#173177'}}
    #     for openid in openid_list:
    #         await send_wx(openid, data)

    @staticmethod
    async def send_wx(openid, data):
        param = {'template_id': 'Hv8mju06e6KQ_pMeeFA5smt8j2cDWKEpRTPGjO4hTc8',
                 'url': '',
                 'topcolor': '#173177',
                 'data': data}

        url = 'http://meian.expressgo.cn/wechat/sendTemplateMsg/'
        param_str = json.dumps(param)
        payload = {
            'weChatConfigId': '4544c916-0ee1-4d89-8c8d-10d21287334a',
            'openidList': openid,
            'msgJson': param_str

        }

        # md5_data = json.dumps(payload)
        #
        # md5 = hashlib.md5(md5_data.encode(encoding='UTF-8')).hexdigest()
        # wx = await insert_wx(openid, param_str, md5)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=payload) as resp:
                if resp.status in [200, 201]:
                    r_text = await resp.text()
                    return r_text
