import yaml
import os

def load_yaml_documents(file_path):
    with open(file_path, 'r') as file:
        return list(yaml.safe_load_all(file))

def categorize_yaml_by_kind(docs):
    categorized_resources = {}
    for doc in docs:
        if 'kind' in doc:
            kind = doc['kind']
            if kind not in categorized_resources:
                categorized_resources[kind] = []
            categorized_resources[kind].append(doc)
    return categorized_resources

def create_directories(base_dir, resource_types):
    os.makedirs(base_dir, exist_ok=True)
    folder_paths = {}
    for resource_type in resource_types:
        folder_path = os.path.join(base_dir, resource_type)
        os.makedirs(folder_path, exist_ok=True)
        folder_paths[resource_type] = folder_path
    return folder_paths

def save_resources_to_files(folder_paths, categorized_resources):
    for resource_type, resources in categorized_resources.items():
        for index, resource in enumerate(resources):
            file_name = f"{resource.get('metadata', {}).get('name', 'resource')}_{index+1}.yaml"
            file_path = os.path.join(folder_paths[resource_type], file_name)
            with open(file_path, 'w') as outfile:
                yaml.dump(resource, outfile)

def split_and_save_yaml(file_path):
    docs = load_yaml_documents(file_path)
    categorized_resources = categorize_yaml_by_kind(docs)
    base_dir = f"{os.getcwd()}/split_yaml/"
    folder_paths = create_directories(base_dir, categorized_resources.keys())
    save_resources_to_files(folder_paths, categorized_resources)
    print(folder_paths)


if __name__ == "__main__":
    yml_file_path = 'opentelemetry-demo.yaml'
    split_and_save_yaml(yml_file_path)
