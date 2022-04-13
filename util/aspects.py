import logging

from django.db import transaction

logger = logging.getLogger('api')


def ginza_transactional(func):
    def wrapper(*args, **kwargs):
        with transaction.atomic():
            save_point = transaction.savepoint()
            try:
                ret = func(*args, **kwargs)
                transaction.savepoint_commit(save_point)
                return ret
            except Exception as e:
                logger.error('transaction rollback cause : ' + repr(e))
                transaction.savepoint_rollback(save_point)
                raise e
    return wrapper
