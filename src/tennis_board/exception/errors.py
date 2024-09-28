class ApplicationError(Exception):
    def __init__(self, status_code: int, status: str, message: str) -> None:
        super().__init__()
        self.status_code = status_code
        self.status = status
        self.message = message
