# film-review

## Deployment

The project was deployed on Heroku using the following steps:

### Within VS Code:

- Install gunicorn for use as a Web Server Gateway Interface (WSGI)
- Create a Procfile to specify gunicorn as the WSGI when the project is deloyed on Heroku
- Update ALLOWED_HOSTS in settings.py with the project host's details
- Git add, commit and push

### On Heroku

- Create and name a new app using European Common Runtime
- From within 'Settings', 'Reveal Config Vars' and add sensitive information
- From within 'Deploy', select 'GitHub', search for the repository to connect to, then select 'Connect'
- Scroll to find the section titled 'Manual Deply', select 'Main' from the dropdown menu, then select 'Deploy Branch'
- Once the build has finished, select 'Open App' to view the deployed project
