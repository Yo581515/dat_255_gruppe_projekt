import os


def create_text_file(file_name, content=""):
    try:
        with open(file_name, 'x') as file:
            file.write(content)
        return "file created successfully."
    except Exception as e:
        return f"An error occurred: {e}"


def delete_file(file_name):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            return f"File '{file_name}' has been deleted."
        else:
            return f"File '{file_name}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"


def delete_all_txt_files():
    try:
        for file_name in os.listdir():
            if file_name.endswith('.txt'):
                os.remove(file_name)
                print(f"File '{file_name}' has been deleted.")
        return "All txt files have been deleted."
    except Exception as e:
        return f"An error occurred: {e}"


def finish_conversation(value=False):
    return not value
