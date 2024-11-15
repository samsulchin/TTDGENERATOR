from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

app = Flask(__name__)

# Jalur folder font
FONT_FOLDER = "static/fonts"

@app.route("/", methods=["GET", "POST"])
def index():
    signature_image = None
    if request.method == "POST":
        # Ambil teks dan font dari form
        name = request.form.get("name")
        font_choice = request.form.get("font")

        if name and font_choice:
            # Jalur ke file font yang dipilih
            font_path = os.path.join(FONT_FOLDER, font_choice)
            if not os.path.exists(font_path):
                print(f"Font file not found: {font_path}")
                return "Error: Font file not found."

            # Buat nama file unik untuk gambar
            output_filename = f"static/{uuid.uuid4().hex}.png"
            # Buat gambar tanda tangan
            create_signature(name, font_path, output_filename)
            signature_image = output_filename

    return render_template("index.html", signature_image=signature_image)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

def create_signature(text, font_path, output_path):
    # Tentukan ukuran gambar
    image_width = 800
    image_height = 200

    # Buat gambar kosong dengan latar belakang putih
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Muat font tulisan tangan
    font_size = 100
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error saat memuat font: {e}")
        return

    # Hitung ukuran teks menggunakan textbbox untuk versi baru Pillow
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Hitung posisi teks agar berada di tengah gambar
    position = ((image_width - text_width) // 2, (image_height - text_height) // 2)

    # Gambar teks di gambar
    draw.text(position, text, fill="black", font=font)

    # Simpan gambar sebagai PNG
    image.save(output_path)

if __name__ == "__main__":
    app.run(debug=True)
