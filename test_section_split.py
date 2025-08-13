#!/usr/bin/env python3
"""
Test script for the HTML section splitting functionality using SplitHTML class.
"""

import os
import yaml
from src.usdm4_legacy.import_.split_html import SplitHTML
from simple_error_log.errors import Errors

def load_html_file(filename):
    """Load HTML content from a file in the protocols directory."""
    filepath = os.path.join("protocols/cleaned", filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def save_sections_to_yaml(sections, output_filename):
    """Save sections to a YAML file."""
    try:
        # Create the protocols/sections directory if it doesn't exist
        os.makedirs("protocols/sections", exist_ok=True)
        
        output_path = os.path.join("protocols/sections", output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            yaml.dump(sections, file, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"Sections saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving sections to YAML: {e}")
        return False

def test_file(filename):
    """Test section splitting on a specific HTML file."""
    print(f"\n{'='*60}")
    print(f"TESTING FILE: {filename}")
    print('='*60)
    
    html_content = load_html_file(filename)
    if html_content is None:
        return
    
    print("Original HTML length:", len(html_content))
    
    # Initialize error handling
    errors = Errors()
    
    # Use SplitHTML class to split document into sections
    splitter = SplitHTML(html_content, errors)
    sections = splitter.execute()
    
    if sections is None:
        print("Error: SplitHTML.execute() returned None")
        if errors.has_errors():
            print("Errors encountered:")
            for error in errors.get_errors():
                print(f"- {error}")
        return
    
    print(f"\nSECTION SPLITTING RESULTS:")
    print(f"Number of sections found: {len(sections)}")
    
    if sections:
        print("\nSection Summary:")
        print("-" * 40)
        for i, section in enumerate(sections[:10]):  # Show first 10 sections
            content_length = len(section['html_content'])
            print(f"{i+1:2d}. Section {section['section_number']}: {section['section_title'][:50]}{'...' if len(section['section_title']) > 50 else ''}")
            print(f"    Content length: {content_length} characters")
        
        if len(sections) > 10:
            print(f"    ... and {len(sections) - 10} more sections")
        
        # Show a sample section in detail
        if sections:
            print(f"\nSAMPLE SECTION DETAIL (Section {sections[0]['section_number']}):")
            print("-" * 40)
            print(f"Number: {sections[0]['section_number']}")
            print(f"Title: {sections[0]['section_title']}")
            print(f"Content preview: {sections[0]['html_content'][:200]}{'...' if len(sections[0]['html_content']) > 200 else ''}")
    
    # Save sections to YAML file
    base_filename = os.path.splitext(filename)[0]
    yaml_filename = f"{base_filename}_sections.yaml"
    
    if save_sections_to_yaml(sections, yaml_filename):
        print(f"\nSections successfully saved to protocols/sections/{yaml_filename}")
    
    print("\nSection splitting completed successfully!")

def test_simple_cases():
    """Test with simple HTML cases to verify the section splitting logic."""
    print("\n" + "="*60)
    print("TESTING SIMPLE SECTION SPLITTING CASES")
    print("="*60)
    
    test_cases = [
        {
            "name": "Basic sections with numbers",
            "html": '''<html><body>
                <h2>1. Introduction</h2>
                <p>This is the introduction content.</p>
                <h2>2. Methods</h2>
                <p>This is the methods content.</p>
                <h3>2.1. Study Design</h3>
                <p>Study design details.</p>
                </body></html>'''
        },
        {
            "name": "Sections with subsections",
            "html": '''<html><body>
                <h1>1. Background</h1>
                <p>Background information.</p>
                <h2>1.1. Rationale</h2>
                <p>Rationale content.</p>
                <h2>1.2. Objectives</h2>
                <p>Objectives content.</p>
                <h1>2. Study Design</h1>
                <p>Study design content.</p>
                </body></html>'''
        },
        {
            "name": "Document with pre-section content",
            "html": '''<html><body>
                <h1>Document Title</h1>
                <p>This is some introductory content before any numbered sections.</p>
                <h2>Protocol Information</h2>
                <p>More pre-section content here.</p>
                <h2>1. Introduction</h2>
                <p>This is the first numbered section.</p>
                <h2>2. Methods</h2>
                <p>This is the second numbered section.</p>
                </body></html>'''
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("-" * 40)
        
        errors = Errors()
        splitter = SplitHTML(test_case['html'], errors)
        sections = splitter.execute()
        
        if sections:
            print(f"Found {len(sections)} sections:")
            for section in sections:
                print(f"  - Section {section['section_number']}: {section['section_title']}")
                print(f"    Content: {section['html_content'][:100]}{'...' if len(section['html_content']) > 100 else ''}")
        else:
            print("No sections found")
        
        print("Test completed successfully!")

def main():
    # Test with available HTML files from protocols directory
    html_files = [
        "EliLilly_NCT03421379_Diabetes.html",
        "EliLilly_NCT04184622_Diabetes.html", 
        "AZ_NCT03402841_Oncology.html",
        "BMS_NCT04730349_Oncology.html",
        "Roche_NCT02291289_Oncology.html"
    ]
    
    print("HTML Section Splitting Test")
    print("Testing with real protocol files from protocols directory")
    print("Using SplitHTML class methods")
    print("Results will be saved as YAML files in protocols/sections/")
    
    for filename in html_files:
        test_file(filename)
    
    # Test simple cases
    test_simple_cases()

if __name__ == "__main__":
    main()
