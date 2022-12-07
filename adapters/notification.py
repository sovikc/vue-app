from vue import user


class UserNotification(user.AbstractUserNotification):

    # TODO use a 3rd party email provider e.g. SendGrid or SNS
    def notify_user(person: user.User):
        pass
