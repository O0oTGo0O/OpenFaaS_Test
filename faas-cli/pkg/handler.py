import io
import json
import joblib
from PIL import Image
import numpy as np
from .mysql import Database
import sklearn

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    req = json.loads(req)
    image_id = req['image_id']
    model_name = req['model_name']
    database = Database(host='166.111.73.96', user='root', password='123456', database='openfaas_test')

    # load the model
    model = database.get_model(model_name)
    model = io.BytesIO(model)
    model = joblib.load(model)

    # load the image
    image = database.get_image(image_id)
    buffer = io.BytesIO(image)
    image = Image.open(buffer)
    image = np.array(image).reshape((1, -1))


    # store to the database
    database.update_label(image_id, model.predict(image)[0])
    return json.dumps(str(model.predict(image)[0]))