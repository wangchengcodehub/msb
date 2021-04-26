import etcd3
import config


class EtcdClient(object):
    def __init__(self, host, port):
        self.client = etcd3.client(host=host, port=port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def etcd_put(self, key, value, *args, **kwargs):
        """
        写入数据到etcd
        :param key: etcd key
        :param value: etcd value
        :param args:
        :param kwargs:
        :return: code msg
        """
        # 判断形参类型，必须为字符串
        assert not hasattr(str, key), AttributeError
        assert not hasattr(str, value), AttributeError
        try:
            self.etcd_transaction(key=key, value=value)
        except BaseException as err:
            self.client.close()
            return -1, err
        else:
            return 0, "ok"

    def etcd_transaction(self, key, value, *args, **kwargs):
        """
        通过事务方式将数据写入到etcd中
        :param key: etcd key
        :param value: etcd value
        :return:
        """
        # etcd 事务控制:
        return self.client.transaction(
            compare=[
                self.client.transactions.value(key) == value,
                self.client.transactions.version(key) > 0,
            ],
            success=[
                self.client.transactions.put(key, value),
            ],
            failure=[
                self.client.transactions.put(key, value),
            ]
        )

    def watch_prefix(self, key):
        return self.client.watch_prefix(key)


# 暴露etcd对象：
etcd_client = EtcdClient(**config.MsbConfig.ETCD_CLIENT)
