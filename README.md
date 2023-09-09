# backend_Cahlp


### server login details  
`ssh -i Lightsail-server.pem ubuntu@3.0.184.230` 

### install the required packages  
`chmod +x setup.sh`  
`./setup.sh`  
`source backend_Cahlp-env/bin/activate`  
`pip freeze > requirements.txt`  

### Tutorials  
install mongodb: [Click here](https://www.cherryservers.com/blog/how-to-install-and-start-using-mongodb-on-ubuntu-20-04)  
fix mongdb user auth failed : (click here)[https://stackoverflow.com/questions/35881662/show-dbs-gives-not-authorized-to-execute-command-error]  

### test admin login  
id: demo@gmail.com  
password : demo  

### endpoints  
register endpoint  
`{}/register`  
`required fields : {username}, {email}, {password}, {mobile}`  