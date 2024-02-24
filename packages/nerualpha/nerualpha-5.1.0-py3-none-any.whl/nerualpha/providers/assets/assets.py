from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.services.config.IConfig import IConfig
from nerualpha.session.ISession import ISession
from nerualpha.providers.assets.IAssets import IAssets
from nerualpha.providers.assets.contracts.directoryPayload import DirectoryPayload
from nerualpha.providers.assets.contracts.removeAssetPayload import RemoveAssetPayload
from nerualpha.providers.assets.contracts.listAssetsPayload import ListAssetsPayload
from nerualpha.IBridge import IBridge
from nerualpha.providers.assets.assetsActions import AssetsActions
from nerualpha.request.requestMethods import RequestMethods
from nerualpha.session.requestInterfaceWithParams import RequestInterfaceWithParams
from nerualpha.request.requestParams import RequestParams
from nerualpha.providers.assets.contracts.linkPayload import LinkPayload
from nerualpha.providers.assets.contracts.assetLinkResponse import AssetLinkResponse
from nerualpha.providers.assets.contracts.assetListResponse import AssetListResponse
from nerualpha.request.formDataObject import FormDataObject
from nerualpha.request.IFormDataObject import IFormDataObject
from nerualpha.request.responseTypes import ResponseTypes
from nerualpha.providers.assets.fileRetentionPeriod import FileRetentionPeriod

@dataclass
class Assets(IAssets):
    bridge: IBridge
    session: ISession
    config: IConfig
    provider: str = field(default = "vonage-assets")
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = session.bridge
        self.config = session.config
    
    def createDir(self,name: str):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = DirectoryPayload(name)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.Mkdir)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def remove(self,remoteFilePath: str,recursive: bool = False):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = RemoveAssetPayload(remoteFilePath,recursive)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.Remove)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def getRemoteFile(self,remoteFilePath: str):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.GET
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.Binary,{"key": remoteFilePath})
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.responseType = ResponseTypes.STREAM
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def generateLink(self,remoteFilePath: str,duration: str = "5m"):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = LinkPayload(remoteFilePath,duration)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.Link)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def uploadFiles(self,localFilePaths: List[str],remoteDir: str,retentionPeriod: FileRetentionPeriod = None):
        streams = []
        for i in range(0,localFilePaths.__len__()):
            streams.append(self.bridge.createReadStream(localFilePaths[i]))
        
        return self.uploadData(streams,remoteDir,None,retentionPeriod)
    
    def uploadData(self,data: List[object],remoteDir: str,filenames: List[str] = None,retentionPeriod: FileRetentionPeriod = None):
        url = self.config.getExecutionUrl(self.provider,AssetsActions.Copy,{"dst": remoteDir,"retention": retentionPeriod})
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = []
        for i in range(0,data.__len__()):
            formData = FormDataObject()
            formData.name = f'file[{i}]'
            formData.value = data[i]
            if filenames is not None and filenames[i] is not None:
                formData.filename = filenames[i]
            
            requestParams.data.append(formData)
        
        requestParams.url = url
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.headers["Content-Type"] = "multipart/form-data"
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def list(self,remotePath: str,recursive: bool = False,limit: int = 1000):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = ListAssetsPayload(remotePath,recursive,limit)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.List)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
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
