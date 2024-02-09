def movie_stars(movie_dict):
  for movie in movie_dict:
      movie['stars'] = add_stars(movie['Rating'])
  return movie_dict

def add_stars(rating):
  my_return = ""
  for x in range(1, 6):
      if rating >= x:
          checked = "checked"
      elif rating > x - 1 and rating < x: 
          checked = "half-checked"
      else:
          checked = ""
      my_return += f"<span class=\"fa fa-star {checked}\"></span>"
  return my_return

def title_case_fields(data):
  for key in data:
      match key:
          case 'First_Name' | 'Last_Name' | 'Address_Line1' | 'Address_Line2' | 'City':
              data[key] = data[key].title()
          case _:
              continue

def category_to_icon(category_name):
  icon_map = {
      'Breakfast': 'fas fa-egg',
      'Lunch': 'fas fa-hamburger',
      'Dinner': 'fas fa-utensils',
      'Dessert': 'fas fa-ice-cream',
      'Salad': 'fas fa-leaf',
      'Side Dish': 'fas fa-pepper-hot',
  }
  return icon_map.get(category_name, 'fas fa-question')  # Default icon
