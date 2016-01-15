# coding: utf-8
from datetime import date


def age(birthdate):
    today = date.today()
    years = today.year - birthdate.year - 1
    if today.month > birthdate.month or (today.month == birthdate.month and today.day >= birthdate.day):
        years += 1
    return max(0, years)
