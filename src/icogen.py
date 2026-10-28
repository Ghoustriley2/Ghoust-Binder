from PIL import Image

# Создаем новую картинку размером 64x64 пикселя, красного цвета (RGB: 255, 0, 0)
img = Image.new('RGB', (64, 64), color=(255, 0, 0))

# Сохраняем её в формате иконки
img.save('icon.ico', format='ICO')

print("Тестовый файл icon.ico успешно создан в этой папке!")