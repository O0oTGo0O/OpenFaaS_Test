import io
import json
from PIL import Image, JpegImagePlugin
from .mysql import Database

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    req = json.loads(req)
    database = Database(host='166.111.73.96', user='root', password='123456', database='openfaas_test')
    image = database.get_image(req['id'])
    buffer = io.BytesIO(image)
    image = Image.open(buffer)

    if isinstance(image, JpegImagePlugin.JpegImageFile):
        label = database.get_label(req['id'])
        return json.dumps(label)
    return None
