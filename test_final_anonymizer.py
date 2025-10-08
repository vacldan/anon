#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the Final Working Anonymizer
"""

import tempfile
from pathlib import Path
from anonymizer_final_working import WorkingAnonymizer, AnonymizationLevel, DocumentProcessor

def test_basic_functionality():
    """Test basic anonymization functionality"""
    print("🧪 Testování základní funkcionality...")
    
    # Create test anonymizer
    anonymizer = WorkingAnonymizer(AnonymizationLevel.STANDARD)
    
    # Test text with various sensitive data
    test_text = """
    Smlouva o pracovním poměru
    
    Zaměstnanec: Jan Novák
    Datum narození: 15.3.1985
    Rodné číslo: 850315/1234
    Adresa: Václavské náměstí 1, 110 00 Praha
    Telefon: +420 123 456 789
    Email: jan.novak@email.cz
    Bankovní účet: 123456-7890123456/0100
    
    Zaměstnavatel: ABC s.r.o.
    IČO: 12345678
    """
    
    print("📄 Původní text:")
    print(test_text)
    print("\n" + "="*60 + "\n")
    
    # Anonymize
    anonymized = anonymizer.anonymize_text(test_text)
    
    print("🔒 Anonymizovaný text:")
    print(anonymized)
    print("\n" + "="*60 + "\n")
    
    # Show statistics
    stats = anonymizer.get_statistics()
    print("📊 Statistiky:")
    for category, count in stats.items():
        print(f"  {category}: {count}")
    
    print("\n" + "="*60 + "\n")
    
    # Show replacements
    print("🗂️  Náhrady:")
    for tag, values in anonymizer.replacements.items():
        print(f"  {tag}: {values}")
    
    return anonymized, stats

def test_document_processing():
    """Test document processing with temporary files"""
    print("\n🧪 Testování zpracování dokumentů...")
    
    # Create test text file
    test_content = """
    SMLOUVA O PRACOVNÍM POMĚRU
    
    Zaměstnanec: Marie Svobodová
    Datum narození: 22.7.1990
    Rodné číslo: 900722/1234
    Adresa trvalého bydliště: Hlavní 123, 602 00 Brno
    Telefon: +420 987 654 321
    Email: marie.svobodova@firma.cz
    
    Zaměstnavatel: XYZ s.r.o.
    IČO: 87654321
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        input_path = Path(f.name)
    
    try:
        # Process document
        anonymizer = WorkingAnonymizer(AnonymizationLevel.STANDARD)
        processor = DocumentProcessor(anonymizer)
        
        output_path = input_path.parent / f"{input_path.stem}_anonymized{input_path.suffix}"
        result = processor.process_text(input_path, output_path)
        
        print(f"✅ Dokument zpracován a uložen do: {output_path}")
        print(f"⏱️  Čas zpracování: {result.processing_time:.2f} sekund")
        print(f"📊 Statistiky: {result.statistics}")
        
        # Read and display anonymized content
        with open(output_path, 'r', encoding='utf-8') as f:
            anonymized_content = f.read()
        
        print("\n📋 Anonymizovaný obsah:")
        print(anonymized_content)
        
        return result
        
    finally:
        # Cleanup
        input_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)

def test_different_levels():
    """Test different anonymization levels"""
    print("\n🧪 Testování různých úrovní anonymizace...")
    
    test_text = "Jan Novák má telefon 123 456 789 a bydlí na Václavské 1, Praha."
    
    for level in AnonymizationLevel:
        print(f"\n📊 Úroveň: {level.value}")
        anonymizer = WorkingAnonymizer(level)
        anonymized = anonymizer.anonymize_text(test_text)
        stats = anonymizer.get_statistics()
        
        print(f"Původní: {test_text}")
        print(f"Anonymizovaný: {anonymized}")
        print(f"Statistiky: {stats}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n🧪 Testování hraničních případů...")
    
    anonymizer = WorkingAnonymizer(AnonymizationLevel.STANDARD)
    
    # Test cases
    test_cases = [
        "",  # Empty string
        "   ",  # Whitespace only
        "Žádná citlivá data",  # No sensitive data
        "Jan Novák a Petr Svoboda",  # Multiple names
        "Telefon: 123 456 789, Email: test@email.cz",  # Multiple patterns
        "Zákon č. 89/2012 Sb.",  # Legal reference (should not be anonymized)
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{test_case}'")
        result = anonymizer.anonymize_text(test_case)
        stats = anonymizer.get_statistics()
        print(f"Výsledek: '{result}'")
        print(f"Statistiky: {stats}")

if __name__ == "__main__":
    print("🚀 Testovací sada pro Final Working Anonymizer")
    print("=" * 60)
    
    try:
        # Run tests
        test_basic_functionality()
        test_document_processing()
        test_different_levels()
        test_edge_cases()
        
        print("\n✅ Všechny testy dokončeny úspěšně!")
        print("🎯 Anonymizátor je připraven k použití!")
        
    except Exception as e:
        print(f"\n❌ Test selhal: {e}")
        import traceback
        traceback.print_exc()