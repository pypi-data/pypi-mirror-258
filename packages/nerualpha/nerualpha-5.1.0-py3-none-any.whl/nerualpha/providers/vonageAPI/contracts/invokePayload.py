from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.vonageAPI.contracts.IInvokePayload import IInvokePayload
T = TypeVar('T')
T = TypeVar("T")

@dataclass
class InvokePayload(IInvokePayload,Generic[T]):
    body: T
    method: str
    url: str
    headers: Dict[str,str] = None
    def __init__(self,url: str,method: str,body: T,headers: Dict[str,str] = None):
        self.url = url
        self.method = method
        self.body = body
        if headers is not None:
            self.headers = headers
        
    
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
