from .oauth import Oauth


class OauthJWT(Oauth):

    def __call__(self, request, *args, **kwargs):
        pass
