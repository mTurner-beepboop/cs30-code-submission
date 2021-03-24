from rest_framework import serializers
from django.utils import timezone
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


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatfileEntry
        fields = '__all__'

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

    #TODO: write update method
    def update(self, instance, valid_data):
        instance.ref_num = valid_data.pop('ref_num') #ref_number likely won't need changed

        #Get old information
        nav_info = instance.navigation_info #unlikely that navigation info will be chagned too but keep functionality
        calc_info = instance.calculation_info
        other_info = instance.other_info

        #Get new information
        nav_data = valid_data.pop('navigation_info')
        calc_data = valid_data.pop('calculation_info')
        other_data = valid_data.pop('other_info')

        #update
        nav_info.scope = nav_data['scope']
        nav_info.level_1 = nav_data['level1']
        nav_info.level_2 = nav_data['level2']
        nav_info.level_3 = nav_data['level3']
        nav_info.level_4 = nav_data['level4']
        nav_info.level_5 = nav_data['level5']

        calc_info.ef = calc_data['ef']
        calc_info.cu = calc_data['cu']

        other_info.preference = other_data['preference']
        other_info.source = other_data['source']
        other_info.last_updated = timezone.now #should default to current time

        #save
        nav_info.save()
        calc_info.save()
        other_info.save()
        instance.save()

        return instance
