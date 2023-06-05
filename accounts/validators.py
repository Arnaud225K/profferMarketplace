from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] # profile_image.jpg jpg is [1]
    #print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Недопустимое расширение файла. Допустимые расширения:' +str(valid_extensions))