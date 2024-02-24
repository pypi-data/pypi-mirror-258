from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IPlayStreamPayload import IPlayStreamPayload
from nerualpha.providers.voice.csEvents import CSEvents
from nerualpha.providers.voice.contracts.IPlayStreamBody import IPlayStreamBody

@dataclass
class PlayStreamPayload(IPlayStreamPayload):
    body: IPlayStreamBody
    type_: str
    to: str = None
    def __init__(self,body: IPlayStreamBody,to: str = None):
        self.type_ = CSEvents.AudioPlay
        self.body = body
        if to is not None:
            self.to = to
        
    
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
