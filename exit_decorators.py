import atexit
import threading
import logging


class ExitHandler:
    def __init__(self, program_exit_handler=None,
                 function_exit_handler=None,
                 thread_exit_handler=None,
                 logger: logging = None):
        self.program_exit_handler = program_exit_handler
        self.function_exit_handler = function_exit_handler
        self.thread_exit_handler = thread_exit_handler
        self.entity_names = {
            "program": "Program",
            "function": "Function",
            "thread": "Thread"
        }
        self.logger = logger or logging.getLogger()

    def handle_exit(self):
        if self.program_exit_handler:
            self.program_exit_handler()
        elif self.function_exit_handler and threading.current_thread() == threading.main_thread():
            self.function_exit_handler()
        elif self.thread_exit_handler:
            self.thread_exit_handler()
        else:
            exiting_entity = self.get_exiting_entity()
            self.logger.info(f"{self.entity_names[exiting_entity]} is exiting")

    def get_exiting_entity(self):
        if threading.current_thread() == threading.main_thread():
            return "program"
        elif self.function_exit_handler:
            return "function"
        else:
            return "thread"


def program_exit_decorator(program_exit_handler=None):
    def decorator(func):
        exit_handler = ExitHandler(program_exit_handler=program_exit_handler)
        atexit.register(exit_handler.handle_exit)
        return func
    return decorator


def function_exit_decorator(function_exit_handler=None):
    def decorator(func):
        exit_handler = ExitHandler(function_exit_handler=function_exit_handler)
        return func
    return decorator


def thread_exit_decorator(thread_exit_handler=None):
    def decorator(func):
        exit_handler = ExitHandler(thread_exit_handler=thread_exit_handler)
        return func
    return decorator


# Usage example
if __name__ == "__main__":
    def my_program_exit_handler():
        print("Custom program exit handler")

    def my_function_exit_handler():
        print("Custom function exit handler")

    def my_thread_exit_handler():
        print("Custom thread exit handler")

    @program_exit_decorator(program_exit_handler=my_program_exit_handler)
    def main():
        print("Main function")

    @function_exit_decorator(function_exit_handler=my_function_exit_handler)
    def my_function():
        print("My function")

    @thread_exit_decorator(thread_exit_handler=my_thread_exit_handler)
    def my_thread():
        print("My thread")

    main()
