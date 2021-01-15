from rest_framework import serializers
from api.models import FlatfileEntry, NavigationInfo, CalculationInfo, OtherInfo

class NavigationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NavigationInfo
        fields = ('scope','level1','level2','level3','level4','level5')
    
class CalculationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CalculationInfo
        fields = ('ef','cu')

class OtherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OtherInfo
        fields = ('last_update','preference','source')
        
class ApiSerializer(serializers.ModelSerializer):
    navigation_info = NavigationSerializer(read_only=False)
    calculation_info = CalculationSerializer(read_only=False)
    other_info = OtherSerializer(read_only=False)
    
    class Meta:
        model = FlatfileEntry
        fields = "__all__"
        
    def create(self, valid_data):
        nav_data = valid_data.pop('navigation_info')
        calc_data = valid_data.pop('calculation_info')
        other_data = valid_data.pop('other_info')
        
        n = NavigationInfo.objects.create(**nav_data)
        c = CalculationInfo.objects.create(**calc_data)
        o = OtherInfo.objects.create(**other_data)
        
        entry = FlatfileEntry.objects.create(**valid_data, navigation_info=n, calculation_info=c, other_info=o)
        
        
        return entry