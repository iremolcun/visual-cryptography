import numpy as np
from PIL import Image
import random

# 1. Giriş Görüntüsünü İşleme
def process_image(image_path):
    """
    Giriş görüntüsünü binary formata dönüştür.
    """
    image = Image.open(image_path).convert('L')  # Gri seviye formatına dönüştür
    threshold = 128  # Gri seviyesinin altındaki değerler siyah, üstündeki beyaz olacak
    binary_image = image.point(lambda p: 255 if p > threshold else 0)  # Binary hale getir

    # Binary görüntüyü kaydet
    binary_image_path = 'binary_image.png'
    binary_image.save(binary_image_path)
    print(f"Binary görüntü kaydedildi: {binary_image_path}")

    return binary_image

# 2. Özel XOR Fonksiyonu
def custom_xor(a, b):
    """
    Geliştirilmiş XOR işlemi:
    - 0 XOR 0 = 0
    - 0 XOR 1 = 1
    - 1 XOR 0 = 1
    - 1 XOR 1 = 1
    """
    return a | b  # Mantıken OR işlemi ile aynı

# 3. Pay Görüntülerini Oluşturma (Visual Cryptography)
def generate_shares(secret_image_path):
    """
    Gizli görüntüyü 3 paya böler ve payları kaydeder.
    """
    # Gizli görüntüyü aç (binary format)
    secret_image = Image.open(secret_image_path).convert('1')  # Binary format
    width, height = secret_image.size

    # Paylar için yeni boş görüntüler oluştur
    share1 = Image.new('1', (width, height))
    share2 = Image.new('1', (width, height))
    share3 = Image.new('1', (width, height))

    # Gizli görüntüdeki her piksel için payları oluştur
    for x in range(width):
        for y in range(height):
            pixel = secret_image.getpixel((x, y))  # Gizli görüntü pikseli
            random_bit1 = random.randint(0, 1)  # Rastgele bit 1
            random_bit2 = random.randint(0, 1)  # Rastgele bit 2

            if pixel == 0:  # Siyah piksel
                share1.putpixel((x, y), random_bit1)
                share2.putpixel((x, y), random_bit2)
                share3.putpixel((x, y), custom_xor(random_bit1, random_bit2))  # Geliştirilmiş XOR
            else:  # Beyaz piksel
                share1.putpixel((x, y), random_bit1)
                share2.putpixel((x, y), random_bit2)
                share3.putpixel((x, y), 1 - custom_xor(random_bit1, random_bit2))  # Ters XOR

    # Payları kaydet
    share1.save('share1.png')
    share2.save('share2.png')
    share3.save('share3.png')

    print("Paylar kaydedildi: share1.png, share2.png, share3.png")
    return 'share1.png', 'share2.png', 'share3.png'

# 4. Payları Birleştirme
def combine_shares(share_paths):
    """
    3 pay görüntüsünü birleştirerek gizli görüntüyü yeniden oluşturur.
    """
    shares = [Image.open(share_path).convert('1') for share_path in share_paths]
    width, height = shares[0].size

    # Birleştirilmiş görüntü
    combined_image = Image.new('1', (width, height))

    for x in range(width):
        for y in range(height):
            pixel_values = [share.getpixel((x, y)) for share in shares]
            combined_pixel = custom_xor(pixel_values[0], custom_xor(pixel_values[1], pixel_values[2]))
            combined_image.putpixel((x, y), combined_pixel)

    # Birleştirilmiş görüntüyü kaydet
    combined_image_path = 'combined_image.png'
    combined_image.save(combined_image_path)
    print(f"Birleştirilmiş görüntü kaydedildi: {combined_image_path}")

    return combined_image_path

# Kullanım
if __name__ == "__main__":
    # 1. Giriş görüntüsünü binary formata dönüştür
    binary_image = process_image('secret_image.png')

    # 2. Payları oluştur
    share1, share2, share3 = generate_shares('binary_image.png')

    # 3. Payları birleştir ve sonucu doğrula
    combined_image = combine_shares([share1, share2, share3])
