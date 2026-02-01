# ============================================
# FILE: parsers/base_parser.py
# PURPOSE: Abstract base class for all language parsers
# ============================================

from abc import ABC, abstractmethod

class BaseParser(ABC):
    """Interface that all language parsers must implement"""
    
    @abstractmethod
    def parse(self, code):
        """
        Parse code and extract functions/methods.
        
        Args:
            code (str): Source code to parse
            
        Returns:
            list: List of function dictionaries containing:
                - name: Function name
                - args: List of arguments
                - return_type: Return type (if available)
                - body: Function body code
                - line: Starting line number
                - calls: List of functions called by this function
        """
        pass
    
    @abstractmethod
    def get_dependencies(self, code):
        """
        Extract external dependencies/imports.
        
        Args:
            code (str): Source code
            
        Returns:
            list: List of dependency names
        """
        pass
