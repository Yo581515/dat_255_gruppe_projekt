import json
from openai import OpenAI
import functions as fh
import function_tools as tls
import os
import time
from dotenv import load_dotenv

load_dotenv()


class Assistant():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.tools = [tls.code_interpreter,tls.create_file_function, tls.delete_file_function,
                      tls.delete_all_txt_files_function, tls.finish_conversation_function, tls.date_time_now_function
            , tls.local_temperature_info]

        self.assistant = self.client.beta.assistants.create(
            name="file_handler_bot",
            instructions="You help manage creating and deleting files in a directory. You can create a file, delete a file, or delete all txt files in the directory. Keep responses under 20 words.",
            tools=self.tools,
            model="gpt-3.5-turbo"
        )

        self.thread = self.client.beta.threads.create()

    def response_message(self, messages):
        # EXPECTS MESSAGES IN ASC ORDER!
        m = '\n'.join(thread_message.content[0].text.value for thread_message in messages.data)
        return m

    def wait_on_run(self, run, thread):
        '''
        Simple function that waits on the run of a particular thread.
        Returns the run once the thread has been run.
        '''
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            # print(run.status)
            time.sleep(0.5)
        # print("return", run.status)
        return run

    def send_message(self, text):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=text
        )

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        continue_conversation = True
        run = self.wait_on_run(run, self.thread)
        # print("waited on run 1", run.status)
        if run.status == "requires_action":
            tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print("Function Name:", name)
            print("Function Arguments:")
            print(arguments)
            response = None

            match name:
                case "create_text_file":
                    response = fh.create_text_file(str(arguments['file_name']), str(arguments.get('content', '')))
                case "delete_file":
                    response = fh.delete_file(arguments['file_name'])
                case "delete_all_txt_files":
                    response = fh.delete_all_txt_files()
                case "finish_conversation":
                    continue_conversation = fh.finish_conversation(arguments['value'])
                    response = "Goodbye!"
                case "date_time_now":
                    response = fh.date_time_now()
                case "local_temperature_info":
                    response = fh.local_temperature_info()
                case _:
                    response = "I'm sorry, I don't understand that command."

            run = self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread.id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(response),
                    }
                ],
            )

        run = self.wait_on_run(run, self.thread)
        # print("waited on run 2", run.status)

        messages = self.client.beta.threads.messages.list(
            self.thread.id,
            order="asc",
            after=message.id
        )

        return self.response_message(messages), continue_conversation

    def dissconnect_assistant(self):

        my_assistants = self.client.beta.assistants.list(
            order="desc",
            limit="20",
        )
        response = self.client.beta.assistants.delete(my_assistants.data[0].id)
        print(response)
