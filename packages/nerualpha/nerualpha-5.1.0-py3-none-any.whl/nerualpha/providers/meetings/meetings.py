from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.ISession import ISession
from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.vonageAPI.IVonageAPI import IVonageAPI
from nerualpha.providers.vonageAPI.vonageAPI import VonageAPI
from nerualpha.providers.meetings.contracts.deleteRoomPayload import DeleteRoomPayload
from nerualpha.providers.meetings.contracts.ICreateRoomPayload import ICreateRoomPayload
from nerualpha.providers.meetings.contracts.updateRoomDetails import UpdateRoomDetails
from nerualpha.providers.meetings.contracts.updateRoomPayload import UpdateRoomPayload
from nerualpha.providers.meetings.contracts.roomResponse import RoomResponse
from nerualpha.providers.meetings.contracts.getRoomsResponse import GetRoomsResponse
from nerualpha.request.requestMethods import RequestMethods

@dataclass
class Meetings:
    baseUrl: str
    vonageAPI: IVonageAPI
    session: ISession
    def __init__(self,session: ISession):
        self.session = session
        self.vonageAPI = VonageAPI(self.session)
        self.baseUrl = "https://api-eu.vonage.com/beta/meetings"
    
    def getRoom(self,roomId: str):
        url = f'{self.baseUrl}/rooms/{roomId}'
        method = RequestMethods.GET
        return self.vonageAPI.invoke(url,method,None)
    
    def getRooms(self,paginationUrl: str = None):
        url = f'{self.baseUrl}/rooms'
        if paginationUrl is not None:
            url = paginationUrl
        
        method = RequestMethods.GET
        return self.vonageAPI.invoke(url,method,None)
    
    def createRoom(self,createRoomPayload: ICreateRoomPayload):
        url = f'{self.baseUrl}/rooms'
        method = RequestMethods.POST
        return self.vonageAPI.invoke(url,method,createRoomPayload)
    
    def updateRoom(self,roomId: str,expiry: str,expireAfterUse: bool):
        details = UpdateRoomDetails(expiry,expireAfterUse)
        payload = UpdateRoomPayload(details)
        url = f'{self.baseUrl}/rooms/{roomId}'
        method = RequestMethods.PATCH
        return self.vonageAPI.invoke(url,method,payload)
    
    def deleteRoom(self,roomId: str):
        url = f'{self.baseUrl}/rooms/{roomId}'
        method = RequestMethods.DEL
        payload = DeleteRoomPayload()
        return self.vonageAPI.invoke(url,method,payload)
    
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
