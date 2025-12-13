# 🗂️ TaskBoard

**TaskBoard** is a simple task management web application.  

---

## 🚀 App features
- The user can create an account and log in to the application.

- The user can add, edit, and delete tasks.

- The user can view all tasks added to the application.

- The user can search for tasks using a keyword.

- The application includes user pages that display statistics and the tasks created by the user.

- The user can assign importance and due-date to a task.

- The user can contribute to listed tasks.

---

## 👀 Install the app

- Clone repository:

      git clone https://github.com/rasmuskoo/taskboard.git
      cd taskboard
  
- Install the Flask library:
  
      $ pip install flask

- Create virtual environment:

      python3 -m venv venv
      source venv/bin/activate
      venv\Scripts\activate
  
- Create the database tables and add initial data:
  
      $ sqlite3 database.db < schema.sql
  
- You can start the application with:
  
      $ flask run

