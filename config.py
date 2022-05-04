#Токен бота
TOKEN = '1038330525:AAHtatdaj1wSAnDQTr5uBqdd1k9LILqe1Eo'

#Токен для получения погоды
WEATHER_TOKEN = 'bf31c42882f1947674dec4e565d46ab8'

#Адрес NSD
PATH = 'https://keystone.itsm365.com/'

#headers - нужно для правильного формирования POST и GET запросов в ITSM365
headers = {
            'Authorization': 'Basic UnVkb21hbkRTQE1PUy5QT0xVUy5HTEQ6MTIz',
            'Cookie': 'JSESSIONID=F6142A7BA1F133CF7C2AFC77DB5D8BA6'
            }

#AccessKEY - system
ACCESSKEY = '28cf9fea-605b-4aa0-937e-f56dda00f371'

#Данные для подключения к PostgreSQL
PG_DATABASE = 'd80f0uj85llbhp'
PG_USER = 'pspdigkdmeocay'
PG_PASSWORD = '20761c78ace93389b679235bfc5bf3878d2813e39ddf4ed1112b1a41241f787e'
PG_HOST = 'ec2-54-73-152-36.eu-west-1.compute.amazonaws.com'
PG_PORT = '5432'


#Токен для умного дома
TOKEN_YA = 'AQAAAAAFLtOZAAe4db-vapmss0__kWOD_XPm_7A'

#Id сценариев для умного дома
ON_TORCH = '06b1f07c-8398-43b7-a955-a6eae8e01ef9'   #включение торшера
OFF_TORCH = '4efb5db2-e2ba-44df-bfb6-1f4e5e6aacac'  #выключение торшера
ON_NIGHTLIGHT = '0c808047-75cd-4b88-bff1-0133c0e04731'   #включение ночник
OFF_NIGHTLIGHT = '3e4b7015-b8f7-4960-a28f-04dc2e62ac93'  #выключение ночник
ON_RVC = 'c69dcd35-9f2e-41e9-88dd-09f7966370cf'   #включение беляшика
OFF_RVC = 'c3fb019a-a401-4ce1-ba2d-712f2aa18648'  #выключение беляшика
ON_CHANDELIER = 'af35d472-3958-4b11-8752-c5edc371a460' #включение люстры
OFF_CHANDELIER = '77b44b3f-1b9a-47d6-ba94-90f15785f753' #выключение люстры
СHILL = '4beec2c2-f872-4849-87c1-ae129c340218' #Чиллим
IM_OUT = '1bda2834-cc62-4a76-9289-7e6cc413aed7' #Я ухожу



#Id устройств умного дома
TORCH = 'fc1cb1da-e6a6-4673-9cfa-c1d7dd7013f3'
NIGHTLIGHT = '5631b7c3-a44b-48ea-939d-b835a6a65344'
RVC = '98f2e08b-e6cd-4bf1-a9a3-edccdf1f2acf'
CHANDELIER = '22db0572-5c70-43d5-9f1d-0414724d5218'
