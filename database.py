# This class deals with reading file, comparing files, and returning arrays with the content of the files
class Database():      
    def load_items_from_file(file_path): # Loads items from a file into an array, separating by the ";". Returns array regaurdless of content
        array = []
        try:
            with open(file_path, 'r') as file:
                items = file.read().split(';')                
            for i in range(len(items)):
                array.append(items[i])
            return array
        except FileNotFoundError:
            return array
    def food_array():            
        return Database.load_items_from_file("food_items.txt")
    def calorie_array():
        return Database.load_items_from_file("calorite_count.txt")
    def protein_array():
        return Database.load_items_from_file("protein_count.txt")
# This method compares a variable to a specific array and returns the index value of that array if it is found. Returns -1 if not found
    def compare_with_array(input_text, new_array): 
        if input_text in new_array:
            index = new_array.index(input_text)
            return index
        else:
            return -1
