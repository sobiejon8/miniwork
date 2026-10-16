from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect

ORDERS_DB = []
ADMIN_CARD = "8600 1234 5678 9012 (Sobirjon)"


def home_view(request):
    if request.session.get('is_verified'):
        full_name = request.session.get('full_name')
        phone = request.session.get('phone')

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'create_order':
                title = request.POST.get('order_title')
                desc = request.POST.get('order_desc')
                budget = float(request.POST.get('order_budget'))
                ORDERS_DB.append({
                    'title': title,
                    'description': desc,
                    'budget': budget,
                    'client_name': full_name,
                    'client_phone': phone,
                    'status': 'waiting_payment',
                    'admin_card': ADMIN_CARD,
                    'developer_name': None,
                    'developer_phone': None,
                    'project_file': None,
                    'messages': []
                })
            elif action == 'pay_order':
                order_id = int(request.POST.get('order_id'))
                if 0 <= order_id < len(ORDERS_DB):
                    ORDERS_DB[order_id]['status'] = 'open'
            elif action == 'take_order':
                order_id = int(request.POST.get('order_id'))
                if 0 <= order_id < len(ORDERS_DB):
                    ORDERS_DB[order_id]['status'] = 'in_progress'
                    ORDERS_DB[order_id]['developer_name'] = full_name
                    ORDERS_DB[order_id]['developer_phone'] = phone
            elif action == 'submit_project':
                order_id = int(request.POST.get('order_id'))
                project_link = request.POST.get('project_link')
                if 0 <= order_id < len(ORDERS_DB):
                    ORDERS_DB[order_id]['status'] = 'submitted'
                    ORDERS_DB[order_id]['project_file'] = project_link
            elif action == 'approve_project':
                order_id = int(request.POST.get('order_id'))
                if 0 <= order_id < len(ORDERS_DB):
                    budget = ORDERS_DB[order_id]['budget']
                    commission = budget * 0.10
                    dev_earnings = budget * 0.90
                    ORDERS_DB[order_id]['status'] = 'completed'
                    ORDERS_DB[order_id]['commission'] = commission
                    ORDERS_DB[order_id]['dev_earnings'] = dev_earnings
            elif action == 'send_message':
                order_id = int(request.POST.get('order_id'))
                msg_text = request.POST.get('msg_text')
                if 0 <= order_id < len(ORDERS_DB) and msg_text:
                    ORDERS_DB[order_id]['messages'].append({
                        'sender': full_name,
                        'text': msg_text
                    })

            return redirect('home')

        return render(request, 'dashboard.html', {
            'full_name': full_name,
            'phone': phone,
            'orders': ORDERS_DB
        })

    if request.method == 'POST':
        step = request.POST.get('step')
        if step == 'send_phone':
            request.session['temp_name'] = request.POST.get('full_name')
            request.session['temp_phone'] = request.POST.get('phone')
            return render(request, 'verify_sms.html', {'phone': request.session['temp_phone']})
        elif step == 'verify_code':
            code = request.POST.get('code')
            if code == '1234':
                request.session['is_verified'] = True
                request.session['full_name'] = request.session.get('temp_name')
                request.session['phone'] = request.session.get('temp_phone')
                return redirect('home')
            else:
                return render(request, 'verify_sms.html',
                              {'phone': request.session.get('temp_phone'), 'error': 'Kod xato! (Test kodi: 1234)'})

    return render(request, 'home.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
]