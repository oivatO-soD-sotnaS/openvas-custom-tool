# Python CLI Application for Report Import and Management

This project is a Python-based Command-Line Interface (CLI) application designed to efficiently import and organize OpenVAS reports into a structured database (MySQL or PostgreSQL). The application provides tools to fetch reports, configure environment variables, and inspect the current environment setup.

---

## Features

### Commands

1. **fetch**
   - Imports data from all existing OpenVAS reports into a local database.
   - Organizes the data into three main tables:
     - `report`
     - `vulnerability`
     - `report_vulnerability` (equivalent to a results table).
   - Command:
     ```bash
     python cli_tool/main.py fetch
     ```

2. **configure**
   - Configures the necessary environment variables and saves them in the `cli_tool/.env` file.
   - Usage:
     ```bash
     python cli_tool/main.py configure
     ```
   - Options:
     - `--gmp`: Configures only the GMP-related environment variables for OpenVAS.
     - `--database`: Configures only the database-related environment variables.

3. **show-vars**
   - Displays the current environment variables from the `.env` file.
   - Command:
     ```bash
     python cli_tool/main.py show-vars
     ```

---

## Installation

Before running the application, ensure the required Python packages are installed. A `requirements.txt` file is provided in the root of the project.

### Steps:
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <project_directory>
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Configure environment variables:**
   Run the `configure` command to set up your environment variables. For example:
   ```bash
   python cli_tool/main.py configure
   ```
   To configure only GMP-related variables:
   ```bash
   python cli_tool/main.py configure --gmp
   ```
   To configure only database-related variables:
   ```bash
   python cli_tool/main.py configure --database
   ```

2. **Fetch reports:**
   Import and organize reports into the database:
   ```bash
   python cli_tool/main.py fetch
   ```

3. **View environment variables:**
   Check the current environment variable settings:
   ```bash
   python cli_tool/main.py show-vars
   ```

---

## Database Compatibility
- **MySQL**
- **PostgreSQL**

Ensure the target database is properly configured and accessible before running the `fetch` command.

---

## Notes
- The `.env` file stores sensitive information (e.g., credentials) unencrypted. Handle it with care and restrict access appropriately.
- Ensure OpenVAS is set up and accessible for the `fetch` command to work.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

Feel free to contribute or report issues to improve this tool!
