from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from rest_framework import status
import json

@api_view(['POST'])
def calculate_footprint(request):
    try:
        product_name = request.data.get('name')
        life_cycle_stages = request.data.get('life_cycle_stages')
        weights = request.data.get('weights')

        if not all([product_name, life_cycle_stages, weights]):
            return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(life_cycle_stages, str):
            life_cycle_stages = json.loads(life_cycle_stages)
        if isinstance(weights, str):
            weights = json.loads(weights)


        x_values = get_x_values_from_llm(product_name, life_cycle_stages)
        weighted_average_emission = calculate_weighted_average_emission(x_values, weights)

        product, created = Product.objects.update_or_create(
            name=product_name,
            defaults={
                'life_cycle_stages': life_cycle_stages,
                'weights': weights,
                'weighted_average_emission': weighted_average_emission,
                'optimized_emission': 0,
            }
        )
        
        return Response({'weighted_average_emission': weighted_average_emission})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_x_values_from_llm(product_name, life_cycle_stages):

    return {'x1': 10, 'x2': 20, 'x3': 30}

def calculate_weighted_average_emission(x_values, weights):
    x1, x2, x3 = x_values['x1'], x_values['x2'], x_values['x3']
    w1, w2, w3 = weights['manufacturing'], weights['use_cycle_phase'], weights['transportation']
    weighted_sum = w1 * x1 + w2 * x2 + w3 * x3
    total_weight = w1 + w2 + w3
    weighted_average = weighted_sum / total_weight
    return weighted_average


# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_x_values_from_llm(product_name, life_cycle_stages):
#     # Initialize the LLM (e.g., OpenAI's GPT model through Langchain)
#     llm = load_qa_chain(ChatGoogleGenerativeAI)
    

#     # Construct the prompt for the LLM
#     prompt = construct_prompt(product_name, life_cycle_stages)

#     # Send the prompt to the LLM and get a response
#     response = llm(prompt)

#     # Process the response to extract x1, x2, and x3 values
#     x_values = extract_x_values(response)

#     return x_values

# def construct_prompt(product_name, life_cycle_stages):
#     # Construct a detailed prompt that asks for the CO2 emissions for each lifecycle stage
#     prompt = f"Please provide the industry segment benchmark CO2 emissions of '{product_name}' for the following life cycle stages: {', '.join(life_cycle_stages)}."
#     return prompt

# def extract_x_values(response):
#     # Parse the response from the LLM to extract the x1, x2, and x3 values
#     # This will be specific to how the LLM structures its response
#     # You might need to apply some string manipulation or even further LLM queries to get clean data
#     # This is a placeholder for the logic you would use to parse the response
#     x_values = {
#         'x1': parse_value_from_response(response, 'manufacturing'),
#         'x2': parse_value_from_response(response, 'use_cycle_phase'),
#         'x3': parse_value_from_response(response, 'transportation')
#     }
#     return x_values

# def parse_value_from_response(response, stage_name):
#     # Implement a method to parse the LLM response and extract the numeric value for the given stage_name
#     # Placeholder for parsing logic
#     return 0  # Replace this with actual parsed value

