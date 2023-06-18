import os
import subprocess
import yaml
import logging
import datetime
from helpers.download_utils import download_resources

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, f'{datetime.datetime.now().strftime("%Y_%m_%d")}.log'),
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load configuration from YAML file
try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except Exception as e:
    logging.error(f'[ERROR] Failed to load config.yml. Trace: {e}')
    exit(1)

# Get resources from config
resources = config.get('resources', [])

# Download resources from config.yaml
download_resources(resources, logging)

# Rsync files from includes folder
try:
    result = subprocess.run(['rsync', '-avzPh', '/home/demo/source/includes/', '/home/demo/source/stable-diffusion-webui/'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    logging.info(f'[INFO] Successfully rsynced includes folder. Output: {result.stdout}')
except subprocess.CalledProcessError as e:
    logging.error(f'[ERROR] Failed to rsync includes folder. Error: {e.stderr}')

# Launch App
try:
    logging.info(f'[INFO] Starting WebUI')
    os.chdir("/home/demo/source/stable-diffusion-webui")
    os.system("python launch.py --port 8266 --listen --cors-allow-origins=* --xformers --enable-insecure-extension-access --theme dark --gradio-queue --disable-safe-unpickle")
except Exception as e:
    logging.error(f'[ERROR] Failed to start WebUI. Error: {e}')
