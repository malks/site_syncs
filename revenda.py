#!/usr/bin/python3
import requests
from mysql_connection import run_select,run_sql,run_select_array_ret,new_conn

if __name__ == "__main__":
    main_conn=new_conn()
    current_sub=0
    payload_subs=[]
    psub={}

    url = "https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8"
    element_id = "e25b175"

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

    for submission in submissions:
        if current_sub!=submission["submission_id"]:
            current_sub=submission["submission_id"]
            if len(psub)>0:
                payload_subs.append(psub)
            psub={}
            psub["00N4W00000S0yWk"]=""
            psub["debug"]="1"
            psub["debugEmail"]="osmar.gascho@nbwdigital.com.br"
            psub["external"]="1"
            psub["lead_source"]="Site"
            psub["oid"]="00D4W000007QCau"
            psub["retURL"]="http://lunelli.com.br"
            psub["recordType"]="0124W000000u0SMQAY"
        
        key = str(submission["key"])
        val = str(submission["value"])
        if key == "nome":
            psub["first_name"]=val.split(" ")[0]
            psub["last_name"]=val.split(" ")[-1]
        elif key == "email":
            psub["00N4W00000S0yaO"]=val
        elif key == "telefone":
            #psub["00N4W00000S0yah"]=val[1:3]
            #psub["phone"]=val[5:10]+val[11:-1]
            psub["00N4W00000S0yaK"]=val[1:3]
            psub["mobile"]=val[5:10]+val[11:15]
        elif key == "mensagem":
            psub["00N4W00000S0yae"]=val
        elif key == "marcas":
            if val.find(",")<0:
                psub["00N4W00000S0ya8"]=val
            else:
                psub["00N4W00000S0ya8"]=[item.strip() for item in val.split(",")]
        elif key == "tipo_pessoa":
            psub["00N4W00000S0yag"]=val
        elif key == "lojista":
            psub["company"]=val
        elif key == "cnpj":
            psub["00N4W00000S0yaA"]=val
        elif key == "cep":
            psub["00N4W00000S0yai"]=val.replace("-","")
        elif key == "rev_rua":
            psub["00N4W00000S0yaq"]=val
        elif key == "rev_bairro":
            psub["00N4W00000S0yab"]=val
        elif key == "rev_uf":
            psub["00N4W00000S0yao"]=val
        elif key == "rev_cidade":
            psub["00N4W00000S0yaE"]=val
        elif key == "campo_site":
            psub["url"]=val
        elif key == "campo_insta":
            psub["00N4W00000S0yaV"]=val
        elif key == "campo_fb":
            psub["00N4W00000S0yaQ"]=val
        elif key == "field_02dfc81":
            if val.find(",")<0:
                psub["00N4W00000S0yaJ"]=val
            else:
                psub["00N4W00000S0yaJ"]=[item.strip() for item in val.split(",")]
            
    payload_subs.append(psub)
            
    if current_sub!=0:
        update="UPDATE lunelli2.last_salesforce_sync SET submission_id='"+str(current_sub)+"' WHERE element_id='"+element_id+"'"
        run_sql(update,main_conn)

    if len(payload_subs)>0:
        for payload in payload_subs:
            response = requests.request("POST", url, data=payload)
            print(payload)
            print(response)
    else :
        print("Nada novo")
    exit()