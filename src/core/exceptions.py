class NotFoundException(Exception):
    """Exceção levantada quando um recurso não é encontrado."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)