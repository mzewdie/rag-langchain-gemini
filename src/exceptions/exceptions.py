

class EmbeddingQuotaExceededError(Exception):

    def __init__(self, retry_after: int=None):
        self.retry_after = retry_after