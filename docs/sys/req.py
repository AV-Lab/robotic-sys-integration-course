import requests

url = 'http://ec2-54-158-190-205.compute-1.amazonaws.com/robot'
# url = 'https://www.w3schools.com/python/demopage.php'

myobj = {'age': 'somevalue'}


print("calling " + url)
x = requests.post(url, json = myobj)


#object_methods = [method_name for method_name in dir(x)
#                  if callable(getattr(x, method_name))]
# print(object_methods); 

print(x.text)

