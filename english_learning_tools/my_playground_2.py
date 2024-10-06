import os

def list_directory_structure(root_dir):
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"{sub_indent}{file} (content):")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(content)
            else:
                print(f"{sub_indent}{file}")

# 使用範例：指定要遍歷的資料夾路徑
directory_to_traverse = r"D:\it_project\github_sync\Miscellaneous"
list_directory_structure(directory_to_traverse)
