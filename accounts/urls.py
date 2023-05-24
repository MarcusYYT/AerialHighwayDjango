from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # path('auth/', include('django.contrib.auth.urls'))
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 这一行代码定义了一个Django路由，当用户访问api/accounts/token/时，会调用TokenObtainPairView.as_view()视图函数。
    # 这个视图函数是由django-rest-framework-simplejwt库提供的，用于处理JSON Web Token（JWT）的获取。
    # TokenObtainPairView视图函数会验证用户提供的用户名和密码，如果凭据有效，将返回一个访问令牌（access token）和一个刷新令牌（refresh token）。
    # 访问令牌用于在API请求中进行身份验证，而刷新令牌用于在访问令牌过期后获取新的访问令牌。
    # name='token_obtain_pair' 是为这个路由分配一个名字，以便在其他地方引用它。
    # 例如，在模板中，您可以使用 {% url 'token_obtain_pair' %} 来生成这个路由的URL。在Python代码中，您可以使用 reverse('token_obtain_pair') 来获得URL。
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('getuser/', views.GetUsernameView.as_view(), name='get_username')
    # path('register/', views.register, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
]