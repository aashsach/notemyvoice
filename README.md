# NoteMyVoice

NoteMyVoice is an app to create notes and memos.
You can either create notes by
- Voice: We use assemblyAI api to transcribe what you speak and then store it to database.
- Text: You can also type your note or thought, which is then stored in the database.

Each  note is automatically augmented with a heading and an thumbnail image.

Every note stored in the database can be searched using a simple interface.
For searching, you just need to either type/speak your query, and we will do the rest usiing vector matching.

In addition, we provide a simple chat interface, where in you can not only search but brainstorm over your ideas.

# Please find all the interfaces at :
-  [List and search all stored notes](/list_note)
-  [Create a new note](/create_note)
-  [Chat with stored notes](/chat_notes)