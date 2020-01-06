import yaml
import os

def load_manifest():
    manifest_content = yaml.load(os.getenv('manifest'))
    return manifest_content

def load_requirements():
    requirements_content = os.getenv('requirements')
    requirements = requirements_content.split('\n')
    return requirements

def load_installer():
    installer_content = yaml.load(os.getenv('installer'))
    return installer_content

if __name__ == "__main__":
    manifest = load_manifest()
    print(manifest)

    requirements = load_requirements()
    print(requirements)

    installer = load_installer()
    print(installer)