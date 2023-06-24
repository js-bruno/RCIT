import json
from difflib import get_close_matches

def chat_base(knowledge_path: str):
    knowledge_base: dict = load_knowledge_base(knowledge_path)
    while True:
        user_input: str = input("YOU: ")
        if user_input.lower() == "quit":
            break
            
        questions: list = [q.get("question") for q in knowledge_base["questions"]]
        best_match: str | None = find_best_match(user_input, questions)

        if best_match:
            awnser: str = get_answer_for_question(user_input, knowledge_base)
            print(f"BOT: {awnser}")
        else:
            print('BOT: I dont\'t know the answer. Can yo teach me ?')
            new_answer: str = input("Type: the answer of 'skip' to SKIP:")
            
            if new_answer.lower() != "skip":
                knowledge_base["questions"].append(
                    {"question": user_input, "answer": new_answer},
                )
                save_knowledge_base(knowledge_path, knowledge_base)
                print("BOT: Thank you! I learn a new response!")

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data
        
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, question: list[str]) -> str | None :
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: str) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


if __name__ == "__main__":
    chat_base(knowledge_path="knowledge_base.json")