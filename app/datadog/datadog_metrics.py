import os

from datadog import initialize
from datadog.threadstats import ThreadStats


statsd = ThreadStats()

ENVIRON = f"spotifiuby:{os.environ.get('ENVIRONMENT', 'test')}"

"""
    CA 1: Métricas de nuevos usuarios utilizando mail y contraseña
    CA 2: Métricas de nuevos usuarios utilizando identidad federada
    CA 3: Métricas de login de usuarios utilizando mail y contraseña
    CA 4: Métricas de login de usuarios utilizando identidad federada
    CA 5: Métricas de usuarios bloqueados
    CA 6: Métricas de recupero de contraseña
"""


class DataDogMetric():

    def update_users(self):
        statsd.gauge(
            'spotifiuby.total-users', 10, tags=[ENVIRON],
        )

    def new_login(self):
        """Métricas de login de usuarios utilizando mail y contraseña"""
        statsd.increment('spotifiuby.new-login', tags=[ENVIRON])

    def new_user(self):
        """Métricas de nuevos usuarios utilizando mail y contraseña"""
        statsd.increment('spotifiuby.new-user', tags=[ENVIRON])
        update_users()

    def new_login_federated(self):
        """Métricas de login de usuarios utilizando identidad federada"""
        metric = 'spotifiuby.new-login-federated'
        statsd.increment(metric, tags=[ENVIRON])

    def new_user_federated(self):
        """Métricas de nuevos usuarios utilizando identidad federada"""
        metric = 'spotifiuby.new-user-federated'
        statsd.increment(metric, tags=[ENVIRON])
        update_users()

    def update_blocked_users(self):
        """Métricas de usuarios bloqueados"""
        statsd.gauge(
            'spotifiuby.blocked-users',
            10,  # obtener los usuarios bloqueados por una query a la bdd
            tags=[ENVIRON],
        )

    def password_reset(self):
        """Métricas de recupero de contraseña"""
        statsd.increment('spotifiuby.password-reset', tags=[ENVIRON])

    def start(self, new_app):
        options = {'statsd_host': '127.0.0.1', 'statsd_port': 8125}
        initialize(**options)
        statsd.start()

        if os.environ.get('ENVIRONMENT', 'test') == 'test':
            return

        with new_app.app_context():
            self.update_blocked_users()
            self.update_users()
