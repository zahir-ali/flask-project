# from flask import Flask, request, render_template, send_file
# import pandas as pd
# import os
# import qrcode

# app = Flask(__name__)
# UPLOAD_FOLDER = "uploads"
# QR_FOLDER = "uploads/qrcodes"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(QR_FOLDER, exist_ok=True)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     file = request.files["file"]
#     if file:
#         filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(filepath)

#         # file extension check
#         ext = os.path.splitext(file.filename)[1].lower()

#         if ext == ".csv":
#             df = pd.read_csv(filepath)
#         elif ext == ".xlsx":
#             df = pd.read_excel(filepath, engine="openpyxl")
#         elif ext == ".xls":
#             df = pd.read_excel(filepath, engine="xlrd")
#         else:
#             return "Invalid file format. Please upload .csv, .xls, or .xlsx file."

#         # Purane QR codes delete kar do
#         for f in os.listdir(QR_FOLDER):
#             os.remove(os.path.join(QR_FOLDER, f))

#         # Har row ka QR code banao
#         img_tags = ""
#         for i, row in df.iterrows():
#             row_data = row.to_string(index=False)   # Row ko text me convert
#             qr = qrcode.make(row_data)
#             qr_path = os.path.join(QR_FOLDER, f"qr_{i+1}.png")
#             qr.save(qr_path)
#             img_tags += f"<p>Row {i+1}</p><img src='/qrcode/{i+1}' alt='QR Code Row {i+1}'><br><br>"

#         return f"""
#         <h3>QR Codes Generated ({len(df)} rows)</h3>
#         {img_tags}
#         """

#     return "No file uploaded"

# @app.route("/qrcode/<int:row_id>")
# def serve_qrcode(row_id):
#     qr_path = os.path.join(QR_FOLDER, f"qr_{row_id}.png")
#     if os.path.exists(qr_path):
#         return send_file(qr_path, mimetype="image/png")
#     return "QR code not found", 404

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, render_template
import pandas as pd
import qrcode
import io
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        df = pd.read_csv(file)  # CSV read karna

        qr_codes = []
        for _, row in df.iterrows():
            data = str(row.to_dict())  # har row ko dict -> string
            qr = qrcode.make(data)

            # memory buffer me save
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

            qr_codes.append(img_str)

        return render_template("index.html", qr_codes=qr_codes)

    return "No file uploaded"

if __name__ == "__main__":
    app.run(debug=True)
