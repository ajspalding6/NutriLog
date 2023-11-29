import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

from kivy.uix.widget import Widget
import datetime
# Import a database manipulation file
from database import Database

# Creates global arrays from files
food_array = Database.food_array()
calorie_array = Database.calorie_array()
protein_array = Database.protein_array()

class FoodList(ScrollView): # Creates a scrollable food list for the user to reference
    def __init__(self, **kwargs): # Initialzes the properties of ScrollView
        super(FoodList, self).__init__(**kwargs) 
        self.size_hint = (None, None)
        self.size = (300, 400)
        self.bar_width = 10
        self.grid = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.grid)

    def add_new_food_item(self, index): # Creates the widgets for a new food item
        size = (300, 60)


        new_food_item_layout = GridLayout(rows=2, size_hint=(None, None), size=size)

        horizontal1 = BoxLayout(
            orientation='horizontal', 
            size_hint=(None, None), 
            size=(size[0], size[1])
            )

        food_label = Label(
            text=food_array[index], 
            size_hint=(None, None), 
            size=(size[0] // 2, size[1] // 60),
            font_size=20,
            shorten=True,
            shorten_from='left',
            ellipsis_options={food_array[index]: '>dsafdsaf>', 'mosfdafade':'cendsfdfsdfdster'}
            )
        horizontal1.add_widget(food_label)

        filler = Widget(
            size_hint=(None, None),
            size=(size[0] // 7, size[1] // 2)
        )
        horizontal1.add_widget(filler)

        edit_button = Button(
            text="Edit", 
            size_hint=(None, None), 
            size=(size[0]// 8, size[1] // 2)
            )
        edit_button.bind(on_release=lambda btn: self.edit_food_list_item_popup_method(new_food_item_layout, index))
        horizontal1.add_widget(edit_button)

        delete_button = Button(
            text="Delete", 
            size_hint=(None, None), 
            size=(size[0] // 8, size[1] // 2)
            )
        delete_button.bind(on_release=lambda btn: self.delete_widget(new_food_item_layout))
        horizontal1.add_widget(delete_button)

        horizontal2 = BoxLayout(
            orientation='horizontal', 
            size_hint=(None, None), 
            size=(size[0], size[1] // 2)
            )

        calorie_label = Label(
            text=calorie_array[index] + " calories", 
            size_hint=(None, None), 
            size=(size[0] // 2, size[1] // 2)
            )
        horizontal2.add_widget(calorie_label)

        protein_label = Label(
            text=(protein_array[index] + "g of protein"), 
            size_hint=(None, None), 
            size=(size[0] // 2, size[1] // 2)
            )
        horizontal2.add_widget(protein_label)

        new_food_item_layout.add_widget(horizontal1)
        new_food_item_layout.add_widget(horizontal2)

        self.grid.add_widget(new_food_item_layout) # Adds the widgets and increases the grid height
        self.grid.height += size[1]

    def start_up(self): # Creates the necessary widgets if the file has content on start up
        for i in range(len(food_array)):
            if i > 0:
                self.add_new_food_item(i)

    def delete_widget(self, widget): # Deletes the widget from the food list ScrollView and writes into file
        if widget in self.grid.children:
            index = Database.compare_with_array(widget.children[1].children[2].text, food_array)
            self.grid.remove_widget(widget)
            self.grid.height -= widget.height
            if index < len(food_array):
                del food_array[index]
                del calorie_array[index]
                del protein_array[index]
                
                # Update data in files to match the widgets
                write_food_array = ';'.join(food_array)
                write_calorie_array = ';'.join(calorie_array)
                write_protein_array = ';'.join(protein_array)
                with open("food_items.txt", 'w') as food:
                    food.write(write_food_array)
                with open("calorite_count.txt", 'w') as calorie:
                    calorie.write(write_calorie_array)
                with open("protein_count.txt", 'w') as protein:
                    protein.write(write_protein_array)    

    def edit_widget(self, widget, index): # Edits the data the user selected 
        if widget in self.grid.children:
            index = Database.compare_with_array(widget.children[1].children[2].text, food_array)

            # Update the data arrays with the new values
            food_array[index] = self.new_food_input.text
            calorie_array[index] = self.new_calorie_input.text
            protein_array[index] = self.new_protein_input.text

            # Update the labels in the widget
            widget.children[1].children[2].text = self.new_food_input.text  # Update the food label
            widget.children[0].children[1].text = self.new_calorie_input.text + " calories" # Update the calorie label
            widget.children[0].children[0].text = self.new_protein_input.text + "g of protein" # Update the protein label

            # Rewrites arrays with separators to files
            write_food_array = ';'.join(food_array)
            write_calorie_array = ';'.join(str(calorie_array))
            write_protein_array = ';'.join(str(protein_array))
            with open("food_items.txt", 'w') as food:
                food.write(write_food_array)
            with open("calorite_count.txt", 'w') as calorie:
                calorie.write(write_calorie_array)
            with open("protein_count.txt", 'w') as protein:
                protein.write(write_protein_array)    
            self.edit_food_item_popup.dismiss()

    def edit_food_list_item_popup_method(self, widget, index): # Prompts the user for new values 
        # Creates a popup to enter the new values
        content = BoxLayout(orientation='vertical')
        self.new_food_input = TextInput(
            text=food_array[index], 
            hint_text="Food"
            )
        self.new_calorie_input = TextInput(
            text=calorie_array[index], 
            hint_text="Calories"
            )
        self.new_protein_input = TextInput(
            text=protein_array[index], 
            hint_text="Protein"
            )
        self.edited_items_enter_button = Button(
            text="Enter", 
            on_release= 
                (lambda btn: self.edit_widget(widget, index)) # Calls the data entry method
            )
        content.add_widget(self.new_food_input)
        content.add_widget(self.new_calorie_input)
        content.add_widget(self.new_protein_input)
        content.add_widget(self.edited_items_enter_button)
        self.edit_food_item_popup = Popup(
            title="Enter new values", 
            content=content, 
            size_hint=(None,None), 
            size=(400,400))
        self.edit_food_item_popup.open()

class Eating_Diary(ScrollView): # Creates a scrollable eating diary for the user to reference
    def __init__(self, **kwargs): # Initializes the properties of ScrollView and declares start up variables
        super(Eating_Diary, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (300, 400)
        self.bar_width = 10
        self.grid = GridLayout(cols=1, size_hint_y=None)
        self.pos_hint={'center_x':0.8, 'center_y':0.7}
        self.add_widget(self.grid)
        self.food_info_array = []
        self.widget_list1 = []
        self.calories_label = Label()
        self.counter = 0     
        
    def new_eaten_item(self, index, servings_size):
        self.counter += 1
        calories = int(servings_size) * int(calorie_array[index])
        protein =  int(servings_size) * int(protein_array[index])
        size = (300, 60)
        
        # Creates a gridlayout to hold all layouts
        new_eaten_item = GridLayout(rows=2, size_hint=(None, None), size=size)

        # Creates a box layout for the first three widgets
        food_edit_delete = BoxLayout(
            orientation='horizontal', 
            size_hint=(None, None), 
            size=(size[0], size[1] // 2))

        # Changes from 'serving' to 'servings' if necessary
        text = food_array[index] + ": " + servings_size + " serving"
        if int(servings_size) > 1:
            text = food_array[index] + ": " + servings_size + " servings"

        food_name = Label(
            text=food_array[index], 
            size_hint=(None, None), 
            size=(size[0] // 2, size[1] // 2)
            )
        food_edit_delete.add_widget(food_name)
        
        delete_button = Button(
            text="Delete", 
            size_hint=(None, None), 
            size=(size[0] // 4, 
            size[1] // 2),
            )
        delete_button.id = str(self.counter)
        delete_button.bind(on_release=lambda instance, btn_id=delete_button.id: self.delete_widget(btn_id, new_eaten_item))

        edit_button = Button(
            text="Edit", 
            size_hint=(None, None), 
            size=(size[0] // 4, size[1] // 2)
            )
        edit_button.bind(on_release=lambda btn: self.new_food_item_popup_method(new_eaten_item, servings_size, index, delete_button.id))
        
        food_edit_delete.add_widget(edit_button)
        food_edit_delete.add_widget(delete_button)

        # Creates a second boxlayout for the bottom two widgets
        cal_pro = BoxLayout(
            orientation='horizontal', 
            size_hint=(None, None), 
            size=(size[0], size[1] // 2)
        )
        calories_text = str(calories) + " calories"
        self.calories_label = Label(
                text=calories_text, 
                size_hint=(None, None), 
                size=(size[0] // 2, size[1] // 2)
                )
        cal_pro.add_widget(self.calories_label)
        
        protein_text = str(protein) + "g of protein"
        self.protein_label = Label(
            text=(str(protein) + "g of protein"), 
                size_hint=(None, None), 
                size=(size[0] // 2, size[1] // 2)
                )
        cal_pro.add_widget(self.protein_label)

        self.widget_list1.append(food_edit_delete)

        # Adds both boxlayouts to the gridlayout
        new_eaten_item.add_widget(food_edit_delete)
        new_eaten_item.add_widget(cal_pro)

        # Adds widgets and increases height of the grid
        self.grid.add_widget(new_eaten_item)
        self.grid.height += size[1]

        # Adds widget information to an array
        self.food_info = "NEW" + food_array[index] + ";" + servings_size + ";" + str(calories) + ";" + str(protein)
        self.food_info_array.append(self.food_info)
    
    def clear_diary_method(self, instance): # Clears the widgets from the screen and clears the file containing the data
        with open("eating_diary.txt", 'w+') as e_file:
                    e_file.close()

        self.grid.clear_widgets()
    
    def test(self): # Calls a method with parameters
        self.write_food_info_to_file(self.food_info_array[len(self.food_info_array)-1], 'a')
    
    def write_food_info_to_file(self, param, edit_type): # Writes whatever array was passed into the eating_diary file
        with open("eating_diary.txt", edit_type) as food_info:
            for i in range(len(param)):
                food_info.write(param[i])
        
    def delete_widget(self, widget_id, widget): # Deletes a widget from the eating diary ScrolLView and writes into file
        # Deletes the widget and adjusts grid height
        for i, layout in enumerate(self.widget_list1):
            if layout.children[0].id == widget_id:
                self.food_info_array.remove(self.food_info_array[i])
                self.grid.remove_widget(widget)
                self.grid.height -= widget.height

        # Writes the updated data into a file
        with open("eating_diary.txt", 'w+') as f:
            for i in range(len(self.food_info_array)):
                f.write(self.food_info_array[i])

    def edit_widget(self, widget, serving_size, widget_id): # Edits the data the user selected
        if widget in self.grid.children:
            index = Database.compare_with_array(widget.children[1].children[2].text, food_array)

            # Update the data arrays with the new values
            print(food_array[index])
            food_array[index] = self.new_food_input.text
            calorie_array[index] = int(calorie_array[index]) * int(serving_size)
            protein_array[index] = int(protein_array[index]) * int(serving_size)
            print(food_array[index])

            # Update the labels in the widget
            widget.children[1].children[2].text = self.new_food_input.text  # Update the food label
            widget.children[0].children[1].text = str(calorie_array[index]) + " caloires" # Update the calorie label
            widget.children[0].children[0].text = str(protein_array[index]) + "g of protein" # Update the protein label
            self.food_info_array[int(widget_id)-1] = "NEW" + food_array[index] + ";" + serving_size + ";" + str(calorie_array[index]) + ";" + str(protein_array[index])
            
            # Calls the method to write data into files, passing in the array and edit type
            self.write_food_info_to_file(self.food_info_array, 'w+')
    
    def new_food_item_popup_method(self, widget, seriving_size, index, widget_id): # Prompts the user for new values
        # Creates a popup to enter the new values
        content = BoxLayout(orientation='vertical')
        self.new_food_input = TextInput(
            text=food_array[index], 
            hint_text="Food"
            )
        self.new_serving_size = TextInput(
            text=seriving_size, 
            hint_text="Serving size"
            )
        self.edited_items_enter_button = Button(
            text="Enter", 
            on_release= lambda btn: self.edit_widget(widget, 
            self.new_serving_size.text, widget_id)
            ) # Calls the data entry method
        self.edited_items_enter_button.bind(on_press=self.close_popup)
        content.add_widget(self.new_food_input)
        content.add_widget(self.new_serving_size)
        content.add_widget(self.edited_items_enter_button)
        self.new_food_item_popup = Popup(
            title="Enter new values", 
            content=content, 
            size_hint=(None,None), 
            size=(400,400)
            )
        self.new_food_item_popup.open()

    def close_popup(self, instance): # Dismisses the edit item popup
        self.new_food_item_popup.dismiss()

    def read_from_file(self, filename): # Reads data from files to create the widgets for start up data
        # Read any data if it exists
        with open(filename, "r") as f:
            text = f.read()
        self.food_name=self.serving_size=calories=protein=None
        index = 0
        # Split blocks of data by the keyword "NEW"
        self.blocks = text.split("NEW")
        for block in self.blocks:
            i=0
            # Split the already-split blocks into lines
            lines = block.split(";")
            for line in lines:
                i += 1
                if i==1:
                    self.food_name = line
                    if line != "": # If data exists in the file
                        index = Database.compare_with_array(self.food_name, food_array)
                if i==2:
                    self.serving_size = line
                if i==3:
                    calories = line
                if i==4:
                    protein = line
                print("INdex:",index)
            if index!=0: # If the index returns a found value
                self.new_eaten_item(index, self.serving_size)
                
class Dashboard(FloatLayout):
    def __init__(self, **kwargs): # Initialize start up variables and create widgets
        super(Dashboard, self).__init__(**kwargs)
      
        self.food_list = FoodList()
        self.eaten_item = Eating_Diary()
        self.food_item_input = 0
        self.protein_input = 0
        self.calories_input = 0
        self.food_list.start_up()
        self.time()
        self.eaten_item.read_from_file("eating_diary.txt")
        self.protein_goal_num = "0"
        self.calorie_goal_num = "0"
        self.running_total_calories = 0
        self.running_total_protein = 0
        float_layout = FloatLayout()
        
        # Create start up widgets
        self.clear_diary = Button(
            text="Clear diary",
            size_hint=(None, None),
        )
        self.clear_diary.bind(on_press=self.are_you_sure)
        self.add_widget(self.clear_diary)

        self.food_input = TextInput(
            size_hint=(None, None),
            size=(200, 30),
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            hint_text="Food item",
            multiline=False
        )

        self.serving_size_input = TextInput(
            size_hint=(None, None),
            size=(200, 30),
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            hint_text="Serving size",
            multiline=False
        )

        enter_food_button = Button(
            size_hint=(None, None),
            size=(200, 60),
            text="Enter Food Item",
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        enter_food_button.bind(on_press=self.scan_array)
        
        eating_diary_label = Label(
            text="Eating Diary:",
            size_hint=(None, None),
            size=(200,40),
            pos_hint={'center_x':0.8, 'center_y':0.9}
        )

        self.entered_food_item = Label(
            size_hint=(None, None),
            text="filler",
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        food_list_label = Label(
            text="Food List",
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_y':0.9}
        )

        add_item_button = Button(
            text="Add Item",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={'center_y':0.9}
        )
        add_item_button.bind(on_press=self.food_search)

        self.current_food_input = Label(
            text=self.food_input.text
        )

        self.calorie_goal_label = Button(
            text="",
            size_hint=(None, None),
            size=(150, 30),
            pos_hint={'center_x':0.5, 'center_y':0.2}
        )
        self.calorie_goal_label.bind(on_press=lambda instance: self.protein_goal_popup(0))

        self.protein_goal_label = Button(
            text=("175/0"),
            size_hint=(None, None),
            size=(150, 40),
            pos_hint={'center_x':0.5, 'center_y':0.3}
        )
        self.protein_goal_label.bind(on_press=lambda instance: self.protein_goal_popup(1))

        # Add the scroll windows to a layout
        self.eating_diary_scroll = BoxLayout(orientation='vertical')
        self.eating_diary_scroll.pos_hint={'center_y':0.8}
        self.eating_diary_scroll.add_widget(eating_diary_label)
        self.eating_diary_scroll.add_widget(self.eaten_item)

        self.food_list_scroll = BoxLayout(orientation='vertical')
        self.food_list_scroll.pos_hint={'center_y':0.8}

        self.food_list_scroll.add_widget(food_list_label)
        self.food_list_scroll.add_widget(add_item_button)
        self.food_list_scroll.add_widget(self.food_list)

        # Add widgets and scroll widgets to float_layout 
        float_layout.add_widget(self.food_input)
        float_layout.add_widget(self.serving_size_input)
        float_layout.add_widget(enter_food_button)
        float_layout.add_widget(self.entered_food_item)
        float_layout.add_widget(self.current_food_input)
        float_layout.add_widget(self.food_list_scroll)
        float_layout.add_widget(self.eating_diary_scroll)
        float_layout.add_widget(self.protein_goal_label)
        float_layout.add_widget(self.calorie_goal_label)
        
        # Add entire layout to Dashboard
        self.add_widget(float_layout)

    def scan_array(self, instance): # Scan the array of food for the value entered by the user
        # Find what index calories and protein need to be to match the food item
        self.index1 = Database.compare_with_array(self.food_input.text, food_array)
        print(self.index1)

        if self.index1 < 0: # If the item is not found
            script = "Cannot locate " + self.food_input.text
            text = Label(text=script)
            ok_button = Button(
                text="Ok", 
                on_press=self.close_popup(self.food_not_found_popup)
                )
            
            self.food_not_found_popup = Popup(
                title="Food not found", 
                content=ok_button, 
                size_hint=(None, None), 
                size=(300,300)
                )
            self.food_not_found_popup.open()
            return False
        else: # If the item is found
            # Calculate protein and calories of the item
            self.calories = int(calorie_array[self.index1]) * int(self.serving_size_input.text)
            self.protein = int(protein_array[self.index1]) * int(self.serving_size_input.text)

            # Add the above values to the running total
            self.running_total_calories += self.calories
            self.running_total_protein += self.protein
            self.calorie_num = str(self.running_total_calories)
            self.protein_num = str(self.running_total_protein)
            self.protein_goal_label.text = ("175/" + self.protein_num)
            self.calorie_goal_label.text = ("2400/" + self.calorie_num)
            servings = "serving"
            if int(self.serving_size_input.text) > 1:
                servings = "servings"
            current_food_text = (food_array[self.index1] + 
                "\n" + self.serving_size_input.text + " " + servings + 
                "\n" + str(self.calories) + " calories\n" + 
                str(self.protein) + "g of protein")

            self.entered_food_item.text = current_food_text
            self.eaten_item.new_eaten_item(self.index1, self.serving_size_input.text)

            # Call a method with parameters that are only available in the class the method is in
            self.eaten_item.test()

            # Call the time method for handling new days
            self.time()

            # Reset the input fields textboxes to be empty
            self.food_input.text = ""
            self.serving_size_input.text = ""
    
    def close_popup(self, instance, popup): # Dismiss whatever popup is passed in
        popup.dismiss()
        
    def add_new_structure(self, instance): # Add a food item to the food list when called
        self.food_list.add_new_food_item()

    def food_search(self, instance): # The popup for adding a food item
        content = BoxLayout(orientation="vertical")

        self.food_item_input = TextInput(
            hint_text="New food itme"
            )
        self.calories_input = TextInput(
            hint_text="Calories")
        self.protein_input = TextInput(hint_text="Protein"
        )
        self.add_food_submit_button = Button(
            text="Enter"
            )
        self.add_food_submit_button.bind(on_press=self.validate_input)

        # Add the TextInput widgets to the content layout
        content.add_widget(self.food_item_input)
        content.add_widget(self.calories_input)
        content.add_widget(self.protein_input)
        content.add_widget(self.add_food_submit_button)

        # Create and open the Popup
        self.add_food_popup = Popup(
            title="Add food item", 
            content=content, 
            size_hint=(None, None), 
            size=(400, 400)
            )
        self.add_food_popup.open()

    def validate_input(self, instance): # Make sure the entered values are mathematically correct
        
        food = self.food_item_input.text
        calories = self.calories_input.text
        protein = self.protein_input.text
        cal = pro = foo = False
        try: # Make sure food is a string
            food = str(food)
            foo = True
        except ValueError:
            pass
        try: # Make sure calories is an integer
            calories = int(calories)
            cal = True
        except ValueError:
            pass
        try: # Make sure protein is an integer
            protein = int(protein)
            pro = True
        except ValueError:
            pass
        if cal and pro and foo:
            print("Youre awsome")
            self.add_food_item(str(food), str(calories), str(protein))
        else:
            self.reset()
            # If the inputs are not the correct type, change the hint_text to remind the user
            self.food_item_input.hint_text = "Must be a word"
            self.calories_input.hint_text = "Must be a number"
            self.calories_input.hint_text = "Must be a number"

    def add_food_item(self, food, calorie, protein): # Call popup promting user for item, calorie and protein

        food_array
        calorie_array
        protein_array
        food_array.append(food)
        calorie_array.append(calorie)
        protein_array.append(protein)
        self.food_list_text = "\n".join(food_array)
        self.write_arrays_in_file()
        self.food_list.add_new_food_item(len(food_array)-1)
        self.add_food_popup.dismiss()

    def write_arrays_in_file(self): # Write the updated food, calorie, and protein array in their files
        
        write_food_array = ';'.join(food_array)
        write_calorie_array = ';'.join(calorie_array)
        write_protein_array = ';'.join(protein_array)
        with open("food_items.txt", 'w') as food:
            food.write(write_food_array)
        with open("calorite_count.txt", 'w') as calorie:
            calorie.write(write_calorie_array)
        with open("protein_count.txt", 'w') as protein:
            protein.write(write_protein_array)

    def protein_goal_popup(self, param): # Create the popup for editing calorie/protein goals
        if param > 0:
            text= "Protein goal"
        else:
            text= "Calorie goal"
        self.protein_popup_input = TextInput(hint_text=text)
        protein_popup_enter_button =  Button(text="Enter")
        content=BoxLayout(orientation='vertical')
        content.add_widget(self.protein_popup_input)
        content.add_widget(protein_popup_enter_button)
        self.protein_popup = Popup(
            title="Goal",
            content=content,
            size=(400, 400),
            size_hint=(None, None)
            )    
        protein_popup_enter_button.bind(on_press=lambda instance: self.validate_protein_input(self.protein_popup_input, param))
        self.protein_popup.open()
    
    def validate_protein_input(self, input_text, param): # Based on param, add data to the respective goal labels
        input = input_text.text

        # Make sure the goal is a number
        try: 
            input = int(input)
            pro = True
        except ValueError:
            self.protein_popup_input.hint_text = "Must be a number"
            pro = False

        if pro:
            if param > 0: # 0 for protein
                self.protein_popup_input.text = str(self.protein_popup_input.text)
                self.protein_goal_label.text = (str(self.protein_popup_input.text) + "/" + self.protein_num)
            else: # 1 for calories
                self.protein_popup_input.text = str(self.protein_popup_input.text)
                self.calorie_goal_label.text = (str(self.protein_popup_input.text) + "/" + self.calorie_num)
            self.protein_popup.dismiss()
    
    def time(self): # Deals with time manipulation and testing 
        current_time = datetime.datetime.now().strftime("%d") # Sets the current time
        with open("time_file.txt", 'r+') as file:
            text = file.read() # Reads the time inputted to the file
            if str(text) != str(current_time): # If they are the same days, pass. If not, clear the eating diary and input a new time to the time file
                with open("eating_diary.txt", 'w+') as e_file:
                    e_file.close()
                with open("time_file.txt", 'w') as f:
                    print("overwrittem")
                    f.write(str(current_time))

    def are_you_sure(self, instance): # Creates a popup verifying the user wants to clear the food diary
        content = BoxLayout(orientation='vertical')
        verify_label  = Label(
            text="Are you sure you want to \nclear ALL food entries?\n\nThis action CANNOT be undone",
            halign='center'
        )
        yes_button = Button(
            text = "YES",
            on_press=self.button_press
        )
        no_button = Button(
            text="NO",
            on_press=self.close_verify_popup
        )
        content.add_widget(verify_label)
        content.add_widget(yes_button)
        content.add_widget(no_button)
        self.are_you_sure_popup = Popup(
            title='Verify',
            content=content,
            size=(300,300),
            size_hint=(None,None)
        )
        self.are_you_sure_popup.open()
    
    def button_press(self, instance): # Calls two methods on a button press
        self.eaten_item.clear_diary_method(instance)
        self.close_verify_popup(instance)
    
    def close_verify_popup(self, instance): # Dismisses the the verify popup
        self.are_you_sure_popup.dismiss()

class TrackerApp(App):
    def build(self):
        return Dashboard()

if __name__ == '__main__':
    TrackerApp().run()