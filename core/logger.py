class Logger:

    def __init__(self, log_widget):
        self.log_widget = log_widget

    def write(self, message):
        self.log_widget.append(message)

    def clear(self):
        self.log_widget.clear()