
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

