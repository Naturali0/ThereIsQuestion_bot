from dataclasses import dataclass



@dataclass
class Question:
    q_type:str
    question:str


@dataclass
class PollQuestion(Question):
    answers:list[str]
    correct: list[int]


@dataclass
class InineKeyboardQuestion(Question):
    answers:list[str]
    correct: int
    

@dataclass
class OpenQuestion(Question):
    correct:str
