class PiixxieError(Exception):
    """
    Generic error base class for anything Piixxie related.
    """
    pass


class VerificationError(PiixxieError):
    """
    Generic error raised when input image does not meet our requirements
    for processing.
    """
    pass


class DimensionError(VerificationError):
    """
    Error for when input image does not have dimensions which are a multiple
    of the pixel size.
    """
    pass
