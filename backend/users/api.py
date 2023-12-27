from django.contrib import auth
from django.contrib.auth.models import User
from django.db import transaction
from ninja import Router

from backend.common import response, Error
from users.schema import RegisterIn, LoginIn

router = Router(tags=["users"])


@router.post("/register", auth=None)
@transaction.atomic
def user_register(request, payload: RegisterIn):
    """
    用户注册接口
    - username：用户名
    - password：密码
    - confirm_password：确认密码
    """
    # 判断两次密码输入是否一致
    if payload.password != payload.confirm_password:
        return response(error=Error.PWD_ERROR)
    if payload.username is None or payload.username == "":
        return response(error=Error.USERNAME_IS_NULL)
    try:
        # 用户密码加密
        User.objects.get_by_natural_key(payload.username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)
    user = User.objects.create_user(username=payload.username, password=payload.password)
    users_info = {
        "id": user.id,
        "username": user.username
    }
    return response(item=users_info)


@router.post("/login", auth=None)
def user_login(request, payload: LoginIn):
    """
    用户登录接口
    - username：用户名
    - password：密码
    """
    username = payload.username
    password = payload.password
    # 用户认证
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        # 会向django_session表 创建一条数据
        auth.login(request, user)
        # 获取最新的session信息
        token = request.session
        user_info = {
            "id": user.id,
            "username": user.username,
            "token": token.session_key
        }
        return response(item=user_info)
    else:
        return response(error=Error.USER_OR_PWD_ERROR)


@router.get("/info")
def user_info(request):
    """
    获取当前登录的用户信息接口
    """
    # 获取当前登录的用户信息
    user = auth.get_user(request)
    if user.username != "":
        user_info = {
            'id': user.id,
            'username': user.username,
            'image': 'rose.png',
        }
        return response(item=user_info)
    else:
        return response(error=Error.USER_NOT_LOGIN)


@router.delete("/logout")
def user_logout(request):
    """
    用户退出登录接口
    """
    # 用户退出登录
    auth.logout(request)
    return response()
