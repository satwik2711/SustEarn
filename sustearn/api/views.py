# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Products
# from rest_framework import status
# import json
# import requests
# import os
# import re


# import google.generativeai as genai

# genai.configure(api_key='AIzaSyBSseEKOSkx9ndTBli4XWfgH0RiL9g2R10')

# def fetch_emission_directly(product_name):
#     model = genai.GenerativeModel("gemini-pro")
#     prompt = f"Provide a numerical value only on the emission of the product '{product_name}' as per your understanding, no text required, just integer output. The value should be in unites mtCO2e. Don't just print a random number, try to provide a value that is as close as possible to the actual emission value. REMEMBER: The value should be in unites mtCO2e. DO NOT PRINT RANDOM VALUE"
#     response = model.generate_content(prompt)
#     return response.text

# def fetch_life_cycle_stages(product_description, product_name):
#     model = genai.GenerativeModel("gemini-pro")
#     prompt = f"Given a product description '{product_description}', list the main life cycle stages of the product- '{product_name}'."
#     response = model.generate_content(prompt)
#     return response.text


# def fetch_industry_benchmark_lca(product_name):
#     model = genai.GenerativeModel("gemini-pro")
#     prompt = f"Provide a numerical value only on the industry benchmark Life-Cycle Assessment (LCA) for the product '{product_name}'."
#     response = model.generate_content(prompt)
#     match = re.search(r"\d+\.?\d*", response.text)
#     lca_data = float(match.group(0)) if match else None

#     response_data = {
#         "lca_data": lca_data
#     }

#     return response_data

# def get_x_values_from_llm(product_name, life_cycle_stages):
#     model = genai.GenerativeModel("gemini-pro")
#     x_values = {}
#     for stage in life_cycle_stages:
#         prompt = f"Provide a numerical value only on the industry segment benchmark for products similar to '{product_name}' for the life cycle stage '{stage}'."
#         response = model.generate_content(prompt)
#         match = re.search(r"\d+\.?\d*", response.text)
#         numerical_value = float(match.group(0)) if match else None
#         x_values[stage] = numerical_value
#     return x_values


# def optimize_emission(weighted_average_emission, industry_lca):
#     lower_bound = industry_lca * (-10 / 100)
#     upper_bound = industry_lca * (10/ 100)
#     if lower_bound < weighted_average_emission < upper_bound:
#         return weighted_average_emission
#     else:
#         return max(min(weighted_average_emission, upper_bound), lower_bound)
    

# def calculate_weighted_average_emission(x_values, weights):
#     weighted_sum = sum(x_values[key] * weights[key] for key in x_values)
#     total_weight = sum(weights.values())
#     return weighted_sum / total_weight if total_weight else None

# @api_view(['POST'])
# def get_emission(request):
#     product_name = request.data.get('name')
#     if not product_name:
#         return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)
    
#     emission = fetch_emission_directly(product_name)
#     return Response({'emission': emission})


# @api_view(['POST'])
# def get_life_cycle_stages(request):
#     product_name = request.data.get('name')
#     product_description = request.data.get('description')
#     if not all([product_name, product_description]):
#         return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)
    
#     life_cycle_stages = fetch_life_cycle_stages(product_description, product_name)
#     return Response({'life_cycle_stages': life_cycle_stages})



# @api_view(['POST'])
# def calculate_footprint(request):
#     try:
#         life_cycle_stages = request.data.get('life_cycle_stages')
#         product_name = request.data.get('name')
#         weights_input = request.data.get('weights', {})

#         if not product_name or not life_cycle_stages:
#             return Response({'error': 'Missing necessary data'}, status=status.HTTP_400_BAD_REQUEST)

#         weight = 1 / len(life_cycle_stages) if not weights_input else None
#         weights = {stage: weights_input.get(stage, weight) for stage in life_cycle_stages}
        
#         x_values = get_x_values_from_llm(product_name, life_cycle_stages)
#         weighted_average_emission = calculate_weighted_average_emission(x_values, weights)

#         industry_lca = fetch_industry_benchmark_lca(product_name)
#         optimized_emission = optimize_emission(weighted_average_emission, industry_lca['lca_data'])

#         product, created = Products.objects.update_or_create(
#             name=product_name,
#             defaults={
#                 'life_cycle_stages': json.dumps(life_cycle_stages),
#                 'weights': json.dumps(weights),
#                 'weighted_average_emission': weighted_average_emission,
#                 'optimized_emission': optimized_emission,
#             }
#         )

#         return Response({'weighted_average_emission': weighted_average_emission, 'optimized_emission': optimized_emission})
    
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# NEW CODE

import openai

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products
from rest_framework import status
import json
import os
import re


import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def fetch_emission_directly(product_name):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Let's think step by step to determine the emission value of the product '{product_name}'. 
    1. Consider the typical emissions associated with the production and lifecycle of such products.
    2. Use any relevant industry benchmarks or standards to guide your estimation.
    3. Provide a numerical value in units of mtCO2e, which is a commonly used measure for emissions.
    4. Ensure the value is as close as possible to the actual emission value. 
    Provide the emission value in units of mtCO2e without any additional text: 
    """
    response = model.generate_content(prompt)
    return response.text

def fetch_life_cycle_stages(product_description, product_name):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Given the product description '{product_description}', let's identify the main life cycle stages for the product '{product_name}' step by step. 
    1. Think about the different phases a product goes through from raw material extraction to disposal or recycling.
    2. Common stages include raw material extraction, manufacturing, transportation, usage, and end-of-life disposal.
    3. Ensure to list the stages in a logical order. 
    Provide the list of life cycle stages: 
    """
    response = model.generate_content(prompt)
    return response.text

def fetch_industry_benchmark_lca(product_name):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Let's determine the industry benchmark Life-Cycle Assessment (LCA) value for the product '{product_name}' step by step.
    1. Consider typical LCA values for similar products in the same industry.
    2. Use any known benchmarks or standards to guide the estimation.
    3. Provide a numerical value representing the LCA in units of mtCO2e.
    4. Ensure the value is as close as possible to an accurate benchmark.
    Provide the LCA value in units of mtCO2e without any additional text:
    """
    response = model.generate_content(prompt)
    match = re.search(r"\d+\.?\d*", response.text)
    lca_data = float(match.group(0)) if match else None

    response_data = {
        "lca_data": lca_data
    }

    return response_data

def get_x_values_from_llm(product_name, life_cycle_stages):
    model = genai.GenerativeModel("gemini-pro")
    x_values = {}
    for stage in life_cycle_stages:
        prompt = f"""
        Let's determine the numerical value for the industry segment benchmark for products similar to '{product_name}' during the life cycle stage '{stage}' step by step.
        1. Think about the typical emissions or environmental impacts associated with this stage for similar products.
        2. Use any known industry benchmarks or standards for guidance.
        3. Provide a numerical value representing the impact for this stage in units of mtCO2e.
        4. Ensure the value is as close as possible to an accurate benchmark.
        Provide the value in units of mtCO2e without any additional text:
        """
        response = model.generate_content(prompt)
        match = re.search(r"\d+\.?\d*", response.text)
        numerical_value = float(match.group(0)) if match else None
        x_values[stage] = numerical_value
    return x_values

def optimize_emission(weighted_average_emission, industry_lca):
    lower_bound = industry_lca * (-10 / 100)
    upper_bound = industry_lca * (10 / 100)
    if lower_bound < weighted_average_emission < upper_bound:
        return weighted_average_emission
    else:
        return max(min(weighted_average_emission, upper_bound), lower_bound)
    

def calculate_weighted_average_emission(x_values, weights):
    weighted_sum = sum(x_values[key] * weights[key] for key in x_values)
    total_weight = sum(weights.values())
    return weighted_sum / total_weight if total_weight else None

@api_view(['POST'])
def get_emission(request):
    product_name = request.data.get('name')
    if not product_name:
        return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)
    
    emission = fetch_emission_directly(product_name)
    return Response({'emission': emission})


@api_view(['POST'])
def get_life_cycle_stages(request):
    product_name = request.data.get('name')
    product_description = request.data.get('description')
    if not all([product_name, product_description]):
        return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)
    
    life_cycle_stages = fetch_life_cycle_stages(product_description, product_name)
    return Response({'life_cycle_stages': life_cycle_stages})


@api_view(['POST'])
def calculate_footprint(request):
    try:
        life_cycle_stages = request.data.get('life_cycle_stages')
        product_name = request.data.get('name')
        weights_input = request.data.get('weights', {})

        if not product_name or not life_cycle_stages:
            return Response({'error': 'Missing necessary data'}, status=status.HTTP_400_BAD_REQUEST)

        weight = 1 / len(life_cycle_stages) if not weights_input else None
        weights = {stage: weights_input.get(stage, weight) for stage in life_cycle_stages}
        
        x_values = get_x_values_from_llm(product_name, life_cycle_stages)
        weighted_average_emission = calculate_weighted_average_emission(x_values, weights)

        industry_lca = fetch_industry_benchmark_lca(product_name)
        optimized_emission = optimize_emission(weighted_average_emission, industry_lca['lca_data'])

        product, created = Products.objects.update_or_create(
            name=product_name,
            defaults={
                'life_cycle_stages': json.dumps(life_cycle_stages),
                'weights': json.dumps(weights),
                'weighted_average_emission': weighted_average_emission,
                'optimized_emission': optimized_emission,
            }
        )

        return Response({'weighted_average_emission': weighted_average_emission, 'optimized_emission': optimized_emission})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
