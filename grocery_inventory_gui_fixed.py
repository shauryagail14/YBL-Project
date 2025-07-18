import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class Product:
    def __init__(self, name="Milk", category="Dairy", expiry_date=None, stock_quantity=10, supplier="ABC Dairy"):
        self.name = name
        self.category = category
        self.expiry_date = expiry_date or (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.stock_quantity = stock_quantity
        self.supplier = supplier


class InventoryManager:
    def __init__(self):
        self.products = [
            Product("Milk", "Dairy", (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"), 15, "ABC Dairy"),
            Product("Bread", "Bakery", (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"), 20, "XYZ Bakery"),
            Product("Eggs", "Dairy", (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"), 30, "ABC Dairy"),
            Product("Apples", "Produce", (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"), 25, "Fresh Farms"),
            Product("Chicken", "Meat", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), 12, "Meat Co"),
        ]

    def get_expiring_products(self, days_threshold=7):
        today = datetime.now()
        threshold_date = today + timedelta(days=days_threshold)
        expiring = []
        
        for product in self.products:
            product_date = datetime.strptime(product.expiry_date, "%Y-%m-%d")
            if product_date <= threshold_date:
                expiring.append(product)
        
        return expiring
    
    def get_low_stock_products(self, threshold=15):
        return [p for p in self.products if p.stock_quantity < threshold]
    
    def get_all_products(self):
        return self.products
    
    def add_product(self, product):
        self.products.append(product)
    
    def update_product(self, product_name, new_quantity):
        for product in self.products:
            if product.name.lower() == product_name.lower():
                product.stock_quantity = new_quantity
                return True
        return False


class InventoryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FreshMart Retail - Inventory Manager")
        self.root.geometry("1000x700")
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.inventory_manager = InventoryManager()
        
        self.create_menu()
        self.show_dashboard()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Dashboard menu
        menubar.add_command(label="Dashboard", command=self.show_dashboard)
        
        # Inventory menu
        inventory_menu = tk.Menu(menubar, tearoff=0)
        inventory_menu.add_command(label="View All Products", command=self.show_all_products)
        inventory_menu.add_command(label="Add New Product", command=self.show_add_product)
        inventory_menu.add_command(label="Update Stock", command=self.show_update_stock)
        menubar.add_cascade(label="Inventory", menu=inventory_menu)
        
        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        reports_menu.add_command(label="Expiring Soon", command=self.show_expiring_products)
        reports_menu.add_command(label="Low Stock", command=self.show_low_stock)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        
        self.root.config(menu=menubar)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()
        
        title = ttk.Label(self.main_frame, text="DASHBOARD", style='Header.TLabel')
        title.pack(pady=20)
        
        # Create dashboard widgets
        dashboard_frame = ttk.Frame(self.main_frame)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Summary cards
        summary_frame = ttk.Frame(dashboard_frame)
        summary_frame.pack(fill=tk.X, pady=10)
        
        total_products = len(self.inventory_manager.get_all_products())
        expiring_soon = len(self.inventory_manager.get_expiring_products(7))
        low_stock = len(self.inventory_manager.get_low_stock_products(15))
        
        self.create_summary_card(summary_frame, "Total Products", total_products, "#4e73df")
        self.create_summary_card(summary_frame, "Expiring Soon", expiring_soon, "#f6c23e")
        self.create_summary_card(summary_frame, "Low Stock", low_stock, "#e74a3b")
        
        # Recent activity frame
        activity_frame = ttk.LabelFrame(dashboard_frame, text="Recent Activity", padding=10)
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Name", "Category", "Expiry Date", "Stock", "Supplier")
        tree = ttk.Treeview(activity_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        
        for product in self.inventory_manager.get_all_products()[:5]:  # Show first 5 products
            tree.insert("", tk.END, values=(
                product.name, 
                product.category, 
                product.expiry_date, 
                product.stock_quantity, 
                product.supplier
            ))
        
        scrollbar = ttk.Scrollbar(activity_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

    def create_summary_card(self, parent, title, value, color):
        card = ttk.Frame(parent, relief=tk.RAISED, borderwidth=2)
        card.pack(side=tk.LEFT, expand=True, fill=tk.Y, padx=5)
        
        title_label = ttk.Label(card, text=title, font=('Arial', 10))
        title_label.pack(pady=(5, 0))
        
        value_label = ttk.Label(card, text=str(value), font=('Arial', 24, 'bold'), foreground=color)
        value_label.pack(pady=(0, 5))

    def show_all_products(self):
        self.clear_main_frame()
        
        title = ttk.Label(self.main_frame, text="ALL PRODUCTS", style='Header.TLabel')
        title.pack(pady=20)
        
        # Search and filter frame
        filter_frame = ttk.Frame(self.main_frame)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(filter_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Search", command=lambda: self.search_products(search_entry.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Refresh", command=self.show_all_products).pack(side=tk.LEFT, padx=5)
        
        # Products table
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Name", "Category", "Expiry Date", "Stock", "Supplier")
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=150, anchor=tk.CENTER)
        
        for product in self.inventory_manager.get_all_products():
            self.products_tree.insert("", tk.END, values=(
                product.name, 
                product.category, 
                product.expiry_date, 
                product.stock_quantity, 
                product.supplier
            ))
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)

    def search_products(self, search_term):
        if not search_term:
            return
        
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
            
        for product in self.inventory_manager.get_all_products():
            if search_term.lower() in product.name.lower() or search_term.lower() in product.category.lower():
                self.products_tree.insert("", tk.END, values=(
                    product.name, 
                    product.category, 
                    product.expiry_date, 
                    product.stock_quantity, 
                    product.supplier
                ))

    def show_expiring_products(self):
        self.clear_main_frame()
        
        title = ttk.Label(self.main_frame, text="PRODUCTS EXPIRING SOON (within 7 days)", style='Header.TLabel')
        title.pack(pady=20)
        
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Name", "Category", "Expiry Date", "Stock", "Supplier")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)
        
        for product in self.inventory_manager.get_expiring_products(7):
            tree.insert("", tk.END, values=(
                product.name, 
                product.category, 
                product.expiry_date, 
                product.stock_quantity, 
                product.supplier
            ))
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

    def show_low_stock(self):
        self.clear_main_frame()
        
        title = ttk.Label(self.main_frame, text="LOW STOCK PRODUCTS (<15 items)", style='Header.TLabel')
        title.pack(pady=20)
        
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Name", "Category", "Expiry Date", "Stock", "Supplier")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)
        
        for product in self.inventory_manager.get_low_stock_products(15):
            tree.insert("", tk.END, values=(
                product.name, 
                product.category, 
                product.expiry_date, 
                product.stock_quantity, 
                product.supplier
            ))
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

    def show_add_product(self):
        self.clear_main_frame()
        
        title = ttk.Label(self.main_frame, text="ADD NEW PRODUCT", style='Header.TLabel')
        title.pack(pady=20)
        
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        # Form fields
        fields = [
            ("Name", "entry"),
            ("Category", "entry"),
            ("Expiry Date (YYYY-MM-DD)", "entry"),
            ("Stock Quantity", "entry"),
            ("Supplier", "entry")
        ]
        
        self.entry_widgets = {}
        for i, (label_text, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            if widget_type == "entry":
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                self.entry_widgets[label_text] = entry
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save_product).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.show_dashboard).pack(side=tk.LEFT, padx=10)

    def save_product(self):
        try:
            name = self.entry_widgets["Name"].get()
            category = self.entry_widgets["Category"].get()
            expiry_date = self.entry_widgets["Expiry Date (YYYY-MM-DD)"].get()
            stock_quantity = int(self.entry_widgets["Stock Quantity"].get())
            supplier = self.entry_widgets["Supplier"].get()
            
            if not all([name, category, expiry_date, supplier]):
                messagebox.showwarning("Warning", "Please fill in all fields")
                return
                
            new_product = Product(name, category, expiry_date, stock_quantity, supplier)
            self.inventory_manager.add_product(new_product)
            
            messagebox.showinfo("Success", "Product added successfully!")
            self.show_all_products()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values (stock must be a number)")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_update_stock(self):
        self.clear_main_frame()
        
        title = ttk.Label(self.main_frame, text="UPDATE PRODUCT STOCK", style='Header.TLabel')
        title.pack(pady=20)
        
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        # Product selection
        ttk.Label(form_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.product_combobox = ttk.Combobox(form_frame, values=[p.name for p in self.inventory_manager.get_all_products()])
        self.product_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # New quantity
        ttk.Label(form_frame, text="New Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Update", command=self.update_stock).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.show_dashboard).pack(side=tk.LEFT, padx=10)

    def update_stock(self):
        product_name = self.product_combobox.get()
        new_quantity = self.quantity_entry.get()
        
        if not product_name or not new_quantity:
            messagebox.showwarning("Warning", "Please select a product and enter a quantity")
            return
            
        try:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                raise ValueError("Quantity cannot be negative")
                
            if self.inventory_manager.update_product(product_name, new_quantity):
                messagebox.showinfo("Success", "Stock quantity updated successfully!")
                self.show_all_products()
            else:
                messagebox.showerror("Error", "Product not found")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity: {str(e)}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = InventoryGUI()
    app.run()
