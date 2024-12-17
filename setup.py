from setuptools import setup, find_packages

# Function to read the requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

# Read dependencies from requirements.txt
install_requires = parse_requirements('requirements.txt')

setup(
    name="openvas-cli",  # Name of the project
    version="0.1",  # Version number
    description="A CLI app to automate simple tasks regarding openvas",  # Short description
    author="Otávio dos Santos Lima",  # Author's name
    author_email="santos.lima.otavio07@gmail.com",  # Author's email
    url="https://github.com/oivatO-soD-sotnaS/openvas-custom-tool",  # Project's URL (e.g., GitHub repository)
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=install_requires,
    entry_points={  # Entry points for command line tools (if any)
        "console_scripts": [
            "openvas-cli=cli_tool.main:app",  # Example: to create a command-line tool
        ],
    },
)
