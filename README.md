# Local environment setup
#### 1. Create a virtual environment and activate it.

#### 2. Clone repository and cd to the folder:

```
(wagenv) #:~/wagtail$ git clone https://github.com/ckan/ckan.org.git
```

#### 3. For local development: comment `psycopg2` in `requirements.txt`.

#### 4. Pip install requrements.txt

#### 5. Remove `cache` and `media` links from ckan.org folder.

#### 6. Create `media` folder in the `ckan.org` directory.

#### 7. Create `static` folder in the `ckan.org` directory and run `python manage.py collectstatic`.

#### 8.We can use sqlite db for local development, switch it in the settings:

```
diff --git a/ckanorg/settings/base.py b/ckanorg/settings/base.py
index be311ca..ec8777f 100644
--- a/ckanorg/settings/base.py
+++ b/ckanorg/settings/base.py
@@ -225,11 +225,7 @@ with open(BASE_DIR + '/../config/secret.txt') as f:
 
 DATABASES = {
     'default': {
-        'ENGINE': 'django.db.backends.postgresql_psycopg2',
-        'NAME': 'ckanorg',
-        'USER': 'ckanorg',
-        'PASSWORD': DB_PASS,
-        'HOST': DB_HOST,
-        'PORT': 5432,
+        'ENGINE': 'django.db.backends.sqlite3',
+        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
 }
```

#### 9. To not create all pages from the scratch you can use existing dummy sqlite database.
(Ask managers for `db.sqlite3` file and copy it into the `ckan.org` folder).
Otherwise run: `python manage.py makemigrations; python manage.py migrate`.

#### 10. We can disable wagtail cache for local development:

```
diff --git a/ckanorg/settings/base.py b/ckanorg/settings/base.py
index be311ca..3837822 100644
--- a/ckanorg/settings/base.py
+++ b/ckanorg/settings/base.py
@@ -49,7 +49,6 @@ INSTALLED_APPS = [
     'wagtail.admin',
     'wagtail.core',
 
-    'wagtailcache',
     'modelcluster',
     'taggit',
 
@@ -87,18 +86,8 @@ MIDDLEWARE = [
     'django.contrib.messages.middleware.MessageMiddleware',
     'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'wagtail.contrib.redirects.middleware.RedirectMiddleware',
-    'wagtailcache.cache.FetchFromCacheMiddleware',
 ]
 
-CACHES = {
-    'default': {
-        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
-        'LOCATION': os.path.join(BASE_DIR, 'cache'),
-        'KEY_PREFIX': 'wagtailcache',
-        'TIMEOUT': 3600, # one hour (in seconds)
-    }
-}
-
 X_FRAME_OPTIONS = 'ALLOWALL'
 ROOT_URLCONF = 'ckanorg.urls'
```

#### 11. Re-configure email backend:

```
diff --git a/ckanorg/settings/base.py b/ckanorg/settings/base.py
index be311ca..d0b68dc 100644
--- a/ckanorg/settings/base.py
+++ b/ckanorg/settings/base.py
@@ -192,11 +181,13 @@ WAGTAIL_SITE_NAME = "ckanorg"
 BASE_URL = '<https://ckan.org'>
 
 EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
-EMAIL_HOST = 'email-smtp.eu-central-1.amazonaws.com'
+EMAIL_HOST = 'smtp.gmail.com'
 EMAIL_USE_TLS = True
 EMAIL_PORT = 587
-EMAIL_HOST_USER = 'AKIAUWX42BAVQ3UFZFUU'
-DEFAULT_FROM_EMAIL = 'noreply@ckan.org'
+EMAIL_HOST_USER = 'linkdigitaltest@gmail.com'
+DEFAULT_FROM_EMAIL = 'linkdigitaltest@gmail.com'
+EMAIL_HOST_PASSWORD = 'my-password'
+
 
 ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
 ACCOUNT_CONFIRM_EMAIL_ON_GET = True
```

#### 12. Remove secret info section and add `SECRET_KEY` variable:

```
@@ -216,20 +207,11 @@ ALLOWED_HOSTS = ['*']
 
 WAGTAIL_APPEND_SLASH = False
 
-with open(BASE_DIR + '/../config/secret.txt') as f:
-    data = f.read().strip().split(',')
-    SECRET_KEY = data[0]
-    EMAIL_HOST_PASSWORD = data[1]
-    DB_HOST = data[2]
-    DB_PASS = data[3]
+SECRET_KEY = "qwerty"
```

#### 13. Start the local server: `python manage.py runserver`.

#### 14. Go to: `http://127.0.0.1:8000/`.

You will not see some images, as media folder is empty. If you need them, you can edit pages in admin section and upload your test images.
(To login as admin into the provided sqlite database, contact managers).

#### 15. Use:

`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py collectstatic`

to work with django models and styles.
