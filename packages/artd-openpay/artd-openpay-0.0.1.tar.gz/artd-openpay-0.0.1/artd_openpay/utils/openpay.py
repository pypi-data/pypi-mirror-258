import openpay
from artd_openpay.models import OpenPay , OpenPayCard , OpenpayCharge
from artd_partner.models import Partner
from artd_customer.models import Customer
class OpenPayUtil():
    
    __partner=None
    __production_client_id=None
    __production_client_secret=None
    __production_public_key=None

    def __init__(self, partner:Partner):
        self.__partner = OpenPay.objects.filter(partner=partner).first()
        self.__production_client_id = self.__partner.production_client_id
        self.__production_client_secret = self.__partner.production_client_secret
        self.__production_public_key = self.__partner.production_public_key
        openpay.api_key = self.__production_client_secret
        openpay.verify_ssl_certs = False
        openpay.merchant_id = self.__production_client_id
        openpay.country = 'co'
        print(self.__production_client_id , self.__production_client_secret , self.__production_public_key,sep="\n")
    
    def create_customer(self,name,last_name,email,phone_number):
        try:
            customer_count = Customer.objects.filter(email=email , phone = phone_number).count()
            if customer_count == 0:
                customer = openpay.Customer.create(
                    name=name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number
                )
                Customer.objects.create(
                    name = name,
                    last_name = last_name,
                    email = email,
                    phone = phone_number,
                    other_data  = customer,
                )
                print(customer)
            else:
                print("The customer already exists")
        except Exception as e:
            print(e)

    def get_openpay_customer(self,email,phone):
        artd_customer=Customer.objects.filter(email=email,phone=phone).first()
        print(artd_customer)
        other_data = artd_customer.other_data
        print(other_data["id"])
        customer = openpay.Customer.retrieve(other_data["id"])
        return customer , artd_customer

    def store_card(self,email,phone,card_number,holder_name,expiration_year,expiration_month,cvv2):
        customer , artd_customer = self.get_openpay_customer(email=email,phone=phone)
        print(customer)
        card = customer.cards.create(
            card_number=card_number,
            holder_name=holder_name,
            expiration_year=expiration_year,
            expiration_month=expiration_month,
            cvv2=cvv2,
        )
        OpenPayCard.objects.create(
            customer = artd_customer,
            bank_code = card["bank_code"],
            brand = card["brand"],
            card_number = card["card_number"],
            expiration_month = card["expiration_month"],
            expiration_year = card["expiration_year"],
            holder_name = card["holder_name"],
            card_id = card["id"],
            card_type = card["type"],
            other_data = card
        )

    def delete_card(self,email,phone,card_id):
        try:
            print(email,phone,sep="\n")
            customer , artd_customer = self.get_openpay_customer(email=email,phone=phone)
            card = customer.cards.retrieve(card_id)
            card.delete()
        except Exception as e:
            print(e)
        try:
            OpenPayCard.objects.filter(card_id=card_id).delete()
        except Exception as e:
            print(e)

    def create_charge(self, email ,phone , card_id ,device_session_id,amount ):
        customer , artd_customer = self.get_openpay_customer(email=email,phone=phone)
        card = OpenPayCard.objects.filter(card_id=card_id).first()
        charge = customer.charges.create(
            source_id=card_id, 
            method="card", 
            amount=amount, 
            description="Charge", 
            capture=False, 
            currency = "COP" , 
            device_session_id = device_session_id
        )
        charge.capture(merchant=False)
        OpenpayCharge.objects.create(
            card=card,
            amount=charge["amount"],
            charge_id=charge["id"],
            authorization=charge["authorization"],
            status=charge["status"],
            other_data = charge
        )
        print(charge)

    def all_customers_card(self,email,phone):
        artd_customer=Customer.objects.filter(email=email,phone=phone).first()
        customer_open_pay_id = artd_customer.other_data["id"]
        customer = openpay.Customer.retrieve(customer_open_pay_id)
        cards = customer.cards.all()
        print(cards)