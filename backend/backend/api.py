from django.contrib.sessions.models import Session
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.security import HttpBearer

from ai.api import router as ai_router
from api_infos.api import router as api_infos_router
from apis.api import router as apis_router
from cases.api import router as cases_router
from commons.api import router as commons_router
from envs.api import router as env_router
from httprunner_project.api import router as httprunner_project_router
from modules.api import router as modules_router
from project.api import router as projects_router
from test_data.api import router as test_data_router
from users.api import router as users_router


class InvalidToken(Exception):
    """
    无效token异常
    """
    pass


class OverdueToken(Exception):
    """
    过期token异常
    """
    pass


class GlobalAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        """
        自定义认证token处理
        """
        try:
            Session.objects.get(pk=token)
            # 获取设置session有效时间
            # SESSION_COOKIE_AGE
            # 当前时间
            # session创建时间
        except Session.DoesNotExist:
            raise InvalidToken
        else:
            return token


api = NinjaAPI(auth=GlobalAuth())


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    """
    无效token返回
    """
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@api.exception_handler(OverdueToken)
def in_overdue_token(request, exc):
    """
    过期token返回
    """
    return api.create_response(request, {"detail": "overdue token supplied"}, status=401)


# tags commons URI:/api/commons/xxx
api.add_router("/commons/", commons_router)
# tags users URI:/api/users/xxx
api.add_router("/users/", users_router)
# tags projects URI:/api/projects/xxx
api.add_router("/projects/", projects_router)
# tags modules URI:/api/modules/xxx
api.add_router("/modules/", modules_router)
# tags apis URI:/api/apis/xxx
api.add_router("/apis/", apis_router)
# tags env URI:/api/env/xxx
api.add_router("/env/", env_router)
# tags cases URI:/api/cases/xxx
api.add_router("/cases/", cases_router)
# tags api info URI:/api/info/xxx
api.add_router("/info/", api_infos_router)
# tags test data URI:/api/test/xxx
api.add_router("/test/", test_data_router)
# tags httprunner project data URI:/api/httprunner/xxx
api.add_router("/httprunner/", httprunner_project_router)
# tags ai project data URI:/api/httprunner/xxx
api.add_router("/ai/", ai_router)
