import inspect

from ytvs.client.unofficial import resources
from ytvs.client.unofficial.client import UnofficialClient
from ytvs.client.unofficial.resources.base_resource import Resource
from ytvs.constants import DEFAULT_API_KEY


def is_resource_endpoint(obj):
    """
    객체가 Resource의 인스턴스인지 확인.
    :param obj: 검사할 객체입니다.
    :return: 객체가 Resource의 인스턴스인 경우 True를 반환.
    """
    return isinstance(obj, Resource)


class UnofficialApi:
    # 비공식 APi를 구성하는 Resource 클래스들의 인스턴스를 초기화.
    search = resources.SearchResource()
    video = resources.VideoResource()
    channel = resources.ChannelResource()
    comment = resources.CommentResource()
    comment_thread = resources.CommentThreadResource()
    transcript = resources.TranscriptResource()

    def __new__(cls,
                proxies=None,
                use_tor: bool = False,
                tor_port:int = 9050,
                aws_apigw_endpoint=None,
                *args, **kwargs):
        """
        unofficialapi 클래스의 새 인스턴스를 생성.
        모든 sub resource들을 unofficialclient와 연결.
        :return: unofficialapi의 새 인스턴스.
        """
        self = super().__new__(cls)

        # 비공식 클라이언트 인스턴스를 생성.
        client = UnofficialClient(proxy_host=proxies,
                                  use_tor=use_tor,
                                  tor_port=tor_port,
                                  aws_apigw_endpoint=aws_apigw_endpoint)

        # 모든 리소스 엔드포인트를 UnofficialClient와 연결합니다.
        sub_resources = inspect.getmembers(self, is_resource_endpoint)
        for name, resource in sub_resources:
            resource_cls = type(resource)
            resource = resource_cls(client)
            setattr(self, name, resource)

        return self

    def __init__(self,
                 api_key=None,
                 proxies=None,
                 use_tor:bool=False,
                 aws_apigw_endpoint=None,
                 tor_port:int=9050
                 ):
        """
        UnofficialApi 클래스의 생성자.
        :param api_key: API 키입니다. 기본값은 ytvs.constants에서 정의된 DEFAULT_API_KEY.
        """
        self.api_key = api_key or DEFAULT_API_KEY
        self.proxies = proxies
        self.use_tor = use_tor
        self.tor_port = tor_port
        self.aws_apigw_endpoint = aws_apigw_endpoint
