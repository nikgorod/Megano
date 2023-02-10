from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from .serializers import SiteSettingsSerializer
from .models import GoodCategory, DynamicSiteSettings, Catalog, GoodTags, UserProfile, User, Specification
from .registration import *
from rest_framework.response import Response
from .forms import ReviewForm, ProfileForm, SearchForm
from .filter import *
from django.contrib import messages
from .service import AddReview, ProfileEdit, ordering_catalog


class SettingsApiView(APIView):

    def get(self, request):
        settings = DynamicSiteSettings.objects.get()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)


def site_settings(request):
    return {'site_settings': DynamicSiteSettings.load()}


class MainPage(View):
    """Главная страница сайта"""
    def get(self, request):
        good_categories = GoodCategory.objects.prefetch_related('good').filter(active_goods=True)
        favorite_categories = good_categories[:3]
        try:
            items = [Catalog.objects.select_related('good').prefetch_related('images').filter
                         (good__category_id=i.id).order_by('price')[0] for i in favorite_categories]
        except IndexError:
            items = []
        limited_edition = Catalog.objects.select_related('shop', 'good').prefetch_related('images').filter(
            limited_edition=True)[:16]
        top_goods = Catalog.objects.select_related('shop', 'good').prefetch_related('images').all().order_by('good')[:8]
        search_form = SearchForm()
        return render(request, 'app_shop/index.html', {'good_categories': good_categories,
                                                       'favorite_categories': items,
                                                       'top_goods': top_goods,
                                                       'limited_edition': limited_edition,
                                                       'search_form': search_form})


class PersonalDetailView(DetailView, LoginRequiredMixin):
    """Представление пользователя"""
    model = UserProfile
    template_name = 'app_shop/personal_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalDetailView, self).get_context_data(**kwargs)
        context['good_categories'] = GoodCategory.objects.filter(active_goods=True)
        context['search_form'] = SearchForm()
        return context


class ProfileDetailView(DetailView, LoginRequiredMixin):
    """Представление для редактирования пользователя"""
    model = UserProfile
    template_name = 'app_shop/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['profile_form'] = ProfileForm(initial={'last_name': f'{self.request.user.profile.last_name} '
                                                                    f'{self.request.user.profile.first_name} '
                                                                    f'{self.request.user.profile.middle_name}',
                                                       'tel': self.request.user.profile.tel,
                                                       'email': self.request.user.email})
        context['password_form'] = SetPasswordForm(self.request.user)
        context['good_categories'] = GoodCategory.objects.filter(active_goods=True)
        context['search_form'] = SearchForm()
        return context

    def post(self, request, pk):
        profile_form = ProfileForm(request.POST, request.FILES)
        password_form = SetPasswordForm(request.user, request.POST)
        un_valid_tel = profile_form.data.get('tel')
        valid_tel = un_valid_tel[4:7] + un_valid_tel[9:12] + un_valid_tel[13:15] + un_valid_tel[16:18]
        updated_data = request.POST.copy()
        updated_data.update({'tel': valid_tel})
        form = ProfileForm(data=updated_data, files=request.FILES, instance=self.request.user.profile)
        if form.is_valid() and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            user_profile = form.save(commit=False)
            new_avatar = form.cleaned_data['avatar']
            new_name = form.cleaned_data['last_name'].split()
            new_tel = form.cleaned_data['tel']
            new_email = form.cleaned_data['email']
            print(new_avatar)
            if new_avatar:
                ProfileEdit.avatar_edit(user_profile, new_avatar)
            username_check = ProfileEdit.username_edit(user_profile, new_name)
            tel_check = ProfileEdit.tel_edit(user_profile, new_tel)
            email_check = ProfileEdit.email_edit(user_profile, new_email)
            if not tel_check:
                messages.add_message(request, messages.INFO, 'Такой телефонный номер уже зарегистрирован!')
            elif not email_check:
                messages.add_message(request, messages.INFO, 'Такой email уже зарегистрирован!')
            elif not username_check:
                messages.add_message(request, messages.INFO, 'Неверные данные ФИО!')
            else:
                user_profile.save()
                messages.add_message(request, messages.INFO, 'Профиль успешно сохранён!')
            return redirect(reverse('profile', kwargs={'pk': pk}))
        else:
            return redirect(reverse('profile', kwargs={'pk': pk}))


class CatalogDetailView(DetailView):
    """Детальное представление товрар"""
    model = Catalog

    def get_context_data(self, **kwargs):
        context = super(CatalogDetailView, self).get_context_data(**kwargs)
        context['reviews'] = AddReview.get_list_of_reviews_at_good(self.kwargs['pk'])
        context['reviews_form'] = ReviewForm()
        context['good_categories'] = GoodCategory.objects.filter(active_goods=True)
        context['search_form'] = SearchForm()
        return context

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            AddReview.add_review_to_good(form, request, pk)
            return redirect(reverse('catalog_detail', kwargs={'pk': pk}) + '#reviews')


class CatalogListView(ListView):
    """Представление каталога по категории"""
    model = Catalog
    context_object_name = 'catalog_goods'
    template_name = 'catalog_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        ordering = ordering_catalog(self.request.GET.get('ordering'))
        if ordering:
            context['filter'] = CatalogFilter(self.request.GET, queryset=Catalog.objects.select_related('good').prefetch_related(
                'images').filter(
                good__category_id=self.kwargs['category_id']).annotate(reviews_num=Count('reviews')).order_by(ordering))
        else:
            context['filter'] = CatalogFilter(self.request.GET, queryset=Catalog.objects.select_related('good').prefetch_related(
                'images').filter(
                good__category_id=self.kwargs['category_id']))
        paginator = Paginator(context['filter'].qs, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['range_page'] = "".join(map(str, (range(1, page_obj.paginator.num_pages + 1))))
        context['good_categories'] = GoodCategory.objects.filter(active_goods=True)
        context['search_form'] = SearchForm()
        return context


class CatalogAllListView(ListView):
    """Представление каталога всех товаров"""
    model = Catalog
    context_object_name = 'catalog_goods'
    template_name = 'catalog_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogAllListView, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        form = SearchForm(self.request.GET)

        search = False

        if form.is_valid():
            qdict = form.data
            dict_ = {k: qdict.getlist(k) if len(qdict.getlist(k)) > 1 else v for k, v in qdict.items()}
            try:
                text = dict_['search'][0]
                print(text)
                context['filter'] = CatalogFilter(self.request.GET, queryset=Catalog.objects.select_related('good').
                                                  prefetch_related('images').filter(
                    good__name__icontains=text
                ))
                search = True
            except KeyError:
                context['filter'] = CatalogFilter(self.request.GET, queryset=Catalog.objects.select_related('good').
                                                  prefetch_related('images').all())

        ordering = ordering_catalog(self.request.GET.get('ordering'))
        if ordering:
            context['filter'] = CatalogFilter(self.request.GET,
                                          queryset=Catalog.objects.select_related('good').prefetch_related(
                                              'images').all().annotate(reviews_num=Count('reviews')).order_by(ordering))
        elif search is not True:
            context['filter'] = CatalogFilter(self.request.GET,
                                          queryset=Catalog.objects.select_related('good').prefetch_related(
                                              'images').all())

        paginator = Paginator(context['filter'].qs, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['range_page'] = "".join(map(str, (range(1, page_obj.paginator.num_pages + 1))))
        context['good_categories'] = GoodCategory.objects.filter(active_goods=True)
        return context
