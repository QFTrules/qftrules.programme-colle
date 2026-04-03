def classes_fruits(fruits):
  """
  Entrée : fruits (list) : liste de chaînes de caractères
  Sortie : classes (list) : liste de chaînes de caractères
  """
  classes = []
  for fruit in fruits:
      if fruit not in classes:
          classes.append(fruit)
  return classes