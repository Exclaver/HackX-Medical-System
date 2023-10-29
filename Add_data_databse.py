# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# # import speechrecognition as sp

# # file_name=sp.speech()

# cred = credentials.Certificate("ServiceAccountKey.json")
# firebase_admin.initialize_app(cred,{
#     'databaseURL':"https://contactlessvending-default-rtdb.firebaseio.com/"
# })
# ref= db.reference('Students')
# data={
#     "Devansh":
#         {
#             "name":"Devansh Matha",
#             "Credits":69
#         },
#     "Deepak":
#     {
#         "name":"Deepak",
#         "Credits":70
#     }
# }
# for key,value in data.items():
#     ref.child(key).update(value)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://hackx-medical-system-default-rtdb.firebaseio.com/"
})

ref=db.reference('Medical')

data={
    "Doctors":{
    "1234":
        {
            "name":"Gustavo Fring",
            "Position":"Senior Doctor",
            "specialization":"cardiac",
            "Age":"69",
            "Hospital":"AIMS"
        },
    "4321":
        {
        "name":"Gustavo Fring",
        "Position":"Senior Doctor",
        "specialization":"cardiac",
        "Age":"69",
        "Hospital":"AIMS"
    }},
    "patent":{
        "4321":{
        "name":"jesse Pinkman",
        "Disease":"fever",
        "age":"69",
        "Status":"Cured"
    },
     "4321":{
        "name":"jesse Pinkman",
        "Disease":"fever",
        "age":"69",
        "Status":"Cured"}}
}
for key,value in data.items():
    ref.child(key).set(value)


