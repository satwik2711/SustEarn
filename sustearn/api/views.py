# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Products
# from rest_framework import status
# import json
# import requests
# import os
# import re


# import google.generativeai as genai

# genai.configure(api_key='AIzaSyCr3BXiE3eqOSGGZe6UK0GUkgKaeHlOEBQ')

# def fetch_life_cycle_stages(product_description, product_name):
#     model = genai.GenerativeModel("gemini-pro")
#     prompt = f"Given a product description '{product_description}', list the main life cycle stages of the product- '{product_name}'."
#     response = model.generate_content(prompt)

#     life_cycle_stages = []
#     for line in response.text.split("\n"):
#         if line.startswith("The main life cycle stages"):
#             continue  # Skip the introductory line
#         if line.strip().isdigit():
#             continue  # Skip empty or number-only lines
#         if '.' in line:
#             # Extract part after the number and period
#             stage = line.split('.', 1)[1].strip()
#             if stage:  # Ensure it's not empty
#                 life_cycle_stages.append(stage)

#     response_data = {
#         "life_cycle_stages": life_cycle_stages
#     }

#     return response_data


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
    
#     # Extracting the list of life cycle stages from the dictionary if necessary
#     if isinstance(life_cycle_stages, dict) and 'life_cycle_stages' in life_cycle_stages:
#         life_cycle_stages = life_cycle_stages['life_cycle_stages']

#     x_values = {}
    
#     for stage in life_cycle_stages:
#         # Ensure stage is a string and not empty
#         if isinstance(stage, str) and stage.strip():
#             prompt = f"Provide a numerical value only on the industry segment benchmark for products similar to '{product_name}' for the life cycle stage '{stage}'."
#             response = model.generate_content(prompt)

#             match = re.search(r"\d+\.?\d*", response.text)
#             numerical_value = float(match.group(0)) if match else None
       
#             x_values[f'x[{stage}]'] = numerical_value

#     return x_values



# def optimize_emission(weighted_average_emission, industry_lca):
#     lower_bound = industry_lca * (-20 / 100)
#     upper_bound = industry_lca * (20 / 100)
#     if lower_bound < weighted_average_emission < upper_bound:
#         return weighted_average_emission
#     else:
#         return max(min(weighted_average_emission, upper_bound), lower_bound)

# @api_view(['POST'])
# def calculate_footprint(request):
#     try:
#         product_name = request.data.get('name')
#         product_description = request.data.get('description')

#         life_cycle_stages = fetch_life_cycle_stages(product_description)
#         weight = 1 / len(life_cycle_stages)
#         weights = {stage: weight for stage in life_cycle_stages}

#         if not all([product_name, product_description]):
#             return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

#         x_values = get_x_values_from_llm(product_name, life_cycle_stages)
#         weighted_average_emission = calculate_weighted_average_emission(x_values, weights)

#         #OPTIMISER FUNCTION
#         industry_lca = fetch_industry_benchmark_lca(product_name)
#         optimized_emission = optimize_emission(weighted_average_emission, industry_lca)

#         product, created = Products.objects.update_or_create(
#             name=product_name,
#             defaults={
#                 'life_cycle_stages': life_cycle_stages,
#                 'weights': weights,
#                 'weighted_average_emission': weighted_average_emission,
#                 'optimized_emission': optimized_emission,
#             }
#         )
        
#         return Response({'weighted_average_emission': weighted_average_emission,
#                      'optimized_emission': optimized_emission})
    
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def calculate_weighted_average_emission(x_values, weights):
#     x1, x2, x3 = x_values['x1'], x_values['x2'], x_values['x3']
#     w1, w2, w3 = weights['manufacturing'], weights['use_cycle_phase'], weights['transportation']
#     weighted_sum = w1 * x1 + w2 * x2 + w3 * x3
#     total_weight = x1+x2+x3
#     weighted_average = weighted_sum / total_weight
#     return weighted_average


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products
from rest_framework import status
import json
import requests
import os
import re


import google.generativeai as genai

genai.configure(api_key='AIzaSyBSseEKOSkx9ndTBli4XWfgH0RiL9g2R10')

def fetch_life_cycle_stages(product_description, product_name):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Given a product description '{product_description}', list the main life cycle stages of the product- '{product_name}'."
    response = model.generate_content(prompt)
    return response.text


def fetch_industry_benchmark_lca(product_name):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Provide a numerical value only on the industry benchmark Life-Cycle Assessment (LCA) for the product '{product_name}'."
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
        prompt = f"Provide a numerical value only on the industry segment benchmark for products similar to '{product_name}' for the life cycle stage '{stage}'."
        response = model.generate_content(prompt)
        match = re.search(r"\d+\.?\d*", response.text)
        numerical_value = float(match.group(0)) if match else None
        x_values[stage] = numerical_value
    return x_values


def optimize_emission(weighted_average_emission, industry_lca):
    lower_bound = industry_lca * (-20 / 100)
    upper_bound = industry_lca * (20 / 100)
    if lower_bound < weighted_average_emission < upper_bound:
        return weighted_average_emission
    else:
        return max(min(weighted_average_emission, upper_bound), lower_bound)
    

def calculate_weighted_average_emission(x_values, weights):
    weighted_sum = sum(x_values[key] * weights[key] for key in x_values)
    total_weight = sum(weights.values())
    return weighted_sum / total_weight if total_weight else None


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




