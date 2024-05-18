import json
from django.http.response import HttpResponse
import datetime

# dict型をJSONとして変換し、レスポンスとして返却する
def make_json_response(data, status=200):
    return HttpResponse(json.dumps(data, default=json_serial, ensure_ascii=False), content_type='application/json; charset=UTF-8', status=status)

# リクエストボディからJSONをロードする。ボディにデータがない場合400を返却
def request_body_to_json(request_body):
    if not request_body:
        return HttpResponse(status=400)
    request_json = request_body.decode("utf-8")
    return json.loads(request_json)

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        return obj.astimezone().isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
