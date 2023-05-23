import atexit
import threading
import logging


class ExitHandler:
    def __init__(self, logger: logging = None):
        self.program_exit_handler = None
        self.function_exit_handler = None
        self.thread_exit_handler = None
        self.entity_names = {
            "program": "Program",
            "function": "Function",
            "thread": "Thread"
        }
        self.logger = logger or logging.getLogger()

    def set_program_exit_handler(self, handler_func):
        self.program_exit_handler = handler_func

    def set_function_exit_handler(self, handler_func):
        self.function_exit_handler = handler_func

    def set_thread_exit_handler(self, handler_func):
        self.thread_exit_handler = handler_func

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


def exit_handler_decorator(exit_handler_func):
    def decorator(func):
        exit_handler = ExitHandler()
        exit_handler.set_program_exit_handler(exit_handler_func)
        atexit.register(exit_handler.handle_exit)
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

    @exit_handler_decorator(my_program_exit_handler)
    def main():
        print("Main function")

    @exit_handler_decorator(my_function_exit_handler)
    def my_function():
        print("My function")

    @exit_handler_decorator(my_thread_exit_handler)
    def my_thread():
        print("My thread")

    main()
