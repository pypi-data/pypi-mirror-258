from setuptools import setup

setup(
    name='nipyproto',
    version='1.1',
    description='Post only client for Nostr, Activity Pub, and AT',
    py_modules=['nipyproto'],
    install_requires=['pynostr', 'mastodon.py', 'atproto', 'keyring'],
    entry_points={
        'console_scripts': [
            'nipyproto = nipyproto:nipyproto',
        ],
    },
)
