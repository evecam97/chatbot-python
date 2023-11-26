import json 
from difflib import get_close_matches

# We load the JSON file
def load_knowledgeBase(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
        return data

#We modify the JSON file with a new question with its answer
def save_knowledgeBase(file_path:str,data:dict):
    with open(file_path,"w") as file:
        json.dump(data,file,indent=2)

#Find the best answer to the user's question
def find_bestMatch(user_question:str,questions:list[str]) -> str | None:
    matches: list = get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

#Get the answer of the JSON file
def get_answer4question(question:str,knowledge_base:dict) -> str | None:
    for q in knowledge_base["questions"]:
        quser = q["question"]
        if quser == question:
            return q["answer"]
        
#Main function
def chat_bot():
    knowledge_base: dict = load_knowledgeBase('knowledgeBase.json')

    while True:
        user_input: str = input('You: ')

        if(user_input.lower() == 'quit'):
            break

        best_match: str | None = find_bestMatch(user_input,[q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer4question(best_match,knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t the answer. Can u teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input,"answer": new_answer})
                save_knowledgeBase('knowledgeBase.json',knowledge_base)
                print("Thanks! I learned a new response :D")

        
    
    
    

if __name__ == '__main__':
    chat_bot()
