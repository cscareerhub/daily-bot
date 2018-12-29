# All Tasks
- SQL backing database:
    - structure: 
        - *Question*: Index (INT NOT NULL PK), Text Block (TEXT NOT NULL), Last Date Asked (DATE)
        - *Answers*: Index (INT NOT NULL PK), User ID (???), URL to solution (VARCHAR(2083) NOT NULL), Question Index (INT NOT NULL FK to Question)

- Commands:
    - [x] *Add Question*: Add question to database
    - [ ] *Remove Question*: Remove from database
    - [x] *Force Question*: force bot to push question to channel
    - [ ] *Add Solution*: add or change solution for user
    - [ ] *List Solutions*: list solutions for users given a question index
    - [ ] *List Questions*: list questions by index and date
    - [ ] *Re-open Connection*: Re open connection to server if closes
    - [ ] *Alter Users*: add users that can communicate with bot

- Other:
    - [x] Timer to know when to run question
    - [ ] Bot backend
        - [x] Target channel
        - [ ] Communication with right people only
    - [ ] General SQL integration
    - [ ] Add SQL cache
    - [ ] Alter Dockerfile
        - [ ] include vim in base package
        - [ ] start psql automatically
        - [ ] add psql defaults in base package
        - [ ] go straight to `vim .env`
    
# Potential Order
1. Database Communication
2. Adding + Outputting Questions
3. Timer on Questions
4. Removing Questions from db
5. Caching 
6. Save answers in database
7. Improve SQL querying
8. **[Really this is just running parallel]** Security checks for users only adding valid inputs per role level.
    