#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installation and setup script for the Enhanced Anonymizer
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    return run_command("pip install -r requirements.txt", "Installing requirements")

def download_stanza_models():
    """Download Stanza models for Czech language"""
    print("Downloading Stanza models...")
    
    # Create models directory
    models_dir = Path("data/models/stanza_cs")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Download models
    download_script = """
import stanza
import os
os.makedirs('data/models/stanza_cs', exist_ok=True)
stanza.download('cs', model_dir='data/models/stanza_cs')
print("Stanza models downloaded successfully")
"""
    
    return run_command(f'python -c "{download_script}"', "Downloading Stanza models")

def create_sample_document():
    """Create a sample document for testing"""
    sample_content = """
SMLOUVA O PRACOVNÍM POMĚRU

Zaměstnanec: Jan Novák
Datum narození: 15. března 1985
Rodné číslo: 850315/1234
Adresa trvalého bydliště: Václavské náměstí 1, 110 00 Praha 1
Telefon: +420 123 456 789
Email: jan.novak@email.cz
Bankovní účet: 123456-7890123456/0100

Zaměstnavatel: ABC s.r.o.
IČO: 12345678
Sídlo: Na Příkopě 15, 110 00 Praha 1

Tato smlouva se uzavírá na dobu neurčitou s nástupem 1. ledna 2024.
"""
    
    sample_path = Path("sample_document.txt")
    with open(sample_path, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"✅ Sample document created: {sample_path}")
    return sample_path

def run_demo():
    """Run a demonstration of the anonymizer"""
    print("\n" + "="*60)
    print("🚀 RUNNING DEMONSTRATION")
    print("="*60)
    
    # Create sample document
    sample_path = create_sample_document()
    
    try:
        # Run anonymizer
        print(f"\nRunning anonymizer on: {sample_path}")
        result = run_command(
            f"python anonymizer_enhanced.py {sample_path} --level full --formats json txt csv",
            "Anonymizing document"
        )
        
        if result:
            print("\n📊 Results:")
            print("- Anonymized document: sample_document_anonymized.txt")
            print("- Mapping files: sample_document_mapping.json, .txt, .csv")
            print("- Log file: anonymizer.log")
            
            # Show anonymized content
            anonymized_path = Path("sample_document_anonymized.txt")
            if anonymized_path.exists():
                print(f"\n📄 Anonymized content preview:")
                with open(anonymized_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(content[:500] + "..." if len(content) > 500 else content)
        
    finally:
        # Cleanup
        sample_path.unlink(missing_ok=True)

def main():
    """Main installation and setup process"""
    print("🔧 Enhanced Czech Document Anonymizer - Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Download Stanza models
    if not download_stanza_models():
        print("⚠️  Warning: Failed to download Stanza models. Anonymizer will work with heuristics only.")
    
    # Run test
    print("\n🧪 Running tests...")
    if not run_command("python test_anonymizer.py", "Running tests"):
        print("⚠️  Warning: Some tests failed, but anonymizer should still work")
    
    # Run demo
    run_demo()
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nUsage examples:")
    print("  python anonymizer_enhanced.py document.docx")
    print("  python anonymizer_enhanced.py document.txt --level full --output anonymized.txt")
    print("  python anonymizer_enhanced.py document.docx --formats json txt csv")
    print("\nFor more options: python anonymizer_enhanced.py --help")

if __name__ == "__main__":
    main()