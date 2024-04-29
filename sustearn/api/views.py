from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products
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

        product, created = Products.objects.update_or_create(
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



