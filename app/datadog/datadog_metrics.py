import os

from datadog import initialize
from datadog.threadstats import ThreadStats


statsd = ThreadStats()

ENVIRON = f"spotifiuby:{os.environ.get('ENVIRONMENT', 'test')}"


def update_users(count_users):
    statsd.gauge(
        'spotifiuby.total-users', count_users, tags=[ENVIRON],
    )


def new_login(provider):
    statsd.increment(f'spotifiuby.new-login.{provider}', tags=[ENVIRON])


def new_user(provider):
    statsd.increment(f'spotifiuby.new-user.{provider}', tags=[ENVIRON])
    update_users()