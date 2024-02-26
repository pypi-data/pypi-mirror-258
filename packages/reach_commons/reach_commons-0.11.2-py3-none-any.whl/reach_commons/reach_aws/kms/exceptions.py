from reach_commons.utils import deprecated


@deprecated("Use reach_commons.exceptions instead")
class KMSClientException(Exception):
    pass
