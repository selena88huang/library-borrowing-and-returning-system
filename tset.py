import warnings
# warnings.simplefilter("ignore")
import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
import datetime
from tkinter import Canvas
import importlib
from midterm_base import registed
from midterm_base import new_df



#進入借書系統
def userwin(user_id):
    # print(registed.loc[user_id])
    temp = pd.DataFrame(registed.loc[user_id])
    temp = registed.loc[user_id]
    print(temp)
    print(temp["history"])
    
    #編輯borrowable狀態
    def edit_borrow(bookid):
        # Get selected item to Edit
        booktemp = pd.DataFrame(new_df.loc[bookid])
        booktemp = new_df.loc[bookid]
        selected_item = tree.selection()[0]
        print(tree.selection())
        tree.item(selected_item, text=new_df["id"][bookid], values=(new_df["題名"][bookid],new_df["作者/創建者"][bookid],0))
        global borrowable
        borrowable = 0
        booktemp['borrowable'] = 0

        new_df.loc[bookid] = booktemp
        new_df.to_excel("new_df.xlsx")
    
    def edit_return(bookid):
        # Get selected item to Edit
        booktemp = pd.DataFrame(new_df.loc[bookid])
        booktemp = new_df.loc[bookid]
        selected_item = tree.selection()[0]
        print(tree.selection())
        tree.item(selected_item, text=new_df["id"][bookid], values=(new_df["題名"][bookid],new_df["作者/創建者"][bookid],1))
        global borrowable
        borrowable = 1
        booktemp['borrowable'] = 1

        new_df.loc[bookid] = booktemp
        new_df.to_excel("new_df.xlsx")

    #借書
    def borrowbook(bookid,borrowable):
        if borrowable == 1:
            time = datetime.date.today()
            bookname = new_df["題名"][int(bookid)]
            # print(type(eval(temp['history'])))
            # print(type([(bookname,time)]))
            try:
                eval(temp["history"])
            except:
                temp["history"] = temp["history"]+[(bookname,time)] #0是寫死的
                
                # registed["history"][user_id]+[bookname,time]
                temp["borrow_num"] += 1 #0是寫死的
                #bookid-->bookname
                temp["deadline"] = temp["deadline"]+[(bookname,time+datetime.timedelta(days=7))] #0是寫死的
                # registed["deadline"][user_id]+[(int(bookid),time+datetime.timedelta(days=7))]
                edit_borrow(int(bookid))
                messagebox.showinfo('借書成功', ("Thank you! Your borrow time:",time))
            else:
                
                temp["history"] = eval(temp["history"])+[(bookname,time)] #0是寫死的
                
                # registed["history"][user_id]+[bookname,time]
                temp["borrow_num"] += 1 #0是寫死的
                #bookid-->bookname
                temp["deadline"] = eval(temp["deadline"])+[(bookname,time+datetime.timedelta(days=7))] #0是寫死的
                # registed["deadline"][user_id]+[(int(bookid),time+datetime.timedelta(days=7))]
                edit_borrow(int(bookid))
                messagebox.showinfo('借書成功', ("Thank you! Your borrow time:",time))
        elif borrowable == -1:
            messagebox.showinfo('請先選擇書籍', '請先選擇書籍')
        else:
            messagebox.showinfo('已被借走', 'Sorry')
    
    #還書
    def returnbook(bookid,borrowable):
        if borrowable == 0:
            time = datetime.date.today()
            temp["borrow_num"] -= 1 #0是寫死的
            # x = temp["deadline"] #0是寫死的
            for i, a in enumerate(temp["deadline"]):
                print(i)
                print(a)

                if new_df["題名"][int(bookid)] == a[0]:
                    if i + 1 <= len(temp["deadline"]):
                        print("1",temp['deadline'])
                        temp['deadline'] = temp["deadline"][:i] + temp["deadline"][i+1:] #0是寫死的
                        print("2",temp['deadline'])
                    else:
                        print("3",temp['deadline'])
                        temp['deadline'] = temp["deadline"][:i] #0是寫死的
                        print("4",temp['deadline'])
            edit_return(int(bookid))
            messagebox.showinfo('還書成功', ('Thank you!','Your return time:',time))
        elif borrowable == -1:
            messagebox.showinfo('請先選擇書籍', '請先選擇書籍')
        else:
            messagebox.showinfo('尚未借閱', 'Sorry')

    #個人資料頁面
    def view_profile():
        try:
            temp["history"][0][1]
            
        except:
            messagebox.showinfo(title="提醒",message="您還尚未借任何書")
        else:
            profile= tk.Tk()
            profile.title('個人資料')
            profile.focus_force()
            profile.geometry("700x350")
            profile.resizable(False, False)

            notebook = ttk.Notebook(profile,padding=15)
            notebook.pack()
            frame1 = ttk.Frame(notebook, width=900, height=500)
            frame2 = ttk.Frame(notebook, width=900, height=500)
            frame1.pack(fill='both', expand=True)
            frame2.pack(fill='both', expand=True)
            notebook.add(frame1, text='歷史借閱紀錄')
            notebook.add(frame2, text='待歸還書籍')


            tk.Label(frame1,text="歷史借閱數量").pack()
            tk.Label(frame1,text=len(temp["history"])).pack() #0是寫死的
            history_tree=ttk.Treeview(frame1,columns=("0","1"))
            history_tree.heading("0",text="書名")
            history_tree.heading("1",text="借閱日期")

            for i in range(len(temp["history"])): #0是寫死的
                
                bookname= temp["history"][i][0] #第一個0是寫死的
                borrowdate= temp["history"][i][1] #第一個0是寫死的
                # print(borrowdate)
                history_tree.insert("",index="end",text=i+1,values=(bookname,borrowdate))
            history_tree.pack()


            tk.Label(frame2,text="待歸還數量").pack()
            tk.Label(frame2,text=str(temp["borrow_num"])).pack() #0是寫死的
            deadline_tree=ttk.Treeview(frame2,columns=("0","1"))
            deadline_tree.heading("0",text="書名")
            deadline_tree.heading("1",text="歸還期限")

            for i in range(len(temp["deadline"])): #0是寫死的
                # print(temp["deadline"][i][0])
                bookname = temp["deadline"][i][0]
                # bookname=new_df["題名"][int(registed["deadline"][user_id])[i][0]] #第一個0是寫死的
                deadline = temp["deadline"][i][1]+datetime.timedelta(days=7) #第一個0是寫死的
                deadline_tree.insert("",index="end",text=i+1,values=(bookname,deadline))
            deadline_tree.pack()

    #搜尋
    def check_search_null():
        search_content = search_book.get()
        if(search_content == ""):
            messagebox.showerror(title="error",message="不能為空，請輸入欲搜尋的文字")
        else:
            search_bookname(search_content)
    
    def search_bookname(search_content):
        bookname_list=new_df["題名"].values.tolist()
        bookid=new_df["id"].values.tolist()
        book_view=list(zip(bookid,bookname_list))
        search_result_list=[]
        for i in book_view:
            if search_content.lower() in i[1].lower() :
                search_result_list.append(i)
        print(search_result_list)
        search_page= tk.Tk()
        search_page.title('搜尋結果')
        tk.Label(search_page,text="搜尋結果").pack()
        search_page.focus_force()
        search_page.geometry("500x300")
        search_page.resizable(False, False)

        search_tree=ttk.Treeview(search_page,columns=("0"))
        search_tree.heading("0",text="書名")
        for i in search_result_list:
            text=i[0]
            value=i[1]
            if value[len(value)-1] == " ":
                value=value[:len(value)-1]
            value = value.replace(" ","_")
            search_tree.insert("",index="end",text=text,values=value)  
        search_tree.pack()

    #登出
    def logout():
        msg = messagebox.askquestion(title="您正在登出",message="確定要登出嗎",)
        if msg=="yes":
            root.destroy()
            registed.loc[user_id] = temp
            print(registed.loc[user_id])
            registed.to_excel("registed.xlsx")
            # registed.to_csv("registed.csv")
            
            
            # new_df.to_excel("new_df.xlsx")
            lobby()
    
    #預約
    def reserve():
        messagebox.showinfo('預約成功', '預約成功！')




    root = tk.Tk()
    root.title('借書系統')
    root.geometry('%dx%d+%d+%d' % (1200,520,600,600))
    root.resizable(False, False)

    menubar = tk.Menu(root)
    menubar.add_command(label="個人資料", command=view_profile)
    menubar.add_command(label="登出", command=logout)  # 登出還沒寫
    root.config(menu=menubar)

    mylabel = tk.Label(root, text="歡迎來到寫到快崩潰的圖書館借書系統！")
    mylabel.grid(column=0, row=0, columnspan=3)  # 放在 (0,0)

    search_book = tk.Entry(root, width=40, font=('Arial 18'))
    search_book.grid(column=0, row=1, columnspan=2, padx=50, pady=10)  # 放在 (0,1)

    buttonExample = tk.Button(root,text="搜尋書名",command=check_search_null)
    buttonExample.config(width='25', height='2')
    buttonExample.grid(column=2, row=1, padx=50, pady=10)  # 放在 (2,1)

    s = ttk.Style()
    s.configure('Treeview', rowheight=30)
    tree=ttk.Treeview(root,columns=("0","1","2"))
    tree.heading("0",text="題名")
    tree.heading("1",text="作者/創建者")
    tree.heading("2",text="是否可借閱")

    for i in range(100):
        tree.insert("",index="end",text=new_df["id"][i],values=(new_df["題名"][i],new_df["作者/創建者"][i],new_df["borrowable"][i]))
    tree.grid(column=0, row=2, columnspan=3, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,2)

    buttonExample = tk.Button(root,text="借書",command=lambda : borrowbook(bookid, borrowable))
    buttonExample.config(width='25', height='2')
    buttonExample.grid(column=0, row=3, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,3)

    buttonExample = tk.Button(root,text="還書",command=lambda : returnbook(bookid, borrowable))
    buttonExample.config(width='25', height='2')
    buttonExample.grid(column=1, row=3, sticky=tk.EW, padx=50, pady=10)  # 放在 (1,3)

    buttonExample = tk.Button(root,text="預約",command=reserve)   # reserve還沒寫
    buttonExample.config(width='25', height='2')
    buttonExample.grid(column=2, row=3, sticky=tk.W, padx=50, pady=10)  # 放在 (1,3)

    #選取書籍
    def selectItem(event):
        curItem = tree.focus()
        global bookid
        bookid = tree.item(curItem)["text"]
        global borrowable
        borrowable = tree.item(curItem)["values"][2]
        print(bookid,borrowable)

    tree.bind('<ButtonRelease>', selectItem)
    
    #雙擊書籍
    def doubleclickItem(event,bookid):
        bookInfo = tk.Tk()
        bookInfo.title('書本資料')
        tk.Label(bookInfo,text="書本資料").pack()
        bookInfo.focus_force()
        bookInfo.geometry("800x600")
        text = tk.Text(bookInfo, height=40)
        
        for i in new_df:
            text.insert("end",(str(i) + ":" + str(new_df[i][int(bookid)]) +"\n\n\n"))
        text['state'] = 'disabled'
        text.pack()
        
    tree.bind('<Double-Button-1>',lambda event: doubleclickItem(event,bookid))

    root.mainloop()


#登入驗證
def lobby():
    def chkidpw():
        id = account.get()
        pw = password.get()
        if(id == ""):
            messagebox.showerror(title="error",message="不能為空，請輸入帳號")
            
        elif(pw == ""):
            messagebox.showerror(title="errorinfo",message="不能為空，請輸入密碼")
        else:
            verid(id,pw)
    
    def verpw(id,pw):

        if registed.loc[id]['pw']==pw:
            messagebox.showinfo(title="welocme",message="歡迎使用")
            window.destroy()
            userwin(id)
        else:
            messagebox.showerror(title="error",message="請先註冊或帳號或密碼輸入錯誤!")

    def verid(id,pw):

        try:
            registed.loc[id]
        except:
            messagebox.showerror(title="error",message="請先註冊或帳號或密碼輸入錯誤!")
        else:
            verpw(id,pw)
        

#註冊
    def regist():

        def chkregist():
            count=0
            id = registid.get()
            pw = registpw.get()
            repw = reregistpw.get()
            
            if(id == ""):
            
                messagebox.showerror(title="error",message="不能為空，請輸入帳號")
                regist.focus_force()
            else:
                count+=1
            
            if(pw == ""):
                messagebox.showerror(title="errorinfo",message="不能為空，請輸入密碼")
                regist.focus_force()
            else:
                count+=1
            
            if (repw==pw):
                count+=1    
            else:
                messagebox.showerror(title="errorinfo",message="輸入的密碼不一致")
                regist.focus_force()
            
            if(count==3): 
                try:
                    registed.loc[id]
                    messagebox.showerror(title="error",message="此帳號已被註冊")
                    regist.focus_force()
                except:
                    count+=1

            if(count>3):         
                registed.loc[str(id)] = [str(pw),list() ,0,list()]
                messagebox.showinfo(title="註冊成功",message="歡迎使用!")
                print(registed)
                registed.to_excel("registed.xlsx",encoding="utf-8")
                regist.destroy()
            
        
        regist = tk.Toplevel(window)
        regist.geometry('500x550')
        regist.resizable(False, False)
        # regist.focus_force()

        mylabel = tk.Label(regist, text="使用者註冊")
        mylabel.grid(column=0, row=0, columnspan=2, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,0)

        regist_id = tk.Label(regist,text="請輸入想創建帳號:",fg="green",height=4, font=('Arial 12'))
        regist_id.grid(column=0, row=1, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,1)

        regist_pw = tk.Label(regist,text="請輸入想設定密碼:",fg="green",height=4, font=('Arial 12'))
        regist_pw.grid(column=0, row=2, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,2)

        re_pw = tk.Label(regist,text="請再次輸入密碼:",fg="green",height=4, font=('Arial 12'))
        re_pw.grid(column=0, row=3, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,3)
        
        registid = tk.Entry(regist,width=10, font=('Arial 12'))
        registid.grid(column=1, row=1, sticky=tk.EW, padx=50, pady=10)  # 放在 (1,1)
        # alertmsg=tk.StringVar(regist)

        registpw = tk.Entry(regist,width=10, font=('Arial 12'),show="*")
        registpw.grid(column=1, row=2, sticky=tk.EW, padx=50, pady=10)  # 放在 (1,2)

        reregistpw = tk.Entry(regist,width=10, font=('Arial 12'),show="*")
        reregistpw.grid(column=1, row=3, sticky=tk.EW, padx=50, pady=10)  # 放在 (1,3)

        register = tk.Button(regist,text="確認",command=chkregist,width='15', height='2')
        register.grid(column=0, row=4, columnspan=2, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,4)
        
        regist.mainloop()
        
        
        
    window = tk.Tk()
    window.title('圖書館借書系統')
    # bg = PhotoImage( file ='pic.gif')
    # canvas1 = Canvas( window, width = 400,height = 400)
  
    # canvas1.pack(fill = "both", expand = True)
    
    # # Display image
    # canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    window.geometry('600x480')
    window.resizable(False, False)
    # window.iconbitmap('icon.ico')

    mylabel = tk.Label(window, text="使用者登入")
    mylabel.grid(column=0, row=0, columnspan=2)  # 放在 (0,0)

    enter_id = tk.Label(window,text="請輸入帳號:",fg="green",height=4, font=('Arial 12'))
    enter_id.grid(column=0, row=2, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,2)

    enter_pw = tk.Label(window,text="請輸入密碼:",fg="green",height=4, font=('Arial 12'))
    enter_pw.grid(column=0, row=3, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,3)

    account = tk.Entry(window,width=10, font=('Arial 12'))
    account.grid(column=1, row=2, sticky=tk.EW, padx=50, pady=10)  # 放在 (1,2)
    alertmsg=tk.StringVar()
            
    password = tk.Entry(window,width=10, font=('Arial 12'),show="*")
    password.grid(column=1, row=3, sticky=tk.EW, padx=50, pady=10)  # 放在 (1,3)

    register = tk.Button(window,text="註冊",command=regist,width='15', height='2')
    register.grid(column=0, row=4, sticky=tk.EW, padx=50, pady=10)  # 放在 (0,4)

    login = tk.Button(window,text="登入",command=chkidpw,width='15', height='2')
    login.grid(column=1, row=4, sticky=tk.EW, padx=50, pady=10)  # 放在 (1,4)

    window.mainloop()
    
lobby()