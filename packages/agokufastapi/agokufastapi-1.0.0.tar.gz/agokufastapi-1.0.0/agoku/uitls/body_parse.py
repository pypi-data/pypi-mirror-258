from fastapi import Request
async def get_body(request: Request):
    """
    获取客户端提交的body数据
    :param request:
    :return:
    """
    body = {}
    try:
        body = await request.json()
    except Exception as e:
        body = {}
    finally:
        request.state.body = body

    return body


async def get_body_json(request: Request):
    """
    获取客户端提交的body数据
    :param request:
    :return:
    """
    body = {}
    try:
        body = await request.json()
    except Exception as e:
        body = {}
    finally:
        request.state.body = body

    return body