from django import template

register = template.Library()

@register.simple_tag
def replace(request, key, value):
    url_dict = request.GET.copy() #query: []をurl_dictに代入
    url_dict[key] = value #pagenation.htmlで引数にとっている、pageとpage_obj.---を追加
    return url_dict.urlencode() #urlの形にしてリターン