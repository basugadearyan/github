import tkinter as tk
from tkinter import ttk,messagebox
from datetime import date,datetime
import calendar
from database import setup_database,get_connection

class App:
 def __init__(self,r):
  self.r=r;r.title("Daily Expenses Tracking System");r.geometry("1200x750")
  self.ensure_modes();self.build();self.load_all();self.refresh()
 def db(self): return get_connection()
 def ensure_modes(self):
  c=self.db();q=c.cursor()
  q.execute("""CREATE TABLE IF NOT EXISTS payment_modes(
   payment_mode_id INT AUTO_INCREMENT PRIMARY KEY,
   mode_name VARCHAR(100) UNIQUE NOT NULL)""")
  for x in ["Cash","UPI","Card","Net Banking"]: q.execute("INSERT IGNORE INTO payment_modes(mode_name) VALUES(%s)",(x,))
  c.commit();q.close();c.close()
 def build(self):
  tk.Label(self.r,text="DAILY EXPENSES TRACKING SYSTEM",font=("Arial",22,"bold")).pack(pady=10)
  self.user=tk.Label(self.r,text="User: ");self.user.pack()
  n=ttk.Notebook(self.r);n.pack(fill="both",expand=True,padx=10,pady=10)
  self.dash,self.exp,self.inc,self.bud,self.manage,self.rep=[tk.Frame(n) for _ in range(6)]
  for f,t in zip([self.dash,self.exp,self.inc,self.bud,self.manage,self.rep],
                 ["Dashboard","Expenses","Income","Budget","Categories & Modes","Reports"]): n.add(f,text=t)
  self.build_dash();self.build_exp();self.build_income();self.build_budget();self.build_manage();self.build_report()
 def build_dash(self):
  self.cards={}
  f=tk.Frame(self.dash);f.pack(fill="x",pady=20)
  for i,x in enumerate(["Today Expense","Month Expense","Month Income","Balance","Budget"]):
   z=tk.LabelFrame(f,text=x,padx=20,pady=15);z.grid(row=0,column=i,padx=5,sticky="nsew");f.columnconfigure(i,weight=1)
   self.cards[x]=tk.Label(z,text="₹ 0.00",font=("Arial",16,"bold"));self.cards[x].pack()
  self.bmsg=tk.Label(self.dash,text="",font=("Arial",13));self.bmsg.pack(pady=20)
  tk.Button(self.dash,text="Refresh Dashboard",command=self.refresh).pack()
 def build_exp(self):
  f=tk.LabelFrame(self.exp,text="Expense Information");f.pack(fill="x",padx=10,pady=10)
  fields=["Title","Amount","Date","Category","Payment","Description"]
  for i,x in enumerate(fields): tk.Label(f,text=x).grid(row=i//3*2,column=i%3*2,padx=5,pady=3)
  self.title=tk.Entry(f,width=22);self.amount=tk.Entry(f,width=22);self.edate=tk.Entry(f,width=22)
  self.cat=ttk.Combobox(f,width=19,state="readonly");self.mode=ttk.Combobox(f,width=19,state="readonly");self.desc=tk.Entry(f,width=22)
  ws=[self.title,self.amount,self.edate,self.cat,self.mode,self.desc]
  for i,w in enumerate(ws): w.grid(row=i//3*2,column=i%3*2+1,padx=5,pady=3)
  self.edate.insert(0,date.today().isoformat())
  bf=tk.Frame(self.exp);bf.pack(pady=5)
  for t,cmd in [("Add",self.add_exp),("Update",self.update_exp),("Delete",self.delete_exp),("Clear",self.clear_exp)]:
   tk.Button(bf,text=t,width=12,command=cmd).pack(side="left",padx=3)
  sf=tk.Frame(self.exp);sf.pack(fill="x",padx=10)
  tk.Label(sf,text="Search").pack(side="left");self.search=tk.Entry(sf,width=30);self.search.pack(side="left",padx=5)
  tk.Button(sf,text="Search",command=self.search_exp).pack(side="left");tk.Button(sf,text="Show All",command=self.view_exp).pack(side="left",padx=5)
  cols=("ID","Title","Amount","Date","Category","Payment","Description")
  self.et=ttk.Treeview(self.exp,columns=cols,show="headings")
  for x in cols:self.et.heading(x,text=x);self.et.column(x,width=140)
  self.et.pack(fill="both",expand=True,padx=10,pady=10);self.et.bind("<Double-1>",self.select_exp)
 def load_all(self):
  c=self.db();q=c.cursor();q.execute("SELECT category_name FROM categories ORDER BY category_name");self.categories=[x[0] for x in q.fetchall()]
  q.execute("SELECT mode_name FROM payment_modes ORDER BY mode_name");self.modes=[x[0] for x in q.fetchall()];q.close();c.close()
  self.cat["values"]=self.categories;self.mode["values"]=self.modes
  if self.categories:self.cat.current(0)
  if self.modes:self.mode.current(0)
 def add_exp(self):
  try:
   a=float(self.amount.get());datetime.strptime(self.edate.get(),"%Y-%m-%d")
   if a<=0:raise ValueError
   c=self.db();q=c.cursor();q.execute("SELECT category_id FROM categories WHERE category_name=%s",(self.cat.get(),));cid=q.fetchone()[0]
   q.execute("""INSERT INTO expenses(title,amount,expense_date,category_id,payment_mode,description)
   VALUES(%s,%s,%s,%s,%s,%s)""",(self.title.get(),a,self.edate.get(),cid,self.mode.get(),self.desc.get()))
   c.commit();q.close();c.close();messagebox.showinfo("Success","Expense added.");self.clear_exp();self.refresh()
  except Exception as e: messagebox.showerror("Error",str(e))
 def select_exp(self,e=None):
  s=self.et.selection()
  if not s:return
  v=self.et.item(s[0],"values")
  for w,val in [(self.title,v[1]),(self.amount,v[2]),(self.edate,v[3]),(self.cat,v[4]),(self.mode,v[5]),(self.desc,v[6])]:
   if isinstance(w,ttk.Combobox):w.set(val)
   else:w.delete(0,"end");w.insert(0,val)
 def update_exp(self):
  s=self.et.selection()
  if not s:return messagebox.showwarning("Select","Select an expense first.")
  try:
   eid=self.et.item(s[0],"values")[0];c=self.db();q=c.cursor();q.execute("SELECT category_id FROM categories WHERE category_name=%s",(self.cat.get(),));cid=q.fetchone()[0]
   q.execute("""UPDATE expenses SET title=%s,amount=%s,expense_date=%s,category_id=%s,payment_mode=%s,description=%s WHERE expense_id=%s""",
    (self.title.get(),float(self.amount.get()),self.edate.get(),cid,self.mode.get(),self.desc.get(),eid))
   c.commit();q.close();c.close();self.refresh();messagebox.showinfo("Success","Expense updated.")
  except Exception as e:messagebox.showerror("Error",str(e))
 def delete_exp(self):
  s=self.et.selection()
  if not s:return
  if not messagebox.askyesno("Delete","Delete selected expense?"):return
  c=self.db();q=c.cursor();q.execute("DELETE FROM expenses WHERE expense_id=%s",(self.et.item(s[0],"values")[0],));c.commit();q.close();c.close();self.refresh()
 def clear_exp(self):
  for w in [self.title,self.amount,self.desc]:w.delete(0,"end")
  self.edate.delete(0,"end");self.edate.insert(0,date.today().isoformat())
 def view_exp(self,keyword=""):
  for x in self.et.get_children():self.et.delete(x)
  c=self.db();q=c.cursor()
  if keyword:
   z="%"+keyword+"%";q.execute("""SELECT e.expense_id,e.title,e.amount,e.expense_date,c.category_name,e.payment_mode,e.description
   FROM expenses e JOIN categories c ON e.category_id=c.category_id
   WHERE e.title LIKE %s OR c.category_name LIKE %s OR e.payment_mode LIKE %s OR e.description LIKE %s
   ORDER BY e.expense_date DESC""",(z,z,z,z))
  else:q.execute("""SELECT e.expense_id,e.title,e.amount,e.expense_date,c.category_name,e.payment_mode,e.description
   FROM expenses e JOIN categories c ON e.category_id=c.category_id ORDER BY e.expense_date DESC""")
  for x in q.fetchall():self.et.insert("","end",values=x)
  q.close();c.close()
 def search_exp(self):self.view_exp(self.search.get())
 def build_income(self):
  f=tk.LabelFrame(self.inc,text="Income");f.pack(fill="x",padx=10,pady=20)
  for i,x in enumerate(["Source","Amount","Date","Remarks"]):tk.Label(f,text=x).grid(row=0,column=i*2,padx=5)
  self.isource=tk.Entry(f,width=20);self.iamount=tk.Entry(f,width=20);self.idate=tk.Entry(f,width=20);self.irem=tk.Entry(f,width=20)
  for i,w in enumerate([self.isource,self.iamount,self.idate,self.irem]):w.grid(row=0,column=i*2+1,padx=5)
  self.idate.insert(0,date.today().isoformat());tk.Button(f,text="Add Income",command=self.add_income).grid(row=1,column=0,columnspan=8,pady=10)
  self.ibal=tk.Label(self.inc,text="",font=("Arial",15,"bold"));self.ibal.pack(pady=20)
 def add_income(self):
  try:
   datetime.strptime(self.idate.get(),"%Y-%m-%d");a=float(self.iamount.get())
   c=self.db();q=c.cursor();q.execute("INSERT INTO income(source,amount,income_date,remarks) VALUES(%s,%s,%s,%s)",(self.isource.get(),a,self.idate.get(),self.irem.get()));c.commit();q.close();c.close();self.refresh();messagebox.showinfo("Success","Income added.")
  except Exception as e:messagebox.showerror("Error",str(e))
 def build_manage(self):
  a=tk.LabelFrame(self.manage,text="Categories");a.pack(side="left",fill="both",expand=True,padx=10,pady=10)
  self.newcat=tk.Entry(a);self.newcat.pack(pady=10);tk.Button(a,text="Add Category",command=self.add_cat).pack();self.clist=tk.Listbox(a);self.clist.pack(fill="both",expand=True,pady=10)
  b=tk.LabelFrame(self.manage,text="Payment Modes");b.pack(side="right",fill="both",expand=True,padx=10,pady=10)
  self.newmode=tk.Entry(b);self.newmode.pack(pady=10);tk.Button(b,text="Add Payment Mode",command=self.add_mode).pack();self.mlist=tk.Listbox(b);self.mlist.pack(fill="both",expand=True,pady=10)
 def add_cat(self):
  try:
   c=self.db();q=c.cursor();q.execute("INSERT INTO categories(category_name) VALUES(%s)",(self.newcat.get(),));c.commit();q.close();c.close();self.newcat.delete(0,"end");self.refresh()
  except Exception as e:messagebox.showerror("Error",str(e))
 def add_mode(self):
  try:
   c=self.db();q=c.cursor();q.execute("INSERT INTO payment_modes(mode_name) VALUES(%s)",(self.newmode.get(),));c.commit();q.close();c.close();self.newmode.delete(0,"end");self.refresh()
  except Exception as e:messagebox.showerror("Error",str(e))
 def build_budget(self):
  f=tk.LabelFrame(self.bud,text="Set Monthly / Category Budget");f.pack(fill="x",padx=10,pady=15)
  tk.Label(f,text="Category").grid(row=0,column=0,padx=5);self.bcat=ttk.Combobox(f,width=20,state="readonly");self.bcat.grid(row=0,column=1)
  tk.Label(f,text="Amount").grid(row=0,column=2);self.bamt=tk.Entry(f,width=20);self.bamt.grid(row=0,column=3)
  tk.Label(f,text="Start").grid(row=1,column=0,pady=5);self.bs=tk.Entry(f,width=20);self.bs.grid(row=1,column=1);self.bs.insert(0,date.today().replace(day=1).isoformat())
  tk.Label(f,text="End").grid(row=1,column=2);self.be=tk.Entry(f,width=20);self.be.grid(row=1,column=3)
  last=calendar.monthrange(date.today().year,date.today().month)[1];self.be.insert(0,date.today().replace(day=last).isoformat())
  tk.Button(f,text="Set Budget",command=self.set_budget).grid(row=2,column=0,columnspan=4,pady=8)
  self.bstatus=tk.Label(self.bud,text="",font=("Arial",13,"bold"));self.bstatus.pack(pady=10)
 def set_budget(self):
  try:
   a=float(self.bamt.get());datetime.strptime(self.bs.get(),"%Y-%m-%d");datetime.strptime(self.be.get(),"%Y-%m-%d")
   c=self.db();q=c.cursor();q.execute("SELECT category_id FROM categories WHERE category_name=%s",(self.bcat.get(),));cid=q.fetchone()[0]
   q.execute("INSERT INTO budgets(category_id,amount,start_date,end_date) VALUES(%s,%s,%s,%s)",(cid,a,self.bs.get(),self.be.get()));c.commit();q.close();c.close();self.refresh();messagebox.showinfo("Success","Budget saved.")
  except Exception as e:messagebox.showerror("Error",str(e))
 def build_report(self):
  f=tk.Frame(self.rep);f.pack(pady=10)
  for t,cmd in [("Daily Total",self.daily_report),("Monthly Total",self.month_report),("Category Report",self.category_report),("Monthly Summary",self.summary),("Chart",self.chart)]:
   tk.Button(f,text=t,width=16,command=cmd).pack(side="left",padx=4)
  self.rt=tk.Text(self.rep,font=("Consolas",11));self.rt.pack(fill="both",expand=True,padx=10,pady=10)
 def report(self,s):
  self.rt.delete("1.0","end");self.rt.insert("end",s)
 def daily_report(self):
  c=self.db();q=c.cursor();q.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE expense_date=%s",(date.today().isoformat(),));x=float(q.fetchone()[0]);q.close();c.close();self.report(f"DAILY EXPENSE REPORT\nDate: {date.today()}\nTotal: ₹ {x:.2f}")
 def month_report(self):
  s=date.today().replace(day=1).isoformat();e=date.today().isoformat();c=self.db();q=c.cursor()
  q.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE expense_date BETWEEN %s AND %s",(s,e));ex=float(q.fetchone()[0])
  q.execute("SELECT COALESCE(SUM(amount),0) FROM income WHERE income_date BETWEEN %s AND %s",(s,e));inc=float(q.fetchone()[0]);q.close();c.close()
  self.report(f"MONTHLY REPORT\nIncome: ₹ {inc:.2f}\nExpense: ₹ {ex:.2f}\nBalance: ₹ {inc-ex:.2f}")
 def category_report(self):
  c=self.db();q=c.cursor();q.execute("""SELECT c.category_name,COALESCE(SUM(e.amount),0)
  FROM categories c LEFT JOIN expenses e ON c.category_id=e.category_id GROUP BY c.category_id,c.category_name ORDER BY 2 DESC""")
  self.report("CATEGORY-WISE REPORT\n"+"-"*45+"\n"+"\n".join(f"{a:<25} ₹ {float(b):.2f}" for a,b in q.fetchall()));q.close();c.close()
 def summary(self):
  s=date.today().replace(day=1).isoformat();c=self.db();q=c.cursor();q.execute("SELECT expense_date,SUM(amount) FROM expenses WHERE expense_date>= %s GROUP BY expense_date ORDER BY expense_date",(s,));rows=q.fetchall();q.close();c.close();self.report("MONTHLY SUMMARY\n"+"\n".join(f"{a}  ₹ {float(b):.2f}" for a,b in rows))
 def chart(self):
  try:
   import matplotlib.pyplot as plt
   c=self.db();q=c.cursor();q.execute("""SELECT c.category_name,SUM(e.amount) FROM expenses e JOIN categories c ON e.category_id=c.category_id GROUP BY c.category_id,c.category_name ORDER BY 2 DESC""");r=q.fetchall();q.close();c.close()
   if not r:return messagebox.showinfo("Chart","No expense data.")
   plt.figure(figsize=(9,5));plt.bar([x[0] for x in r],[float(x[1]) for x in r]);plt.title("Category-wise Expenses");plt.xlabel("Category");plt.ylabel("Amount");plt.xticks(rotation=30);plt.tight_layout();plt.show()
  except Exception as e:messagebox.showerror("Chart Error",str(e))
 def total(self,kind):
  c=self.db();q=c.cursor()
  if kind=="day":q.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE expense_date=%s",(date.today().isoformat(),))
  else:q.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE YEAR(expense_date)=YEAR(CURDATE()) AND MONTH(expense_date)=MONTH(CURDATE())")
  x=float(q.fetchone()[0]);q.close();c.close();return x
 def income_total(self):
  c=self.db();q=c.cursor();q.execute("SELECT COALESCE(SUM(amount),0) FROM income");x=float(q.fetchone()[0]);q.close();c.close();return x
 def budget_total(self):
  c=self.db();q=c.cursor();q.execute("SELECT COALESCE(SUM(amount),0) FROM budgets WHERE start_date<=CURDATE() AND end_date>=CURDATE()");x=float(q.fetchone()[0]);q.close();c.close();return x
 def refresh(self):
  try:
   self.load_all();self.cat["values"]=self.categories;self.mode["values"]=self.modes;self.bcat["values"]=self.categories
   for w,l in [(self.clist,self.categories),(self.mlist,self.modes)]:w.delete(0,"end");[w.insert("end",x) for x in l]
   d=self.total("day");m=self.total("month");i=self.income_total();b=self.budget_total()
   self.cards["Today Expense"].config(text=f"₹ {d:.2f}");self.cards["Month Expense"].config(text=f"₹ {m:.2f}")
   self.cards["Month Income"].config(text=f"₹ {i:.2f}");self.cards["Balance"].config(text=f"₹ {i-m:.2f}");self.cards["Budget"].config(text=f"₹ {b:.2f}")
   self.bmsg.config(text=("Budget exceeded by ₹ %.2f"%(m-b)) if b and m>b else ("Budget remaining: ₹ %.2f"%(b-m)) if b else "No active budget set.")
   self.ibal.config(text=f"Current Balance: ₹ {i-m:.2f}");self.view_exp()
  except Exception as e:messagebox.showerror("Refresh Error",str(e))

if __name__=="__main__":
 setup_database()
 root=tk.Tk();App(root);root.mainloop()
