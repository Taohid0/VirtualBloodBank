from django.shortcuts import render
from  django.http import HttpResponse
from django.views import generic
from django.views.decorators import csrf
from django.views import decorators
import json
from django.utils.decorators import method_decorator
import requests
from bloodBank import models as bloodBankModels
from datetime import date,datetime
from bloodBank import utils

ACCESS_TOKEN ="EAAG7tMnXamcBAAvoBIW616fVeSsWxptV8czcSj1HRsjW5itD2UOTJropoRUgnt9C4jorsrdw1wAYsxaqAppccixS2QNqzuXiAwT4Td7hsm4AXHvbneDAhrIxDhNk9gBp61qRanwGYu1vZBV3kWwF2vLRXQRG7BVJAbKaFgKuZAhLM8dI9v"


def send_message(fbid,received_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":received_message}})
    status = requests.post(post_message_url,headers={"Content-Type":"application/json"},data = response_msg)
    print(status.json())


def update_info_for_registration(fbid,information):


    if information[4].strip()[0].lower()!='n' and utils.check_phone_number(information[4].strip()==False):
        answer = "অনুগ্রহ করে সঠিক মোবাইল নাম্বার দিন । "
        return answer

    try:
        to_update_info = bloodBankModels.Donor.objects.filter(user_id=fbid)
        for i in to_update_info:
            #i.name = information[1].strip()
            i.blood_group = information[1].replace(" ", "").strip()
            i.blood_group = i.blood_group.upper().strip()
            i.district = information[2].strip()
            if (information[3][0].lower() != 'n'):
                i.date = information[3].strip()
            if (information[4].strip()[0].lower()!= "n"):
                i.contact_number = information[4].strip().replace(" ","").replace("-","")
            i.isDeleted = False
            i.save()
            answer = "আপনি পূর্বে Registration করেছেন ।\n" \
                     "তাই আপনার সম্প্রতি দেয়া তথ্য দিয়ে আপনার পূর্বের সকল তথ্য Update করা হয়েছে। \n" \
                     "আপনার সকল তথ্য দেখতে My info লিখে send করুন, ধন্যবাদ। "
            return  answer
    except Exception as err:
        print(err)
        answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
        flag = True
        return  answer

def post_facebook_message(fbid,received_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN
    flag = False
    answer = "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
    try:


        information = received_message.strip().split("\n")

        if(received_message.lower().strip()=="help"):
            answer = "Donor হিসেবে Registration করতে Registration লিখে send করুন। \n\n" \
                     "আপনার তথ্য জানতে My info লিখে Send করুন। \n\n" \
                     "রক্তদানের তারিখ Update করতে চাইলে Update date of donation লিখে send করুন।\n\n"  \
                     "আপনার অন্যান্য তথ্য Update করতে চাইলে Update info লিখে send করুন।\n\n" \
                     "Donor হিসেবে আপনার registration বাতিল করতে চাইলে Unregister my profile লিখে send করুন।\n\n" \
                     "রক্তের Donor খুঁজতে চাইলে Search donor লিখে send করুন।\n\n" \
                     "কোন ফোন নাম্বারের বিষয়ে complain করতে চাইলে, \ncomplain\nPhone number\nyour complain message\nলিখে send করুন।\n\n" \
                     "অন্য কোন তথ্য আমাদেরকে জানাতে চাইলে, \nother\nyour message\nলিখে send করুন,\n" \
                     "ধন্যবাদ । "
        elif (received_message.lower().strip()== "registration" ):

            answer = "(অনুগ্রহ করে কোন ভুয়া তথ্য দিবেন না । " \
                     "অন্যথায়, আপনার বিরুদ্ধে আইনানুগ ব্যবস্থা নেয়া হবে)\n\n"\
                     "Registration করার জন্য নিচের তথ্য নির্দিষ্ট ফরম্যাটে লিখে send করুন \n\n" \
                     "Register\n" \
                     "" \
                     "Blood group \n" \
                     "District name\n" \
                     "Date of last donation (year-month-day ফরম্যাটে লিখুন, যদি আগে কখনো রক্ত না দিয়ে থাকেন তাহলে NA লিখুন)\n" \
                     "Mobile number (আপনার মোবাইল নাম্বার রক্তদান ছাড়া অন্য কোন উদ্দেশ্য ব্যবহার করা হবে না " \
                     "এবং গোপন রাখা হবে । " \
                     "Mobile number না দিতে চাইলে NA লিখুন ) " \
                     "যেমন, \n\n" \
                     "Register\n" \
                     "" \
                     "O-\n" \
                     "Khulna\n"\
                     "2016-12-25\n" \
                     "0**********\n\n"

        elif (received_message.lower().strip()=="my info"):

            try:

                donor_info = bloodBankModels.Donor.objects.filter(user_id=fbid)

                if(len(donor_info)==0):
                    seekers_info = bloodBankModels.Blood_seeker.objects.filter(user_id=fbid)
                    answer = "রক্তদাতা হিসেবে আপনি এখনো Virtual Blood Bank এ registration করেননি \n" \
                             "আপনি মোট "+str(len(seekers_info))+ " বার রক্ত চেয়ে আবেদন করেছেন । "
                else:
                    #name = donor_info[0].name
                    group=donor_info[0].blood_group
                    district = donor_info[0].district
                    dt = donor_info[0].date
                    number = donor_info[0].contact_number
                    activeness = "Inactive"
                    if(donor_info[0].isDeleted==False):
                        activeness = "Active"


                    seekers_info = bloodBankModels.Blood_seeker.objects.filter(user_id=fbid)
                    counter = len(seekers_info)

                    answer = "আপনার তথ্য, \n" \
                             "" \
                             "Blood group : "+group+"\n" \
                              "District : "+district+"\n" \
                              "Last date of donation : "+str(dt)+"\n" \
                                "Contact Number : "+str(number)+"\n" \
                                "Status : "+activeness+"\n" \
                                "আপনি মোট "+str(counter)+ " বার রক্ত চেয়ে আবেদন করেছেন । "
            except Exception as err:
                answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "

        elif (received_message.lower().strip()=="update date of donation"):

            answer = "আপনার বিগত রক্তদানের তারিখ update করার জন্য নিচের তথ্য নির্দিষ্ট format এ  লিখে send করুন \n\n" \
                     "Update date\n"\
                     "Date of last donation (year-month-day ফরম্যাটে লিখুন)" \
                     "\nযেমন,\n" \
                     "Update date\n" \
                     "2017-5-5"

        elif (received_message.lower().strip()=="update info"):

            answer = "আপনার তথ্য Update করার জন্য  নিচের তথ্য নির্দিষ্ট ফরম্যাটে লিখে send করুন। \n\n" \
                     "Update my info\n" \
                     "" \
                     "blood group\n" \
                     "District name\n" \
                     "Date of last donation (year-month-day ফরম্যাটে লিখুন, যদি আগে কখনো রক্ত না দিয়ে থাকেন তাহলে NA লিখুন)\n"\
                     "Mobile number (আপনার ফোন নাম্বার রক্তদান ছাড়া অন্য কোন উদ্দেশ্য ব্যবহার করা হবে না " \
                     "এবং গোপন রাখা হবে । " \
                     "Mobile number না দিতে চাইলে NA লিখুন)\nযেমন, \n\n" \
                     "Update my info\n" \
                     "" \
                     "O+\n" \
                     "Dhaka\n" \
                     "2017-1-1\n" \
                     "0**********\n"


        elif (received_message.lower().strip()=="search donor"):

            answer = "(অনুগ্রহ করে কোন ভুয়া তথ্য দিবেন না বা অপ্রয়োজনে রক্তের জন্য আবেদন করবেন না ।\n" \
                     "অন্যথায়, আপনার বিরুদ্ধে আইনানুগ ব্যবস্থা নেয়া হবে)\n\n" \
                     "Blood Donor খোঁজার জন্য নিচের format এ মেসেজ দিন।\n\n" \
                     "Need\n" \
                     "Blood group\n" \
                     "Clinic/Hospital name (যেখানে রক্ত সংগ্রহ করা হবে)\n"\
                     "District name\n" \
                     "Date (year-month-day ফরম্যাটে লিখুন)\n" \
                     "Mobile number\n" \
                     "রক্তদাতা যদি দূরে থাকেন তাহলে তার নিকটবর্তী কোন হাসপাতালে তিনি রক্ত দিতে চাইলে আপনি সেখান থেকে রক্ত " \
                     "সংগ্রহ করতে আগ্রহী হলে YES লিখুন, অন্যথায় NO লিখুন। \nযেমন,\n\n" \
                     "Need\n" \
                     "O-\n" \
                     "Dhaka Medical College Hospital\n" \
                     "Dhaka\n" \
                     "2017-1-1 \n" \
                     "0**********\n" \
                     "YES"

        elif (received_message.lower().strip()=="unregister my profile"):

            try:
                unregister_objects = bloodBankModels.Donor.objects.filter(user_id=fbid)[0]
                unregister_objects.isDeleted = True
                unregister_objects.save()
                answer = "আপনার প্রোফাইলটি সফলভাবে unregistered করা হয়েছে । আপনি প্রয়োজনে পুনরায় registration করতে পারবে, ধন্যবাদ ।"
            except Exception as err:
                answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন। ধন্যবাদ । "

       # elif(received_message.lower().strip()=="other"):
            #answer = "other message"

        elif (information[0].lower().strip()=="register"):
            donor_object = bloodBankModels.Donor()

            all_donors = bloodBankModels.Donor.objects.all()
            donor_id = list()
            for i in all_donors:
                donor_id.append(i.user_id)

            test_flag = False

            if(len(information)!=5):
                flag = True
            elif fbid in donor_id:
                answer = update_info_for_registration(fbid,information)

            else:
                information[4] = information[4].replace(" ", "").replace("-", "")
                if information[4].strip()[0].lower()!='n' and utils.check_phone_number(information[4])==False:
                    answer = "অনুগ্রহ করে সঠিক মোবাইল নাম্বার দিন । "
                else:
                    try:
                        donor_object.user_id = fbid
                        #donor_object.name = information[1].strip()
                        donor_object.blood_group = information[1].replace(" ","")
                        donor_object.blood_group = donor_object.blood_group.upper().strip()
                        donor_object.district = information[2].strip().lower()
                        if(information[3][0].lower()!='n'):
                            donor_object.date = information[3].strip()
                        if(information[4][0].lower().strip()!='n'):
                            donor_object.contact_number = information[4].strip()
                        else:
                            donor_object.contact_number = information[4].strip()

                        donor_object.save()
                        answer = "অভিনন্দন, আপনার Registration সফলভাবে সম্পন্ন হয়েছে ।\n" \
                                 "আপনার সকল তথ্য দেখতে My info লিখে send করুন। "

                        district_object = bloodBankModels.District_info.objects.filter(district_name=information[2].strip())

                        if(len(district_object)==0):
                            new_district_object = bloodBankModels.District_info()
                            new_district_object.district_name = information[2].strip().lower()
                            new_district_object.donor_counter= 1
                            new_district_object.save()

                        else:
                            district_object[0].donor_counter= district_object[0].donor_counter+1
                            district_object[0].save()

                        blood_info_object = bloodBankModels.Blood_group_info.objects.filter(blood_group=information[1].replace(" ","").upper())

                        if (len(blood_info_object)==0):
                            new_blood_info = bloodBankModels.Blood_group_info()
                            new_blood_info.blood_group = information[1].replace(" ","").upper()
                            new_blood_info.donor_counter = 1
                            new_blood_info.save()
                        else:
                            blood_info_object[0].donor_counter = blood_info_object[0].donor_counter+1
                            blood_info_object[0].save()

                    except Exception as err:
                        answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                     "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
                        flag = True



        elif(information[0].lower().strip()=="update date"):

            try:
                to_update  = bloodBankModels.Donor.objects.filter(user_id=fbid)

                for i in to_update:
                    i.date = information[1].replace(" ","").strip()
                    i.save()
                    answer = "আপনার তথ্য সফলভাবে update করা হয়েছে, ধন্যবাদ। "
            except Exception as err:
                answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
                print(err)
                flag = True


        elif (information[0].lower().strip()=="update my info"):
            if(len(information)!=5):
                flag = True
            else:
                information[4] = information[4].replace(" ", "").replace("-", "")
                if information[4].strip()[0].lower()!='n' and utils.check_phone_number(information[4])==False:
                    answer = "অনুগ্রহ করে সঠিক মোবাইল নাম্বার দিন । "
                else:

                    try:
                        to_update_info  = bloodBankModels.Donor.objects.filter(user_id=fbid)
                        for i in to_update_info:
                            #i.name = information[1].strip()
                            i.blood_group = information[1].replace(" ","")
                            i.blood_group=i.blood_group.upper().strip()
                            i.district = information[2].strip()
                            if(information[3][0].lower()!='n'):
                                i.date = information[3].strip()
                            if(information[4].lower().strip()[0]!="n"):
                                i.contact_number = information[4].strip().replace(" ","").replace("-","")
                            i.save()
                            answer = "আপনার সকল তথ্য সঠিকভাবে update করা হয়েছে, ধন্যবাদ।"
                    except Exception as err:
                        answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                     "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
                        print(err)
                        flag = True




        elif (information[0].lower().strip()=="need"):

            if(len(information)!=7):
                flag = True
            else:
                dateformat = information[4].strip().split("-")
                information[5] =information[5].replace(" ","").replace("-","")
                if information[5].strip()[5].lower()!='n' and utils.check_phone_number(information[5])==False:
                    answer = "অনুগ্রহ করে সঠিক মোবাইল নাম্বার দিন । "

                elif utils.check_date(dateformat)==False:
                    answer = "অনুগ্রহ করে সঠিকভাবে Date লিখুন । "

                else:

                    try:
                        blocked_list=bloodBankModels.Blocked_List.objects.filter(phone_number=information[5].replace(" ","").replace("-","") ) or \
                            bloodBankModels.Blocked_List.objects.filter(user_id=fbid)
                        blocked_contacts = list()
                        blocked_user_id = list()
                        for i in blocked_list:
                            blocked_contacts.append(i.phone_number.replace(" ","").replace("-",""))

                        for i in blocked_list:
                            blocked_user_id.append(i.user_id)

                        #print(blocked_contacts,str(fbid),str(information[5]),blocked_user_id)
                        if (fbid in blocked_user_id or information[5].strip().replace(" ","").replace("-","") in blocked_contacts):
                            answer = "দুঃখিত আপনার এই প্রোফাইল বা ফোন নাম্বার টি blocked listed"
                        else:
                            donors = bloodBankModels.Donor.objects.filter(blood_group=information[1].upper().strip())
                            print(donors)
                            seekers = bloodBankModels.Blood_seeker()
                            seekers.phone_number= information[5].strip().replace(" ","").replace("-","")
                            seekers.user_id = fbid
                            seekers.save()
                            sent = list()
                            counter = 0
                            for i in donors:
                                today= datetime.today()
                                year_today =today.year
                                month_today = today.month
                                day_today =today.day
                                difference = date(2017,1,1)-date(2016,1,1)
                                optional = ""

                                if(information[6].lower().strip()[0]=='y'):
                                    optional = "\nআপনি দূরে থাকলে প্রয়োজনে আপনার সুবিধা অনুযায়ী নিকটবর্তী কোন হাসপাতালে রক্ত সংগ্রহ করা হবে । "
                                if(i.date!=None):
                                    difference = date(year_today,month_today,day_today)-date(i.date.year,i.date.month,i.date.day)
                                    print(difference.days)
                                if(abs(difference.days)>=90 and information[3].lower().strip()==i.district.lower().strip() and i.isDeleted==False and i.user_id not in sent):
                                    message =                 " একজন রোগীর জন্য রক্ত প্রয়োজন ।\n" \
                                                               "Blood Group : "+information[1].upper().strip()+"\n" \
                                                               "Place : "+information[2].strip()+"\n" \
                                                               "District : "+information[3].strip()+"\n" \
                                                                "Date : "+information[4].strip()+"\n" \
                                                                "Contact Number : "+information[5].strip()+"\n" \
                                                                ""+optional.strip()+"\n" \
                                                                "আপনার পক্ষে রক্ত দেয়া সম্ভব হলে অনুগ্রহ করে এই নাম্বারে যোগাযোগ করে " \
                                                                            "রক্ত দিতে অনুরোধ করা হল।\n" \
                                                                            "নিজে রক্ত দিন, অন্যকে রক্ত দিতে উৎসাহিত করুন, ধন্যবাদ । "
                                    counter = counter+1
                                    sent.append(i.user_id)
                                    send_message(i.user_id,message)

                            if(counter>0):
                                answer = str(counter) + " জনকে রক্ত দানের জন্য অনুরোধ করা হয়েছে ।\nতাদের পক্ষে রক্ত দেয়া সম্ভব হলে" \
                                                             " আপনার ফোনে যোগাযোগ করা হবে ।\n\nকেউ রক্ত দিলে বা" \
                                                             " virtual blood bank থেকে আপনি উপকৃত হলে আমাদের পেজে পোস্ট করে জানাতে" \
                                                             "" \
                                                             " অনুরোধ করা হল । ধন্যবাদ ।"
                            else:
                                answer = "দুঃখিত, এই মুহুর্তে আপনার জেলায় "+information[1].upper()+ " গ্রুপের কোন রক্তদাতার তথ্য আমাদের কাছে নেই ।\n" \
                                          "virtual blood bank থেকে আপনি উপকৃত হলে আমাদের পেজে পোস্ট করে জানাতে " \
                                                                                            "অনুরোধ করা হলো, ধন্যবাদ । "

                    except Exception as err:
                        answer  =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                     "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
                        flag = True
                        print(err)



        elif (information[0].lower().strip()=="complain"):
            if(len(information)<3):
                flag = True
            else:
                try:
                    answer = "আপনার সমস্যার জন্য আমরা আন্তরিকভাবে দুঃখিত।\n" \
                             "আপনার অভিযোগটি খুব গুরুত্বের সাথে বিবেচনা করা হচ্ছে।" \
                             "এই নাম্বার এবং এই ব্যবহারকারীকে সাময়িকভাবে Blocked listed করা হয়েছে।\n" \
                             "খুব দ্রুতই আপনার সমস্যার সমাধান করা হবে, ধন্যবাদ। "
                    complain_object = bloodBankModels.Blocked_List()
                    to_be_blocked_id = bloodBankModels.Blood_seeker.objects.filter(phone_number=information[1].strip().replace(" ","").replace("-",""))
                    ids = list()
                    for i in to_be_blocked_id:
                        ids.append(i.user_id)
                    if(len(ids)>0):
                        for i in ids:
                            complain_object.user_id = i
                            complain_object.phone_number = information[1].strip().replace(" ","").replace("-","")
                            complain_object.save()
                    print(len(ids))
                    myself = "1470158926379675"
                    send_message(myself, "Complain From " + fbid + " to " + information[1].strip()+" \nComplain \n"+str(information[2:]))
                except Exception as err:
                    answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
                    flag = True
                    print(err)

        elif (information[0].lower().strip()=="other" or information[0].lower().strip()=="others"):
            myself ="1470158926379675"
            send_message(myself,"Other message From "+fbid + " \n" +str(information[1:]))
            answer = "আপনার মূল্যবান মতামতের জন্য ধন্যবাদ ।\n" \
                     "নিজে রক্ত দিন, অন্যকে রক্ত দিতে উৎসাহিত করুন ।"

        else:
            flag = True
            answer = "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                     "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন ।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "

        '''if(flag==True):
            answer = "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                     "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন । \nিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "'''
    except Exception as err:
        answer =  "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
        print(err)

    response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":answer}})
    status = requests.post(post_message_url,headers={"Content-Type":"application/json"},data = response_msg)
    print(status.json())

class blood_view_class(generic.View):
    def get(self,request,*args,**kwargs):
        if self.request.GET["hub.verify_token"]=="4321":
            return HttpResponse(self.request.GET["hub.challenge"])
        else:
            return HttpResponse ("Error, invalid token")

    @method_decorator(csrf.csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self,request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        sender = ""
        try:

            incoming_message = json.loads(self.request.body.decode("utf-8"))

            for entry in incoming_message["entry"]:
                for message in entry["messaging"]:
                    if "message" in message:
                        sender = message["sender"]["id"]
                        #print(message)
                        post_facebook_message(message["sender"]["id"],message["message"]["text"])
                        print(message)
        except Exception as err:
            text = "অনুগ্রহ করে নির্দিষ্ট format এ message দিন ।\nনির্দিষ্ট format ব্যতিত অন্য কোন format এ message দিলে আপনি " \
                 "কাঙ্ক্ষিত সেবা থেকে বঞ্চিত হতে পারেন ।\nবিস্তারিত জানতে পেজে help লিখে message দিন । ধন্যবাদ । "
            send_message(sender,text)
        return HttpResponse()