import torch
import transformers


class Llama3:
    def __init__(self, model_path: str):
        self.prompt = ""
        self.model_id = model_path
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_id,
            device_map='auto',
            torch_dtype=torch.bfloat16,
            model_kwargs={
                "quantization_config": {"load_in_4bit": True},
                "low_cpu_mem_usage": True
            }
        )

    def get_response(self, query: str,
                     prompt: str = "You are an AI assistant that provides concise and accurate answers.Make proper use of markdown in your answer.The user will prompt you with something and you must add your answer after `-AI:`.\n",
                     user_role: str = "User", ai_role="AI", post_process: bool = True,
                     max_tokens: int = 256, temperature: float = 0.7, top_p: float = 0.9,
                     top_k: int = 50, repetition_penalty: float = 1.2, stop_words: list = None) -> \
            (tuple[str, str]):

        # Prompt Engineering for the model
        self.prompt = (
                prompt +
                "|||\n"
                f"- {user_role}: {query}\n"
                f"- {ai_role}:"
        )
        # Generate output with the current pipeline
        outputs = self.pipeline(
            self.prompt,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            eos_token_id=self.pipeline.tokenizer.eos_token_id,
        )

        # Extract response text, isolating the text generated after the prompt part
        raw_response = outputs[0]["generated_text"]
        response = self.__extract_relevant_response(raw_response)

        # Optional: Post-process the response to fix incomplete sentences
        if post_process:
            response = self._post_process_response(response, stop_words=stop_words)

        return response, raw_response

    def __extract_relevant_response(self, generated_text: str) -> str:
        """
        Extracts the relevant portion of the model's response by removing the start prompt
        and returning everything that follows it.
        """
        return generated_text[len(self.prompt):].strip()

    @staticmethod
    def _post_process_response(response: str, stop_words: list = None) -> str:
        """
        Post-processes the response to ensure sentences are complete and optionally truncate after stop words.
        If the response does not end with a valid punctuation mark (., !, ?, ;), it trims everything after
        the last valid punctuation mark.

        :param response: The generated response to clean up.
        :param stop_words: List of stop words to detect where the response should stop (optional).
        :return: The cleaned response.
        """
        # List of valid punctuation marks
        valid_punctuations = ('.', '!', '?', ';', ')', '}', ']', "'", '"')

        # Find the last valid punctuation
        last_punctuation_index = max(response.rfind(punc) for punc in valid_punctuations)

        # If no valid punctuation is found, return the response as-is
        if last_punctuation_index == -1:
            last_punctuation_index = len(response)

        # Truncate everything after the last valid punctuation
        response = response[:last_punctuation_index + 1]  # Include the punctuation itself

        # Optionally truncate based on stop words
        if stop_words:
            for word in stop_words:
                if word in response:
                    response = response.split(word)[0] + word

        return response
