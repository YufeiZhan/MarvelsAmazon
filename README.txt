MEMBERS and ROLES:
Honggang Min (hm246): Users
Ryan Wu (yw609): Products
Yufei Zhan (yz858): Carts
Longtian Ye (ly086): Sellers
Qianyu Yang (qy46): Social

TASKS DONE:
----------- Milestone 2 ----------- 
Yufei Zhan (yz858): 
 1. set up project repo and created branches for each role
 2. designed frontend using Honggang Min's draft design using Figma
 3. implemented content descriptions and logical flow/connections for the login/register view and the buyer view in Figma

Honggang Min (hm246):
 1. Translated the five parts' text requirements into preliminary design components.
 2. Created the intermediate components needed for the buyer, seller, and login views in Figma under 'Draft'.

Longtian Ye (ly186):
1. Drafted a diagram for our database design and Identified constraints included for each table 
2. Implemented logic flow/connections for seller view using Figma

Ryan Wu (yw609):
1. Drew the UML diagram with Longtian’s draft and identified the unique keys
2. Wrote down the tables in the report and drafted the constraints in the report

Ethan Yang (qy46):
1. Modified the UML diagram to fix some relationship between tables and identified all the foreign keys
2. Wrote the assumptions and completed the constraints in the report 

----------- Milestone 3 ----------- 
Yufei Zhan (yz858):
1. Revised the database schema and updated the schema design
2. Implemented frontend of the navigation bar 
3. Implemented the Cart flow including the endpoint and data model to fetch all cart items for the user 
4. Integrated several other flows into the navigation bar
Code implemented: /app/carts.py, models/cart.py, templates/cart.html, templates/base.html

Honggang Min (hm246):
1. Implemented the public view for buyers's accounts
2. Implemented the feature where 'users can update all information except the id' while ensuring email uniqueness. Also setup the associated flows and endpoints.
Code implemented: /app/users.py, models/user.py, templates/update.html, templates/account.html

Ethan Yang (qy46):
1. Created the schema of the database in `create.sql`, debuged the database setup process
2. Generated fake data and the `dummy user` for demo purposes
3. Added the model, controller and view components for Social guru
4. Modified the backend api and frontend template for Index to connect the homepage with the database
5. Helped debuged the backend and frontend for Product and Seller
Code implemented: /app/reviews.py, models/reviews.py, templates/review.html

Longtian Ye (ly186):
1. Completed the Seller counterpart including backend API endpoints, model and frontend elements 
2. Created fake data according to our database design schema
3. Modified the backend User model to fix the login page issues and adapt to our database design.
Code implemented: /models/seller.py, app/seller.py, templates/seller.html

Yanzheng Wu (yw609):
1. Implemented the model, controller and view components for Product guru
2. Implemented the feature that users can find top expensive products to display
3. Generated fake data of products and users, and helped debuged model components adapting to our database
Code implemented: /models/product.py, app/products.py, templates/product.html




LINK to GITLAB REPO: https://gitlab.oit.duke.edu/youngnbroke/mini-amazon
LINK to Milestone 3 Video: https://duke.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=b16ddf97-2995-494e-9919-b140003e7ef2