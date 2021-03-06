from menu import Menu, MenuItem
from django.urls import reverse

Menu.add_item("main", MenuItem("Profile", reverse('my_profile_page'), weight=0, check=lambda request: request.user.is_authenticated))
Menu.add_item("main", MenuItem("Logout", reverse('logout'), weight=30, check=lambda request: request.user.is_authenticated))
Menu.add_item("main", MenuItem("Register", reverse('register'), weight=20, check=lambda request: not request.user.is_authenticated))
Menu.add_item("main", MenuItem("Login", reverse('login'), weight=30, check=lambda request: not request.user.is_authenticated))

chalkboard_children = (
MenuItem("Owned chalkboards", reverse('own_chalkboard'), weight=0),
MenuItem("Joined chalkboards", reverse('joined_chalkboard'), weight=0),
MenuItem("Public chalkboards", reverse('public_chalkboard'), weight=0)
)

Menu.add_item("main", MenuItem("Chalkboards", reverse('home'), weight=0, children=chalkboard_children, check=lambda request: request.user.is_authenticated))
