
# ECR Untagged Image Manager

The ecr_untagged_manager.py script is designed to help manage untagged images in an AWS Elastic Container Registry (ECR) repository. It lists all untagged images within a specified repository and can optionally delete them, supporting a dry run mode for safety.

### Features

<b>List Untagged Images</b>: Retrieves all untagged images from the specified ECR repository.
<b>Delete Untagged Images</b>: Deletes the retrieved untagged images in batches.
<b>Dry Run Mode</b>: Simulates the deletion process without actually removing images, allowing for safe testing.

### Prerequisites

Before you start, ensure you have the following:

- Python 3.x installed.
- AWS CLI configured with appropriate credentials and permissions.
- Boto3 installed. You can install it using pip install boto3.

### Usage

<b>List Untagged Images and Write to File</b>:
Simply run the script with the repository name to list untagged images. This will also write the image digests to untagged.json.
```
python ecr_untagged_manager.py -r <repository-name>
```

<b>Delete Untagged Images</b>:
Run the script without the dry run flag to delete all untagged images in the specified repository.
```
python ecr_untagged_manager.py -r <repository-name> -d
```

### Important Notes

Use the delete mode (-d) to delete untagged images.
Ensure you have the necessary AWS permissions to list and delete images in ECR.
Always verify that it is safe to delete the untagged images, as this operation is irreversible.

### Contributing

Feel free to fork this project and submit pull requests with enhancements or fixes. For major changes, please open an issue first to discuss what you would like to change.
