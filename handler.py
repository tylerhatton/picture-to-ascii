from PIL import Image
import urllib.request
import json

# ascii characters used to build the output text
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


# verify image file has jpg, jpeg, or png extension
def verify_image_file(url):
    image_extensions = [".jpg", ".jpeg", ".png"]
    for extension in image_extensions:
        if url.endswith(extension):
            return(True)
    return(False)


# resize image according to a new width
def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height/width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return(resized_image)


# convert each pixel to grayscale
def grayify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)


# convert pixels to a string of ascii characters
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)


# GET request function
def get(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Lambda"})
    }


# POST request function
def post(event, context):
    new_width = 100
    download_path = "/tmp/image"
    url = json.loads(event['body'])['url']

    # verify image file has jpg, jpeg, or png extension
    if verify_image_file(url):
        urllib.request.urlretrieve(url, download_path)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps("Invalid image file")
        }

    # attempt to open image
    try:
        image = Image.open(download_path)
    except:
        return {
            "statusCode": 400,
            "body": json.dumps("Invalid image file")
        }

    # convert image to ascii
    new_image_data = pixels_to_ascii(grayify(resize_image(image, new_width)))

    # format
    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[index:(index+new_width)]
                             for index in range(0, pixel_count, new_width)])

    # return result
    response_body = ascii_image
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html',
        },
        "body": response_body
    }
