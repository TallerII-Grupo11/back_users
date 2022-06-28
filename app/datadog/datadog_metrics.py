import os
from typing import List

from datadog import initialize, statsd

"""
    CA 1: Métricas de nuevos usuarios utilizando mail y contraseña
    CA 2: Métricas de nuevos usuarios utilizando identidad federada
    CA 3: Métricas de login de usuarios utilizando mail y contraseña
    CA 4: Métricas de login de usuarios utilizando identidad federada
    CA 5: Métricas de usuarios bloqueados
    CA 6: Métricas de recupero de contraseña
"""

options = {
    'statsd_host': '127.0.0.1',
    'statsd_port': 8125,
}
initialize(**options)


class DataDogMetric:
    @staticmethod
    def increment(metric: str, tags: List[str] = None):
        if os.environ.get('ENVIRONMENT', 'test') != 'prod':
            return
        statsd.increment(metric, tags=tags)

    @staticmethod
    def new_login():
        """Métricas de login de usuarios utilizando mail y contraseña"""
        DataDogMetric.increment("spotifiuby.login", tags=["method:email"])

    @staticmethod
    def new_login_federated():
        """Métricas de login de usuarios utilizando identidad federada"""
        DataDogMetric.increment("spotifiuby.login", tags=["method:federated"])

    @staticmethod
    def new_user():
        """Métricas de nuevos usuarios utilizando mail y contraseña"""
        DataDogMetric.increment("spotifiuby.new-user", tags=["method:email"])

    @staticmethod
    def new_user_federated():
        """Métricas de nuevos usuarios utilizando identidad federada"""
        DataDogMetric.increment("spotifiuby.new-user", tags=["method:federated"])

    @staticmethod
    def blocked_user():
        """Métricas de nuevos usuarios utilizando identidad federada"""
        DataDogMetric.increment("spotifiuby.blocked-user")

    @staticmethod
    def password_reset():
        """Métricas de recupero de contraseña"""
        DataDogMetric.increment("spotifiuby.password-reset")
