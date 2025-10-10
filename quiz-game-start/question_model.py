class Question:
    """A quiz question with text and correct answer."""
    
    def __init__(self, q_text, q_answer):
        """Initialize a question with text and answer.
        
        Args:
            q_text (str): The question text
            q_answer (str): The correct answer
        """
        self.text = q_text
        self.answer = q_answer

