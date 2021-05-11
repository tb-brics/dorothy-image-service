from image_service.models import Image, ImageSampling
import os

def run():

    sample =[]
    with open('/sampling_images.txt', 'r') as f:
        for image in f:
            sample.append((os.path.splitext(image)[0]).strip())

    china_images_ids = []
    for image in Image.objects.all().filter(dataset__name='china'):
        china_images_ids.append(image.project_id)

    index = 0
    for image in sample:
        index+=1
        img_id = [s for s in china_images_ids if image in s][0]
        image_sampling__obj = ImageSampling(image=Image.objects.filter(project_id=img_id)[0], insertion_date='2021-03-30', rank_position=index)
        image_sampling__obj.save()

    print(f'Added {index} images to sampling')
