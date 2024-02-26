from reach_commons.utils import deprecated


@deprecated("Use reach_commons.aws.exceptions instead")
class SNSClientException(Exception):
    pass


@deprecated("Use reach_commons.aws.exceptions instead")
class HubspotBusinessNotFoundException(Exception):
    def __init__(self, business_id, message="Business not found"):
        self.business_id = business_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}. Business ID: {self.business_id}"


@deprecated("Use reach_commons.aws.exceptions instead")
class HubspotUserNotFoundException(Exception):
    def __init__(self, user_id, message="User not found"):
        self.user_id = user_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}. User ID: {self.user_id}"


@deprecated("Use reach_commons.aws.exceptions instead")
class SQSClientTopicNotFound(SNSClientException):
    pass


@deprecated("Use reach_commons.aws.exceptions instead")
class SQSClientPublishError(SNSClientException):
    pass
