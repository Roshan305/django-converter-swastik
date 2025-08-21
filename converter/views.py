from django.shortcuts import render
from googletrans import Translator, LANGUAGES
from forex_python.converter import CurrencyRates, CurrencyCodes
from django.http import JsonResponse

def home(request):
    # Convert LANGUAGES dictionary to a list of tuples for the template
    languages_list = [(code, name) for code, name in LANGUAGES.items()]
    return render(request, 'converter/home.html', {
        'languages': languages_list,
    })

def translate_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        src_lang = request.POST.get('src_lang', 'auto')
        dest_lang = request.POST.get('dest_lang', 'en')
        
        translator = Translator()
        try:
            translation = translator.translate(text, src=src_lang, dest=dest_lang)
            return JsonResponse({
                'original_text': text,
                'translated_text': translation.text,
                'source_language': translation.src,
                'destination_language': translation.dest,
                'pronunciation': translation.pronunciation if translation.pronunciation else 'Not available'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def convert_currency(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 1))
        from_currency = request.POST.get('from_currency', 'USD').upper()
        to_currency = request.POST.get('to_currency', 'EUR').upper()
        
        c = CurrencyRates()
        cc = CurrencyCodes()
        
        try:
            converted_amount = c.convert(from_currency, to_currency, amount)
            from_symbol = cc.get_symbol(from_currency)
            to_symbol = cc.get_symbol(to_currency)
            
            return JsonResponse({
                'original_amount': f"{from_symbol}{amount:.2f}",
                'converted_amount': f"{to_symbol}{converted_amount:.2f}",
                'from_currency': from_currency,
                'to_currency': to_currency,
                'rate': c.get_rate(from_currency, to_currency)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)