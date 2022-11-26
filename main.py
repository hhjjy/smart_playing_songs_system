from pydantic import BaseModel, ValidationError, validator
from dataclasses import dataclass
from fastapi import FastAPI
from pydantic import BaseModel,ValidationError, validator
from typing import Optional
import re
class Command(BaseModel):
    instruction:str
    data:str = ""
    # 驗證指令格式
    @validator("instruction",pre=True)
    def check_instructions(cls, v):
        Insturction_definition = ["PLAY","STOP","NEXT","LAST","URL"]
        if v in Insturction_definition:
            return v 
        else:
            raise ValidationError
    # 驗證url格式 轉換 id 
    @validator("data",pre=True)
    def check_url_to_id(cls,v):
        # s = r"[a-zA-Z0-9_-]{11}"
        pattern = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        # 1. 驗證url正確性
        url_checker = re.compile(pattern)
        result = url_checker.match(v)
        # 2. 驗證ID正確性
        id_checker = re.compile(r"[A-Za-z0-9_\-]{11}")
        # 3. 結果判別
        if result != None:
            if id_checker.match(result.groups()[5]): # 如果匹配的文字又長度文字又對上則視為正確
                return result.groups()[5][0:11] #取得id 0~10個的文字
        raise ValidationError

app = FastAPI()
    
# get youtube video from post method
# /test/demo_form.php?name1=value1&name2=value2 
# @app.post("/CMD")
# async def command():
#     return ""
#     # return f{"message":"we get the youtube video"}
    
# root : 當輸入路徑"/"，返回一個json file
@app.get("/")
async def root():
    return {"message":"hello world"}

# 
@app.post("/command/")
async def create_cmd(command: Command):
    return command


# @app.post("/items/")
# async def create_item(item: Item):
#     return item