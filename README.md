# MoneyControl POM Test Suite

A comprehensive Page Object Model (POM) based test suite for MoneyControl website using Selenium WebDriver and Pytest.

## 🏗️ Project Structure

```
pom_moneycontrol/
├── config/
│   ├── __init__.py
│   └── config.py                 # Test configuration and settings
├── pages/
│   ├── __init__.py
│   ├── base_page.py             # Base page object class
│   ├── home_page.py             # Homepage page object
│   └── login_page.py            # Login page object
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py        # WebDriver factory
│   └── otp_fetcher.py           # OTP fetching utility
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration and fixtures
│   └── test_moneycontrol_login.py # Test cases
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Pytest Framework**: Modern Python testing framework with powerful features
- **OTP Automation**: Automatic OTP fetching from Gmail using IMAP
- **Configurable**: Centralized configuration management
- **Reusable Components**: Modular design for easy maintenance
- **Cross-browser Support**: Ready for multiple browser support
- **Detailed Logging**: Comprehensive test execution logging

## 📋 Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- ChromeDriver (automatically managed by webdriver-manager)
- Gmail account with App Password for OTP fetching

## 🛠️ Installation

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd pom_moneycontrol
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials**
   Edit `config/config.py` and update:
   - `EMAIL`: Your Gmail address
   - `PASSWORD`: Your Gmail App Password (not regular password)

## ⚙️ Configuration

### Gmail App Password Setup

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Create an App Password for "Mail"
4. Use this App Password in the config file

### Test Configuration

Key configuration options in `config/config.py`:

```python
# Timeouts
EXPLICIT_WAIT = 30        # Maximum wait time for elements
OTP_WAIT_TIME = 8         # Wait time for OTP email

# OTP Settings
OTP_MAX_RETRIES = 6       # Maximum OTP fetch attempts
OTP_WAIT_INTERVAL = 5     # Wait between OTP fetch attempts
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Run only smoke tests
pytest -m smoke

# Run only login tests
pytest -m login

# Run only OTP tests
pytest -m otp
```

### Run Specific Test File
```bash
pytest tests/test_moneycontrol_login.py
```

### Run Specific Test Method
```bash
pytest tests/test_moneycontrol_login.py::TestMoneyControlLogin::test_homepage_loads_successfully
```

### Run Tests with HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### Run Tests in Parallel
```bash
pytest -n auto
```

## 📊 Test Categories

### Smoke Tests (`@pytest.mark.smoke`)
- Basic functionality tests
- Critical path validation
- Quick execution

### Login Tests (`@pytest.mark.login`)
- Login page navigation
- Email field validation
- Form submission

### OTP Tests (`@pytest.mark.otp`)
- OTP sending functionality
- OTP fetching from email
- OTP validation

## 🔧 Customization

### Adding New Page Objects

1. Create a new file in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class variables
4. Implement page-specific methods

Example:
```python
from .base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    # Locators
    ELEMENT_LOCATOR = (By.ID, "element-id")
    
    def perform_action(self):
        self.click_element(self.ELEMENT_LOCATOR)
```

### Adding New Test Cases

1. Create test methods in existing test classes or create new test files
2. Use appropriate pytest markers
3. Follow naming convention: `test_<functionality>_<scenario>`

### Extending Configuration

Add new configuration options in `config/config.py`:

```python
class TestConfig:
    # Add new configuration
    NEW_SETTING = "value"
    
    @classmethod
    def get_new_setting(cls):
        return cls.NEW_SETTING
```

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver Issues**
   - Ensure Chrome browser is installed
   - Update Chrome to latest version
   - Clear browser cache

2. **OTP Fetching Issues**
   - Verify Gmail App Password is correct
   - Check Gmail IMAP is enabled
   - Ensure 2FA is enabled on Gmail account

3. **Element Not Found**
   - Check if website structure changed
   - Update locators in page objects
   - Increase wait times in configuration

### Debug Mode

Run tests with verbose output:
```bash
pytest -v -s
```

## 📈 Best Practices

1. **Page Object Model**: Keep page objects focused on single responsibility
2. **Locators**: Use stable locators (ID, name) over XPath when possible
3. **Wait Strategies**: Use explicit waits for better reliability
4. **Test Data**: Keep test data separate from test logic
5. **Error Handling**: Implement proper exception handling
6. **Documentation**: Document complex test scenarios

## 🤝 Contributing

1. Follow the existing code structure
2. Add appropriate docstrings
3. Include test cases for new features
4. Update documentation as needed

## 📄 License

This project is for educational and testing purposes.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review test logs for error details
3. Verify configuration settings 