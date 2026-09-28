from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
import sqlite3, os
DB=os.getenv('SOTERO_DB','sotero_leads.db')
SECRET=os.getenv('SOTERO_WEBHOOK_SECRET','troque-este-segredo')
app=FastAPI(title='Sotero Leads V1')
class Lead(BaseModel):
 external_lead_id: Optional[str]=None; name:str; phone:Optional[str]=None; email:Optional[EmailStr]=None
 city:Optional[str]=None; neighborhood:Optional[str]=None; niche:str='Outros'; product:Optional[str]=None
 intent:Optional[str]=None; budget:Optional[str]=None; income_range:Optional[str]=None; down_payment:Optional[str]=None
 deadline:Optional[str]=None; source:str='Landing Page'; campaign:Optional[str]=None; ad_group:Optional[str]=None
 keyword:Optional[str]=None; consent_contact:bool=False; notes:Optional[str]=None
def conn():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def score(x):
 s=20+(20 if x.consent_contact else 0)+(15 if x.phone else 0)+(5 if x.email else 0)+(10 if x.budget else 0)+(10 if x.income_range and x.income_range!='Prefiro não informar' else 0)+(5 if x.keyword else 0)
 s += 15 if x.deadline=='Até 30 dias' else 10 if x.deadline=='31–90 dias' else 5 if x.deadline=='3–6 meses' else 0
 return min(100,s)
@app.on_event('startup')
def startup():
 c=conn(); c.executescript(open('schema.sql',encoding='utf-8').read()); c.commit(); c.close()
@app.get('/health')
def health(): return {'ok':True}
@app.post('/api/leads')
def create(x:Lead, x_webhook_secret:Optional[str]=Header(default=None)):
 if not x.consent_contact: raise HTTPException(400,'Consentimento de contato não informado')
 if x_webhook_secret and x_webhook_secret!=SECRET: raise HTTPException(401,'Webhook inválido')
 s=score(x); c=conn()
 try:
  cur=c.execute('''INSERT INTO leads(external_lead_id,name,phone,email,city,neighborhood,niche,product,intent,budget,income_range,down_payment,deadline,source,campaign,ad_group,keyword,consent_contact,score,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
   (x.external_lead_id,x.name,x.phone,x.email,x.city,x.neighborhood,x.niche,x.product,x.intent,x.budget,x.income_range,x.down_payment,x.deadline,x.source,x.campaign,x.ad_group,x.keyword,int(x.consent_contact),s,x.notes))
  c.commit(); lid=cur.lastrowid
 except sqlite3.IntegrityError: raise HTTPException(409,'Lead duplicado')
 finally: c.close()
 return {'ok':True,'lead_id':lid,'score':s,'classification':'QUENTE' if s>=80 else 'MORNO' if s>=60 else 'FRIO'}
@app.get('/api/leads')
def list_leads(limit:int=100):
 c=conn(); rows=[dict(r) for r in c.execute('SELECT * FROM leads ORDER BY id DESC LIMIT ?',(min(limit,500),)).fetchall()]; c.close(); return rows
