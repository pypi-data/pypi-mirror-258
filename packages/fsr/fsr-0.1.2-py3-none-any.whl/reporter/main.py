import argparse
import json
import os
import shutil
from server import start_server

def main():
    parser = argparse.ArgumentParser(description="Utility for generating and serving test reports.")
    parser.add_argument("command", choices=["generate", "serve"], help="Command to run.")
    parser.add_argument("file_path", help="Path to the report.json file.")
    args = parser.parse_args()

    if args.command == "generate":
        generate_report(args.file_path)
    elif args.command == "serve":
        generate_report(args.file_path)
        start_server('test_report')

def generate_report(file_path):
    report_dir = os.path.join(os.getcwd(), 'test_report')
    source_dir = os.path.join(os.getcwd(), 'report_web')
    files_to_copy = ['app.js', 'style.css', 'index.html']
    data_dir = os.path.join(report_dir, 'data')

    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)
    os.makedirs(data_dir, exist_ok=True)

    goldens_dir = os.path.join(data_dir, 'goldens')
    failures_dir = os.path.join(data_dir, 'failures')
    os.makedirs(goldens_dir, exist_ok=True)
    os.makedirs(failures_dir, exist_ok=True)

    process_file_to_json(file_path, os.path.join(data_dir, 'data.json'), os.getcwd())

    for file_name in files_to_copy:
        source_file_path = os.path.join(source_dir, file_name)
        destination_file_path = os.path.join(report_dir, file_name)
        shutil.copy(source_file_path, destination_file_path)

def find_images(test_name, base_dir, type):
    target_dir = os.path.join(os.getcwd(), 'test_report', 'data', type)
    images = []
    for root, dirs, files in os.walk(base_dir):
        if type in root.split(os.sep):
            for file in files:
                if file.startswith(test_name) and file.endswith('.png'):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(target_dir, file)
                    if source_path != destination_path:
                        shutil.copy(source_path, destination_path)
                        relative_path = os.path.relpath(destination_path, os.path.join(os.getcwd(), 'test_report'))
                        images.append(relative_path)
    return images

def process_file_to_json(file_path, output_json_path, base_dir):
    encodings = ['utf-8', 'utf-16', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        else:
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
                    test_results.append({
                        'id': test_id,
                        'name': test_name,
                        'result': None,
                        'messages': [],
                        'images': {
                            'goldens': find_images(test_name, base_dir, 'goldens'),
                            'failures': find_images(test_name, base_dir, 'failures')
                        }
                    })
                elif test_info:
                    if test_result:
                        test_info['result'] = test_result
                    test_info['messages'].extend(messages)
        except json.JSONDecodeError:
            continue

    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(test_results, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
