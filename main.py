import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

qr_code_folder = "qr_codes"
certificate_folder = "certificates"

os.makedirs(qr_code_folder, exist_ok=True)
os.makedirs(certificate_folder, exist_ok=True)

def get_unique_filename(base_name, folder):
    count = 1
    filename = f"{base_name}.png"
    while os.path.exists(os.path.join(folder, filename)):
        filename = f"{base_name}_{count}.png"
        count += 1
    return filename

def generate_certificate(user_name, user_id):
    base_name = user_name.replace(" ", "_")
    output_certificate_png = os.path.join(certificate_folder, get_unique_filename(base_name, certificate_folder))
    qr_image_path = os.path.join(qr_code_folder, get_unique_filename(base_name, qr_code_folder))
    
    qr_data = f"Name: {user_name}, ID: {user_id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    qr_img.save(qr_image_path)
    
    certificate = Image.open("certificate_template.png")
    draw = ImageDraw.Draw(certificate)
    
    font_path = "anastasia_script.ttf"
    font_size = 180
    font = ImageFont.truetype(font_path, font_size)
    
    text_position = (840, 610)
    text_color = "#c69c46"
    draw.text(text_position, user_name, fill=text_color, font=font)
    
    qr_code_image = Image.open(qr_image_path).resize((200, 200))
    qr_code_position = (80, 1115)
    certificate.paste(qr_code_image, qr_code_position)
    
    certificate.save(output_certificate_png, "PNG")
    
    print(f"Certificate generated successfully: {output_certificate_png}")

def main():
    while True:
        user_name = input("Enter the user's name: ")
        user_id = input("Enter the user's ID: ")
        generate_certificate(user_name, user_id)
        another = input("Do you want to generate another certificate? (yes/no): ").strip().lower()
        if another != "yes":
            break

if __name__ == "__main__":
    main()
