#NutriLog
Overview
This is a simple Python application for tracking your food intake. It provides a user interface where you can manage a list of food items, record the amount you've eaten, and keep track of the calories and protein consumed. The app uses the Kivy framework for the graphical user interface.

Features
Food List: Maintain a list of different food items.
Eating Diary: Record your daily food intake with serving sizes, calories, and protein content.
Editing and Deleting: Easily edit or delete entries from both the food list and eating diary.
Goals: Set and track your daily goals for calories and protein.
Requirements
Python 3
Kivy

Add Food Items:
Click on "Add Item" to add new food items to your list.
Enter the food name, calories, and protein content.
Record Your Food Intake:

Enter the food item you've eaten and the serving size.
The app will calculate and display the calories and protein consumed.
Edit or Delete Entries:

Long-press on a food item in the food list or eating diary to edit or delete it.

Set Goals:
Click on the "Calorie Goal" or "Protein Goal" labels to set your daily goals.
The app will show your progress towards these goals.
Clear Diary:

Click on "Clear Diary" to remove all entries from your eating diary. This action is irreversible.

File Structure
app.py: Main application script.
database.py: File containing database-related functions.
food_items.txt: File storing the list of food items.
calorite_count.txt: File storing the calories corresponding to each food item.
protein_count.txt: File storing the protein content corresponding to each food item.
eating_diary.txt: File storing the daily food intake entries.
time_file.txt: File storing the last recorded date.

Acknowledgments
This application was created using the Kivy framework. Kivy is an open-source Python library for developing multi-touch applications. Visit Kivy for more information.
