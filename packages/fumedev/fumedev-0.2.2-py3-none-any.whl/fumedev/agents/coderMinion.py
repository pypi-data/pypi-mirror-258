from fumedev import env

from fumedev.agents.agent import Agent
from openai import OpenAI
from fumedev.coder.coder.coders import Coder
from fumedev.coder.coder.models.model import Model
from fumedev.utils.get_changed_files import get_changed_files

from fumedev.utils.get_dependents.get_dependents import get_dependents

class CoderMinion(Agent):
    """
    The CoderMinion class, inheriting from Agent, is responsible for automating coding tasks. 
    It utilizes OpenAI's GPT models to generate code based on the provided task and file paths.
    """
    def __init__(self, task, file_paths):
        """
        Initializes the CoderMinion with a specific task and related file paths.

        :param task: The coding task description.
        :param file_paths: A list of file paths in the codebase relevant to the task.
        """
        super().__init__()
        self.task = task
        self.file_paths = file_paths

    def code(self):
        """
        Executes the coding task by processing the provided file paths, generating code
        with an AI model and applying the code changes to the codebase.
        """
        client = OpenAI(api_key=env.OPENAI_API_KEY,base_url=env.BASE_URL)

        files = self.file_paths
        dependent_files = []

        # TAKES WAY TOO LONG AND IDK WHY!
        for file in self.file_paths:
            dependent_files +=  get_dependents(file)
            
        files += dependent_files[:3]
        gpt4_model = Model.create(name='gpt-4-turbo-preview', client=client)
        gpt4_model.max_context_tokens
        coder = Coder.create(client=client, fnames=files, main_model=gpt4_model, use_git=False, code_theme="dark")
        coder.run(self.task)
        self.apply_changes()

    def flush_chat(self):
        """
        Clears the chat messages stored in this CoderMinion instance.

        :return: An empty list representing the cleared messages.
        """
        self.messages = []
        return self.messages
    
    @staticmethod
    def apply_changes():
        """
        Applies the changes suggested by the AI model to the codebase files.
        """
        changed_files = get_changed_files()

        for path in changed_files:
            if env.absolute_path('codebase/') in path:
                if not path.startswith(env.absolute_path('codebase/')):
                    continue

                new_file = path
            else:
                new_file = env.absolute_path('codebase/') + path

            old_file = env.PROJECT_PATH + '/' + path.replace(env.absolute_path('codebase/'), '')
            with open(new_file, 'r') as new_f:
                new_content = new_f.read()
            with open(old_file, 'w') as old_f:
                old_f.write(new_content)