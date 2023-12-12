from .apiRequest import request

healt_check = request('http://localhost:8080/server/actuator/health')
rest_test = request('http://localhost:8080/server/api/core/bitstreamformats?page=0&size=20')
rest_status = request('http://localhost:8080/server/rest')
browses = request('http://localhost:8080/server/api/discover/browses')