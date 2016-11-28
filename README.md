# BLOG
login as one of them:

username: ss, password: 12345678 - ordinary user

username: anna, password: 12345678 - superuser

They have much different permissions.

## API urls

127.0.0.1:8000/api/posts/ - list of  posts

.../post/<slug>/edit/ - edit a post if you have permission

.../post/<slug>/delete/ - delete

.../post/<slug>/ - details of the post

.../create/ - create the post

## Searching, example

'''
127.0.0.1:8000/api/posts/?search=<post_name>&q=<username>&ordering=<field_name>
'''

API provides a double search. It's possible to search for name of post, username or content.
You can order queryset by title, id, etc. Or reverse it with '-'.