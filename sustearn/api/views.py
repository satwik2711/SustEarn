from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products
from rest_framework import status
import json
import requests
import os

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"


def send_gemini_request(prompt):

  headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {GEMINI_API_KEY}'}
  data = {'contents': [{'parts': [{'text': prompt}]}]}

  response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)
  return response

def fetch_life_cycle_stages(product_name, product_description):
  """
  Fetches life cycle stages using Gemini's API and prompt engineering.

  Args:
      product_name: Name of the product.
      product_description: Description of the product.

  Returns:
      A list of life cycle stages or an empty list if unsuccessful.
  """

  prompt = f"Given a product description '{product_description}', identify the main life cycle stages involved in the making of '{product_name}'."

  response = send_gemini_request(prompt)
  life_cycle_stages = []
  if response.status_code == 200:
    lifecycle_data = json.loads(response.content)
    life_cycle_stages = lifecycle_data.get('contents', [])[0].get('parts', [])[0].get('generatedText', "")

  return life_cycle_stages


def fetch_industry_benchmark_lca(product_name):
    return 100  # Dummy industry benchmark LCA value

def get_x_values_from_llm(product_name, life_cycle_stages):
    return {'x1': 10, 'x2': 20, 'x3': 30}


def optimize_emission(weighted_average_emission, industry_lca):
    lower_bound = industry_lca * (-20 / 100)
    upper_bound = industry_lca * (20 / 100)
    if lower_bound < weighted_average_emission < upper_bound:
        return weighted_average_emission
    else:
        return max(min(weighted_average_emission, upper_bound), lower_bound)

@api_view(['POST'])
def calculate_footprint(request):
    try:
        product_name = request.data.get('name')
        product_description = request.data.get('description')

        life_cycle_stages = fetch_life_cycle_stages(product_name)
        weight = 1 / len(life_cycle_stages)
        weights = {stage: weight for stage in life_cycle_stages}

        if not all([product_name, product_description]):
            return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

        x_values = get_x_values_from_llm(product_name, life_cycle_stages)
        weighted_average_emission = calculate_weighted_average_emission(x_values, weights)

        #OPTIMISER FUNCTION
        industry_lca = fetch_industry_benchmark_lca(product_name)
        optimized_emission = optimize_emission(weighted_average_emission, industry_lca)

        product, created = Products.objects.update_or_create(
            name=product_name,
            defaults={
                'life_cycle_stages': life_cycle_stages,
                'weights': weights,
                'weighted_average_emission': weighted_average_emission,
                'optimized_emission': optimized_emission,
            }
        )
        
        return Response({'weighted_average_emission': weighted_average_emission,
                     'optimized_emission': optimized_emission})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def calculate_weighted_average_emission(x_values, weights):
    x1, x2, x3 = x_values['x1'], x_values['x2'], x_values['x3']
    w1, w2, w3 = weights['manufacturing'], weights['use_cycle_phase'], weights['transportation']
    weighted_sum = w1 * x1 + w2 * x2 + w3 * x3
    total_weight = x1+x2+x3
    weighted_average = weighted_sum / total_weight
    return weighted_average



