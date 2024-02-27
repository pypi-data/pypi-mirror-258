from finter.framework_model.submission.helper_execute import load_and_run
from finter.framework_model.submission.helper_notebook import (
    extract_and_convert_notebook,
)
from finter.framework_model.submission.helper_submission import submit_model
from finter.settings import logger


class NotebookSubmissionHelper:
    def __init__(self, cell_indices, notebook_name, model_name, model_info):
        self.cell_indices = cell_indices
        self.notebook_name = notebook_name
        self.model_name = model_name
        self.model_info = model_info

        self.model_type = model_info["type"]

    def process(self, start, end, run=False, submit=False):
        """
        Extracts and optionally runs the notebook based on the if_run flag.

        :param start: Start date for the run method.
        :param end: End date for the run method.
        :param if_run: Flag to determine whether to run after extract.
        """
        # Extract and convert the notebook
        output_file_path = extract_and_convert_notebook(
            self.cell_indices,
            self.notebook_name,
            self.model_name,
            model_type=self.model_type,
        )

        if not output_file_path:
            logger.error("Error extracting notebook.")
            return

        logger.info(f"Notebook extracted to {output_file_path}")

        # Conditionally run the extracted notebook
        if run:
            self.position = load_and_run(
                start, end, output_file_path, model_type=self.model_type
            )
            logger.info("Notebook run successfully.")

        if submit:
            self.submit_result = submit_model(self.model_info, self.model_name)
            logger.info("Model submitted successfully.")
