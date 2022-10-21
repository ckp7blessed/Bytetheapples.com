# DEVELOPMENT SETTINGS 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kh1rty#33s4aw37+(c0a)6+$bb^)_qhcm&8&$lzyuu(8m9y01d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# AWS S3 
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_REGION_NAME = 'us-east-2'
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_ADDRESSING_STYLE = "virtual"

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'