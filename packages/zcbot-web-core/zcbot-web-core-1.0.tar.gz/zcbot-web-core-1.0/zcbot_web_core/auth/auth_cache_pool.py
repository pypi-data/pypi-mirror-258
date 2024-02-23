# -*- coding: utf-8 -*-
import json
import logging
from typing import List, Set, Optional
from ..client.redis_client import Redis
from ..lib import cfg
from ..model.items import AuthUser

logger = logging.getLogger(__name__)
rds = Redis(redis_uri=cfg.get('AUTH_REDIS_URL', None), redis_db=cfg.get('AUTH_REDIS_DB', None)).client
default_expire = 43200


def save_cached_user(access_token: str, user: AuthUser, expire: int = None):
    if user:
        _expire = expire or default_expire
        user_json = json.dumps(user, default=lambda o: o.__dict__, ensure_ascii=False)
        rds.set(f'share:access:{access_token}', user_json, ex=_expire)


def get_cached_user(access_token: str) -> Optional[AuthUser]:
    rs = rds.get(f'share:access:{access_token}')
    if rs:
        js_user = json.loads(rs)
        if isinstance(js_user, str):
            js_user = json.loads(js_user)
        user = AuthUser(**js_user)
        user.userName = js_user.get('username')
        return user

    return None


def has_user(access_token: str) -> bool:
    return rds.exists(f'share:access:{access_token}')


def save_cached_permission(access_token: str, permissions: Set[str], expire: int = None):
    if permissions:
        key = f'share:permissions:{access_token}'
        for per in permissions:
            rds.sadd(key, per)
        _expire = expire or default_expire
        rds.expire(key, _expire)


def has_permission(access_token: str, permission: str) -> bool:
    return rds.sismember(f'share:permissions:{access_token}', f'"{permission}"')


def get_cached_permission(access_token: str) -> List[str]:
    return rds.smembers(f'share:permissions:{access_token}')


def clean_cache(access_token: str):
    rds.delete(f'share:access:{access_token}')
    rds.delete(f'share:permissions:{access_token}')


def get_user_by_token(token_str: str) -> Optional[AuthUser]:
    rs = rds.get(f'share:access:{token_str}')
    if rs:
        js_user = json.loads(rs)
        if isinstance(js_user, str):
            js_user = json.loads(js_user)
        user = AuthUser(**js_user)
        user.userName = js_user.get('name')
        return user

    return None
