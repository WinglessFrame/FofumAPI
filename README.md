## **Forum API project**
### ~~My first django-rest task project~~  😁 
####Django-rest forum API
###This project contains two apps:
* ##### *accounts* - managing JWT registration and authentication
* ##### *Forum* - forum logic
## Cool features:
* #### I used [mptt](https://github.com/django-mptt/django-mptt) for comment model to create reddit-like comments for posts and decrease amount of queries to database
* #### As database i used PostgreSQL
* #### I generated API docs using [drf-spectacular](https://github.com/tfranzel/drf-spectacular) ***They are not perfect as in some places i used weired logic for code (for example, custom token obtain endpoint in accounts app)***
    * #### To open docs go to the _/api/schema/swagger-ui/_ endpoint
    
## Things I would like to add in the future:
- [ ] Cover apps separately  with django, django-rest tests
    
