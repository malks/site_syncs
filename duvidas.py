#!/usr/bin/python3
import requests
from send_mail import send_mail
from mysql_connection import run_select,run_sql,run_select_array_ret,new_conn

if __name__ == "__main__":
    main_conn=new_conn()
    current_sub=0
    payload_subs=[]
    psub={}

    done_mails=[]
    ecom_mails=[]

    url = "https://webto.salesforce.com/servlet/servlet.WebToCase?encoding=UTF-8"
    element_id = "ab8fab7"

    sql="""
        SELECT 
            v.*
        FROM
            wp_e_submissions_values v
        JOIN
            wp_e_submissions s
        ON
            s.id=v.submission_id
        JOIN
            last_salesforce_sync lss
        ON
            lss.element_id=s.element_id
        AND
            s.id>lss.submission_id
        WHERE
            s.element_id='"""+element_id+"""'
    """

    submissions=run_select(sql,main_conn)


    sql="SELECT email FROM salesforce_synced_mails WHERE synced_at>=DATE_SUB(NOW(), INTERVAL 24 HOUR)"

    nonomails=run_select_array_ret(sql,main_conn)


    for submission in submissions:
        if current_sub!=submission["submission_id"]:
            current_sub=submission["submission_id"]
            if len(psub)>0 and str(psub["email"]) not in nonomails:
                payload_subs.append(psub)
            psub={}
            psub["00N4W00000S0yWk"]=""
            #psub["debug"]="1"
            #psub["debugEmail"]="osmar.gascho@nbwdigital.com.br"
            psub["external"]="1"
            psub["orgid"]="00D4W000007QCau"
            psub["retURL"]="http://lunelli.com.br"
            psub["recordType"]="0124W000000u0SMQAY"
        
        key = str(submission["key"])
        val = str(submission["value"])
        if key == "nome":
            psub["00N4W00000S0yWc"]=val
        elif key == "email":
            psub["email"]=val
        elif key == "telefone":
            psub["00N4W00000S0yWW"]=val[1:3]
            psub["00N4W00000S0yX1"]=val[5:10]+val[11:15]
        elif key == "mensagem":
            psub["description"]=val
        elif key == "field_84d5bbe" and val=="Lojas Virtuais":
            ecom_mails.append(psub["email"])

    payload_subs.append(psub)

    if current_sub!=0:
        update="UPDATE lunelli2.last_salesforce_sync SET submission_id='"+str(current_sub)+"' WHERE element_id='"+element_id+"'"
        run_sql(update,main_conn)

    if len(payload_subs)>0:
        for payload in payload_subs:
            if str(payload["email"]) not in done_mails and str(payload["email"]) not in nonomails:
                if payload["email"] in ecom_mails:
                    send_mail(payload)
                else:
                    response = requests.request("POST", url, data=payload)
                    done_mails.append(str(payload["email"]))
                    print(payload)
                    print(response)

        if len(done_mails)>0:
            for mail in done_mails:
                insert="INSERT INTO lunelli2.salesforce_synced_mails (`email`) VALUES ('"+mail+"') ON DUPLICATE KEY UPDATE synced_at=NOW()"
                run_sql(insert,main_conn)
    else :
        print("Nada novo")
    exit()