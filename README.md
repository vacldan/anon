# Enhanced Czech Document Anonymizer

A comprehensive anonymization system for Czech documents that detects and replaces sensitive personal data with anonymized markers while maintaining detailed mapping for potential de-anonymization.

## 🚀 Features

- **Advanced Name Detection**: Multiple strategies for detecting Czech first names and surnames
- **Comprehensive Pattern Matching**: Detects various types of sensitive data including:
  - Birth dates and birth numbers (RČ)
  - ID card numbers
  - Bank account numbers and IBAN
  - Phone numbers and email addresses
  - Addresses and license plates
  - VIN numbers and more
- **Multiple Anonymization Levels**: Minimal, Standard, and Full detection modes
- **Robust Error Handling**: Comprehensive logging and error recovery
- **Multiple Output Formats**: DOCX, TXT, JSON, CSV mapping files
- **NLP Integration**: Optional Stanza NLP pipeline for enhanced name detection
- **Detailed Mapping**: Complete tracking of all anonymized data with original values

## 📋 Requirements

- Python 3.8 or higher
- Required packages (see `requirements.txt`):
  - `python-docx` - For DOCX document processing
  - `stanza` - For advanced NLP processing (optional)
  - `unicodedata2` - For text normalization

## 🛠️ Installation

### Quick Setup

```bash
# Clone or download the files
# Run the automated setup
python install_and_run.py
```

### Manual Installation

```bash
# Install required packages
pip install -r requirements.txt

# Download Stanza models (optional, for enhanced name detection)
python -c "import stanza; stanza.download('cs', model_dir='data/models/stanza_cs')"
```

## 📖 Usage

### Basic Usage

```bash
# Anonymize a document with default settings
python anonymizer_enhanced.py document.docx

# Specify output file
python anonymizer_enhanced.py input.docx --output anonymized.docx

# Use full anonymization level
python anonymizer_enhanced.py document.txt --level full
```

### Advanced Usage

```bash
# Multiple output formats for mapping
python anonymizer_enhanced.py document.docx --formats json txt csv

# Set logging level
python anonymizer_enhanced.py document.docx --log-level DEBUG

# Process text file with custom output
python anonymizer_enhanced.py data.txt --output processed.txt --level standard
```

### Command Line Options

```
positional arguments:
  input                 Input document path

optional arguments:
  -h, --help            Show help message
  --output OUTPUT, -o   Output document path
  --level {minimal,standard,full}
                        Anonymization level (default: standard)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging level (default: INFO)
  --formats {json,txt,csv} [FORMATS ...]
                        Mapping output formats (default: ['json', 'txt'])
```

## 🎯 Anonymization Levels

### Minimal
- Only detects obvious personal data
- Basic name patterns
- Essential identifiers (birth numbers, etc.)

### Standard (Default)
- Comprehensive personal data detection
- Advanced name recognition
- All common Czech personal identifiers
- Address and contact information

### Full
- Maximum detection sensitivity
- Additional patterns (passport numbers, credit cards, etc.)
- Context-aware detection
- Extended validation rules

## 📊 Output Files

The anonymizer generates several output files:

1. **Anonymized Document**: `[original_name]_anonymized.[ext]`
2. **Mapping Files**:
   - `[original_name]_mapping.json` - Complete mapping in JSON format
   - `[original_name]_mapping.txt` - Human-readable mapping
   - `[original_name]_mapping.csv` - CSV format for data analysis
3. **Log File**: `anonymizer.log` - Processing logs and warnings

## 🔍 Detection Patterns

### Personal Names
- Czech first names (male and female)
- Surnames with common Czech suffixes
- Name variants and possessive forms
- Context-aware detection

### Identifiers
- **Birth Numbers (RČ)**: Validates Czech birth number format
- **ID Cards**: 9-digit numbers with context validation
- **Bank Accounts**: Czech bank account format
- **IBAN**: International bank account numbers

### Contact Information
- **Phone Numbers**: Czech mobile and landline formats
- **Email Addresses**: Standard email validation
- **Addresses**: Czech address patterns

### Other Data
- **Dates**: Birth dates and other personal dates
- **VIN Numbers**: Vehicle identification numbers
- **License Plates**: Czech license plate format
- **Credit Cards**: Basic credit card number patterns

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_anonymizer.py
```

The test suite includes:
- Basic anonymization functionality
- Document processing tests
- Different anonymization levels
- Error handling verification

## 📝 Example

### Input Document
```
Smlouva o pracovním poměru

Zaměstnanec: Jan Novák
Datum narození: 15. března 1985
Rodné číslo: 850315/1234
Adresa: Václavské náměstí 1, 110 00 Praha
Telefon: +420 123 456 789
Email: jan.novak@email.cz
```

### Anonymized Output
```
Smlouva o pracovním poměru

Zaměstnanec: [[PERSON_1]]
Datum narození: [[DATE_1]]
Rodné číslo: [[BIRTH_ID_1]]
Adresa: [[ADDRESS_1]]
Telefon: [[PHONE_1]]
Email: [[EMAIL_1]]
```

### Mapping File (JSON)
```json
{
  "metadata": {
    "created_at": "2024-01-15T10:30:00",
    "statistics": {
      "PERSON": 1,
      "DATE": 1,
      "BIRTH_ID": 1,
      "ADDRESS": 1,
      "PHONE": 1,
      "EMAIL": 1
    }
  },
  "replacements": {
    "[[PERSON_1]]": ["Jan Novák"],
    "[[DATE_1]]": ["15. března 1985"],
    "[[BIRTH_ID_1]]": ["850315/1234"],
    "[[ADDRESS_1]]": ["Václavské náměstí 1, 110 00 Praha"],
    "[[PHONE_1]]": ["+420 123 456 789"],
    "[[EMAIL_1]]": ["jan.novak@email.cz"]
  }
}
```

## 🔧 Configuration

### Customizing Detection Patterns

You can modify the detection patterns by editing the `PatternDetector` class in `anonymizer_enhanced.py`:

```python
# Add custom pattern
custom_pattern = DetectionPattern(
    name="custom_id",
    pattern=re.compile(r'\bCUSTOM\d{6}\b'),
    category="CUSTOM_ID"
)
```

### Adding New Name Databases

Extend the `CzechNameDetector` class to include additional name databases:

```python
def _load_custom_names(self) -> Set[str]:
    # Load from external source
    return set(custom_names)
```

## 🚨 Important Notes

1. **Data Privacy**: This tool is designed for legitimate anonymization purposes. Always ensure compliance with data protection regulations.

2. **Backup**: Always keep backups of original documents before anonymization.

3. **Validation**: Review anonymized documents to ensure all sensitive data has been properly identified and replaced.

4. **Mapping Security**: Store mapping files securely as they contain the original sensitive data.

5. **Performance**: Large documents may take longer to process. Consider using appropriate anonymization levels.

## 🐛 Troubleshooting

### Common Issues

1. **Stanza Installation Issues**:
   ```bash
   # If Stanza fails to install, the anonymizer will work with heuristics only
   pip install stanza --no-deps
   pip install protobuf
   ```

2. **Memory Issues with Large Documents**:
   - Use minimal anonymization level
   - Process documents in smaller chunks
   - Increase system memory

3. **Encoding Issues**:
   - Ensure documents are saved in UTF-8 encoding
   - Check file permissions

### Log Analysis

Check the `anonymizer.log` file for detailed processing information and error messages.

## 📄 License

This project is provided as-is for educational and legitimate anonymization purposes. Users are responsible for compliance with applicable data protection laws and regulations.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the log files
3. Run the test suite to verify functionality
4. Submit detailed issue reports with sample documents (anonymized)

---

**⚠️ Disclaimer**: This tool is designed for legitimate data anonymization purposes. Users must ensure compliance with all applicable data protection laws and regulations. The authors are not responsible for misuse of this tool.