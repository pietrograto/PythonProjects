class QuizBrain:
    """Manages quiz flow, scoring, and question progression."""

    def __init__(self, q_list):
        """Initialize quiz with question list.
        
        Args:
            q_list (list): List of Question objects
        """
        self.question_number = 0
        self.score = 0
        self.question_list = q_list

    def still_has_questions(self):
        """Check if there are more questions to ask.
        
        Returns:
            bool: True if more questions remain
        """
        return self.question_number < len(self.question_list)

    def next_question(self):
        """Present the next question to the user."""
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ")
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        """Check user's answer and update score.
        
        Args:
            user_answer (str): User's input answer
            correct_answer (str): The correct answer
        """
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong.")
        print(f"The correct answer was: {correct_answer}.")
        print(f"Your current score is: {self.score}/{self.question_number}")
        print("\n")


