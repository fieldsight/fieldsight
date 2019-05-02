from django.core.management.base import BaseCommand
from onadata.apps.fieldsight.models import Sector


SUB_SECTOR_LIST = [
    {'AGRICULTURE, FISHING AND FORESTRY': 'Crops'},
    {'AGRICULTURE, FISHING AND FORESTRY': 'Livestock'},
    {'AGRICULTURE, FISHING AND FORESTRY': 'Irrigation and Drainage'},
    {'AGRICULTURE, FISHING AND FORESTRY': 'Agricultural Extension, Research, and Other Support Activities'},
    {'AGRICULTURE, FISHING AND FORESTRY': 'Forestry'},
    {'AGRICULTURE, FISHING AND FORESTRY': 'Fisheries'},
    {'AGRICULTURE, FISHING AND FORESTRY': 'Public Administration-Agriculture, Fishing & Forestry'},
    {'AGRICULTURE, FISHING AND FORESTRY': 'Other Agriculture, Fishing and Forestry'},
    {'EDUCATION': 'Early Childhood Education'},
    {'EDUCATION': 'Primary Education'},
    {'EDUCATION': 'Secondary Education'},
    {'EDUCATION': 'Tertiary Education'},
    {'EDUCATION': 'Workforce Development and Vocational Education'},
    {'EDUCATION': 'Adult Basic and Continuing Education'},
    {'EDUCATION': 'Public Administration-Education'},
    {'EDUCATION': 'Other Education'},
    {'ENERGY AND EXTRACTIVES': 'Mining'},
    {'ENERGY AND EXTRACTIVES': 'Oil and Gas'},
    {'ENERGY AND EXTRACTIVES': 'Renewable Energy Hydro'},
    {'ENERGY AND EXTRACTIVES': 'Renewable Energy Solar'},
    {'ENERGY AND EXTRACTIVES': 'Renewable Energy Wind'},
    {'ENERGY AND EXTRACTIVES': 'Renewable Energy Biomass'},
    {'ENERGY AND EXTRACTIVES': 'Renewable Energy Geothermal'},
    {'ENERGY AND EXTRACTIVES': 'Non-Renewable Energy Generation'},
    {'ENERGY AND EXTRACTIVES': 'Energy Transmission and Distribution'},
    {'ENERGY AND EXTRACTIVES': 'Public Administration-Energy and Extractives'},
    {'ENERGY AND EXTRACTIVES': 'Other Energy and Extractives'},
    {'ENERGY AND EXTRACTIVES': 'Law and Justice'},
    {'ENERGY AND EXTRACTIVES': 'Other Public Administration'},
    {'FINANCIAL SECTOR': 'Banking Institutions'},
    {'FINANCIAL SECTOR': 'Insurance and Pension'},
    {'FINANCIAL SECTOR': 'Capital Markets'},
    {'FINANCIAL SECTOR': 'Public Administration-Financial Sector'},
    {'FINANCIAL SECTOR': 'Other Non-bank Financial Institutions'},
    {'HEALTH': 'Health'},
    {'HEALTH': 'Health Facilities and Construction'},
    {'HEALTH': 'Public Administration-Health'},
    {'SOCIAL PROTECTION': 'Social Protection'},
    {'SOCIAL PROTECTION': 'Public Administration-Social Protection'},
    {'INDUSTRY, TRADE AND SERVICES': 'Agricultural markets, commercialization and agri-business'},
    {'INDUSTRY, TRADE AND SERVICES': 'Trade'},
    {'INDUSTRY, TRADE AND SERVICES': 'Services'},
    {'INDUSTRY, TRADE AND SERVICES': 'Manufacturing'},
    {'INDUSTRY, TRADE AND SERVICES': 'Tourism'},
    {'INDUSTRY, TRADE AND SERVICES': 'Public Administration-Industry, Trade and Services'},
    {'INDUSTRY, TRADE AND SERVICES': 'Other Industry, Trade and Services'},
    {'HOUSING': 'Housing'},
    {'HOUSING': 'Social Housing'},
    {'HOUSING': 'Housing Construction'},
    {'INFORMATION AND COMMUNICATIONS TECHNOLOGIES': 'ICT Infrastructure'},
    {'INFORMATION AND COMMUNICATIONS TECHNOLOGIES': 'ICT Services'},
    {'INFORMATION AND COMMUNICATIONS TECHNOLOGIES': 'Public Administration-Information and Communications Technologies'},
    {'INFORMATION AND COMMUNICATIONS TECHNOLOGIES': 'Other Information and Communications Technologies'},
    {'PUBLIC ADMINISTRATION': 'Central Government (Central Agencies)'},
    {'PUBLIC ADMINISTRATION': 'Sub National Government'},
    {'WATER, SANITATION AND WASTE MANAGEMENT': 'Sanitation'},
    {'WATER, SANITATION AND WASTE MANAGEMENT': 'Waste Management'},
    {'WATER, SANITATION AND WASTE MANAGEMENT': 'Water Supply'},
    {'WATER, SANITATION AND WASTE MANAGEMENT': 'Public Administration-Water, Sanitation and Waste Management'},
    {'WATER, SANITATION AND WASTE MANAGEMENT': 'Other Water Supply, Sanitation and Waste Management'},
    {'TRANSPORTATION': 'Rural and Inter-Urban Roads'},
    {'TRANSPORTATION': 'Railways'},
    {'TRANSPORTATION': 'Aviation'},
    {'TRANSPORTATION': 'Ports/Waterways'},
    {'TRANSPORTATION': 'Urban Transport'},
    {'TRANSPORTATION': 'Public Administration-Transportation'},
    {'TRANSPORTATION': 'Other Transportation'},
]


class Command(BaseCommand):
    help = 'Create sectors and respective sub-sectors'

    def handle(self, *args, **options):
        for item in SUB_SECTOR_LIST:
            sector, created = Sector.objects.get_or_create(sector=None, name=item.keys())
            sub_sector, created = Sector.objects.get_or_create(sector=sector, name=item.values())

            self.stdout.write('Successfully created Sector .. "%s"' % sector)


