from typing import List

from django.db import models


class Allergy(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"<{self.name}>"

    @staticmethod
    def get_supported_allergies() -> List[str]:
        supported_allergies = [allergy.name for allergy in Allergy.objects.all()]
        return supported_allergies
