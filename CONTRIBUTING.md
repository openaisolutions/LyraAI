# Contributing to LYRA AI

We welcome contributions from the community! Here's how you can help:

## How to Contribute

### Reporting Bugs
- Open an issue on GitHub with a clear description of the bug.
- Include steps to reproduce, expected behavior, and actual behavior.
- Add labels like `bug` or `help wanted` if applicable.

### Suggesting Features
- Open an issue with the `enhancement` label.
- Describe the feature, its use case, and potential implementation.

### Code Contributions
1. **Fork the repository** and create a feature branch (`git checkout -b feature/your-feature`).
2. **Commit your changes** with clear, descriptive messages.
3. **Push to your fork** and open a pull request to `main`.
4. **Ensure tests pass** (run `pytest` locally).
5. **Follow the code style**:
   - Use 4 spaces for indentation.
   - Keep lines under 88 characters.
   - Use descriptive variable/function names.
   - Add docstrings for new functions/classes.

### Pull Request Guidelines
- PRs should be **focused** (one feature/bug per PR).
- Include a **description** of changes and their purpose.
- Reference any related issues (e.g., `Fixes #123`).
- Ensure all **tests pass** and **linting checks** (if applicable) are green.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sevir65/LyraAI.git
   cd LyraAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install in development mode:
   ```bash
   pip install -e .
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Code of Conduct
By contributing, you agree to uphold our [Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). Be respectful and inclusive.

## License
By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
