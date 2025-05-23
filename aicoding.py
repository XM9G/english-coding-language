import os
import dotenv

from openai import OpenAI
import sys


def run(filepath, debug=False):
    '''
    This will run the english code in the file given in the filepath.
    '''
    dotenv.load_dotenv()
    if not filepath.endswith('.ss'):
        raise ValueError("File must be a .ss file")

    with open(filepath, "r") as f:
        data = f.read()
        XAI_API_KEY = os.environ.get("XAI_API_KEY")
        
        if not XAI_API_KEY:
            raise ValueError("XAI_API_KEY environment variable is not set")
        
        client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",
        )

        completion = client.chat.completions.create(
            model="grok-3-mini",
            messages=[
                {"role": "system", "content": "You must only give python code which will do the instructions given by the user. No other words just python code. No explanation. No markdown. No ```backticks```, No comments."},
                {"role": "user", "content": data}
            ]
        )

        response = completion.choices[0].message.content
        if debug:
            print(f'{response}')
        exec(response)
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        debug = sys.argv[2] if len(sys.argv) > 2 else False
        run(filepath, debug)
    else:
        print("Please provide a filepath as a command line argument.")