# Contributing to Pipecat Arabic Voice Agent (Sara)

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for everyone
- Respect differing viewpoints and experiences

## How Can I Contribute?

### Types of Contributions

1. **Bug Fixes**: Fix issues with the agent's functionality
2. **Feature Enhancements**: Add new capabilities or improve existing ones
3. **Documentation**: Improve README, add examples, or clarify instructions
4. **Testing**: Add test cases or improve test coverage
5. **Translations**: Help with Arabic language improvements or add dialect support
6. **Examples**: Create new use cases or scenarios

### Areas We'd Love Help With

- Adding support for Arabic dialects (Egyptian, Gulf, Levantine, Maghrebi)
- Improving speaker diarization accuracy
- Creating more conversation scenarios (hotel booking, customer service, etc.)
- Performance optimizations
- Better error handling and recovery
- Integration with additional transport layers
- Testing with different Arabic voices

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/Pipecat-Arabic-Agent-Sara.git
cd Pipecat-Arabic-Agent-Sara
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e ".[dev]"  # Install development dependencies
```

### 4. Set Up Environment Variables

Copy `.env.example` to `.env` and add your API keys.

### 5. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 100)
- Use type hints where appropriate
- Write docstrings for functions and classes

### Code Formatting

Format your code before committing:

```bash
black agent.py
```

### Comments

- Use clear, descriptive variable and function names
- Add comments for complex logic
- Include Arabic text examples in comments when relevant
- Document any assumptions about Arabic language handling

### Example Code Style

```python
async def process_arabic_order(
    customer_input: str,
    speaker_id: str
) -> dict:
    """Process a customer's order in Arabic.

    Args:
        customer_input: The transcribed Arabic text from the customer
        speaker_id: The speaker identifier (e.g., "S1", "S2")

    Returns:
        dict: Parsed order with items and prices

    Example:
        >>> process_arabic_order("أريد برجر كلاسيك", "S1")
        {'speaker': 'S1', 'items': ['classic_burger'], 'total': 25}
    """
    # Implementation here
    pass
```

## Pull Request Process

### Before Submitting

1. **Test Your Changes**: Ensure the agent runs without errors
2. **Update Documentation**: Update README.md if you've changed functionality
3. **Add Examples**: Include usage examples for new features
4. **Check Arabic Text**: Verify Arabic text displays correctly
5. **Clean Up**: Remove debugging code and commented-out lines

### Submitting a Pull Request

1. **Commit Your Changes**

```bash
git add .
git commit -m "Brief description of your changes"
```

Use clear commit messages:
- `feat: Add support for Egyptian Arabic dialect`
- `fix: Resolve speaker diarization timing issue`
- `docs: Update installation instructions`
- `refactor: Simplify LLM context management`

2. **Push to Your Fork**

```bash
git push origin feature/your-feature-name
```

3. **Open a Pull Request**

- Go to the original repository on GitHub
- Click "New Pull Request"
- Select your fork and branch
- Fill in the PR template with:
  - Description of changes
  - Why the change is needed
  - How to test the changes
  - Any breaking changes

### Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
How to test these changes:
1. Step 1
2. Step 2

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tested with real Arabic speech input
- [ ] No breaking changes (or documented if so)
```

### Review Process

- Maintainers will review your PR within a few days
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Reporting Bugs

### Before Reporting

- Check if the issue already exists in [GitHub Issues](https://github.com/yourusername/Pipecat-Arabic-Agent-Sara/issues)
- Verify your API keys are valid and have sufficient credits
- Test with the latest version of the code

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## To Reproduce
Steps to reproduce:
1. Run command '...'
2. Say '...' (include Arabic text if relevant)
3. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- Python version:
- OS:
- Pipecat version:
- API services used:

## Logs
```
Paste relevant error logs here
```

## Arabic Text Examples
If relevant, include example Arabic phrases
```

## Suggesting Enhancements

We welcome feature suggestions! Please open an issue with:

- Clear description of the enhancement
- Use case or scenario where it would be helpful
- Any Arabic language considerations
- Potential implementation approach (optional)

## Arabic Language Guidelines

When working with Arabic text in this project:

1. **Use Modern Standard Arabic (MSA)** as the default
2. **Right-to-Left Support**: Ensure text displays correctly
3. **Diacritics**: Be mindful of tashkeel (diacritical marks)
4. **Numerals**: Use Eastern Arabic numerals (٠١٢٣) or Western (0123) consistently
5. **Testing**: Test with various Arabic inputs including:
   - Short phrases
   - Long sentences
   - Numbers and prices
   - Mixed Arabic/English (if applicable)

## Questions?

- Open an issue for questions
- Join the [Pipecat Discord](https://discord.gg/pipecat) community
- Check the [Pipecat Documentation](https://docs.pipecat.ai/)

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Project README (for significant contributions)
- Release notes

Thank you for contributing to making Arabic voice AI more accessible!
