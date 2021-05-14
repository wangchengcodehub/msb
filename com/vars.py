class Implemented(object):
    pass


class Status(object):

    BAD_REQUEST = "400"             # 客户端请求的语法错误，服务器无法理解
    UNAUTHORIZED = "401"            # 请求要求用户的身份认证
    FORBIDDEN = "403"               # 服务器理解请求客户端的请求，但是拒绝执行此请求
    NOT_FOUND = "404"               # 服务器无法根据客户端的请求找到资源

    OK = "200"                      # 请求成功
    CREATED = "201"                 # 已创建。成功请求并创建了新的资源
    ACCEPTED = "202"                # 已接受。已经接受请求，但未处理完成
    NO_CONTENT = "204"              # 无内容。服务器成功处理，但未返回内容

    INTERNAL_SERVER_ERROR = "500"   # 请求未完成。服务器遇到不可预知的情况。
    NOT_IMPLEMENTED = "501"         # 请求未完成。服务器不支持所请求的功能，或者服务器无法完成请求。


class ETCD(object):
    NAMESPACE = "/default/"
    DELETE = 1
    PUT = 0


class VISUAL_RANGE(object):
    """
    可见范围: 系统间:0，系统内:1，全部:0|1(默认)
    """
    OUTSIDE = "0"
    INSIDE = "1"
    DEFAULT = "0|1"


class PROTOCOL(object):
    """
    协议:（REST、UI、HTTP、TCP、UDP）
    """
    TCP = "tcp"
    HTTP = "http"






