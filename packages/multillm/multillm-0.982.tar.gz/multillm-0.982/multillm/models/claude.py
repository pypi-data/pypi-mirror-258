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
        """
        Anthropic response: {
    "id": "msg_0187fAnrkoF8HbKm1Pi6jthf",
    "content": [
        {
        "text": "Here is a sample C function to test TCP sockets:\n\n```c\n#include <stdio.h> \n#include <stdlib.h>\n#include <string.h>\n#include <sys/types.h>\n#include <sys/socket.h>\n#include <netinet/in.h>\n#include <arpa/inet.h>\n\nvoid test_tcp_socket()\n{\n  int socket_fd;\n  struct sockaddr_in server_address;\n\n  // Create socket file descriptor\n  socket_fd = socket(AF_INET, SOCK_STREAM, 0);\n  if(socket_fd < 0) {\n    perror(\"Error opening socket\");\n    exit(1);\n  }\n\n  // Initialize server address \n  memset(&server_address, 0, sizeof(server_address));  \n  server_address.sin_family = AF_INET;\n  server_address.sin_addr.s_addr = inet_addr(\"127.0.0.1\"); // Server IP address \n  server_address.sin_port = htons(5000); // Server port\n\n  // Connect to server\n  if(connect(socket_fd, (struct sockaddr*) &server_address, sizeof(server_address)) < 0){\n    perror(\"Connection failed\");\n    exit(1);\n  }\n\n  printf(\"Connected to the server!\\n\");\n\n  close(socket_fd);\n}\n```\n\nThis function creates a TCP client socket, connects to a server listening on localhost port 5000, and prints a success message if connection is successful. It closes the socket afterwards.",
        "type": "text"
        }
    ],
    "model": "claude-instant-1.2",
    """
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
            print("({0}) error:  credential file doesn't exist" .format(self.__class__.__name__))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials




        client = Anthropic(
        # This is the default and can be omitted
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

        response = client.messages.create(
        max_tokens=10000,
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

