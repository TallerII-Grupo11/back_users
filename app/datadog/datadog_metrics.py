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


def new_login():
    """Métricas de login de usuarios utilizando mail y contraseña"""
    statsd.increment(f'spotifiuby.new-login', tags=[ENVIRON])


def new_user():
    """Métricas de nuevos usuarios utilizando mail y contraseña"""
    statsd.increment(f'spotifiuby.new-user', tags=[ENVIRON])
    update_users()

def new_login_federated():
    """Métricas de login de usuarios utilizando identidad federada"""
    metric = f'spotifiuby.new-login-federated'
    statsd.increment(metric, tags=[ENVIRON])


def new_user_federated():
    """Métricas de nuevos usuarios utilizando identidad federada"""
    metric = f'spotifiuby.new-user-federated'
    statsd.increment(metric, tags=[ENVIRON])
    update_users()

def update_blocked_users():
    """Métricas de usuarios bloqueados"""
    statsd.gauge(
        'spotifiuby.blocked-users',
        10, # obtener los usuarios bloqueados por una query a la bdd
        tags=[ENVIRON],
    )

def password_reset():
    """Métricas de recupero de contraseña"""
    statsd.increment('spotifiuby.password-reset', tags=[ENVIRON])