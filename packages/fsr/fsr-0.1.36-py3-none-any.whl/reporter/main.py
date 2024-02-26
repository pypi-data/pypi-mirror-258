import argparse
import json
import os
import shutil
import logging
from .server import start_server

def configure_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=level, datefmt='%Y-%m-%d %H:%M:%S')

def main():
    parser = argparse.ArgumentParser(description="Utility for generating and serving test reports.")
    parser.add_argument("command", choices=["generate", "serve"], help="Command to run.")
    parser.add_argument("file_path", help="Path to the report.json file.")
    parser.add_argument("--test-type", "-t", choices=["default", "goldens"], default="default", help="Type of tests to run.")
    parser.add_argument("--image-folder", "-i", default="/test", help="Folder path for images.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging.")
    args = parser.parse_args()

    configure_logging(args.verbose)

    logging.debug("Starting with args: %s", args)

    if args.command == "generate":
        generate_report(args.file_path, args.test_type, args.image_folder)
    elif args.command == "serve":
        generate_report(args.file_path, args.test_type, args.image_folder)
        start_server('test_report')

def generate_report(file_path, test_type, image_folder):
    logging.info("Generating report for %s with test type %s and image folder %s", file_path, test_type, image_folder)
    package_dir = os.path.dirname(os.path.abspath(__file__))
    report_dir = os.path.join(os.getcwd(), 'test_report')
    source_dir = os.path.join(package_dir, 'report_web')
    files_to_copy = ['app.js', 'style.css', 'index.html']
    data_dir = os.path.join(report_dir, 'data')

    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)
        logging.debug("Existing report directory removed: %s", report_dir)
    os.makedirs(data_dir, exist_ok=True)
    logging.debug("Data directory created: %s", data_dir)

    if test_type == "goldens":
        goldens_dir = os.path.join(data_dir, 'goldens')
        failures_dir = os.path.join(data_dir, 'failures')
        os.makedirs(goldens_dir, exist_ok=True)
        os.makedirs(failures_dir, exist_ok=True)
        logging.debug("Goldens and failures directories created.")

    process_file_to_json(file_path, os.path.join(data_dir, 'data.json'), os.getcwd(), test_type, image_folder)

    for file_name in files_to_copy:
        source_file_path = os.path.join(source_dir, file_name)
        destination_file_path = os.path.join(report_dir, file_name)
        shutil.copy(source_file_path, destination_file_path)
        logging.debug("File copied: %s", file_name)

def find_images(test_name, base_dir, type, image_folder):
    logging.debug("Searching for images for test %s of type %s in %s", test_name, type, image_folder)
    target_dir = os.path.join(os.getcwd(), 'test_report', 'data', type)
    images = []
    for root, dirs, files in os.walk(base_dir):
        if type in root.split(os.sep) and root.startswith(image_folder):
            for file in files:
                if file.startswith(test_name) and file.endswith('.png'):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(target_dir, file)
                    if source_path != destination_path:
                        shutil.copy(source_path, destination_path)
                        relative_path = os.path.relpath(destination_path, os.path.join(os.getcwd(), 'test_report'))
                        images.append(relative_path)
                        logging.debug("Image found and copied: %s", file)
    if not images:
        logging.info("For test %s, images not found.", test_name)
    return images

def process_file_to_json(file_path, output_json_path, base_dir, test_type, image_folder):
    logging.debug("Processing file %s", file_path)
    encodings = ['utf-8', 'utf-16', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        else:
            logging.error("All encodings failed for %s", file_path)
            raise ValueError(f"All encodings failed for {file_path}")

    test_results = []
    for line in content:
        try:
            item = json.loads(line)
            if item['type'] in ['testStart', 'testDone', 'print']:
                test_name = item.get('test', {}).get('name', '')
                if any(skip_phrase in test_name for skip_phrase in ['tearDownAll', 'tearDown', 'setUpAll', 'setUp', 'loading']):
                    continue
                test_id = item.get('testID') or item.get('test', {}).get('id')
                test_result = item.get('result')
                messages = [item['message']] if 'message' in item else []

                test_info = next((test for test in test_results if test['id'] == test_id), None)
                if item['type'] == 'testStart':
                    images_info = {}
                    if test_type == "goldens":
                        images_info = {
                            'goldens': find_images(test_name, base_dir, 'goldens', image_folder),
                            'failures': find_images(test_name, base_dir, 'failures', image_folder)
                        }
                    test_results.append({
                        'id': test_id,
                        'name': test_name,
                        'result': None,
                        'messages': [],
                        'images': images_info
                    })
                    logging.debug("Test started: %s", test_name)
                elif test_info:
                    if test_result:
                        test_info['result'] = test_result
                    test_info['messages'].extend(messages)
                    logging.debug("Test done: %s", test_name)
        except json.JSONDecodeError:
            logging.warning("JSON decode error encountered. Skipping line.")
            continue

    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(test_results, file, ensure_ascii=False, indent=4)
        logging.info("Test report generated: %s", output_json_path)

if __name__ == "__main__":
    main()