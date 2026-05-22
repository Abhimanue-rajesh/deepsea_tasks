# from django.shortcuts import render


def dashboard_callback(request, context):

    context.update(
        {
            "temp": "temp",
        }
    )

    return context
