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
