import firebase_admin
from firebase_admin import auth, credentials

from app.conf.config import Settings
from app.domain.users.model.user import User, UserStatus


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Firebase(metaclass=Singleton):
    def __init__(self, settings: Settings):
        opt = {
            "projectId": settings.firebase_project_id,
            "storageBucket": settings.firebase_storage_bucket,
        }

        cred = {
            "type": "service_account",
            "project_id": settings.firebase_project_id,
            "private_key_id": settings.firebase_private_key_id,
            "private_key": settings.firebase_private_key.replace("\\n", "\n"),
            "client_email": settings.firebase_client_email,
            "client_id": settings.firebase_client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": settings.firebase_client_cert_url,
        }
        print(dict(cred))
        cc = credentials.Certificate(dict(cred))
        self.app_users = firebase_admin.initialize_app(
            credential=cc, options=opt, name="users"
        )
        # self.app_admins = firebase_admin.initialize_app(
        #     credential=cc, options=opt, name="Admins"
        # )

    def update_user(self, user: User):
        disabled = UserStatus.BLOCKED == user.status
        return auth.update_user(
            user.firebase_id,
            email=user.email,
            disabled=disabled,
            app=self.app_users,
        )

    # def update_admin(self, admin: Admin):
    #     disabled = AdminStatus.BLOCKED == admin.status
    #     return auth.update_user(
    #         admin.firebase_id,
    #         email=admin.email,
    #         disabled=disabled,
    #         app=self.app_admins,
    #     )
