from PIL import Image

im = Image.open('test.webp').convert('RGB')
im.save('test.jpg', 'jpeg')