import os,sys
import json
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt
import requests
from anthropic import Anthropic

""" Google vertexai imports """
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from anthropic import AnthropicVertex


# Google ANTHROPIC interface
"""
The CLAUDE class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
"""
class CLAUDE(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "CLAUDE",
            "model" : "chat-bison@001",
            "credentials" : "key.json"
        }
        #if kwargs:
        # super().__init__(kwargs)
        #else:
        #    super().__init__(defaults)

        
    
    # Get Text
    def get_content(self, response):
        resp = response
        #sys.stdout = sys.__stdout__
    
        """ Get the text from the response of an LLM """
        try:
            if self.is_code(str(resp)):
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), True
            else:
                #print('CLAUDE is not code')
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), False
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('CLAUDE response failed {}'.format(e))


    

    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"

        """ Get credentials file set in the config, and set appropriate variables for your model """
        if not os.path.exists(self.credentials):
            try:
                api_key = os.environ["ANTHROPIC_API_KEY"]
            except Exception as e:
                print('the env variable ANTHROPIC_API_KEY is not set')

        else:
            f = open(self.credentials, "r")
            api_key = f.readline()

        
        client = Anthropic(
        # This is the default and can be omitted
        #api_key=os.environ.get("ANTHROPIC_API_KEY"),
        api_key=api_key
        )

        response = client.messages.create(
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": prompt.get_string(),
            }
            ],
            model="claude-2.1",
        )


        print('claude reponse: {0}' .format(response))
        resp = response.model_dump_json()
    

        response = self.get_content(resp)


        if not response:
            return None, None
        else: 
            content, is_code = self.get_content(response)
        if content and taskid:
            self.publish_to_redis(content, taskid)
        
        return(content), is_code

