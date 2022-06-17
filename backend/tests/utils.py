from faker import Faker


fake = Faker()


def create_image(image_format: str = "jpeg"):
    filename = fake.file_name("image", image_format)
    data = fake.image(image_format=image_format)
    return filename, data, f"image/{image_format}"
