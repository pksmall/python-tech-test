import os


class MainConfig(object):
    """Production configuration."""
    LANGUAGES = ['en', 'ru']
    ADMIN_SECRET_KEY = '983aSDOASbhasIF34u3segkdfs7845879tsgerudfg'
    SECRET_KEY = '4wgq3wrg3wdfs3rhuffdbadfks;sh4faw34w'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    STRIPE_SECRET_KEY = 'foo'
    STRIPE_PUBLISHABLE_KEY = 'bar'
    ACCESS_TOKEN_EXPIRATION = 86400
    REFRESH_TOKEN_EXPIRATION = 86400
