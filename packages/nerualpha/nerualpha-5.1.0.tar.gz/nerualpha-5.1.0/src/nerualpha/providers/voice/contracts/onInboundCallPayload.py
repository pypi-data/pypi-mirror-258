from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IOnInboundCallPayload import IOnInboundCallPayload
from nerualpha.session.IWrappedCallback import IWrappedCallback
from nerualpha.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint

@dataclass
class OnInboundCallPayload(IOnInboundCallPayload):
    to: IChannelPhoneEndpoint
    callback: IWrappedCallback
    from_: IChannelPhoneEndpoint = None
    def __init__(self,callback: IWrappedCallback,to: IChannelPhoneEndpoint,from_: IChannelPhoneEndpoint = None):
        self.callback = callback
        self.to = to
        if from_ is not None:
            self.from_ = from_
        
    
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
