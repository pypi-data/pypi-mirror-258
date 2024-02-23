class XML:
    def __init__(self, xml_file: str) -> None:
        from importlib import metadata as pypi
        import xml.etree.ElementTree as ET
        import subprocess
        import requests
        import logging
        self.xml = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        try:
            user_ver = str(pypi.version('hxml'))
            pypi_ver = str(requests.get("https://pypi.org/pypi/hxml/json").json()['info']['version'])
            if not user_ver == pypi_ver:
                subprocess.run(['pip', 'install', f'hxml=={pypi_ver}'])
            else:
                pass
        except pypi.PackageNotFoundError as e:
            logging.error(f"Package hxml not found: {e}")
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve version from PyPI for hxml: {e}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install hxml package: {e}")

    def get_root_item(self, item: str):
        import hollos_get_data_recursive
        root_element_name = self.root.tag
        if item != root_element_name:
            print(f"Error: Provided item '{item}' does not match root element '{root_element_name}'.")
            return None
        
        data = {}
        for child in self.root:
            data[child.tag] = hollos_get_data_recursive.init()._get_data_recursive(child)
        
        return data