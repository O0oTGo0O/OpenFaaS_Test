from .func import Sequence
import json
def handle(req):
    req = json.loads(req)
    if req['function'] == 'sort':
        return Sequence.sort(json.dumps(req))
    if req['function'] == 'cut':
        return Sequence.cut(json.dumps(req))
    if req['function'] == 'reverse':
        return Sequence.reverse(json.dumps(req))
    return None