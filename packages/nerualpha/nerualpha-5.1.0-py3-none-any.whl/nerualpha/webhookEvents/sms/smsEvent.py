from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.webhookEvents.sms.ISMSEvent import ISMSEvent
from nerualpha.webhookEvents.sms.ISMSMetadata import ISMSMetadata
from nerualpha.webhookEvents.sms.ISMSUsage import ISMSUsage

@dataclass
class SMSEvent(ISMSEvent):
    to: str
    timestamp: str
    message_uuid: str
    from_: str
    channel: str
    usage: ISMSUsage = None
    sms: ISMSMetadata = None
    def __init__(self):
        pass
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
