# Contributing to StayUp 🤝

Thank you for your interest in contributing to StayUp! We love your input! 🎉

## Ways to Contribute 🌟

1. Report bugs 🐛
2. Suggest new features 💡
3. Submit pull requests 🔧
4. Improve documentation 📚
5. Share the project ⭐

## Getting Started 🚀

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/manthanmtg/stayup.git
   cd stayup
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Process 💻

1. Create a new branch:
   ```bash
   git checkout -b feature-or-fix-name
   ```
2. Make your changes
3. Install the package locally for testing:
   ```bash
   # Make sure you're in your virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in editable mode with development dependencies
   pip install -e ".[dev]"
   
   # Verify installation
   python -c "import stayup; print(stayup.__version__)"
   ```
4. Run tests:
   ```bash
   pytest
   ```
5. Update documentation if needed
6. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
7. Push to your fork:
   ```bash
   git push origin feature-or-fix-name
   ```
8. Open a Pull Request

## Pull Request Guidelines 📋

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Follow the existing code style
5. Keep your PR small and focused
6. Write a clear PR description

## Code Style 🎨

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

## Running Tests ✅

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_specific.py

# Run with coverage
pytest --cov=stayup
```

## Documentation 📚

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Keep code comments current
- Update example usage if needed

## Need Help? 💭

- Open an issue for questions
- Join our community discussions
- Check existing issues and PRs

## Code of Conduct 🤝

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Recognition ⭐

Contributors will be acknowledged in our releases and README.

---

Thank you for contributing to StayUp! 🙏
