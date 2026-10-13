from django import forms

JOBS = ["admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired",
        "self-employed", "services", "student", "technician", "unemployed", "unknown"]
YN = [("yes", "Yes"), ("no", "No")]


def ch(options):
    return [(o, o.capitalize()) for o in options]


class CustomerForm(forms.Form):
    age = forms.IntegerField(min_value=18, max_value=100)
    job = forms.ChoiceField(choices=ch(JOBS))
    education = forms.ChoiceField(choices=ch(["primary", "secondary", "tertiary", "unknown"]))
    balance = forms.IntegerField(label="Bank balance (€)")
    housing = forms.ChoiceField(label="Housing loan", choices=YN, widget=forms.RadioSelect, initial="no")
    loan = forms.ChoiceField(label="Personal loan", choices=YN, widget=forms.RadioSelect, initial="no")
    contact = forms.ChoiceField(label="Contact type", choices=ch(["cellular", "telephone", "unknown"]))
    campaign = forms.IntegerField(label="Contacts in this campaign", min_value=1, initial=1)
    previous = forms.IntegerField(label="Contacts in earlier campaigns", min_value=0, initial=0)
    pdays = forms.IntegerField(label="Days since last contact (-1 if never)", min_value=-1, initial=-1)
    poutcome = forms.ChoiceField(label="Earlier campaign outcome",
                                 choices=ch(["unknown", "success", "failure", "other"]))
