import requests
import json
from typing import Optional, Dict, Any

class PyLibsMetaSearch:
    """Simple library to search pylibsmeta data from raw GitHub"""
    
    BASE_URL = "https://raw.githubusercontent.com/tushkum34-cloud/pylibsmeta/main/lib_db"
    
    @staticmethod
    def encode_version(version: str) -> str:
        """
        Encode version string to pylibsmeta format
        Examples:
            "2.31.0" → "v0002003100000"
            "1.0" → "v0001000000000"
            "3" → "v0003000000000"
        """
        parts = version.split(".")
        parts += ["0"] * (3 - len(parts))
        parts = [p.zfill(4) for p in parts[:3]]
        return "v" + "".join(parts)
    
    @staticmethod
    def get_latest_version(package_name: str) -> str:
        """
        Fetch latest version of a package from PyPI and return it.

        Raises:
            ValueError: if package not found on PyPI
        """
        url = f"https://pypi.org/pypi/{package_name}/json"

        res = requests.get(url)
        if res.status_code != 200:
            raise ValueError(f"Library '{package_name}' not found on PyPI")

        data = res.json()
        version = data["info"]["version"]
        return version
    
    @staticmethod
    def search(library_name: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Search for a library in pylibsmeta database
        
        Args:
            library_name: Name of the library (e.g., 'requests', 'numpy')
            version: Optional version (e.g., '2.31.0'). If not provided, searches latest
        
        Returns:
            Dictionary with library metadata, or None if not found
        """
        
        if not library_name or not isinstance(library_name, str):
            raise ValueError("Library name must be a non-empty string")
        
        # Format library name (lowercase, replace spaces/dashes)
        lib_name = library_name.lower().replace(' ', '_').replace('-', '_')
        
        # Build filename
        if version:
            encoded_version = PyLibsMetaSearch.encode_version(version)
            filename = f"{lib_name}_{encoded_version}.json"
        else:
            # Search for latest version
            filename = f"{lib_name}_{PyLibsMetaSearch.encode_version(PyLibsMetaSearch.get_latest_version(library_name))}.json"
        
        # Build raw GitHub URL
        url = f"{PyLibsMetaSearch.BASE_URL}/{filename}"
        
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                metadata = response.json()
                return {
                    'library': library_name,
                    'version': version or 'unknown',
                    'filename': filename,
                    'metadata': metadata,
                    'status': 'found'
                }
            elif response.status_code == 404:
                return {
                    'library': library_name,
                    'version': version or 'latest',
                    'status': 'not_found',
                    'url': url
                }
            else:
                return {
                    'library': library_name,
                    'status': 'error',
                    'error': f"HTTP {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'library': library_name,
                'status': 'error',
                'error': 'Request timeout'
            }
        except requests.exceptions.RequestException as e:
            return {
                'library': library_name,
                'status': 'error',
                'error': str(e)
            }
    
    @staticmethod
    def get_symbols(library_name: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get just the symbols/metadata for a library"""
        result = PyLibsMetaSearch.search(library_name, version)
        
        if result and result.get('status') == 'found':
            return result['metadata']
        return None
    
    @staticmethod
    def get_functions(library_name: str, version: Optional[str] = None) -> Optional[list]:
        """Get list of all functions in a library"""
        metadata = PyLibsMetaSearch.get_symbols(library_name, version)
        
        if not metadata:
            return None
        
        functions = []
        for key, value in metadata.items():
            # If value is a list, it's a function signature
            if isinstance(value, list):
                functions.append({
                    'name': key,
                    'params': value
                })
        
        return functions
    
    @staticmethod
    def get_classes(library_name: str, version: Optional[str] = None) -> Optional[Dict[str, Dict]]:
        """Get all classes and their methods"""
        metadata = PyLibsMetaSearch.get_symbols(library_name, version)
        
        if not metadata:
            return None
        
        classes = {}
        for key, value in metadata.items():
            # If value is a dict, it's a class with methods
            if isinstance(value, dict):
                classes[key] = value
        
        return classes


# Example usage
if __name__ == "__main__":
    # Test version encoding
    print("Version encoding tests:")
    print(f"'2.31.0' → {PyLibsMetaSearch.encode_version('2.31.0')}")
    print(f"'1.0' → {PyLibsMetaSearch.encode_version('1.0')}")
    print(f"'3' → {PyLibsMetaSearch.encode_version('3')}")
    print()
    
    # Search for requests library
    result = PyLibsMetaSearch.search("requests")
    print("Search Result:", json.dumps(result, indent=2))
    
    # Get functions
    functions = PyLibsMetaSearch.get_functions("requests")
    print("\nFunctions:", functions[:3] if functions else None)
    
    # Get classes
    classes = PyLibsMetaSearch.get_classes("requests")
    print("\nClasses:", list(classes.keys())[:3] if classes else None)