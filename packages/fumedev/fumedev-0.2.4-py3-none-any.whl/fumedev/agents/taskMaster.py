import tiktoken
from openai import OpenAI
import fumedev.env as env
from fumedev.agents.agent import Agent
from fumedev.prompts import task_master_system_prompt, task_master_user_prompt
from fumedev.utils.process_snippets import process_snippets

class TaskMaster(Agent):
    def __init__(self, task, snippets):
        self.messages = []
        self.task = task
        self.snippets = snippets
        self.client = OpenAI()

    def solve(self, feedback="", old_plan=""):
        context = self._generate_context()
        if not context:
            print('Too many files in. the context')
            return False
        
        self.messages = [{'role': 'system', 'content': task_master_system_prompt()},
                         {'role': 'user', 'content': task_master_user_prompt(task=self.task, context=context, feedback=feedback, old_plan=old_plan)}]
        
        stream = self.client.chat.completions.create(model=env.BASE_MODEL, messages=self.messages, stream=True)
        collected_messages = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunk_message = chunk.choices[0].delta.content  # extract the message
                collected_messages.append(chunk_message) 
                print(chunk_message, end="")

        collected_messages = [m for m in collected_messages if m is not None]
        full_reply_content = ''.join([m for m in collected_messages])

        return full_reply_content

    def _generate_context(self, max_tokens = 70000):
        encoding = tiktoken.encoding_for_model(env.BASE_MODEL)
        increment = 100
        iteration = 1
        num_tokens = 0

        while num_tokens < max_tokens:
            context_files = process_snippets(snippets=self.snippets, lines_before=increment*iteration, lines_after=increment*iteration)
            context_str = self._format_snippets(snippets=context_files)
            new_num_tokens = len(encoding.encode(context_str))
            iteration += 1
            if new_num_tokens == num_tokens:
                break
            else:
                num_tokens = new_num_tokens

        if iteration == 1:
            return False
        else:
            context_files = process_snippets(snippets=self.snippets, lines_before=increment*(iteration-1), lines_after=increment*(iteration-1))
            context_str = self._format_snippets(snippets=context_files)
            return context_str

    def _format_snippets(self, snippets):
        res = ""

        for s in snippets:
            res += f"# File Path: {s.get('file_path')}\n{s.get('code')}\n\n"

        return res
