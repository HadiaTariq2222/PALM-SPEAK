from . import views

urlpatterns =[
    path('', views.home_page, name='home'),
    path('', views.login_page, name='login'),
    path('', views.register_page, name='register'),
    path('', views.forgot_password, name='forgetPass'),
    path('', views.reset_password, name='resetPassword'),
    path('', views.success_page, name='success'),
    path('', views.token_send_page, name='token_send'),
    path('', views.error, name='error'),
    path('', views.forgot_password, name='forgot'),
    path('', views.service, name='service'),
    path('', views.about_us, name='indAboutUs'),
    path('', views.contact_us, name='indContactUs'),
]
