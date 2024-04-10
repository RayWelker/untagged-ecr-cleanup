import boto3
import json
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Manage untagged images in AWS ECR.')
parser.add_argument('-r', '--repository', type=str, required=True, help='The name of the ECR repository.')
parser.add_argument('-d', '--delete', action='store_true', help='Actually delete the images (default is dry run).')

args = parser.parse_args()

# Initialize the ECR client
session = boto3.Session()
ecr = session.client('ecr')

def list_untagged_images(repository_name):
    untagged_images = []

    # Paginate through list_images results
    paginator = ecr.get_paginator('list_images')
    page_iterator = paginator.paginate(repositoryName=repository_name, filter={'tagStatus': 'UNTAGGED'})

    for page in page_iterator:
        for image in page['imageIds']:
            if 'imageDigest' in image:
                untagged_images.append(image['imageDigest'])

    return untagged_images

def batch_delete_images(repository_name, digests, delete=False):
    if not delete:
        print("DRY RUN: The following images would be deleted (actual deletion not performed):")
        for digest in digests:
            print(f"Repository: {repository_name}, ImageDigest: {digest}")
    else:
        for i in range(0, len(digests), 100):
            chunk = digests[i:i+100]
            response = ecr.batch_delete_image(
                repositoryName=repository_name,
                imageIds=[{'imageDigest': digest} for digest in chunk]
            )
            print(response)

if __name__ == "__main__":
    # List untagged images
    untagged_images = list_untagged_images(args.repository)
    
    # Optionally write the image digests to a file for record-keeping
    with open('untagged.json', 'w') as file:
        json.dump(untagged_images, file)
    print(f"Untagged image digests have been written to untagged.json.")

    # Batch delete images with an option for dry run
    if untagged_images:
        batch_delete_images(args.repository, untagged_images, delete=args.delete)
        if not args.delete:
            print(f"DRY RUN: {len(untagged_images)} untagged images identified for deletion.")
        else:
            print(f"Deleted {len(untagged_images)} untagged images.")
    else:
        print("No untagged images to delete.")
