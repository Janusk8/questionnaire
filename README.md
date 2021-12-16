L'API produit des QCMs de 5, 10 ou 20 questions. L'utilisateur choisit un type de test (use) ainsi qu'une ou plusieurs catégories (subject). Les questions sont retournées dans un ordre aléatoire: ainsi, une requête avec les mêmes paramètres pourra retourner des questions différentes.

Endpoints:

GET /status
Cette fonction renvoie 1 si l'API fonctionne.

POST /post_questions
Cette fonction renvoie une série de questions
       
POST /post_question
Cette fonction permet a un utilisateur admin de créer une nouvelle question
