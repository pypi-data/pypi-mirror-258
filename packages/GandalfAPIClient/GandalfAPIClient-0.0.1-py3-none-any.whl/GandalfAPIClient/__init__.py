from GandalfAPIClient.main import MovieAPI, QuoteAPI


class GandalfAPI:
    def __init__(self, api_key):
        self.movie = MovieAPI(api_key)
        self.quote = QuoteAPI(api_key)


__version__ = "0.0.1"
__all__ = "__version__", "GandalfAPI"
