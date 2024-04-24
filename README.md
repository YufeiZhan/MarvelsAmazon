# Mini-Amazon
Based on  [Rickard Stureborg](http://www.rickard.stureborg.com) and [Yihao Hu](https://www.linkedin.com/in/yihaoh/)'s code, we implemented a mini-amazon website where people can buy things from us.

## Dummy User
For development purpose, we have a dummy user that can be used to test newly-implemented functionalities.

**Username**: dummy@duke.edu <br>
**Password**: 123
<br>
**Username2**: woodtina@gmail.com <br>
**Password2**: pass1
<br>
**DemoUsername**: tony.stark@mcu.com <br>
**DemoPassword**: 123


## Development Notes
### To run website locally:
1. Enter container environment: to to your 516-container folder and run **‘docker compose start’** and **‘docker compose exec -it ubuntu bash --login’**
2. Enter Python virtual environment: cd into your mini-amazon folder and enter virtual env by **‘poetry shell’**
3. Init the database with **`db/setup.sh`**: cd into **`/db`** directory and run **`./setup.sh`** or **`./setup.sh generated`**
4. Run the flask server using **'flask run'** and enter **'localhost:8080'** in your browser 

### To interact with database:
To change schema, modify 	‘db/create.sql’ and ‘db/load.sql’ and run ‘db/setup.sh’ to recreate the database from scratch. <br><br>
Use **'psql amazon'** to enter the database. <br><br>
Some useful commands:
- List all tables in database: \dt
- List info of one table: \d [TABLE_NAME]
- Check table with SQL query: SELECT * FROM [TABLE_NAME]

### Links
- **Milestone 2&4 Report**: https://docs.google.com/document/d/1sPQoiLw9mXILVjCTQzOSzXuBwGrz5qWqYeKRn_aJMYQ/edit?usp=sharing
- **Database design**: https://lucid.app/lucidchart/b888d686-46d6-44e5-a180-3501dc886c98/edit?invitationId=inv_de774230-9b13-42ec-8b57-4c7cc1f3fb67&page=0_0#
- **Website Figma**: https://www.figma.com/file/yUVon71jBbMF8h5J8P4IyM/Mini-Amazon?type=design&node-id=0%3A1&mode=design&t=4pAnItnrbubzwm4u-1
- **Tutorial**: https://gitlab.oit.duke.edu/compsci316/mini-amazon-skeleton/-/blob/main/TUTORIAL.md

### Milestones
**Milestone 3 (03/26)**: at least 1 backend API endpoint + frontend for each Guru; demo video (<3 min)

**Milestone 4 (04/16)**: functionalities almost complete and integrated; test on large database; demo video (< 5min)

**Final Milestone (05/03)**: full functionalities; final report + demo video

### Roles
**Users Guru**: Peter <br>

**Products Guru**: Ryan <br>

**Carts Guru**: Selina <br>

**Seller Guru**: Ye Long-tian <br>

**Social Guru**: Ethan <br>

### Todo:
- [] Some database schemas creation in create.sql didn't enforce primary key constraint
- [] Fix Cartitems status field (should only has 2 status)
- [] Filter the reviews (most recent # reviews)
- [x] For buyer and seller, provide different page views
- [x] Fix Balance value
- [] Order History and Sale History integrate to a same page
- [] Add image to product field
- [] Change users's updateRole to PUT request
- [] Deal with the case where page is out of range
- [] Cartitems add a time field to sort it in cart
- [] Cart: refine quantity condition + implement coupon, remove all, and submit

## Note on Hiding Credentials

Use the file `.flaskenv` for passwords/secret keys --- we are talking
about passwords used to access your database server, for example (not
user passwords for your website in CSV files for loading sample
database).  This file is NOT tracked by `git` and it was automatically
generated when you first ran `./install.sh`.  Don't check it into
`git` because your credentials would be exposed to everybody on GitLab
if you are not careful.
