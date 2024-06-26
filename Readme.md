# Bluberi Chat Application 

This is team vegetables Info2602 Project. Welcome to Bluberi, a dynamic web chat platform 
facilitating meaningful conversations among users who share common interests, passions, and experiences.

## App Availability

You can view and test the web site at [Site Link](https://bluberi.onrender.com)

## Features
-   Authentication, Authorization and Integrity.

-   Search Functionality - Search for specific chat rooms.

-   Intuitive and engaging user interface.

-   Sending messages in realtime amongst room members.

-   Ability to create read delete and update chat rooms.

## Installation

<details>
<summary>
  <code>There are several ways you can run this application</code>
</summary>

-   [Downloading repository as ZIP](https://github.com/carrot2803/Bluberi/archive/refs/heads/master.zip)
-   Running the following command in a terminal, provided the [GitHub CLI](https://cli.github.com/) has been previously installed:

```sh
git clone https://github.com/carrot2803/Bluberi.git
```

<code>Install Flask and dependencies: </code>

Run the following command to install the required dependencies:

```sh
pip install -r requirements.txt
```

Initialize the app:

```sh
flask init
```

Run the app:

```sh
flask run
```

</details>

## Routes

### Auth Routes

1. <u>/signup</u> [POST]: Signs up a new user.
2. <u>/login</u> [POST]: Logs in the user.
3. <u>/logout</u> [GET]: Logs out the user.

### Chat Routes

1. <u>/chat</u> [GET]: Renders the chat page.
2. <u>/chat/&lt;room_name&gt;</u> [GET]: Renders the chat room with the specified room name.
3. <u>/chat/&lt;room_name&gt;/add_member</u> [POST]: Adds a user to the specified chat room.
4. <u>/chat/&lt;room_name&gt;</u> [POST]: Creates a new chat room with the specified name.
5. <u>/chat/&lt;room_name&gt;</u> [PUT]: Updates the name of the specified chat room.
6. <u>/chat/&lt;room_name&gt;</u> [DELETE]: Deletes the specified chat room.


## Snippets

Landing Page<br/>
![Screenshot 1](https://i.imgur.com/2LgVMzn.png)

Wireframe<br/>
![Screenshot 2](https://i.imgur.com/0hAEHSl.png)

<br/>

View more wireframes at [Figma link](https://www.figma.com/file/fHduUjck8Yksurlyh4t37k/Wireframes?type=design&node-id=0%3A1&mode=design&t=ebXI87cTBHldO5L7-1)
View more UI at [Figma link](https://www.figma.com/file/FXXLagx7B9ORLYrHCw2YWX/Feature-Recording?type=design&node-id=3%3A14&mode=design&t=XDFpj9lJKsMEgHa9-1)