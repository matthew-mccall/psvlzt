# Static files folder

Place your static files (JavaScript, CSS, images, etc.) in this folder. Then
load them in your templates using the static template tag.

```html

{% load static %}


<script src="{% static 'custom_ui_tutorial_app/some_script.js' %}"></script>
```

See
[Part 6 of the Django tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial06/)
for more information.
