from src.workflow import run_qa

persian_question = "کتاب راجع به چی چیزها میباشد"
answer = run_qa(persian_question)
print(answer)