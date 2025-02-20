from src.database.models import Answer


def create_answers_detail_text(answer: Answer) -> str:
    return f"User: {answer.user.name}\nText answer: {answer.text_answer}\n"
