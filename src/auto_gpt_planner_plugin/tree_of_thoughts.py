import openai
from .utils import process_response

class TreeOfThoughts:
    """This class manages the Tree of Thoughts."""

    def __init__(self, problem, model, max_tokens):
        self.problem = "Define the problem here"
        self.model = "gpt-3.5-turbo"  # or whichever model you're using
        self.max_tokens = 4096  # or your desired token limit
        self.thoughts = []

    def generate(self):
        """
        Generate a Tree of Thoughts for the given problem using the GPT-4 model.
        """
        # Call the OpenAI API for chat completion
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an assistant that generates potential solutions to problems.",
                    },
                    {
                        "role": "user",
                        "content": f"Generate potential solutions for the following problem: {self.problem}",
                    },
                ],
                max_tokens=self.max_tokens,
                n=1,
                temperature=0.5,
            )
        except Exception as e:
            print(f"Failed to generate Tree of Thoughts: {e}")
            return None

        # Process the OpenAI response
        try:
            processed_response = process_response(response)
        except Exception as e:
            print(f"Failed to process response: {e}")
            return None

        # The Tree of Thoughts is represented as a list of potential solutions
        self.thoughts = processed_response.split('\n')

        return self.thoughts

    def evaluate(self):
        """
        Evaluate a Tree of Thoughts using the GPT-4 model and select the best solution.
        """
        best_solution = None
        best_solution_score = -1

        for solution in self.thoughts:
            # Call the OpenAI API for chat completion
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an assistant that evaluates the quality of solutions.",
                        },
                        {
                            "role": "user",
                            "content": f"Evaluate the following solution: {solution}",
                        },
                    ],
                    max_tokens=self.max_tokens,
                    n=1,
                    temperature=0.5,
                )
            except Exception as e:
                print(f"Failed to evaluate solution: {e}")
                continue

            # Process the OpenAI response
            try:
                processed_response = process_response(response)
            except Exception as e:
                print(f"Failed to process response: {e}")
                continue

            # Assume the response is a score for the solution
            score = float(processed_response)

            if score > best_solution_score:
                best_solution = solution
                best_solution_score = score

        return best_solution
