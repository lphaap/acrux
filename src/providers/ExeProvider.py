import src.utils.logger as logger;
import subprocess
import platform


class ExeProvider:

    def run_executable(executable_path):
        """
        Run the specified executable.

        Args:
        - executable_path (str): Path to the executable file.

        Raises:
        - Exception: If an error occurs while running the executable.
        """
        try:
            subprocess.run([executable_path])
        except Exception as e:
            logger.log(f"Error running executable: {e}")

    def execute(executable_path):
        """
        Main function to gather user input and execute the specified executable.
        """
        try:
            # Check if the platform is supported
            supported_platforms = ["Windows", "Linux", "Darwin"]
            current_platform = platform.system()

            if current_platform in supported_platforms:
                ExeProvider.run_executable(executable_path)
            else:
                logger.log(f"Unsupported operating system: {current_platform}")

        except Exception as e:
            logger.log(f"An unexpected error occurred: {e}")
