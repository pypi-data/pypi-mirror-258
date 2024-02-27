import asyncio
import datetime
import sqlite3
import ssl
from pathlib import Path
from typing import Any, Callable, Final, List, Optional, Tuple, Union

import aiomysql
from aiotieba import get_logger as LOG
from aiotieba.typing import UserInfo

from .config import DB_CONFIG


def exec_handler_MySQL(create_table_func: Callable, default_ret: Any):
    """
    处理MySQL异常

    Args:
        create_table_func (Callable): 在无法连接数据库(2003)或表不存在时(1146)执行自动建表
        default_ret (Any): 出现错误时的默认返回值
    """

    def decorator(func):
        async def wrapper(self: "MySQLDB", *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except aiomysql.Error as err:
                try:
                    code = err.args[0]
                    if code in [2003, 1049]:
                        LOG().warning("无法连接数据库 将尝试自动建库")
                        await self.create_database()
                        await create_table_func(self)
                    elif code == 1146:
                        LOG().warning("表不存在 将尝试自动建表")
                        await create_table_func(self)
                except Exception:
                    pass
            return default_ret

        return wrapper

    return decorator


class MySQLDB(object):
    """
    MySQL交互

    Args:
        fname (str): 操作的目标贴吧名. Defaults to ''.

    Attributes:
        fname (str): 操作的目标贴吧名

    Note:
        容器特点: 读多写少 允许外部访问 数据安全性好
        一般用于数据持久化
    """

    __slots__ = ['fname', '_pool']

    _default_port: Final[int] = 3306
    _default_db_name: Final[str] = 'aiotieba'
    _default_minsize: Final[int] = 0
    _default_maxsize: Final[int] = 16
    _default_pool_recycle: Final[int] = 28800

    def __init__(self, fname: str = '') -> None:
        self.fname = fname
        self._pool: aiomysql.Pool = None

    async def __aenter__(self) -> "MySQLDB":
        await self._create_pool()
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None) -> None:
        if self._pool is not None:
            self._pool.close()
            await self._pool.wait_closed()

    async def _create_pool(self) -> None:
        """
        创建连接池
        """

        ssl_ctx = None
        if cafile := DB_CONFIG.get('ssl_cafile'):
            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_ctx.load_verify_locations(cafile=cafile)

        self._pool: aiomysql.Pool = await aiomysql.create_pool(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            db=DB_CONFIG.get('db', self._default_db_name),
            minsize=DB_CONFIG.get('minsize', self._default_minsize),
            maxsize=DB_CONFIG.get('maxsize', self._default_maxsize),
            pool_recycle=DB_CONFIG.get('pool_recycle', self._default_pool_recycle),
            loop=asyncio.get_running_loop(),
            autocommit=True,
            host=DB_CONFIG.get('host', 'localhost'),
            port=DB_CONFIG.get('port', self._default_port),
            unix_socket=DB_CONFIG.get('unix_socket'),
            ssl=ssl_ctx,
        )

    async def create_database(self) -> bool:
        """
        创建并初始化数据库

        Returns:
            bool: 操作是否成功
        """

        try:
            conn: aiomysql.Connection = await aiomysql.connect(
                host=DB_CONFIG.get('host', 'localhost'),
                port=DB_CONFIG.get('port', self._default_port),
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                unix_socket=DB_CONFIG.get('unix_socket'),
                autocommit=True,
                loop=asyncio.get_running_loop(),
                ssl=self._pool._conn_kwargs['ssl'],
            )

            async with conn.cursor() as cursor:
                db_name = DB_CONFIG.get('db', self._default_db_name)
                await cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")

            await self._create_pool()
            await conn.ensure_closed()

        except aiomysql.Error as err:
            LOG().warning(f"{err}. 请检查配置文件中的`Database`字段是否填写正确")
            return False

        LOG().info(f"成功创建并初始化数据库. db_name={db_name}")
        return True

    async def _create_table_forum(self) -> None:
        """
        创建表forum
        """

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "CREATE TABLE IF NOT EXISTS `forum` \
                    (`fid` INT PRIMARY KEY, `fname` VARCHAR(36) UNIQUE NOT NULL)"
                )
                LOG().info("成功创建表forum")

    @exec_handler_MySQL(_create_table_forum, 0)
    async def get_fid(self, fname: str) -> int:
        """
        通过贴吧名获取forum_id

        Args:
            fname (str): 贴吧名

        Returns:
            int: 该贴吧的forum_id
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT `fid` FROM `forum` WHERE `fname`='{fname}'")

                if res_tuple := await cursor.fetchone():
                    return res_tuple[0]
                return 0

        except aiomysql.Error as err:
            LOG().warning(f"{err}. fname={self.fname}")
            raise

    @exec_handler_MySQL(_create_table_forum, '')
    async def get_fname(self, fid: int) -> str:
        """
        通过forum_id获取贴吧名

        Args:
            fid (int): forum_id

        Returns:
            str: 该贴吧的贴吧名
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT `fname` FROM `forum` WHERE `fid`={fid}")
                    if res_tuple := await cursor.fetchone():
                        return res_tuple[0]
                    return ''

        except aiomysql.Error as err:
            LOG().warning(f"{err}. fid={fid}")
            raise

    @exec_handler_MySQL(_create_table_forum, False)
    async def add_forum(self, fid: int, fname: str) -> bool:
        """
        向表forum添加forum_id和贴吧名的映射关系

        Args:
            fid (int): forum_id
            fname (str): 贴吧名

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"INSERT IGNORE INTO `forum` VALUES ({fid},'{fname}')")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. fname={self.fname} fid={fid}")
            raise

    async def _create_table_user(self) -> None:
        """
        创建表user
        """

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "CREATE TABLE IF NOT EXISTS `user` \
                    (`user_id` BIGINT PRIMARY KEY, `user_name` VARCHAR(14) NOT NULL DEFAULT '', `portrait` VARCHAR(36) UNIQUE NOT NULL, \
                    INDEX `user_name`(user_name))"
                )
                LOG().info("成功创建表user")

    @exec_handler_MySQL(_create_table_user, UserInfo())
    async def get_userinfo(self, _id: Union[str, int]) -> UserInfo:
        """
        获取用户信息

        Args:
            _id (str | int): 用户id user_id/user_name/portrait

        Returns:
            UserInfo: 用户信息 仅包含user_name/portrait/user_id
        """

        user = UserInfo(_id)

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    if user.user_id:
                        await cursor.execute(f"SELECT * FROM `user` WHERE `user_id`={user.user_id}")
                    elif user.portrait:
                        await cursor.execute(f"SELECT * FROM `user` WHERE `portrait`='{user.portrait}'")
                    elif user.user_name:
                        await cursor.execute(f"SELECT * FROM `user` WHERE `user_name`='{user.user_name}'")
                    else:
                        raise ValueError("Null input")

                    if res_tuple := await cursor.fetchone():
                        user = UserInfo()
                        user.user_id = res_tuple[0]
                        user.user_name = res_tuple[1]
                        user.portrait = res_tuple[2]
                        return user
                    return UserInfo()

        except aiomysql.Error as err:
            LOG().warning(f"{err}. user={user}")
            raise
        except Exception as err:
            LOG().warning(f"{err}. user={user}")
            return UserInfo()

    @exec_handler_MySQL(_create_table_user, False)
    async def add_user(self, user: UserInfo) -> bool:
        """
        将用户信息添加到表user

        Args:
            user (UserInfo): 待添加的用户信息

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"INSERT IGNORE INTO `user` VALUES ({user.user_id}, {user.user_name}, {user.portrait})"
                    )
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. user={user}")
            raise

    @exec_handler_MySQL(_create_table_user, False)
    async def del_user(self, user: UserInfo) -> bool:
        """
        从表user中删除用户信息

        Args:
            user (UserInfo): 待删除的用户信息

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    if user.user_id:
                        await cursor.execute(f"DELETE FROM `user` WHERE `user_id`={user.user_id}")
                    elif user.portrait:
                        await cursor.execute(f"DELETE FROM `user` WHERE `portrait`='{user.portrait}'")
                    elif user.user_name:
                        await cursor.execute(f"DELETE FROM `user` WHERE `user_name`='{user.user_name}'")
                    else:
                        raise ValueError("Null input")

                    LOG().info(f"Succeeded. user={user}")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. user={user}")
            raise
        except Exception as err:
            LOG().warning(f"{err}. user={user}")
            return False

    async def _create_table_tid(self) -> None:
        """
        创建表tid_{fname}
        """

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS `tid_{self.fname}` \
                    (`tid` BIGINT PRIMARY KEY, `tag` TINYINT NOT NULL DEFAULT 1, `record_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    INDEX `tag`(tag))"
                )
                await cursor.execute(
                    f"""CREATE EVENT IF NOT EXISTS `event_auto_del_tid_{self.fname}` \
                    ON SCHEDULE EVERY 1 DAY STARTS '2000-01-01 00:00:00' \
                    DO DELETE FROM `tid_{self.fname}` WHERE `record_time`<(CURRENT_TIMESTAMP() + INTERVAL -15 DAY)"""
                )
                LOG().info(f"成功创建表tid_{self.fname}")

    @exec_handler_MySQL(_create_table_tid, False)
    async def add_tid(self, tid: int, *, tag: int = 0) -> bool:
        """
        将tid添加到表tid_{fname}

        Args:
            tid (int): 主题帖tid
            tag (int, optional): 自定义标签. Defaults to 0.

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"REPLACE INTO `tid_{self.fname}` VALUES ({tid},{tag},DEFAULT)")
                    LOG().info(f"Succeeded. forum={self.fname} tid={tid} tag={tag}")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} tid={tid}")
            raise

    @exec_handler_MySQL(_create_table_tid, None)
    async def get_tid(self, tid: int) -> Optional[int]:
        """
        获取表tid_{fname}中tid对应的tag值

        Args:
            tid (int): 主题帖tid

        Returns:
            int | None: 自定义标签 None表示表中无记录
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT `tag` FROM `tid_{self.fname}` WHERE `tid`={tid}")

                    if res_tuple := await cursor.fetchone():
                        return res_tuple[0]
                    return None

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} tid={tid}")
            raise

    @exec_handler_MySQL(_create_table_tid, False)
    async def del_tid(self, tid: int) -> bool:
        """
        从表tid_{fname}中删除tid

        Args:
            tid (int): 主题帖tid

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"DELETE FROM `tid_{self.fname}` WHERE `tid`={tid}")

                    LOG().info(f"Succeeded. forum={self.fname} tid={tid}")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} tid={tid}")
            raise

    @exec_handler_MySQL(_create_table_tid, [])
    async def get_tid_list(self, tag: int = 0, *, limit: int = 128, offset: int = 0) -> List[int]:
        """
        获取表tid_{fname}中对应tag的tid列表

        Args:
            tag (int, optional): 待匹配的tag值. Defaults to 0.
            limit (int, optional): 返回数量限制. Defaults to 128.
            offset (int, optional): 偏移. Defaults to 0.

        Returns:
            list[int]: tid列表
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT `tid` FROM `tid_{self.fname}` WHERE `tag`={tag} LIMIT {limit} OFFSET {offset}"
                    )

                    res_tuples = await cursor.fetchall()
                    res_list = [res_tuple[0] for res_tuple in res_tuples]
                    return res_list

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname}")
            raise

    async def _create_table_user_id(self) -> None:
        """
        创建表user_id_{fname}
        """

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS `user_id_{self.fname}` \
                    (`user_id` BIGINT PRIMARY KEY, `permission` TINYINT NOT NULL DEFAULT 0, `note` VARCHAR(64) NOT NULL DEFAULT '', `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    INDEX `permission`(permission), INDEX `record_time`(record_time))"
                )
                LOG().info(f"成功创建表user_id_{self.fname}")

    @exec_handler_MySQL(_create_table_user_id, False)
    async def add_user_id(self, user_id: int, /, permission: int = 0, *, note: str = '') -> bool:
        """
        将user_id添加到表user_id_{fname}

        Args:
            user_id (int): 用户的user_id
            permission (int, optional): 权限级别. Defaults to 0.
            note (str, optional): 备注. Defaults to ''.

        Returns:
            bool: True成功 False失败
        """

        if not user_id:
            return False

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"REPLACE INTO `user_id_{self.fname}` VALUES ({user_id},{permission},'{note}',DEFAULT)"
                    )

                    LOG().info(f"Succeeded. forum={self.fname} user_id={user_id} permission={permission}")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} user_id={user_id}")
            raise

    @exec_handler_MySQL(_create_table_user_id, False)
    async def del_user_id(self, user_id: int) -> bool:
        """
        从表user_id_{fname}中删除user_id

        Args:
            user_id (int): 用户的user_id

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"DELETE FROM `user_id_{self.fname}` WHERE `user_id`={user_id}")

                    LOG().info(f"Succeeded. forum={self.fname} user_id={user_id}")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} user_id={user_id}")
            raise

    @exec_handler_MySQL(_create_table_user_id, 0)
    async def get_user_id(self, user_id: int) -> int:
        """
        获取表user_id_{fname}中user_id的权限级别

        Args:
            user_id (int): 用户的user_id

        Returns:
            int: 权限级别
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT `permission` FROM `user_id_{self.fname}` WHERE `user_id`={user_id}")

                    if res_tuple := await cursor.fetchone():
                        return res_tuple[0]
                    return 0

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} user_id={user_id}")
            raise

    @exec_handler_MySQL(_create_table_user_id, (0, '', datetime.datetime(1970, 1, 1)))
    async def get_user_id_full(self, user_id: int) -> Tuple[int, str, datetime.datetime]:
        """
        获取表user_id_{fname}中user_id的完整信息

        Args:
            user_id (int): 用户的user_id

        Returns:
            tuple[int, str, datetime.datetime]: 权限级别, 备注, 记录时间
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT `permission`,`note`,`record_time` FROM `user_id_{self.fname}` WHERE `user_id`={user_id}"
                    )
                    if res_tuple := await cursor.fetchone():
                        return res_tuple
                    return 0, '', datetime.datetime(1970, 1, 1)

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} user_id={user_id}")
            raise

    @exec_handler_MySQL(_create_table_user_id, [])
    async def get_user_id_list(
        self, lower_permission: int = 0, upper_permission: int = 5, *, limit: int = 1, offset: int = 0
    ) -> List[int]:
        """
        获取表user_id_{fname}中user_id的列表

        Args:
            lower_permission (int, optional): 获取所有权限级别大于等于lower_permission的user_id. Defaults to 0.
            upper_permission (int, optional): 获取所有权限级别小于等于upper_permission的user_id. Defaults to 5.
            limit (int, optional): 返回数量限制. Defaults to 1.
            offset (int, optional): 偏移. Defaults to 0.

        Returns:
            list[int]: user_id列表
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT `user_id` FROM `user_id_{self.fname}` WHERE `permission`>={lower_permission} AND `permission`<={upper_permission} ORDER BY `record_time` DESC LIMIT {limit} OFFSET {offset}"
                    )

                    res_tuples = await cursor.fetchall()
                    res_list = [res_tuple[0] for res_tuple in res_tuples]
                    return res_list

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname}")
            raise

    async def _create_table_imghash(self) -> None:
        """
        创建表imghash_{fname}
        """

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS `imghash_{self.fname}` \
                    (`img_hash` BIGINT UNSIGNED PRIMARY KEY, `raw_hash` CHAR(40) UNIQUE NOT NULL, `permission` TINYINT NOT NULL DEFAULT 0, `note` VARCHAR(64) NOT NULL DEFAULT '', `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    INDEX `permission`(permission), INDEX `record_time`(record_time))"
                )
                LOG().info(f"成功创建表imghash_{self.fname}")

    @exec_handler_MySQL(_create_table_imghash, False)
    async def add_imghash(self, img_hash: int, raw_hash: str, /, permission: int = 0, *, note: str = '') -> bool:
        """
        将img_hash添加到表imghash_{fname}

        Args:
            img_hash (int): 图像的ahash
            raw_hash (str): 贴吧图床hash
            permission (int, optional): 封锁级别. Defaults to 0.
            note (str, optional): 备注. Defaults to ''.

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"REPLACE INTO `imghash_{self.fname}` VALUES ({img_hash},'{raw_hash}',{permission},'{note}',DEFAULT)"
                    )

                    LOG().info(f"Succeeded. forum={self.fname} img_hash={img_hash} permission={permission}")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} img_hash={img_hash}")
            raise

    @exec_handler_MySQL(_create_table_imghash, False)
    async def del_imghash(self, img_hash: int, *, hamming_dist: int = 0) -> bool:
        """
        从表imghash_{fname}中删除img_hash

        Args:
            img_hash (int): 图像的ahash
            hamming_dist (int): 匹配的最大海明距离 默认为0 即要求图像ahash完全一致

        Returns:
            bool: True成功 False失败
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    if hamming_dist > 0:
                        await cursor.execute(
                            f"DELETE FROM `imghash_{self.fname}` WHERE BIT_COUNT(`img_hash`^{img_hash})<={hamming_dist}"
                        )
                    else:
                        await cursor.execute(f"DELETE FROM `imghash_{self.fname}` WHERE `img_hash`={img_hash}")

                    LOG().info(f"Succeeded. forum={self.fname} img_hash={img_hash}")
                    return True

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} img_hash={img_hash}")
            raise

    @exec_handler_MySQL(_create_table_imghash, 0)
    async def get_imghash(self, img_hash: int, *, hamming_dist: int = 0) -> int:
        """
        获取表imghash_{fname}中img_hash的封锁级别

        Args:
            img_hash (int): 图像的ahash
            hamming_dist (int): 匹配的最大海明距离 默认为0 即要求图像ahash完全一致

        Returns:
            int: 封锁级别
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    if hamming_dist > 0:
                        await cursor.execute(
                            f"SELECT `permission`,BIT_COUNT(`img_hash`^{img_hash}) AS hd FROM `imghash_{self.fname}` HAVING hd<={hamming_dist} ORDER BY hd ASC LIMIT 1"
                        )
                    else:
                        await cursor.execute(
                            f"SELECT `permission` FROM `imghash_{self.fname}` WHERE `img_hash`={img_hash}"
                        )

                    if res_tuple := await cursor.fetchone():
                        return res_tuple[0]
                    return 0

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} img_hash={img_hash}")
            raise

    @exec_handler_MySQL(_create_table_imghash, (0, ''))
    async def get_imghash_full(self, img_hash: int, *, hamming_dist: int = 0) -> Tuple[int, str]:
        """
        获取表imghash_{fname}中img_hash的完整信息

        Args:
            img_hash (int): 图像的ahash
            hamming_dist (int): 匹配的最大海明距离 默认为0 即要求图像ahash完全一致

        Returns:
            tuple[int, str]: 封锁级别, 备注
        """

        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    if hamming_dist > 0:
                        await cursor.execute(
                            f"SELECT `permission`,`note`,BIT_COUNT(`img_hash`^{img_hash}) AS hd FROM `imghash_{self.fname}` HAVING hd<={hamming_dist} ORDER BY hd ASC LIMIT 1"
                        )
                    else:
                        await cursor.execute(
                            f"SELECT `permission`,`note` FROM `imghash_{self.fname}` WHERE `img_hash`={img_hash}"
                        )

                    if res_tuple := await cursor.fetchone():
                        return res_tuple[:2]
                    return 0, ''

        except aiomysql.Error as err:
            LOG().warning(f"{err}. forum={self.fname} img_hash={img_hash}")
            raise


class SQLiteDB(object):
    """
    SQLite交互

    Args:
        fname (str): 操作的目标贴吧名. Defaults to ''.

    Attributes:
        fname (str): 操作的目标贴吧名

    Note:
        容器特点: 读多写多 不允许外部访问 数据安全性差
        一般用于快速缓存
    """

    __slots__ = ['fname', '_conn']

    def __init__(self, fname: str = '') -> None:
        self.fname = fname
        db_path = Path(f".cache/{self.fname}.sqlite")
        need_init = False

        if not db_path.exists():
            need_init = True
            db_path.parent.mkdir(0o755, exist_ok=True)

        self._conn = sqlite3.connect(str(db_path), timeout=15.0, isolation_level=None, cached_statements=64)
        self._conn.execute("PRAGMA journal_mode=OFF")
        self._conn.execute("PRAGMA synchronous=OFF")
        if need_init:
            self._create_table_id()

    def close(self) -> None:
        self._conn.close()

    def _create_table_id(self) -> None:
        """
        创建表id_{fname}
        """

        self._conn.execute(
            f"CREATE TABLE IF NOT EXISTS `id_{self.fname}` \
            (`id` INTEGER PRIMARY KEY, `tag` INTEGER NOT NULL, `record_time` INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )

    def add_id(self, _id: int, *, tag: int = 0) -> bool:
        """
        将id添加到表id_{fname}

        Args:
            _id (int): tid或pid
            tag (int, optional): 自定义标签. Defaults to 0.

        Returns:
            bool: True成功 False失败
        """

        try:
            self._conn.execute(f"REPLACE INTO `id_{self.fname}` VALUES ({_id},{tag},NULL)")
        except sqlite3.Error as err:
            LOG().warning(f"{err}. forum={self.fname} id={_id}")
            return False
        return True

    def get_id(self, _id: int) -> Optional[int]:
        """
        获取表id_{fname}中id对应的tag值

        Args:
            _id (int): tid或pid

        Returns:
            int | None: 自定义标签 None表示表中无id
        """

        try:
            cursor = self._conn.execute(f"SELECT `tag` FROM `id_{self.fname}` WHERE `id`={_id}")
        except sqlite3.Error as err:
            LOG().warning(f"{err}. forum={self.fname} id={_id}")
            return False
        else:
            if res_tuple := cursor.fetchone():
                return res_tuple[0]
            return None

    def del_id(self, _id: int) -> bool:
        """
        从表id_{fname}中删除id

        Args:
            _id (int): tid或pid

        Returns:
            bool: True成功 False失败
        """

        try:
            self._conn.execute(f"DELETE FROM `id_{self.fname}` WHERE `id`={_id}")
        except sqlite3.Error as err:
            LOG().warning(f"{err}. forum={self.fname} id={_id}")
            return False

        LOG().info(f"Succeeded. forum={self.fname} id={_id}")
        return True

    def truncate(self, day: int) -> bool:
        """
        删除表id_{fname}中day天前的陈旧记录

        Args:
            day (int)

        Returns:
            bool: True成功 False失败
        """

        try:
            self._conn.execute(f"DELETE FROM `id_{self.fname}` WHERE `record_time` < datetime('now','-{day} day')")
            self._conn.execute("VACUUM")
        except sqlite3.Error as err:
            LOG().warning(f"{err}. forum={self.fname}")
            return False

        LOG().info(f"Succeeded. forum={self.fname} day={day}")
        return True
