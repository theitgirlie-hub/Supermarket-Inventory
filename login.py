import tkinter as tk 
from databases import * 
from tkinter import ttk
import mysql.connector as sql
import tkinter.messagebox as msg
from tkinter import END,ttk
import datetime
from gtts import gTTS
import pygame
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import threading



def play_audio(text):
    tts=gTTS(text=text,lang="en")
    audio_file="register_into.mp3"
    tts.save(audio_file)
   
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    os.remove(audio_file)

def initializer_connection():
    try:
        con = sql.connect(
            host="localhost",
            user="root",
            password="",
            database="treats"
        )
        cur = con.cursor()
        create_database(cur)
        create_table(cur)
        return cur, con
    except sql.Error as e:
        print(f"Error connecting to the database: {e}")
        return None, None

def create_database(cur):
    cur.execute(" show databases")
    temp=cur.fetchall()
    databases=[item[0] for item in temp]
    
    if "treats" not in databases:
        cur.execute("create database treats")
        cur.execute("use treats")
def create_table(cur):
    cur.execute("show tables")
    temp=cur.fetchall()
    tables=[item[0] for item in temp]
    if "staff" not in tables:
        cur.execute(''' create table  staff(
            staffId INT AUTO_INCREMENT PRIMARY KEY,
            firstName VARCHAR(100),
            lastName VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            phoneNumber VARCHAR(20),
            gender VARCHAR(1),
            age INT,
            address VARCHAR(200),
            jobDescription VARCHAR(100),
            jobRole VARCHAR(10),
            Restricted BOOLEAN
        )''')
    elif "products" not in tables:
        cur.execute(''' create table products (
                ItemId INTEGER PRIMARY KEY,
                ItemName TEXT UNIQUE,
                ItemQty INTEGER,
                ItemPrice VARCHAR(20)
            )
                    ''')

def treats(cur,data):
    con=sql.connect(
       host="localhost",
       user="root",
       password="",
       database="treats"
    )
    
    cur=con.cursor()

    query = """SELECT Restricted FROM staff WHERE email=%s AND password=%s"""
    cur.execute(query, (data['email'], data['password']))
    result = cur.fetchone()
    
    if result is None:
        return False 
    
    is_restricted = result[0]
    
    if is_restricted:
        return False  
    
    return True  

def register(cur, data):
    print(data)

    query = """INSERT INTO staff (firstName, lastName,password, email,phoneNumber, gender, age, address,jobDescription,jobRole) 
               VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
    values = (
        data["firstName"],
        data["lastName"],
        data["password"],
        data["email"],
        data["phoneNumber"],
        data["gender"],
        data["age"],
        data["address"],
        data["jobDescription"],
        data["jobRole"]
    )
    con=sql.connect(
       host="localhost",
       user="root",
       password="",
       database="treats"
    )
    
    cur=con.cursor()
    cur.execute(query, values)
    con.commit() 
con, cur=initializer_connection()

def fetch_job_description_from_db(cur,email):
    query = "SELECT jobDescription FROM staff WHERE email = %s"
    try:
        cur.execute(query, (email,))
        result = cur.fetchone()
        if result:
            return result[0]  
        else:
            print("No job description found for the given email.")
            return None
    except sql.Error as e: 
        print(f"Database error occurred: {e}")
        return None
    except Exception as e: 
        print(f"An error occurred: {e}")
        return None
cur, con = initializer_connection()


def center_window(width,height):
    x=(main.winfo_screenwidth()//2)-(width//2)
    y=(main.winfo_screenheight()//2)-(height//2)
    main.geometry(f'{width}x{height}+{x}+{y}')

PRIMARY_COLOR = "#4A90E2"
SECONDARY_COLOR = "#D9E6F2"
ACCENT_COLOR = "#E94E77"
BACKGROUND_COLOR = "#F5F5F5"
FRAME_BG="#f5f1e9"  
TEXT_COLOR = "#333333"
BUTTON_COLOR = PRIMARY_COLOR
BUTTON_TEXT_COLOR = "white"

# PRIMARY_COLOR = "#2E7D32"         
# SECONDARY_COLOR = "#A5D6A7"        
# ACCENT_COLOR = "#F9A825"           
# BACKGROUND_COLOR = "#F1F8E9"              
# TEXT_COLOR = "#212121" 
# BUTTON_COLOR = PRIMARY_COLOR   
# BUTTON_TEXT_COLOR = "#FFFFFF" 

# PRIMARY_COLOR = "#007BFF"          
# SECONDARY_COLOR = "#E3F2FD"        
# ACCENT_COLOR = "#FF6F20"           
# BACKGROUND_COLOR = "#F9F9F9"   
# BUTTON_COLOR = PRIMARY_COLOR
# TEXT_COLOR = "#333333"            
# BUTTON_TEXT_COLOR = "#FFFFFF"  

# PRIMARY_COLOR = "#6D4C41"          
# SECONDARY_COLOR = "#BCAAA4"       
# ACCENT_COLOR = "#FFB74D"           
# BACKGROUND_COLOR = "#FAFAFA" 
# BUTTON_COLOR = PRIMARY_COLOR              
# TEXT_COLOR = "#212121"             
# BUTTON_TEXT_COLOR = "#FFFFFF"

class welcomeWindow(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root=root 
        self.root.title("TREATS SUPERMARKET")
        self.root.resizable(False,True)
        center_window(360,250)
        self.pack(fill=tk.BOTH, expand=True)

        

        self.configure(bg=FRAME_BG_COLOR)

        self.background_image = tk.PhotoImage(file="images/mmm3.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1) 
        
        # welcome_label = tk.Label(self, text="Welcome to TREATS!", font=("Times New Roman", 16, "bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR)
        # welcome_label.pack(pady=(10, 20))

       

        login_button=tk.Button(self, text="Sign in", width=10,font=("Times New Roman",12,"bold"),  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat", command=self.open_sigin_window)
        login_button.pack(padx=20,pady=(20,5))
        
        register_button=tk.Button(self, text="Sign up", width=10,font=("Times New Roman",12,"bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,relief="flat", command=self.open_reegister_window)
        register_button.pack(pady=10)
        self.pack()
    def open_sigin_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        SigninWindow(self.root)
        
    def open_reegister_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        signUpWindow(self.root)


class SigninWindow(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root=root
        self.root.title("SIGN IN HERE!")
        self.root.resizable(False,True)
        center_window(330,170)
        self.pack(fill=tk.BOTH)

        self.configure(bg=FRAME_BG_COLOR)
        self.background_image = tk.PhotoImage(file="images/mmm3.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1) 
        
        tk.Label(self,text="UserName:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=0,column=0)
        self.username_entry=tk.Entry(self)
        self.username_entry.grid(row=0,column=1,padx=10,pady=10)
            
        tk.Label(self,text="Password:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=1,column=0)
        self.password_entry=tk.Entry(self,show="*")
        self.password_entry.grid(row=1,column=1,padx=10,pady=10)

        tk.Label(self, text="JobDescription:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, sticky="w")
        jobs=["Supervisor","Director","Salesperson","Inventory Personnel"]
        self.jobd_combobox = ttk.Combobox(self, values=jobs, width=26)
        self.jobd_combobox.grid(row=2, column=1,padx=16, pady=10)
        
        
        submit_button=tk.Button(self,text="Sign in",width=8, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat",command=self.submit)
        submit_button.grid(row=3, column=1, sticky="e", padx=10, pady=10)
        
        back_button=tk.Button(self,text="Back",width=8, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat", command=self.back)
        back_button.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.pack()
        
    def back(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        welcomeWindow(self.root)


    def submit(self):
      data = {}
      data["email"] = self.username_entry.get()
      data["password"] = self.password_entry.get()
      data["jobDescription"] = self.jobd_combobox.get()
    
      if treats(cur, data):
        expected_job_description = fetch_job_description_from_db(cur, data["email"]) 
        if self.jobd_combobox.get() == expected_job_description:
            msg.showinfo("Alert", "Login Successful!")
            for widget in self.winfo_children():
                widget.destroy()
            self.destroy()

            if expected_job_description == "Salesperson":
                mainWindowSales(self.root)
            elif expected_job_description == "Inventory Personnel":
                mainWindowStock(self.root)
            elif expected_job_description == "Supervisor":
                mainWindowAdmin(self.root)
            elif expected_job_description == "Director":
                mainWindowAdmin(self.root)
        else:
            msg.showinfo("Unauthorized user:", "Job description mismatch.")
            self.jobd_combobox.set('')
            print("Unauthorized User: Job description mismatch.")
      else:
        msg.showinfo("Account Restricted", "Please visit the supervisor. ")
        print("Unauthorized User: Invalid credentials or account restricted.")

 
        
class signUpWindow(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root=root 
        self.root.title("SIGN UP HERE!")
        self.root.resizable(False,True)
       
    

        self.background_image = tk.PhotoImage(file="images/mmm3.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1) 
        center_window(300,450)
        
        
         
        tk.Label(self, text="FirstName:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR,fg=TEXT_COLOR).grid(row=0, column=0, sticky="w")
        self.first_name_entry=tk.Entry(self, width=26)
        self.first_name_entry.grid(row=0,column=1, padx=10, pady=10, sticky="e")
        
        tk.Label(self, text="LastName:",font=("Times New Roman",12,"bold"), bg=FRAME_BG_COLOR,fg=TEXT_COLOR).grid(row=1, column=0, sticky="w")
        self.last_name_entry=tk.Entry(self, width=26)
        self.last_name_entry.grid(row=1,column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Password:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR,fg=TEXT_COLOR).grid(row=2, column=0, sticky="w")
        self.password_entry=tk.Entry(self, width=26,show="*")
        self.password_entry.grid(row=2,column=1, padx=10, pady=10, sticky="e")
        
        tk.Label(self, text="Email:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=3, column=0, sticky="w")
        self.email_entry=tk.Entry(self, width=26)
        self.email_entry.grid(row=3,column=1, padx=10, pady=10, sticky="e")
        
        tk.Label(self, text="PhoneNumber:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR,fg=TEXT_COLOR).grid(row=4, column=0, sticky="w")
        self.phoneNumber_entry=tk.Entry(self, width=26)
        self.phoneNumber_entry.grid(row=4,column=1, padx=10, pady=10, sticky="e")
        
        tk.Label(self, text="Gender:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=5, column=0, sticky="w")
        self.gender_entry=tk.Entry(self, width=26)
        self.gender_entry.grid(row=5,column=1, padx=10, pady=10, sticky="e")
        
        tk.Label(self, text="Age:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=6, column=0, sticky="w")
        self.age_entry=tk.Entry(self, width=26)
        self.age_entry.grid(row=6,column=1, padx=10, pady=10, sticky="e")
        
        tk.Label(self, text="Address:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=7, column=0, sticky="w")
        self.address_entry=tk.Entry(self, width=26)
        self.address_entry.grid(row=7,column=1, padx=10, pady=10, sticky="e")
        
        tk.Label(self, text="JobDescription:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).grid(row=8, column=0, sticky="w")
        jobs=["Supervisor","Director","Salesperson","Inventory Personnel"]
        self.jobd_combobox = ttk.Combobox(self, values=jobs, width=22)
        self.jobd_combobox.grid(row=8, column=1,padx=12, pady=10)
        
        tk.Label(self, text="JobRole:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR,fg=TEXT_COLOR).grid(row=9, column=0, sticky="w")
        role = ["Admin","Staff"]
        self.role_combobox = ttk.Combobox(self, values=role, width=22)
        self.role_combobox.grid(row=9, column=1, pady=10)
        
        self.btnReg=tk.Button(self, text="Register", width=8,bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,relief="flat" ,command=self.Reg)
        self.btnReg.grid(row=10, column=1, sticky="e", padx=10, pady=10)
        
        self.back=tk.Button(self, text="Back", width=8, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,relief="flat",command=self.back)
        self.back.grid(row=10, column=0, sticky="w", padx=10, pady=(10,10))
        
        self.pack()
        
    def Reg(self):
       
          data={}
          firstName=self.first_name_entry.get()
          lastName=self.last_name_entry.get()
          password=self.password_entry.get()
          email=self.email_entry.get()
          phoneNumber=self.phoneNumber_entry.get()
          gender=self.gender_entry.get()
          age=self.age_entry.get()
          address=self.address_entry.get()
          jobDescription=self.jobd_combobox.get()
          jobRole=self.role_combobox.get()

          if (firstName=="" and lastName=="" and password=="" and email=="" and phoneNumber=="" and gender=="" and age=="" and address==""and jobDescription=="" and jobRole==""):
            msg.showinfo("Empty Record","Please fill the form!")
          else:
            data["firstName"]=self.first_name_entry.get()
            data["lastName"]=self.last_name_entry.get()
            data["password"]=self.password_entry.get()
            data["email"]=self.email_entry.get()
            data["phoneNumber"]=self.phoneNumber_entry.get()
            data["gender"]=self.gender_entry.get()
            data["age"]=self.age_entry.get()
            data["address"]=self.address_entry.get()
            data["jobDescription"]=self.jobd_combobox.get()
            data["jobRole"]=self.role_combobox.get()
         
            
            register(cur,data)
            msg.showinfo("Registration Successful","Please Sign In Now!")
            
            self.first_name_entry.delete(0,END)
            self.last_name_entry.delete(0,END)
            self.password_entry.delete(0,END)
            self.email_entry.delete(0,END)
            self.phoneNumber_entry.delete(0,END)
            self.gender_entry.delete(0,END)
            self.age_entry.delete(0,END)
            self.address_entry.delete(0,END)
            self.jobd_combobox.set('')
            self.role_combobox.set('')
        
            

    
    def back(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        welcomeWindow(self.root)
            

def inventory(cur, data):
    print(data)

    query = """INSERT INTO products (ItemId, ItemName,ItemQty,ItemPrice) 
               VALUES (%s, %s, %s, %s)"""
    values = (
        data["ItemId"],
        data["ItemName"],
        data["ItemQty"],
        data["ItemPrice"]
    )
    con=sql.connect(
       host="localhost",
       user="root",
       password="",
       database="treats"
    )
    try:
        cur.execute(query, values)
        con.commit()
        print("Product added successfully.")
    except Exception as e:
        print(f"Error inserting product: {e}")


class mainWindowSales(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill=tk.BOTH, expand=True)
        self.root.title("SALES AT TREATS")
        center_window(1000,650)
        self.root.resizable(False,False)
        self.selected_products = {}
        self.bill_displayed = False

        self.configure(bg=BACKGROUND_COLOR)
        self.background_image = tk.PhotoImage(file="images/sup.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1) 
        
        


        pygame.mixer.init()

        
        self.time_label = tk.Label(self, font=("Times New Roman", 12,"bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.time_label.pack(pady=(10, 0))  
        self.update_time()  
        
        search_frame = tk.Frame(self,bg=FRAME_BG_COLOR)
        search_frame.pack(pady=10)

        
        tk.Label(search_frame, text="Search Product:",font=("Times New Roman",13,"bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", self.search_product)

        
        products_frame = tk.Frame(self,bg=FRAME_BG_COLOR)
        products_frame.pack(pady=5)

        tk.Label(products_frame, text="Available Products", font=("Times New Roman",12,"bold"),bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.products_listbox = tk.Listbox(products_frame, width=60, height=10,bg=FRAME_BG_COLOR)
        self.products_listbox.pack()
        self.products_listbox.bind('<Double-Button-1>', self.add_selected_product)

       
        selected_frame = tk.Frame(self,bg=FRAME_BG_COLOR)
        selected_frame.pack(pady=10)

        tk.Label(selected_frame, text="Selected Products",font=("Times New Roman",12,"bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.selected_listbox = tk.Listbox(selected_frame, width=60, height=10,bg=FRAME_BG_COLOR)
        self.selected_listbox.pack()

        
        self.quantity_frame = tk.Frame(selected_frame,bg=FRAME_BG_COLOR)
        self.quantity_frame.pack(pady=5)

        tk.Label(self.quantity_frame, text="Quantity:",font=("Times New Roman",12,"bold"),bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT)
        self.quantity_entry = tk.Entry(self.quantity_frame, width=5)
        self.quantity_entry.pack(side=tk.LEFT)
        self.quantity_entry.bind("<Return>", self.update_selected_quantity)

        
        billing_frame = tk.Frame(self,bg=FRAME_BG_COLOR)
        billing_frame.pack(pady=5)

        self.total_label = tk.Label(billing_frame, text="Total Bill: ₦0.00", font=("Times New Roman", 14, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.total_label.pack()

        
        self.update_button = tk.Button(billing_frame, text="Show Bill", command=self.update_quantity,relief="flat",font=("Times New Roman", 12, "bold"),width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        self.update_button.pack(pady=0)

        self.logout_button = tk.Button(self, text="Log Out", bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,relief="flat",font=("Times New Roman",12,"bold"),width=10,command=self.logout)
        self.logout_button.pack(pady=10)



      
        self.update_product_list()

    def update_time(self):
       current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       self.time_label.config(text=current_time)
       self.after(1000, self.update_time)  

    def update_product_list(self):
        self.products_listbox.delete(0, END)
        cur.execute("SELECT ItemName, ItemQty, ItemPrice FROM products ORDER BY ItemName")
        rows = cur.fetchall()
        if not rows:
            self.products_listbox.insert(END, "No items in inventory.")
            return
        for ItemName, qty, price in rows:
            try:
                price = float(price)
                self.products_listbox.insert(END, f"{ItemName} - Quantity Left: {qty} - Price: ₦{price:.2f}")
            except ValueError:
                self.products_listbox.insert(END, f"{ItemName} - Quantity Left: {qty} - Price: Invalid Price")
    
    def logout(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        welcomeWindow(self.root)

    def search_product(self, event=None):
        search_term = self.search_var.get().strip().lower()
        self.products_listbox.delete(0, END)
        if search_term == "":
            self.update_product_list()
            return
        cur.execute("SELECT ItemName, ItemQty, ItemPrice FROM products WHERE LOWER(ItemName) LIKE %s ORDER BY ItemName", (f'%{search_term}%',))
        rows = cur.fetchall()
        if not rows:
            self.products_listbox.insert(END, "No matching products found.")
            return
        for ItemName, qty, price in rows:
            try:
                price = float(price)
                self.products_listbox.insert(END, f"{ItemName} - Quantity Left: {qty} - Price: ₦{price:.2f}")
            except ValueError:
                self.products_listbox.insert(END, f"{ItemName} - Quantity Left: {qty} - Price: Invalid Price")

    def add_selected_product(self, event=None):
        selection = self.products_listbox.curselection()
        if not selection:
            return
        selected_text = self.products_listbox.get(selection[0])
        item_name = selected_text.split(" - ")[0]

        cur.execute("SELECT ItemQty, ItemPrice FROM products WHERE ItemName = %s", (item_name,))
        row = cur.fetchone()
        if not row:
            msg.showerror("Error", "Selected product not found in database.")
            return
        qty, price = row
        if qty <= 0:
            msg.showwarning("Out of Stock", f"The product '{item_name}' is out of stock.")
            return

        if item_name in self.selected_products:
            if self.selected_products[item_name]['qty'] < qty:
                self.selected_products[item_name]['qty'] += 1
            else:
                msg.showwarning("Stock Limit", f"No more stock available for '{item_name}'.")
                return
        else:
            self.selected_products[item_name] = {'qty': 1, 'price': price}
         
        self.refresh_selected_products()
        self.calculate_total()
        self.bill_displayed = False 

    def refresh_selected_products(self):
        self.selected_listbox.delete(0, END)
        for item, info in self.selected_products.items():
            total_price = info['qty'] * float(info['price'])
            self.selected_listbox.insert(END, f"{item} - Qty: {info['qty']} - Subtotal: ₦{total_price:.2f}")

    def calculate_total(self):
        total = 0.0
        for info in self.selected_products.values():
            total += info['qty'] * float(info['price'])
        self.total_label.config(text=f"Total Bill: ₦{total:.2f}")
        return total  

    def update_selected_quantity(self, event=None):
        index = self.selected_listbox.curselection()
        if not index:
            return
        selected_item = self.selected_listbox.get(index[0])
        item_name = selected_item.split(" - ")[0]

        try:
            new_qty = int(self.quantity_entry.get())
            if new_qty < 1:
                msg.showwarning("Invalid Quantity", "Quantity must be at least 1.")
                return
            if item_name in self.selected_products:
                self.selected_products[item_name]['qty'] = new_qty
                self.refresh_selected_products()
                self.calculate_total()
        except ValueError:
            msg.showwarning("Invalid Input", "Please enter a valid quantity.")

    def update_quantity(self):
       if not self.selected_products:
         msg.showwarning("No Products Selected", "Please select products to update.")
         return

       for item, info in self.selected_products.items():
        cur.execute("UPDATE products SET ItemQty = ItemQty - %s WHERE ItemName = %s", (info['qty'], item))
        con.commit()

       bill_details = "\n".join([f"{item} - Qty: {info['qty']} - Subtotal: ₦{info['qty'] * float(info['price']):.2f}" for item, info in self.selected_products.items()])
       total_amount = self.calculate_total()
       bill_message = f"Bill Details:\n{bill_details}\n\nTotal Amount: ₦{total_amount:.2f}"

       if not self.bill_displayed: 
          if msg.askyesno("Confirm Bill", "Do you want to see the bill?"):
            threading.Thread(target=play_audio, args=(bill_message,)).start()
            msg.showinfo("Bill", bill_message)
            self.generate_pdf_bill()
            self.bill_displayed = True  
       else:
        msg.showinfo("Info", "The bill has already been displayed for this transaction.")

       self.selected_products.clear()
       self.refresh_selected_products()
       self.calculate_total()
       self.quantity_entry.delete(0, END)


    
    def generate_pdf_bill(self):
      total_amount = self.calculate_total()
      bill_details = "\n".join([f"{item} - Qty: {info['qty']} - Subtotal: ₦{info['qty'] * float(info['price']):.2f}" for item, info in self.selected_products.items()])
    
    
      current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
      pdf_file = "bill.pdf"
      c = canvas.Canvas(pdf_file, pagesize=letter)
    
   
      c.drawString(100, 750, "Treats Supermarket")
      c.drawString(100, 730, f"Date: {current_date}")
      c.drawString(100, 710, "Bill Details:")
    
   
      y_position = 690  
      for line in bill_details.split('\n'):
         c.drawString(100, y_position, line)
         y_position -= 20  
    
    
      c.drawString(100, y_position, f"Total Amount: ₦{total_amount:.2f}")
      c.drawString(100, 600, "Thank you for shopping with us!")
    
      c.save()
    
      msg.showinfo("PDF Generated", f"Bill has been generated and saved as {pdf_file}.")


FRAME_BG_COLOR = "#f5f1e9"  # Soft beige
LABEL_BG_COLOR = "#f5f1e9"  # Matching frame color
LABEL_FG_COLOR = "#4a4a4a"  # Dark gray for readability
BUTTON_BG_COLOR = "#669966"  # Muted green button background
BUTTON_FG_COLOR = "#ffffff"

class mainWindowStock(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill=tk.BOTH, expand=True)
        self.root.title("INVENTORY AT TREATS")
        center_window(1000, 620)

        self.configure(bg=BACKGROUND_COLOR)

        
        self.background_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.background_frame.place(relwidth=1, relheight=1)

        self.background_image = tk.PhotoImage(file="images/supermarket.png")
        self.background_label = tk.Label(self.background_frame, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.create_widgets()
        self.update_product_list()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)

    def create_widgets(self):
        input_frame = tk.Frame(self, bg=FRAME_BG,width=400)
        input_frame.pack(pady=5, padx=10)
        input_frame.pack_propagate(False)

        self.time_label = tk.Label(self, font=("Times New Roman", 12, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.time_label.pack(pady=(10, 0))
        self.update_time()

        tk.Label(input_frame, text="Item Name:", font=("Times New Roman", 12, "bold"), bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_name = tk.Entry(input_frame, width=25)
        self.entry_name.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Quantity:", font=("Times New Roman", 12, "bold"), bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_quantity = tk.Entry(input_frame, width=25)
        self.entry_quantity.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Price (₦):", font=("Times New Roman", 12, "bold"), bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_price = tk.Entry(input_frame, width=25)
        self.entry_price.grid(row=2, column=1, padx=5, pady=2)
        
        add_button = tk.Button(input_frame, text="Add Item", font=("Times New Roman", 12, "bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, relief="flat",width=12,command=self.add_item)
        add_button.grid(row=3, column=0, columnspan=2, pady=(6, 5), sticky="ew")
        tk.Label(self, text="Inventory Items and Quantities:", font=("Times New Roman", 12, "bold"), bg=FRAME_BG_COLOR, fg=LABEL_FG_COLOR).pack(pady=(10, 0))

        self.listbox = tk.Listbox(self, width=50, height=15)
        self.listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.listbox, orient=tk.VERTICAL,bg=FRAME_BG)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.logout_button = tk.Button(self, text="Log Out", font=("Times New Roman", 12, "bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat", command=self.logout)
        self.logout_button.pack(pady=10)

    def add_item(self):
        name = self.entry_name.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()
        if not name:
            msg.showerror("Input Error", "Item name cannot be empty.")
            return
        if not quantity.isdigit() or int(quantity) <= 0:
            msg.showerror("Input Error", "Quantity must be a positive integer.")
            return
        try:
            price_val = float(price)
            if price_val < 0:
                raise ValueError
        except ValueError:
            msg.showerror("Input Error", "Please enter a valid price (non-negative number).")
            return
        
        cur.execute("SELECT ItemQty FROM products WHERE ItemName = %s", (name,))
        result = cur.fetchone()
        if result:
            new_quantity = result[0] + int(quantity)
            cur.execute(
                "UPDATE products SET ItemQty = %s, ItemPrice = %s WHERE ItemName = %s",
                (new_quantity, price_val, name)
            )
        else:
            cur.execute(
                "INSERT INTO products (ItemName, ItemQty, ItemPrice) VALUES (%s, %s, %s)",
                (name, int(quantity), price_val)
            )
        con.commit()
        msg.showinfo("Success", f"Item '{name}' successfully added/updated.")

        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.update_product_list()
    
    def logout(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        welcomeWindow(self.root)
    
    def update_product_list(self):
        self.listbox.delete(0, tk.END)
        cur.execute("SELECT ItemName, ItemQty, ItemPrice FROM products ORDER BY ItemName")
        rows = cur.fetchall()
        if not rows:
            self.listbox.insert(tk.END, "No items in inventory.")
            return
        for ItemName, qty, price in rows:
            try:
                price = float(price) 
                self.listbox.insert(tk.END, f"{ItemName} - Quantity Left: {qty} - Price: ₦{price:.2f}")
            except ValueError:
                self.listbox.insert(tk.END, f"{ItemName} - Quantity Left: {qty} - Price: Invalid Price")

        








class mainWindowAdmin(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        center_window(800, 600)
        self.pack(fill=tk.BOTH, expand=True)
        self.root.title("SUPERVISING TREATS")

        self.configure(bg=BACKGROUND_COLOR)

        
        self.background_image = tk.PhotoImage(file="images/U.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1) 
        
        self.time_label = tk.Label(self, font=("Times New Roman", 12,"bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR)
        self.time_label.pack(pady=(10, 0))  
        self.update_time()
       
        self.staff_frame = tk.LabelFrame(self, text="Staff Management",font=("Times New Roman",12,"bold"), padx=10, pady=10,width=750, fg=TEXT_COLOR,bg=FRAME_BG_COLOR)
        self.staff_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.staff_listbox = tk.Listbox(self.staff_frame, width=50, height=10,bg=FRAME_BG_COLOR)
        self.staff_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.staff_scrollbar = tk.Scrollbar(self.staff_frame,bg=FRAME_BG_COLOR)
        self.staff_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.staff_listbox.config(yscrollcommand=self.staff_scrollbar.set)
        self.staff_scrollbar.config(command=self.staff_listbox.yview)

        self.load_staff()

        self.restrict_button = tk.Button(self.staff_frame, text="Restrict Login",font=("Times New Roman",10,"bold"),width=12, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,relief="flat", command=self.restrict_staff)
        self.restrict_button.pack(pady=10)
        
        self.unrestrict_button = tk.Button(self.staff_frame, text="Unrestrict Login", font=("Times New Roman", 10, "bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,width=12, relief="flat", command=self.unrestrict_staff)
        self.unrestrict_button.pack(pady=5)

        self.add_button = tk.Button(self.staff_frame, text="Add Staff", font=("Times New Roman", 10, "bold"), width=12, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat", command=self.add_staff)
        self.add_button.pack(pady=10)
        
        self.remove_button = tk.Button(self.staff_frame, text="Remove Staff", font=("Times New Roman", 10, "bold"), width=12, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat", command=self.remove_staff)
        self.remove_button.pack(pady=5)

        self.product_frame = tk.LabelFrame(self, text="Product Management",font=("Times New Roman",12,"bold"), padx=10, pady=10,fg=TEXT_COLOR,bg=FRAME_BG_COLOR)
        self.product_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.product_listbox = tk.Listbox(self.product_frame, width=50, height=10,bg=FRAME_BG_COLOR)
        self.product_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.product_scrollbar = tk.Scrollbar(self.product_frame,bg=FRAME_BG_COLOR)
        self.product_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_listbox.config(yscrollcommand=self.product_scrollbar.set)
        self.product_scrollbar.config(command=self.product_listbox.yview)

        self.load_products()
        
        self.add_product_button = tk.Button(self.product_frame, text="Add Product", font=("Times New Roman", 10, "bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, width=12, relief="flat", command=self.add_product)
        self.add_product_button.pack(pady=5)

        self.edit_button = tk.Button(self.product_frame, text="Edit Product",font=("Times New Roman",10,"bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,width=12,relief="flat", command=self.edit_product)
        self.edit_button.pack(pady=10)

        self.logout_button = tk.Button(self, text="Log Out",font=("Times New Roman",12,"bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,relief="flat", command=self.logout)
        self.logout_button.pack(pady=10)


    
    def update_time(self):
      current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      self.time_label.config(text=current_time)
      self.after(1000, self.update_time) 

    def logout(self):
        
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        welcomeWindow(self.root)
   
    def add_staff(self):
         add_window = tk.Toplevel(self.root)
         add_window.title("Add Staff")
         add_window.geometry("300x250")
         self.configure(bg=BACKGROUND_COLOR)
    
         tk.Label(add_window, text="First Name:", font=("Times New Roman", 12, "bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
         first_name_entry = tk.Entry(add_window)
         first_name_entry.pack(pady=5)
    
         tk.Label(add_window, text="Last Name:", font=("Times New Roman", 12, "bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
         last_name_entry = tk.Entry(add_window)
         last_name_entry.pack(pady=5)
    
         tk.Label(add_window, text="Email:", font=("Times New Roman", 12, "bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
         email_entry = tk.Entry(add_window)
         email_entry.pack(pady=5)

         def save_staff():
           first_name = first_name_entry.get()
           last_name = last_name_entry.get()
           email = email_entry.get()
           if not first_name or not last_name or not email:
               msg.showerror("Input Error", "Please fill in all fields.")
               return
           cur.execute("INSERT INTO staff (firstName, lastName, email, Restricted) VALUES (%s, %s, %s, FALSE)", (first_name, last_name, email))
           con.commit()
           msg.showinfo("Success", "Staff member added successfully.")
           add_window.destroy()
           self.load_staff()

         save_button = tk.Button(add_window, text="Add Staff", bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat", command=save_staff)
         save_button.pack(pady=10)


    def remove_staff(self):
        selection = self.staff_listbox.curselection()
        if not selection:
            msg.showwarning("Selection Error", "Please select a staff member to remove.")
            return
        selected_text = self.staff_listbox.get(selection[0])
        email = selected_text.split(" - ")[1] 
        cur.execute("DELETE FROM staff WHERE email = %s", (email,))
        con.commit()
        msg.showinfo("Success", f"{selected_text} has been removed from the staff.")
        self.load_staff()

    def load_staff(self):
        self.staff_listbox.delete(0, END)
        cur.execute("SELECT firstName, lastName, email FROM staff")
        rows = cur.fetchall()
        for first_name, last_name, email in rows:
            self.staff_listbox.insert(END, f"{first_name} {last_name} - {email}")

    def restrict_staff(self):
        selection = self.staff_listbox.curselection()
        if not selection:
            msg.showwarning("Selection Error", "Please select a staff member to restrict.")
            return
        selected_text = self.staff_listbox.get(selection[0])
        email = selected_text.split(" - ")[1] 

        
        cur.execute("UPDATE staff SET Restricted = TRUE WHERE email = %s", (email,))
        con.commit()
        msg.showinfo("Success", f"{selected_text} has been restricted from logging in.")
        self.load_staff()
     
    def unrestrict_staff(self):
        selection = self.staff_listbox.curselection()
        if not selection:
            msg.showwarning("Selection Error", "Please select a staff member to unrestrict.")
            return
        selected_text = self.staff_listbox.get(selection[0])
        email = selected_text.split(" - ")[1] 
        cur.execute("UPDATE staff SET Restricted = FALSE WHERE email = %s", (email,))
        con.commit()
        msg.showinfo("Success", f"{selected_text} has been unrestricted for logging in.")
        self.load_staff()


    def load_products(self):
        self.product_listbox.delete(0, END)
        cur.execute("SELECT ItemName, ItemQty, ItemPrice FROM products")
        rows = cur.fetchall()
        for item_name, qty, price in rows:
            self.product_listbox.insert(END, f"{item_name} - Qty: {qty} - Price: ₦{price}")
    
    def add_product(self):
        add_product_window = tk.Toplevel(self.root)
        add_product_window.title("Add Product")
        add_product_window.geometry("300x250")
        self.configure(bg=BACKGROUND_COLOR)
       
        tk.Label(add_product_window, text="Product Name:", font=("Times New Roman", 12, "bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        product_name_entry = tk.Entry(add_product_window)
        product_name_entry.pack(pady=5)
        tk.Label(add_product_window, text="Quantity:", font=("Times New Roman", 12, "bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        quantity_entry = tk.Entry(add_product_window)
        quantity_entry.pack(pady=5)
        tk.Label(add_product_window, text="Price:", font=("Times New Roman", 12, "bold"), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        price_entry = tk.Entry(add_product_window)
        price_entry.pack(pady=5)

        def save_product():
            product_name = product_name_entry.get()
            quantity = quantity_entry.get()
            price = price_entry.get()
            if not product_name or not quantity.isdigit() or float(price) < 0:
                msg.showerror("Input Error", "Please enter valid product name, quantity, and price.")
                return
            cur.execute("INSERT INTO products (ItemName, ItemQty, ItemPrice) VALUES (%s, %s, %s)", (product_name, int(quantity), float(price)))
            con.commit()
            msg.showinfo("Success", "Product added successfully.")
            add_product_window.destroy()
            self.load_products()
        save_button = tk.Button(add_product_window, text="Add Product", bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, relief="flat", command=save_product)
        save_button.pack(pady=10)

    def edit_product(self):
        selection = self.product_listbox.curselection()
        if not selection:
            msg.showwarning("Selection Error", "Please select a product to edit.")
            return
        selected_text = self.product_listbox.get(selection[0])
        item_name = selected_text.split(" - ")[0]  

        
        self.edit_product_window(item_name)

    def edit_product_window(self, item_name):
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Product: {item_name}")
        edit_window.geometry("300x200")
        self.configure(bg=BACKGROUND_COLOR)

        tk.Label(edit_window, text="New Quantity:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.pack(pady=5)

        tk.Label(edit_window, text="New Price:",font=("Times New Roman",12,"bold"),bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        price_entry = tk.Entry(edit_window)
        price_entry.pack(pady=5)

        def save_changes():
            new_qty = quantity_entry.get()
            new_price = price_entry.get()
            if not new_qty.isdigit() or float(new_price) < 0:
                msg.showerror("Input Error", "Please enter valid quantity and price.")
                return
            cur.execute("UPDATE products SET ItemQty = %s, ItemPrice = %s WHERE ItemName = %s",
                        (int(new_qty), float(new_price), item_name))
            con.commit()
            msg.showinfo("Success", "Product details updated successfully.")
            edit_window.destroy()
            self.load_products() 

        save_button = tk.Button(edit_window, text="Save Changes", bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,relief="flat",command=save_changes)
        save_button.pack(pady=10)




main=tk.Tk()
main.configure(bg="#fff")
welcomeWindow(main)
main.mainloop()


