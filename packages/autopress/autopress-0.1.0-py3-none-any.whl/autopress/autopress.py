from autopress.openai import generate
import re
from typing import Optional
from autopress.utils import convert_tag
import importlib
import clisync

class Autopress():
    """This class is used to generate docstrings from a method 
    signature or a class signature.  
    It is used as a singleton and it's methods are static.
    """

    @staticmethod
    @clisync.include()
    def from_file(file: str, 
                  output: str, 
                  replace: Optional[bool] = False, 
                  id: Optional[str] = None) -> str:
        """Open a markdown file and replace the tags with the generated docstring.

        The supported tags are:
            - <ClassAutopress/> with props:
                - module: the module name
                - cls: the class name
            - <MethodAutopress/> with props:
                - module: the module name
                - method: the method name

        Args:
            file (str): the input file
            output (str): the output file
            replace (bool): If True, the method will not replace the content already generated. Defaults to False.
            id (bool): If set, the method will only replace the tag with the given id. Defaults to None.

        Returns:
            str: the content of the file
        """
        select_id = id
        with open(file) as f:
            content = f.read()

        # Find all MethodAutopress tags and get what's inside
        method_tags = re.findall(r"<MethodAutopress.*?/>", content)
        for tag in method_tags:
            module = re.search(r"module=\"(.*?)\"", tag).group(1)
            method = re.search(r"method=\"(.*?)\"", tag).group(1)
            existing_id = re.search(r"id=\"(.*?)\"", tag)
            if replace and existing_id:
                continue
            if select_id and existing_id and existing_id.group(1) != select_id:
                continue
            docstring = Autopress.from_method(module, method)
            content = convert_tag(content, tag, docstring, existing_id)
          
        # Find all ClassAutopress tags and get what's inside
        class_tags = re.findall(r"<ClassAutopress.*?/>-", content)
        for tag in class_tags:
            module = re.search(r"module=\"(.*?)\"", tag).group(1)
            cls = re.search(r"cls=\"(.*?)\"", tag).group(1)
            existing_id = re.search(r"id=\"(.*?)\"", tag)
            if replace and existing_id:
                continue
            if select_id and existing_id and existing_id.group(1) != select_id:
                continue
            docstring = Autopress.from_class(module, cls)
            content = convert_tag(content, tag, docstring, existing_id)

        # Write the content to the output file
        with open(output, "w") as f:
            f.write(content)
        return content
    
    @staticmethod
    @clisync.include()
    def from_docstring(docstring: str) -> str:
        """Use this method to generate a docstring from a string.
        We do not recommend using this method directly. Other method
        are more robust and handle more functionalities.

        Args:
            docstring (str): the docstring
        
        Returns:
            str: the generated docstring
        """
        return generate(docstring)
    
    @staticmethod
    @clisync.include()
    def from_method(module: str, method: str) -> str:
        """Use this method to generate a docstring from a method signature.

        Usage:
            module = 'torch.nn.functional'
            method = 'relu'
            docstring = Generate.from_method(module, method)
        
        Args:
            module (str): the module name
            method (str): the method signature 

        Returns:
            str: the generated docstring
        """
        # Load the method and get the __doc__ attribute
        module = importlib.import_module(module)
        while "." in method:
            module = getattr(module, method.split(".")[0])
            method = method.split(".")[1]
        method_name = method
        method = getattr(module, method)
        if callable(method):
            header = f"\n### `{module.__name__}.{method_name}`\n"
            prompt = Autopress._get_prompt(method)
            result = header + generate(prompt) + "\n"
        return result
    
    @staticmethod
    @clisync.include()
    def from_class(module: str, cls: str) -> str:
        """Use this method to generate a docstring from a class signature.

        Usage:
            module = 'torch.nn'
            cls = 'Linear'
            docstring = Generate.from_class(module, cls)

        Args:
            module (str): the module name
            cls (str): the class signature 

        Returns:
            str: the generated docstring
        """
        # Load the class and get the
        module = importlib.import_module(module)
        cls = getattr(module, cls)
        # For each method in the class, generate the docstring
        result = f"# {cls.__name__}\n"
        for method in dir(cls):
            if method.startswith("__"):
                continue
            if method.__doc__ is None:
                continue
            method = getattr(cls, method)
            if callable(method):
                header = f"\n## `{cls.__name__}.{method.__name__}`\n"
                prompt = Autopress._get_prompt(method)
                result += header + generate(prompt) + "\n"
        return result
    
    @staticmethod
    def _get_prompt(method: callable):
        return f"__annotations__: {method.__annotations__}\n__doc__:{method.__doc__}"
