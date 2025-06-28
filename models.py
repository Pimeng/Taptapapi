from pydantic import BaseModel


class AppidAndCount(BaseModel):
    appid: int  # 应用ID
    count: int  # 数量

class OnlyAppid(BaseModel):
    appid: int  # 应用ID

class OnlyGroupid(BaseModel):
    groupid: int  # 群组ID

class UpdateInfo(BaseModel):
    version: str  # 版本号
    info: str     # 更新信息