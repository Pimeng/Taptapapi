from fastapi import APIRouter, HTTPException
import requests
from models import 数据模型

router = APIRouter(
    prefix="/v1", # 前缀 这里是版本号
)

@router.post('/请求端点', response_model=dict)
async def 请求方法导出(request_data: 数据模型):
    base_url = "" # API端点
    params = {
        "X-UA": "",# 请求信息 Taptap强制要X-UA
    }

    try:
        response = requests.get(base_url, params, timeout=5)
        
        if response.status_code == 404:
            error_data = response.json()
            error_msg = error_data.get("data", {}).get("msg", "")
            raise HTTPException(
                status_code=404,
                detail="" + error_msg # 404报错处理
            )
        
        response.raise_for_status()
        
        try:
            data = response.json()
        except ValueError:
            raise HTTPException(
                status_code=500,
                detail="API响应不是有效的JSON格式"
            )
        
        if not data.get("success"):
            error_msg = data.get("data", {}).get("msg", "API请求失败")
            raise HTTPException(
                status_code=400,
                detail="API请求失败，请检查API是否正确，或尝试更新以解决问题。" + error_msg
            )

        #
        #   这里是处理得到的数据
        #

        return # 这里是要返回的信息
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"请求API失败: {str(e)}"
        )
    except (ValueError, KeyError, IndexError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"解析API响应失败: {str(e)}"
        )
        