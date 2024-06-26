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
Code implemented: /app/carts.py, models/cart.py, templates/cart.html, templates/base.html, /app/index.py, /templates/index.html

Honggang Min (hm246):
1. Implemented the public view for buyers's accounts
2. Implemented the feature where 'users can update all information except the id' while ensuring email uniqueness. Also setup the associated flows and endpoints.
Code implemented: /app/users.py, models/user.py, templates/update.html, templates/account.html, /app/index.py

Ethan Yang (qy46):
1. Created the schema of the database in `create.sql`, debuged the database setup process
2. Generated fake data and the `dummy user` for demo purposes
3. Added the model, controller and view components for Social guru
4. Modified the backend api and frontend template for Index to connect the homepage with the database
5. Helped debuged the backend and frontend for Product and Seller
Code implemented: /app/reviews.py, models/reviews.py, templates/review.html, /app/index.py, /templates/index.html, /app/user.py

Longtian Ye (ly186):
1. Completed the Seller counterpart including backend API endpoints, model and frontend elements 
2. Created fake data according to our database design schema
3. Modified the backend User model to fix the login page issues and adapt to our database design.
Code implemented: /models/seller.py, /app/seller.py, templates/seller.html, /app/user.py

Yanzheng Wu (yw609):
1. Implemented the model, controller and view components for Product guru
2. Implemented the feature that users can find top expensive products to display
3. Generated fake data of products and users, and helped debuged model components adapting to our database
Code implemented: /models/product.py, /app/products.py, /templates/product.html, /app/index.py, /templates/index.html

LINK to GITLAB REPO: https://gitlab.oit.duke.edu/youngnbroke/mini-amazon
LINK to Milestone 3 Video: https://duke.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=b16ddf97-2995-494e-9919-b140003e7ef2
----------- Milestone 4 ----------- 
Ethan Yang (qy46):
1. Modified gen.py to generate large scale data that satisfied the relationship constraints; manually generated interesting demo data on top of the randomly generated large scale data for demo purposes
2. Modified the template and API endpoint for social guru to adapt the pagination; Modified the template for social guru to match the web design
3. Fixed base template to make toggle button real-time interactive
4. Updated the database design and Figma for report

Longtian Ye (ly186):
1. Drafted gen.py to generate large scale data according to our database table design schema and debugged to pass our constraints.
2. Implemented pagination for seller inventory page.
3. Added a functionality for seller to add new product to its inventory.

Yanzheng Wu (yw609):
1. Implemented search functionality enabling users to quickly find products by name
2. Added feature whereby a buyer can view all the sellers' information associated with each product listed on the main page
3. Implemented functionality for buyers to add product to cart

Honggang Min (hm246):
1. Tested and finalized requirement no.3 of user balance topup and withdraw.
2. Aligned the buttons with the designs from Figma.

Yufei Zhan (yz858):
1. Implemented buyer/seller toggle to switch role and view and update with database
2. Implemented pagination functionality on products to be used in different parts of the app
3. Modified the template and API endpoint for cart guru to adapt the pagination and match Figma's design as well as functionalities

LINK to GITLAB REPO: https://gitlab.oit.duke.edu/youngnbroke/mini-amazon
LINK to Milestone 4 Video: https://duke.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=5c07378e-cd40-4da1-bb05-b15500413b7b

----------- Milestone Last ----------- 
Ethan Yang (qy46):
1. Perform data preprocessing to clean the demo data
2. Implemented all social guru features (full-stack)
3. Fixed bugs in product, user, order pages
4. Updated the database design for report

Yufei Zhan (yz858):
1. Order submission
2. Order details

Longtian Ye (ly186):
1. Seller inventory page
2. Sale history
3. Modified background

Yanzheng Wu (yw609):
1. Product page
2. Main Page

Honggang Min (hm246):
1. User login page
2. User detail page
3. Public view pages


LINK to GITLAB REPO: https://gitlab.oit.duke.edu/youngnbroke/mini-amazon
LINK to demo: Please find the demo link in our Gitlab README.md