import functools

from stash.consts import SIZE_KB, SIZE_MB, SIZE_GB
from stash.manager import StashManager
from stash.options import StashOptions


def size_kb(n: int) -> int:
    return SIZE_KB * n


def size_mb(n: int) -> int:
    return SIZE_MB * n


def size_gb(n: int) -> int:
    return SIZE_GB * n


def _init_cache(storage, codec, options: StashOptions) -> StashManager:
    cache_man = StashManager(storage=storage, codec=codec, options=options)
    return cache_man


def _init_fs_cache(codec, options: StashOptions) -> StashManager:
    from .storages.filesystem import FileSystemStorage

    return _init_cache(
        storage=FileSystemStorage(options=options), codec=codec, options=options
    )


def get_fs_zlib_stash(options: StashOptions) -> StashManager:
    from .codecs.zlib import ZlibCodec

    return _init_fs_cache(ZlibCodec(), options=options)


def get_fs_brotli_stash(options: StashOptions) -> StashManager:
    from .codecs.brotli import BrotliCodec

    return _init_fs_cache(BrotliCodec(), options=options)


def get_fs_zstd_stash(options: StashOptions) -> StashManager:
    from .codecs.zstd import ZstdCodec

    return _init_fs_cache(ZstdCodec(), options=options)


def get_fs_lzma_stash(options: StashOptions) -> StashManager:
    from .codecs.lzma import LzmaCodec

    return _init_fs_cache(LzmaCodec(), options=options)


def get_mongo_zlib_stash(options: StashOptions) -> StashManager:
    from .codecs.zlib import ZlibCodec
    from .storages.mongodb import MongoDbStorage

    storage = MongoDbStorage(options=options)
    return _init_cache(storage, ZlibCodec(), options=options)


def get_lmdb_brotli_stash(options: StashOptions) -> StashManager:
    from .codecs.brotli import BrotliCodec
    from .storages.lmdb import LmdbStorage

    storage = LmdbStorage(options=options)
    return _init_cache(storage, BrotliCodec(), options=options)


def get_lmdb_lzma_stash(options: StashOptions) -> StashManager:
    from .codecs.lzma import LzmaCodec
    from .storages.lmdb import LmdbStorage

    storage = LmdbStorage(options=options)
    return _init_cache(storage, LzmaCodec(), options=options)


def get_lmdb_stash(options: StashOptions) -> StashManager:
    from .codecs.passthru import PassthruCodec
    from .storages.lmdb import LmdbStorage

    storage = LmdbStorage(options=options)
    return _init_cache(storage, PassthruCodec(), options=options)


def get_lmdb_zlib_stash(options: StashOptions) -> StashManager:
    from .codecs.zlib import ZlibCodec
    from .storages.lmdb import LmdbStorage

    storage = LmdbStorage(options=options)
    return _init_cache(storage, ZlibCodec(), options=options)


def get_lmdb_zstd_stash(options: StashOptions) -> StashManager:
    from .codecs.zstd import ZstdCodec
    from .storages.lmdb import LmdbStorage

    storage = LmdbStorage(options=options)
    return _init_cache(storage, ZstdCodec(), options=options)


def get_fs_stash(options: StashOptions) -> StashManager:
    return _init_fs_cache(codec=None, options=options)


def get_null_stash() -> StashManager:
    from .storages.null import NullStorage
    from .codecs.passthru import PassthruCodec

    options = StashOptions()
    return _init_cache(
        storage=NullStorage(options=options), codec=PassthruCodec(), options=options
    )


def get_dbm_zstd_stash(options: StashOptions) -> StashManager:
    from .codecs.zstd import ZstdCodec
    from .storages.dbm_ import DbmStorage

    storage = DbmStorage(options=options)
    return _init_cache(storage, ZstdCodec(), options=options)


def get_dbm_zlib_stash(options: StashOptions) -> StashManager:
    from .codecs.zlib import ZlibCodec
    from .storages.dbm_ import DbmStorage

    storage = DbmStorage(options=options)
    return _init_cache(storage, ZlibCodec(), options=options)


def get_dbm_brotli_stash(options: StashOptions) -> StashManager:
    from .codecs.brotli import BrotliCodec
    from .storages.dbm_ import DbmStorage

    storage = DbmStorage(options=options)
    return _init_cache(storage, BrotliCodec(), options=options)


def get_dbm_lzma_stash(options: StashOptions) -> StashManager:
    from .codecs.lzma import LzmaCodec
    from .storages.dbm_ import DbmStorage

    storage = DbmStorage(options=options)
    return _init_cache(storage, LzmaCodec(), options=options)


def get_dbm_stash(options: StashOptions) -> StashManager:
    from .storages.dbm_ import DbmStorage
    from .codecs.passthru import PassthruCodec

    storage = DbmStorage(options=options)
    return _init_cache(storage, codec=PassthruCodec(), options=options)


def get_lsmdb_brotli_stash(options: StashOptions) -> StashManager:
    from .codecs.brotli import BrotliCodec
    from .storages.lsmdb import LsmDbStorage

    storage = LsmDbStorage(options=options)
    return _init_cache(storage, BrotliCodec(), options=options)


def get_lsmdb_zstd_stash(options: StashOptions) -> StashManager:
    from .codecs.zstd import ZstdCodec
    from .storages.lsmdb import LsmDbStorage

    storage = LsmDbStorage(options=options)
    return _init_cache(storage, ZstdCodec(), options=options)


def get_lsmdb_lzma_stash(options: StashOptions) -> StashManager:
    from .codecs.lzma import LzmaCodec
    from .storages.lsmdb import LsmDbStorage

    storage = LsmDbStorage(options=options)
    return _init_cache(storage, LzmaCodec(), options=options)


def get_lsmdb_zlib_stash(options: StashOptions) -> StashManager:
    from .codecs.zlib import ZlibCodec
    from .storages.lsmdb import LsmDbStorage

    storage = LsmDbStorage(options=options)
    return _init_cache(storage, ZlibCodec(), options=options)


def get_lsmdb_stash(options: StashOptions) -> StashManager:
    from .storages.lsmdb import LsmDbStorage
    from .codecs.passthru import PassthruCodec

    storage = LsmDbStorage(options=options)
    return _init_cache(storage, codec=PassthruCodec(), options=options)


def get_leveldb_stash(options: StashOptions) -> StashManager:
    from .storages.leveldb import LeveldbStorage
    from .codecs.passthru import PassthruCodec

    storage = LeveldbStorage(options=options)
    return _init_cache(storage, codec=PassthruCodec(), options=options)


def get_leveldb_brotli_stash(options: StashOptions) -> StashManager:
    from .codecs.brotli import BrotliCodec
    from .storages.leveldb import LeveldbStorage

    storage = LeveldbStorage(options=options)
    return _init_cache(storage, BrotliCodec(), options=options)


def get_leveldb_zstd_stash(options: StashOptions) -> StashManager:
    from .codecs.zstd import ZstdCodec
    from .storages.leveldb import LeveldbStorage

    storage = LeveldbStorage(options=options)
    return _init_cache(storage, ZstdCodec(), options=options)


def get_leveldb_lzma_stash(options: StashOptions) -> StashManager:
    from .codecs.lzma import LzmaCodec
    from .storages.leveldb import LeveldbStorage

    storage = LeveldbStorage(options=options)
    return _init_cache(storage, LzmaCodec(), options=options)


def get_leveldb_zlib_stash(options: StashOptions) -> StashManager:
    from .codecs.zlib import ZlibCodec
    from .storages.leveldb import LeveldbStorage

    storage = LeveldbStorage(options=options)
    return _init_cache(storage, ZlibCodec(), options=options)


def stashify(stash: StashManager = None):
    stash_ = stash

    def decorator(function):
        stash = stash_
        if stash is None:
            stash = get_fs_stash(StashOptions())

        @functools.wraps(function)
        def func(*args, **kwargs):
            key = str(args)
            if not stash.exists(key):
                content = function(*args, **kwargs)
                stash.write(key=key, content=content)
                return content

            return stash.read(key)

        return func

    return decorator
