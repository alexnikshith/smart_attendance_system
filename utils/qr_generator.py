# import qrcode
# from datetime import datetime

# def generate_qr(session_name):
#     data = f"{session_name}|{datetime.now()}"
#     img = qrcode.make(data)
#     img.save("static/qr.png")




# import qrcode
# import json

# def generate_qr(session_id):
#     data = json.dumps({
#         "session_id": session_id
#     })

#     img = qrcode.make(data)
#     img.save("static/qr.png")


import qrcode
import json
import os

def generate_qr(session_id):
    data = json.dumps({"session_id": session_id})

    img = qrcode.make(data)

    # Ensure static folder exists
    if not os.path.exists("static"):
        os.makedirs("static")

    img.save("static/qr.png")
