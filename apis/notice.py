from fastapi import APIRouter, HTTPException
import requests
from models import OnlyGroupid

router = APIRouter(
    prefix="/v1",
)

@router.post('/getappnoticeinfo', response_model=dict)
async def get_app_notice_info(request_data: OnlyGroupid):
    base_url = "https://api.taptapdada.com/feed/v7/by-group"
    params = {
        "X-UA": "V=1&PN=TapTap&VN_CODE=284001001&LANG=zh_CN",
        "type": "official",
        "group_id": request_data.groupid
    }

    try:
        response = requests.get(base_url, params, timeout=5)
        
        if response.status_code == 404:
            error_data = response.json()
            error_msg = error_data.get("data", {}).get("msg", "GroupID不存在或无法访问")
            raise HTTPException(
                status_code=404,
                detail="尝试访问的GroupID不存在，请检查你的GroupID。错误详情：" + error_msg
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

        # 公告数据处理段
        notice_list = []
        
        # 提取第一个moment的信息
        first_moment = data['data']['list'][0]['moment']
        author = first_moment['author']['user']['name']
        title = first_moment['topic']['title']
        content = first_moment['topic']['summary']
        
        notice_list.append({
            "author": author,
            "title": title,
            "content": content
        })
        
        return {"notice": notice_list}
    
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