from django.shortcuts import render
from .models import tehran
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import tehranserializer
import joblib
import os
import numpy as np

# مسیر مدل ML
model_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "ml_model", "rf_model.pkl"
)
model = joblib.load(model_path)

# API برای CRUD دیتابیس


class tehranAPIView(APIView):
    def get(self, request):
        tasks = tehran.objects.all()
        serializer = tehranserializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = tehranserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PredictTehranAPIView(APIView):
    # تعریف map برای Address → Avg_Price_adrs
    # عدد کلید، LabelEncoded Address است
    # مقدار، میانگین قیمت بر اساس Address
    address_avg_map = {
        0: 4000000,
        1: 5500000,
        2: 7000000,
        # ... همه کدهای Address که مدل هنگام train دیده
    }

    def post(self, request):
        data = request.data
        try:
            # محاسبه Priceـsquareـmeter
            price_per_sqm = float(data.get("Priceـsquareـmeter", 0))
            if price_per_sqm == 0:
                price_per_sqm = float(data["Price"]) / float(data["Area"])

            # گرفتن Avg_Price_adrs از map
            address_encoded = int(data["Address"])
            avg_price_by_address = self.address_avg_map.get(
                address_encoded, 0
            )  # default=0 اگر پیدا نشد

            # فقط ستون‌های train شده به مدل می‌روند
            features = np.array(
                [
                    [
                        price_per_sqm,
                        float(data["Area"]),
                        avg_price_by_address,
                        int(data["Room"]),
                    ]
                ]
            )

            # پیش‌بینی
            prediction = model.predict(features)

            return Response(
                {"predicted_price": prediction[0]}, status=status.HTTP_200_OK
            )

        except KeyError as e:
            return Response(
                {"error": f"Missing field {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
