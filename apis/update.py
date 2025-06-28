from fastapi import APIRouter, HTTPException
import requests
from models import AppidAndCount

router = APIRouter(
    prefix="/v1",
)

@router.post('/getappupdateinfo', response_model=dict)
async def get_app_update_info(request_data: AppidAndCount):
    base_url = "https://api.taptapdada.com/apk/v1/list-by-app"
    params = {
        "referer": "app",
        "X-UA": "V=1&PN=TapTap&VN_CODE=283021001&LANG=zh_CN",
        "from": 0,
        "limit": request_data.count,
        "app_id": request_data.appid
    }
    
    try:
        if request_data.count > 10 :
            raise HTTPException(
                status_code=400,
                detail="请求的更新数量超过限制，最大值为10。"
            )
        response = requests.get(base_url, params=params, timeout=5)
        
        if response.status_code == 404:
            error_data = response.json()
            error_msg = error_data.get("data", {}).get("msg", "APPID不存在或无法访问")
            raise HTTPException(
                status_code=404,
                detail="尝试访问的APPID不存在，请检查你的APPID。错误详情：" + error_msg
            )
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("success"):
            error_msg = data.get("data", {}).get("msg", "API请求失败")
            raise HTTPException(
                status_code=400,
                detail="API请求失败，请检查API是否正确，或尝试更新以解决问题。" + error_msg
            )
        
        update_list = []
        for item in data.get("data", {}).get("list", []):
            version = item.get("version_label", "未知版本")
            whatsnew = item.get("whatsnew", {}).get("text", "无更新日志")
            update_list.append({
                "version": version,
                "info": whatsnew
            })
        
        return {"updates": update_list}
    
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