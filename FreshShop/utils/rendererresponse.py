from rest_framework.renderers import JSONRenderer

class Customrenderer(JSONRenderer):
    def render(self,data,accepted_media_type=None,renderer_context=None):
        if renderer_context:
            if isinstance(data,dict):
                msg = data.pop("msg","请求成功")
                code = data.pop("code",0)
            else:
                msg = "请求成功"
                code = 0
            ret = {
                "msg":msg,
                "code":code,
                "author":"clw",
                "data":data
            }
            return super(Customrenderer, self).render(ret,accepted_media_type,renderer_context)
        else:
            return super(Customrenderer, self).render(data,accepted_media_type,renderer_context)