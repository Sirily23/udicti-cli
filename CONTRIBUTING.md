# Contributing to UDICTI CLI

First off, thank you for considering contributing to UDICTI CLI! It's people like you that make this such a great tool for the UDSM developer community.

We welcome contributions of all kinds, from fixing bugs and adding new features to improving documentation and reporting issues.

## How to Contribute

### Reporting Issues
If you find a bug, have a feature request, or a question, please [open an issue](https://github.com/Sirily23/udicti-cli/issues). Please provide as much information as possible, including:
- A clear and descriptive title.
- A detailed description of the issue or feature request.
- Steps to reproduce the bug.
- Your operating system and Python version.

### Submitting Pull Requests
If you'd like to contribute code, please follow these steps:

1.  **Fork the Repository**
    Click the "Fork" button at the top right of the [repository page](https://github.com/Sirily23/udicti-cli).

2.  **Clone Your Fork**
    ```bash
    git clone https://github.com/YOUR_USERNAME/udicti-cli.git
    cd udicti-cli
    ```

3.  **Set Up the Development Environment**
    We recommend using a virtual environment to keep dependencies isolated.
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate

    # Install the tool in "editable" mode with development dependencies
    pip install -e .
    ```

4.  **Create a New Branch**
    Create a new branch for your feature or bug fix. Use a descriptive name.
    ```bash
    git checkout -b feature/your-awesome-feature
    ```

5.  **Make Your Changes**
    Write your code! Make sure to follow the project's coding style.

6.  **Format and Lint Your Code**
    Before committing, please run the formatting and linting scripts to ensure your code adheres to the project's standards.
    ```bash
    # Format the code
    ./scripts/format.sh

    # Lint the code
    ./scripts/lint.sh
    ```

7.  **Commit Your Changes**
    Use a clear and descriptive commit message.
    ```bash
    git commit -m "feat: Add awesome new feature"
    ```

8.  **Push to Your Fork**
    ```bash
    git push origin feature/your-awesome-feature
    ```

9.  **Open a Pull Request**
    Go to the original repository on GitHub and open a pull request. Provide a clear description of your changes and link to any relevant issues.

## Code of Conduct
To ensure a welcoming and inclusive environment, we expect all contributors to adhere to our Code of Conduct. Please be respectful and considerate of others. Harassment or discriminatory behavior will not be tolerated.

Thank you for your contribution!
