from app import es
from app import app
import random





#from flask import Flask, render_template,request,redirect, url_for

r = random.randrange(1,10)

def insert(index, name, email, mobile, password):
    
    b = {
        'name':name,
        'mobile':mobile,
        'email':email,
        'password':password
    }
    res = es.index(index=index, doc_type='registration_info', id=r, body=b)
    return True

    
def search(email,password):
    body = {
        'from':0,
        'size':0,
        'query':{
            'bool':{
                'must':[
                    {
                        'match':{
                            'email':email 
                        }
                        },
                    
                        {
                            'match':{
                                'password':password

                            }
                        }
                    ]
                }    
            }
            
        }
        
    resp = es.search(index='userdata',doc_type='registration_info', body=body)
    hits = resp['hits']['hits']

    if hits:
        for i in hits:
            if i['_source']['email']==email and i['_source']['password']==password:
                return True
                break
            else:
                return False

    else:
        return False  

def search_phone(mobile,password):
    body = {
        'from':0,
        'size':0,
        'query':{
            'bool':{
                'must':[
                    {
                        'match':{
                            'mobile':mobile 
                        }
                        },
                    
                        {
                            'match':{
                                'password':password

                            }
                        }
                    ]
                }    
            }
            
        }
        
    resp = es.search(index='userdata',doc_type='registration_info', body=body)
    hits = resp['hits']['hits']

    if hits:
        for i in hits:
            if i['_source']['mobile']==mobile and i['_source']['password']== password:
                return True
                break
            else:
                return False


    else:
        return False  

def update_email(mobile, password, email): 
    e1  ={
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "mobile.keyword" :mobile
                                    }
                            },
                            {
                                "match": {
                                    "email.keyword": password
                                        
                                    }
                                }
                                ]
                                }
                        },
                        "script" : {
                            "source": "ctx._source.email=params.tag",
                            "lang": "painless",
                            "params": {
                                "tag" : email
                                }
                                }
                                }   
        
    es.update_by_query(index = "emps", doc_type = 'detail', body = e1)
    return True
    

def update_phone(email, password, mobile):
    e1  ={
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "mobile.keyword" :email
                                    }
                            },
                            {
                                "match": {
                                    "email.keyword": password
                                        
                                    }
                                }
                                ]
                                }
                        },
                        "script" : {
                            "source": "ctx._source.mobile=params.tag",
                            "lang": "painless",
                            "params": {
                                "tag" : mobile
                                }
                                }
                                }   
        
    es.update_by_query(index = "emps", doc_type = 'detail', body = e1)
    return True



def delete(email,password):
    
    body={
        "query": {
            "match": {
            "email": email,
            "password":password
            }
        }
        }

    res = es.delete_by_query(index="userdata", doc_type='registration_info', body=body)
    return True
