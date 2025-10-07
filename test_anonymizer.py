#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the Enhanced Anonymizer
"""

import tempfile
from pathlib import Path
from anonymizer_enhanced import EnhancedAnonymizer, AnonymizationLevel, DocumentProcessor

def test_basic_anonymization():
    """Test basic anonymization functionality"""
    print("Testing basic anonymization...")
    
    # Create test anonymizer
    anonymizer = EnhancedAnonymizer(AnonymizationLevel.STANDARD)
    
    # Test text with various sensitive data
    test_text = """
    Jmenuji se Jan Novák a narodil jsem se 15.3.1985.
    Můj rodné číslo je 850315/1234 a bydlím na Václavské náměstí 1, 110 00 Praha.
    Můj telefon je +420 123 456 789 a email jan.novak@email.cz.
    Můj bankovní účet je 123456-7890123456/0100.
    """
    
    print("Original text:")
    print(test_text)
    print("\n" + "="*50 + "\n")
    
    # Anonymize
    anonymized = anonymizer.anonymize_text(test_text)
    
    print("Anonymized text:")
    print(anonymized)
    print("\n" + "="*50 + "\n")
    
    # Show statistics
    stats = anonymizer.get_statistics()
    print("Statistics:")
    for category, count in stats.items():
        print(f"  {category}: {count}")
    
    print("\n" + "="*50 + "\n")
    
    # Show replacements
    print("Replacements:")
    for tag, values in anonymizer.replacements.items():
        print(f"  {tag}: {values}")
    
    return anonymized, stats

def test_document_processing():
    """Test document processing with temporary files"""
    print("\nTesting document processing...")
    
    # Create test text file
    test_content = """
    Smlouva o pracovním poměru
    
    Zaměstnanec: Marie Svobodová
    Datum narození: 22.7.1990
    Rodné číslo: 900722/1234
    Adresa: Hlavní 123, 602 00 Brno
    Telefon: +420 987 654 321
    Email: marie.svobodova@firma.cz
    
    Zaměstnavatel: ABC s.r.o.
    IČO: 12345678
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        input_path = Path(f.name)
    
    try:
        # Process document
        anonymizer = EnhancedAnonymizer(AnonymizationLevel.STANDARD)
        processor = DocumentProcessor(anonymizer)
        
        output_path = input_path.parent / f"{input_path.stem}_anonymized{input_path.suffix}"
        result = processor.process_text(input_path, output_path)
        
        print(f"Processed document saved to: {output_path}")
        print(f"Processing time: {result.processing_time:.2f} seconds")
        print(f"Statistics: {result.statistics}")
        
        # Read and display anonymized content
        with open(output_path, 'r', encoding='utf-8') as f:
            anonymized_content = f.read()
        
        print("\nAnonymized content:")
        print(anonymized_content)
        
        return result
        
    finally:
        # Cleanup
        input_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)

def test_different_levels():
    """Test different anonymization levels"""
    print("\nTesting different anonymization levels...")
    
    test_text = "Jan Novák má telefon 123 456 789 a bydlí na Václavské 1, Praha."
    
    for level in AnonymizationLevel:
        print(f"\nLevel: {level.value}")
        anonymizer = EnhancedAnonymizer(level)
        anonymized = anonymizer.anonymize_text(test_text)
        stats = anonymizer.get_statistics()
        
        print(f"Original: {test_text}")
        print(f"Anonymized: {anonymized}")
        print(f"Statistics: {stats}")

if __name__ == "__main__":
    print("Enhanced Anonymizer Test Suite")
    print("=" * 50)
    
    try:
        # Run tests
        test_basic_anonymization()
        test_document_processing()
        test_different_levels()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()