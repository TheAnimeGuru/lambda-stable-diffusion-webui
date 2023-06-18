import subprocess
import os

# Function to download using wget
def download_with_wget(url, download_directory, logging, file_name=None):
    # Use the provided file_name or extract filename from URL
    if file_name is None:
        file_name = url.split('/')[-1]
    
    # Check if the file already exists
    if os.path.exists(os.path.join(download_directory, file_name)):
        logging.info(f'[INFO] File {file_name} already exists in {download_directory}. Skipping download.')
        return
    
    # Download using wget if file does not exist
    try:
        subprocess.run(['wget', url, '-O', os.path.join(download_directory, file_name)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f'[INFO] Successfully downloaded {url} to {download_directory} as {file_name} using wget.')
    except subprocess.CalledProcessError as e:
        logging.error(f'[ERROR] Failed to download {url} to {download_directory} as {file_name} using wget. Error: {e.stderr}')

# Function to clone using git
def clone_with_git(url: str, download_directory: str, logging) -> None:
    try:
        subprocess.run(['git', 'clone', url, download_directory], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f'[INFO] Successfully cloned {url} to {download_directory} using git.')
    except subprocess.CalledProcessError as e:
        logging.error(f'[ERROR] Failed to clone {url} to {download_directory} using git. Error: {e.stderr}')

def download_resources(resources: list, logging) -> None:
    # Download each resource using the specified method
    for resource in resources:
        url = resource['url']
        download_directory = resource['download_directory']
        method = resource.get('method', 'wget') # default to wget if method is not specified
        file_name = resource.get('file_name', None)
        
        # Create the download directory if it does not exist
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        # Download the resource using the specified method
        if method == 'wget':
            download_with_wget(url, download_directory, logging, file_name)
        elif method == 'git':
            clone_with_git(url, download_directory, logging)
        else:
            logging.error(f'[ERROR] Unknown method {method} for resource {url}')