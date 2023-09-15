from pathlib import Path
from langchain import PromptTemplate

ROOT_PATH = Path(__file__).absolute().parent

AUDIO_FILE_PATH = ROOT_PATH / "audio_files"
CONFIG_PATH = ROOT_PATH


TITLE_OF_NOTE_PROMPT = PromptTemplate.from_template(
    template="Given a note enclosed in triple backticks, give small heading for it."
             "Heading should not more more than 4 words and should describe main theme of the note."
             "Output should only contain heading and nothing else."
             "```"
             "{note}"
             "```",
)
print(TITLE_OF_NOTE_PROMPT)

KEYWORD_OF_NOTE_PROMPT = PromptTemplate.from_template(
    template="Given a note enclosed in triple backticks, I want to find best image describing it."
             "For finding images i need keyword that i can search on google."
             "Give me just one keyword that describes the note using which i can search for images."
             "Output should only contain keyword and nothing else."
             "```"
             "{note}"
             "```",
    # input_variables=["note"]
)

print(AUDIO_FILE_PATH)
