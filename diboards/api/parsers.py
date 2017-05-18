from flask_restplus import fields, reqparse

# get /board/<uuid>/qr
# ----------------------------------------------------------------------
qrparser = reqparse.RequestParser()
qrparser.add_argument('height', type=int, required=True)
qrparser.add_argument('width', type=int, required=True)
qrparser.add_argument('roundedEdges', type=bool)

# post /user
# ------------------------------------------------------------------------
userparser = reqparse.RequestParser()
qrparser.add_argument('height', type=int, required=True)
qrparser.add_argument('width', type=int, required=True)




