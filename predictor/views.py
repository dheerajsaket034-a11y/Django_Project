from django.shortcuts import render
from .forms import CustomerForm
from .ml import predict, model_accuracy
from .models import Prediction


def home(request):
    result = None
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            will, proba = predict(data)
            Prediction.objects.create(**data, probability=proba, will_subscribe=will)
            result = {"will": will, "percent": round(proba * 100, 1)}
    else:
        form = CustomerForm()
    return render(request, "predictor/home.html", {
        "form": form, "result": result,
        "history": Prediction.objects.all()[:8], "accuracy": model_accuracy()})
