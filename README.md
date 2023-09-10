# backend_Cahlp


### server login details  
`ssh -i Lightsail-server.pem ubuntu@3.0.184.230` 

### install the required packages  
`pip freeze > requirements.txt (don't run this)`  
`chmod +x setup.sh`  
`./setup.sh`  
`source backend_Cahlp-env/bin/activate`  


### Tutorials  
install mongodb: [Click here](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)  
create user mongodb: [click here](https://www.cherryservers.com/blog/how-to-install-and-start-using-mongodb-on-ubuntu-20-04)  
fix mongdb user auth failed : [click here](https://stackoverflow.com/questions/35881662/show-dbs-gives-not-authorized-to-execute-command-error) 

### test admin login  
username: demo  
email: demo@gmail.com  
password : demo  
`admin page : {}/admin`  

### endpoints  
endpoint support both : session login , token base login  
for token login you can add Authorization: Token your-auth-token in your header ( you can optain the token from login endpoint)  
register endpoint  
`{}/register,`  
`required fields : {username}, {email}, {password}, {mobile}`  
`method : POST`  
login endpoint  
`{}/login`  
`required fields : {email}, {password}`  
`method : POST`  
device register  
`{}/devreg`  
`required fields : {mac}, {username}`  
`method : GET, login required`  
mac address stream data  
`{mac address}`  
`required fields : {mac}`  
`method : GET, login required`  
sensor data receiver  
`{}/sensors`  
`required fields : {temp}, {ph}, {tds}`  
`method : GET , login required`  
request Sensor Data(latest data)
`{}/sensors/request`  
`required fields : {mac}`  
`method : GET, login required`  
device reset  
`{}/devicereset`  
`required fields : {mac}, {username}`  
`method : GET, login required`
OTA LATEST GET VERSION  
`{}/ota/vcheck=OTAversion`  
`method: GET`  
OTA LATEST VERSION, DOWNLOAD LINK  
`{}/ota/update`  
`method: GET`