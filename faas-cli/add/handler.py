def handle(req):
    array = req.replace('\n', '').split(',')
    rlt = 0
    for i in array:
        rlt += int(i)
    return rlt