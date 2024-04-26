import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStatusBar, QTableWidget, QTableWidgetItem,QTextEdit,QComboBox


class ProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Add Product')
        self.setGeometry(200,100,600,400)
        # Create the main widget and set it as the central widget of the window
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        #main_widget.setGeometry(360,450,200,300)


        # Create the layout for the widget
        main_layout = QVBoxLayout(main_widget)

        self.category_combo_box = QComboBox(self)
        self.category_combo_box.addItem('Phone')
        self.category_combo_box.addItem('TV')
        self.category_combo_box.addItem('PC')
        self.category_combo_box.addItem('Housewares')
       
        
        # Create a brand combo box
        self.brand_combo_box = QComboBox(self)
        

        # Set up signal-slot connections
        self.category_combo_box.currentIndexChanged.connect(self.update_brands)

        # Initialize the brands for the first category
        #self.update_brands()



        # Create the labels and line edits for the product name,price,code,staock amount,marka,kategori
        productCode_label =QLabel("Product Code:",main_widget)
        self.pr_code_edit =QLineEdit(main_widget)
        name_label = QLabel('Product Name:', main_widget)
        self.name_edit = QLineEdit(main_widget)
        stock_amount=QLabel('Stock Amount')
        self.stock_amount_edit=QLineEdit(main_widget)    
        product_expln =QLabel("Product Explain:",main_widget)
        self.productexpl_textedit=QTextEdit(main_widget)
        #self.productexpl_textedit.setGeometry(50,75,100,200)
        price_label = QLabel('Product Price:', main_widget)
        self.price_edit = QLineEdit(main_widget)
        cmbmarka_label =QLabel("Brand")
        cmbKategory_label =QLabel("Kategory")
        
            

            # Create the layout for the labels and line edits
        input_layout = QVBoxLayout()
        input_layout.addWidget(productCode_label)            
        input_layout.addWidget(self.pr_code_edit)
        input_layout.addWidget(name_label)
        input_layout.addWidget(self.name_edit)
        input_layout.addWidget(price_label)
        input_layout.addWidget(self.price_edit)
        input_layout.addWidget(stock_amount)
        input_layout.addWidget(self.stock_amount_edit)
        input_layout.addWidget(cmbKategory_label)
        input_layout.addWidget(self.category_combo_box)
        input_layout.addWidget(cmbmarka_label)
        input_layout.addWidget(self.brand_combo_box)


        input_layout.addWidget(product_expln)
        input_layout.addWidget(self.productexpl_textedit)




        # Create the button to add the product
        add_button = QPushButton('Add Product', main_widget)
        add_button.clicked.connect(self.add_product)

        show_button =QPushButton("Show Products",main_widget)
       # show_button.clicked.connect(self.kayıt_listele)

        delete_button =QPushButton("Delete Product",main_widget)
        delete_button.clicked.connect(self.delete_product)
        # Create the layout for the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(add_button)
        button_layout.addWidget(show_button)
        button_layout.addWidget(delete_button)
        # Add the input and button layouts to the main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)

        # Create the table to display the products
        self.table = QTableWidget(main_widget)
        self.table.setColumnCount(7)
        
        self.table.setHorizontalHeaderLabels(['Product Code','Product Name', 'Product Price','Stock Amount','Product Explain','Marka','Kategori'])
        main_layout.addWidget(self.table)
        
        # Create the database connection and table
        self.connection = sqlite3.connect('products.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS products (urunKodu int,name text,price int,stokMiktarı int,urunAçıklaması text,marka text,kategori text)')

        # Load the products into the table
        self.load_products()

        # Create the status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        
    def add_product(self):
        ürünkodu =self.pr_code_edit.text()
        name = self.name_edit.text()
        price = self.price_edit.text()
        Ürünaçıklması =self.productexpl_textedit.toPlainText()
        stokMiktarı =self.stock_amount_edit.text()
        self.category_combo_box.currentIndexChanged.connect(self.update_brands)
        self.update_brands()




        marka =self.brand_combo_box.currentText()
        kategori =self.category_combo_box.currentText()
        # Validate that the name and price are not empty
        if not name:
            self.show_error('Product name cannot be empty')
            

        if not price:
            self.show_error('Product price cannot be empty')
            
        try:
            price = float(price)
        except ValueError:
            self.show_error('Product price must be a number')
            
        

   
        # Add the product to the database
        self.cursor.execute('INSERT INTO products (urunKodu,name,price,stokMiktarı,urunAçıklaması,marka,kategori) VALUES (?,?,?,?,?,?,?)', (ürünkodu,name, price,stokMiktarı,Ürünaçıklması,marka,kategori))
        self.connection.commit()

        # Clear the input fields
        self.name_edit.clear()
        self.price_edit.clear()
        self.productexpl_textedit.clear()
        self.pr_code_edit.clear()
        self.stock_amount_edit.clear()
        self.brand_combo_box.clear()
       

        # Show a message in the status bar
        self.status_bar.showMessage('Product added successfully',msecs=3000)

        # Reload the products into the table
        self.load_products()


    def delete_product(self):
        selected_row =self.table.currentRow()

        if selected_row >=0:
            ürünkodu =self.table.item(selected_row,0).text()

            # database commits
            self.cursor.execute("""DELETE FROM products WHERE urunKodu=?""",(ürünkodu,))
            self.connection.commit()

            self.table.removeRow(selected_row)
            self.status_bar.showMessage("Product deleted",msecs= 3000)

        else:
            self.show_error("no product deleted")     

    def show_error(self, message):
        # Show an error message in a popup dialog
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle('Error')
        error_dialog.setText(message)
        error_dialog.exec()




    def load_products(self):
        # Clear the table
        self.table.setRowCount(0)

        # Load the products from the database
        self.cursor.execute('SELECT urunKodu,name,price,stokMiktarı,urunAçıklaması,marka,kategori FROM products')
        products = self.cursor.fetchall()

        # Add the products to the table
        for row, product in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(product[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(product[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(product[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(product[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(product[4])))
            self.table.setItem(row, 5, QTableWidgetItem(str(product[5])))
            self.table.setItem(row, 6, QTableWidgetItem(str(product[6])))
    
   
       
    def update_brands(self):
        # Get the selected category
        category = self.category_combo_box.currentText()

        # Clear the existing brands
        self.brand_combo_box.clear()

        # Add the brands for the selected category
        if category=="Phone":
                
                self.brand_combo_box.addItem("Apple")
                self.brand_combo_box.addItem("Samsung")
                self.brand_combo_box.addItem("Huawei")
                self.brand_combo_box.addItem("Lg")
                self.brand_combo_box.addItem("Nokia")
                self.brand_combo_box.addItem("Oppo")
                self.brand_combo_box.addItem("Realme")
                self.brand_combo_box.addItem("Xioami")
        elif category=="TV":
               
                self.brand_combo_box.addItem("Samsung")    
                self.brand_combo_box.addItem("LG")    
                self.brand_combo_box.addItem("Philips")    
                self.brand_combo_box.addItem("Sony")    
                self.brand_combo_box.addItem("Grunding")    
                self.brand_combo_box.addItem("Vestel")    
        elif category=="PC":
               
                self.brand_combo_box.addItem("Apple")
                self.brand_combo_box.addItem("Hp")
                self.brand_combo_box.addItem("Huawei")
                self.brand_combo_box.addItem("Asus Rog")
                self.brand_combo_box.addItem("Dell")
                self.brand_combo_box.addItem("Monster")
                self.brand_combo_box.addItem("Lenovo")
        elif category=="Housewares":
               
                self.brand_combo_box.addItem("Samsung")
                self.brand_combo_box.addItem("Siemens")
                self.brand_combo_box.addItem("Bosch")
                self.brand_combo_box.addItem("Profilo")
                self.brand_combo_box.addItem("Vestel")
                self.brand_combo_box.addItem("Arçelik")
                self.brand_combo_box.addItem("Beko")

    

app = QApplication(sys.argv)
window =ProductWindow()
window.show()
sys.exit(app.exec())