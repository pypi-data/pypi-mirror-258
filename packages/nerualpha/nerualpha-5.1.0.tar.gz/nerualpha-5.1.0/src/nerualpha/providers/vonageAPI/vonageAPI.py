from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.vonageAPIActions import VonageAPIActions
from nerualpha.session.actionPayload import ActionPayload
from nerualpha.providers.vonageAPI.IVonageAPI import IVonageAPI
from nerualpha.session.ISession import ISession
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
T = TypeVar('T')
K = TypeVar('K')
@dataclass
class VonageAPI(IVonageAPI):
    session: ISession
    provider: str = field(default = "vonage-api")
    def __init__(self,session: ISession):
        self.session = session
    
    def invoke(self,url: str,method: str,body: T,headers: Dict[str,str] = None):
        payload = InvokePayload(url,method,body,headers)
        action = ActionPayload(self.provider,VonageAPIActions.Invoke,payload)
        return RequestInterface(self.session,action)
    
    def reprJSON(self):
        result = {}
        dict = asdict(self)
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type", "return_":"return"}
        for key in dict:
            val = getattr(self, key)

            if val is not None:
                if type(val) is list:
                    parsedList = []
                    for i in val:
                        if hasattr(i,'reprJSON'):
                            parsedList.append(i.reprJSON())
                        else:
                            parsedList.append(i)
                    val = parsedList

                if hasattr(val,'reprJSON'):
                    val = val.reprJSON()
                if key in keywordsMap:
                    key = keywordsMap[key]
                result.__setitem__(key.replace('_hyphen_', '-'), val)
        return result
