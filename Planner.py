import customtkinter as ctk
import json
import os
import time
from PIL import Image

# Item visual da lista de tarefas
class List_Item(ctk.CTkFrame):

	def __init__(self, master, desc='Tarefa', date='', **kwargs):
		super().__init__(master, **kwargs)
		self.desc = desc
		self.data = date

		self.create_widgets(desc,date)

	def create_widgets(self,desc='Tarefa', date=''):
		self.configure(corner_radius=10, fg_color="#E0E0E0", height=60)
		

		self.label = ctk.CTkLabel(self, text=f"{desc} - {date} ", anchor="w", justify="left")
		self.bt_remove = ctk.CTkButton(self, text="",width=25,height=25,command=self.destroy,fg_color='red',image=self.master.master.master.master.master.master.icon_trash)

		self.label.pack(side='left', padx=10, pady=10)
		self.bt_remove.pack(anchor='center' ,side='right', padx=10, pady=10)

		self.pack(expand=True,fill="x", pady=5)

	def destroy(self):
		if self in self.master.master.items:
			self.master.master.items.remove(self)
		return super().destroy()

# Container de categoria que agrupa vários itens
class List_Categ(ctk.CTkFrame):
	def __init__(self, master, title="Categoria", **kwargs):
		super().__init__(master, **kwargs)
		self.desc = title
		self.create_widgets(title)
		self.items = []


	def create_widgets(self, title):
		self.configure(corner_radius=10, fg_color="#D0D0D0")
		self.bt_remove = ctk.CTkButton(self, width=25,height=25 , text="",image=self.master.master.master.master.icon_trash, command=self.destroy, fg_color='red')

		self.title_label = ctk.CTkLabel(self, text=title, anchor="w", font=ctk.CTkFont(size=32, weight="bold"))
		icon = ctk.CTkImage(dark_image=Image.open("./icons/plus.png"), size=(20, 20))
		self.bt_open_add = ctk.CTkButton(self, width=40, text='', image=self.master.master.master.master.icon_plus,command=self.open_frame)
		
		self.add_items = ctk.CTkFrame(self, fg_color="transparent")
		self.items_frame = ctk.CTkFrame(self, fg_color="transparent")

		self.entry_item = ctk.CTkEntry(self.add_items, width=200, placeholder_text='descricao tarefa')
		self.bt_add_item = ctk.CTkButton(self.add_items, width=40, text='Add Tarefas', command=self.add_tarefa)

		self.bt_add_item.pack(side='right',fill="x",padx=10)
		self.entry_item.pack(side='right',fill="x",padx=10)

		self.items_frame.pack(side='bottom',fill="both", expand=True, padx=10, pady=(0, 10))
		self.bt_remove.pack(anchor='center',side='left',fill="x", padx=10, pady=5)
		self.title_label.pack(side='left',fill="x", padx=10, pady=5)
		self.bt_open_add.pack(side='right',fill="x", padx=10, pady=5)

		self.add_items.pack_forget()

		self.pack(side='bottom',padx=10, pady=10, fill="x", expand=True)
	
	def open_frame(self):
		self.bt_open_add.configure(image=self.master.master.master.master.icon_up,command=self.close_frame)
		self.add_items.pack(side='bottom',fill="both", expand=True, padx=10, pady=(0, 10),after=self.items_frame)
	
	def close_frame(self):
		self.bt_open_add.configure(image=self.master.master.master.master.icon_plus,command=self.open_frame)
		self.add_items.pack_forget()

	def add_tarefa(self):
		date = time.strftime('%H:%M de %d/%m/%y')
		desc = self.entry_item.get()
		self.entry_item.delete(0,ctk.END)
		self.add_item(desc, date)


	def add_item(self, desc = str, date = '', commit = True):
		item = List_Item(self.items_frame, desc=desc, date=date)
		if commit:
			self.items.append(item)
			self.master.master.master.master.save_tasks()

	def clear_items(self):
		for widget in self.items_frame.winfo_children():
			widget.destroy()

	def destroy(self):
		self.master.master.master.master.categorias.remove(self)
		return super().destroy()

# App principal
class PlannerApp(ctk.CTk):
	PLANNER_FILE = "planner.json"
	icon_plus = ctk.CTkImage(dark_image=Image.open("./icons/plus.png"), size=(20, 20))
	icon_up = ctk.CTkImage(dark_image=Image.open("./icons/menu-up.png"), size=(20, 20))
	icon_trash = ctk.CTkImage(dark_image=Image.open("./icons/trash-can.png"), size=(20, 20))
	categorias = []

	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode("light")
		ctk.set_default_color_theme("blue")
		self.protocol("WM_DELETE_WINDOW", self.on_close)
		self.create_widgets()
		self.load_tasks()

	def on_close(self):
		self.save_tasks()
		self.destroy()

	def create_widgets(self):
		self.title("Planner")

		self.label = ctk.CTkLabel(self, text='Planner',anchor='w',font = ctk.CTkFont(size=74, weight="bold"), height=40, fg_color='transparent')

		self.add_catego = ctk.CTkFrame(self)
		self.barra_edit = ctk.CTkFrame(self)
		self.frame_catego = ctk.CTkScrollableFrame(self,label_text='LISTA DE CATEGORIAS',width=400,height=400)

		self.label_add_catego = ctk.CTkLabel(self.barra_edit, text='Adicionar Categoria',width=80, fg_color='transparent')
		self.bt_add_catego = ctk.CTkButton(self.barra_edit, text='',image=self.icon_plus, width=40,command=self.open_frame)

		self.label.pack(fill='x',padx=(10,),pady=40)
		self.bt_add_catego.pack(side='right',padx=(0,40),pady=10)
		self.label_add_catego.pack(side='right',padx=(0,10),pady=10)
		
		self.barra_edit.pack(fill='x')
		self.frame_catego.pack(expand=True,fill='both')

		self.add_button = ctk.CTkButton(self.add_catego, text="Adicionar Categoria", command=self.add_categoria)
		self.catego_entry = ctk.CTkEntry(self.add_catego, placeholder_text="Descrição da Categoria", width=400)

		self.catego_entry.pack(side='right', fill='x',padx=5,pady=5)
		self.add_button.pack(side='right',padx=5,pady=5)
		
	def open_frame(self):
		self.bt_add_catego.configure(image=self.icon_up,command=self.close_frame)
		self.add_catego.pack(fill='x',after=self.barra_edit)
	
	def close_frame(self):
		self.bt_add_catego.configure(image=self.icon_plus,command=self.open_frame)
		self.add_catego.pack_forget()

	def add_categoria(self):
		desc = self.catego_entry.get()
		self.catego_entry.delete(0,ctk.END)


		if desc and desc != '':
			catego = List_Categ(self.frame_catego,title=desc)
			catego.add_item('Adicione Tarefas A esta categoria',commit=False)

			self.categorias.append(catego)

			self.save_tasks()

			self.catego_entry.delete(0, ctk.END)

	def save_tasks(self):
		#pegando os mcomponentes e transformando em uma unica variavel
		tasks = {}
		for catego in self.categorias:
			if len(catego.items) != 0 :
				items = [(tarefa.desc,tarefa.data) for tarefa in catego.items]
				tasks[catego.desc] = items
			else:
				tasks[catego.desc] = []

		with open(self.PLANNER_FILE, "w", encoding="utf-8") as f:
			json.dump(tasks, f, indent=4)

	def load_from_bd(self):
		if os.path.exists(self.PLANNER_FILE):
			with open(self.PLANNER_FILE, "r", encoding="utf-8") as f:
				return json.load(f)
		return {"Categoria":[("items exemplo","Data exemplo"),("Lapis",'14:50 de 09/12/2024')]}
	
	def load_tasks(self):
		tasks = self.load_from_bd()

		for catego,tarefas in tasks.items():
			task_group = List_Categ(self.frame_catego, title=f"{catego}")
			self.categorias.append(task_group)
			
			for tarefa in tarefas:
				tarefa_descricao = tarefa[0]
				tarefa_data = tarefa[1]
				task_group.add_item(desc=tarefa_descricao, date=tarefa_data)

			


if __name__ == "__main__":
	app = PlannerApp()
	app.mainloop()
