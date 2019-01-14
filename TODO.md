# All Tasks
- SQL backing database:
    - structure: 
        - *Question*: Index (INT NOT NULL PK), Leetcode (VARCHAR(2083)), Text Block (TEXT NOT NULL), Company (TEXT NOT NULL), Data Structure (TEXT), Last Date Asked (DATE)
        - *Admin*: Index (INT NOT NULL PK), User ID (VARCHAR(19))

- Commands:
    - [x] *Add Question*: Add question to database
    - [x] *Remove Question*: Remove from database
    - [x] *Force Question*: force bot to push question to channel
    - [ ] *Add Admin*: add admin
    - [ ] *Remove Adming*: removes admin
    - [x] *List Questions*: list questions by index and date
    - [ ] *Re-open Connection*: Re open connection to database server if closes

- Other:
    - [x] Timer to know when to run question
    - [ ] Bot backend
        - [x] Target channel
        - [ ] Communication with right people only
    - [x] General SQL integration
    - [ ] Add SQL cache
    - [x] Alter Dockerfile
        - [x] include vim in base package (TODO: switch this to the psql base)
        - [x] start psql automatically
        - [x] add psql defaults in base package
        - [x] go straight to `vim .env`
    - [ ] Change SQL
        - [x] New Question model
        - [x] Alter tests
        - [x] Alter commands
        - [ ] Add leetcode link command
    - [ ] Un-screw the saving (the array in on_message is all kinds of messy inside)
    
# Potential Order
1. Database Communication
2. Adding + Outputting Questions
3. Timer on Questions
4. Removing Questions from db
5. Caching 
7. Improve SQL querying
8. **[Really this is just running parallel]** Security checks for users only adding valid inputs per role level.
    