from django import forms

SKIN_CHOICES = (
    ("light_1", "Light 1"),
    ("light_2", "Light 2"),
    ("medium_1", "Medium 1"),
    ("medium_2", "Medium 2"),
    ("dark_1", "Dark 1"),
    ("dark_2", "Dark 2"),
)

HAIR_CHOICES = (
    ("curly_long", "Curly Long"),
    ("curly_short", "Curly Short"),
    ("straight", "Straight"),
    ("braids", "Braids"),
    ("buzz", "Buzz Cut"),
    ("bald", "Bald"),
)

HAIR_COLOR_CHOICES = (
    ("black", "Black"),
    ("brown", "Brown"),
    ("blonde", "Blonde"),
    ("red", "Red"),
    ("auburn", "Auburn"),
)

EYES_CHOICES = (
    ("round", "Round"),
    ("almond", "Almond"),
    ("sparkly", "Sparkly"),
    ("sleepy", "Sleepy"),
    ("wide", "Wide"),
)

MOUTH_CHOICES = (
    ("smile", "Smile"),
    ("grin", "Grin"),
    ("laugh", "Laugh"),
    ("surprised", "Surprised"),
    ("neutral", "Neutral"),
)

OUTFIT_CHOICES = (
    ("hoodie_blue", "Blue Hoodie"),
    ("tee_green", "Green Tee"),
    ("uniform", "Uniform"),
    ("jacket_red", "Red Jacket"),
    ("dress_yellow", "Yellow Dress"),
)

ACCESSORY_CHOICES = (
    ("none", "None"),
    ("glasses", "Glasses"),
    ("headphones", "Headphones"),
    ("hat", "Hat"),
    ("bow", "Bow"),
)

BACKGROUND_CHOICES = (
    ("sky_blue", "Sky Blue"),
    ("sunset", "Sunset"),
    ("mint", "Mint"),
    ("lavender", "Lavender"),
    ("paper", "Paper"),
)

EXPRESSION_CHOICES = (
    ("happy", "Happy"),
    ("calm", "Calm"),
    ("excited", "Excited"),
    ("focused", "Focused"),
    ("playful", "Playful"),
)


class AvatarBuilderForm(forms.Form):
    skin = forms.ChoiceField(
        choices=SKIN_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    hair = forms.ChoiceField(
        choices=HAIR_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    hair_color = forms.ChoiceField(
        choices=HAIR_COLOR_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    eyes = forms.ChoiceField(
        choices=EYES_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    mouth = forms.ChoiceField(
        choices=MOUTH_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    outfit = forms.ChoiceField(
        choices=OUTFIT_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    accessory = forms.ChoiceField(
        choices=ACCESSORY_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    background = forms.ChoiceField(
        choices=BACKGROUND_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    expression = forms.ChoiceField(
        choices=EXPRESSION_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )

    def to_avatar_config(self):
        return {
            "skin": self.cleaned_data["skin"],
            "hair": self.cleaned_data["hair"],
            "hair_color": self.cleaned_data["hair_color"],
            "eyes": self.cleaned_data["eyes"],
            "mouth": self.cleaned_data["mouth"],
            "outfit": self.cleaned_data["outfit"],
            "accessory": self.cleaned_data["accessory"],
            "background": self.cleaned_data["background"],
            "expression": self.cleaned_data["expression"],
        }
