# Architecture of AI Agent for Disaster Resource and Volunteer Allocation

## Overview
The AI Agent for Disaster Resource and Volunteer Allocation project aims to efficiently allocate resources and volunteers during disaster situations. The system leverages data-driven optimization techniques to minimize unmet needs while ensuring that resources are allocated effectively.

## Project Structure
The project is organized into several key components, each serving a specific purpose:

- **src/**: Contains the main source code for the application.
  - **data/**: Responsible for data loading, preprocessing, and schema definitions.
    - **loader.py**: Functions to load data from CSV files into a DataFrame.
    - **preprocess.py**: Functions to preprocess the data, including handling missing values and converting severity levels.
    - **schemas.py**: Defines data schemas for validation.
  - **optimization/**: Implements the optimization logic for resource allocation.
    - **solver.py**: Contains the optimization logic using the PuLP library.
    - **model.py**: Defines the optimization model and objective function.
    - **constraints.py**: Specifies constraints for the optimization problem.
  - **ui/**: Manages the user interface components.
    - **dashboard.py**: Sets up the Streamlit dashboard for displaying results.
    - **components/**: Contains reusable UI components.
      - **maps.py**: Functions for visualizing data on maps.
      - **controls.py**: UI controls for user interaction.
    - **templates/**: HTML templates for the dashboard layout.
      - **layout.html**: Provides the HTML layout for the dashboard.
  - **agents/**: Manages the allocation of resources and training of models.
    - **dispatcher.py**: Allocates resources and volunteers to different zones.
    - **trainer.py**: Contains logic for training models if needed.
  - **utils/**: Utility functions for various operations.
    - **io.py**: Input and output operations.
    - **metrics.py**: Functions to calculate and display metrics related to optimization results.
  - **__init__.py**: Marks the directory as a Python package.

- **data/**: Contains raw and processed data files.
  - **raw/**: Directory for raw data files.
  - **processed/**: Directory for processed data files.

- **notebooks/**: Contains Jupyter notebooks for exploratory data analysis.
  - **exploration.ipynb**: Notebook for data exploration.

- **tests/**: Contains unit tests for various components of the project.
  - **test_data.py**: Unit tests for data loading and preprocessing.
  - **test_optimization.py**: Unit tests for optimization logic.
  - **test_ui.py**: Unit tests for the dashboard UI.

- **docs/**: Documentation for the project.
  - **architecture.md**: Document detailing the architecture of the project.

- **scripts/**: Contains scripts for running the application and tests.
  - **run_server.sh**: Script to run the Streamlit server.
  - **run_tests.sh**: Script to run the test suite.

- **pyproject.toml**: Configuration file specifying dependencies and settings for the project.

- **requirements.txt**: Lists required Python packages for the project.

- **.gitignore**: Specifies files and directories to be ignored by Git.

- **README.md**: Instructions on how to run the dashboard and other project details.

## Technologies Used
- Python: The primary programming language for the project.
- Pandas: For data manipulation and analysis.
- PuLP: For optimization and linear programming.
- Streamlit: For building the web dashboard.
- Jupyter Notebook: For exploratory data analysis.

## Conclusion
This architecture provides a comprehensive framework for developing an AI agent that can effectively allocate resources and volunteers during disasters. Each component is designed to work seamlessly with others, ensuring a robust and efficient system.