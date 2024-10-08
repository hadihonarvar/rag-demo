#store image in s3
import boto3
from botocore.exceptions import NoCredentialsError

def upload_file_to_s3(file_name, bucket, object_name=None, region='us-east-1'):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Initialize a session using Amazon S3
    s3_client = boto3.client('s3')

    try:
        # Upload the file to S3
        s3_client.upload_file(file_name, bucket, object_name)

        # Generate the S3 file URL
        url = f"https://{bucket}.s3.{region}.amazonaws.com/{object_name}"
        print(f"File {file_name} uploaded to S3 bucket {bucket} as {object_name}.")
        print(f"File URL: {url}")

        return url
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return None
    except NoCredentialsError:
        print("Credentials not available.")
        return None

# Example usage:
# url = upload_file_to_s3('path/to/file.txt', 'your-bucket-name', 'optional/s3/key/file.txt')
# print(url)
def upload_image_to_s3(image_url, bucket_name):
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        image_data = response.content

        filename = image_url

        # Upload the image data to your S3 bucket
        s3.put_object(Body=image_data, Bucket=bucket_name, Key=filename)

        return f"Image {image_url} uploaded to S3 successfully"

    except NoCredentialsError:
        return "Credentials not found or invalid"