CKAN: ckan.org website
===
Source code for the ckan.org website

## Information
- Title:  `ckan.org`
- Contributors:  `Alex-Pavlyuk`, `ostyhar`, `rbrtmrtn`, `amercader`, `alexmorev`
- Preview: [https://ckan.org/]()

## Directory Hierarchy
```
|—— blog
|    |—— management
|        |—— commands
|—— ckan_pages
|—— ckanorg
|    |—— settings
|    |—— static
|        |—— css
|        |—— fonts
|        |—— img
|        |—— js
|        |—— scss
|    |—— templates
|        |—— account
|        |—— blog
|        |—— ckan_pages
|        |—— contact
|        |—— events
|        |—— faq
|        |—— home
|        |—— snippets
|        |—— tags
|        |—— wagtailadmin
|        |—— wagtailmetadata
|—— contact
|—— dashboard
|—— events
|—— faq
|—— home
|—— managers
|—— menus
|—— scss
|    |—— base
|    |—— components
|    |—— layout
|    |—— main.scss
|    |—— sections
|    |—— vendor
|—— search
|    |—— templates
|        |—— search
|—— streams
|—— Dockerfile
|—— LICENSE.txt
|—— README.md
|—— cache
|—— media
|—— manage.py
|—— requirements.txt
```

## Install & Dependencies
- Python 3.8 or higher
- Django 4.2
- Wagtail 5.0.2
- all dependencies from `requirements.txt`

### Local environment setup
#### 1. Create a virtual environment and activate it.
```
#:~/wagtail$ python3 -m venv wagenv 
```
```
#:~/wagtail$ source wagenv/bin/activate 
```

#### 2. Clone repository and cd to the folder:

```
(wagenv) #:~/wagtail$ git clone https://github.com/ckan/ckan.org.git
```

#### 3. For local development: if will use sqlite db, comment `psycopg2` in `requirements.txt`.

#### 4. Install `wheel` library 
```
(wagenv) #:~/wagtail$ pip install wheel
```

#### 5. Install all required dependencies from `requirements.txt` in project root folder. Be aware about versions of these dependencies!!!
```
(wagenv) #:~/wagtail$ pip install -r requirements.txt
```

#### 6. Remove `cache` and `media` links from ckan.org folder.

#### 7. Create `media` folder in the `ckan.org` directory.

#### 8. Create `static` folder in the `ckan.org` directory and run `python manage.py collectstatic`.

#### 9. You can use sqlite db for local development, switch it in the settings:

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
NOTE. Wagtail 5.0.2 uses PostgreSQL 12 or later

#### 10. To not create all pages from the scratch you can use existing dummy sqlite database.
(Ask managers for `db.sqlite3` file and copy it into the `ckan.org` folder).
Otherwise run: `python manage.py makemigrations; python manage.py migrate`.

#### 11. We can disable wagtail cache for local development:

```
diff --git a/ckanorg/settings/base.py b/ckanorg/settings/base.py
index be311ca..3837822 100644
--- a/ckanorg/settings/base.py
+++ b/ckanorg/settings/base.py
@@ -49,7 +49,6 @@ INSTALLED_APPS = [
     'wagtail.admin',

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

#### 12. Re-configure email backend:

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

#### 13. Remove secret info section and add `SECRET_KEY` variable:

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

#### 14. Start the local server: `python manage.py runserver`.

#### 15. Go to: `http://127.0.0.1:8000/`.

You will not see some images, as media folder is empty. If you need them, you can edit pages in admin section and upload your test images.
(To login as admin into the provided sqlite database, contact managers).

#### 16. Use:

`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py collectstatic`

to work with django models and styles.

#### 17. Populate reference table:

Populate the references table and ensure that usage counts for images, documents and snippets are displayed accurately

`python manage.py rebuild_references_index`

## Instructions on how to deploy changes
1. Create a new fork from `main` branch of the repository `https://github.com/ckan/ckan.org`. A fork is a copy of a repository. Forking a repository allows you to freely experiment with changes without affecting the original project. So all tasks that you push are going to our fork repository, not the main one.
If it was done earlier be sure you have cloned `main` branch of the repository with last updates.
2. Create a new branch from `main` branch of your forked repository and name it as "`[task key] / [task summary]`".
3. Make all required changes.
4. Push your finished task code to your fork repository (cloned).
5. Deploy your changes to Development environment by making a Pull Request to `develop` branch of original repository so the PO (Product owner) can merge it after he/she will test the work done on Development.

## Code Details
### Tested Platform
- software
  ```
  OS: Ubuntu 22.04.2 LTS (Jammy)
  Python: 3.8.17
  ```
- hardware
  ```
  CPU: Intel® Core™ i7
  GPU: Intel® HD Graphics 4000
  ```

## References
- [site](https://ckan.org/)
- [readme](https://github.com/ckan/ckan.org#readme)
- [code](https://github.com/ckan/ckan.org)
  
## License
This material is copyright (c) 2006-2018 Open Knowledge Foundation and contributors.

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0 whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html 
