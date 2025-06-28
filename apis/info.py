from fastapi import APIRouter, HTTPException
import requests
from models import OnlyAppid
import time

router = APIRouter(
    prefix="/v1",
)

@router.post('/getappinfo', response_model=dict)
async def get_app_info(request_data: OnlyAppid):
    base_url = "https://api.taptapdada.com/app/v6/detail"
    params = {
        "X-UA": "V=1&PN=TapTap&VN_CODE=284001001&LANG=zh_CN",
        "id" : request_data.appid,
    }

    try:
        response = requests.get(base_url, params, timeout=5)
        
        if response.status_code == 404:
            error_data = response.json()
            error_msg = error_data.get("data", {}).get("msg", "APPID")
            raise HTTPException(
                status_code=404,
                detail="不存在的APPID，请检查APPID是否正确。错误详情：" + error_msg # 404报错处理
            )
        
        response.raise_for_status()
        
        try: 
            data = response.json()
        except ValueError:
            error_data = response.text
            raise HTTPException(
                status_code=500,
                detail="API响应不是有效的JSON格式" + error_data
            )
        
        if not data.get("success"):
            error_msg = data.get("data", {}).get("msg", "API请求失败")
            raise HTTPException(
                status_code=400,
                detail="API请求失败，请检查API是否正确，或尝试更新以解决问题。" + error_msg
            )

        # 存一手数据
        raw = data.get("data", {}).get("app", {})

        # 获取应用信息
        app_packgename = raw.get('identifier', '未知包名')

        app_name = raw.get('title', '未知应用')

        app_icon = raw.get('icon', {}).get('url', 'https://www.taptap.cn/favicon.ico')

        updated_time = raw.get('update_time')
        if isinstance(updated_time, int):
            app_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updated_time))
        else:
            app_update_time = '未知更新时间'
        
        app_screenshots = raw.get('screenshots', [])
    
        app_description = raw.get('description', '无介绍')
        
        developer = raw.get('developer_bar', [])
        if isinstance(developer, list) and developer:
            app_developer = developer[0].get('text', '未知开发者')
        else:
            app_developer = '未知开发者'


        # 组合
        app_info = {
            "packname": app_packgename,
            "name": app_name,
            "icon": app_icon,
            "update_time": app_update_time,
            "screenshots": app_screenshots,
            "description": app_description,
            "app_developer": app_developer
        }

        return app_info
    
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
