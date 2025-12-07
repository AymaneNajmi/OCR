"""
Food-IA Source Package
"""

__version__ = '2.0.0'
__author__ = 'Food-IA Team'

from .meal_predictor import FoodRecognizer, get_recognizer, predict_meal
from .data_loader import load_food_data
from .food_model import create_food_cnn

__all__ = [
    'FoodRecognizer',
    'get_recognizer',
    'predict_meal',
    'load_food_data',
    'create_food_cnn',
]
