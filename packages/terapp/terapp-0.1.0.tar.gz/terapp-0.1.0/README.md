# `Ter` CLI Framework

[![Author](https://img.shields.io/badge/author-Ming_doan-red.svg)]()
[![Version](https://img.shields.io/badge/version-alpha_0.0.1-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

Ter is the CLI Framework that will build a CLI application with cool syntax which will amaze your school coding projects.

In Ter, we are strongly amaze the syntax and terminologies of other modern UI framework. Our main purpose of creating this framework is to make the terminal app more interactive and fancy with pages, command prompt, and built-in UI.

## Main concept of `Ter`

Everything that you can see on the terminal screen is the result of `print` statement in Python. Then the screen is paused to wait for the user command by `input` statement. We consider everytime that printing out and waiting for input for future change is a `state` (inspired by React).

Each state includes:

> clear screen -> render component -> pause program -> run logic

The state will continuously loop until the `exit` method is called.

- Clear screen phase: Create your terminal and ready to print new content.
- Render component phase: Render your content with new data. (State is changed)
- Pause programm phase: Pause program to listen input from user.
- Run logic phase: Execute logic based on user input to change the data.

## Quick start

- Install `terapp` in Python package.

```bash
$ pip install terapp
```

- Create a simple `Ter` app

```python
# Import libs
import terapp

# Create app instance
app = terapp.Ter()

# Define Screen
class MyScreen(ter.Component):
    def __init__(self):
        self.count = 0

    # Override render method
    def render(self, context):
        print("Counting app")
        print(self.count) # Print count value

    # Override prompt method
    def prompt(self):
        return "Enter your number: "

    # Override logic method
    def logic(self, command, context):
        # Add user number to count
        self.count += int(command)

# Add Screen to route. Ter will get the first route as init screen
app.register_routes({
    'home': MyScreen
})

# Begin loop of your app
app.run()
```

## Folder Structure

Ter is strongly recommending uses organize app's files. By using this structure, your app is more scalable and easy to maintain in the future.

```
your_folder
    └ screens
    |    └ your_screen.py
    └ state
    |    └ your_state.py
    └ main.py
```

- screens folder contains all your screen of your app.
- state folder contains all global state of your app. (Inspired by Redux)
- main.py contains the `app` instance and some config for your app.

## Ter App

Ter manages every things in the app instance. Include all the screen in your app.

```python
from terapp import Ter
app = Ter()
```

Ter provides the Config class which includes all the custom config of app. Ter config includes:

- `default_pause_message` (str): If you don't override the `prompt` method, this string will be displayed instead.

```python
from terapp import Ter, Config
app = Ter(
    config=Config(default_pause_message="Press enter to continue...")
)
# Or you can provide config by config method
app.config(
    config=Config(default_pause_message="Press enter to continue...")
)
```

## Component

In ter, we define every screen is a component which always have methods:

- `render` (required): This method will run first and do all code inside it before program will be pause.
- `prompt` (optional): This method must return a string for a user prompt message. If not, the prompt message will use `default_pause_message` instead.
- `logic` (optional): This method will run after the user complete typing the prompt to run your desired logic before the new loop.

```python
from terapp import Component

class YourScreen(Component):
    def __init__(self):
        # Define your local variable here
        self.local_variable = ...

    # Render method
    def render(self, context):
        # Print something
        ...

    # Prompt method, optional
    def prompt(self):
        return "Some message"

    # Logic method, optional
    def logic(self, command, context):
        # Do somthing with use input at command params
        ...
```

To add your screen into app, register routes in `main.py` file

```python
# Import YourScreen class from screens folder
from screens import YourScreen

# The register_routes method requires a dictionary of Components
app.register_routes({
    'identify_of_route': YourScreen
})
```

## Navigation

Consider we have 2 screens as below in `main.py` file.

```python
# Import Screens class from screens folder
from screens import Screen1, Screen2

# The register_routes method requires a dictionary of Components
app.register_routes({
    's1': Screen1
    's2': Screen2
})
```

We want to navigate from `Screen1` to `Screen2` at logic method of `Screen1`

```python
class Screen1:
    ...

    def logic(self, command, context):
        # Navigate to Screen 2 if user type `2`
        if command == '2':
            # Use navigate method of Context and passing the key of Screen
            context.navigate('s2')
```

## Global State

The term of state management is strongly inspired by Redux library in React framework. It stores the value of and be accessing in diffirent Screens. Unlike the local varable that we define at the `__init__` method of a Screen which only accessed inside the class, this state can be store, update anywhere in your app.

Create your state at `state/your_state.py` file.

```python
from terapp import State

# Initialize store instance
store = State(init_state=0)

# Create a name for an event and this action
store.reducers(
    reducer='increase_count',
    action=lambda state, payload: state += payload
)
```

Import the store instance into the Screen

```python
from state.your_state import store

class Screen:
    ...

    def logic(self, command, context):
        # Increase the count value
        # Use dispatch method, access by the event name and passing new data
        store.dispatch(
            reducer='increase_count',
            payload=int(command)
        )
```

The `init_state` can be a dictionary or anything

```python
store = State(init_state={
    'name': "Ming Doan",
    'age': 20
})

store.reducers(
    reducer='change_name',
    action=lambda state, payload: {
        'name': payload # Update name
    }
)
```

## High level UI

Ter is providing some quick UI in terminal app.

- Header

```python
from terapp import Header

class Screen:
    ...

    def render(self, contex):
        print(Header(context, "This is header"))
```

## Future development

Ter was only the alpha version, the future update will arrive soon. (Depend on Author 😁🙌)

Author & Maintainer **Ming Doan**

- Email: quangminh57dng@gmail.com
- Github: https://github.com/Ming-doan
- Facebook: https://www.facebook.com/ming.doan/
